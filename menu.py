import sys
import math
import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango, PangoCairo

import actions

#-- Menu config
fontname = 'Sans'

# Bar colours
bar_bkg_color  = (0.8, 0.8, 0.8) # #141414
bar_text_color = (0.1, 0.1, 0.1)
bar_cur_color  = (0.3, 0.3, 0.3)

# Menu colours
menu_bkg_color   = (0.92, 0.92, 0.92)    # #ebebeb
menu_sel_color   = (0.259, 0.498, 0.929) # #427fed
menu_text_color  = (0.1, 0.1, 0.1)       # #030303
menu_sep_color   = (0.8, 0.8, 0.8)
panel_bkg_color  = (0.8, 0.8, 0.8)


class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'query_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self):

        # sizes
        self.width = 480
        self.height = 60
        self.offset = 6
        self.item_height = 48 # = height - 2 * offset
        self.lines = 5

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

    def is_action_panel_visible(self):
        return self.action_panel_visible

    def hide_action_panel(self):
        self.action_panel_visible = False
        self.actions = []
        self.action_selected = 0
        self.queue_draw()

    def show_action_panel(self, actions=None):
        if actions is not None:
            self.actions = list(actions)
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

    #------------
    # Cairo draw
    #------------
    def draw_rect(self, cr, x, y, width, height, color):
        cr.set_source_rgb(*color)
        cr.rectangle(x, y, width, height)
        cr.fill()

    def draw_text(self, cr, x, y, text, color, size=12):
        layout = PangoCairo.create_layout(cr)
        font = Pango.FontDescription('%s %s' % (fontname, size))
        layout.set_font_description(font)
        layout.set_text(u'%s' % text, -1)
        cr.set_source_rgb(*color)
        PangoCairo.update_layout(cr, layout)

        width, height = layout.get_pixel_size()
        cr.move_to(x, y - height/2)
        PangoCairo.show_layout(cr, layout)
        return (width, height)

    def draw_bar(self, cr):
        """
                       6px
            ---------------------------
        6px |10px Query|              | 6px
            ---------------------------
                       6px
        """

        self.draw_rect(cr, 6, 6, self.width-12,
                       self.height-12, bar_bkg_color)

        (w, h) = self.draw_text(cr, 16, 30,
                       self.query, bar_text_color, 28)

        # cursor
        cursor_x = w + 18
        self.draw_rect(cr, cursor_x, 11, 2, 38, bar_cur_color)

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
        ---------------------------------------
        | TEXT                  | default |   |
        |                       |         | > |
        | subtext               | action  |   |
        ---------------------------------------
        """

        # pos -> (x, y)
        base_x = 0
        base_y = self.height + pos * self.item_height
        middle_y = base_y + self.item_height * 0.5

        # separator
        self.draw_separator(cr, 10, base_y+self.item_height-1, self.width-10)

        # selected background
        if selected:
            self.draw_rect(cr, base_x, base_y, self.width,
                           self.item_height, menu_sel_color)

        # text position
        x = base_x + 10

        if item.get('subtext', False):
            # text
            y = base_y + self.item_height * 0.375
            if selected:
                self.draw_text(cr, x, y, item.get('text'), (1, 1, 1))
            else:
                self.draw_text(cr, x, y, item.get('text'), menu_text_color)

            # subtext
            y = base_y + 0.75 * self.item_height
            if selected:
                self.draw_text(cr, x, y, item.get('subtext'), (1, 1, 1), 8)
            else:
                self.draw_text(cr, x, y, item.get('subtext'), menu_text_color, 8)

        else:
            # text
            if selected:
                self.draw_text(cr, x, middle_y, item.get('text'), (1, 1, 1))
            else:
                self.draw_text(cr, x, middle_y, item.get('text'), menu_text_color)

        # Default action and more actions arrow
        if selected:

            default_action_name = actions.actions[item.get('type')][0][0]
            self.draw_text(cr, self.width-60, middle_y, default_action_name, (1, 1, 1), 10)

            # arrow
            cr.set_source_rgb(1, 1, 1)
            cr.set_line_width(1.5)
            cr.move_to(self.width-10, base_y + 0.5 * self.item_height + 4)
            cr.rel_line_to(4, -4)
            cr.rel_line_to(-4, -4)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

    def draw_action_panel(self, cr):
        base_x = 0.7 * self.width
        width = self.width - base_x
        height = self.item_height * 0.6

        self.draw_rect(cr, base_x, self.height, self.width,
                       5*self.item_height, panel_bkg_color)

        #self.draw_separator(cr, base_x, self.height,
        #                    self.bar_height + 5 * self.item_height, 'v')

        for pos, action in enumerate(self.actions):

            base_y =  self.height + pos * height

            self.draw_separator(cr, base_x, base_y+height-1, width)

            text_color = menu_text_color

            if self.action_selected == pos:
                self.draw_rect(cr, base_x, base_y, width,
                               height, menu_sel_color)
                text_color = (1, 1, 1)

            self.draw_text(cr, base_x+10, base_y + 0.5*height,
                           action[0], text_color, 10)

    def draw(self, widget, event):
        cr = Gdk.cairo_create(widget.get_window())

        # draw window rectangle
        cr.set_source_rgb(*menu_bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        # draw bar
        self.draw_bar(cr)

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
