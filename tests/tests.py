import unittest

from job_search import JobSearch


class TestFeedEndpoints(unittest.TestCase):

    def setUp(self):
        self.endpoints = [
            {
                'name': 'Feed 1',
                'url': 'example.com/feed_1?'
                        'search_term=python'
                        '&location=leeds'
                        '&distance=5'
            },
            {
                'name': 'Feed 2',
                'url': 'example.com/feed_2?'
                        'search_term=python'
                        '&location=leeds'
                        '&distance=5'
            }
        ]
        self.endpoint_args = {
            'search_term': 'python',
            'location': 'leeds',
            'distance': 5
        }
        self.job_search = JobSearch('tests/endpoints.json', self.endpoint_args)

    def test_endpoints_loaded(self):
        self.assertListEqual(self.endpoints, self.job_search.endpoints)
