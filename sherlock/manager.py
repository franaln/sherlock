import os
import sys
import logging
import importlib

from sherlock import cache
from sherlock import similarity

actions_dict = {
    'app': (
        ('Open',             'open_app'),
        ('Open in terminal', 'open_app_terminal'),
    ),

    'file': (
        ('Open',                 'open_file'),
        ('Open dir',             'open_dir'),
        ('Open dir in terminal', 'open_dir_terminal'),
        ('Explore',              'explore'),
    ),

    'dir': (
        ('Open',             'open_dir'),
        ('Open in terminal', 'open_dir_terminal'),
        ('Explore',          'explore'),
    ),

    'url': (
        ('Open', 'open_url'),
        ('Copy', 'copy_to_clipboard'),
    ),

    'cmd': (
        ('Run',             'run_cmd'),
        ('Copy to console', 'copy_to_console')
    ),

    'text': (
        ('Copy', 'copy_to_clipboard'),
    ),
}


class Manager:

    def __init__(self, config):

        self.config = config

        self.logger = logging.getLogger(__name__)

        # plugins
        self.plugins = dict()

        self.normal_plugins   = []
        self.trigger_plugins  = []
        self.fallback_plugins = []
        self.cache_plugins    = []
        self.auto_plugins     = []

        self.load_plugins()

    def import_plugin(self, name):
        try:
            plugin = importlib.import_module(name)
            self.logger.info('plugin loaded: %s' % name)
        except ImportError:
            self.logger.error('error loading plugin: %s' % name)
            return None

        return plugin

    def load_plugins(self):

        plugins_dir = os.path.dirname(__file__) + '/plugins'
        sys.path.append(plugins_dir)

        for name in self.config.plugins:
            plugin = self.import_plugin(name)

            if plugin is not None:
                self.plugins[name] = plugin

                if hasattr(plugin, 'match_trigger'):
                    self.trigger_plugins.append(name)
                else:
                    self.normal_plugins.append(name)

                if hasattr(plugin, 'get_fallback_items'):
                    self.fallback_plugins.append(name)

                if hasattr(plugin, 'update_cache'):
                    self.cache_plugins.append(name)

                if hasattr(plugin, 'get_auto_items'):
                    self.auto_plugins.append(name)


    def update_cache(self):
        for name in self.cache_plugins:
            self.logger.info('updating cache: %s' % name)
            self.plugins[name].update_cache()
            cache.load_cachedict(name)

        # self.logger.info('updating trie data')
        # similarity.update_trie_data(self.plugins)

        self.logger.info('updating caches done.')

        return True

    def load_cache(self):
        for name in self.cache_plugins:
            cache.load_cachedict(name)

    def clear_cache(self):
        cache.clear_cachedict()

    def get_fallback_items(self, query):
        items = []
        for name in self.fallback_plugins:
            if name in self.plugins:
                items.extend(self.plugins[name].get_fallback_items(query))
            elif name in self.trigger_plugins:
                items.extend(self.trigger_plugins[name].get_fallback_items(query))

        # # shell command
        # it = ItemCmd("run '%s' in a shell" % query, query)
        # items.append(it)

        return items

    # --------
    # Actions
    # --------
    def get_actions(self, item):
        """ return posible actions for the item """
        if 'actions' in item:
            return item['actions']

        return actions_dict.get(item['category'], ())

    def get_action(self, name):
        pass


    # ---------
    # Iterators
    # ---------
    def loop_normal_plugins(self):
        for name in self.normal_plugins:
            yield self.plugins[name]

    def loop_trigger_plugins(self):
        for name in self.trigger_plugins:
            yield self.plugins[name]

    def loop_auto_plugins(self):
        for name in self.auto_plugins:
            yield self.plugins[name]
