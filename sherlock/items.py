import os

class Item(object):

    __slots__ = ('title', 'subtitle', 'category', 'arg', 'score', 'keys')

    def __init__(self, title, subtitle='', keys=[], category='text', arg=None, score=0.0):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg
        self.score = score
        self.keys = keys

        if category == 'text' and arg is None:
            self.arg = self.title

    @classmethod
    def from_dict(cls, d):
        return cls(d['title'], d['subtitle'], d['keys'], d['category'], d['arg'])

    def to_dict(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'keys': self.keys,
            'category': self.category,
            'arg': self.arg
        }

    def __str__(self):
        return '%s (%s)' % (self.title, self.score)

    def __eq__(self, other):
        return (self.title == other.title and
                self.subtitle == other.subtitle and
                self.category == other.category and
                self.arg == other.arg)

    def get_actions(self):
        return (
            ('Copy', 'copy_to_clipboard'),
            ('Large type', 'show_large_type'),
            ('Show QR code', 'show_qrcode'),
        )


class ItemText(Item):
    def __init__(self, text):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='text',
                      arg=None)

    def get_actions(self):
        return (
            ('Copy', 'copy_to_clipboard'),
            ('Large type', 'show_large_type'),
            ('Show QR code', 'show_qrcode'),
        )

    def copy_to_clipboard(self):
        # "primary":
        xsel_proc = subprocess.Popen(['xsel', '-pi'], stdin=subprocess.PIPE)
        xsel_proc.communicate(self.arg.encode('utf-8'))

        # "clipboard":
        xsel_proc = subprocess.Popen(['xsel', '-bi'], stdin=subprocess.PIPE)
        xsel_proc.communicate(self.arg.encode('utf-8'))


class ItemUri(Item):
    def __init__(self, name, path):

        path = path
        key = name

        if os.path.isdir(path):
            name = '%s/' % name
            path = '%s/' % path

        Item.__init__(self, title=name, subtitle=path, keys=[key,], category='uri',
                      arg=path.replace(' ', r'%20'))

    def is_dir(self):
        return self.path.endswith('/') #os.path.isdir(self.arg)

    def is_file(self):
        return (not self.path.endswith('/')) #os.path.isfile(self.arg)

    def get_actions(self):
        return (
            ('Open', 'open_uri'),
            ('Open folder', 'open_folder'),
            ('Explore', 'explore'),
        )

    def open_uri(self):
        run_cmd_setsid('open file://' + self.arg)

    def open_folder(self):
        if self.is_file():
            dir_ = '/'.join(self.arg.split('/')[:-1])
        else:
            dir_ = self.arg

        run_cmd_setsid('thunar '+dir_)

    def explore(self):
        pass


class ItemApp(Item):
    def __init__(self, name, exe, desktop, keys):
        Item.__init__(self, title=name, subtitle=exe,
                      keys=keys, category='app',
                      arg=desktop)

    def __cmp__(self, other):
        return (self.app_exe == other.app_exe)

    def get_actions(self):
        return (
            ('Run', 'run_app'),
            ('Run in terminal', 'run_app_in_terminal'),
        )

    def run_app(self):
        run_cmd_setsid(self.arg)

    def run_app_in_terminal(self):
        print('urxvtc -e "%s"' % arg)
        os.system('setsid urxvt -e "%s" +hold' % arg)


class ItemCmd(Item):
    def __init__(self, text, cmd):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='cmd',
                      arg=cmd)

    def get_actions(self):
           return (
               ('Run', 'run_cmd'),
               ('Copy to console', 'copy_to_console')
           )

    def run_cmd(self):
        pass

    def copy_to_console(self):
        pass

class ItemAction(Item):
    def __init__(self, title, fn, no_filter=False):
        Item.__init__(self, title=title, subtitle='', keys=[title,], category='action',
                      arg=fn)

class ItemPlugin(Item):
    def __init__(self, title, kw):
        Item.__init__(self, title=title, subtitle='keyword: %s' % kw,
                      keys=[title,], category='plugin',
                      arg=kw)

        self.items = []
        self.score = 200

    def add(self, it):
        self.items.append(it)



actions = dict()

actions['app'] = [
    ('Run', 'run_app'),
    ('Run in terminal', 'run_app_in_terminal'),
]

actions['uri'] = [
    ('Open', 'open_uri'),
    ('Open folder', 'open_folder'),
    ('Explore', 'explore'),
    #('Console', 'open_console_uri'),
]

actions['cmd'] = [
    ('Run', 'run_cmd'),
    ('Copy to console', 'copy_to_console')
]

actions['text'] = [
    ('Copy', 'copy_to_clipboard'),
    ('Large type', 'show_large_type'),
    ('Show QR code', 'show_qrcode'),
]
