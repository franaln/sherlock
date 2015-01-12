import time

from gi.repository import GObject, GLib

class Bar(GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):
        self.cursor = 0
        self.query = ''

        self.counter = 0
        self.updated = False

        GObject.GObject.__init__(self)

        GLib.timeout_add(250, self.check)

    def addchar(self, char):
        self.counter = time.time()
        self.updated = True
        self.query = '%s%s' % (self.query, char)
        #self.queue_draw()

    def delchar(self):
        self.counter = time.time()
        self.updated = True
        self.query = self.query[:-1]
        #self.queue_draw()

    def update(self, text):
        self.counter = time.time()
        self.updated = True
        self.query = text
        self.cursor = len(text)

    def check(self):
        if time.time() > (self.counter + 0.25) and self.updated:
            self.updated = False
            self.emit('query_changed', self.query)
        return True
