import os

class Item(object):

    def __init__(self, title, subtitle='', category='text', arg=None, score=0.0, no_filter=False):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg
        self.score = score
        self.no_filter = no_filter

        if category == 'text' and arg is None:
            self.arg = self.title

    @classmethod
    def from_dict(cls, d):
        return cls(d['title'], d['subtitle'], d['category'], d['arg'])

    def to_dict(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'category': self.category,
            'arg': self.arg
        }


class ItemText(Item):
    def __init__(self, text, score):
        Item.__init__(self, title=text, subtitle='', category='text', arg=None, score=score)


class ItemUri(Item):
    def __init__(self, path):
        name = os.path.basename(path)
        Item.__init__(self, title=name, subtitle=path, category='uri', arg=path)


class ItemApp(Item):
    def __init__(self, text, score):
        Item.__init__(self, title=text, subtitle='', category='text', arg=None, score=score)


class ItemCmd(Item):
    def __init__(self, text, score):
        Item.__init__(self, title=text, subtitle='', category='text', arg=None, score=score)
