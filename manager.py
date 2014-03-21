# plugin manager

from plugins.applications import ApplicationsPlugin
from plugins.calculator import CalculatorPlugin
from plugins.screen import ScreenPlugin
from plugins.system import SystemPlugin

class PluginManager:

    def __init__(self):

        plugins = [
            ApplicationsPlugin(),
            CalculatorPlugin(),
            ScreenPlugin(),
            SystemPlugin(),
        ]

        self.plugins = {p.name: p for p in plugins}


    def get_plugins(self):
        for plugin in self.plugins.values():
            yield plugin

    def get_plugin(self, name):
        return self.plugins.get(name, None)
