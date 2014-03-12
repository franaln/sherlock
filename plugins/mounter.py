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
