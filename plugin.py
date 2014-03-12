# plugin base

class Plugin:

    def __init(self, name, cmd):
        self.name = name
        self.cmd = cmd
        #self._actions = []
        # engine = SearchEngine()

    def get_actions(self):
        raise Exception('Not implemented')

    def get_matches(self, query):
        raise Exception('Not implemented')
