# sherlock config

#-------------
# Theme/Style
#-------------
# Font
fontname = 'Cantarell' #Sans'

# Colours
background_color = (0.92, 0.92, 0.92) # #ebebeb
bar_color        = (0.92, 0.92, 0.92) # #cccccc
separator_color  = (0.80, 0.80, 0.80) # #cccccc
selection_color  = (0.30, 0.60, 0.93) # #427fed
text_color       = (0.10, 0.10, 0.10) # #030303
subtext_color    = (0.50, 0.50, 0.50)
seltext_color    = (1.00, 1.00, 1.00)

#--------------
# Basic search
#--------------
basic_search = [
    'applications',
    'system',
    'calculator',
    'files',
]

files_include = [
    '~/Dropbox',
    '~/Downloads',
    '~/cosas',
]

#---------
# Plugins
#---------
plugins = {
    'df': 'disks',
    'scr': 'screen',
    'temp': 'temperature',
}

# Fallback plugins
# (Use it when there are no other matches)
# fallback_plugins = {
#     #'Search /home for query': '',
#     #'Search google for query': 'calculator',
# }


#-------------
# Directories
#-------------
plugins_dir = '~/dev/sherlock/plugins/'
cache_dir   = '~/.cache/sherlock/'
