# drawer

import cairo
from gi.repository import Pango, PangoCairo

import config

bar_width = config.width
bar_height = config.height
item_height = config.item_height
lines = config.lines
fontname = config.fontname

bkg_color = config.bkg_color
bar_color = config.bar_color
sep_color = config.sep_color
sel_color = config.sel_color

text_color    = config.text_color
subtext_color = config.subtext_color
seltext_color = config.seltext_color

bar_height_middle = bar_height*0.5

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

def draw_text(cr, x, y, text, color, size=12):
    layout = PangoCairo.create_layout(cr)

    set_font(layout, size)

    layout.set_text(u'%s' % text, -1)
    cr.set_source_rgb(*color)
    PangoCairo.update_layout(cr, layout)

    w, h = layout.get_pixel_size()

    cr.move_to(x, y - h/2)
    PangoCairo.show_layout(cr, layout)

def draw_query(cr, text):

    x = 16
    y =  bar_height*0.5

    color = config.text_color
    size = 28

    layout = PangoCairo.create_layout(cr)

    set_font(layout, size)

    layout.set_text(u'%s' % text, -1)
    cr.set_source_rgb(*color)
    PangoCairo.update_layout(cr, layout)

    w, h = layout.get_pixel_size()

    while w > 440:
        size = size - 1
        set_font(layout, size)
        w, h = layout.get_pixel_size()

    cr.move_to(x, y - h/2)
    PangoCairo.show_layout(cr, layout)

    draw_rect(cr, w+18, 11, 2, 38, text_color)

    return w, h

def draw_window(cr):
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

    draw_rect(cr, 6, 6, bar_width-12,
              bar_height-12, bar_color)

    draw_query(cr, query)



def draw_item(cr, pos, item, selected):
    """
    ---------------------------------------
    | TEXT                  | default |   |
    | subtext               | action  |   |
    ---------------------------------------
    """

    # pos -> (x, y)
    base_y = bar_height + pos * item_height
    middle_y = base_y + 0.5 * item_height

    draw_separator(cr, 0, base_y+item_height-1, bar_width)

    if selected:
        draw_rect(cr, 0, base_y, bar_width,
                  item_height, sel_color)

    textx = 10

    if item.subtitle:
        y = base_y + item_height * 0.375
        if selected:
            draw_text(cr, textx, y, item.title, seltext_color)
        else:
            draw_text(cr, textx, y, item.title, text_color)

        y = base_y + 0.75 * item_height
        if selected:
            draw_text(cr, textx, y, item.subtitle, seltext_color, 8)
        else:
            draw_text(cr, textx, y, item.subtitle, subtext_color, 8)

    else:
        if selected:
            draw_text(cr, textx, middle_y, item.title, seltext_color)
        else:
            draw_text(cr, textx, middle_y, item.title, text_color)

    # Default action and more actions arrow
    # if selected:

    #     default_action_name = actions.actions[item.category][0][0]
    #     draw_text(cr, width-60, middle_y, default_action_name, (1, 1, 1), 10)

    # arrow
    # cr.set_source_rgb(1, 1, 1)
    # cr.set_line_width(1.5)
    # cr.move_to(config.width-10, base_y + 0.5 * config.item_height + 4)
    # cr.rel_line_to(4, -4)
    # cr.rel_line_to(-4, -4)
    # cr.set_line_join(cairo.LINE_JOIN_ROUND)
    # cr.stroke()

    # Colour
    # if item.category == 'text':
    #     color = config.txt_color
    # elif item.category == 'app':
    #     color = config.app_color
    # elif item.category == 'uri':
    #     color = config.uri_color
    # elif item.category == 'cmd':
    #     color = config.cmd_color
    # print (item.category)
    # draw_rect(cr, 0, base_y, 2,
    #               config.item_height, color)



def draw_action_panel(cr, actions, selected):
    base_x = 0.7 * bar_width
    width = bar_width - base_x
    height = item_height * 0.6

    h = 5 * item_height

    draw_rect(cr, base_x, bar_height, bar_width,
              h, bkg_color)

    draw_separator(cr, base_x, bar_height, h, 'v')

    for pos, action in enumerate(actions):

        base_y =  bar_height + pos * height

        draw_separator(cr, base_x, base_y+height-1, width)

        text_color = text_color

        if selected == pos:
            draw_rect(cr, base_x, base_y, width,
                      height, sel_color)

            text_color = seltext_color

        draw_text(cr, base_x+10, base_y + 0.5*height,
                  action[0], text_color, 10)
