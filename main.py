# main app

import os
import sys
import math
import importlib
import multiprocessing
from gi.repository import Gtk, Gdk, GObject

import config
import utils
import drawer
import actions

from attic import Attic
from item import Item


class Sherlock(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # config
        self.width = 480
        self.height = 70
        self.lines = 5

        # plugins
        self.plugins_dir = config.plugins_dir
        self.base_plugins = dict()
        self.keyword_plugins = dict()
        self.fallback_plugins = dict()

        # data
        self.query = ''

        self.items = []
        self.selected = 0
        self.actions = []
        self.action_selected = 0

        self.menu_visible = False
        self.action_panel_visible = False
        self.file_navigation_mode = False

        # Attic
        self.attic = Attic()

        # window
        GObject.GObject.__init__(self)
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_title('Sherlock')
        self.set_size_request(self.width, self.height)

        self.connect('draw', self.draw)
        self.connect('key_press_event', self.on_key_press)
        self.connect('delete-event', self.close)
        self.connect('focus-out-event', self.close)
        self.connect('query_changed', self.on_query_changed)

        self.show_all()

        # load plugins
        self.load_plugins()


    #---------
    # Plugins
    #---------
    def import_plugin(self, name):
        try:
            plugin = importlib.import_module(name)
        except ImportError:
            return None
        return plugin

    def load_plugins(self):

        sys.path.append(self.plugins_dir)

        for name in config.base_plugins:
            plugin = self.import_plugin(name)
            if plugin is not None:
                self.base_plugins[name] = plugin

        for kw, name in config.keyword_plugins.items():
            if os.path.isfile(os.path.join(self.plugins_dir, '%s.py' % name)):
                self.keyword_plugins[kw] = name

        for text, name in config.fallback_plugins.items():
            if os.path.isfile(os.path.join(self.plugins_dir, '%s.py' % name)):
                self.fallback_plugins[text] = name


    #-------------
    # Draw window
    #-------------
    def draw(self, widget, event):
        cr = Gdk.cairo_create(widget.get_window())

        drawer.draw_background(cr)
        drawer.draw_bar(cr, self.query)

        if not self.menu_visible or not self.items:
            return

        first_item = 0 if (self.selected < self.lines) else \
                     (self.selected - self.lines + 1)

        n_items = len(self.items)
        max_items = min(self.lines, n_items)

        for i in range(max_items):
            drawer.draw_item(cr, i, self.items[first_item+i],
                             (first_item+i == self.selected))

        if self.action_panel_visible:
            drawer.draw_action_panel(cr, self.actions, self.action_selected)
        else:
            if n_items > self.lines:
                scroll_perc = self.selected/n_items
                drawer.draw_scrollbar(cr, scroll_perc)

        return False


    #------
    # Menu
    #------
    def show_menu(self):
        self.menu_visible = True
        self.queue_draw()
        self.resize(self.width, self.height + 240)

    def hide_menu(self):
        self.resize(self.width, self.height)
        self.queue_draw()
        self.menu_visible = False

    def clear_menu(self):
        self.items = []
        self.selected = 0
        self.hide_menu()


    #--------------
    # Action panel
    #--------------
    def show_action_panel(self):
        match = self.items[self.selected]
        match_actions = actions.actions[match.category]

        if len(match_actions) < 2:
            return

        if match_actions:
            self.actions = list(match_actions)
        self.action_panel_visible = True
        self.queue_draw()

    def hide_action_panel(self):
        if not self.action_panel_visible:
            return
        self.action_panel_visible = False
        self.actions = []
        self.action_selected = 0
        self.queue_draw()

    def toggle_action_panel(self):
        if self.action_panel_visible:
            self.hide_action_panel()
        else:
            self.show_action_panel()

    def actionate(self):
        match = self.items[self.selected]
        action = actions.actions[match.category][self.action_selected][1]

        self.attic.add(self.query, match, None)
        action(match.arg)

        self.close()


    #--------
    # Search
    #--------
    def start_file_navigation(self):
        import filenavigation
        self.items = filenavigation.get_matches(self.query)
        self.file_navigation_mode = True

    def search_worker(self, name, query, items):
        items[name] = self.base_plugins[name].get_matches(query)
        return

    def basic_search(self, query):

        jobs = []
        manager = multiprocessing.Manager()
        items = manager.dict()

        for name in self.base_plugins.keys():
            p = multiprocessing.Process(target=self.search_worker, args=(name, query, items))
            jobs.append(p)
            p.start()

        for j in jobs:
            j.join()

        for matches in items.values():
            if matches:
                self.items.extend(matches)

        # attic
        ## 1. Get similar queries in attic
        ## 2. Get sum histogram
        ## 3. Compute new score as (score * attic_score)/100
        #histogram = self.attic.get_histogram(query)
        #self.attic.sort_items(query, self.items)
        #print (histogram)
        #for item in self.items:
        #    print(item.title, item.score)
        # Reorder using attic info
        #for item in self.items:
        #if histogram:

        #    for b in histogram:

        #print(histogram)
            # total = 0
            # for item, count in histogram:
            #     total += count

            #     for item in self.items:

            #     print(item, count)

            # for item, count in histogram:
            #     total += count
            #     print(item, count)

        # order matches by score
        self.items  = utils.filter(query, self.items, key=lambda x: x.title)
        #self.items = sorted(self.items, key=lambda m: m.score, reverse=True)



    # def get_history(self):
    #     history = self.attic.get_last()
    #     self.items = [Item.from_dict(h[2]) for h in history]

    # def show_previous_queries(self):


    def clear_search(self):
        if self.items:
            del self.items[:]

        self.selected = 0
        self.file_navigation_mode = False
        self.hide_action_panel()

    def on_query_changed(self, widget, query):

        self.clear_search()

        if not query:
            self.clear_menu()
            return

        # File navigation
        if query.startswith('/') or query.startswith('~/'):
            self.start_file_navigation()

        # Keyword plugin
        elif query.startswith('!'):
            self.file_navigation_mode = False
            query = query[1:]
            for keyword, name in self.keyword_plugins.items():

                if query.startswith(keyword):
                    plugin = self.import_plugin(name)
                    matches = plugin.get_matches(query.replace(keyword, ''))

                    if matches:
                        self.items.extend(matches)

                    break

        # Basic search
        else:
            self.file_navigation_mode = False
            self.basic_search(query)

        # fallback plugins
        if not self.items:
            for text in self.fallback_plugins.keys():
                title = text.replace('query', '\'%s\'' % query)
                it = Item(title)
                self.items.append(it)

        # show menu
        if self.items:
            self.show_menu()
        else:
            self.clear_menu()


    #--------------
    # Key press cb
    #--------------
    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if key == 'BackSpace':
                self.update_query('')
            return

        if key == 'Escape':
            self.close()

        elif key == 'Left':
            if self.file_navigation_mode == True:
                idx = self.query[:-1].rfind('/')
                self.update_query(self.query[:idx]+'/')

        elif key == 'Right':
            if self.file_navigation_mode == True and self.selected >= 0:
                self.update_query(self.items[self.selected].arg)

        elif key == 'Down':
            if not self.menu_visible:
                #if not self.query:
                #    self.get_history()
                if self.items:
                    self.show_menu()
            else:
                self.select_down()

        elif key == 'Up':
            #if not self.query or self.selected == 0:
            #    self.show_previous_query()
            #else:
            self.select_up()

        elif key == 'BackSpace':
            self.del_char()

        elif 'Return' in key:
            self.actionate()

        elif 'Tab' in key:
            if self.items:
                self.toggle_action_panel()

        elif 'Alt' in key or \
             'Control' in key:
            pass

        else:
            self.add_char(event.string)

    #---
    def show_previous_query(self):
        query = self.attic.get_query()
        if query is not None:
            self.update_query(query)

    def select_down(self):
        if self.action_panel_visible:
            if self.action_selected == len(self.actions) - 1:
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
        self.query = '%s%s' % (self.query, char)
        self.queue_draw()
        self.emit('query_changed', self.query)

    def del_char(self):
        self.query = self.query[:-1]
        self.queue_draw()
        self.emit('query_changed', self.query)

    def update_query(self, query):
        self.query = query
        self.cursor = len(query)
        self.emit('query_changed', self.query)


    #-------------
    # Run & close
    #-------------
    def run(self):
        Gtk.main()

    def close(self, *args):
        self.attic.save()
        Gtk.main_quit()
