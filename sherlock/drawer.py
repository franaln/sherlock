# drawer

import cairo
from gi.repository import Pango, PangoCairo, Gdk

from sherlock import config
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

# Sizes
width  = 800
height = 500 # 90 + 82*5

bar_w = 800
bar_h = 90

menu_w = 800
menu_h = 410

item_h = 82
item_m = 41

right_x = 0.5 * width
right_w = width - right_x
left_w = right_x

query_x = 25
query_y = bar_h * 0.5

# pos_x = (Gdk.Screen.width() - width) * 0.5
# pos_y = (Gdk.Screen.height() - height) * 0.5

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


def draw_item(cr, pos, item, selected=False, debug=False):
    draw_item_text(cr, pos, item, selected, debug)

def draw_item_text(cr, pos, item, selected, debug=False):

    """
    ---------------------------------
    | TEXT                  |       |
    | subtext               |       |
    ---------------------------------
    """

    # pos -> (x, y)
    base_y = bar_h + pos * item_h

    if pos == 0:
        draw_horizontal_separator(cr, -5, base_y, width+10)

    if selected:
        draw_rect(cr, 0, base_y, width, item_h, sel_color)
    elif pos < 4:
        draw_horizontal_separator(cr, 0, base_y + item_h - 1, width)

    text_h = item_m
    title = item.title

    if isinstance(title, list) or isinstance(title, tuple):

        title_list = title

        # divide text width in ncols columns
        ncols = len(title_list)
        col_w = int(left_w / ncols)

        space_w = calc_text_width(cr, ' ', 18)

        title = ''
        for i, l in enumerate(title_list):
            title += l

            space_px = int(col_w - calc_text_width(cr, l, 18))
            nspaces = int(space_px / space_w)

            title += ' '*nspaces

    if item.subtitle:
        if selected:
            draw_text(cr, 20, base_y+6, left_w, text_h, title, seltext_color, 20)
        else:
            draw_text(cr, 20, base_y+6, left_w, text_h, title, text_color, 20)

        y = base_y + item_h * 0.5
        if selected:
            draw_text(cr, 20, y, left_w, text_h, item.subtitle, seltext_color, 10)
        else:
            draw_text(cr, 20, y, left_w, text_h, item.subtitle, subtext_color, 10)

    else:
        if selected:
            draw_text(cr, 20, base_y, left_w, item_h, title, text_color, 20)
        else:
            draw_text(cr, 20, base_y, left_w, item_h, title, text_color, 20)

    # Default action and more actions arrow
    if debug:
        draw_text(cr, left_w + right_w*0.5, base_y, right_w, item_h, item.score, text_color, 10)

    elif selected:
        try:
            action_name = items.actions[item.category][0][0]
            draw_text(cr, left_w + right_w*0.5, base_y, right_w, item_h, action_name, seltext_color, 12)
        except:
            pass

        # arrow
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1.5)
        cr.move_to(width-20, base_y + item_m + 4)
        cr.rel_line_to(4, -4)
        cr.rel_line_to(-4, -4)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()


def draw_right_panel(cr, actions, selected):

    draw_rect(cr, right_x, bar_h, right_w, menu_h, bkg_color)

    draw_vertical_separator(cr, right_x, bar_h, menu_h)

    for pos, action in enumerate(actions):

        base_y =  bar_h + 82 * pos

        draw_horizontal_separator(cr, right_x, base_y+81, right_w)

        if selected == pos:
            draw_rect(cr, right_x, base_y, right_w, 82, sel_color)
            draw_text(cr, right_x+10, base_y, right_w, 82, action[0], seltext_color)
        else:
            draw_text(cr, right_x+10, base_y, right_w, 82, action[0], text_color)
