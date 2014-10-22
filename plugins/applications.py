# Applications plugin

# FIX: i want to eliminate th gtk dependecies.
from gi.repository import Gio

from items import Item
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


applications = utils.get_cached_data('apps', _get_apps, max_age=600)

def get_matches(query):

    return applications
