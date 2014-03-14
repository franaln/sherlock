import sys, math, cairo
from gi.repository import Gtk, Gdk, GObject


class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # config
        self.height = 28
        self.width = 480
        self.line_height = 28
        self.lines = 5
        self.xoffset = 10
        self.yoffset = 6
        self.sf_color = (1, 1, 1)
        self.sb_color = (0.259, 0.498, 0.929)
        self.nf_color = (1, 1, 1)
        self.nb_color = (0.141, 0.141, 0.141)

        # data
        self.items = []
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

    def show_box(self):
        self.height = self.line_height * (self.lines + 1)
        self.resize(self.width, self.height)
        self.queue_draw()

    def hide_box(self):
        pass

    def add_char(self, char):
        self.query += char
        self.queue_draw()
        self.emit('query_changed', self.query)

    def rm_char(self):
        self.query = self.query[:-1]
        self.queue_draw()
        self.emit('query_changed', self.query)

    def draw_item(self, cr, pos, item, selected):
        x = 0
        y = (pos+1) * self.line_height

        # background rectangle
        if selected:
            self.draw_rect(cr, 0, y, self.width, y+self.line_height, self.sb_color)
        else:
            self.draw_rect(cr, 0, y, self.width, y+self.line_height, self.nb_color)

        # text
        self.draw_text(cr, x, y, item.title, self.nf_color)

    def draw_rect(self, cr, xb, yb, xe, ye, color):
        cr.set_source_rgb(*color)
        cr.rectangle(xb, yb, xe, ye)
        cr.fill()

    def draw_text(self, cr, base_x, base_y, text, color):
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(14)

        (x_bearing, y_bearing, text_width, text_height) = cr.text_extents(text)[:4]

        x = base_x + self.xoffset
        y = base_y + self.line_height/2 - (text_height/2 + y_bearing) # centered

        cr.move_to(x, y)
        cr.set_source_rgb(*color)
        cr.show_text(text)

    def draw(self, widget, event):

        # get cairo context
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*self.nb_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw search entry
        self.draw_rect(cr, 0, 0, self.width, self.line_height, self.nb_color)

        self.draw_text(cr, 0, 0, self.query, self.nf_color)
        # cr.set_source_rgb(*self.nf_color)
        # cr.set_line_width(1)
        # cr.move_to(10, 2)
        # cr.line_to(10, self.line_height-2)
        # cr.stroke()

        if not self.items:
            return

        show_items = []
        if self.selected < self.lines:
            first_item = 0 #self.selected
        else:
            first_item = self.selected - self.lines + 1

        max_items = min(5,len(self.items))

        for i in range(max_items):
            self.draw_item(cr, i, self.items[first_item+i], (first_item+i == self.selected))

        return False

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
