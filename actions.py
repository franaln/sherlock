# actions

import subprocess
from gi.repository import Gio, Gdk, Notify


## Fallback searches

def do_search_google():
    pass


## Common actions

def do_run_cmd(match, target=None):
    cmd_list = match['arg'].split()
    subprocess.call(cmd_list)

def do_run(match):
    # title='Run'
    # subtitle='Run an application, action or script'

    display = Gdk.Display.get_default()

    app = Gio.DesktopAppInfo().new_from_filename(match.arg)
    app.launch(None, display.get_app_launch_context())

def do_run_in_terminal(match):
    # title='Run in Terminal'
    # subtitle='Run application or command in terminal'
    original = Gio.DesktopAppInfo().new_from_filename(match.arg)
    app = Gio.AppInfo.create_from_commandline(original.get_commandline(),
                                              original.get_name(),
                                              AppInfoCreateFlags.NEEDS_TERMINAL)
    display = Gdk.Display.get_default()
    app.launch(None, display.get_app_launch_context())

def  do_open(match):
    # title: 'Open'
    # subtitle: 'Open using default application'

    f = Gio.File.new_for_uri(match.arg)

    app_info = f.query_default_handler(None)
    files = []
    files.append(f)

    display = Gdk.Display.get_default ();
    app_info.launch(files, display.get_app_launch_context())

def do_open_in_folder(match):
    # title: 'Open folder'
    # subtitle: 'Open folder containing this file'

    f = Gio.File.new_for_uri(match.arg)
    f = f.get_parent()

    app_info = f.query_default_handler(None)

    files = []
    files.append(f)

    display = Gdk.Display.get_default()
    app_info.launch(files, display.get_app_launch_context())


## Outputs

def do_copy_to_clipboard(match):
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








actions = {

    'Run': do_run,
    'Run command': do_run_cmd,
    'Run in terminal': do_run_in_terminal,
    'Open': do_open,
    'Open in folder': do_open_in_folder,

    'Copy to clipboard': do_copy_to_clipboard,

}
