#!/usr/bin/env python

import sys, math, cairo
from gi.repository import Gtk, Gdk, GObject

from menu import Menu
from plugins.applications import Applications

class Main():

    def __init__(self):

        self.menu = Menu()
        self.menu.connect('key_press_event', self.on_key_press)
        self.menu.connect('delete-event', self.close)
        self.menu.connect('query_changed', self.on_query_changed)

        self.plugin = Applications()


    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        Gtk.main_quit()

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
            pass
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


    def reset_search(self):
        self.menu.clear()

    def on_query_changed(self, widget, query):
        if not query:
            self.reset_search()
            return

        matches = self.plugin.get_matches(query)

        print('%s > %s' % (query, matches))

        self.menu.show(matches)

        # results = Results()

        # self.results_box.clear()
        # for match in matches:
        #     self.results_box.add_result(match)

        # self.results_box.show()
