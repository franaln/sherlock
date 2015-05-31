# Sherlock main

import os
import sys
import json
import logging
import importlib
import threading
import cairo
from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf, Poppler

from sherlock import config
from sherlock import utils
from sherlock import drawer
from sherlock import actions
from sherlock import search
from sherlock import items as items_
from sherlock.bar import Bar
from sherlock.attic import Attic

cache_dir = os.path.expanduser(config.cache_dir)
attic_path = os.path.join(cache_dir, 'attic')

lock = threading.Lock()

class Sherlock(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'menu-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self, debug=False):

        # logger
        formatter = '%(levelname)s (%(name)s) %(message)s'
        if debug:
            logging.basicConfig(level=logging.DEBUG, format=formatter)
        else:
            logging.basicConfig(level=logging.INFO, format=formatter)
        self.logger = logging.getLogger(__name__)

        self.logger.info('starting sherlock...')

        # config
        self.width = 600
        self.height = 100

        # plugins
        self.plugins_dir = os.path.expanduser(config.plugins_dir)
        self.base_plugins = dict()
        self.keyword_plugins = dict()
        self.fallback_plugins = dict()

        # bar
        self.bar = Bar()

        # menu
        self.items = []
        self.selected = 0
        self.actions = []
        self.action_selected = 0
        self.menu_visible = False
        self.action_panel_visible = False

        # Attic
        self.attic = Attic(attic_path)

        # window
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_size_request(self.width, self.height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_title('Sherlock')
        self.show_all()

        self.connect('draw', self.draw)

        self.connect('key_press_event', self.on_key_press)
        self.connect('delete-event', self.close)
        self.connect('focus-out-event', self.close)
        self.bar.connect('update', self.on_bar_update)
        self.bar.connect('query-change', self.on_query_change)
        self.connect('menu-update', self.on_menu_update)

        # preview
        self.preview = None

        # plugins
        self.load_plugins()
        self.worker = search.SearchWorker()


    # ---------
    #  Plugins
    # ---------
    def import_plugin(self, name):
        try:
            plugin = importlib.import_module(name)
            self.logger.info('pluging %s loaded.' % name)
        except ImportError:
            self.logger.error('error loading plugin %s.' % name)
            return None
        return plugin

    def load_plugins(self):

        sys.path.append(self.plugins_dir)

        for name in config.basic_search:
            plugin = self.import_plugin(name)

            if plugin is not None:
                self.base_plugins[name] = plugin

        for kw, name in config.plugins.items():
            if os.path.isfile(os.path.join(self.plugins_dir, '%s.py' % name)):
                self.keyword_plugins[kw] = name

        for text, name in config.fallback_plugins.items():
            if os.path.isfile(os.path.join(self.plugins_dir, '%s.py' % name)):
                self.fallback_plugins[text] = name

    # -----------
    #  Callbacks
    # -----------
    def on_bar_update(self, widget):
        self.queue_draw()

    def on_menu_update(self, widget):
        if self.bar.query and self.items:
            self.show_menu()
        else:
            self.clear_menu()

    def on_query_change(self, widget, query):
        self.queue_draw()

        self.clear_menu()

        if self.preview is not None:
            self.preview.hide()

        # File navigation
        if self.file_navigation_mode(query):
            self.logger.info('file navigation: %s' % query)
            self.file_navigation(query)

        # Search
        else:
            self.search(query)

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        self.logger.debug('key pressed: %s', key)

        # CTRL is pressed
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if key == 'Left':
                self.bar.move_cursor_left()
            elif key == 'Right':
                self.bar.move_cursor_right()
            elif key == 'Up':
                self.previous_query()
            elif key == 'Down':
                self.next_query()
            elif 'space' in key:
                self.toggle_preview()
            elif key == 'y':
                self.bar.addchar(utils.get_selection())
            elif key == 'Backspace':
                print('bu')
                self.bar.clear()

            return

        if key == 'Escape':
            self.close()

        elif key == 'Left':
            if self.file_navigation_mode():
                self.file_navigation_back()

        elif key == 'Down':
            if not self.menu_visible:
                if self.bar.is_empty():
                    self.show_history()
                if self.items:
                    self.show_menu()
            else:
                self.select_down()

        elif key == 'Up':
            self.select_up()

        elif key == 'BackSpace':
            self.bar.delchar()

        elif key == 'Delete':
            self.bar.delchar(True)

        # Return/Right: execute default action on selected item
        elif 'Return' in key or key == 'Right':
            if self.file_navigation_mode() and self.selected_item().is_dir():
                self.file_navigation_cd()
            else:
                self.actionate()

        elif 'Tab' in key:
            if self.items:
                self.toggle_action_panel()

        elif 'Alt' in key or 'Control' in key:
            pass

        else:
            if event.string:
                self.bar.addchar(event.string)

    def search_plugin(self, plugin, query):
        self.worker.add_update(self.plugin_done, plugin, query)

    def plugin_done(self, task_id, query, result):

        with lock:
            if result:
                self.items.extend(result)

                #self.items = sorted(self.items, key=lambda x: x.score, reverse=True)

                if query:
                    self.attic.sort(query, self.items)

                    #if len(query) > 1:
                    #self.items.extend(self.attic.get_similar(query))

                self.items = sorted(self.items, key=lambda x: x.score, reverse=True)

        self.emit('menu-update')

    # -------------
    #  Run & close
    # -------------
    def run(self):
        Gtk.main()

    def close(self, *args):
        self.logger.info('closing...')
        self.attic.save()
        Gtk.main_quit()

    # ------
    #  Menu
    # ------
    def clear_menu(self):
        if self.items:
            del self.items[:]
        self.selected = 0
        self.hide_action_panel()
        self.hide_menu()

    def show_menu(self):
        self.menu_visible = True
        self.resize(self.width, self.height + 300)
        self.queue_draw()

    def hide_menu(self):
        self.resize(self.width, self.height)
        self.menu_visible = False
        self.queue_draw()

    def show_action_panel(self):
        match = self.items[self.selected]
        match_actions = items_.actions[match.category]

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


    def selected_item(self):
        return self.items[self.selected]

    # -------------
    #  Draw window
    # -------------
    def draw(self, widget, event):

        cr = Gdk.cairo_create(widget.get_window())

        drawer.draw_background(cr)

        self.bar.draw(cr)

        if not self.menu_visible or not self.items:
            return

        first_item = 0 if (self.selected < 5) else (self.selected - 4)

        n_items = len(self.items)
        max_items = min(5, n_items)

        for i in range(max_items):
            drawer.draw_item(cr, i, self.items[first_item + i],
                             (first_item + i == self.selected))

        if self.action_panel_visible:
            drawer.draw_action_panel(cr, self.actions, self.action_selected)

        return False

    # --------
    #  Search
    # --------
    def search(self, query):

        if not query:
            self.clear_menu()
            return

        self.logger.info('searching %s' % query)

        matches = []

        # Keyword plugin
        if query.startswith('.'):
            query = query[1:].strip()

            for keyword, name in self.keyword_plugins.items():

                if query.startswith(keyword):

                    query = query[len(keyword):].strip()

                    if isinstance(name, str):
                        self.keyword_plugins[keyword] = self.import_plugin(name)

                    plugin_matches = self.keyword_plugins[keyword].get_matches(query)

                    if plugin_matches:
                        matches.extend(plugin_matches)

                    break

        # Basic search
        if not matches:

            for name in self.base_plugins.keys():
                plugin = self.base_plugins[name]
                self.search_plugin(plugin, query)

            if self.keyword_plugins:
                for kw, name in self.keyword_plugins.items():
                    if query in kw:
                        self.items.append(items_.ItemPlugin(name, kw))

        # fallback plugins
        if not self.items:
            for text in self.fallback_plugins.keys():
                title = text.replace('query', '\'%s\'' % query)
                it = items_.ItemText(title, no_filter=True)
                self.items.append(it)

        # order matches by score
        if matches:
            self.items.extend(matches)
        else:
            it = items_.ItemCmd("run '%s' in a shell" % query, query)

            self.items.append(it)

        self.emit('menu-update')

    # --------
    #  Action
    # --------
    def actionate(self):

        item_selected = self.selected
        if item_selected < 0:
            item_selected = 0

        match = self.items[item_selected]
        action_name = items_.actions[match.category][self.action_selected][1]

        self.attic.add(self.bar.query, match, None)

        if action_name == 'explore' or os.path.isdir(match.arg):
            self.explore(match.arg)
            return

        action = getattr(actions, action_name)
        self.logger.info('executing %s %s' % (action_name, match.arg))

        action(match.arg)

        self.close()


    # -----------
    #  Navigation
    # -----------
    def show_previous_query(self):
        query = self.attic.get_query()
        if query is not None:
            self.bar.addchar(query)

    def select_down(self):
        if self.action_panel_visible:
            if self.action_selected == len(self.actions) - 1:
                return
            self.action_selected += 1
        else:
            if self.selected == len(self.items) - 1:
                return
            self.selected += 1

            if self.preview is not None and self.preview.get_visible():
                self.update_preview()

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

            if self.preview is not None and self.preview.get_visible():
                self.update_preview()

        self.queue_draw()

    def previous_query(self):
        previous_query = self.attic.get_previous_query()

        if previous_query is not None:
            self.bar.addchar(previous_query)

    def next_query(self):
        next_query = self.attic.get_next_query()

        if next_query is not None:
            self.bar.addchar(next_query)

    def show_history(self):
        self.items = self.attic.get_history()
        self.show_menu()

    # -----------------
    #  File navigation
    # -----------------
    def file_navigation_mode(self, query=None):
        if query is None:
            query = self.bar.query
        return (query.startswith('/') or query.startswith('~/'))

    def file_navigation(self, query):

        query = os.path.expanduser(query)

        idx = query.rfind('/')
        if idx >= 0:
            path = query[:idx+1]
            query = query[idx+1:]
        else:
            path = query
            query = ''

        path_content = os.listdir(path)

        items = []
        for p in path_content:

            # exclude hidden files
            if p.startswith('.'):
                continue

            # filter by query
            if query and query.lower() not in p.lower():
                continue

            abspath = os.path.join(path, p)

            items.append(items_.ItemUri(abspath))

        # sort items by
        self.items = sorted(items, key=lambda it: it.arg)

        self.emit('menu-update')

    def file_navigation_cd(self):
        new_query = self.items[self.selected].arg
        self.bar.addchar(new_query.replace(os.environ['HOME'], '~'), True)

    def file_navigation_back(self):
        query = os.path.expanduser(self.bar.query[:-1])
        idx = query.rfind('/')
        new_query = query[:idx]+'/'
        self.bar.addchar(new_query.replace(os.environ['HOME'], '~'), True)

    def explore(self, arg):
        self.bar.addchar(arg, True)

    # -----------------
    #  File Preview
    # -----------------
    def toggle_preview(self):
        if self.preview is None:
            self.create_preview()
        elif self.preview is not None and self.preview.get_visible():
            self.preview.hide()
        else:
            self.update_preview()

    def create_preview(self):
        self.preview = Gtk.Window(type=Gtk.WindowType.POPUP)

        self.box = Gtk.Box()
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        self.preview.add(self.box)

        self.image = Gtk.Image()
        self.box.pack_start(self.image, False, False, 0)

        self.update_preview()

    def update_preview(self):

        item_selected = self.selected if self.selected >= 0 else 0
        path = self.items[item_selected].arg

        pb = None

        # if path is an image
        try:
            pb = GdkPixbuf.Pixbuf.new_from_file(path)
        except:
            pass

        # if path is a pdf
        if pb is None and path.endswith('.pdf'):
            try:
                doc = Poppler.Document.new_from_file('file://'+path)

                page = doc.get_page(0)

                width, height = page.get_size()

                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                             int(width), int(height))
                ctx = cairo.Context(surface)

                page.render(ctx)

                ctx.set_operator(cairo.OPERATOR_DEST_OVER)
                ctx.set_source_rgb(1, 1, 1)
                ctx.paint()

                pb = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)
            except:
                pass

        if pb is None:
            self.preview.hide()
            return

        self.logger.info('showing preview for %s' % path)

        screen_w = Gdk.Screen.width()
        screen_h = Gdk.Screen.height()

        w, h = pb.get_width(), pb.get_height()
        ratio = w/h

        max_w = screen_w
        max_h = screen_h/2 - self.height/2

        if h > max_h:
            pb = pb.scale_simple(ratio*max_h, max_h, GdkPixbuf.InterpType.BILINEAR)
        elif w > max_w:
            pb = pb.scale_simple(max_w, max_w/ratio, GdkPixbuf.InterpType.BILINEAR)

        self.image.set_from_pixbuf(pb)

        w, h = pb.get_width(), pb.get_height()
        self.preview.resize(w, h)

        xpos = screen_w/2 - w/2
        ypos = screen_h/2 - h - self.height/2
        self.preview.move(xpos, ypos)

        self.preview.show_all()
