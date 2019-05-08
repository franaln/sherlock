# System commands plugin

import re
from sherlock import utils

# Name, keys, icon, cmd
_cmds = [
    ('Sleep',     ('sleep', 'suspend'),             'system-suspend',     'systmectl suspend'),
    ('Power off', ('poweroff', 'halt', 'shutdown'), 'system-shutdown',    'systemctl poweroff'),
    ('Reboot',    ('reboot', 'reset'),              'system-reboot',      'systemctl reboot'),
    ('Hibernate', ('hibernate'),                    'system-hibernate',   'systemctl hibernate'),
    ('Lock',      ('lock',),                        'system-lock-screen', 'slimlock'),
    ('Logout',    ('logout', 'exit'),               'system-log-out',     'openbox --exit'),
]

_actions_hdmi = [
    ('HDMI (video only)',  'xrandr --output HDMI1 --auto && xrandr --output VGA1  --off ; xrandr --output eDP1  --off'),
    ('HDMI (video+audio)', 'pactl set-card-profile 0 output:hdmi-stereo && xrandr --output HDMI1 --auto && xrandr --output VGA1 --off && xrandr --output eDP1 --off'),
##    ('<- HDMI ',              (), '', 'pactl set-card-profile 0 output:analog-stereo+input:analog-stereo && xrandr --output eDP1 --auto && xrandr --output HDMI1 --off && xrandr --output VGA1 --off'),
##    ('eDP + HDMI', 'xrandr --output eDP1 --auto && xrandr --output HDMI1 --auto && xrandr --output VGA1 --off'),
]

_actions_vga = [
    ('-> VGA', 'xrandr --output VGA1 --auto && xrandr --output eDP1  --off && xrandr --output HDMI1 --off'),
    ('eDP + VGA', 'xrandr --output eDP1 --auto && xrandr --output VGA1  --auto && xrandr --output HDMI1 --off'),
    ('eDP', 'xrandr --output eDP1 --auto && xrandr --output HDMI1 --off && xrandr --output VGA1  --off'),
]

def _check_devices():
    devices = []

    output = utils.get_cmd_output(['xrandr', '-q'])
    for line in output.split('\n'):
        splitline = line.split()

        if not splitline[1] == 'connected':
            continue

        device = re.findall(r'^[a-zA-Z]+', splitline[0])[0]

        if device != 'eDP':
            devices.append(device)

    return devices


def get_items(query):

    for name, keys, icon, cmd in _cmds:
        yield {
            'text': name,
            'subtext': '',
            'keys': keys,
            'arg': cmd,
            'category': 'cmd',
            'icon': icon,
        }


def get_auto_items():

    devices = _check_devices()

    if devices:
        for dev in devices:
            if dev == 'HDMI':
                yield {
                    'text': '%s connected' % dev,
                    'keys': (dev,),
                    'icon': 'display',
                    'actions': _actions_hdmi,
                }
            elif dev == 'VGA':
                yield {
                    'text': '%s connected' % dev,
                    'keys': (dev,),
                    'icon': 'display',
                    'actions': _actions_vga,
                }
