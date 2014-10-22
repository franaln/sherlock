# Files plugin

import os
import utils
from items import ItemUri

exclude = ('.git', '.svn')

def _get_files():
    files = []

    for root, dirnames, filenames in os.walk("/home/fran/Dropbox"):

        if root in exclude or root.startswith('.'):
            continue

        for i, dn in enumerate(dirnames):
            if dn.startswith('.') or dn in exclude:
                del dirnames[i]
                continue

            files.append(ItemUri(os.path.join(root, dn)))

        for fn in filenames:
            if fn.startswith('.') or fn in exclude:
                continue

            files.append(ItemUri(os.path.join(root, fn)))

    return files


files = utils.get_cached_data('files', _get_files, max_age=1000)

def get_matches(query):

    return files
