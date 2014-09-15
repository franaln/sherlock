# Applications plugin

# FIX: i want to eliminate th gtk dependecies.
from gi.repository import Gio

from item import Item
import utils

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
    if app.subtitle and app.subtitle is not None:
        return app.subtitle
    return app.title

def get_matches(query):

    if not query:
        return False

    return utils.get_cached_data('apps', _get_apps, max_age=600)
