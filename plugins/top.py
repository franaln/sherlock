import os
import signal
import operator

#from plugin import Plugin

# class Task(Leaf):
#     def __init__(self, path, name, description=None):
#         Leaf.__init__(self, path, name)
#         self._description = description

#     def get_description(self):
#         return self._description

#     def get_actions(self):
#         yield SendSignal()

#     def get_icon_name(self):
#         return 'applications-system'


# class SendSignal(Action):
#     def __init__(self):
#         Action.__init__(self, 'Send Signal')

#     def activate(self, leaf, iobj):
#         os.kill(leaf.object, iobj.object)

#     def requires_object(self):
#         return True

#     def object_types(self):
#         yield _Signal

#     def object_source(self, for_item=None):
#         return _SignalsSource()


# class _Signal(Leaf):
#     def get_description(self):
#         return "kill -%s ..." % self.object


# get all signals from signal package
# _SIGNALS = [
#         _Signal(getattr(signal, signame), signame[3:])
#         for signame in sorted(dir(signal))
#         if signame.startswith('SIG') and not signame.startswith('SIG_')
# ]


# class _SignalsSource(Source):
#         def __init__(self):
#                 Source.__init__(self, _("Signals"))

#         def get_items(self):
#                 return _SIGNALS

#         def provides(self):
#                 yield _Signal


# class TaskSource(Source, PicklingHelperMixin):
#         task_update_interval_sec = 5

#         def __init__(self, name=_("Running Tasks")):
#                 Source.__init__(self, name)
#                 self._cache = []
#                 self._version = 2

#         def pickle_prepare(self):
#                 # clear saved processes
#                 self.mark_for_update()

#         def initialize(self):
#                 self._timer = scheduler.Timer()

#         def finalize(self):
#                 self._timer = None
#                 self._cache = []

#         def _async_top_finished(self, acommand, stdout, stderr):
#                 self._cache = []

#                 processes = parse_top_output(stdout)
#                 # sort processes (top don't allow to sort via cmd line)
#                 if __kupfer_settings__['sort_order'] == _("Memory usage (descending)"):
#                         processes = sorted(processes, key=operator.itemgetter(2),
#                                            reverse=True)
#                 elif __kupfer_settings__['sort_order'] == _("Commandline"):
#                         processes = sorted(processes, key=operator.itemgetter(4))
#                 # default: by cpu

#                 fields = _("pid: %(pid)s  cpu: %(cpu)g%%  mem: %(mem)g%%  time: %(time)s")
#                 for pid, cpu, mem, ptime, cmd in processes:
#                         description = fields % dict(pid=pid, cpu=cpu, mem=mem, time=ptime)
#                         self._cache.append(Task(pid, cmd, description))

#                 self.mark_for_update()

#         def _async_top_start(self):
#                 uid = os.getuid()
#                 utils.AsyncCommand(["top", "-b", "-n", "1", "-u", "%d" % uid],
#                                    self._async_top_finished, 60, env=["LC_NUMERIC=C"])

#         def get_items(self):
#                 for task in self._cache:
#                         yield task
#                 update_wait = self.task_update_interval_sec if self._cache else 0
#                 # update after a few seconds
#                 self._timer.set(update_wait, self._async_top_start)

#         def get_description(self):
#                 return _("Running tasks for current user")

#         def get_icon_name(self):
#                 return "system"

#         def provides(self):
#                 yield Task


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


import os
import utils

from items import Item

def get_matches(query):

    uid = os.getuid()

    out = utils.get_cmd_output(["top", "-b", "-n", "1", "-u", "%d" % uid])


    processes = [process for process in parse_top_output(out)]

    # sort processes (top don't allow to sort via cmd line)
    processes = sorted(processes, key=operator.itemgetter(2),
                       reverse=True)

    items = []
    for p in processes:

        title = os.path.basename(p[4])
        subtitle = '%s, %s, %s, %s' % (p[0], p[1], p[2], p[3])

        items.append(Item(title, subtitle))

    return items

# fields = _("pid: %(pid)s  cpu: %(cpu)g%%  mem: %(mem)g%%  time: %(time)s")
# for pid, cpu, mem, ptime, cmd in processes:
#     description = fields % dict(pid=pid, cpu=cpu, mem=mem, time=ptime)
#     self._cache.append(Task(pid, cmd, description))
