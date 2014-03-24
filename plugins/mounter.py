from plugin import Plugin


class MounterPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Mounter', keywords=['mount', 'umount'], True)

        self._matches = []
        self._actions = []

    def get_devices():
        output = check_output('cat /proc/partitions')
        devs = [v for v in re.findall('sd[a-z]', output) if v != 'sda']
        return devs




    def get_matches(self, query):







def mount

mkdir -p /media/name
mount -U 1000 dev /media/choice


#     # mount)

#     #     choice=$(cat /proc/partitions | grep -o sd[[:alpha:]] | grep -v major | grep -v "sda" | xdmenu "mount")

#     #   if [[ $choice == "" ]] ; then
#     #       exit 1
#     #   else
#     #         mkdir -p /media/$choice
#     #       mount -U 1000 $choice /media/$choice
#     #     fi
#     #     ;;

#     # umount)

#     #     usb=$(mount | awk '$3 ~ /\/media\// || /\/mnt\// { print $3 }' | xdmenu "umount")

#     #     if [[ "$usb" == "" || ! -d "$usb" ]]; then
#     #         exit 1
#     #     fi

#     #     if umount "$usb"; then
#     #         notify-send "You can now safely remove $usb"
#     #     else
#     #         notify-send "Some apps are using $usb"
#     #     fi
#     #     exit 0
#     #     ;;


    target=( $(awk '/media\/[\^A-Z]/ {print $3}' <(mount)) )
    #shares=(Safebox Scout Sentinel)

    checkbusy() {
        grep "PID" <(lsof +d "$target" &>/dev/null)
        if [[ $? -eq 0 ]]; then
            printf "%s\n" "${target##*/} busyâ€¦"
            exit 1
        fi
    }

    exstatus() {
        if [[ $? -eq 0 ]]; then
            printf "%s\n" "${target##*/} unmountedâ€¦"
        else
            printf "%s\n" "Failed to unmount."
        fi
    }

    # check for multiple devices
    if (( "${#target[@]}" > 1 )); then
        choice=$(echo $target | xmenu "umount")
    fi

    # check for share
    for drive in "${shares[@]}"; do
        if [[ "$drive" = "${target##*/}" ]]; then
            share="$drive"
        fi
    done

    # options per filesystem
    if [[ -n "$target" ]]; then
        for drive in "${shares[@]}"; do
            if [[ "$drive" = "${target##*/}" && "${target##*/}" = Safebox ]]; then
                cmd=$(sudo safebox close)
            elif [[ "$drive" = "${target##*/}" ]]; then
                cmd=$(sudo umount "$target")
        else
                cmd=$(udiskie-umount -d "$target" &>/dev/null)
            fi
        done
    # do it
        checkbusy
        # flush to disk
        /usr/bin/sync && $cmd
        exstatus
    else
    printf "%s\n" "No drive mounted!"
    fi
}
