# plugin manager

from plugins.applications import ApplicationsPlugin
from plugins.calculator import CalculatorPlugin
from plugins.screen import ScreenPlugin
from plugins.system import SystemPlugin


# Base plugins
# Always search in these plugins
base_plugins = [
    ApplicationsPlugin(),
    CalculatorPlugin(),
    SystemPlugin(),
]

# Extra plugins
# Only search in these plugins when a keyword is provided
extra_plugins = [
    ScreenPlugin(),
]
