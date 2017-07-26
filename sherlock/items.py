import os

class Item(object):

    __slots__ = ('title', 'subtitle', 'category', 'arg', 'score', 'keys')

    def __init__(self, title, subtitle='', keys=[], category='text', arg=None, score=0.0):
        self.title = title
        self.subtitle = subtitle
        self.keys = keys
        self.category = category
        self.arg = arg

        self.score = score # temporal because it depends the query (0. by default)

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
        return (self.to_dict() == other.to_dict())

    def get_actions(self):
        return (
            ('Copy', 'copy_to_clipboard'),
            # ('Large type',   'show_large_type'),
            # ('Show QR code', 'show_qrcode'),
        )



# Apps
class ItemApp(Item):
    def __init__(self, title, subtitle, arg, keys):
        Item.__init__(self, title=title, subtitle=subtitle,
                      keys=keys, category='app',
                      arg=arg)

    def get_actions(self):
        return (
            ('Run', 'run_app'),
            ('Run in terminal', 'run_app_in_terminal'),
        )


# Files
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
            ('Open',        'open_uri'),
            ('Open folder', 'open_folder'),
            ('Explore',     'explore'),
        )


# Text
class ItemText(Item):
    def __init__(self, text):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='text',
                      arg=None)

    def get_actions(self):
        return (
            ('Copy',         'copy_to_clipboard'),
            # ('Large type',   'show_large_type'),
            # ('Show QR code', 'show_qrcode'),
        )


# Command
class ItemCmd(Item):
    def __init__(self, text, cmd):
        Item.__init__(self, title=text, subtitle='', keys=[text,], category='cmd',
                      arg=cmd)

    def get_actions(self):
           return (
               ('Run', 'run_cmd'),
               ('Copy to console', 'copy_to_console')
           )


# class ItemAction(Item):
#     def __init__(self, title, fn, no_filter=False):
#         Item.__init__(self, title=title, subtitle='', keys=[title,], category='action',
#                       arg=fn)

# class ItemPlugin(Item):
#     def __init__(self, title, kw):
#         Item.__init__(self, title=title, subtitle='keyword: %s' % kw,
#                       keys=[title,], category='plugin',
#                       arg=kw)

#         self.items = []
#         self.score = 200

#     def add(self, it):
#         self.items.append(it)
