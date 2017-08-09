from sherlock.items import Item

_engines = [
    ('gg', 'Google',  'https://www.google.com/search?q=%s'),
    ('yt', 'Youtube', 'https://www.youtube.com/results?search_query=%s'),
    ('gh', 'GitHub',  'https://github.com/search?utf8=✓&q=%s'),
    ('wiki', 'Wikipedia', 'https://en.wikipedia.org/w/index.php?search=%s'),
]

def match_trigger(query):
    for trigger, name, url in _engines:
        if query.startswith('%s ' % trigger):
            return True

def get_items(query):
    for trigger, name, url in _engines:
        if query.startswith(trigger+' '):
            search_expr = query.replace('%s ' % trigger, '')
            arg = url % search_expr
            yield Item(text='Search "%s" with %s' % (search_expr, name), subtext=arg,
                       arg=arg, category='url')

def get_fallback_items(query):
    for _, name, url in _engines:
        arg = url % query
        yield Item(text='Search "%s" with %s' % (query, name), subtext=arg, arg=arg,
                   category='url')
