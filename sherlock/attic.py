import os
import json
import logging
from datetime import datetime
from gi.repository import GLib

from sherlock import utils

history_size = 100

class Attic:

    def __init__(self, path):

        self.logger = logging.getLogger(__name__)

        self.path = path

        if os.path.isfile(self.path):
            self.load()
        else:
            self.events  = []  # Event: (date, query, match, action, score)

        # create bonus dict
        self.bonus = dict()
        for event in self.events:
            item = event[2]
            title = item['text']
            if not title in self.bonus:
                self.bonus[title] = 1
            else:
                self.bonus[title] += 1

        # self.pos = -1
        self.changed = False
        GLib.timeout_add_seconds(1800, self.save)


    def load(self):
        self.logger.info('loading attic from %s' % self.path)
        with open(self.path, 'r') as f:
            try:
                self.events = json.loads(f.read())
            except:
                # backup file for now
                utils.copy_file(self.path, self.path+'.backup')
                self.events = []


    def save(self):
        if not self.changed:
            return
        self.logger.info('saving events')
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.events))
        self.changed = False
        # self.logger.info('saving history')
        # with open(self.history_path, 'w') as f:
        #     f.write(json.dumps(self.history))
        return True


    def add(self, query, item, action):

        if not query:
            return

        self.logger.info('adding event to attic: query=%s, item=%s, action=%s' % (query, item, action))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # add event to history
        item_to_save = { key: value for key, value in item.items() if key not in ('score', 'bonus') }

        event = (timestamp, query, item_to_save, action, item.get('score', 0.0))

        self.events.insert(0, event)

        # if len(self.history) > history_size:
        #     del self.history[history_size:]

        self.save()
        #self.changed = True


    def remove(self):
        self.changed = True


    def get_next_query(self):
        pass
        # self.pos -= 1
        # if self.pos < 0:
        #     self.pos = 0
        #     return None
        # return self.events[self.pos][1]


    def get_previous_query(self):
        pass
        # self.pos += 1
        # if self.pos >= len(self.events):
        #     self.pos = len(self.events)
        #     return None
        # return self.events[self.pos][1]


    def get_history(self):
        pass
        #return [ Item.from_dict(ev[2]) for ev in self.events ]


    def get_last_items(self):
        last_items = []
        for ev in self.events:
            item = ev[2]
            if item not in last_items:
                last_items.append(item)
            if len(last_items) >= 10:
                break

        return last_items

    # def get_total_score(self):
    #     total = 0
    #     for b in self.attic.values:
    #         total += b
    #     return total


    def get_item_bonus(self, item):
        return self.bonus.get(item['text'], 0)

    # def get_similar(self, query):

    #     similar_items = []
    #     for q in self.attic.keys():

    #         if q == query:
    #             continue

    #         d = distance(query, q)
    #         if d < 2:
    #             items = self.attic[q]
    #             similar_items.extend([Item.from_dict(i[0]) for i in items])

    #     return similar_items
