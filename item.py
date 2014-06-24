class Item(object):

    def __init__(self, title, subtitle='', category='text', arg=None):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg

        if category == 'text' and arg is None:
            self.arg = self.title

    def __str__(self):
        return '%s' % self.title

    def __eq__(self, other):
        return (self.title == other.title and
                self.subtitle == other.subtitle and
                self.category == other.category and
                self.arg == other.arg)

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
