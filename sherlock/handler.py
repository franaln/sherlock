import os
import sys
import logging
import importlib

class Handler:

    def __init__(self, config):

        self.config = config

        self.logger = logging.getLogger(__name__)

        # plugins
        self.plugins = dict()
        self.load_plugins()

    def import_plugin(self, name):
        try:
            plugin = importlib.import_module(name)
            self.logger.info('pluging %s loaded.' % name)
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
                self.plugins[name] = plugin

    # def check_automatic_plugins(self):
    #     for name, plugin in self.automatic_plugins.items():
    #         self.logger.info('checking automatic plugin %s' % name)
    #         matches = plugin.get_matches()
    #         if matches:
    #             self.items.extend(matches)
    #             self.emit('menu-update')

    def update_cache(self):
        for name, plugin in self.plugins.items():
            try:
                plugin.update_cache()
                self.logger.info('updating %s cache' % name)
            except AttributeError:
                self.logger.debug('updateing cache: skipping plugin %s (doesn\'t have a update cache method)' % name)
        return True
