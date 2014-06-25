# Applications plugin

# FIX: i want to eliminate th gtk dependecies.
from gi.repository import Gio

from item import Item
import utils

name = 'Applications'

def _get_apps():
    apps = []
    for app in Gio.app_info_get_all():
        item = Item(
            app.get_name(),
            app.get_executable(),
            'app',
            app.get_filename(),
        )
        apps.append(item)

    return apps

def _search_key(app):
    return '%s %s' % (app.title, app.subtitle)

def get_matches(query):

    if not query:
        return False

    all_apps = utils.get_cached_data('apps', _get_apps, max_age=600)

    matches = utils.filter(query, all_apps, key=_search_key)

    return matches
