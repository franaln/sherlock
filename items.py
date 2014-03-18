# item: base class for menu item

class Item:

    def __init__(self, title, subtitle='', icon=None):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

class Match(Item):
    def __init__(self, title, subtitle, icon, score): #, last_time, icon, score):
        Item.__init__(self, title, subtitle, icon)
        self.score = score

    def __str__(self): # for debug
        return '%s(%s) [%i]' % (self.title, self.subtitle, self.score)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.title == other.title)

class Action(Item):
    def __init__(self, title, subtitle):
        Item.__init__(self, title, subtitle)

    def execute(self):
        raise Exception('Not implemented')
