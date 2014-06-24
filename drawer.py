# draw menu

import cairo
from gi.repository import Pango, PangoCairo

import config


def draw_rect(cr, x, y, width, height, color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_separator(cr, x, y, size, orientation='h'):
    cr.set_source_rgb(*config.sep_color)
    cr.set_line_width(0.8)

    if orientation == 'h':
        cr.move_to(x+5, y)
        cr.line_to(x+size-5, y)
    elif orientation == 'v':
        cr.move_to(x, y+5)
        cr.line_to(x, y+size-5)
    cr.stroke()

def draw_text(cr, x, y, text, color, size=12):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (config.fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    cr.set_source_rgb(*color)
    PangoCairo.update_layout(cr, layout)

    w, h = layout.get_pixel_size()
    cr.move_to(x, y - h/2)
    PangoCairo.show_layout(cr, layout)
    return w, h

def draw_window(cr):
    cr.set_source_rgb(*config.bkg_color)
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
              config.height-12, config.bar_color)

    (w, h) = draw_text(cr, 16, 30,
                       query, config.text_color, 28)

    # cursor
    draw_rect(cr, w+18, 11, 2, 38, config.text_color)


def draw_item(cr, pos, item, selected):
    """
    ---------------------------------------
    | TEXT                  | default |   |
    | subtext               | action  |   |
    ---------------------------------------
    """

    # pos -> (x, y)
    base_y = config.height + pos * config.item_height
    middle_y = base_y + config.item_height * 0.5

    draw_separator(cr, 0, base_y+config.item_height-1, config.width)

    if selected:
        draw_rect(cr, 0, base_y, config.width,
                  config.item_height, config.sel_color)

    textx = 10

    if item.subtitle:
        y = base_y + config.item_height * 0.375
        if selected:
            draw_text(cr, textx, y, item.title, config.seltext_color)
        else:
            draw_text(cr, textx, y, item.title, config.text_color)

        y = base_y + 0.75 * config.item_height
        if selected:
            draw_text(cr, textx, y, item.subtitle, config.seltext_color, 8)
        else:
            draw_text(cr, textx, y, item.subtitle, config.subtext_color, 8)

    else:
        if selected:
            draw_text(cr, textx, middle_y, item.title, config.seltext_color)
        else:
            draw_text(cr, textx, middle_y, item.title, config.text_color)

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
    base_x = 0.7 * config.width
    width = config.width - base_x
    height = config.item_height * 0.6

    h = 5 * config.item_height

    draw_rect(cr, base_x, config.height, config.width,
              h, config.bkg_color)

    draw_separator(cr, base_x, config.height, h, 'v')

    for pos, action in enumerate(actions):

        base_y =  config.height + pos * height

        draw_separator(cr, base_x, base_y+height-1, width)

        text_color = config.text_color

        if selected == pos:
            draw_rect(cr, base_x, base_y, width,
                      height, config.sel_color)

            text_color = config.seltext_color

        draw_text(cr, base_x+10, base_y + 0.5*height,
                  action[0], text_color, 10)
