import os
import operator

import sherlock.utils as utils

from sherlock.items import Item

def parse_top_output(out):

    """
    Yield tuples of (pid, cpu, mem, ptime, cmd)
    """

    fields_map = None
    fields_count = 0
    header_read = False
    for line in out.split('\n'):
        line = line.strip()
        if line == '':
            header_read = True
            continue

        if not header_read:
            continue

        if line.startswith('PID'): # assume pid is first col
            fields_map = dict(((name, pos) for pos, name in enumerate(line.split())))
            fields_count = len(fields_map)
            continue	# skip header

        line_fields = line.split(None, fields_count-1)
        pid = line_fields[0]
        cpu = line_fields[fields_map['%CPU']]
        mem = line_fields[fields_map['%MEM']]
        ptime = line_fields[fields_map['TIME+']]
        cmd = line_fields[-1]

        # read command line
        proc_file = '/proc/%s/cmdline' % pid
        if os.path.isfile(proc_file): # also skip (finished) missing tasks
            with open(proc_file, 'rt') as f:
                cmd = f.readline().replace('\x00', ' ') or cmd

        cmd = cmd.split()[0]

        yield (int(pid), float(cpu), float(mem), ptime, cmd)



def get_matches(query):

    uid = os.getuid()

    out = utils.get_cmd_output(["top", "-b", "-n", "1", "-u", "%d" % uid])


    processes = [process for process in parse_top_output(out)]

    # sort processes (top don't allow to sort via cmd line)
    processes = sorted(processes, key=operator.itemgetter(2),
                       reverse=True)

    items = []
    for p in processes:

        title = (os.path.basename(p[4]), 'cpu: %s %%' % p[1], 'mem: %s%%' % p[2])
        subtitle = 'pid: %s' % (p[0])

        items.append(Item(title, subtitle))

    return items

# fields = _("pid: %(pid)s  cpu: %(cpu)g%%  mem: %(mem)g%%  time: %(time)s")
# for pid, cpu, mem, ptime, cmd in processes:
#     description = fields % dict(pid=pid, cpu=cpu, mem=mem, time=ptime)
#     self._cache.append(Task(pid, cmd, description))
