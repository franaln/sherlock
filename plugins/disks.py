# Disks plugin

from item import Item
import utils

def get_matches(query):

    matches = []

    out = utils.get_cmd_output(['df', '-h'])

    out = out.split('\n')

    for line in out:
        if '/dev/' not in line:
            continue

        disk = line.split() ##// [filesystem, size, used, avail, use%, mount]

        title = '%s\t%s\t%s' % (disk[5], disk[1], disk[4])
        subtitle = 'Mounted as: %s' % disk[0]

        matches.append(Item(title, subtitle))

    return matches
