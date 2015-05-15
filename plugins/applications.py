# Applications plugin

# FIX: i want to eliminate th gtk dependecies.
from gi.repository import Gio

import cache
from items import ItemApp


_cached_applications = None

def _get_apps():
    apps = []
    for app in Gio.app_info_get_all():
        item = ItemApp(
            app.get_name(),
            app.get_executable(),
            app.get_filename(),
        )
        apps.append(item)

    return apps


def get_matches(query):

    global _cached_applications

    if _cached_applications is None:
        _cached_applications = cache.get_cached_data('apps', _get_apps, max_age=600)

    return _cached_applications
