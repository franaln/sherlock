# Applications plugin
# Open applications

from plugin import Plugin

from gi.repository import Gio

class ApplicationsPlugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'Applications')
        self._matches = []

    def get_apps(self):
        apps = []
        for app in Gio.app_info_get_all():
            m = {
                'text': app.get_name(),
                'subtext': app.get_executable(),
                'type': 'app',
                'arg': app.get_filename(),
                'uid': None,
                'score': 0
            }
            apps.append(m)

        return apps

    def search_key(self, app):
        return '%s %s' % (app['subtext'], app['text'])

    def get_matches(self, query):
        self.clear_matches()

        if not query:
            return self._matches()

        apps = self.cached_data('apps', self.get_apps, max_age=600)
        apps = self.filter(query, apps, key=self.search_key, include_score=True)

        for m in apps:
            m[0]['score'] = m[1]

            self.add_match_dict(m[0])

        return self._matches
