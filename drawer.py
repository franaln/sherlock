# draw menu

import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango, PangoCairo

import config


def draw_rect(cr, x, y, width, height, color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_text(cr, x, y, text, color, size=12):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (config.fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    cr.set_source_rgb(*color)
    PangoCairo.update_layout(cr, layout)

    width, height = layout.get_pixel_size()
    cr.move_to(x, y - height/2)
    PangoCairo.show_layout(cr, layout)
    return (width, height)

def draw_window(cr):
    cr.set_source_rgb(*config.menu_bkg_color)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

def draw_bar(cr, query):
    """
    6px
    ---------------------------
    6px |10px Query|              | 6px
    ---------------------------
    6px
    """

    draw_rect(cr, 6, 6, config.width-12,
              config.height-12, config.bar_bkg_color)

    (w, h) = draw_text(cr, 16, 30,
                       query, config.bar_text_color, 28)

    # cursor
    draw_rect(cr, w + 18, 11, 2, 38, config.bar_cur_color)

def draw_separator(cr, x, y, size, orientation='h'):
    cr.set_source_rgb(*config.menu_sep_color)
    cr.set_line_width(0.8)
    cr.move_to(x, y)
    if orientation == 'h':
        cr.line_to(x+size, y)
    elif orientation == 'v':
        cr.line_to(x, y+size)
    cr.stroke()

def draw_item(cr, pos, item, selected):
    """
    ---------------------------------------
    | TEXT                  | default |   |
    | subtext               | action  |   |
    ---------------------------------------
    """

    # pos -> (x, y)
    base_x = 0
    base_y = config.height + pos * config.item_height
    middle_y = base_y + config.item_height * 0.5

    # separator
    draw_separator(cr, 10, base_y+config.item_height-1, config.width-10)

    # selected background
    if selected:
        draw_rect(cr, base_x, base_y, config.width,
                  config.item_height, config.menu_sel_color)

    # text position
    x = base_x + 10

    if item.subtitle:
        # text
        y = base_y + config.item_height * 0.375
        if selected:
            draw_text(cr, x, y, item.title, (1, 1, 1))
        else:
            draw_text(cr, x, y, item.title, config.menu_text_color)

        # subtext
        y = base_y + 0.75 * config.item_height
        if selected:
            draw_text(cr, x, y, item.subtitle, (1, 1, 1), 8)
        else:
            draw_text(cr, x, y, item.subtitle, config.menu_text_color, 8)

    else:
        # text
        if selected:
            draw_text(cr, x, middle_y, item.title, (1, 1, 1))
        else:
            draw_text(cr, x, middle_y, item.title, config.menu_text_color)

    # Default action and more actions arrow
    # if selected:

    #     default_action_name = actions.actions[item.category][0][0]
    #     draw_text(cr, width-60, middle_y, default_action_name, (1, 1, 1), 10)

    #     # arrow
    #     cr.set_source_rgb(1, 1, 1)
    #     cr.set_line_width(1.5)
    #     cr.move_to(width-10, base_y + 0.5 * item_height + 4)
    #     cr.rel_line_to(4, -4)
    #     cr.rel_line_to(-4, -4)
    #     cr.set_line_join(cairo.LINE_JOIN_ROUND)
    #     cr.stroke()


def draw_action_panel(cr, actions, selected):
    base_x = 0.7 * config.width
    width = config.width - base_x
    height = config.item_height * 0.6

    draw_rect(cr, base_x, config.height, config.width,
                       5*config.item_height, config.panel_bkg_color)

    #self.draw_separator(cr, base_x, self.height,
    #                    self.bar_height + 5 * self.item_height, 'v')

    for pos, action in enumerate(actions):

        base_y =  config.height + pos * height

        draw_separator(cr, base_x, base_y+height-1, width)

        text_color = config.menu_text_color

        if selected == pos:
            draw_rect(cr, base_x, base_y, width,
                               height, config.menu_sel_color)
            text_color = (1, 1, 1)

            draw_text(cr, base_x+10, base_y + 0.5*height,
                           action[0], text_color, 10)
