# System commands plugin

from sherlock.items import ItemCmd

_cmds = [
    # power
    ItemCmd('Sleep',     'systmectl suspend'),
    ItemCmd('Power off', 'systemctl poweroff'),
    ItemCmd('Reboot',    'systemctl reboot'),
    ItemCmd('Hibernate', 'systemctl hibernate'),
    ItemCmd('Lock',      'slimlock'),
    ItemCmd('Logout',    'openbox --exit'),

    # blank
    ItemCmd('Pause screen blank',  'xset s off; xset -dpms'),
    ItemCmd('Resume screen blank', 'xset s on; xset +dpms'),

    # HDMI

]

def get_matches(query):
    for cmd in _cmds:
        yield cmd
