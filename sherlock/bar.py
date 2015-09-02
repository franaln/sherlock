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

        GLib.timeout_add(250, self.check)

    def _update(self, text):
        self.counter = time.time()
        self.updated = True
        self.query = text
        self.emit('update')

    def addchar(self, char, clear=False):
        if clear:
            self.clear()
        newquery = '%s%s%s' % (self.query[:self.cursor], char, self.query[self.cursor:])
        self._update(newquery)
        self.cursor += len(char)

    def delchar(self, delete=False):
        if delete:
            newquery = '%s%s' % (self.query[:self.cursor], self.query[self.cursor+1:])
        else:
            newquery = '%s%s' % (self.query[:self.cursor-1], self.query[self.cursor:])
            self.cursor -= 1
        print(newquery)
        self._update(newquery)

    def clear(self):
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
        self.cursor -= 1
        self.emit('update')

    def move_cursor_right(self):
        self.cursor += 1
        self.emit('update')

    def draw(self, cr):

        """
                  6px
        ---------------------------
        6px |10px query|              | 6px
        ---------------------------
                  6px
        """
        bar_w = drawer.width - 12
        bar_h = drawer.height - 12

        bar_color = config.bar_color

        # drawer.draw_rect(cr, 6, 6, bar_w, bar_h, bar_color)

        query_x = 16
        query_y = bar_h * 0.5

        # if self.selected:
        #     drawer.draw_rect(cr, query_x, 18, drawer.calc_text_width(cr, self.query, size=38), 60, config.selection_color)

        drawer.draw_variable_text(cr, query_x, query_y, bar_w-20, 0, self.query, size=38)

        #cursor_x = query_x + drawer.calc_text_width(cr, self.query[:self.cursor], size=38)

        # drawer.draw_rect(cr, cursor_x, 18, 2, 60)
