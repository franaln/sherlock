# Calculator plugin

from sherlock import utils
from sherlock.items import ItemText

def get_matches(query):

    if not any(i in query for i in '+-*/%^)('):
        return []

    query = query.replace(' ', '').replace(',', '.')

    result = utils.get_cmd_output(['calc', query])

    if result:
        item = ItemText(result, no_filter=True)
        yield item
