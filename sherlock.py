#! /usr/bin/env python

# Sherlock - olgaaa but smart
#
# Usage: olgaaa [option] or olgaaa
#
# *Needs dmenu patched with the qxyw patch*

# dmenu config
font = 'Cantarell-12'
sf_color = '#ffffff' # selected text
sb_color = '#427fed' # selected background
nf_color = '#333333' # normal text
nb_color = '#f9f9f9' # normal background
height = 28
lines = 10

# olgaaa config
cachedir = "$HOME/.cache/olgaaa"
open = ow
filemanager=dolphin
console=urxvtdc
browser=chromium

# Center dmenu in the screen
xres=`xdpyinfo | grep 'dimensions:' | awk '{print $2}' | cut -dx -f1`
width=$[$xres / 4]
xpos=$[$xres / 2 - $width / 2]
yres=`xdpyinfo | grep 'dimensions:' | awk '{print $2}' | cut -dx -f2`
ypos=$[$yres / 2 - $height*$lines / 2]


# Execute dmenu with the specific options. Takes the prompt text as an option
def dmenu():
dmenu -i -l "$lines" -fn "$font" -sf "$sf_color" -sb "$sb_color" -nf "$nf_color" -nb "$nb_color" -h "$height" -w "$width" -y "$ypos" -x "$xpos" -p $1


option=""

# If there is no input show options...
if [ $# -eq 0 ] ; then
    opts=("apps" "google" "explore" "power" "screen" "search" "calc")

    choice=$(printf "%s\n" "${opts[@]}" | xdmenu "olgaaa")
    if [ "$choice" == "" ] ; then
        exit 1
    else
        option=$choice
    fi

# Else go to the correspondig option
else
    option=$1
fi


# Different launcher options
case "$option" in

    ## Open apps. Show recent apps first
    apps)

        max_recent=50 # Number of recent commands to track
        recent_cache="$cachedir/apps_recent"
        rest_cache="$cachedir/apps_all"

        mkdir -p $cachedir
        touch $recent_cache

        IFS=:
        if stest -dqr -n "$rest_cache" $PATH; then
            stest -flx $PATH | sort -u | grep -vf "$recent_cache" > "$rest_cache"
        fi

        IFS=" "
        cmd=$(cat "$recent_cache" "$rest_cache" | xdmenu "apps") || exit

        if ! grep -qx "$cmd" "$recent_cache" &> /dev/null; then
            grep -vx "$cmd" "$rest_cache" > "$rest_cache.$$"
            mv "$rest_cache.$$" "$rest_cache"
        fi
        echo "$cmd" > "$recent_cache.$$"
        grep -vx "$cmd" "$recent_cache" | head -n "$max_recent" >> "$recent_cache.$$"
        mv "$recent_cache.$$"  "$recent_cache"

        ($cmd | ${SHELL:-"/bin/sh"} &)
        ;;


    ## Power options
    power)
        power_opts=("lock" "logout" "suspend" "poweroff" "reboot" "hibernate")

        choice=$(printf "%s\n" "${power_opts[@]}" |  xdmenu "power")

        if [ "$choice" = "" ] ; then
            exit 1
        elif [ "$choice" = "logout" ] ; then
            openbox --exit
        elif [ "$choice" = "lock" ] ; then
            slimlock
            exit 0
        else
            systemctl $choice
            exit 0
        fi
        ;;


    ## Calculator
    calc)

        result=$(xdmenu "calc" | xargs echo | calc | sed "s/\t//g")

        if [ "$result" != "" ] ; then
            echo $result | xdmenu "result"
            exit 0
        else
            exit 1
        fi
        ;;

    ## Search files
    search)

        input=$(xdmenu "search")

        result=""
        if [ "$input" != '' ] ; then
            result=$(echo "$input" | locate -e -r "$input" | xdmenu "result" )
        else
            return 1
        fi

        if [ "$result" != "" ] ; then
            $open "$result"
        else
            return 1
        fi
        ;;

    ## Screen/VGA/HDMI options
    screen)

        devices=$(xrandr -q | grep [[:upper:]]1)

        availableopts="Laptop only"

        if [[ $devices == *"VGA1 connected"* ]] ; then
            availableopts+="\nVGA only\nLatop & VGA"
        fi

        if [[ $devices == *"HDMI1 connected"* ]] ; then
            availableopts+="\nHDMI only\nHDMI & Laptop"
        fi

        choice=$(echo -e $availableopts | xdmenu "screens")

        case "$choice" in
            "Laptop only")
                xrandr --output eDP1 --auto
                xrandr --output HDMI1 --off
                xrandr --output VGA1  --off
                ;;
            "VGA only")
                xrandr --output VGA1  --auto
                xrandr --output eDP1  --off
                xrandr --output HDMI1 --off
                ;;
            "HDMI only")
                xrandr --output HDMI1 --auto
                sleep 2
                xrandr --output VGA1  --off
                xrandr --output eDP1  --off
                ;;
            "Laptop & VGA")
                xrandr --output eDP1  --auto
                xrandr --output VGA1  --auto
                xrandr --output HDMI1 --off
                ;;
            "Laptop & HDMI")
                xrandr --output eDP1  --auto
                xrandr --output HDMI1 --auto
                xrandr --output VGA1  --off
                ;;
        esac
        exit 0
        ;;


    # Explore files
    explore)

        cd "$HOME"

        choice=1
        while [ "$choice" ]; do

            choice=$((echo ".." ; ls $PWD ; echo "[Open]") | xdmenu "[$(basename $(pwd))]")

            if [ "$choice" ] ; then

                # change dir by hand
                if [[ "$choice" == "cd "* ]] ; then
                    goto=$(echo $choice | cut -d ' ' -f 2)

                    if [ -d $goto ] ; then
                        cd $goto
                    else
                        exit 1
                    fi

                # Folder -> go inside
                elif [[ -d "$choice" ]] ; then
                    cd "$choice"

                # .. -> go up
                elif [ "$choice" == ".." ] ; then
                    cd ..

                # [Open] -> open current dir in $fm
                elif [ "$choice" == "[Open]" ] ; then
                    setsid $filemanager "$PWD"
                    unset file
                    exit 0

                # File -> open
                else
                    $open $choice
                    unset file
                    exit 0
                fi
            fi
        done
        ;;


    # Search in google
    google)

        GS=$(xsel -o | xdmenu "google")

        if [ "$GS" != "" ] ; then
            $browser  http://www.google.com.ar/search?q="$GS"
            wmctrl -a $browser
        else
            return 0
        fi
        ;;

    # mount)

    #     choice=$(cat /proc/partitions | grep -o sd[[:alpha:]] | grep -v major | grep -v "sda" | xdmenu "mount")

    #   if [[ $choice == "" ]] ; then
    #       exit 1
    #   else
    #         mkdir -p /media/$choice
    #       mount -U 1000 $choice /media/$choice
    #     fi
    #     ;;

    # umount)

    #     usb=$(mount | awk '$3 ~ /\/media\// || /\/mnt\// { print $3 }' | xdmenu "umount")

    #     if [[ "$usb" == "" || ! -d "$usb" ]]; then
    #         exit 1
    #     fi

    #     if umount "$usb"; then
    #         notify-send "You can now safely remove $usb"
    #     else
    #         notify-send "Some apps are using $usb"
    #     fi
    #     exit 0
    #     ;;

esac
