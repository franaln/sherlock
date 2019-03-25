# Applications plugin

import os
import glob
from gi.repository import Gio

from sherlock import cache
from sherlock.items import Item

def update_cache():

    apps = []
    exes = []
    # from desktop files
    for app in Gio.app_info_get_all():

        exe = os.path.basename(app.get_executable())

        item = Item(
            text=app.get_name(),
            subtext=app.get_executable(),
            category='app',
            keys=(app.get_name(), exe),
            arg=app.get_filename()
        )
        apps.append(item)
        exes.append(exe)

    # from path
    for path in os.getenv('PATH').split(':'):

        output = glob.glob(path+'/*')

        for exe in output:

            name = os.path.basename(exe)

            if name not in exes:
                item = Item(
                    text=name,
                    subtext=exe,
                    category='app',
                    keys=name,
                    arg=exe,
                )

                apps.append(item)

    cache.cache_data('applications', apps)

    return


def get_items():

    _cached_applications = cache.get_cached_data('applications')

    for app in _cached_applications:
        yield app
