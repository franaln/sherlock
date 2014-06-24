import os
from datetime import datetime

try:
    import cPickle as pickle
except:
    import pickle


# class Event:
#     def __init__(self, query, item):
#         self.time = time.time()
#         self.query = query
#         self.item = item

attic_path = '/home/fran/dev/sherlock/data/attic'

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

    def add(self, query, item):

        if item.category == 'text':
            return

        timestamp = datetime.now()
        event = (timestamp, query, item)

        self.events.insert(0, event)

        if not query in self.attic:
            self.attic[query] = dict()

        for it, count in self.attic[query].items():

            if it == item:
                count += 1
                break
        else:
            self.attic[query][item] = 0

        self.attic[query][item] += 1

    def remove(self):
        pass

    def get_last(self):
        return self.attic

        # Implement score and nearest queries!

    def analise(self):
        pass


# attic[query] = [
#     item_id: count,
#     item_id: count,
# ]

# cada value del dict es un histograma de counts vs items normalizados a 100%

# si no tienen score les asigno este...

# si tienen

#        filter   attic
# item1  80%        80% ->  80%
# item2  50%        20% -> 100%
