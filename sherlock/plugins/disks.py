# Disks plugin

from sherlock.items import Item
from sherlock import utils

def get_matches(query):

    out = utils.get_cmd_output(['df', '-h'])

    out = out.split('\n')

    for line in out:
        if '/dev/' not in line or 'tmp' in line:
            continue

        disk = line.split() ##// [filesystem, size, used, avail, use%, mount]

        title = [disk[5], '%s / %s (%s)' % (disk[2], disk[1], disk[4])]
        subtitle = 'Mounted as: %s' % disk[0]

        yield Item(title, subtitle)
