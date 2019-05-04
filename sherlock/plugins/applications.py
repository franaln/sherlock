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

        exe = os.path.basename(app.get_executable())

        item = {
            'text': app.get_name(),
            'subtext': app.get_executable(),
            'category': 'app',
            'keys': (app.get_name(), exe),
            'arg': app.get_filename(),
            'icon': app.get_icon().to_string() if app.get_icon() is not None else '',
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


def get_items():

    _cached_applications = cache.get_cached_data('applications')

    for app in _cached_applications:
        yield app
