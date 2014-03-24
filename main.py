# main app

from gi.repository import Gtk, Gdk

from menu import Menu
from manager import PluginManager
import actions

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

    def do_search(self, widget, query):

        # clear matches
        if self.matches:
            del self.matches[:]

        if not query:
            self.reset_search()
            return

        # check if query is keyword
        query_split = query.split()
        for plugin in self.manager.keyword_plugins:
            if query_split[0] in plugin.keywords:
                matches = plugin.get_matches(query_split[1:])
                self.matches += matches
                break
        else:
            for plugin in self.manager.plugins:

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

    def toggle_action_panel(self):
        if self.menu.is_action_panel_visible():
            self.menu.hide_action_panel()
            return

        match = self.matches[self.menu.selected]
        match_type = match.get('type')

        _actions = actions.actions[match_type]

        if len(_actions) < 2:
            return

        self.menu.show_action_panel(_actions)

    def actionate(self):

        match = self.matches[self.menu.selected]
        match_type = match.get('type')

        # get selected or defaul_action
        action = actions.actions[match_type][self.menu.action_selected][1]

        action(match.get('arg'))

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
            self.actionate()
        elif 'Tab' in key:
            self.toggle_action_panel()
        elif 'Alt' in key or \
             'Control' in key:
            pass
        else:
            self.menu.add_char(event.string)
