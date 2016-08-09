import pickle
from StringIO import StringIO
import unittest

import feedparser
from mock import patch

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


class TestFeedParsing(unittest.TestCase):

    def setUp(self):
        # Sample feed data
        self.feed_1 = feedparser.parse('tests/example_feed_1.xml')
        self.feed_2 = feedparser.parse('tests/example_feed_2.xml')
        self.endpoint_args = {
            'search_term': 'python',
            'location': 'leeds',
            'distance': 5
        }
        self.job_search = JobSearch('tests/endpoints.json', self.endpoint_args)

    def test_merge_feeds(self):
        self.job_search.feeds = [self.feed_1, self.feed_2]
        self.job_search.merge_feeds()
        self.assertListEqual(
            pickle.load(open('tests/merged_feeds.pkl')),
            self.job_search.merged_feeds
        )

    @patch.object(feedparser, 'parse')
    def test_fetch_feeds(self, mock_parse):
        mock_parse.side_effect = [self.feed_1, self.feed_2]
        # Check `feeds` is empty
        self.assertListEqual([], self.job_search.feeds)
        self.job_search.fetch_feeds()
        # test `feeds` is populated after call to `fetch_feeds`
        self.assertListEqual([self.feed_1, self.feed_2], self.job_search.feeds)

    @patch('sys.stdout', new_callable=StringIO)
    def test_feed_display(self, mock_stdout):
        self.job_search.feeds = [self.feed_1, self.feed_2]
        self.job_search.merge_feeds()
        self.job_search.display_feeds()
        self.assertEqual(
            mock_stdout.getvalue(),
            open('tests/feed_output.txt', 'r').read()
        )
