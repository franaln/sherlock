import os
import json
import re

from sherlock import cache
from sherlock.items import ItemUrl

def get_bookmarks(node):
    if 'url' in node:
        if not re.match("javascript:", node['url']):
            yield node
    elif 'children' in node:
        for n in node['children']:
            yield from get_bookmarks(n)
    else:
        yield None

def update_cache():

    with open(os.path.expanduser('~/.config/chromium/Default/Bookmarks')) as f:
        content = json.loads(f.read())

    bookmarks = []
    for n in get_bookmarks(content['roots']['bookmark_bar']):
        if n is not None:
            bookmarks.append(ItemUrl(n['name'], n['url']))

    cache.cache_data('bookmarks', bookmarks)


def get_items():

    for bookmark in cache.get_cached_data('bookmarks'):
        yield bookmark
