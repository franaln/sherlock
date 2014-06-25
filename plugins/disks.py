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

        matches.append(Item(disk[0]))

    return matches
