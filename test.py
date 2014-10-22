# test

from main import Sherlock

test_queries = [
    'ini',  # --> no matches
    'nau',  # --> (apps) nautilus
    'sle',  # --> (system) sleep
    '2+2',  # --> (calc) 4
    'Susy', # --> (files) ~/Susy
]

s = Sherlock()

for query in test_queries:
    print('---\nQuery: {}'.format(query))

    s.on_query_changed(None, query)

    if s.items:
        print('Matches:')
        print(', '.join(['%s (%s)' % (i.title, i.score) for i in s.items[:10]]))
    else:
        print('No matches!')
