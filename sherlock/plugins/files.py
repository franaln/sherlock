# Files plugin

import os
from sherlock import utils
from sherlock import cache
from sherlock import config
from sherlock.items import ItemUri

exclude = ('.git', '.svn')
include_ext = config.include_ext

files = None

def _get_files():

    _files = []

    home = os.path.expanduser('~')

    for fname in os.listdir(home):

        if fname in exclude or fname.startswith('.') or '/.' in fname:
            continue

        _files.append(ItemUri(fname, os.path.join(home, fname)))


    for dirname in config.include_files:

        for root, dirnames, filenames in os.walk(os.path.expanduser(dirname)):

            if root in exclude or root.startswith('.') or '/.' in root:
                continue

            if dirnames and len(dirnames) > 1:
                dirnames = sorted(dirnames, key=lambda x: os.stat(os.path.join(root, x)).st_ino)

            for i, dn in enumerate(dirnames):
                if dn.startswith('.') or dn in exclude:
                    del dirnames[i]
                    continue

                _files.append(ItemUri(dn, os.path.join(root, dn)))

            for fn in filenames:
                if fn.startswith('.') or fn in exclude:
                    continue

                if '.' in fn and fn[fn.index('.'):] not in include_ext:
                    continue

                _files.append(ItemUri(fn, os.path.join(root, fn)))

    return _files

def get_matches(query):

    global files

    if files is None:
        files = cache.get_cached_data('files', _get_files, max_age=1000)

    for f in files:
        yield f
