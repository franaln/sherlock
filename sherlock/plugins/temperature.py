# Disks plugin

from sherlock.items import Item
from sherlock import utils

def get_matches(query):

    matches = []

    out = utils.get_cmd_output(['sensors',])

    out = out.split('\n')

    for line in out:
        if 'Core' not in line:
            continue

        core, temp = line.split(':') ##// [filesystem, size, used, avail, use%, mount]

        temp = temp.split()[0]

        title = '%s: %s' % (core, temp)  ##'%s \t\t %s / %s \t\t %s' % (disk[0], disk[2], disk[1], disk[4])
        subtitle = ''

        matches.append(Item(title, subtitle))

    return matches


# asus-isa-0000
# Adapter: ISA adapter
# temp1:        +73.0°C

# coretemp-isa-0000
# Adapter: ISA adapter
# Physical id 0:  +73.0°C  (high = +87.0°C, crit = +105.0°C)
# Core 0:         +73.0°C  (high = +87.0°C, crit = +105.0°C)
# Core 1:         +72.0°C  (high = +87.0°C, crit = +105.0°C)
