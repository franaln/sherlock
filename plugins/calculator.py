# Calculator plugin

import re, utils
from plugin import Plugin

math_re = re.compile('^\\(*(-?\\d+([.,]\\d+)?)([*/+-^]\\(*(-?\\d+([.,]\\d+)?)\\)*)+$')

class CalculatorPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Calculator', 'calc')
        self._items = []

    def get_actions(self):
        return None

    def get_matches(self, query):
        self.clear_matches()

        if math_re.search(query) is None:
            return None

        query = query.replace(" ", "").replace(",", ".")

        result = utils.check_output(['calc', query])

        self.add_item(title=result, subtitle=query, score=100)

        return self._items



# import re

# # input is a list of tokens (token is a number or operator)
# tokens = raw_input()

# # remove whitespace
# tokens = re.sub('\s+', '', tokens)

# # split by addition/subtraction operators
# tokens = re.split('(-|\+)', tokens)

# # takes in a string of numbers, *s, and /s. returns the result
# def solve_term(tokens):
#     tokens = re.split('(/|\*)', tokens)
#     ret = float(tokens[0])
#     for op, num in zip(tokens[1::2], tokens[2::2]):
#         num = float(num)
#         if op == '*':
#             ret *= num
#         else:
#             ret /= num
#     return ret

# # initialize final result to the first term's value
# result = solve_term(tokens[0])

# # calculate the final result by adding/subtracting terms
# for op, num in zip(tokens[1::2], tokens[2::2]):
#     result +=  solve_term(num) * (1 if op == '+' else -1)

# print result
