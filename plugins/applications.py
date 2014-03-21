# Applications plugin
# Open applications

from objects import Match
from plugin import Plugin
from actions import Run, RunTerminal

from gi.repository import Gio


class ApplicationsPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Applications', 'app')
        self._matches = []
        self._actions = [
            Run(),
            RunTerminal(),
        ]

    def get_apps(self):
        apps = []
        for app in Gio.app_info_get_all():
            a = {
                'name': app.get_name(),
                'desc': app.get_description(),
                'exec': app.get_executable(),
                'fname': app.get_filename()
            }
            apps.append(a)

        return apps

    def search_key(self, app):
        return ' %s %s' % (app['name'], app['exec'])

    def get_matches(self, query):

        self.clear_matches()

        apps = self.cached_data('apps', self.get_apps, max_age=600)

        if query:
            apps = self.filter(query, apps, key=self.search_key, include_score=True)

        for m in apps:
            title = m[0]['name']
            subtitle = '%s (%s)' % (m[0]['desc'], m[0]['exec']) if m[0]['desc'] is not None else ''
            filename = m[0]['fname']

            self.add_match(title=title, subtitle=subtitle,
                           arg=filename, score=m[1])

        return self._matches
