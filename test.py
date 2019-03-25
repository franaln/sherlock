import time

from sherlock import files, applications, bookmarks
from sherlock.search import filter_items


# Update cache
#@profile
def update_cache():
    print('------------------------')
    print('updating cache')

    start_time = time.time()

    applications.update_cache()
    files.update_cache()
    bookmarks.update_cache()

    return (time.time() - start_time)


# Search some queries
#@profile
def search(query):

    start_time = time.time()

    print('------------------------')
    print('results for "%s":' % query)

    matches = []
    matches.extend(filter_items(applications.get_items(), query, min_score=80, max_results=10))
    matches.extend(filter_items(files.get_items(), query, min_score=80, max_results=10))
    matches.extend(filter_items(bookmarks.get_items(), query, min_score=80, max_results=10))

    matches = sorted(matches, key=lambda x: x.score, reverse=True)

    for m in matches:
        print(m)

    return (time.time() - start_time)


t0 = update_cache()
t1 = search('arch')
t2 = search('naut')
t3 = search('moriond')
t4 = search('pavu')


# Result
print('------------------------')
print('t0 = %.4f seconds' % t0)
print('t1 = %.4f seconds' % t1)
print('t2 = %.4f seconds' % t2)
print('t3 = %.4f seconds' % t3)
print('t4 = %.4f seconds' % t4)
print('Total = %.4f seconds' % (t0+t1+t2+t3+t4))
print('------------------------')
