from flask import Flask, jsonify, request, make_response
import requests
from app.post import Post, PostSchema
from operator import attrgetter
from pprint import pprint
import time, json
from threading import Thread
import queue
import requests_cache

app = Flask(__name__)
requests_cache.install_cache('api_cache',
                             backend='sqlite',
                             expire_after=2 * 60)


# Route 1
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify(success=True), 200


# Route 2
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Get URL arguements to pass along
    tags = request.args.get('tags')

    # Set default if arg is None
    sortBy = request.args.get('sortBy') or 'id'

    # Validate args too.
    if sortBy not in ['id', 'reads', 'likes', 'popularity']:
        return jsonify(error="sortBy parameter is invalid"), 400

    direction = request.args.get('direction') or 'asc'
    if direction not in ['asc', 'desc']:
        return jsonify(error="direction parameter is invalid"), 400

    # Set boolean direction for easier sorting later
    direction = True if direction == 'desc' else False

    schema = PostSchema(many=True)
    if tags is None:
        # Need to specify at least one tag
        return jsonify(error="Tags parameter is required"), 400
    else:
        tags = tags.split(',')

        urls = []
        API_HOST = ''
        for tag in tags:
            # Make URLs
            urls.append(API_HOST + "posts?tag=" + tag)

        # Create a thread for each unique tag request to API
        # Save results of each thread to queue
        que = queue.Queue()
        threads = [
            Thread(target=lambda q, url: q.put(fetch_post(url)),
                   args=(que, url)) for url in urls
        ]
        for thread in threads:
            thread.start()
            # This is silly. The threads may finish at different times, causing
            # the final results to be not in the order the tags were provided.
            # So, space out the calls a bit.
            time.sleep(0.07)
        for thread in threads:
            thread.join()

        # Get application-definition of all posts
        posts = []
        while not que.empty():
            posts.extend(schema.load(que.get()))

        # only collect unique ids
        all_posts = {}
        for post in posts:
            all_posts.setdefault(post.id, post)

        # Turn to list so we can sort.
        all_posts = list(all_posts.values())

        # Sort
        all_posts.sort(key=attrgetter(sortBy), reverse=direction)

        # Serialize and return
        result = schema.dump(all_posts)
        return jsonify(posts=result), 200


def fetch_post(url):
    posts_json = requests.get(url).json().get('posts')
    return posts_json


if __name__ == "main":
    app.run()