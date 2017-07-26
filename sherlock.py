#! /usr/bin/python
# Sherlock

import os
import sys
import argparse

import dbus
import dbus.bus
import dbus.mainloop.glib

# Don't import ./sherlock.py when running an installed binary at /usr/.../sherlock.py
if __file__[:4] == '/usr' :
    sys.path.remove(os.path.dirname(__file__))

from sherlock.main import Sherlock

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quit', action='store_true', help='Quit')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug output')

    args = parser.parse_args()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    request = bus.request_name("org.sherlock.Daemon", dbus.bus.NAME_FLAG_DO_NOT_QUEUE)

    if request != dbus.bus.REQUEST_NAME_REPLY_EXISTS:
        if args.quit:
            print('not running')
            return True
        app = Sherlock(bus, '/', "org.sherlock.Daemon", args.debug)
    else:
        obj = bus.get_object("org.sherlock.Daemon", "/")
        app = dbus.Interface(obj, "org.sherlock.Daemon")

    if args.quit:
        app.close()
    else:
        app.run()

    return True


if __name__ == '__main__':
    sys.exit(main())
