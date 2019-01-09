#!/usr/bin/env python

import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

import requests


def format_date(str):
    return datetime.strptime(str, '%Y-%m-%dT%H:%M:%SZ').isoformat().split('T')[0]


def make_data(data):
    subtitle = "{} updated / {} created".format(format_date(data['last_edited_date']), format_date(data['created_date']))
    url = "https://paper.dropbox.com/doc/{}".format(data['doc_id'])
    return {
        'uid': data['doc_id'],
        'title': data['title'],
        'subtitle': subtitle,
        'arg': url,
        'autocomplete': data['title']
    }


query = sys.argv[1]
token = os.environ['token']
url = 'https://api.dropboxapi.com/2/paper/docs/search'
limit = 100
data = {'query': query, 'limit': limit}
headers = {
    'content-type': 'application/json',
    'Authorization': "Bearer {}".format(token)
}
r = requests.post(url, headers=headers, data=json.dumps(data))
data = map(make_data, r.json()['docs'])
sys.stdout.write(json.dumps({'items': data}))
