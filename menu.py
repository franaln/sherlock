import sys, math, cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango, PangoCairo

import config

class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # config
        self.width = 480
        self.height = 60

        self.offset = 6
        self.bar_width  = self.width - 12
        self.bar_height = self.height - 12
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
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)

        self.set_title('Sherlock')

        self.set_size_request(self.width, self.height)

        self.connect('draw', self.draw)

        self.show_all()

    def get_selected(self):
        return self.selected

    def show_menu(self, items=None):
        if items is not None:
            self.items = list(items)
        self._show_box()

    def hide_menu(self):
        self._hide_box()

    def clear_menu(self):
        self.items = []
        self.selected = 0
        self._hide_box()

    def select_next(self):
        if self.selected == len(self.items) - 1:
            return
        self.selected += 1
        self.queue_draw()

    def select_prev(self):
        if self.selected == 0:
            self._hide_box()
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

    def _show_box(self):
        self.resize(self.width, self.height+self.item_height * self.lines)
        self.queue_draw()

    def _hide_box(self):
        self.resize(self.width, self.height)
        self.queue_draw()

    def draw_rect(self, cr, x, y, width, height, color):
        cr.set_source_rgb(*color)
        cr.rectangle(x, y, width, height)
        cr.fill()

    def draw_text(self, cr, x, y, text, color, size=12, cursor=False):
        layout = PangoCairo.create_layout(cr)
        fontname = config.font
        font = Pango.FontDescription('%s %s' % (fontname, size))
        layout.set_font_description(font)

        layout.set_text(u'%s' % text, -1)
        cr.set_source_rgb(*color)
        PangoCairo.update_layout(cr, layout)

        width, height = layout.get_pixel_size()

        cr.move_to(x, y - height/2)
        PangoCairo.show_layout(cr, layout)

        return (width, height)

    def draw(self, widget, event):
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*config.menu_bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw query entry
        self.draw_query(cr)

        # draw items box if there are items to show
        if not self.items:
            return

        first_item =  0 if (self.selected < self.lines) else (self.selected - self.lines + 1)
        max_items = min(self.lines, len(self.items))

        for i in range(max_items):
            self.draw_item(cr, i, self.items[first_item+i], (first_item+i == self.selected))

        return False

    def draw_query(self, cr):
        self.draw_rect(cr, self.offset, self.offset, self.bar_width,
                       self.bar_height, config.query_bkg_color)

        (w, h) = self.draw_text(cr, self.offset + 10, self.offset + self.bar_height/2,
                       self.query, config.query_text_color, 28, True)

        # cursor
        cursor_x = self.offset + 12 + w
        self.draw_rect(cr, cursor_x, self.offset+5, 1, self.bar_height-10, config.query_cur_color)

    def draw_item(self, cr, pos, item, selected):

        """
        ---------------------------------
        | title                 | more  |
        | subtitle              |       |
        ---------------------------------
        """

        # pos to (x, y)
        base_x = 0
        base_y = self.height + pos * self.item_height

        # horizontal line below
        y = base_y + self.item_height - 1
        cr. move_to(10, y)
        cr.set_source_rgb(*config.menu_sep_color)
        cr.set_line_width(0.8)
        cr.line_to(self.width-10, y)
        cr.stroke()

        # selected background
        if selected:
            self.draw_rect(cr, base_x, base_y, self.width, self.item_height, config.menu_sel_color)

        # icon (not icon for now!)
        #x = base_x + 5
        #y = base_y + (self.item_height - 40) / 2

        #icon_size = 40

        #cr.save()
        #cr.translate(x, y)

        #cr.rectangle(0, 0, icon_size, icon_size)
        #cr.clip ()

        # name = '/usr/share/icons/hicolor/48x48/apps/evince.png'
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(item.icon, icon_size, icon_size)
        # pixbuf = add_background(pixbuf)

        # Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        # cr.paint()

        #cr.restore()

        # title
        x = base_x + 10 #+ 60
        y = base_y + self.item_height * (3/8)
        if selected:
            self.draw_text(cr, x, y, item.title, (1, 1, 1))
        else:
            self.draw_text(cr, x, y, item.title, config.menu_title_color)

        # subtitle
        x = base_x + 10 #+ 60
        y = base_y + (3/4) * self.item_height
        if selected:
            self.draw_text(cr, x, y, item.subtitle, (1, 1, 1), 8)
        else:
            self.draw_text(cr, x, y, item.subtitle, config.menu_sub_color, 8)

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
