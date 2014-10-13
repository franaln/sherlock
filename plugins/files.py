# Files plugin

import os
import utils
from items import ItemUri

def _get_files():
    files = []

    for root, dirnames, filenames in os.walk("/home/fran/Dropbox"):
        for fn in filenames+dirnames:
            path = os.path.join(root, fn)

            if '/.' in path:
                continue

            item = ItemUri(path)
            files.append(item)

    return files


def get_matches(query):

    return utils.get_cached_data('files', _get_files, max_age=1000)
