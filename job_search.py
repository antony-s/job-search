import json

import feedparser


class JobSearch(object):

    def __init__(self, endpoints, args):
        # Load the endpoints and add search args
        self.endpoints = [
            {'name': endpoint['name'], 'url': endpoint['url'].format(**args)}
            for endpoint in json.load(open(endpoints))
        ]
        self.feeds = []
        self.merged_feeds = []

    def merge_feeds(self):
        self.merged_feeds = [
            entry for feed in self.feeds for entry in feed['entries']
        ]
        # Sort by latest date first
        self.merged_feeds.sort(
            key=lambda feed: feed['published_parsed'], reverse=True
        )

    def fetch_feeds(self):
        self.feeds = [
            feedparser.parse(endpoint['url']) for endpoint in self.endpoints
        ]

    def display_feeds(self):
        for feed in self.merged_feeds:
            print 'Title: {}'.format(feed.title)
            print 'Company: {}'.format(feed.author)
            print 'Summary: {}'.format(feed.summary)
            print 'Link(s): {}'.format(
                ' '.join([link.href for link in feed.links])
            )
            print '---'
