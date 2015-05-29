import os
import logging
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle

import utils
from items import Item

history_size = 100

def distance(str1, str2):
    """ return the Levenshtein distance
    between two strings """

    d = dict()
    for i in range(len(str1)+1):
        d[i] = dict()
        d[i][0] = i

    for i in range(len(str2)+1):
        d[0][i] = i

    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1,
                          d[i-1][j-1]+(not str1[i-1] == str2[j-1]))

    return d[len(str1)][len(str2)]

class Attic:

    def __init__(self, path):

        self.logger = logging.getLogger(__name__)

        self.path = path

        if os.path.isfile(self.path):
            self.load()
        else:
            self.events = []
            self.attic = dict()

        self.pos = len(self.events)

    def load(self):
        self.logger.info('loading attic')
        with open(self.path, 'rb') as f:
            self.events = pickle.load(f)
            self.attic  = pickle.load(f)

    def save(self):
        self.logger.info('saving attic')
        with open(self.path, 'wb') as f:
            pickle.dump(self.events, f)
            pickle.dump(self.attic, f)

    def add(self, query, item, action):

        # if item.category == 'text':
        #     return

        self.logger.info('adding query=%s, item=%s, action=%s to the attic' % (query, item, action))

        timestamp = datetime.now()
        item_dict = item.to_dict()

        event = (timestamp, query, item_dict, action)

        self.events.insert(0, event)

        if len(self.events) > history_size:
            del self.events[history_size:]

        if not query in self.attic:
            self.attic[query] = []

        for n, it in enumerate(self.attic[query]):
            if it[0]['title'] == item_dict['title']:
                self.attic[query][n][1] += 1
                break
        else:
            self.attic[query].append([item_dict, 1])

    def remove(self):
        pass

    def get_next_query(self):
        self.pos += 1
        if self.pos >= len(self.events):
            self.pos = len(self.events)
            return None
        return self.events[self.pos][1]

    def get_previous_query(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
            return None
        return self.events[self.pos][1]

    def get_history(self):
        return [ Item.from_dict(ev[2]) for ev in self.events ]

    def sort(self, query, items):

        if query not in self.attic:
            return

        total = 0
        for b in self.attic[query]:
            total += b[1]

        for item in items:
            for sitem, count in self.attic[query]:
                if item.title == sitem['title']:
                    item.score *= count/total

                else:
                    item.score *= 1/total

    def get_similar(self, query):

        similar_items = []

        for q in self.attic.keys():

            if q == query:
                continue

            d = distance(query, q)

            if d < 2:
                items = self.attic[q]

                similar_items.extend([Item.from_dict(i[0]) for i in items])

        return similar_items
