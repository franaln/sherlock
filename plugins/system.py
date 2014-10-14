# System commands plugin

from items import Item
import utils

_cmds = (
    Item('Lock',      '',  'cmd', 'slimlock'),
    Item('Logout',    '',  'cmd', 'openbox --exit'),
    #Item('Logout',    '', 'cmd', 'killall compiz'),
    Item('Sleep',     '',  'cmd', 'systmectl suspend'),
    Item('Power off', '',  'cmd', 'systemctl poweroff'),
    Item('Reboot',    '',  'cmd', 'systemctl reboot'),
    Item('Hibernate', '',  'cmd', 'systemctl hibernate'),
)


def get_matches(query):

    return utils.filter(query, _cmds, key=lambda x: x.title)
