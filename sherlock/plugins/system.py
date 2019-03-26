# System commands plugin

_cmds = [
    ('Sleep',     'systmectl suspend'),
    ('Power off', 'systemctl poweroff'),
    ('Reboot',    'systemctl reboot'),
    ('Hibernate', 'systemctl hibernate'),
    ('Lock',      'slimlock'),
    ('Logout',    'openbox --exit'),
]

def get_items():
    for name, cmd in _cmds:
        yield {'text': name, 'subtext': '', 'keys': (name,), 'arg': cmd, 'category': 'cmd'}
