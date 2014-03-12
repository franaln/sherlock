#     ## Screen/VGA/HDMI options
#     screen)

#         devices=$(xrandr -q | grep [[:upper:]]1)

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
