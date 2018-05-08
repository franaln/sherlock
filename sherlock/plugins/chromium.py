import os
import re
import json
import sqlite3

from sherlock import utils, cache
from sherlock.items import Item

bookmarks_file = os.path.expanduser('~/.config/chromium/Default/Bookmarks')
history_file = os.path.expanduser('~/.config/chromium/Default/History')

def _get_bookmarks(node):
    if 'url' in node:
        if not re.match("javascript:", node['url']):
            yield node
    elif 'children' in node:
        for n in node['children']:
            yield from _get_bookmarks(n)
    else:
        yield None

def get_bookmarks():

    with open(bookmarks_file) as f:
        content = json.loads(f.read())

    bookmarks = []
    for n in _get_bookmarks(content['roots']['bookmark_bar']):
        if n is not None:
            name, url = n['name'], n['url']
            bookmarks.append(
                Item(text=name,
                    subtext=url,
                    keys=[name,],
                    category='url',
                    arg=url)
            )

    for n in _get_bookmarks(content['roots']['other']):
        if n is not None:
            name, url = n['name'], n['url']
            bookmarks.append(
                Item(text=name,
                    subtext=url,
                    keys=[name,],
                    category='url',
                    arg=url)
            )

    return bookmarks


def get_history():

    tmp_history_file = os.path.join('/tmp', 'History')

    utils.copy_file(history_file, tmp_history_file)

    conn = sqlite3.connect(os.path.expanduser(tmp_history_file))
    c = conn.cursor()

    result = c.execute('SELECT datetime(last_visit_time/1000000-11644473600, "unixepoch") as last_visited, last_visit_time, url , title, visit_count FROM urls;')

    history = []
    # for row in result:
    #     last_visited, last_visit_time, url , name, visit_count = row

    for last_visited, last_visit_time, url , name, visit_count in result:

        if visit_count < 10:
            continue

        it = Item(
            text=name,
            subtext=url,
            keys=[name,],
            category='url',
            arg=url)

        if not it in history:
            history.append(it)

    return history

def get_bookmarks_and_history():
    return (get_bookmarks() + get_history())

def update_cache():
    cache.cache_data('chromium', get_bookmarks_and_history())

def get_items():
    for item in cache.get_cached_data('chromium'):
        yield item
