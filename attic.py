import os
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle

attic_path = '/home/fran/dev/sherlock/data/attic'
history_size = 100

class Attic:

    def __init__(self):
        self.events = []
        self.attic = dict()

        if os.path.isfile(attic_path):
            self.load()

    def load(self):
        with open(attic_path, 'rb') as f:
            self.events = pickle.load(f)
            self.attic  = pickle.load(f)

    def save(self):
        with open(attic_path, 'wb') as f:
            pickle.dump(self.events, f)
            pickle.dump(self.attic, f)

    def add(self, query, item, action):

        # if item.category == 'text':
        #     return

        timestamp = datetime.now()

        event = (timestamp, query, item.to_dict(), action)

        self.events.insert(0, event)

        if len(self.events) > history_size:
            del self.events[history_size:]

        # if not query in self.attic:
        #     self.attic[query] = dict()

        # for it, count in self.attic[query].items():

        #     if it == item:
        #         count += 1
        #         break
        # else:
        #     self.attic[query][item] = 0

        # self.attic[query][item] += 1

    def remove(self):
        pass

    def get_item_history(self):
        for event in self.events:
            yield event[2]

    def get_query_history(self):
        for event in self.events:
            yield event[1]


        # Implement score and nearest queries!

    def analise(self):
        pass
