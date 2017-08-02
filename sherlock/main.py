# Sherlock main

import os
import sys
import json
import cairo
import logging
import importlib
import threading
import datetime

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Poppler', '0.18')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf, Poppler

import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib

from sherlock.menu import Menu
from sherlock.manager import Manager
from sherlock.attic2 import Attic

from sherlock import utils
from sherlock import search

from sherlock import actions
from sherlock.items import Item, ItemUri

config_dir = os.path.expanduser('~/.config/sherlock')
cache_dir  = os.path.expanduser('~/.cache/sherlock/')
attic_path = os.path.join(cache_dir, 'attic')

lock = threading.Lock()

use_threads = False

home_dir = os.environ['HOME']


class Sherlock(dbus.service.Object):

    def __init__ (self, bus, path, name, debug):

        dbus.service.Object.__init__(self, bus, path, name)

        self.running = False
        self.showing = False

        self.debug = debug

        # logger
        formatter = '%(levelname)s (%(name)s) %(message)s'
        if debug:
            logging.basicConfig(level=logging.DEBUG, format=formatter)
        else:
            logging.basicConfig(level=logging.INFO, format=formatter)
        self.logger = logging.getLogger(__name__)

        self.logger.info('starting sherlock...')

        # config
        config_file = os.path.join(config_dir, 'config.py')
        if os.path.exists(config_file) and os.path.isfile(config_file):
            self.logger.info('loading configfile from %s' % config_file)
            sys.path.append(config_dir)
            config = importlib.import_module('config')
        else:
            self.logger.info('loading default configfile')
            from sherlock import config

        self.config = config

        # Menu & Manager & Attic
        self.menu = Menu(config, debug)
        self.manager = Manager(config)
        self.attic = Attic(attic_path)

        self.commands = [
            'clear',
            'update',
        ]

        # recreate db
        self.manager.update_cache()
        GLib.timeout_add_seconds(1800, self.manager.update_cache)

        # preview
        self.preview = None

        #
        self.menu.connect('delete-event', Gtk.main_quit)
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('focus-out-event', self.on_hide_menu)
        self.menu.connect('menu-update', self.menu.on_menu_update)
        self.menu.connect('query-change', self.on_query_change)

    # -------------
    #  Run & close
    # -------------
    @dbus.service.method("org.sherlock.Daemon", in_signature='', out_signature='')
    def run(self):
        if self.running:
            if not self.showing:
                self.show_menu()
            else:
                self.hide_menu()
        else:
            self.running = True
            Gtk.main()
            self.running = False

    @dbus.service.method("org.sherlock.Daemon", in_signature='', out_signature='')
    def close(self, *args):
        self.logger.info('closing...')
        self.attic.save()
        self.showing = False
        Gtk.main_quit()


    # -----------
    #  Callbacks
    # -----------
    def on_hide_menu(self, widget, a):
        self.hide_menu()
        if self.preview is not None:
            self.preview.hide()
            self.preview = None

    def on_query_change(self, widget, query):
        self.logger.debug('query change: %s', query)

        # Clear menu
        self.menu.hide_right_panel()
        self.menu.clear_menu()

        if not query:
            self.menu.emit('menu-update')
            return

        self.search(query)

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        # CTRL is pressed
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if key == 'Left':
                self.menu.move_cursor_left()
            elif key == 'Right':
                self.menu.move_cursor_right()
            elif key == 'Up':
                self.previous_query()
            elif key == 'Down':
                self.next_query()
            elif key == 'a':
                self.menu.move_cursor_begin()
            elif key == 'e':
                self.menu.move_cursor_end()
            elif key == 'BackSpace':
                self.menu.clear_bar()
            elif 'space' in key:
                self.toggle_preview()
            elif key == 'y':
                self.menu.addchar(utils.get_selection())
            elif key == 'h':
                #self.show_history()
                pass

            return

        if key == 'Escape':
            self.hide_menu()

        elif key == 'Left':
            if self.file_navigation_mode():
                self.file_navigation_cd_back()

        elif key == 'Down':
            # if not self.menu_visible:
            #     if self.bar.is_empty():
            #         self.show_history()
            #     if self.matches:
            #         self.show_menu()
            # else:
            self.menu.select_down()

        elif key == 'Up':
            # if not self.menu_visible and self.bar.is_empty():
            #     #self.bar.select()
            #     #self.previous_query()
            # else:
            self.menu.select_up()

        elif key == 'BackSpace':
            self.menu.delchar()

        elif key == 'Delete':
            self.menu.delchar(True)

        # Return/Right: execute default action on selected item
        elif 'Return' in key or key == 'Right':
            if self.file_navigation_mode(): ## and self.right_item_selected < 1:
                self.file_navigation_cd()
            else:
                self.actionate()

        elif 'Tab' in key:
            if self.menu.items:
                self.menu.toggle_right_panel()

        elif 'Alt' in key or 'Control' in key:
            pass

        else:
            if event.string:
                self.menu.addchar(event.string)


    # ----------------
    # Show / Hide menu
    # ----------------
    def show_menu(self):
        # self.check_automatic_plugins()
        self.menu.present()
        self.showing = True

    def hide_menu(self):
        self.menu.clear_bar()
        self.menu.hide()
        self.showing = False


    # ---------
    #  Actions
    # ---------
    def run_internal_command(self, cmd):
        if cmd == 'clear':
            pass #cache.clear_cache()
        elif cmd == 'update':
            pass # update cache

    def actionate(self):

        match = self.menu.selected_item()
        if match is None:
            return

        match_actions = match.get_actions()
        if self.menu.right_item_selected >= 0:
            action_name = match_actions[self.menu.right_item_selected][1]
        else:
            action_name = match_actions[0][1]

        if action_name == 'explore':
            if os.path.isdir(match.arg) or os.path.isfile(match.arg):
                self.explore(match.arg)
            return

        try:
            action = getattr(actions, action_name)
        except:
            self.logger.error('action %s not implemented' % action_name)

        self.attic.add(self.menu.query, match, action_name)

        self.logger.info('executing: %s %s' % (action_name, match.arg))
        action(match.arg)

        self.hide_menu()


    # -----------
    #  Navigation
    # -----------
    def previous_query(self):
        self.menu.clear_bar()
        previous_query = self.attic.get_previous_query()
        if previous_query is not None:
            self.menu.addchar(previous_query)

    def next_query(self):
        self.menu.clear_bar()
        next_query = self.attic.get_next_query()
        if next_query is not None:
            self.menu.addchar(next_query)

    # def show_history(self):
    #     self.items = self.attic.get_history()
    #     self.menu.emit('menu-update')


    # ---------------
    # File navigation
    # ---------------
    def file_navigation_mode(self, query=None):
        if query is None:
            query = self.menu.query
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

            items.append(ItemUri(p, abspath))

        return sorted(items, key=lambda it: it.arg)

    def file_navigation_cd(self):
        if self.menu.selected_item() is not None:
            new_query = self.menu.selected_item().arg
            self.menu.addchar(new_query.replace(home_dir, '~'), True)

    def file_navigation_cd_back(self):
        query = os.path.expanduser(self.menu.query[:-1])
        idx = query.rfind('/')
        new_query = query[:idx]+'/'
        self.menu.addchar(new_query.replace(home_dir, '~'), True)

    def explore(self, arg):
        self.menu.addchar(arg.replace(home_dir, '~'), True)

    # --------
    #  Search
    # --------
    def do_cache_thread_search(self, gen_items, query, result):
        matches = search.filter_items(gen_items, query, min_score=60.0)
        result.extend(matches)

    def search(self, query):

        if not query:
            return

        self.logger.info('searching %s' % query)

        matches = []

        if self.preview is not None:
            self.preview.hide()


        # 0. check if match trigger: command('), navigation (~ o /)
        if query.startswith("'"):
            self.logger.info('shell command trigger')
            cmd = query[1:]
            it = ItemCmd("run '%s' in a shell" % cmd, cmd)
            it.score = 1000
            matches.append(it)


        # File navigation
        if self.file_navigation_mode(query):
            self.logger.info('file navigation: %s' % query)
            matches.extend(self.file_navigation(query))
            self.menu.items = matches
            self.menu.emit('menu-update')
            return

        # Check if match internal command
        if query in self.commands:
            pass #self.run_command(query)

        # Check if match any plugin trigger
        for plugin in self.manager.trigger_plugins.values():
            if plugin.match_trigger(query):
                matches.extend([ it for it in plugin.get_items(query) ])


        # if query == '.' and self.keyword_plugins:
        #     for kw, name in self.keyword_plugins.items():
        #         self.items.append(items_.ItemPlugin(name, kw))

        # 3. filter applications, files, bookmarks, system commands
        if not matches:
            if use_threads:
                result = []

                # # merge db and split in 4?
                # j1 = threading.Thread(target=self.do_cache_thread_search, args=(applications.get_items(), query, result))
                # j2 = threading.Thread(target=self.do_cache_thread_search, args=(files.get_items(), query, result))
                # j3 = threading.Thread(target=self.do_cache_thread_search, args=(bookmarks.get_items(), query, result))

                # j1.start()
                # j2.start()
                # j3.start()

                # j1.join()
                # j2.join()
                # j3.join()

            # matches.extend(result)
            else:
                for plugin in self.manager.plugins.values():
                    plugin_matches = search.filter_items(plugin.get_items(), query, min_score=60.0)
                    matches.extend(plugin_matches)


        # Fallback plugins
        if not matches:
            matches = self.manager.get_fallback_items(query)


        self.menu.items = self.sort_items(matches)
        self.menu.emit('menu-update')


    # --------
    #  Sort
    # --------
    def sort_items(self, items):

        for m in items:
            m.bonus = self.attic.get_item_bonus(m)

        items = sorted(items, key=lambda x: x.score+x.bonus, reverse=True)

        # self.items = [i for i in self.items if i.score > 60.]
        #if len(query) > 1:
        #self.items.extend(self.attic.get_similar(query))

        return items


    # -----------------
    #  File Preview
    # -----------------
    def toggle_preview(self):
        if self.preview is None:
            self.create_preview()
        elif self.preview is not None and self.preview.get_visible():
            self.preview.hide()
            self.menu.move(0.5*Gdk.Screen.width()-0.5*width, 0.5*Gdk.Screen.height()-0.5*height)
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

        path = self.menu.selected_item().arg

        pb = None
        # if path is an image
        try:
            pb = GdkPixbuf.Pixbuf.new_from_file(path)
        except:
            pass

        # if path is a pdf
        if pb is None and path.endswith('.pdf'):
            try:
                doc = Poppler.Document.new_from_file('file://%s' % path)

                page = doc.get_page(0)

                width, height = page.get_size()

                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
                ctx = cairo.Context(surface)
                ctx.save()
                page.render(ctx)
                ctx.restore()

                ctx.set_operator(cairo.OPERATOR_DEST_OVER)
                ctx.set_source_rgb(1, 1, 1)
                ctx.paint()

                pb = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)
            except:
                raise #pass

        if pb is None:
            self.preview.hide()
            return

        self.logger.info('showing preview for %s' % path)

        screen_w = Gdk.Screen.width()
        screen_h = Gdk.Screen.height()

        w, h = pb.get_width(), pb.get_height()

        max_w = 0.66*screen_w
        max_h = screen_h

        ratio = min(max_w/float(w), max_h/float(h))

        if w > max_w or h > max_h:

            new_w = w  * ratio
            new_h = h * ratio

            pb = pb.scale_simple(new_w, new_h, GdkPixbuf.InterpType.BILINEAR)

        self.image.set_from_pixbuf(pb)

        w, h = pb.get_width(), pb.get_height()
        self.preview.resize(w, h)

        xpos = 0.66 * screen_w - 0.5 * w
        ypos = 0.50 * screen_h - 0.5 * h
        self.preview.move(xpos, ypos)

        self.menu.move(20, 0.5*screen_h-0.5*self.menu.height)

        self.preview.show_all()
