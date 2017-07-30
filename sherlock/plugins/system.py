# System commands plugin

from sherlock.items import ItemCmd

_cmds = [
    ItemCmd('Sleep',     'systmectl suspend'),
    ItemCmd('Power off', 'systemctl poweroff'),
    ItemCmd('Reboot',    'systemctl reboot'),
    ItemCmd('Hibernate', 'systemctl hibernate'),
    ItemCmd('Lock',      'slimlock'),
    ItemCmd('Logout',    'openbox --exit'),
]

def get_items():
    for cmd in _cmds:
        yield cmd
