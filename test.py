# test

from main import Sherlock

test_queries = [
    'ini',  # --> no matches
    'nau',  # --> (apps) nautilus
    'sle',  # --> (system) sleep
    '2+2',  # --> (calc) 4
]

s = Sherlock()


for query in test_queries:
    print('---\nQuery: {}'.format(query))

    s.do_search(None, query)

    if s.items:
        print('Matches:')
        print(', '.join([i.title for i in s.items]))
    else:
        print('No matches!')
