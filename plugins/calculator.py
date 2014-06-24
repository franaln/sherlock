# Calculator plugin

import re
import utils
from item import Item

name    = 'Calculator'
keyword = 'calc'

def get_matches(query):

    if not any(i in query for i in '+-*/%^'):
        return False

    query = query.replace(' ', '').replace(',', '.')

    result = utils.check_output(['calc', query])

    if result:
        item = Item(title=result, subtitle='',
                    category='text')
        return [(item, 100), ]

    return False
