# Calculator plugin

import re, utils
from plugin import Plugin

class CalculatorPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Calculator', 'calc')
        self._matches = []

    def get_matches(self, query):
        self.clear_matches()

        query = query.replace(' ', '').replace(',', '.')

        result = utils.check_output(['calc', query])

        if result:
            self.add_match(text=result, subtext='', score=100)

        return self._matches
