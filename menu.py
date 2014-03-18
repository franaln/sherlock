import sys, math, cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

white = (1.0, 1.0, 1.0)

query_color = (0.1, 0.1, 0.1)
title_color = (0.1, 0.1, 0.1) # #030303
subtitle_color = (0.2, 0.2, 0.2) # #050505

bkg_color      = (0.92, 0.92, 0.92) # #ebebeb
selected_color = (0.259, 0.498, 0.929) # #427fed
entry_color    = (0.8, 0.8, 0.8) # #141414
line_color     = (0.8, 0.8, 0.8)

def add_background(pixbuf, color=0xebebebff):
    """ adds a background with given color to
    the pixbuf and returns the result as new Pixbuf"""
    result = GdkPixbuf.Pixbuf().new(pixbuf.get_colorspace(),
                                    True,
                                    pixbuf.get_bits_per_sample(),
                                    pixbuf.get_width(),
                                    pixbuf.get_height(),
    )
    result.fill(color)
    pixbuf.composite(result, 0, 0,
                     pixbuf.get_width(), pixbuf.get_height(),
                     0, 0,
                     1, 1,
                     GdkPixbuf.InterpType.NEAREST,
                     255)
    return result




class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # config
        self.width = 480
        self.height = 60

        self.offset = 6
        self.bar_width  = self.width - self.offset * 2
        self.bar_height = self.height - self.offset * 2
        self.item_height = 48

        self.lines = 5
        self.max_items = 20

        # data
        self.items = []
        self.actions = []
        self.selected = 0
        self.query = ''

        GObject.GObject.__init__(self)
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_app_paintable(True)
        self.set_decorated(False)
        #self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)

        self.set_title('Sherlock')

        self.set_size_request(self.width, self.height)

        self.connect('draw', self.draw)
        self.connect('screen-changed', self.screen_changed)

        self.screen_changed(self)
        self.show_all()

    def show(self, items):
        self.items = list(items)
        self.show_box()

    def clear(self):
        self.items = []
        self.selected = 0
        self.hide_box()

    def show_box(self):
        self.resize(self.width, self.height+self.item_height * self.lines)
        self.queue_draw()

    def hide_box(self):
        self.resize(self.width, self.height)
        self.queue_draw()

    def add_char(self, char):
        self.query += char
        self.queue_draw()
        self.emit('query_changed', self.query)

    def rm_char(self):
        self.query = self.query[:-1]
        self.queue_draw()
        self.emit('query_changed', self.query)

    def do_query_changed(self, entry):
        self.waiting = False

    def show_actions(self):
        #if self.items.
        pass


    def draw_rect(self, cr, x, y, width, height, color):
        cr.set_source_rgb(*color)
        cr.rectangle(x, y, width, height)
        cr.fill()

    def draw_text(self, cr, x, y, text, color, size=14):
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(size)

        descent, font_height = cr.font_extents()[1:3]

        (x_bearing, y_bearing, text_width, text_height) = cr.text_extents(text)[:4]

        y = y - descent + font_height / 2

        cr.move_to(x, y)
        cr.set_source_rgb(*color)
        cr.show_text(text)


    def draw_icon(self, cr, icon, x, y):
        pass
        # ctx.save ();
        # ctx.translate (x, y);
        # draw_icon_in_position (ctx, m.icon_name, icon_size);
        # ctx.restore ();

    def draw_icon_in_position(self, cr, name, pixel_size):
        pass

    # def get_icon(self, name, pixel_size):
    #     if name == "":
    #         return None

    #     #string key = "%s|%d".printf (name,pixel_size);
    #     #info = map.get (key);

    #     if info is None:
    #         pixbuf = self.get_pixbuf(name, pixel_size)
    #         if pixbuf is None:
    #             pixbuf = get_pixbuf ("unknown", pixel_size)
    #         if pixbuf is None:
    #             return null
    #         info = PixbufInfo(pixbuf)
    #             map.set (key, info);
    #         }
    #         return info.pixbuf;
    #     }

    #     private Gdk.Pixbuf? get_pixbuf (string name, int pixel_size)
    #     {
    #         try {
    #                 var icon = GLib.Icon.new_for_string(name);
    #                 if (icon == null) return null;

    #                 Gtk.IconInfo iconinfo = this.theme.lookup_by_gicon (icon, pixel_size, Gtk.IconLookupFlags.FORCE_SIZE);
    #                 if (iconinfo == null) return null;

    #                 Gdk.Pixbuf icon_pixbuf = iconinfo.load_icon ();
    #                 if (icon_pixbuf != null) return icon_pixbuf;
    #         } catch (Error e) { }
    #         return null;




    def draw(self, widget, event):
        # get cairo context
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw search entry
        self.draw_rect(cr, self.offset, self.offset, self.bar_width,
                       self.bar_height, entry_color)
        self.draw_text(cr, self.offset + 10, self.offset + self.bar_height/2,
                       self.query, query_color, 32)

        # cursor
        # cr. move_to(self.offset + 15 + width, self.offset + self.bar_height - 2)
        # cr.set_source_rgb(*query_color)
        # cr.set_line_width(0.8)
        # cr.line_to(self.offset + 15 + width, self.offset + 2)
        # cr.stroke()


        # draw items box if there are items to show
        if not self.items:
            return

        first_item =  0 if (self.selected < self.lines) else (self.selected - self.lines + 1)
        max_items = min(self.lines, len(self.items))

        for i in range(max_items):
            self.draw_item(cr, i, self.items[first_item+i], (first_item+i == self.selected))

        return False

    def draw_item(self, cr, pos, item, selected):

        """
        ----------------------------------------
        | icon | title                 |       |
        |      | subtitle              |       |
        ----------------------------------------
        """

        # pos to (x, y)
        base_x = 0
        base_y = self.height + pos * self.item_height

        # horizontal line below
        y = base_y + self.item_height - 1
        cr. move_to(10, y)
        cr.set_source_rgb(*line_color)
        cr.set_line_width(0.8)
        cr.line_to(self.width-10, y)
        cr.stroke()

        # selected background
        if selected:
            self.draw_rect(cr, base_x, base_y, self.width, self.item_height, selected_color)

        # icon
        x = base_x + 5
        y = base_y + (self.item_height - 40) / 2

        icon_size = 40

        cr.save()
        cr.translate(x, y)

        cr.rectangle(0, 0, icon_size, icon_size)
        cr.clip ()

        name = '/usr/share/icons/hicolor/48x48/apps/evince.png'
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(name, icon_size, icon_size)
        pixbuf = add_background(pixbuf)

        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

        cr.restore()

        # title
        x = base_x + 60
        y = base_y + self.item_height * (3/8)
        if selected:
            self.draw_text(cr, x, y, item.title, (1, 1, 1))
        else:
            self.draw_text(cr, x, y, item.title, title_color)

        # subtitle
        x = base_x + 60
        y = base_y + (3/4) * self.item_height
        if selected:
            self.draw_text(cr, x, y, item.subtitle, (1, 1, 1), 10)
        else:
            self.draw_text(cr, x, y, item.subtitle, subtitle_color, 10)


        # if selected:
        #     default_action = 'Open'
        #     cr.set_font_size(10)
        #     text_width = cr.text_extents(default_action)[2]

        #     self.draw_text(cr, self.width-text_width-30, y, default_action, self.nf_color, 10)

        #     cr.set_source_rgb(*self.nf_color)
        #     cr.set_line_width(1.5)
        #     cr.move_to(self.width-10, y + self.item_height/2+4)
        #     cr.rel_line_to(4, -4)
        #     cr.rel_line_to(-4, -4)
        #     cr.set_line_join(cairo.LINE_JOIN_ROUND)
        #     cr.stroke()


    def select_next(self):
        if self.selected == len(self.items) - 1:
            return
        self.selected += 1
        self.queue_draw()

    def select_prev(self):
        if self.selected == 0:
            self.hide_box()
            return
        self.selected -= 1
        self.queue_draw()

    def screen_changed(self, widget, old_screen=None):
        """ If screen changes, it could be possible
        we no longer got rgba colors """
        screen = widget.get_screen()
        visual = screen.get_rgba_visual()
        if visual is None:
            visual = screen.get_rgba_visual()
            self.supports_alpha = False
        else:
            self.supports_alpha = True

        widget.set_visual(visual)
        return True
