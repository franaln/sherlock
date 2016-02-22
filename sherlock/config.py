# sherlock config

#-------------
# Theme/Style
#-------------
# Font
fontname = 'Cantarell' #Sans'

# Colours
background_color = (0.93, 0.93, 0.93) # #ebebeb
bar_color        = (0.93, 0.93, 0.93) # #cccccc
separator_color  = (0.80, 0.80, 0.80) # #cccccc
selection_color  = (0.31, 0.61, 0.91) # #427fed
text_color       = (0.27, 0.27, 0.27) # #454545
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
 #   'path',
]

files_include = [
    '~/Dropbox',
    '~/Downloads',
    '~/cosas',
    # '~/tmp',
    '~/fotos',
]

#---------
# Plugins
#---------
plugins = {
    'df': 'disks',
    'temp': 'temperature',
    'top': 'top',
}

# always check when starts
automatic_plugins = [
    'screen',
    'mounter',
]

# Fallback plugins
# (Use it when there are no other matches)
fallback_plugins = {
    #'Search /home for query': '',
    #'Search google for query': 'calculator',
}


#-------------
# Directories
#-------------
plugins_dir = '~/dev/sherlock/sherlock/plugins/'
cache_dir   = '~/.cache/sherlock/'
