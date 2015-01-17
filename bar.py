# bar widget

import time
from gi.repository import GObject, GLib

import config
import drawer


"""
              6px
    ---------------------------
6px |10px query|              | 6px
    ---------------------------
              6px
"""
bar_o = 6
bar_w = drawer.width - 2*bar_o
bar_h = drawer.height - 2*bar_o

bar_color = config.bar_color

class Bar(GObject.GObject):

    __gsignals__ = {
        'updated': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        self.cursor = 0
        self.query = ''

        self.counter = 0
        self.updated = False

        GObject.GObject.__init__(self)

        GLib.timeout_add(250, self.check)

    def update(self, text):
        self.counter = time.time()
        self.updated = True
        self.query = text
        self.cursor = len(text)
        self.emit('updated')

    def addchar(self, char):
        self.update('%s%s' % (self.query, char))

    def delchar(self):
        self.update(self.query[:-1])

    def clear(self):
        self.update('')

    def check(self):
        if time.time() > (self.counter + 0.25) and self.updated:
            self.updated = False
            self.emit('query_changed', self.query)
        return True

    def draw(self, cr):

        drawer.draw_rect(cr, bar_o, bar_o, bar_w, bar_h, bar_color)

        query_x = 10 + bar_o
        query_y = bar_h * 0.5

        drawer.draw_variable_text(cr, query_x, query_y, bar_w-20, 0, self.query, size=38)

        # if query and selected:
        #     drawer.draw_rect(cr, query_x, query_y-query_h*0.5, query_w+5, query_h, sel_color)

    def is_empty(self):
        return bool(not self.query)
