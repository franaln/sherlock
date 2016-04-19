import os
import logging
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle

from sherlock import utils
from sherlock.items import Item

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
        self.changed = False

    def load(self):
        self.logger.info('loading attic')
        with open(self.path, 'rb') as f:
            try:
                self.events = pickle.load(f)
                self.attic  = pickle.load(f)
            except:
                # backup file for now
                utils.copy_file(self.path, self.path+'.backup')
                self.events = []
                self.attic = dict()

    def save(self):
        if not self.changed:
            return
        self.logger.info('saving attic')
        with open(self.path, 'wb') as f:
            pickle.dump(self.events, f)
            pickle.dump(self.attic, f)

    def add(self, query, item, action):

        self.logger.info('adding query=%s, item=%s, action=%s to the attic' % (query, item, action))

        timestamp = datetime.now()
        item_dict = item.to_dict()

        # add event to history
        event = (timestamp, query, item_dict, action)

        self.events.insert(0, event)

        if len(self.events) > history_size:
            del self.events[history_size:]

        # add to attic histogram
        if not item.title in self.attic:
            self.attic[item.title] = 1
        else:
            self.attic[item.title] += 1

        self.changed = True

    def remove(self):
        self.changed = True

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

    def get_total_score(self):
        total = 0
        for b in self.attic.values:
            total += b
        return total

    def get_item_bonus(self, item):
        return self.attic.get(item.title, -1)

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
