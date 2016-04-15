# common actions

"""
An action must be a function with match as argument

## Actions
  * Run cmd
  * Run application
  * Run application in terminal
  * Open file/folder
  * Open file in folder
  * Web search

## Outputs
  * Copy to clipboard
  * Send notification
  * Large type
  * QR code
"""

import os
import subprocess
from gi.repository import Gtk, Gio, Gdk, Notify, Pango

from sherlock import utils

def do_search_google():
    pass


def escape(text):

    cs = ['(', ')', '[', ']', '\'']

    newtext = text
    for c in cs:
        if c in newtext:
            newtext = newtext.replace(c, '\\%s' % c)

    return newtext



# Common actions
def run_cmd(arg):

    if '&&' in arg:
        cmds = arg.split('&&')
    elif ';' in arg:
        cmds = arg.split(';')
    else:
        cmds = [arg,]

    st = 0
    for cmd in cmds:
        if st == 0:
            st = utils.run_cmd(cmd)
        else:
            break


def run_app(arg):
    # display = Gdk.Display.get_default()
    # app = Gio.DesktopAppInfo().new_from_filename(arg)
    # app.launch(None, display.get_app_launch_context())
    utils.run_cmd('setsid setsid ' + arg)


def run_app_in_terminal(arg):
    original = Gio.DesktopAppInfo().new_from_filename(arg)
    app = Gio.AppInfo.create_from_commandline(original.get_commandline(),
                                              original.get_name(),
                                              Gio.AppInfoCreateFlags.NEEDS_TERMINAL)
    display = Gdk.Display.get_default()
    app.launch(None, display.get_app_launch_context())


def open_uri(arg):
    uri = r'file://' + escape(arg).replace(' ', r'%20')
    run_cmd('open '+uri)


def open_folder(arg):
    run_cmd('setsid nautilus '+arg.split('/')[0])

def open_console_uri(arg):
    run_cmd('setsid urxvt -e "cd %s"' % os.path.dirname(arg))

def copy_cmd_to_console(arg):
    run_cmd('setsid urxvt -e "cd %s"' % os.path.dirname(arg))


# Outputs
def copy_to_clipboard(arg):
    # "primary":
    xsel_proc = subprocess.Popen(['xsel', '-pi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(arg.encode('utf-8'))

    # "clipboard":
    xsel_proc = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
    xsel_proc.communicate(arg.encode('utf-8'))


def send_notification(match):
    #Notify.init ("Hello world")
    noti = Notify.Notification.new('Sherlock', match.arg, 'dialog-information')
    noti.show()

def show_large_type(arg):

    """
    Show @text in a result window.

    Use @title to set a window title
    """
    # class ResultWindowBehavior (object):
    #     def on_text_result_window_key_press_event(self,widget,event, names):
    #         return _window_destroy_on_escape(widget, event)

    #     def on_close_button_clicked(self, widget, names):
    #         names.text_result_window.window.destroy()
    #         return True

    #     def on_copy_button_clicked(self, widget, names):
    #         clip = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    #         textview = names.result_textview
    #         buf = textview.get_buffer()
    #         buf.select_range(*buf.get_bounds())
    #         buf.copy_clipboard(clip)

    # window,textview = builder_get_objects_from_file("result.ui",
    #                                                 ("text_result_window", "result_textview"),
    #                                                 autoconnect_to=ResultWindowBehavior())

    # # Set up text buffer
    #buf = Gtk.TextBuffer()
    # buf.set_text(text)
    # monospace = gtk.TextTag("fixed")
    # monospace.set_property("family", "Monospace")
    # monospace.set_property("scale", pango.SCALE_LARGE)
    # beg, end = buf.get_bounds()
    # tag_table = buf.get_tag_table()
    # tag_table.add(monospace)
    # buf.apply_tag(monospace, beg, end)

    # textview.set_buffer(buf)
    # textview.set_wrap_mode(gtk.WRAP_NONE)

    # if title:
    #     window.set_title(title)

    # if ctx:
    #     ctx.environment.present_window(window)

    # window.show_all()

    # # Fix Sizing:
    # # We want to size the window so that the
    # # TextView is displayed without scrollbars
    # # initially, if it fits on screen.
    # oldwid,oldhei = textview.window.get_size()
    # winwid,winhei = window.get_size()

    # max_hsize, max_vsize = window.get_default_size()
    # wid, hei = textview.size_request()
    # textview.set_wrap_mode(gtk.WRAP_WORD)

    # vsize =int(min(hei + (winhei - oldhei) + 5, max_vsize))
    # hsize =int(min(wid + (winwid - oldwid) + 5, max_hsize))

    # window.resize(hsize, vsize)
    # if ctx:
    #     ctx.environment.present_window(window)
    # else:
    #     window.present_with_time(uievents.current_event_time())



    # def draw():
    #     cr = Gdk.cairo_create(widget.get_window())

    #     cr.set_source_rgb(0.1, 0.1, 0.1)
    #     cr.set_operator(cairo.OPERATOR_SOURCE)
    #     cr.paint()

    window = Gtk.Window()

    text = arg.strip()
    #     window = gtk.Window()
    label = Gtk.Label()
    label.set_text(text)

    # def set_font_size(label, fontsize=48.0):
    #     siz_attr = Pango.AttrFontDesc(
    #         Pango.FontDescription) #(str(fontsize))) #, 0, -1)
    #     attrs = Pango.AttrList()
    #     attrs.insert(siz_attr)
    #     label.set_attributes(attrs)
    #     label.show()

    size = 72.0
    #set_font_size(label, size)

    #if ctx:
    #                 screen = ctx.environment.get_screen()
    #                 window.set_screen(screen)
    #         else:
    screen = Gdk.screen_get_default()

    maxwid = screen.get_width() - 50
    maxhei = screen.get_height() - 100
    wid, hei = label.size_request()

    # If the text contains long lines, we try to
    # hard-wrap the text
    if ((wid > maxwid or hei > maxhei) and
        any(len(L) > 100 for L in text.splitlines())):
        label.set_text(text)

    wid, hei = label.size_request()

    if wid > maxwid or hei > maxhei:
        # Round size down to fit inside
        wscale = maxwid * 1.0/wid
        hscale = maxhei * 1.0/hei
        #set_font_size(label, math.floor(min(wscale, hscale)*size) or 1.0)

    window.add(label)

    #window.set_app_paintable(True)
    window.set_decorated(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_keep_above(True)
    window.set_resizable(False)
    #window.set_property("border-width", 10)
    #window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
    #         label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))

    def _window_destroy(widget, event):
        widget.destroy()
        return True
    window.connect('key-press-event', _window_destroy)
    #window.show_all()
    #         if ctx:
    #             ctx.environment.present_window(window)
    #         else:
    window.show_all() #present_with_time(uievents.current_event_time())



def show_qrcode(match):
    pass
    #image_file = StringIO.StringIO()
    # text = leaf.get_text_representation()
    # version, size, image = qrencode.encode_scaled(text, size=300)
    # image.save(image_file, "ppm")
    # image_contents = image_file.getvalue()
    # image_file.close()

    # loader = gtk.gdk.PixbufLoader("pnm")
    # loader.write(image_contents, len(image_contents))
    # pixbuf = loader.get_pixbuf()
    # loader.close()
    # window = gtk.Window()
    # window.set_default_size(350, 350)
    # image = gtk.Image()
    # image.set_from_pixbuf(pixbuf)
    # image.show()
    # window.add(image)
    # ctx.environment.present_window(window)
