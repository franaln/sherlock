## Font
fontname = 'Sans'

## Colours
bar_bkg_color  = (0.8, 0.8, 0.8) # #141414
bar_text_color = (0.1, 0.1, 0.1)
bar_cur_color  = (0.3, 0.3, 0.3)

menu_bkg_color   = (0.92, 0.92, 0.92)    # #ebebeb
menu_sel_color   = (0.259, 0.498, 0.929) # #427fed
menu_text_color  = (0.1, 0.1, 0.1)       # #030303
menu_sep_color   = (0.8, 0.8, 0.8)
panel_bkg_color  = (0.8, 0.8, 0.8)

## Size
width = 480
height = 60
offset = 6
item_height = 48 # = height - 2 * offset
lines = 5


# Base plugins
# - Search these plugins if no keyword given
base_plugins = [
    'applications',
    'system',
    'calculator',
]

# Extra plugins
# - Only search in these plugins when a keyword is provided
keyword_plugins = [
#    'screens',
]

# Fallback plugins
# - Use it when there are no other matches
fallback_plugins = [

]
