# drawer

import cairo
from gi.repository import Pango, PangoCairo

import config

fontname = config.fontname
bkg_color = config.bkg_color
bar_color = config.bar_color
sep_color = config.sep_color
sel_color = config.sel_color
text_color    = config.text_color
subtext_color = config.subtext_color
seltext_color = config.seltext_color

def draw_rect(cr, x, y, width, height, color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_separator(cr, x, y, size, orientation='h'):
    cr.set_source_rgb(*sep_color)
    cr.set_line_width(0.8)

    if orientation == 'h':
        cr.move_to(x+5, y)
        cr.line_to(x+size-5, y)
    elif orientation == 'v':
        cr.move_to(x, y+5)
        cr.line_to(x, y+size-5)
    cr.stroke()

def set_font(layout, size):
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)

def draw_text(cr, x, y, w, h, text, color, size=12):
    layout = PangoCairo.create_layout(cr)
    set_font(layout, size)
    layout.set_text(u'%s' % text, -1)
    layout.set_ellipsize(Pango.EllipsizeMode.END)
    layout.set_width(Pango.SCALE * w)
    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()
    cr.set_source_rgb(*color)
    cr.move_to(x, y + (h/2 - th/2))
    PangoCairo.show_layout(cr, layout)

def draw_background(cr):
    cr.set_source_rgb(*bkg_color)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

def draw_bar(cr, query):
    """
                    6px
        ---------------------------
    6px |10px query|              | 6px
        ---------------------------
                    6px
    """

    draw_rect(cr, 6, 6, 468, 58, bar_color)

    query_x = 16
    query_y = 35

    layout = PangoCairo.create_layout(cr)

    size = 28
    set_font(layout, size)

    layout.set_text(u'%s' % query, -1)
    cr.set_source_rgb(*text_color)
    PangoCairo.update_layout(cr, layout)

    query_w, query_h = layout.get_pixel_size()

    while query_w > 448:
        size = size - 1
        set_font(layout, size)
        query_w, query_h = layout.get_pixel_size()

    cr.move_to(query_x, query_y - 0.5*query_h)
    PangoCairo.show_layout(cr, layout)

    draw_rect(cr, query_w+18, 16, 2, 38, text_color)


def draw_item(cr, pos, item, selected):
    """
    ---------------------------------------
    | TEXT                  |             |
    | subtext               |             |
    ---------------------------------------
    """

    # pos -> (x, y)
    item_height = 48
    base_y = 70 + pos * item_height
    #middle_y = base_y + 0.5 * item_height

    if selected:
        draw_rect(cr, 0, base_y, 480, item_height, sel_color)
    else:
        draw_separator(cr, 0, base_y + item_height - 1, 480)

    text_h = item_height * 0.5

    if item.subtitle:

        if selected:
            draw_text(cr, 10, base_y+2, 400, text_h, item.title, seltext_color, 14)
        else:
            draw_text(cr, 10, base_y+2, 400, text_h, item.title, text_color, 14)

        y = base_y + item_height * 0.5
        if selected:
            draw_text(cr, 10, y, 400, text_h, item.subtitle, seltext_color, 8)
        else:
            draw_text(cr, 10, y, 400, text_h, item.subtitle, subtext_color, 8)

    else:
        if selected:
            draw_text(cr, 10, base_y, 400, item_height, item.title, seltext_color, 14)
        else:
            draw_text(cr, 10, base_y, 400, item_height, item.title, text_color, 14)

    # Default action and more actions arrow
    if selected:

        # default_action_name = actions.actions[item.category][0][0]
        # draw_text(cr, 420, base_y, 60, item_height, 'test', seltext_color, 8)

        # arrow
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1.5)
        cr.move_to(470, base_y + item_height/2 + 4)
        cr.rel_line_to(4, -4)
        cr.rel_line_to(-4, -4)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()


def draw_scrollbar(cr):
    pass


def draw_action_panel(cr, actions, selected):

    draw_rect(cr, 336, 70, 144, 240, bkg_color)

    draw_separator(cr, 336, 70, 240, 'v')

    for pos, action in enumerate(actions):

        base_y =  70 + 30 * pos

        draw_separator(cr, 336, base_y+29, 144)

        text_color = config.text_color
        if selected == pos:
            text_color = config.seltext_color
            draw_rect(cr, 336, base_y, 144,
                      30, config.sel_color)

        draw_text(cr, 346, base_y, 140, 30,
                  action[0], text_color, 10)
