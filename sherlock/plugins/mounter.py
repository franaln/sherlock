import re
from sherlock import utils
from sherlock.items import ItemCmd

def _check_devices():

    output = utils.get_cmd_output(['cat', '/proc/partitions'])

    devs = [v for v in re.findall('sd[b-z].', output)] # if v != 'sda']

    return devs


def _is_mounted(dev):

    output = utils.get_cmd_output(['udisks', '--show-info', '/dev/%s' % dev])

    for line in output.split('\n'):

        if not line.strip().startswith('is mounted:'):
            continue

        key, value = line.split(':')

        return bool(int(value))



def get_matches(query):

    devices = _check_devices()

    for dev in devices:

        if _is_mounted(dev):
            yield ItemCmd('Unmount /dev/%s' % dev, 'udisks --unmount /dev/%s' % dev)
        else:
            yield ItemCmd('Mount /dev/%s' % dev, 'udisks --mount /dev/%s' % dev)









#     target=( $(awk '/media\/[\^A-Z]/ {print $3}' <(mount)) )
#     #shares=(Safebox Scout Sentinel)

#     checkbusy() {
#         grep "PID" <(lsof +d "$target" &>/dev/null)
#         if [[ $? -eq 0 ]]; then
#             printf "%s\n" "${target##*/} busyâ€¦"
#             exit 1
#         fi
#     }

#     exstatus() {
#         if [[ $? -eq 0 ]]; then
#             printf "%s\n" "${target##*/} unmountedâ€¦"
#         else
#             printf "%s\n" "Failed to unmount."
#         fi
#     }

#     # check for multiple devices
#     if (( "${#target[@]}" > 1 )); then
#         choice=$(echo $target | xmenu "umount")
#     fi

#     # check for share
#     for drive in "${shares[@]}"; do
#         if [[ "$drive" = "${target##*/}" ]]; then
#             share="$drive"
#         fi
#     done

#     # options per filesystem
#     if [[ -n "$target" ]]; then
#         for drive in "${shares[@]}"; do
#             if [[ "$drive" = "${target##*/}" && "${target##*/}" = Safebox ]]; then
#                 cmd=$(sudo safebox close)
#             elif [[ "$drive" = "${target##*/}" ]]; then
#                 cmd=$(sudo umount "$target")
#         else
#                 cmd=$(udiskie-umount -d "$target" &>/dev/null)
#             fi
#         done
#     # do it
#         checkbusy
#         # flush to disk
#         /usr/bin/sync && $cmd
#         exstatus
#     else
#     printf "%s\n" "No drive mounted!"
#     fi
# }
