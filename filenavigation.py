# File navigation

import os
from item import Item
import utils

def get_matches(query):

    query = os.path.expanduser(query)

    idx = query.rfind('/')

    if idx >= 0:
        path = query[:idx+1]
        query = query[idx+1:]
    else:
        path = query
        query = ''

    path_content = os.listdir(path)

    items  = []
    for p in path_content:

        if p.startswith('.'):
            continue

        abspath = os.path.join(path, p)

        if os.path.isdir(abspath):
            #title = '%s/' % p
            abspath += '/'
        #else:
        title = p

        subtitle = abspath

        it = Item(title, subtitle)

        items.append(it)


    if query:
        return [m for m in utils.filter(query, items, key=lambda m: m.title)]

    return items
