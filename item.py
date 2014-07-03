class Item(object):

    def __init__(self, title, subtitle='', category='text', arg=None, score=0.0):
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.arg = arg
        self.score = score

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
