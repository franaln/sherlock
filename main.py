# main app

import os
import sys
import math
import importlib
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

import config
import drawer
import actions
import attic

class Sherlock(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # plugins
        self.plugins_dir = 'plugins'
        self.base_plugins = dict()
        self.keyword_plugins = dict()
        self.fallback_plugins = dict()

        self.load_plugins()

        # data
        self.query = ''
        self.cursor = 0

        self.items = []
        self.selected = 0

        self.action_panel_visible = False
        self.actions = []
        self.action_selected = 0

        self.attic = attic.Attic()

        # window
        GObject.GObject.__init__(self)
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_title('Sherlock')
        self.set_size_request(config.width, config.height)

        self.connect('draw', self.draw)
        self.connect('key_press_event', self.on_key_press)
        self.connect('delete-event', self.close)
        self.connect('query_changed', self.do_search)

        self.show_all()

    def draw(self, widget, event):
        cr = Gdk.cairo_create(widget.get_window())

        drawer.draw_window(cr)

        drawer.draw_bar(cr, self.query)

        if not self.items:
            return

        first_item = 0 if (self.selected < config.lines) else \
                     (self.selected - config.lines + 1)

        max_items = min(config.lines, len(self.items))

        for i in range(max_items):
            drawer.draw_item(cr, i, self.items[first_item+i],
                           (first_item+i == self.selected))

        if self.action_panel_visible:
            drawer.draw_action_panel(cr, self.actions, self.action_selected)

        return False

    def import_plugin(self, dict_, name):
        try:
            plugin = importlib.import_module('.'.join([self.plugins_dir, name]))
        except ImportError:
            return

        if hasattr(plugin, 'keyword'):
            dict_[plugin.keyword] = plugin

    def load_plugins(self):
        for name in config.base_plugins:
            self.import_plugin(self.base_plugins, name)

        for name in config.keyword_plugins:
            self.import_plugin(self.keyword_plugins, name)

        for name in config.fallback_plugins:
            self.import_plugin(self.fallback_plugins, name)

    def show_menu(self):
        self.resize(config.width,
                    config.height + config.item_height * config.lines)
        self.queue_draw()

    def hide_menu(self):
        self.resize(config.width, config.height)
        self.queue_draw()

    def clear_menu(self):
        self.items = []
        self.selected = 0
        self.hide_menu()

    def is_action_panel_visible(self):
        return self.action_panel_visible

    def hide_action_panel(self):
        self.action_panel_visible = False
        self.actions = []
        self.action_selected = 0
        self.queue_draw()

    def show_action_panel(self, actions=None):
        if actions is not None:
            self.actions = list(actions)
        self.action_panel_visible = True
        self.queue_draw()

    def select_down(self):
        if self.action_panel_visible:
            if self.action_selected == len(self.actions) -1:
                return
            self.action_selected += 1
        else:
            if self.selected == len(self.items) - 1:
                return
            self.selected += 1
        self.queue_draw()

    def select_up(self):
        if self.action_panel_visible:
            if self.action_selected == 0:
                return
            self.action_selected -= 1
        else:
            if self.selected == 0:
                self.hide_menu()
                return
            self.selected -= 1
        self.queue_draw()

    def add_char(self, char):
        self.query += char
        self.queue_draw()
        self.emit('query_changed', self.query)

    def rm_char(self):
        self.query = self.query[:-1]
        self.queue_draw()
        self.emit('query_changed', self.query)

    def move_cursor_left(self):
        pass

    def move_cursor_right(self):
        pass

    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        self.attic.save()
        Gtk.main_quit()

    def reset_search(self):
        self.clear_menu()

    def do_search(self, widget, query):

        # clear matches
        if self.items:
            del self.items[:]

        if not query:
            self.reset_search()
            return

        query_split = query.split()
        keyword = query_split[0]

        if keyword in self.keyword_plugins:
            self.items = self.keyword_plugins[keyword].get_matches(query_split[1:])

        else:
            for plugin in self.base_plugins.values():

                matches = plugin.get_matches(query)
                if matches is not None:
                    self.items.extend(matches)

        if not self.items:
            for plugin in self.fallback_plugins.values():
                matches = plugin.get_matches(query)
                if matches is not None:
                    self.items.extend(matches)


        # attic
        ## 1. Get similar queries in attic
        ## 2. Get sum histogram
        ## 3. Compute new score as (score * attic_score)/100

        # order matches by score
        self.items = sorted(self.items, key=lambda m: m[1], reverse=True)

        # remove score
        self.items = [ m[0] for m in self.items ]

        # show menu
        if self.items:
            self.show_menu()
        else:
            self.reset_search()
            return

    def toggle_action_panel(self):
        if self.is_action_panel_visible():
            self.hide_action_panel()
            return

        match = self.items[self.selected]

        _actions = actions.actions[match.category]

        if len(_actions) < 2:
            return

        self.show_action_panel(_actions)

    def actionate(self):

        match = self.items[self.selected]

        action = actions.actions[match.category][self.action_selected][1]

        action(match.arg)

        self.attic.add(self.query, match)
        self.close()

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            return

        if key == 'Escape':
            self.close()
        elif key == 'Left':
            self.move_cursor_left()
        elif key == 'Right':
            self.move_cursor_right()
        elif key == 'Down':
            self.show_menu()
            self.select_down()
        elif key == 'Up':
            self.select_up()
        elif key == 'BackSpace':
            self.rm_char()
        elif 'Return' in key:
            self.actionate()
        elif 'Tab' in key:
            self.toggle_action_panel()
        elif 'Alt' in key or \
             'Control' in key:
            pass
        else:
            self.add_char(event.string)
