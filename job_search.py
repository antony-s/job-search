import json


class JobSearch(object):

    def __init__(self, endpoints, args):
        # Load the endpoints and add search args
        self.endpoints = [
            {'name': endpoint['name'], 'url': endpoint['url'].format(**args)}
            for endpoint in json.load(open(endpoints))
        ]
