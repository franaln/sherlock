from shutil import which

from sherlock.utils import get_cmd_output

_use_calc  = (which('calc') is not None)
_use_units = (which('units') is not None)


def match_trigger(query):
    if len(query) > 2 and  any([i in query for i in '+-*/%^)(']):
        return True


def get_items(query):

    expression = '(%s)' % query.replace(' ', '').replace(',', '.')

    result = get_cmd_output(['calc', expression])

    if result:
        yield {
            'text': '= %s' % result,
            'subtext': '',
            'arg': result,
            'icon': 'accessories-calculator'
        }
