import os

class Item(object):

    def __init__(self, title, subtitle='', keys=[], category='text', arg=None, score=0.0, no_filter=False):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg
        self.score = score
        self.no_filter = no_filter
        # self.key = key

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
        return '[Item: %s (%s)]' % (self.title, self.score)


class ItemText(Item):
    def __init__(self, text, no_filter=False):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='text',
                      arg=None, no_filter=no_filter)

class ItemUri(Item):
    def __init__(self, path, no_filter=False):
        name = os.path.basename(path)
        path = path
        key = name

        if os.path.isdir(path):
            name = '%s/' % name
            path = '%s/' % path

        Item.__init__(self, title=name, subtitle=path, keys=[key,], category='uri',
                      arg=path, no_filter=no_filter)

    def is_dir(self):
        return os.path.isdir(self.arg)

    def is_file(self):
        return os.path.isfile(self.arg)


class ItemApp(Item):
    def __init__(self, name, exe, desktop, keys):
        Item.__init__(self, title=name, subtitle=exe,
                      keys=keys, category='app',
                      arg=desktop)

    def __cmp__(self, other):
        return (self.app_exe == other.app_exe)

class ItemCmd(Item):
    def __init__(self, text, cmd, no_filter=False):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='cmd',
                      arg=cmd, no_filter=no_filter)

class ItemAction(Item):
    def __init__(self, title, fn, no_filter=False):
        Item.__init__(self, title=title, subtitle='', keys=[title,], category='action',
                      arg=fn, no_filter=no_filter)

class ItemPlugin(Item):
    def __init__(self, title, kw):
        Item.__init__(self, title=title, subtitle='keyword: %s' % kw,
                      keys=[title,], category='plugin',
                      arg=title)

# class ItemToggle(Item):
#     def __init



actions = dict()

actions['app'] = [
    ('Run', 'run_app'),
    ('Run in terminal', 'run_app_in_terminal'),
]

actions['uri'] = [
    ('Open', 'open_uri'),
    ('Console', 'open_console_uri'),
    ('Open folder', 'open_folder'),
    ('Explore', 'explore'),
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
