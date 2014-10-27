# Files plugin

import os
import utils
from items import ItemUri

exclude = ('.git', '.svn')

files = None

def _get_files():

    _files = []

    for root, dirnames, filenames in os.walk("/home/fran"):

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
        files = utils.get_cached_data('files', _get_files, max_age=1000)

    return files
