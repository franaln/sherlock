# Calculator plugin

import re, utils
from plugin import Plugin

class CalculatorPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Calculator', 'calc')
        self._matches = []

    def get_matches(self, query):
        self.clear_matches()

        # return no matches if no operators
        oplist = ['+', '-', '/', '*']
        if not [e for e in oplist if e in query]:
            return self._matches

        query = query.replace(' ', '').replace(',', '.')

        result = utils.check_output(['calc', query])

        if result:
            self.add_match(title=result, subtitle='', score=100)

        return self._matches
