import os
import sys
import logging
import importlib

from sherlock import cache

actions_dict = {
    'app': (
        ('Run', 'run_app'),
        ('Run in terminal', 'run_app_terminal'),
    ),

    'file': (
        ('Open', 'open_file'),
        ('Open dir', 'open_dir'),
        ('Open dir in terminal', 'open_dir_terminal'),
        ('Explore', 'explore'),
    ),

    'dir': (
        ('Open', 'open_dir'),
        ('Open in terminal', 'open_dir_terminal'),
        ('Explore', 'explore'),
    ),

    'url': (
        ('Open', 'open_url'),
        ('Copy', 'copy_to_clipboard'),
    ),

    'cmd': (
        ('Run', 'run_cmd'),
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
        self.trigger_plugins = dict()

        self.fallback_plugins = []
        self.cache_plugins = []

        self.load_plugins()

    def import_plugin(self, name):
        try:
            plugin = importlib.import_module(name)
            self.logger.info('plugin %s loaded.' % name)
        except ImportError:
            self.logger.error('error loading plugin %s.' % name)
            return None

        return plugin

    def load_plugins(self):

        plugins_dir = os.path.dirname(__file__) + '/plugins'
        sys.path.append(plugins_dir)

        for name in self.config.basic_plugins:
            plugin = self.import_plugin(name)

            if plugin is not None:
                if hasattr(plugin, 'match_trigger'):
                    self.trigger_plugins[name] = plugin
                else:
                    self.plugins[name] = plugin

                if hasattr(plugin, 'get_fallback_items'):
                    self.fallback_plugins.append(name)

                if hasattr(plugin, 'update_cache'):
                    self.cache_plugins.append(name)

    # def check_automatic_plugins(self):
    #     for name, plugin in self.automatic_plugins.items():
    #         self.logger.info('checking automatic plugin %s' % name)
    #         matches = plugin.get_matches()
    #         if matches:
    #             self.items.extend(matches)
    #             self.emit('menu-update')

    def update_cache(self):
        for name in self.cache_plugins:
            self.plugins[name].update_cache()
            self.logger.info('updating %s cache' % name)
            cache.load_cachedict(name)

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
        return actions_dict.get(item.category, ())

    def get_action(self, name):
        pass
