import os

class Item(object):

    __slots__ = ('text', 'subtext', 'icon', 'keys', 'arg', 'category', 'score', 'bonus')

    def __init__(self, text, subtext='', category='text', icon='', keys=[], arg=None):
        self.text = text
        self.subtext = subtext
        self.icon = icon

        if isinstance(keys, str): # list of strings used to filter items
            self.keys = [keys,]
        else:
            self.keys = keys
        self.arg = arg   # string passed as argument to actions

        self.category = category

        self.score = 0 # temporal values to store the sorting scores
        self.bonus = 0

    @classmethod
    def from_dict(cls, d):
        return cls(d['text'], d['subtext'], d['category'], d['icon'], d['keys'], d['arg'])

    def to_dict(self):
        return {
            'text': self.text,
            'subtext': self.subtext,
            'icon': self.icon,
            'keys': self.keys,
            'arg': self.arg,
        }

    def __str__(self):
        return '%s (%s)' % (self.text, self.score)

    def __eq__(self, other):
        return (self.to_dict() == other.to_dict())
