# drawer

import cairo
from gi.repository import Pango, PangoCairo

import config
import items

fontname      = config.fontname
bkg_color     = config.background_color
bar_color     = config.bar_color
sep_color     = config.separator_color
sel_color     = config.selection_color
text_color    = config.text_color
subtext_color = config.subtext_color
seltext_color = config.seltext_color


width = 600
height = 100

item_h = 60
item_m = item_h * 0.5

bar_o = 6
bar_w = width - 2 * bar_o
bar_h = height - 2 * bar_o

menu_w = width
menu_h = item_h * 5

right_x = 0.7 * width
right_w = width - right_x

left_w = right_x



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

def draw_bar(cr, query, selected=False):
    """
                    6px
        ---------------------------
    6px |10px query|              | 6px
        ---------------------------
                    6px
    """

    draw_rect(cr, bar_o, bar_o, bar_w, bar_h, bar_color)

    query_x = 10 + bar_o
    query_y = bar_h * 0.5

    layout = PangoCairo.create_layout(cr)

    size = 38
    set_font(layout, size)

    layout.set_text(u'%s' % query, -1)

    PangoCairo.update_layout(cr, layout)

    query_w, query_h = layout.get_pixel_size()

    while query_w > bar_w - 20:
        size = size - 1
        set_font(layout, size)
        query_w, query_h = layout.get_pixel_size()

    if query and selected:
        draw_rect(cr, query_x, query_y-query_h*0.5, query_w+5, query_h, sel_color)

    cr.move_to(query_x, query_y - 0.5*query_h)
    cr.set_source_rgb(*text_color)
    PangoCairo.show_layout(cr, layout)

    #draw_rect(cr, query_w+18, 10+bar_o, 2, bar_h-4, text_color)


def draw_item(cr, pos, item, selected=False):
    """
    ---------------------------------
    | TEXT                  |       |
    | subtext               |       |
    ---------------------------------
    """

    # pos -> (x, y)
    base_y = height + pos * item_h

    if selected:
        draw_rect(cr, 0, base_y, width, item_h, sel_color)
    elif pos < 4:
        draw_separator(cr, 0, base_y + item_h - 1, width)

    text_h = item_m
    title = item.title

    if item.subtitle:
        if selected:
            draw_text(cr, 10, base_y+2, left_w, text_h, title, seltext_color, 18)
        else:
            draw_text(cr, 10, base_y+2, left_w, text_h, title, text_color, 18)

        y = base_y + item_h * 0.5
        if selected:
            draw_text(cr, 10, y, left_w, text_h, item.subtitle, seltext_color, 8)
        else:
            draw_text(cr, 10, y, left_w, text_h, item.subtitle, subtext_color, 8)
        #draw_text(cr, 10, base_y, 20, item_h, '-', text_color, 20)
        #draw_rect(cr, 0.15*left_w, y, 0.7*left_w, 5, subtext_color)
        #draw_rect(cr, 0.15*left_w, y, 0.3*left_w, 5, sel_color)
        #draw_text(cr, width-40, base_y, 20, item_h, '+', text_color, 20)

    else:
        if selected:
            draw_text(cr, 10, base_y, left_w, item_h, title, seltext_color, 18)
        else:
            draw_text(cr, 10, base_y, left_w, item_h, title, text_color, 18)


    # cr.set_source_rgb(0, 0, 0)
    # cr.set_line_width(1.5)
    # cr.move_to(15, base_y + item_m)
    # cr.rel_line_to(10, 0)
    # cr.move_to(7.6, base_y + item_m - 5)
    # cr.rel_line_to(-4, -4)
    # cr.set_line_join(cairo.LINE_JOIN_ROUND)
    # cr.stroke()



    # Default action and more actions arrow
    if selected:
        action_name = items.actions[item.category][0][0]
        draw_text(cr, left_w + right_w*0.5, base_y, right_w, item_h, action_name, seltext_color, 10)

        # arrow
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1.5)
        cr.move_to(width-20, base_y + item_m + 4)
        cr.rel_line_to(4, -4)
        cr.rel_line_to(-4, -4)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()

def draw_action_panel(cr, actions, selected):

    draw_rect(cr, right_x, height, right_w, menu_h, bkg_color)

    draw_separator(cr, right_x, height, menu_h, 'v')

    for pos, action in enumerate(actions):

        base_y =  height + 30 * pos

        draw_separator(cr, right_x, base_y+29, right_w)

        if selected == pos:
            draw_rect(cr, right_x, base_y, right_w,
                      30, sel_color)

            draw_text(cr, right_x+10, base_y, right_w, 30,
                      action[0], seltext_color, 10)
        else:
            draw_text(cr, right_x+10, base_y, right_w, 30,
                      action[0], text_color, 10)
