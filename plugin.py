# plugin base

class Plugin:

    def __init(self, name, trigger):
        self.name = name
        self.trigger = trigger

    def get_actions(self):
        raise Exception('Not implemented')

    def get_matches(self, query):
        raise Exception('Not implemented')
