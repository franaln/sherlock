# plugin manager

from plugins.applications import ApplicationsPlugin
from plugins.calculator import CalculatorPlugin
from plugins.screen import ScreenPlugin
from plugins.system import SystemPlugin

class PluginManager:

    def __init__(self):

        self.plugins = [
            ApplicationsPlugin(),
            CalculatorPlugin(),
            SystemPlugin(),
        ]

        self.keyword_plugins = [
            ScreenPlugin(),
        ]

        # self.plugins = {p.name: p for p in plugins}
        # self.keyword_plugins = {p.name: p for p in keyword_plugins}

    # def get_plugins(self):
    #     for plugin in self.plugins: #.values():
    #         yield plugin

    # def get_plugin(self, name):
    #     return self.plugins.get(name, None)
