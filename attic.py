import os
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle

import config
import utils
from items import Item

attic_path = os.path.join(config.cache_dir, 'attic')
history_size = 100

class Attic:

    def __init__(self):
        if os.path.isfile(attic_path):
            self.load()
        else:
            self.events = []
            self.attic = dict()

        self.pos = -1

    def load(self):
        with open(attic_path, 'rb') as f:
            self.events = pickle.load(f)
            self.attic  = pickle.load(f)

    def save(self):
        with open(attic_path, 'wb') as f:
            pickle.dump(self.events, f)
            pickle.dump(self.attic, f)

    def add(self, query, item, action):

        timestamp = datetime.now()
        item_dict = item.to_dict()

        event = (timestamp, query, item_dict, action)

        self.events.insert(0, event)

        if len(self.events) > history_size:
            del self.events[history_size:]

        if not query in self.attic:
            self.attic[query] = []

        for n, it in enumerate(self.attic[query]):
            if it[0] == item_dict:
                self.attic[query][n][1] += 1
                break
        else:
            self.attic[query].append([item_dict, 1])

    def remove(self):
        pass

    def get_query(self):
        self.pos += 1
        if self.pos >= len(self.events):
            return None
        return self.events[self.pos][1]

    def sort(self, query, items):

        if query not in self.attic:
            return

        total = 0
        for b in self.attic[query]:
            total += b[1]

        for sitem, count in self.attic[query]:
            for item in items:
                if item == sitem:
                    item.score *= sitem[1]/total

    def get_similar(self, query):

        similar_items = []

        for q in self.attic.keys():

            if q == query:
                continue

            d = utils.distance(query,q)

            if d < 2:
                items = self.attic[q]

                similar_items.extend([Item.from_dict(i[0]) for i in items])

        return similar_items
