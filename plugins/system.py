# System commands plugin

from plugin import Plugin

class SystemPlugin(Plugin):

    cmds = (
        ('Lock',      'Lock the screen', 'slimlock'),
        ('Logout',    '',                'openbox --exit'),
        ('Sleep',     'Suspend to RAM',  'systmectl suspend'),
        ('Power off', '',                'systemctl poweroff'),
        ('Reboot',    '',                'systemctl reboot'),
        ('Hibernate', 'Suspend to disk', 'systemctl hibernate'),
    )

    def __init__(self):
        Plugin.__init__(self, 'System')
        self._matches = []

    def get_matches(self, query):
        self.clear_matches()

        cmds = self.filter(query, self.cmds, key=lambda x: x[0], include_score=True)

        for m in cmds:
            self.add_match(text=m[0][0], subtext=m[0][1], score=m[1], arg=m[0][2], type='cmd')

        return self._matches
