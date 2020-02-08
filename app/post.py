from marshmallow import Schema, fields, post_load


class Post():
    def __init__(self, post):
        self.author = post.get('author')
        self.authorId = post.get('authorId')
        self.id = post.get('id')
        self.likes = post.get('likes')
        self.popularity = post.get('popularity')
        self.reads = post.get('reads')
        self.tags = post.get('tags')

    def __repr__(self):
        return f'<Post ({self.author}, {self.id})>'


class PostSchema(Schema):
    author = fields.Str()
    authorId = fields.Integer()
    id = fields.Integer()
    likes = fields.Integer()
    popularity = fields.Number()
    reads = fields.Integer()
    tags = fields.List(fields.Str())

    @post_load
    def make_post(self, data, **kwargs):
        return Post(data)