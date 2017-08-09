# Files plugin

import os
from sherlock import utils
from sherlock import cache
from sherlock import config
from sherlock.items import Item

exclude = ('.git', '.svn')

include_dirs = config.files_include
include_extensions = config.files_include_extensions


def update_cache():

    files = []

    home = os.path.expanduser('~')

    for fname in os.listdir(home):

        if fname in exclude or fname.startswith('.') or '/.' in fname:
            continue

        path = os.path.join(home, fname)

        if os.path.isdir(path):
            files.append(
                Item(text=fname, subtext=path, category='dir', keys=fname, arg=path)
            )
        else:
            files.append(
                Item(text=fname, subtext=path, category='file', keys=fname, arg=path)
            )

    for dirname in include_dirs:

        for root, dirnames, filenames in os.walk(os.path.expanduser(dirname)):

            if root in exclude or root.startswith('.') or '/.' in root:
                continue

            if dirnames and len(dirnames) > 1:
                dirnames = sorted(dirnames, key=lambda x: os.stat(os.path.join(root, x)).st_ino)

            for i, dn in enumerate(dirnames):
                if dn.startswith('.') or dn in exclude:
                    del dirnames[i]
                    continue

                path =  os.path.join(root, dn)

                files.append(
                    Item(text=dn, subtext=path, category='dir', keys=dn, arg=path)
                )

            for fn in filenames:
                if fn.startswith('.') or fn in exclude:
                    continue

                if '.' in fn and fn[fn.index('.'):] not in include_extensions:
                    continue

                path = os.path.join(root, fn)

                files.append(
                    Item(text=fn, subtext=path, category='file', keys=fn, arg=path)
                )

    cache.cache_data('files', files)
    return

def get_items():

    _cached_files = cache.get_cached_data('files')

    for f in _cached_files:
        yield f
