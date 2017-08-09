import os
import subprocess
from gi.repository import Gtk, Gio, Gdk, Notify, Pango

from sherlock import utils

# Command
def run_cmd(arg):

    if ' && ' in arg:
        cmds = arg.split('&&')
    elif ' ; ' in arg:
        cmds = arg.split(';')
    else:
        cmds = [arg,]

    st = 0
    for cmd in cmds:
        if st == 0:
            st = utils.run_cmd(cmd)
        else:
            break

def copy_to_console(arg):
    pass


# Apps
def run_app(arg):
    if arg.endswith('.desktop'):
        utils.launch_app(arg)
    else:
        utils.run_cmd('setsid setsid %s' % arg)

def run_app_terminal(self):
    print('urxvtc -e "%s"' % arg)
    os.system('setsid urxvt -e "%s" +hold' % arg)


# Files
def open_uri(arg):
    uri = r'file://' + utils.escape(arg).replace(' ', r'%20')
    run_cmd('open '+uri)

def open_dir(arg):
    if os.path.isfile(arg):
        dir_ = '/'.join(arg.split('/')[:-1])
    else:
        dir_ = arg

    run_cmd('setsid setsid nautilus '+dir_)

def open_dir_terminal(arg):
    if os.path.isfile(arg):
        dir_ = '/'.join(arg.split('/')[:-1])
    else:
        dir_ = arg
    cmd = 'urxvt -e sh -c "cd %s ; bash"' % dir_
    os.system(cmd)


# URL: need update to support other browsers
def open_url(arg):
    browser = os.environ['BROWSER']
    if browser == 'chromium':
        utils.launch_app('/usr/share/applications/chromium.desktop', [arg,])

# Output
def copy_to_clipboard(arg):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    clipboard.set_text(arg, -1)

    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(arg, -1)
