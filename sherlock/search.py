import os
import re
import time
import string
import logging
import threading
import queue

from gi.repository import GObject

from sherlock import items

# Anchor characters in a name
INITIALS = string.ascii_uppercase + string.digits

# Split on non-letters, numbers
split_on_delimiters = re.compile('[^a-zA-Z0-9]').split

def get_matches(plugin, query, min_score=0, max_results=0):

    """ search filter.
    Returns list of items that match query.
    """

    results = [] #dict()

    if not query:
        return []

    query = query.lower()
    querylen = len(query)
    queryset = set(query)

    # Loop over items
    for i, item in enumerate(plugin.get_matches(query)):

        item.score = 0.

        if item.no_filter or not item.keys:
            item.score = 100.0

        for value in item.keys:

            score = 0
            valuelen = len(value)
            valuelow = value.lower()

            # pre-filter any items that do not contain all characters of 'query'
            # to save on running several more expensive tests
            if not queryset <= set(valuelow):
                continue

            # item starts with query (case-insensitive)
            if valuelow.startswith(query) or valuelow.endswith(query):
                score = 100.0 - 2 * (valuelen / querylen)

            if not score:
                # query matches capitalised letters in item,
                # e.g. of = OmniFocus
                initials = ''.join([c for c in value if c in INITIALS])
                leninitials = len(initials)
                if initials.lower().startswith(query):
                    score = 98.0 - (leninitials / querylen)

            if not score:
                # split the item into "atoms", i.e. words separated by
                # spaces or other non-word characters
                atoms = [s.lower() for s in split_on_delimiters(value)]
                # print('atoms : %s  -->  %s' % (value, atoms))
                # initials of the atoms
                initials = ''.join([s[0] for s in atoms if s])

                # is 'query' one of the atoms in item?
                # similar to substring, but scores more highly, as it's
                # a word within the item
                if query in atoms:
                    score = 96.0 - (valuelen / querylen)

            if not score:
                # 'query' matches start (or all) of the initials of the
                # atoms, e.g. 'himym' matches 'How I Met Your Mother'
                # *and* 'how i met your mother' (the capitals rule only
                # matches the former)
                if initials.startswith(query):
                    score = 94.0 - (leninitials / querylen)

                # 'query' is a substring of initials, e.g. 'doh' matches
                # 'The Dukes of Hazzard'
                elif query in initials:
                    score = 92.0 - (leninitials / querylen)

            if not score:
                # 'query' is a substring of item
                if query in value.lower():
                    score = 92.0 - (valuelen / querylen)

            if min_score and score < min_score:
                continue

            if score > 0 and score > item.score:
                # use "reversed" score (i.e. highest becomes lowest) and
                # value as sort key. This means items with the same score
                # will be sorted in alphabetical not reverse alphabetical order
                #results[(100.0 / score, value.lower(), i)] = (item, round(score, 2))
                item.score = round(score, 2)
                # if isinstance(item, items.ItemUri):
                #     results[(100.0/score, time.time() - os.path.getmtime(item.subtitle), value.lower(), i)] = item
                # else:
                #     results[(100.0/score, value.lower(), i)] = item

                # if isinstance(item, items.ItemUri):
                #     import datetime
                #     time_penalty = datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.fromtimestamp(os.path.getmtime(item.subtitle))
                #     item.score -= time_penalty.days if time_penalty.days < 100 else 100

        if item.score > min_score:
            results.append(item)

    # sort on keys, then discard the keys
    #keys = sorted(results.keys(), reverse=False)
    #results = [results.get(k) for k in keys]

    if max_results and len(results) > max_results:
        results = results[:max_results]

    # return list of ordered items
    return results


class SearchWorker:

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.logger.info('starting search worker')

        self.task_id = 0
        self.queue = queue.Queue(maxsize=100)

        for _ in range(4):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):

        for id_, done, plugin, query in iter(self.queue.get, None):
            result = []
            try:
                plugin_matches = get_matches(plugin, query, min_score=60.0, max_results=50)
                result.extend(plugin_matches)
            except IOError:
                pass

            # signal task completion; run done() in the main thread
            GObject.idle_add(done, id_, query, result)

    def add_job(self, callback, plugin, query):
        # executed in the main thread
        self.task_id += 1
        self.queue.put((self.task_id, callback, plugin, query))
        return self.task_id
