# sherlock config
import os

#------------
# Theme/Style
#------------

# Font
fontname = 'Cantarell' #Sans'

# Colours
bkg_color = (0.92, 0.92, 0.92)  # #ebebeb
bar_color = (0.8, 0.8, 0.8)     # #141414
sep_color = (0.8, 0.8, 0.8)     # #141414
sel_color = (0.26, 0.50, 0.93)  # #427fed
scroll_color = (0.2, 0.2, 0.2)

text_color    = (0.1, 0.1, 0.1) # #030303
subtext_color = (0.5, 0.5, 0.5)
seltext_color = (1.0, 1.0, 1.0)

#--------
# Plugins
#--------

# Base plugins
# (Search these plugins if no keyword given)
base_plugins = [
    'applications',
    'system',
    'files',
    'calculator',
]

# Keyword plugins
keyword_plugins = {
    'display': 'screens',
    'disks': 'disks',
    'test': 'disks',
}

# Fallback plugins
# (Use it when there are no other matches)
fallback_plugins = {
    'Search /home for query': 'calculator',
    'Search google for query': 'calculator',
}


#------------
# Directories
#------------
plugins_dir = os.path.expanduser('~/dev/sherlock/plugins/')
cache_dir = os.path.expanduser('~/.cache/sherlock/')
