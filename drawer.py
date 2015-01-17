# drawer

import cairo
from gi.repository import Pango, PangoCairo

import config
import items

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
width = 600
height = 100

item_h = 60
item_m = 0.5*item_h

menu_w = width
menu_h = item_h * 5

right_x = 0.7 * width
right_w = width - right_x
left_w = right_x

toggle_w =0.5*right_w
toggle_h =0.5*item_h
toggle_m =0.5*toggle_w

def draw_background(cr):
    cr.set_source_rgb(*bkg_color)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

def draw_rect(cr, x, y, width, height, color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_horizontal_separator(cr, x, y, size):
    cr.set_source_rgb(*sep_color)
    cr.set_line_width(0.8)
    cr.move_to(x+5, y)
    cr.line_to(x+size-5, y)
    cr.stroke()

def draw_vertical_separator(cr, x, y, size):
    cr.set_source_rgb(*sep_color)
    cr.set_line_width(0.8)
    cr.move_to(x, y+5)
    cr.line_to(x, y+size-5)
    cr.stroke()

def set_font(layout, size):
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)

def draw_text(cr, x, y, w, h, text, color, size=12, center=False):
    layout = PangoCairo.create_layout(cr)
    set_font(layout, size)
    layout.set_text(u'%s' % text, -1)
    layout.set_ellipsize(Pango.EllipsizeMode.END)
    layout.set_width(Pango.SCALE * w)
    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()
    cr.set_source_rgb(*color)
    if center:
        cr.move_to(x + (w/2 - tw/2), y + (h/2 - th/2))
    else:
        cr.move_to(x, y + (h/2 - th/2))
    PangoCairo.show_layout(cr, layout)

def draw_variable_text(cr, x, y, w, h, text, color=text_color, size=12):
    layout = PangoCairo.create_layout(cr)
    set_font(layout, size)

    layout.set_text(u'%s' % text, -1)

    PangoCairo.update_layout(cr, layout)

    text_w, text_h = layout.get_pixel_size()

    print

    while text_w > w:
        size = size - 1
        set_font(layout, size)
        text_w, text_h = layout.get_pixel_size()

    cr.move_to(x, y - 0.5*text_h)
    cr.set_source_rgb(*color)
    PangoCairo.show_layout(cr, layout)


def draw_item(cr, pos, item, selected=False):
    # if pos == 1:
    #     draw_item_slider(cr, pos, item, selected)
    # elif pos == 2:
    #     draw_item_toggle(cr, pos, item, selected)
    # else:
    draw_item_text(cr, pos, item, selected)

def draw_item_text(cr, pos, item, selected):
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
            draw_horizontal_separator(cr, 0, base_y + item_h - 1, width)

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

        else:
            if selected:
                draw_text(cr, 10, base_y, left_w, item_h, title, seltext_color, 18)
            else:
                draw_text(cr, 10, base_y, left_w, item_h, title, text_color, 18)

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

#     def draw_item_slider(cr, pos, item, selected):
#         """
#         ---------------------------------
#         | TEXT         - xxxxxx------ + |
#         ---------------------------------
#         """

#     # pos -> (x, y)
#     base_y = height + pos * item_h

#     if selected:
#         draw_rect(cr, 0, base_y, width, item_h, sel_color)
#     elif pos < 4:
#         draw_separator(cr, 0, base_y + item_h - 1, width)

#     text_h = item_m
#     title = item.title

#     if selected:
#         draw_text(cr, 10, base_y, left_w, item_h, title, seltext_color, 18)
#     else:
#         draw_text(cr, 10, base_y, left_w, item_h, title, text_color, 18)

#     slider_w = right_w * 0.8
#     slider_h = 15

#     slider_x = left_w + right_w * 0.5 - slider_w * 0.5
#     slider_y = base_y + item_h * 0.5 - slider_h * 0.5

#     #draw_text(cr, slider_x-5, base_y, 5, item_h, '-', text_color, 10, True)
#     draw_rect(cr, slider_x, slider_y, slider_w, slider_h, subtext_color)
#     draw_rect(cr, slider_x, slider_y, slider_w*0.9, slider_h, sel_color)
#     #draw_text(cr, width-5, base_y, 5, item_h, '+', text_color, 10, True)


# def draw_item_toggle(cr, pos, item, selected):
#     """
#     ---------------------------------
#     | TEXT                 |NO|YES| |
#     ---------------------------------
#     """

#     # pos -> (x, y)
#     base_y = height + pos * item_h

#     if selected:
#         draw_rect(cr, 0, base_y, width, item_h, sel_color)
#     elif pos < 4:
#         draw_separator(cr, 0, base_y + item_h - 1, width)

#     text_h = item_m
#     title = item.title

#     if selected:
#         draw_text(cr, 10, base_y, left_w, item_h, title, seltext_color, 18)
#     else:
#         draw_text(cr, 10, base_y, left_w, item_h, title, text_color, 18)

#     toggle_x = left_w + right_w * 0.5 - toggle_w * 0.5
#     toggle_y = base_y + item_h * 0.5 - toggle_h * 0.5

#     draw_rect(cr, toggle_x, toggle_y, toggle_w, toggle_h, subtext_color)

#     toggle = True
#     if toggle:
#         draw_rect(cr, toggle_x + toggle_m, toggle_y, toggle_m, toggle_h, sel_color)
#         draw_text(cr, toggle_x+toggle_m, toggle_y, toggle_m, toggle_h, 'YES', text_color, 10, center=True)
#     else:
#         draw_rect(cr, toggle_x, toggle_y, toggle_m, toggle_h, sel_color)
#         draw_text(cr, toggle_x, toggle_y, toggle_m, toggle_h, 'NO', text_color, 10, center=True)

def draw_action_panel(cr, actions, selected):

    draw_rect(cr, right_x, height, right_w, menu_h, bkg_color)

    draw_vertical_separator(cr, right_x, height, menu_h)

    for pos, action in enumerate(actions):

        base_y =  height + 30 * pos

        draw_horizontal_separator(cr, right_x, base_y+29, right_w)

        if selected == pos:
            draw_rect(cr, right_x, base_y, right_w, 30, sel_color)
            draw_text(cr, right_x+10, base_y, right_w, 30, action[0], seltext_color, 10)
        else:
            draw_text(cr, right_x+10, base_y, right_w, 30, action[0], text_color, 10)
