# main app

from gi.repository import Gtk, Gdk

from menu import Menu
from manager import PluginManager

class Main():

    def __init__(self):

        self.menu = Menu()
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('delete-event', self.close)
        self.menu.connect('query_changed', self.do_search)

        self.manager = PluginManager()

        self.matches = []

    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        Gtk.main_quit()

    def reset_search(self):
        self.menu.clear_menu()

    def clear_matches(self):
        if self.matches:
            del self.matches[:]

    def do_search(self, widget, query):
        self.clear_matches()

        if not query:
            self.reset_search()
            return

        #query_split = query.split()

        # for plugin in self.manager.get_plugins():
        #     if query_split[0] == plugin.keyword:
        #         matches = plugin.get_matches(query_split[1:])
        #         self.matches += matches
        #         break
        # else:

        for plugin in self.manager.get_plugins():
            # if plugin.only_keyword:
            #     continue

            matches = plugin.get_matches(query)

            if matches is not None:
                self.matches += matches

        # order matches by score
        self.matches = sorted(self.matches, key=lambda m: m.get('score'), reverse=True)

        # relevance/frequency/learning go here!?!

        # show menu
        if self.matches:
            self.menu.show_menu(self.matches)
        else:
            self.reset_search()
            # show fallback searches
            return

    def do_action(self):

        # get selected match
        match = self.matches[self.menu.get_selected()]

        # get plugin
        plugin = self.manager.get_plugin(match.plugin)

        # get default action
        action = plugin.get_default_action()

        # execte action and hide
        action.execute(match)
        self.close()

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            return

        if key == 'Escape':
            self.close()
        elif key == 'Left':
            self.menu.move_cursor_left()
        elif key == 'Right':
            self.menu.move_cursor_right()
        elif key == 'Down':
            self.menu.show_menu()
            self.menu.select_down()
        elif key == 'Up':
            self.menu.select_up()
        elif key == 'BackSpace':
            self.menu.rm_char()
        elif 'Return' in key:
            self.do_action()
        elif 'Tab' in key:
            self.menu.toggle_action_panel()
        elif 'Alt' in key or \
             'Control' in key:
            pass
        else:
            self.menu.add_char(event.string)
