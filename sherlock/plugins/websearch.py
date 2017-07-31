from sherlock.items import ItemUrl

_engines = [
    ('gg', 'Google',  'https://www.google.com/search?q=%s'),
    ('yt', 'Youtube', 'https://www.youtube.com/results?search_query=%s'),
    ('gh', 'GitHub',  'https://github.com/search?utf8=✓&q=%s'),
    ('wiki', 'Wikipedia', 'https://en.wikipedia.org/w/index.php?search=%s'),
]

need_trigger = True

def match_trigger(query):
    for trigger, name, url in _engines:
        if query.startswith(trigger+' '):
            return True

def get_items(query):
    for trigger, name, url in _engines:
        if query.startswith(trigger+' '):
            search_expr = query.replace(trigger+' ', '')
            arg = url % search_expr
            yield ItemUrl('Search "%s" with %s' % (search_expr, name), arg)

def get_fallback_items(query):
    _, name, url = _engines[0]
    arg = url % search_expr
    yield ItemUrl('Search "%s" with %s' % (query, name), arg)