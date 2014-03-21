# common actions

import subprocess
from gi.repository import Gio, Gdk
from objects import Action

def open_uri(uri):
    f = Gio.File.new_for_uri (uri);

    app_info = f.query_default_handler(None)
    files = []
    files.append(f)

    display = Gdk.Display.get_default ();
    app_info.launch(files, display.get_app_launch_context())


class RunCmd(Action):
    def __init__(self):
        Action.__init__(self, 'Run command')

    def execute(self, match, target=None):
        cmd_list = match.arg.split()
        subprocess.call(cmd_list)


class Open(Action):
    def __init__(self):
        Action.__init__(self, 'Open', 'Open using default application')

    def execute(match, target=None):
        pass

        #     uri_match = UriMatch(match)

    #     if uri_match is not None:
    #         CommonActions.open_uri (uri_match.uri);

    #     else if (file_path.match (match.title))
    #     {
    #       File f;
    #       if (match.title.has_prefix ("~"))
    #       {
    #         f = File.new_for_path (Path.build_filename (Environment.get_home_dir (),
    #                                                     match.title.substring (1),
    #                                                     null));
    #       }
    #       else
    #       {
    #         f = File.new_for_path (match.title);
    #       }
    #       CommonActions.open_uri (f.get_uri ());
    #     }
    #     else
    #     {
    #       CommonActions.open_uri (match.title);
    #     }
    #   }

    #   public override bool valid_for_match (Match match)
    #   {
    #     switch (match.match_type)
    #     {
    #       case MatchType.GENERIC_URI:
    #         return true;
    #       case MatchType.UNKNOWN:
    #         return web_uri.match (match.title) || file_path.match (match.title);
    #       default:
    #         return false;
    #     }
    #   }

    #   private Regex web_uri;
    #   private Regex file_path;

    #   construct
    #   {
    #     try
    #     {
    #       web_uri = new Regex ("^(ftp|http(s)?)://[^.]+\\.[^.]+", RegexCompileFlags.OPTIMIZE);
    #       file_path = new Regex ("^(/|~/)[^/]+", RegexCompileFlags.OPTIMIZE);
    #     }
    #     catch (Error err)
    #     {
    #       Utils.Logger.warning (this, "%s", err.message);
    #     }
    #   }
    # }

class OpenFolder(Action):
    def __init__(self):
        Action.__init__(self, 'Open folder', 'Open folder containing this file')

    def execute(match, target=None):
        pass
        # UriMatch uri_match = match as UriMatch;
        #   return_if_fail (uri_match != null);

        f = Gio.File.new_for_uri (uri_match.uri);
        f = f.get_parent ()

        app_info = f.query_default_handler(None)
        files = []
        files.append(f)

        display = Gdk.Display.get_default()
        app_info.launch(files, display.get_app_launch_context())

        #   public override bool valid_for_match (Match match)
        #   {
        #     if (match.match_type != MatchType.GENERIC_URI) return false;
        #     UriMatch uri_match = match as UriMatch;
        #     var f = File.new_for_uri (uri_match.uri);
        #     var parent = f.get_parent ();
        #     return parent != null && f.is_native ();
        #   }
        # }

class Run(Action):
      def __init__(self):
          Action.__init__(self,
                          title='Run',
                          subtitle='Run an application, action or script')

      def execute (self, match, target=None):
          display = Gdk.Display.get_default()

          app = Gio.DesktopAppInfo().new_from_filename(match.arg)
          app.launch(None, display.get_app_launch_context())

class RunTerminal(Action):
    def __init__(self):
        Action.__init__(self,
                        title='Run in Terminal',
                        subtitle='Run application or command in terminal')

    def execute(self, match, target=None):
        original = app_match.app_info

        app = Gio.AppInfo.create_from_commandline(original.get_commandline(),
                                                  original.get_name(),
                                                  AppInfoCreateFlags.NEEDS_TERMINAL)
        display = Gdk.Display.get_default()
        app.launch(None, display.get_app_launch_context())


# Copy to clipboard
class CopyClipboard(Action):
    def __init__(self):
        Action.__init__(
            title="Copy to Clipboard",
            description="Copy selection to clipboard"
        )

    def execute(self, match, target=None):

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


#     private Gee.List<BaseAction> actions;

#     construct
#     {
#       actions = new Gee.ArrayList<BaseAction> ();

#       actions.add (new Runner ());
#       actions.add (new TerminalRunner ());
#       actions.add (new Opener ());
#       actions.add (new OpenFolder ());
#       actions.add (new ClipboardCopy ());
#     }


# Send notification
class SendNotification(Action):
    def __init__(self):
        Action.__init__(
            title='SendNotification',
            subtitle='Send notification'
        )

# Large type
class LargeType(Action):
    def __init__(self):
        Action.__init__(
            title='LargeType',
            subtitle='...'
        )
