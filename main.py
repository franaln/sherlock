import sys, math

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import cairo

from widgets import SearchBar, ResultsBox
from plugins.applications import Applications

class Result:
    def __init__(self, name, description, time):
        self.name = name
        self.description = description
        self.time = time

class Sherlock:

    def __init__(self):

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)

        self.window.set_default_size(500, 500)
        self.window.set_decorated(False)
        #self.window.set_resizable(False)
        self.window.set_app_paintable(True)
        self.window.skip_taskbar_hint = True
        self.window.skip_pager_hint = True
        self.window.set_position(Gtk.WindowPosition.CENTER)
        #self.window.set_type_hint(Gdk.WindowTypeHint.SPLASHSCREEN)
        self.window.set_keep_above (True)

        self.window.connect('key_press_event', self.on_key_press)
        self.window.connect('delete_event', self.close)

        #if (widget.get_realized ()) make_transparent_bg (widget);

        def make_transparent_bg(widget):
            window = widget.get_window()
            window.set_background_rgba(Gdk.RGBA(0, 0, 0, 0));

        def on_style_updated(widget):
            if widget.get_realized ():
                make_transparent_bg (widget)
                widget.queue_draw()

        def on_composited_change(widget):
            if widget.is_composited ():
                make_transparent_bg (widget);
            else:
                widget.override_background_color(Gtk.StateFlags.NORMAL, None)

        id1 = self.window.connect('realize', make_transparent_bg);
        id2 = self.window.connect('style_updated', on_style_updated);
        id3 = self.window.connect('composited_changed', on_composited_change)

        self.window.disconnect(id1) #realize.disconnect (make_transparent_bg);
        self.window.disconnect(id2) #style_updated.disconnect (on_style_updated);
        self.window.disconnect(id3) #composited_changed.disconnect (on_composited_change);

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # self.action_selector = ActionSelector()
        # for name in ['Apps', 'All']:
        #     self.action_selector.add_name(name)

        self.search_bar = SearchBar()

        self.search_bar.connect('search-changed', self.on_search_changed)

        self.results_box = ResultsBox()


        #self.results_box.add_result(Result('Match1', 'Description1', 1394574398.249458))
        #self.results_box.add_result(Result('Match2', 'Description2', 25.3))
        #self.results_box.add_result(Result('Match3', 'Description3', 25.3))

        # self.head_label = Gtk.Label("Search > Local content")
        # self.head_label.xalign =  0.0;
        # self.head_label.xpad = 2
        # self.head_label.ypad = 2
        # self.main_vbox.pack_start(self.head_label, False);

        # self.left_vbox = Gtk.VBox(False, 4)
        # self.main_image = Gtk.Image()
        # self.main_image.set_pixel_size(self.ICON_SIZE);
        # self.main_image.set_size_request(self.im_size, self.im_size);
        # self.main_image.set_from_icon_name('search', Gtk.IconSize.DIALOG);

        # self.main_label = Gtk.Label('Type to search')
        # self.main_label.set_ellipsize (Pango.EllipsizeMode.END)
        # self.left_vbox.pack_start(main_image, False, True, 0)
        # self.left_vbox.pack_start(main_label, False, True, 0)

        # self.right_vbox = Gtk.VBox(False, 4)
        # self.action_image = Gtk.Image ();
        # self.action_image.set_pixel_size (self.ICON_SIZE);
        # self.action_image.set_size_request (self.im_size, self.im_size);
        # self.action_image.set_from_icon_name('system-run', Gtk.IconSize.DIALOG);

        # self.action_label = Gtk.Label('');
        # self.right_vbox.pack_start(self.action_image, False, True);
        # self.right_vbox.pack_start(self.action_label, False, True)

        # self.hbox = GTk.HBox(False, 6)
        # self.hbox.pack_start(self.left_vbox, False, False, 0)
        # self.hbox.pack_start(self.right_vbox, False, False, 0)

        #self.main_box.pack_start(self.action_selector, False, True, 5)
        self.main_box.pack_start(self.search_bar, False, True, 5)
        self.main_box.pack_end(self.results_box, True, True, 5)

        # self.frame = Gtk.Frame()
        # self.frame.shadow_type = Gtk.ShadowType.OUT; #//ETCHED_OUT;
        # self.frame.add (self.main_box);
        # self.frame.show_all ()

        self.main_box.show_all()
        self.main_box.set_size_request (500, -1)

        self.window.add(self.main_box)


        #self.window.connect("draw", self.area_draw)
        # self.screen = self.window.get_screen()
        # self.visual = self.screen.get_rgba_visual()
        # if self.visual != None and self.screen.is_composited():
        #     print("yay")
        #     self.window.set_visual(self.visual)

        self.window.set_title('Sherlock')

        self.window.show()
        self.results_box.hide()

        self.plugin = Applications()


    # def cairo_rounded_rect(self, cr, x, y, w, h, r):
    #     y2 = y+h
    #     x2 = x+w

    #     cr.move_to (x, y2 - r);
    #     cr.arc (x+r, y+r, r, math.pi, math.pi * 1.5);
    #     cr.arc (x2-r, y+r, r, math.pi * 1.5, math.pi * 2.0);
    #     cr.arc (x2-r, y2-r, r, 0, math.pi * 0.5);
    #     cr.arc (x+r, y2-r, r, math.pi * 0.5, math.pi);


    # def area_draw(self, widget, cr):
    #     container_allocation = widget.get_allocation();

    #     BORDER_RADIUS = 2

    #     width = container_allocation.width + BORDER_RADIUS * 2;
    #     height = container_allocation.height + BORDER_RADIUS * 2;

    #     cr.translate(container_allocation.x - BORDER_RADIUS, container_allocation.y - BORDER_RADIUS);
    #     cr.translate (0.5, 0.5);
    #     cr.set_operator(cairo.OPERATOR_OVER);
    #     cr.translate (-0.5, -0.5);
    #     cr.save ();

    #     bg = widget.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)

    #     # pattern
    #     pat = cairo.LinearGradient(0, 0, 0, height);
    #     pat.add_color_stop_rgba(bg.red, bg.green, bg.blue, 0.0, 0.95)
    #     #cr.set_source_rgba (pat, 0.2, 1.0, StyleType.BG, StateFlags.NORMAL, Mod.NORMAL);
    #     #cr.set_source_rgba (pat, 1.0, 1.0, StyleType.BG, StateFlags.NORMAL, Mod.DARKER);
    #     self.cairo_rounded_rect (cr, 0, 0, width, height, BORDER_RADIUS);
    #     cr.set_source (pat);
    #     cr.set_operator(cairo.OPERATOR_SOURCE);
    #     cr.clip ();
    #     cr.paint ();
    #     cr.restore ();


        # cr.set_source_rgba(bg.red, bg.green, bg.blue, 1.0)

        # cr.set_operator(cairo.OPERATOR_SOURCE)
        # cr.paint()
        # cr.set_operator(cairo.OPERATOR_OVER)
        # #cr.restore()




    def run(self):
        Gtk.main()

    def close(self, arg1=None, arg2=None):
        Gtk.main_quit()


    def on_search_changed(self, entry):
        query = entry.get_text().lower()
        matches = self.plugin.get_matches(query)

        self.results_box.clear()
        for match in matches:
            self.results_box.add_result(Result(match, '', None))

        self.results_box.show()
        print('%s > %s' % (query, matches))

    # def key_press_event(self, event):
    #     #if (im_context.filter_keypress (event)) return true;

    #     key = event.keyval

    #     if key == Gdk.KeySyms.Return or \
    #        key == Gdk.KeySyms.KP_Enter or \
    #        key == Gdk.KeySyms.ISO_Enter:
    #         print("enter pressed")
    #         #   if (current_match != null && current_action != null)
    #         # {
    #         #   current_action.execute (current_match);
    #         #   hide ();
    #         #   search_reset ();
    #         # }
    #     elif key == Gdk.KeySyms.Delete or \
    #          key == Gdk.KeySyms.BackSpace:
    #         print('Delete')
    #         #search_delete_char ();

    #     elif key == Gdk.KeySyms.Escape:
    #       print("escape")
    #       # if (search_string != "")
    #       # {
    #       #   search_reset ();
    #       # }
    #       # else
    #       # {
    #       #   hide ();
    #       self.quit ()

    #     return True


    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        modifiers = Gtk.accelerator_get_default_mod_mask()


        if key == 'Escape':
            self.close()
        elif key == 'Left':
            self.action_selector.select_prev()
        elif key == 'Right':
            self.action_selector.select_next()
        elif key == 'Down':
            self.results_box.show()
        elif key == 'Up':
            self.results_box.hide()

        if event.state and Gdk.ModifierType.CONTROL_MASK:

            ## ctrl-q: exit
            if  key == 'q':
                self.close()

            # ## ctrl-f: find

            # ## ctrl-n: new note
            # elif key == 'n':
            #     self.new_note()

            # ## ctrl-e: edit note
            # elif key == 'e':
            #     self.edit_note()

            # ## ctrl-d: delete note
            # elif key == 'd':
            #     self.delete_note()

            # ## ctrl-h: hide window
            # elif self.stack.get_visible_child_name() == 'list' and key == 'h':
            #     self.show_hide()

            # ## ctrl-x: do nothing!
            # elif key == 'x':
            #     pass

            # ## ctrl-s: update current note content
            # elif key == 's':
            #     text = self.text_buffer.get_text(self.text_buffer.get_start_iter(),
            #                                      self.text_buffer.get_end_iter(), True)
            #     self.db.update_note_prop(self.current_idx, 'content', text)
