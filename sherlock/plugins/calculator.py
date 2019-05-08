import os
from shutil import which

from sherlock.utils import get_cmd_output, run_cmd

_use_calc  = (which('calc') is not None)
_use_units = (which('units') is not None)

def update_cache():
    if _use_units:
        run_cmd('units_cur %s/.units' % os.path.expanduser('~'))


def match_trigger(query):
    if query.startswith('='):
        return True

    if len(query) > 2 and any(i in query for i in '+-*/%^)('):
        return True


def get_items(query):

    extra_calc = query.startswith('=')

    expression = query.replace('=', '').replace(',', '.').strip()

    if extra_calc:

        if not expression:
            text = "Empty input"
            subtext = "Enter something to convert"

        else:

            result = ''

            if _use_calc:
                result = get_cmd_output(['calc', expression])

            if not result and _use_units:

                args = expression.split()

                try:
                    result = get_cmd_output(['units', '-t'] + args)
                except sp.CalledProcessError as e:
                    pass

            if result:
                text = '= %s' % result
                subtext = ''
            else:
                text = 'Input error'
                subtext = 'Check the syntax'


        yield {
            'text': text,
            'subtext': subtext,
            'category': 'text',
            'arg': text,
            'icon': 'accessories-calculator'
        }


    else:

        if _use_calc and expression:

            result = get_cmd_output(['calc', expression])

            if result:
                yield {
                    'text': '= %s' % result,
                    'subtext': '',
                    'arg': result,
                    'icon': 'accessories-calculator'
                }
