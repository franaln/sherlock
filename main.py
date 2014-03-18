from gi.repository import Gtk, Gdk

from menu import Menu
from search import SearchEngine

class Main():

    def __init__(self):

        self.menu = Menu()
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('delete-event', self.close)
        self.menu.connect('query_changed', self.search)

        self.engine = SearchEngine()

    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        Gtk.main_quit()

    def reset_search(self):
        self.menu.clear()

    def search(self, widget, query):

        if not query:
            self.reset_search()
            return

        self.engine.search(query)

        matches = self.engine.matches

        matches.sort(key = lambda x: -x.score)

        if matches:
            print('%s > %s' % (query, matches))
            self.menu.show(matches)
        else:
            self.reset_search()
            return


    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        #modifiers = Gtk.accelerator_get_default_mod_mask()

        if event.state and Gdk.ModifierType.CONTROL_MASK:
            # ## ctrl-q: exit
            # if  key == 'q':
            #     self.close()
            return

        #print(key, Gdk.keyval_to_unicode(event.keyval), event.keyval)

        if key == 'Escape':
            self.close()
        elif key == 'Left':
            pass
        elif key == 'Right':
            sel.menu.show_actions()
        elif key == 'Down':
            self.menu.show_box()
            self.menu.select_next()
        elif key == 'Up':
            self.menu.select_prev()
        elif key == 'BackSpace':
            self.menu.rm_char()
        elif key == 'space':
            self.menu.add_char(' ')
        elif 'Alt' in key or \
             'Shift' in key or \
             'Control' in key or \
             'Return' in key or \
             'Tab' in key:
            pass
        else:
            self.menu.add_char(key)
