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

def get_matches(query=None):

    devices = _check_devices()

    for dev in devices:
        if _is_mounted(dev):
            yield ItemCmd('Unmount /dev/%s' % dev, 'udisks --unmount /dev/%s' % dev)
        else:
            yield ItemCmd('Mount /dev/%s' % dev, 'udisks --mount /dev/%s' % dev)
