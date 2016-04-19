# Screen plugin

import re
from sherlock import utils
from sherlock.items import ItemCmd

items_hdmi = [
    ItemCmd('-> HDMI (video+audio)', 'pactl set-card-profile 0 output:hdmi-stereo && xrandr --output HDMI1 --auto && xrandr --output VGA1 --off && xrandr --output eDP1 --off'),
    ItemCmd('-> HDMI (only video)',  'xrandr --output HDMI1 --auto && xrandr --output VGA1  --off ; xrandr --output eDP1  --off'),
    ItemCmd('<- HDMI ', 'pactl set-card-profile 0 output:analog-stereo+input:analog-stereo && xrandr --output eDP1 --auto && xrandr --output HDMI1 --off && xrandr --output VGA1 --off'),
    ItemCmd('eDP + HDMI', 'xrandr --output eDP1 --auto && xrandr --output HDMI1 --auto && xrandr --output VGA1 --off'),
]

items_vga = [
    ItemCmd('-> VGA', 'xrandr --output VGA1 --auto && xrandr --output eDP1  --off && xrandr --output HDMI1 --off'),
    ItemCmd('eDP + VGA', 'xrandr --output eDP1 --auto && xrandr --output VGA1  --auto && xrandr --output HDMI1 --off'),
    ItemCmd('eDP', 'xrandr --output eDP1 --auto && xrandr --output HDMI1 --off && xrandr --output VGA1  --off'),
]

def _check_devices():
    devices = []

    output = utils.get_cmd_output(['xrandr', '-q'])
    for line in output.split('\n'):
        splitline = line.split()

        if not splitline[1] == 'connected':
            continue

        device = re.findall(r'^[a-zA-Z]+', splitline[0])[0]

        devices.append(device)

    return devices

def get_matches(query):

    items = []

    devices = _check_devices()

    if 'HDMI' in devices:
        items.extend(items_hdmi)

    if 'VGA' in devices:
        items.extend(items_vga)

    return items
