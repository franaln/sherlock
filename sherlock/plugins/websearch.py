# Web search

_engines = [
    ('gg',   'Google',    'google',      'https://www.google.com/search?q=%s'),
    ('yt',   'Youtube',   'web-youtube', 'https://www.youtube.com/results?search_query=%s'),
    ('gh',   'GitHub',    'github',      'https://github.com/search?utf8=✓&q=%s'),
    ('wiki', 'Wikipedia', 'wikipedia',   'https://en.wikipedia.org/w/index.php?search=%s'),
]

def match_trigger(query):
    for trigger, _, _, _ in _engines:
        if query.startswith('%s ' % trigger):
            return True

    return False

def get_items(query):
    for trigger, name, icon, url in _engines:
        if query.startswith(trigger+' '):
            search_expr = query.replace('%s ' % trigger, '')
            arg = url % search_expr
            yield {
                'text': 'Search «%s» with %s' % (search_expr, name),
                'subtext': arg,
                'arg': arg,
                'category': 'url',
                'icon': icon,
            }

def get_fallback_items(query):
    for _, name, icon, url in _engines:
        arg = url % query
        yield {
            'text': 'Search «%s» with %s' % (query, name),
            'subtext': arg,
            'arg': arg,
            'category': 'url',
            'icon': icon,
        }
