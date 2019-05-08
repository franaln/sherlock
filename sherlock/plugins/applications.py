# Applications plugin

import os
import glob
from gi.repository import Gio

from sherlock import cache

def update_cache():

    apps = []
    exes = []
    # from desktop files
    for app in Gio.app_info_get_all():

        name = app.get_name()
        exe = app.get_executable()
        exe_name = os.path.basename(exe)
        icon = app.get_icon()

        if name.lower() == exe_name.lower():
            keys = (name,)
        else:
            keys = (name, exe_name)

        item = {
            'text': name,
            'subtext': exe,
            'category': 'app',
            'keys': keys,
            'arg': app.get_filename(),
            'icon': icon.to_string() if icon is not None else '',
        }

        apps.append(item)
        exes.append(exe)

    # # from path
    # for path in os.getenv('PATH').split(':'):

    #     output = glob.glob(path+'/*')

    #     for exe in output:

    #         name = os.path.basename(exe)

    #         if name not in exes:
    #             item = {
    #                 'text': name,
    #                 'subtext': exe,
    #                 'category': 'app',
    #                 'keys': (name,),
    #                 'arg': exe,
    #                 'icon': '',
    #             }

    #             apps.append(item)

    cache.cache_data('applications', apps)

    return


def get_items(query):

    _cached_applications = cache.get_cached_data('applications')

    for app in _cached_applications:
        yield app
