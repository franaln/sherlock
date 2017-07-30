# utils

import os
import re
import string
import time
import subprocess
import shutil
import shlex
import xdg.DesktopEntry

from gi.repository import Gtk, Gdk, Gio, GLib

def escape(text):
    cs = ['(', ')', '[', ']', '\'']

    newtext = text
    for c in cs:
        if c in newtext:
            newtext = newtext.replace(c, '\\%s' % c)

    return newtext

def get_selection():
    pass
    # clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    #     return clipboard.get_text()


def run_cmd(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()

    return subprocess.call(cmd)


def get_cmd_output(cmd_list):
    try:
        output = subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf8').strip()


def is_running(name):
    processes = str(subprocess.check_output(('ps', '-u', os.environ['USER'], '-o', 'comm',
                                             '--no-headers')), encoding='utf8').rstrip('\n').split('\n')
    return (name in processes)


def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)


def launch_app(desktop_file, paths=[], in_terminal=None, timestamp=None, screen=None):

    paths = [  os.path.expanduser(path) for path in paths ]

    app_info = Gio.DesktopAppInfo.new_from_filename(desktop_file)

    try:
        de = xdg.DesktopEntry.DesktopEntry(desktop_file)
    except:
        raise

    if not de.getExec():
        raise

    desktop_info = {
        "Terminal": de.getTerminal(),
        "StartupNotify": de.getStartupNotify(),
        "Exec": de.getExec(),
        "Path": de.getPath(),
        "Icon": de.getIcon(),
        "Name": de.getName(),
    }


    lex = shlex.shlex(desktop_info['Exec'])
    lex.whitespace_split = True

    try:
        lex_output = list(lex)
    except ValueError:
        lex_output = [s,]

    argv =  lex_output #custom_shlex_split(desktop_info["Exec"])

    new_argv = []
    multiple_needed = False
    for key in argv:
        if key in ['%d', '%D', '%n', '%N', '%v', '%m']:
            continue
        elif key == "%%":
            new_argv.append("%")
        elif key == "%f" or key == "%u":
            multiple_needed = True
            new_argv.append('PATH')
        elif key == "%F" or key == "%U":
            multiple_needed = False
            new_argv.append('PATH')
        else:
            new_argv.append(key)

    launch_cmds = []
    if not multiple_needed:
        cmd = []
        for arg in new_argv:
            if arg == 'PATH':
                for path in paths:
                    cmd.append(path)
            else:
                cmd.append(arg)
        launch_cmds.append(cmd)

    else:
        for path in paths:
            cmd = []
            for arg in new_argv:
                if arg == 'PATH':
                    cmd.append(path)
                else:
                    cmd.append(arg)
            launch_cmds.append(cmd)

    workdir = desktop_info["Path"] or None

    # if in_terminal is None:
    #     in_terminal = desktop_info["Terminal"]
    # if in_terminal:
    #     term = '/usr/share/applications/urxvtc.desktop' #terminal.get_configured_terminal()

    for cmd in launch_cmds:

        if not workdir or not os.path.exists(workdir):
            workdir = "."

        try:
            (pid, _ig1, _ig2, _ig3) = GLib.spawn_async(
                cmd,
                flags=GLib.SpawnFlags.SEARCH_PATH,
                working_directory=workdir)
        except GLib.GError as exc:
            raise SpawnError(exc.message)

        if not pid:
            return False

    return True
