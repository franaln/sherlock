# Basic searches and utilities: apps, files, system cmds, calc

from gi.repository import Gio # FIX: i want to eliminate th gtk dependecies.

import utils
from item import Item


def get_apps():
    apps = []
    for app in Gio.app_info_get_all():
        item = Item(
            app.get_name(),
            app.get_executable(),
            'app',
            app.get_filename(),
        )
        apps.append(item)

    return apps

def get_system_commands():
    lock = Item('Lock', 'Lock the screen', 'cmd', 'slimlock')

    logout = Item('Logout', '', 'cmd', 'killall compiz')

    sleep  = Item('Suspend', 'Suspend to RAM', 'cmd', 'systmectl suspend')
    sleep2 = Item('Sleep', 'Suspend to RAM', 'cmd', 'systmectl suspend')

    halt  = Item('Power off', 'Power off the system', 'cmd', 'systemctl poweroff')
    halt2 = Item('Halt', 'Power off the system', 'cmd', 'systemctl poweroff')

    reboot  = Item('Reboot', 'Reboot the system', 'cmd', 'systemctl reboot')
    reboot2 = Item('Restart', 'Reboot the system', 'cmd', 'systemctl reboot')

    hibernate = Item('Hibernate', 'Suspend to disk', 'cmd', 'systemctl hibernate')

    return [lock, logout, sleep, sleep2, halt, halt2, reboot, reboot2, hibernate]

def get_calc_result():
    pass




def get_matches(query):

    matches = []

    if not query:
        return matches

    # Applications
    all_apps = utils.get_cached_data('apps', _get_apps, max_age=600)

    # System commands
    system_cmds = get_system_commands()

    # Files

    # Calculator.
    if any(i in query for i in '+-*/%^'):

        query = query.replace(' ', '').replace(',', '.')

        result = utils.get_cmd_output(['calc', query])

        if result:
            item = Item(title=result, subtitle='',
                        category='text')

            matches.append((item, 100))



    matches = utils.filter(query, all_apps+system_cmds) #, key=_search_key)

    #return utils.filter(query, _cmds, key=lambda x: x.title)


    pass
