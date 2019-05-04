# System commands plugin

# Name, keys, icon, cmd
_cmds = [
    ('Sleep',     ('sleep', 'suspend'),             'system-suspend',     'systmectl suspend'),
    ('Power off', ('poweroff', 'halt', 'shutdown'), 'system-shutdown',    'systemctl poweroff'),
    ('Reboot',    ('reboot', 'reset'),              'system-reboot',      'systemctl reboot'),
    ('Hibernate', ('hibernate'),                    'system-hibernate',   'systemctl hibernate'),
    ('Lock',      ('lock',),                        'system-lock-screen', 'slimlock'),
    ('Logout',    ('logout', 'exit'),               'system-log-out',     'openbox --exit'),
]

def get_items():
    for name, keys, icon, cmd in _cmds:
        yield {
            'text': name,
            'subtext': '',
            'keys': keys,
            'arg': cmd,
            'category': 'cmd',
            'icon': icon,
        }
