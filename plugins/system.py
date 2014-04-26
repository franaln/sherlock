# System commands plugin

from item import Item
import utils

name     = 'System'
keyword  = 'system'

_cmds = (
    Item('Lock',      'Lock the screen', 'slimlock'),
    Item('Logout',    '',                'openbox --exit'),
    Item('Sleep',     'Suspend to RAM',  'systmectl suspend'),
    Item('Power off', '',                'systemctl poweroff'),
    Item('Reboot',    '',                'systemctl reboot'),
    Item('Hibernate', 'Suspend to disk', 'systemctl hibernate'),
)


def get_matches(query):

    matches = utils.filter(query, _cmds, key=lambda x: x.title)

    return matches
