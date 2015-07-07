# Applications plugin

import os

from gi.repository import Gio # FIX: i want to eliminate th gtk dependecies.

from sherlock import cache
from sherlock.items import ItemApp


_cached_applications = None

def _get_apps():
    apps = []
    for app in Gio.app_info_get_all():
        item = ItemApp(
            app.get_name(),
            app.get_executable(),
            app.get_filename(),
            app.get_name(),
        )
        apps.append(item)
        item = ItemApp(
            app.get_name(),
            app.get_executable(),
            app.get_filename(),
            app.get_executable(),
        )
        apps.append(item)

    return apps


def get_matches(query):

    global _cached_applications

    if _cached_applications is None:
        _cached_applications = cache.get_cached_data('apps', _get_apps, max_age=600)

    return _cached_applications
