# utils

import os
import re
import string
import time
import subprocess
import shutil

from gi.repository import Gtk, Gdk

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
