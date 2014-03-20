# main app

from gi.repository import Gtk, Gdk

from menu import Menu

from plugins.applications import ApplicationsPlugin
from plugins.calculator import CalculatorPlugin
from plugins.screen import ScreenPlugin

class Main():

    def __init__(self):
        self.menu = Menu()
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('delete-event', self.close)
        self.menu.connect('query_changed', self.search)

        self.plugins = [
            ApplicationsPlugin(),
            CalculatorPlugin(),
            ScreenPlugin(),
        ]

        self.matches = []

    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        Gtk.main_quit()

    def reset_search(self):
        self.menu.clear()

    def clear_matches(self):
        del self.matches[:]

    def search(self, widget, query):
        self.clear_matches()

        if not query:
            self.reset_search()
            return

        query_split = query.split()

        for plugin in self.plugins:
            if query_split[0] == plugin.keyword:
                matches = plugin.get_matches(query_split[1:])
                self.matches += matches
                break
        else:
            for plugin in self.plugins:
                matches = plugin.get_matches(query)
                if matches is not None:
                    self.matches += matches

        if self.matches:
            print('%s > %s' % (query, self.matches))
            self.menu.show(self.matches)
        else:
            self.reset_search()
            return

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        #modifiers = Gtk.accelerator_get_default_mod_mask()

        if event.state and Gdk.ModifierType.CONTROL_MASK:
            return

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
        elif 'Return' in key:
            match = self.matches[self.menu.get_selected()]
            action = self.plugins[0].get_default_action()
            action.execute(match)
            self.close()

        elif 'Alt' in key or \
             'Control' in key or \
             'Tab' in key:
            pass
        else:
            self.menu.add_char(event.string)
