# Sherlock main

import os
import sys
import json
import time
import logging
import importlib
import threading
import datetime

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Poppler', '0.18')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf, Poppler, Pango, PangoCairo

import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib

from sherlock.manager import Manager
from sherlock.attic import Attic
from sherlock.clipboard import Clipboard

from sherlock import config
from sherlock import utils
from sherlock import search
from sherlock.drawutils import *
from sherlock import actions

config_dir = os.path.expanduser('~/.config/sherlock')
cache_dir  = os.path.expanduser('~/.cache/sherlock/')
attic_path = os.path.join(cache_dir, 'attic.json')
clipboard_path = os.path.join(cache_dir, 'clipboard.json')

lock = threading.Lock()

use_threads = False

home_dir = os.environ['HOME']

## Size (hardcoded)
win_width  = 800
win_height = 500
bar_w = 800
bar_h = 90
menu_w = 800
menu_h = 410
item_h = 82
item_m = 41
right_x = 500
right_w = 300
query_x = 25
query_y = bar_h * 0.5

# Font/Colors
fontname      = config.fontname
bkg_color     = config.background_color
bar_color     = config.bar_color
sep_color     = config.separator_color
sel_color     = config.selection_color
text_color    = config.text_color
subtext_color = config.subtext_color
seltext_color = config.seltext_color

# modes
MODE_NORMAL          = 0
MODE_HISTORY         = 1
MODE_FILE_NAVIGATION = 2
MODE_CLIPBOARD       = 3

mode_labels = {
    MODE_NORMAL:          '',
    MODE_HISTORY:         'Sherlock History',
    MODE_FILE_NAVIGATION: 'File Navigation',
    MODE_CLIPBOARD:       'Clipboard History',
}


