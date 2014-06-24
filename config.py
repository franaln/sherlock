# sherlock config

#------------
# Theme/Style
#------------

# Font
fontname = 'Cantarell'

# Colours
bkg_color = (0.92, 0.92, 0.92)  # #ebebeb
bar_color = (0.8, 0.8, 0.8)     # #141414
sep_color = (0.8, 0.8, 0.8)     # #141414
sel_color = (0.26, 0.50, 0.93)  # #427fed

text_color    = (0.1, 0.1, 0.1) # #030303
subtext_color = (0.5, 0.5, 0.5)
seltext_color = (1, 1, 1)

app_color = (1.0, 0.0, 0.0)
uri_color = (0.0, 1.0, 0.0)
cmd_color = (0.0, 0.0, 1.0)
txt_color = (0.4, 0.4, 0.4)

# Size
width = 480
height = 60
item_height = 48
lines = 5



#--------
# Plugins
#--------
# Base plugins (Search these plugins if no keyword given)
base_plugins = [
    'applications',
    'system',
    'calculator',
]

# Keyword plugins (Only search in these plugins when a keyword is provided)
keyword_plugins = {
    'scr': 'screens',
}

# Fallback plugins (Use it when there are no other matches)
fallback_plugins = {
    'Search /home for query ...': 'calculator',
    'Search google for query ...': 'calculator',
}


#------------
# Directories
#------------
cache_dir = '/home/fran/dev/sherlock/data'
