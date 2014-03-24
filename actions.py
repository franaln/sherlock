"""
actions
-------

An action must be a function with match['arg'] as argument

"""

import subprocess
from gi.repository import Gio, Gdk, Notify


## Fallback searches
def do_search_google():
    pass


## Common actions
def action_run_cmd(arg):
    cmd_list = arg.split()
    subprocess.call(cmd_list)

def action_run(arg):
    display = Gdk.Display.get_default()

    app = Gio.DesktopAppInfo().new_from_filename(arg)
    app.launch(None, display.get_app_launch_context())

def action_run_in_terminal(arg):
    original = Gio.DesktopAppInfo().new_from_filename(arg)
    app = Gio.AppInfo.create_from_commandline(original.get_commandline(),
                                              original.get_name(),
                                              AppInfoCreateFlags.NEEDS_TERMINAL)
    display = Gdk.Display.get_default()
    app.launch(None, display.get_app_launch_context())

def action_open(arg):
    f = Gio.File.new_for_uri(arg)

    app_info = f.query_default_handler(None)
    files = []
    files.append(f)

    display = Gdk.Display.get_default ();
    app_info.launch(files, display.get_app_launch_context())

def action_open_folder(arg):
    f = Gio.File.new_for_uri(arg)
    f = f.get_parent()

    app_info = f.query_default_handler(None)

    files = []
    files.append(f)

    display = Gdk.Display.get_default()
    app_info.launch(files, display.get_app_launch_context())


## Outputs
def output_copy_to_clipboard(arg):
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

# Send notification
def send_notification(match):
    #Notify.init ("Hello world")
    noti = Notify.Notification.new('Sherlock', match.arg,'dialog-information')
    noti.show()


# Large type
def show_large_type(match):
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
    ('Run', action_run),
    ('Run in terminal', action_run_in_terminal),
]

actions['uri'] = [
    ('Open', action_open),
    ('Open folder', action_open_folder),
]

actions['cmd'] = [
    ('Run', action_run_cmd),
]

actions['text'] = [
    ('Copy', output_copy_to_clipboard),
]
