# Files plugin

import os
import time
import utils
from item import ItemUri


def update_db(cache_path):
    utils.run_cmd('updatedb -l 0 -U %s -o %s' % (os.path.expanduser('~/'), cache_path))

def get_cache_data_age(cache_path):
    if not os.path.exists(cache_path):
        return 0
    return time.time() - os.stat(cache_path).st_mtime

def get_matches(query):

    if not query or len(query) < 3:
        return False

    matches = []

    cache_path = utils.get_cachefile('files.cache')

    age = utils.get_cached_data_age('files')
    if age > 300 or not os.path.exists(cache_path):
        print('updating')
        update_db(cache_path)

    locate_output = utils.get_cmd_output(['locate', '-ei', '-d', cache_path, query])

    for f in locate_output.split('\n'):
        if '/.' in f:
            continue

        item = ItemUri(f)
        matches.append(item)

    return matches
