# sherlock config

#-------------
# Theme/Style
#-------------
# Font
fontname = 'Source Sans Pro'

# Colours
background_color = (0.93, 0.93, 0.93) # #ebebeb
bar_color        = (0.93, 0.93, 0.93) # #cccccc
separator_color  = (0.80, 0.80, 0.80) # #323232
selection_color  = (0.17, 0.25, 0.92) # #427fed
text_color       = (0.27, 0.27, 0.27) # #454545
subtext_color    = (0.50, 0.50, 0.50)
seltext_color    = (1.00, 1.00, 1.00)

# background_color = (0.07, 0.07, 0.07) # #ebebeb
# bar_color        = (0.07, 0.07, 0.07) # #cccccc
# separator_color  = (0.80, 0.80, 0.80) # #323232
# selection_color  = (0.17, 0.25, 0.92) # #427fed
# text_color       = (1.00, 1.00, 1.00) # #454545
# subtext_color    = (0.50, 0.50, 0.50)
# seltext_color    = (0.80, 0.80, 0.80)

#--------------
# Basic search
#--------------
basic_plugins = [
    'calculator',
    'applications',
    'system',
    'files',
    'bashhistory',
    'chromium',
    'websearch',

    'currency',
    'rottenmovies',
]

files_include = [
    '~/Dropbox',
    '~/Downloads',
    '~/cosas',
    '~/ebooks',
    '~/fotos',
    '~/cernbox',
    '~/tmp',
    '~/Music',
    '~/Pictures',

]

files_include_extensions = ['.pdf', '.tex', '.txt', '.md', '.jpg', '.png',]

# #---------
# # Plugins
# #---------
# plugins = {
#     'df':   'disks',
#     'temp': 'temperature',
#     'top':  'top',
#     'time': 'currenttime',
#     'td': 'todo',
# }

# always check when starts
automatic_plugins = [
    # 'screen',
    # 'mounter',
]

cache_dir  = '/home/fran/.cache/sherlock/'
