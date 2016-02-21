# System commands plugin

from sherlock.items import ItemCmd
from sherlock import utils

_cmds = [

    # power
    ItemCmd('Sleep',     'systmectl suspend'),
    ItemCmd('Power off', 'systemctl poweroff'),
    ItemCmd('Reboot',    'systemctl reboot'),
    ItemCmd('Hibernate', 'systemctl hibernate'),
    ItemCmd('Lock',      'slimlock'),
    ItemCmd('Logout', 'openbox --exit'),

    # blank
    ItemCmd('Pause screen blank', 'xset s off; xset -dpms'),
    ItemCmd('Resume screen blank', 'xset s on; xset +dpms'),

    # HDMI


]

# if utils.is_running('openbox'):
#     _cmds.append(ItemCmd('Logout', 'openbox --exit'))
# elif utils.is_running('compiz'):
#     _cmds.append(ItemCmd('Logout','killall compiz'))

def get_matches(query):
    return _cmds
