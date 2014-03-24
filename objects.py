# objects

# Base object class: every item is showable in Menu
class Item(object):
    def __init__(self, title, subtitle='', more=False, rtext=''):
        self.title = title
        self.subtitle = subtitle
        self.more = more
        self.rtext = rtext

class Match(Item):
    def __init__(self, title, subtitle='', actionable=False,
                 arg=None, uid=None, score=0, plugin=None, actions=[]):

        Item.__init__(self, title, subtitle)
        self.title = title
        self.subtitle = subtitle
        self.actionable = actionable
        self.arg = arg
        self.uid = uid
        self.score = score
        self.plugin = plugin

        self.actions = actions

    def __eq__(self, other):
        return (self.title == other.title)

    def get_actions(self):
        yield Open()


class Action(Item):
    def __init__(self, title, subtitle=''):
        Item.__init__(self, title, subtitle, False, '')

    def execute(self, target=None):
        raise NotImplementedError
