"""
actions
-------

An action must be a function with match['arg'] as argument

## Fallback searches

## Common actions
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
from gi.repository import Gio, Gdk, Notify


# Fallback searches
def do_search_google():
    pass


# Common actions
def run_cmd(arg):
    if isinstance(arg, str):
        cmd_list = arg.split()
    subprocess.call(cmd_list)

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
    # title: "Copy to Clipboard",
    # description: "Copy selection to clipboard"

    cb = Gtk.Clipboard.get(Gdk.Atom.NONE)
        #     if (match.match_type == MatchType.GENERIC_URI)
        #     {
        #       UriMatch uri_match = match as UriMatch;
        #       return_if_fail (uri_match != null);

        #       /*
        #        // just wow, Gtk and also Vala are trying really hard to make this hard to do...
        #       Gtk.TargetEntry[] no_entries = {};
        #       Gtk.TargetList l = new Gtk.TargetList (no_entries);
        #       l.add_uri_targets (0);
        #       l.add_text_targets (0);
        #       Gtk.TargetEntry te = Gtk.target_table_new_from_list (l, 2);
        #       cb.set_with_data ();
        #       */
        #       cb.set_text (uri_match.uri, -1);
        #     }
        #     else if (match.match_type == MatchType.TEXT)
        #     {
        #       TextMatch? text_match = match as TextMatch;
        #       string content = text_match != null ? text_match.get_text () : match.title;

        #       cb.set_text (content, -1);
        #     }
        #   }

def send_notification(match):
    #Notify.init ("Hello world")
    noti = Notify.Notification.new('Sherlock', match.arg,'dialog-information')
    noti.show()

def show_large_type(match):
    # def draw():
    #     cr = Gdk.cairo_create(widget.get_window())

    #     cr.set_source_rgb(0.1, 0.1, 0.1)
    #     cr.set_operator(cairo.OPERATOR_SOURCE)
    #     cr.paint()




    # window = Gtk.Window()
    # window.set_app_paintable(True)
    # window.set_decorated(False)
    # window.set_position(Gtk.WindowPosition.CENTER)
    # window.set_keep_above(True)

    pass

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


actions = {}

actions['app'] = [
    ('Run', run_app),
    ('Run in terminal', run_app_in_terminal),
]

actions['uri'] = [
    ('Open', open_uri),
    ('Open folder', open_folder),
]

actions['cmd'] = [
    ('Run', run_cmd),
]

actions['text'] = [
    ('Copy', copy_to_clipboard),
    ('Copy', copy_to_clipboard),
]
