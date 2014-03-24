import sys, math, cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango, PangoCairo

#-- Menu config
menu_font = 'Sans'

# Query colours
bar_bkg_color  = (0.8, 0.8, 0.8) # '#141414'
bar_text_color = (0.1, 0.1, 0.1)
bar_cur_color  = (0.3, 0.3, 0.3)

# Menu colours
menu_bkg_color   = (0.92, 0.92, 0.92)    # #ebebeb
menu_sel_color   = (0.259, 0.498, 0.929) # #427fed
menu_title_color = (0.1, 0.1, 0.1)       # #030303
menu_sub_color   = (0.2, 0.2, 0.2)       # #050505
menu_sep_color   = (0.8, 0.8, 0.8)

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
        self.query = ''
        self.cursor = 0
        self.items = []
        self.selected = 0

        self.action_panel_visible = False
        self.actions = []
        self.action_selected = 0

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
        self.show_all()

    def get_selected(self):
        return self.selected

    def show_menu(self, items=None):
        if items is not None:
            self.items = list(items)
        self.resize(self.width, self.height+self.item_height * self.lines)
        self.queue_draw()

    def hide_menu(self):
        self.resize(self.width, self.height)
        self.queue_draw()

    def clear_menu(self):
        self.items = []
        self.selected = 0
        self.hide_menu()

    def toggle_action_panel(self):
        if self.action_panel_visible:
            self.actions = []
            self.action_panel_visible = False
        else:
            # check if selected item has actions
            self.actions = ['Run', 'Open', 'Copy']
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

    # Cairo draw
    def draw_rect(self, cr, x, y, width, height, color):
        cr.set_source_rgb(*color)
        cr.rectangle(x, y, width, height)
        cr.fill()

    def draw_text(self, cr, x, y, text, color, size=12, cursor=False):
        layout = PangoCairo.create_layout(cr)
        fontname = menu_font
        font = Pango.FontDescription('%s %s' % (fontname, size))
        layout.set_font_description(font)

        layout.set_text(u'%s' % text, -1)
        cr.set_source_rgb(*color)
        PangoCairo.update_layout(cr, layout)

        width, height = layout.get_pixel_size()

        cr.move_to(x, y - height/2)
        PangoCairo.show_layout(cr, layout)

        return (width, height)

    def draw_query(self, cr):
        self.draw_rect(cr, self.offset, self.offset, self.bar_width,
                       self.bar_height, bar_bkg_color)

        (w, h) = self.draw_text(cr, self.offset + 10, self.offset + self.bar_height/2,
                       self.query, bar_text_color, 28, True)

        # cursor
        cursor_x = self.offset + 12 + w
        self.draw_rect(cr, cursor_x, self.offset+5, 1, self.bar_height-10, bar_cur_color)

    def draw_separator(self, cr, x, y, size, orientation='h'):
        cr.set_source_rgb(*menu_sep_color)
        cr.set_line_width(0.8)
        cr.move_to(x, y)
        if orientation == 'h':
            cr.line_to(x+size, y)
        elif orientation == 'v':
            cr.line_to(x, y+size)
        cr.stroke()

    def draw_item(self, cr, pos, item, selected):
        """
        ---------------------------------
        | text                  | more  |
        | subtext               |       |
        ---------------------------------
        """

        # pos to (x, y)
        base_x = 0
        base_y = self.height + pos * self.item_height

        # separator
        y = base_y + self.item_height - 1
        self.draw_separator(cr, 0, y, self.width)

        # selected background
        if selected:
            self.draw_rect(cr, base_x, base_y, self.width,
                           self.item_height, menu_sel_color)

        if item.get('subtext', False):
            # text
            x = base_x + 10
            y = base_y + self.item_height * 0.375
            if selected:
                self.draw_text(cr, x, y, item.get('text'), (1, 1, 1))
            else:
                self.draw_text(cr, x, y, item.get('text'), menu_title_color)

            # subtext
            x = base_x + 10
            y = base_y + 0.75 * self.item_height
            if selected:
                self.draw_text(cr, x, y, item.get('subtext'), (1, 1, 1), 8)
            else:
                self.draw_text(cr, x, y, item.get('subtext'), menu_sub_color, 8)

        else:
            # text
            x = base_x + 10
            y = base_y + 0.5 * self.item_height
            if selected:
                self.draw_text(cr, x, y, item.get('text'), (1, 1, 1))
            else:
                self.draw_text(cr, x, y, item.get('text'), menu_title_color)

        if selected:
            cr.set_source_rgb(1, 1, 1)
            cr.set_line_width(1.5)
            cr.move_to(self.width-20, base_y + self.item_height/2 + 4)
            cr.rel_line_to(4, -4)
            cr.rel_line_to(-4, -4)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

    def draw_action_panel(self, cr):
        base_x = 0.7 * self.width
        width = self.width - base_x

        self.draw_rect(cr, base_x, self.height, width,
                       5*self.item_height, menu_bkg_color)

        cr. move_to(base_x+5, self.bar_height)
        cr.set_source_rgb(*menu_sep_color)
        cr.set_line_width(0.8)
        cr.line_to(base_x+5, self.bar_height + 5 * self.item_height)
        cr.stroke()

        for pos, action in enumerate(self.actions):

            base_y =  self.height + pos * self.item_height

            if self.action_selected == pos:
                self.draw_rect(cr, base_x, base_y, self.width,
                               self.item_height, menu_sel_color)

            self.draw_text(cr, base_x+10, base_y + 0.5*self.item_height,
                           action, menu_title_color)

            self.draw_separator(cr, base_x, base_y+self.item_height-1, width)


    def draw(self, widget, event):
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*menu_bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw bar
        self.draw_query(cr)

        # draw menu if items
        if not self.items:
            return

        first_item =  0 if (self.selected < self.lines) else \
                      (self.selected - self.lines + 1)

        max_items = min(self.lines, len(self.items))

        for i in range(max_items):
            self.draw_item(cr, i, self.items[first_item+i],
                           (first_item+i == self.selected))

        # draw actions
        if self.action_panel_visible:
            self.draw_action_panel(cr)

        return False
