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

import subprocess
from gi.repository import Gtk, Gio, Gdk, Notify, Pango

import utils

def do_search_google():
    pass


# Common actions
def run_cmd(arg):
    utils.run_cmd(arg)

def run_app(arg):
    display = Gdk.Display.get_default()
    app = Gio.DesktopAppInfo().new_from_filename(arg)
    app.launch(None, display.get_app_launch_context())

def run_app_in_terminal(arg):
    original = Gio.DesktopAppInfo().new_from_filename(arg)
    app = Gio.AppInfo.create_from_commandline(original.get_commandline(),
                                              original.get_name(),
                                              Gio.AppInfoCreateFlags.NEEDS_TERMINAL)
    display = Gdk.Display.get_default()
    app.launch(None, display.get_app_launch_context())

    # run_cmd(['/bin/bash', arg

def open_uri(arg):
    f = Gio.File.new_for_uri(arg)

    app_info = f.query_default_handler(None)
    files = []
    files.append(f)

    display = Gdk.Display.get_default ();
    app_info.launch(files, display.get_app_launch_context())

def open_folder(arg):
    f = Gio.File.new_for_uri(arg)
    f = f.get_parent()

    app_info = f.query_default_handler(None)

    files = []
    files.append(f)

    display = Gdk.Display.get_default()
    app_info.launch(files, display.get_app_launch_context())


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

    print(text)

    # def set_font_size(label, fontsize=48.0):
    #     siz_attr = Pango.AttrFontDesc(
    #         Pango.FontDescription(str(fontsize)), 0, -1)
    #     attrs = Pango.AttrList()
    #     attrs.insert(siz_attr)
    #     label.set_attributes(attrs)
    #     label.show()

    #size = 72.0
    #set_font_size(label, size)

    #if ctx:
    #                 screen = ctx.environment.get_screen()
    #                 window.set_screen(screen)
    #         else:
    #screen = Gdk.screen_get_default()

    #maxwid = screen.get_width() - 50
    #maxhei = screen.get_height() - 100
    #wid, hei = label.size_request()

    # If the text contains long lines, we try to
    # hard-wrap the text
    # if ((wid > maxwid or hei > maxhei) and
    #     any(len(L) > 100 for L in text.splitlines())):
    #     label.set_text(_wrap_paragraphs(text))

    # wid, hei = label.size_request()

    # if wid > maxwid or hei > maxhei:
    #     # Round size down to fit inside
    #     wscale = maxwid * 1.0/wid
    #     hscale = maxhei * 1.0/hei
    #     set_font_size(label, math.floor(min(wscale, hscale)*size) or 1.0)

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


actions = {

    'app': [
        ('Run', run_app),
        ('Run in terminal', run_app_in_terminal),
    ],

    'uri': [
        ('Open', open_uri),
        ('Open folder', open_folder),
    ],

    'cmd': [
        ('Run', run_cmd),
    ],

    'text': [
        ('Copy', copy_to_clipboard),
        ('Large type', show_large_type),
        ('Show QR code', show_qrcode),
    ],

}
