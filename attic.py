import os

try:
    import cPickle as pickle
except:
    import pickle


class Event:
    def __init__(self, query, item):
        self.time = time.time()
        self.query = query
        self.item = item

attic_path = '/home/fran/dev/sherlock/data/attic'

class Attic:

    def __init__(self):
        self.attic = dict()

        if os.path.isfile(attic_path):
            self.load()

    def load(self):
        with open(attic_path, 'rb') as f:
            self.attic = pickle.load(f)

    def save(self):
        with open(attic_path, 'wb') as f:
            pickle.dump(self.attic, f)

    def add(self, query, item):
        if not query in self.attic:
            self.attic[query] = []

        self.attic[query].append(item)

    def remove(self):
        pass

# Implement score and nearest queries!

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
