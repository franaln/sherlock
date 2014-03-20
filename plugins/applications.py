# Applications plugin
# Open applications

from plugin import Plugin
from actions import Run

from gi.repository import Gio


class ApplicationsPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Applications', 'app')
        self._items = []
        self._actions = [Run(),]


    def get_actions(self):
        pass

    def get_default_action(self):
        return self._actions[0]

    def get_apps(self):
        apps = []
        for app in Gio.app_info_get_all():

            a = (app.get_name(),
                 app.get_description(),
                 app.get_executable(),
                 app.get_filename()
            )
            apps.append(a)

        return apps

    def search_key(self, app):
        return ' %s %s' % (app[0], app[2])

    def get_matches(self, query):

        self.clear_matches()

        matches = self.cached_data('apps', self.get_apps, max_age=3600)

        if query:
            matches = self.filter(query, matches, key=self.search_key, include_score=True)

        for m in matches:
            title = m[0][0]
            subtitle = '%s (%s)' % (m[0][1], m[0][2]) if m[0][1] is not None else ''
            filename = m[0][3]
            self.add_item(title=title, subtitle=subtitle, arg=filename, score=m[1], plugin_name='Applications')

        return self._items
