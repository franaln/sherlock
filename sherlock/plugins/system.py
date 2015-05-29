# System commands plugin

from sherlock.items import ItemCmd
from sherlock import utils

_cmds = [
    ItemCmd('Sleep',     'systmectl suspend'),
    ItemCmd('Power off', 'systemctl poweroff'),
    ItemCmd('Reboot',    'systemctl reboot'),
    ItemCmd('Hibernate', 'systemctl hibernate'),
    ItemCmd('Lock',      'slimlock'),
]

if utils.is_running('openbox'):
    _cmds.append(ItemCmd('Logout', 'openbox --exit'))
elif utils.is_running('compiz'):
    _cmds.append(ItemCmd('Logout','killall compiz'))

def get_matches(query):
    return _cmds