class Sherlock(GObject.GObject):

    __gsignals__ = {
        'bar-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'query-change': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'menu-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__ (self, debug):

        GObject.GObject.__init__(self)

        self.running = False
        self.showing = False

        self.debug = debug

        # logger
        formatter = '[%(asctime)s] %(levelname)s (%(name)s) %(message)s'
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

        # Manager & Attic & Clipboard
        self.manager = Manager(config)
        self.attic = Attic(attic_path)
        # self.clipboard = Clipboard(clipboard_path)

        self.commands = [
            'quit',
            'update',
            'reload',
        ]

        self.mode = MODE_NORMAL

        # Menu
        self.items = []
        self.item_selected = 0

        self.right_items = []
        self.right_item_selected = 0
        self.right_panel_visible = False

        self.menu = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.menu.set_app_paintable(True)
        self.menu.set_decorated(False)
        self.menu.set_size_request(win_width, win_height)
        self.menu.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.menu.set_keep_above(True)
        self.menu.set_title('Sherlock')

        self.menu.connect('draw', self.draw)

        # Bar
        self.cursor = 0
        self.query = ''
        self.selected = False
        self.counter = 0
        self.updated = False

        GLib.timeout_add(500, self.check) # TODO deactive on hide!

        self.connect('bar-update', self.on_bar_update)

        # recreate db
        self.manager.update_cache()
        GLib.timeout_add_seconds(3600, self.manager.update_cache)

        # preview
        self.preview = None

        #
        self.menu.connect('delete-event', Gtk.main_quit)
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('focus-out-event', self.on_hide_menu)

        self.connect('menu-update', self.on_menu_update)
        self.connect('query-change', self.on_query_change)


    # -------------
    #  Run & close
    # -------------
    def run(self):
        if self.running:
            if not self.showing:
                self.show_menu()
            else:
                self.hide_menu()
        else:
            self.running = True
            Gtk.main()
            #self.running = False

    def close(self, *args):
        self.logger.info('closing...')
        self.attic.save()
        #self.clipboard.save()
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
        self.hide_right_panel()
        self.clear_menu()

        if not query:
            self.emit('menu-update')
            return

        if self.mode == MODE_FILE_NAVIGATION:
            self.handle_query_file_navigation_mode(query)

        elif self.mode == MODE_CLIPBOARD:
            self.handle_query_clipboard_mode(query)

        elif self.mode == MODE_HISTORY:
            self.handle_query_history_mode(query)

        # MODE_NORMAL
        else:
            self.search(query)

    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)

        # CTRL is pressed
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if key == 'Left':
                self.move_cursor_left()
            elif key == 'Right':
                self.move_cursor_right()
            elif key == 'Up':
                if self.item_selected >= 0:
                    self.addchar(self.items[self.item_selected].arg, True)
                else:
                    self.previous_query()

            elif key == 'Down':
                self.next_query()
            elif key == 'a':
                self.move_cursor_begin()
            elif key == 'e':
                self.move_cursor_end()
            elif key == 'BackSpace':
                self.clear_bar()
            elif 'space' in key:
                self.toggle_preview()
            elif key == 'y':
                selected_text = self.clipboard.get_text()
                if selected_text:
                    self.addchar(selected_text)

            # modes
            elif key == 'h':
                self.change_mode(MODE_HISTORY)
                self.show_history()

            elif key == 'v':
                self.change_mode(MODE_CLIPBOARD)
                self.show_clipboard_history()

            elif key == 'f':
                self.enter_file_navigation_mode()

            return

        if key == 'Escape':
            if self.mode != MODE_NORMAL:
                self.back_to_normal_mode()
            else:
                self.hide_menu()

        elif key == 'Down':
            # if not self.menu_visible:
            #     if self.bar.is_empty():
            #         self.show_history()
            #     if self.matches:
            #         self.show_menu()
            # else:
            self.select_down()

        elif key == 'Up':
            # if not self.menu_visible and self.bar.is_empty():
            #     #self.bar.select()
            #     #self.previous_query()
            # else:
            self.select_up()

        elif key == 'BackSpace':
            self.delchar()

        elif key == 'Delete':
            self.delchar(True)

        elif key == 'Left':
            if self.mode == MODE_FILE_NAVIGATION:
                self.file_navigation_cd_back()

        elif key == 'Right':
            if self.mode == MODE_FILE_NAVIGATION:
                self.file_navigation(self.selected_item().arg)
            else:
                if self.items:
                    self.toggle_right_panel()

        elif 'Return' in key:
            self.actionate()

        elif 'Tab' in key:
            if self.items:
                self.toggle_right_panel()

        elif 'Alt' in key or 'Control' in key:
            pass

        else:
            if event.string:
                self.addchar(event.string)


    # ----------------
    # Show / Hide menu
    # ----------------
    def show_menu(self):
        # self.check_automatic_plugins()
        self.clear_bar()
        self.menu.present()
        self.showing = True
        GLib.timeout_add(500, self.check)

    def hide_menu(self):
        self.clear_bar()
        self.manager.clear_cache()
        self.menu.hide()
        self.showing = False


    # ---------
    #  Actions
    # ---------
    def run_internal_command(self, cmd):
        if cmd == 'update':
            self.manager.update_cache()
        elif cmd  == 'reload':
            pass
        elif cmd  == 'quit':
            pass

    def actionate(self):

        match = self.selected_item()
        if match is None:
            return

        match_actions = self.manager.get_actions(match)
        if self.right_item_selected >= 0:
            action_name = match_actions[self.right_item_selected][1]
        else:
            action_name = match_actions[0][1]

        if action_name == 'explore':
            if os.path.isdir(match['arg']) or os.path.isfile(match['arg']):
                self.explore(match['arg'])
            return

        try:
            action = getattr(actions, action_name)
        except:
            self.logger.error('action %s not implemented' % action_name)

        self.attic.add(self.query, match, action_name)

        self.logger.info('executing action "%s" with arg "%s"' % (action_name, match['arg']))
        action(match['arg'])

        self.hide_menu()


    # -----------
    #  Navigation
    # -----------
    def previous_query(self):
        self.clear_bar()
        previous_query = self.attic.get_previous_query()
        if previous_query is not None:
            self.addchar(previous_query)

    def next_query(self):
        self.clear_bar()
        next_query = self.attic.get_next_query()
        if next_query is not None:
            self.addchar(next_query)

    # def show_history(self):
    #     self.items = self.attic.get_history()
    #     self.menu.emit('menu-update')



    #
    # Modes
    #
    def change_mode(self, mode):
        self.mode = mode
        self.logger.info('changing mode to: %s' % mode_labels[mode])

    def back_to_normal_mode(self):
        self.mode = MODE_NORMAL
        self.clear_bar()
        self.clear_menu()

    def handle_query_file_navigation_mode(self):
        pass

    def handle_query_history_mode(self):
        pass

    def handle_query_clipboard_mode(self):
        pass


    # ---------------------
    # File navigation mode
    # ---------------------
    def enter_file_navigation_mode(self):
        self.mode = MODE_FILE_NAVIGATION
        self.logger.info('changing mode to: FILE_NAVIGATION')

        query = self.query
        if not query:
            query = '/home/fran/'

        self.items  = self.file_navigation(query)
        self.emit('menu-update')

    def exit_file_navigation_mode(self):
        self.mode = MODE_NORMAL
        self.logger.info('changing mode to: NORMAL')

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
        for name in path_content:

            # exclude hidden files
            if name.startswith('.'):
                continue

            # filter by query
            if query and query.lower() not in name.lower():
                continue

            abspath = os.path.join(path, name)

            category = 'file'
            if os.path.isdir(path):
                category = 'dir'
                name = '%s/' % name
                abspath = '%s/' % abspath

            items.append({'text': name, 'subtext': abspath, 'category': category,
                              'keys': (name,), 'arg': abspath})

        return sorted(items, key=lambda it: it.arg)

    def file_navigation_cd(self):
        if self.selected_item() is not None:
            new_query = self.selected_item().arg
            self.addchar(new_query.replace(home_dir, '~'), True)

    def file_navigation_cd_back(self):
        query = os.path.expanduser(self.query[:-1])
        idx = query.rfind('/')
        new_query = query[:idx]+'/'
        self.addchar(new_query.replace(home_dir, '~'), True)

    def explore(self, arg):
        self.addchar(arg.replace(home_dir, '~'), True)


    # -----------
    #  Clipboard
    # -----------
    def show_clipboard_history(self):
        self.items = self.clipboard.get_history()
        self.emit('menu-update')


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

        # Check if match any trigger
        # command(')
        if query.startswith("'"):
            self.logger.info('shell command trigger')
            cmd = query[1:]
            it = {'text': "run '%s' in a shell" % cmd, 'subtext': cmd, 'arg': cmd}
            it['score'] = 1000
            matches.append(it)

        # File navigation ('~/' or '/')
        if query.startswith('/') or query.startswith('~/'):
            self.enter_file_navigation_mode()
            return

        # Check if match internal command
        if query.startswith('!') and query[1:] in self.commands:
            self.run_internal_command(query[1:])
            return

        # Check if match any plugin trigger
        for plugin in self.manager.trigger_plugins.values():
            if plugin.match_trigger(query):
                matches.extend([ it for it in plugin.get_items(query) ])

        # Filter non-trigger plugins
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
                    plugin_matches = search.filter_items(plugin.get_items(), query, min_score=80.0, max_results=10)
                    matches.extend(plugin_matches)

        # Fallback plugins
        if not matches:
            matches = self.manager.get_fallback_items(query)

        self.items = self.sort_items(matches)
        self.emit('menu-update')


    # --------
    #  Sort
    # --------
    def sort_items(self, items):

        # for m in items:
        #     m.bonus = self.attic.get_item_bonus(m)

        items = sorted(items, key=lambda x: x.get('score', 0), reverse=True)

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

    # ------
    #  Menu
    # ------
    def on_bar_update(self, widget):
        self.menu.queue_draw()

    def on_menu_update(self, widget):
        self.menu.queue_draw()

    def _update(self, text):
        self.counter = time.time()
        self.updated = True
        self.query = text
        self.emit('bar-update')

    def addchar(self, char, clear=False):
        if clear:
            self.clear_bar()
        newquery = '%s%s%s' % (self.query[:self.cursor], char, self.query[self.cursor:])
        self._update(newquery)
        self.cursor += len(char)

    def delchar(self, delete=False):
        if delete:
            newquery = '%s%s' % (self.query[:self.cursor], self.query[self.cursor+1:])
        else:
            if self.cursor == 0:
                newquery = self.query
            else:
                newquery = '%s%s' % (self.query[:self.cursor-1], self.query[self.cursor:])
                self.cursor -= 1
        self._update(newquery)

    def clear_bar(self):
        self.cursor = 0
        self._update('')

    def is_empty(self):
        return bool(not self.query)

    def check(self):
        if time.time() > (self.counter + 0.25) and self.updated:
            self.updated = False
            self.emit('query-change', self.query)

        if self.showing:
            return True
        else:
            return False

    def select(self):
        self.selected = True

    def move_cursor_begin(self):
        self.cursor = 0
        self.emit('bar-update')

    def move_cursor_end(self):
        self.cursor = len(self.query)
        self.emit('bar-update')

    def move_cursor_left(self):
        if self.cursor <= 0:
            return
        self.cursor -= 1
        self.emit('bar-update')

    def move_cursor_right(self):
        if self.cursor >= len(self.query):
            return
        self.cursor += 1
        self.emit('bar-update')

    def selected_item(self):
        if not self.items:
            return None
        return self.items[self.item_selected] if self.item_selected >=0 else self.items[0]

    def clear_menu(self):
        del self.items[:]
        self.item_selected = -1

    def toggle_right_panel(self):
        if self.right_panel_visible:
            self.hide_right_panel()
        else:
            self.show_right_panel()

    def hide_right_panel(self):
        if not self.right_panel_visible:
            return
        self.right_panel_visible = False
        self.right_items = []
        self.right_item_selected = 0
        self.emit('menu-update')

    def show_right_panel(self):
        match = self.selected_item()

        match_actions = self.manager.get_actions(match)

        if match_actions:
            self.right_items = list(match_actions)
        self.right_panel_visible = True
        self.emit('menu-update')

    def select_down(self):
        if self.right_panel_visible:
            if self.right_item_selected == len(self.right_items) - 1:
                return
            self.right_item_selected += 1
        else:
            if self.item_selected == len(self.items) - 1:
                return
            self.item_selected += 1

            # if self.preview is not None and self.preview.get_visible():
            #     self.update_preview()

        self.emit('menu-update')

    def select_up(self):
        if self.right_panel_visible:
            if self.right_item_selected == 0:
                return
            self.right_item_selected -= 1
        else:
            if self.item_selected == 0:
                return
            self.item_selected -= 1

            # if self.preview is not None and self.preview.get_visible():
            #     self.update_preview()

        self.emit('menu-update')


    def draw(self, widget, event):

        cr = Gdk.cairo_create(widget.get_window())

        draw_background(cr, bkg_color)

        # Bar

        draw_bar(cr, query_x, query_y, bar_w, bar_h, self.query, text_color, fontname, size=38)

        ## mode
        if mode_labels.get(self.mode, ''):
            draw_text(cr, 0.7*win_width, 20, 0.3*win_width-10, 0,
                      mode_labels[self.mode], text_color, fontname, 12, justification='right')

        ## bar/menu separator
        draw_horizontal_separator(cr, 0, bar_h-0.5, win_width, sep_color)

        # Menu
        items = self.items

        ## Info panel
        if not items:
            #     draw_rect(cr, right_x, bar_h+1, right_w, menu_h, bkg_color)

            today = datetime.datetime.today()

            # Date
            date_txt = today.strftime('%A, %d %b %Y')

            draw_text(cr, 0, bar_h+10, right_w, 80, date_txt, text_color, 20, justification='center')

            # Time
            time_1 = today.strftime('%H:%M')

            # h, m = [int(a) for a in today.strftime('%H:%M').split(':')]
            # if h < 5:
            #     time_2 = '%2i:%2i (Home)' % (24-h+5, m)
            # else:
            #     time_2 = '%2i:%2i (Home)' % (h-5, m)

            draw_text(cr, 0, bar_h+70,  right_w, 80, time_1, text_color, 28, justification='center')
            #draw_text(cr, right_x, bar_h+130, right_w, 80, time_2, text_color, 28, justification='center')

