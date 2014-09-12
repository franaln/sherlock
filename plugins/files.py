# Files plugin

import os
import utils
from item import Item


def update_db():
    pass


def get_matches(query):

    if not query:
        return False

    matches = []

    locate_output = utils.get_cmd_output(['locate', '-ei', '-l', '100', query])

    for f in locate_output.split('\n'):
        if '/.' in f:
            continue

        item = Item(
            os.path.basename(f),
            f,
            'uri',
        )
        matches.append(item)

    return matches
