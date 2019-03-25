import cairo
from gi.repository import Pango, PangoCairo

def draw_background(cr, color):
    cr.set_source_rgb(*color)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

def draw_rect(cr, x, y, width, height, color):
    cr.set_source_rgb(*color)
    cr.rectangle(x, y, width, height)
    cr.fill()

def draw_horizontal_separator(cr, x, y, size, color):
    cr.set_source_rgb(*color)
    cr.set_line_width(1.)
    cr.move_to(x, y)
    cr.line_to(x+size, y)
    cr.stroke()

def draw_vertical_separator(cr, x, y, size, color):
    cr.set_source_rgb(*color)
    cr.set_line_width(0.8)
    cr.move_to(x, y)
    cr.line_to(x, y+size)
    cr.stroke()

def calc_text_width(cr, text, size, fontname):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    PangoCairo.update_layout(cr, layout)
    tw, th = layout.get_pixel_size()
    return tw

def draw_text(cr, x, y, w, h, text, color, fontname, size=12, justification='left'):
    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    layout.set_text(u'%s' % text, -1)
    layout.set_ellipsize(Pango.EllipsizeMode.END)
    layout.set_width(Pango.SCALE * w)
    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()
    cr.set_source_rgb(*color)
    if justification == 'center':
        cr.move_to(x + (w*0.5 - tw*0.5), y + (h*0.5 - th*0.5))
    elif justification == 'left':
        cr.move_to(x, y + (h*0.5 - th*0.5))
    elif justification == 'right':
        cr.move_to(x+w-tw, y + (h*0.5 - th*0.5))

    PangoCairo.show_layout(cr, layout)

def draw_bar(cr, x, y, bar_w, bar_h, text, color, fontname, size=12):

    ## query
    query_w = bar_w - 50

    layout = PangoCairo.create_layout(cr)
    font = Pango.FontDescription('%s %s' % (fontname, size))
    layout.set_font_description(font)
    cr.set_source_rgb(*color)
    layout.set_text(u'%s' % text, -1)
    PangoCairo.update_layout(cr, layout)

    tw, th = layout.get_pixel_size()
    while tw > query_w:
        size = size - 1
        font = Pango.FontDescription('%s %s' % (fontname, size))
        layout.set_font_description(font)
        PangoCairo.update_layout(cr, layout)
        tw, th = layout.get_pixel_size()

    cr.move_to(x, y - 0.5 * th)
    PangoCairo.show_layout(cr, layout)

    ## cursor
    tw, th = layout.get_pixel_size()
    cursor_x = x + tw
    cr.set_source_rgb(*color)
    cr.rectangle(cursor_x, 0.25*bar_h, 1.5, 0.50*bar_h)
    cr.fill()


def draw_small_arrow(cr, x, y):
    cr.set_source_rgb(1, 1, 1)
    cr.set_line_width(1.5)
    cr.move_to(x, y)
    cr.rel_line_to(4, -4)
    cr.rel_line_to(-4, -4)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
