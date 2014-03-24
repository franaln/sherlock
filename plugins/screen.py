# Screen plugin

import re
from plugin import Plugin
from utils import check_output

class ScreenPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, 'Screen', 'screen', True)
        self._matches = []

    def check_devices(self):
        devices = []

        output = check_output(['xrandr', '-q'])
        for line in output.split('\n'):
            splitline = line.split()

            if not splitline[1] in ['connected', 'disconnected']:
                continue

            device = re.findall(r'^[a-zA-Z]+', splitline[0])[0]
            status = splitline[1]

            devices.append((device, status))

        return devices

    def get_matches(self, query):
        self.clear_matches()

        devices = self.check_devices()

        for dev in devices:
            if dev[1] == 'connected':
                self.add_match(text=dev[0], subtext=dev[1])


        # Also add the combinations




        return self._matches
#         availableopts="Laptop only"

#         if [[ $devices == *"VGA1 connected"* ]] ; then
#             availableopts+="\nVGA only\nLatop & VGA"
#         fi

#         if [[ $devices == *"HDMI1 connected"* ]] ; then
#             availableopts+="\nHDMI only\nHDMI & Laptop"
#         fi

#         choice=$(echo -e $availableopts | xdmenu "screens")

#         case "$choice" in
#             "Laptop only")
#                 xrandr --output eDP1 --auto
#                 xrandr --output HDMI1 --off
#                 xrandr --output VGA1  --off
#                 ;;
#             "VGA only")
#                 xrandr --output VGA1  --auto
#                 xrandr --output eDP1  --off
#                 xrandr --output HDMI1 --off
#                 ;;
#             "HDMI only")
#                 xrandr --output HDMI1 --auto
#                 sleep 2
#                 xrandr --output VGA1  --off
#                 xrandr --output eDP1  --off
#                 ;;
#             "Laptop & VGA")
#                 xrandr --output eDP1  --auto
#                 xrandr --output VGA1  --auto
#                 xrandr --output HDMI1 --off
#                 ;;
#             "Laptop & HDMI")
#                 xrandr --output eDP1  --auto
#                 xrandr --output HDMI1 --auto
#                 xrandr --output VGA1  --off
#                 ;;
#         esac
#         exit 0
#         ;;
