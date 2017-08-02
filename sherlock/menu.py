import time
from gi.repository import Gtk, Gdk, GObject, GLib

from sherlock import config

import cairo
import datetime
from gi.repository import Pango, PangoCairo, Gdk

from sherlock import items

# Font/Colors
fontname      = config.fontname
bkg_color     = config.background_color
bar_color     = config.bar_color
sep_color     = config.separator_color
sel_color     = config.selection_color
text_color    = config.text_color
subtext_color = config.subtext_color
seltext_color = config.seltext_color


def draw_background(cr):
    cr.set_source_rgb(*bkg_color)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

def draw_rect(cr, x, y, width, height, color=text_color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_horizontal_separator(cr, x, y, size):
    cr.set_source_rgb(*sep_color)
    cr.set_line_width(1.)
    cr.move_to(x+5, y)
    cr.line_to(x+size-5, y)
    cr.stroke()

def draw_vertical_separator(cr, x, y, size):
    cr.set_source_rgb(*sep_color)
    cr.set_line_width(0.8)
    cr.move_to(x, y+5)
    cr.line_to(x, y+size-5)
    cr.stroke()

def calc_text_width(cr, text, size):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    PangoCairo.update_layout(cr, layout)
    tw, th = layout.get_pixel_size()
    return tw

def draw_text(cr, x, y, w, h, text, color, size=12, center=False):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    layout.set_ellipsize(Pango.EllipsizeMode.END)
    layout.set_width(Pango.SCALE * w)
    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()
    cr.set_source_rgb(*color)
    if center:
        cr.move_to(x + (w*0.5 - tw*0.5), y + (h*0.5 - th*0.5))
    else:
        cr.move_to(x, y + (h*0.5 - th*0.5))
    PangoCairo.show_layout(cr, layout)

def draw_variable_text(cr, x, y, w, h, text, color=text_color, size=12):
    layout = PangoCairo.create_layout(cr)

    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    cr.set_source_rgb(*color)

    layout.set_text(u'%s' % text, -1)

    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()

    while tw > w:
        size = size - 1
        font = Pango.FontDescription('%s %s' % (fontname, size))
        layout.set_font_description(font)
        PangoCairo.update_layout(cr, layout)
        tw, th = layout.get_pixel_size()

    cr.move_to(x, y + (h*0.5 - th*0.5))
    PangoCairo.show_layout(cr, layout)




# def draw_info(cr):

#     draw_rect(cr, right_x, bar_h+1, right_w, menu_h, bkg_color)

#     today = datetime.datetime.today()

#     # Date
#     date_txt = today.strftime('%A, %d %b %Y')

#     draw_text(cr, right_x, bar_h+10, right_w, 80, date_txt, text_color, 20, center=True)

#     # Time
#     time_1 = today.strftime('%H:%M')

#     h, m = [int(a) for a in today.strftime('%H:%M').split(':')]
#     if h < 5:
#         time_2 = '%2i:%2i (Home)' % (24-h+5, m)
#     else:
#         time_2 = '%2i:%2i (Home)' % (h-5, m)

#     draw_text(cr, right_x, bar_h+70,  right_w, 80, time_1, text_color, 28, center=True)
#     draw_text(cr, right_x, bar_h+130, right_w, 80, time_2, text_color, 28, center=True)

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




class Menu(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'bar-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'query-change': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'menu-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self, config, debug):

        self.debug = debug

        # Sizes
        self.width  = 800
        self.height = 500 # 90 + 82*5

        self.bar_w = 800
        self.bar_h = 90

        self.menu_w = 800
        self.menu_h = 410

        self.item_h = 82
        self.item_m = 41

        self.right_x = 0.7 * self.width
        self.right_w = self.width - self.right_x
        self.left_w = self.right_x

        self.query_x = 25
        self.query_y = self.bar_h * 0.5

        # Bar
        self.cursor = 0
        self.query = ''
        self.selected = False
        self.counter = 0
        self.updated = False

        GObject.GObject.__init__(self)
        GLib.timeout_add(500, self.check)

        # Menu
        self.items = []
        self.item_selected = 0

        self.right_items = []
        self.right_item_selected = 0
        self.right_panel_visible = False

        # window
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_size_request(self.width, self.height)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_keep_above(True)
        self.set_title('Sherlock')

        self.connect('draw', self.draw)
        self.connect('bar-update', self.on_bar_update)

    def on_bar_update(self, widget):
        self.queue_draw()

    def on_menu_update(self, widget):
        self.queue_draw()


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
        return True

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

        match_actions = match.get_actions()

        if len(match_actions) < 2:
            return

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

    # ------
    #  Draw
    # ------
    def draw_bar(self, cr):

        ## query
        draw_variable_text(cr, self.query_x, self.query_y, self.bar_w-50, 0, self.query, size=38)

        ## cursor
        cursor_x = self.query_x + calc_text_width(cr, self.query[:self.cursor], size=38)

        cr.set_source_rgb(*config.text_color)
        cr.rectangle(cursor_x, 20, 1.5, self.bar_h-40)
        cr.fill()

        ## separator
        cr.set_source_rgb(*config.separator_color)
        cr.rectangle(0, 90, self.width, 1)
        cr.fill()

    def draw_left_side(self, cr):

        items = self.items

        first_item = 0 if (self.item_selected < 5) else (self.item_selected - 4)

        n_items = len(items)
        max_items = min(5, n_items)

        for i in range(max_items):
            self.draw_item(cr, i, items[first_item + i],
                      (first_item + i == self.item_selected), self.debug)

    def draw_right_side(self, cr):
        if self.right_panel_visible:
            self.draw_right_panel(cr, self.right_items, self.right_item_selected)

    def draw(self, widget, event):

        cr = Gdk.cairo_create(widget.get_window())

        draw_background(cr)

        self.draw_bar(cr)
        self.draw_left_side(cr)
        self.draw_right_side(cr)

        return False


    def draw_icon(self, cr, item, x, y):

        pixel_size = 28

        cr.translate (x, y)
        cr.rectangle(0, 0, pixel_size, pixel_size)
        cr.clip()

        icon_theme = Gtk.IconTheme.get_default()
        icon_pixbuf = icon_theme.load_icon("audio-volume-muted-blocked-panel", pixel_size, Gtk.IconLookupFlags.FORCE_SYMBOLIC)

        Gdk.cairo_set_source_pixbuf(cr, icon_pixbuf, 0, 0);
        cr.paint()


    def draw_item(self, cr, pos, item, selected, debug=False):

        """
        ---------------------------------
        |    | TEXT             |       |
        |    | subtext          |       |
        ---------------------------------
        """

        # pos -> (x, y)
        base_y = self.bar_h + pos * self.item_h

        if pos == 0:
            draw_horizontal_separator(cr, -5, base_y, self.width+10)

        if selected:
            draw_rect(cr, 0, base_y, self.width, self.item_h, sel_color)
        elif pos < 4:
            draw_horizontal_separator(cr, 0, base_y + self.item_h - 1, self.width)

        text_h = self.item_m
        title = item.title

        # icon
        # cr.save()
        # self.draw_icon(cr, item, 10, base_y+0.5*self.item_m)
        # cr.restore()

        # text
        if isinstance(title, list) or isinstance(title, tuple):

            title_list = title

            # divide text width in ncols columns
            ncols = len(title_list)
            col_w = int(self.left_w / ncols)

            space_w = calc_text_width(cr, ' ', 18)

            title = ''
            for i, l in enumerate(title_list):
                title += l

                space_px = int(col_w - calc_text_width(cr, l, 18))
                nspaces = int(space_px / space_w)

            title += ' '*nspaces

        if item.subtitle:
            if selected:
                draw_text(cr, 20, base_y+6, self.left_w, text_h, title, seltext_color, 20)
            else:
                draw_text(cr, 20, base_y+6, self.left_w, text_h, title, text_color, 20)

            y = base_y + self.item_h * 0.5
            if selected:
                draw_text(cr, 20, y, self.left_w, text_h, item.subtitle, seltext_color, 10)
            else:
                draw_text(cr, 20, y, self.left_w, text_h, item.subtitle, subtext_color, 10)

        else:
            if selected:
                draw_text(cr, 20, base_y, self.left_w, self.item_h, title, text_color, 20)
            else:
                draw_text(cr, 20, base_y, self.left_w, self.item_h, title, text_color, 20)

        # Default action and more actions arrow
        if debug:
            draw_text(cr, self.left_w + self.right_w*0.5, base_y, self.right_w, self.item_h, '%.2f (%.2f)' % (item.score, item.bonus), text_color, 10)

        elif selected:
            try:
                action_name = item.get_actions()[0][0]
                draw_text(cr, self.left_w + self.right_w*0.5, base_y, self.right_w, self.item_h, action_name, seltext_color, 12)
            except:
                pass

            # arrow
            cr.set_source_rgb(1, 1, 1)
            cr.set_line_width(1.5)
            cr.move_to(self.width-20, base_y + self.item_m + 4)
            cr.rel_line_to(4, -4)
            cr.rel_line_to(-4, -4)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

    def draw_right_panel(self, cr, actions, selected):

        draw_rect(cr, self.right_x, self.bar_h, self.right_w, self.menu_h, bkg_color)

        draw_vertical_separator(cr, self.right_x, self.bar_h, self.menu_h)

        for pos, action in enumerate(actions):

            base_y =  self.bar_h + 82 * pos

            draw_horizontal_separator(cr, self.right_x, base_y+81, self.right_w)

            if selected == pos:
                draw_rect(cr, self.right_x, base_y, self.right_w, 82, sel_color)
                draw_text(cr, self.right_x+10, base_y, self.right_w, 82, action[0], seltext_color)
            else:
                draw_text(cr, self.right_x+10, base_y, self.right_w, 82, action[0], text_color)
