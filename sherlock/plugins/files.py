# Files plugin

import os
from sherlock import utils
from sherlock import cache
from sherlock import config
from sherlock.items import ItemUri

exclude = ('.git', '.svn')

files = None

def _get_files():

    _files = []

    home = os.path.expanduser('~')

    for dirname in config.files_include:

        for root, dirnames, filenames in os.walk(os.path.expanduser(dirname)):

            if root in exclude or root.startswith('.') or '/.' in root:
                continue

            for i, dn in enumerate(dirnames):
                if dn.startswith('.') or dn in exclude:
                    del dirnames[i]
                    continue

                _files.append(ItemUri(os.path.join(root, dn)))

            for fn in filenames:
                if fn.startswith('.') or fn in exclude:
                    continue

                _files.append(ItemUri(os.path.join(root, fn)))

    return _files

def get_matches(query):

    global files

    if files is None:
        files = cache.get_cached_data('files', _get_files, max_age=1000)
    #cmd = ['locate', '-i', '-n', '1000', '-q', '-e', '-r', query]
    #files = [ ItemUri(i) for i in utils.get_cmd_output(cmd).split('\n')]

    return files
