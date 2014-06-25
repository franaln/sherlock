# System commands plugin

from item import Item
import utils

name = 'System'

_cmds = (
    Item('Lock',      'Lock the screen',      'cmd', 'slimlock'),
    #Item('Logout',    '',                     'cmd', 'openbox --exit'),
    Item('Logout',    '',                     'cmd', 'killall compiz'),
    Item('Sleep',     'Suspend to RAM',       'cmd', 'systmectl suspend'),
    Item('Power off', 'Power off the system', 'cmd', 'systemctl poweroff'),
    Item('Reboot',    'Reboot the system',    'cmd', 'systemctl reboot'),
    Item('Hibernate', 'Suspend to disk',      'cmd', 'systemctl hibernate'),
)


def get_matches(query):

    return utils.filter(query, _cmds, key=lambda x: x.title)