#     # Battery: Battery 0: Unknown, 98%
#     #acpi_output = utils.get_cmd_output(['acpi',])


#     # Volume

#     # Weather?

#     # RAM/CPU??
#     # raminfo = Popen(['free', '-m'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
#     # ram = ''.join(filter(re.compile('M').search, raminfo)).split()
#     # used = int(ram[2]) ##- int(ram[4]) - int(ram[5])
#     # usedpercent = ((float(used) / float(ram[1])) * 100)

#     # ramdisplay = '%s MB / %s MB' % (used, ram[1])

#     # draw_text(cr, right_x+10, bar_h+120, right_w, 82, ramdisplay, text_color, 16, center=True)

#     # user = os.getenv('USER')
#     # hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')

#     # p1 = Popen(['df', '-Tlh', '--total', '-t', 'ext4', '-t', 'ext3', '-t', 'ext2', '-t', 'reiserfs', '-t', 'jfs', '-t', 'ntfs', '-t', 'fat32', '-t', 'btrfs', '-t', 'fuseblk'], stdout=PIPE).communicate()[0].decode("Utf-8")
#     # total = p1.splitlines()[-1]
#     # used = total.split()[3]
#     # size = total.split()[2]
#     # usedpercent = float(total.split()[5][:-1])

#     # if usedpercent <= 33:
#     #     disk = '%s%s %s/ %s' % (colorDict['Sensors'][1], used, colorDict['Clear'][0], size)
#     # if usedpercent > 33 and usedpercent < 67:
#     #     disk = '%s%s %s/ %s' % (colorDict['Sensors'][2], used, colorDict['Clear'][0], size)
#     # if usedpercent >= 67:
#     #     disk = '%s%s %s/ %s' % (colorDict['Sensors'][0], used, colorDict['Clear'][0], size)


        else:

           ## Items
           left_w = win_width if not self.right_panel_visible else right_x


           first_item = 0 if (self.item_selected < 5) else (self.item_selected - 4)

           n_items = len(items)
           max_items = min(5, n_items)

           for pos in range(max_items):
               # self.draw_item(cr, i, items[first_item + i],
               #                (first_item + i == self.item_selected), left_w)

               """
               --------------------------------
               | IC | Text                    |
               | ON | Subtext                 |
               --------------------------------
               """

               item = items[first_item + pos]
               selected = (first_item + pos == self.item_selected)

               # pos -> (x, y)
               base_y = bar_h + pos * item_h

               if pos == 0:
                   draw_horizontal_separator(cr, -5, base_y, left_w, sep_color)

               if selected:
                   draw_rect(cr, 0, base_y-1, left_w, item_h+1, sel_color)
               elif pos < 4:
                   draw_horizontal_separator(cr, 0, base_y+item_h, left_w, sep_color)

               text_h = item_m
               text = item['text']

               text_x = 20

               # icon
               if 'icon' in item:
                   cr.save()
                   self.draw_icon(cr, item, 10, base_y+0.5*item_h-14)
                   cr.restore()
                   text_x = 50

               left_text_w = left_w - 2 * text_x

               if item['subtext']:
                   if selected:
                       draw_text(cr, text_x, base_y+6, left_text_w, text_h, text, seltext_color, fontname, 20)
                   else:
                       draw_text(cr, text_x, base_y+6, left_text_w, text_h, text, text_color,    fontname, 20)

                   y = base_y + item_h * 0.5
                   if selected:
                       draw_text(cr, text_x, y, left_text_w, text_h, item['subtext'], seltext_color, fontname, 10)
                   else:
                       draw_text(cr, text_x, y, left_text_w, text_h, item['subtext'], subtext_color, fontname, 10)

               else:
                   if selected:
                       draw_text(cr, text_x, base_y, left_text_w, item_h, text, seltext_color, fontname, 20)
                   else:
                       draw_text(cr, text_x, base_y, left_text_w, item_h, text, text_color, fontname, 20)

               # Default action and more actions arrow
               if selected:
                   try:
                       action_name = self.manager.get_actions(item)[0][0]
                       draw_text(cr, left_w + right_w*0.5, base_y, right_w, item_h, action_name, seltext_color, fontname, 12)
                   except:
                       pass

                   # arrow
                   draw_small_arrow(cr, left_w-15, base_y + item_m + 4)


           ## Right panel
           if self.right_panel_visible:

               draw_rect(cr, right_x, bar_h, right_w, menu_h, bkg_color)

               for pos, action in enumerate(self.right_items):

                   base_y =  bar_h + item_h * pos

                   draw_horizontal_separator(cr, right_x, base_y+81, right_w, sep_color)

                   if self.right_item_selected == pos:
                       draw_rect(cr, right_x, base_y, right_w, 82, sel_color)
                       draw_text(cr, right_x+10, base_y, right_w, 82, action[0], seltext_color, fontname)
                   else:
                       draw_text(cr, right_x+10, base_y, right_w, 82, action[0], text_color, fontname)


               draw_vertical_separator(cr, right_x, bar_h, menu_h, sep_color)

        return False

    def draw_icon(self, cr, item, x, y):

        pixel_size = 28

        cr.translate (x, y)
        cr.rectangle(0, 0, pixel_size, pixel_size)
        cr.clip()

        icon_theme = Gtk.IconTheme.get_default()
        icon_pixbuf = icon_theme.load_icon(item.icon, pixel_size, Gtk.IconLookupFlags.FORCE_SIZE)

        Gdk.cairo_set_source_pixbuf(cr, icon_pixbuf, 0, 0);
        cr.paint()




class SherlockDbus(dbus.service.Object):

    def __init__(self, bus, path, name, debug):
        dbus.service.Object.__init__(self, bus, path, name)
        self.app = Sherlock(debug)

    @dbus.service.method("org.sherlock.Daemon", in_signature='', out_signature='')
    def run(self):
        self.app.run()

    @dbus.service.method("org.sherlock.Daemon", in_signature='', out_signature='')
    def close(self, *args):
        self.app.close()
