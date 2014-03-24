#! /usr/bin/env python3

# Sherlock
#
# Usage: sherlock [option] or sherlock
# Dependecies: dmenu patched with the qxyw patch

import os
import sys
import re
import subprocess

from main import Main

# def install_excepthook():
#     """ Make sure we exit when an unhandled exception occurs. """
#     from gi.repository import Gtk
#     old_hook = sys.excepthook
#     def new_hook(etype, evalue, etb):
#         old_hook(etype, evalue, etb)
#         while Gtk.main_level():
#             Gtk.main_quit()
#             sys.exit()
#     sys.excepthook = new_hook

def main():
    #install_excepthook()
    #sys.excepthook = sys.__excepthook__

    app = Main()
    app.run()

    return True

if __name__ == '__main__':
    sys.exit(main())
