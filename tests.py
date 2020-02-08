import unittest, requests, json
from app import app
from app.post import Post


class APITestCase(unittest.TestCase):
    def setUp(self):
        # Get test app
        self.app = app.test_client()
        self.app.testing = True

    def get_expected_result(self, file):
        # Get expected result
        exp_result = ''
        with open(file) as json_file:
            exp_result = json.load(json_file)
        return exp_result

    def testPing(self):
        '''Test /api/ping route
        '''
        expected = self.get_expected_result('test_data/good_ping.json')
        actual = self.app.get('/api/ping')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('success'),
                         expected.get('success'))

    def testNoTagRequest(self):
        '''Test /api/posts route with no tags
        '''
        expected = self.get_expected_result('test_data/no_tag.json')
        actual = self.app.get('/api/posts')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('error'), expected.get('error'))

    def testInvalidTagRequest(self):
        '''Test /api/posts route with no tags
        '''
        expected = {"posts": [], "status_code": 200}
        actual = self.app.get('/api/posts?tags=invalid')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('posts'), expected.get('posts'))

    def testBadSortRequest(self):
        '''Test /api/posts route with bad sortBy query param
        '''
        expected = self.get_expected_result('test_data/bad_sortBy.json')
        actual = self.app.get('/api/posts?tag=tech&sortBy=invalid')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('error'), expected.get('error'))

    def testBadDirectionRequest(self):
        '''Test /api/posts route with bad direction query param
        '''
        expected = self.get_expected_result('test_data/bad_direction.json')
        actual = self.app.get('/api/posts?tag=tech&direction=invalid')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('error'), expected.get('error'))

    def testOneTag(self):
        '''Test /api/ping route with one valid tag
        '''
        expected = self.get_expected_result('test_data/one_tag.json')
        actual = self.app.get('/api/posts?tags=tech')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('posts'), expected.get('posts'))

    def testTwoTags(self):
        '''Test /api/ping route with two valid tags with default args
        '''
        expected = self.get_expected_result('test_data/two_tags.json')
        actual = self.app.get('/api/posts?tags=history,health')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('posts'), expected.get('posts'))

    def testTwoTagsSortAsc(self):
        '''Test /api/ping route fully, ascending
        '''
        expected = self.get_expected_result('test_data/tags_sort_asc.json')
        actual = self.app.get(
            '/api/posts?tags=tech,history&sortBy=reads&direction=asc')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('posts'), expected.get('posts'))

    def testTwoTagsSortDesc(self):
        '''Test /api/ping route fully, descending
        '''
        expected = self.get_expected_result('test_data/tags_sort_desc.json')
        actual = self.app.get(
            '/api/posts?tags=science,history&sortBy=popularity&direction=desc')

        self.assertEqual(actual.status_code, expected.get('status_code'))
        self.assertEqual(actual.get_json().get('posts'), expected.get('posts'))


if __name__ == "__main__":
    unittest.main(verbosity=2)