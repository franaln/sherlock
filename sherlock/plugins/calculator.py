from sherlock.utils import get_cmd_output
from sherlock.items import Item

def match_trigger(query):
    if any([i in query for i in '+-*/%^)(']):
        return True

def get_items(query):
    expression = query.replace(' ', '').replace(',', '.')

    result = get_cmd_output(['calc', expression])

    yield Item('= %s' % result, '', arg=result)
