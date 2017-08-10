from sherlock.utils import get_cmd_output
from sherlock.items import Item

def match_trigger(query):
    if len(query) > 2 and  any([i in query for i in '+-*/%^)(']):
        return True

def get_items(query):

    expression = '(%s)' % query.replace(' ', '').replace(',', '.')

    result = get_cmd_output(['calc', expression])

    if result:
        yield Item('= %s' % result, '', arg=result)
