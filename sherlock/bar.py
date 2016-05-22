# bar widget

import time
from gi.repository import GObject, GLib

from sherlock import config
from sherlock import drawer


class Bar(GObject.GObject):

    __gsignals__ = {
        'update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'query-change': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        self.cursor = 0
        self.query = ''
        self.selected = False
        self.counter = 0
        self.updated = False

        GObject.GObject.__init__(self)

        GLib.timeout_add(500, self.check)

    def _update(self, text):
        self.counter = time.time()
        self.updated = True
        self.query = text
        self.emit('update')

    def addchar(self, char, clear=False):
        if clear:
            self.clear()
            self.cursor = 0
        newquery = '%s%s%s' % (self.query[:self.cursor], char, self.query[self.cursor:])
        self._update(newquery)
        self.cursor += len(char)

    def delchar(self, delete=False):
        if delete:
            newquery = '%s%s' % (self.query[:self.cursor], self.query[self.cursor+1:])
        else:
            if self.cursor == 0:
                newquery = self.query
            else:
                newquery = '%s%s' % (self.query[:self.cursor-1], self.query[self.cursor:])
                self.cursor -= 1
        self._update(newquery)

    def clear(self):
        self.cursor = 0
        self._update('')

    def is_empty(self):
        return bool(not self.query)

    def check(self):
        if time.time() > (self.counter + 0.25) and self.updated:
            self.updated = False
            self.emit('query-change', self.query)
        return True

    def select(self):
        self.selected = True

    def move_cursor_begin(self):
        self.cursor = 0
        self.emit('update')

    def move_cursor_end(self):
        self.cursor = len(self.query)
        self.emit('update')

    def move_cursor_left(self):
        if self.cursor <= 0:
            return
        self.cursor -= 1
        self.emit('update')

    def move_cursor_right(self):
        if self.cursor >= len(self.query):
            return
        self.cursor += 1
        self.emit('update')
