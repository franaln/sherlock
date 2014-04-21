# Calculator plugin

import re
import utils
from item import Item

name    = 'Calculator'
keyword = 'calc'


def get_matches(query):

    query = query.replace(' ', '').replace(',', '.')

    result = utils.check_output(['calc', query])

    matches = []

    if result:
        item = Item(title=result, subtitle='',
                    category='text')
        matches.append((item, 100))

    return matches
