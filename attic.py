import os
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle

import utils
from items import Item

history_size = 100

class Attic:

    def __init__(self, path):
        self.path = path
        if os.path.isfile(self.path):
            self.load()
        else:
            self.events = []
            self.attic = dict()

        self.pos = len(self.events)

    def load(self):
        with open(self.path, 'rb') as f:
            self.events = pickle.load(f)
            self.attic  = pickle.load(f)

    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.events, f)
            pickle.dump(self.attic, f)

    def add(self, query, item, action):

        if item.category == 'text':
            return

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

            d = utils.distance(query, q)

            if d < 2:
                items = self.attic[q]

                similar_items.extend([Item.from_dict(i[0]) for i in items])

        return similar_items
