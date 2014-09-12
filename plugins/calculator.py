# Calculator plugin

import utils
from item import Item

def get_matches(query):

    if not any(i in query for i in '+-*/%^)('):
        return False

    query = query.replace(' ', '').replace(',', '.')

    result = utils.get_cmd_output(['calc', query])

    if result:
        item = Item(title=result, subtitle='',
                    category='text', score=100)
        return [item, ]

    return False
