import sys

from sherlock.search import *
from sherlock.plugins import files, applications, calculator
from sherlock.attic2 import Attic
from sherlock.config import cache_dir

cache_dir = os.path.expanduser(cache_dir)
attic_path = os.path.join(cache_dir, 'attic2')
attic = Attic(attic_path)

if len(sys.argv) < 2:
    print('usage: test.py query1 [query2]')
    sys.exit()


# 1
query = sys.argv[1]
print('results for "%s":' % query)

matches = []
matches.extend(get_matches(applications, query, min_score=80, max_results=10))
matches.extend(get_matches(files, query, min_score=80, max_results=10))
matches.extend(get_matches(calculator, query, min_score=80, max_results=10))

for m in matches:
    bonus = attic.get_item_bonus(m)
    m.score += bonus

matches = sorted(matches, key=lambda x: x.score, reverse=True)

for m in matches:
    print(m)


# 2
if len(sys.argv) > 2:

    query = sys.argv[2]
    print('results for "%s":' % query)

    matches2 = []
    matches2.extend(get_matches(applications, query, min_score=80, max_results=10))
    matches2.extend(get_matches(files, query, min_score=80, max_results=10))
    matches2.extend(get_matches(calculator, query, min_score=80, max_results=10))

    for m in matches2:
        bonus = attic.get_item_bonus(m)
        m.score += bonus

    matches2 = sorted(matches2, key=lambda x: x.score, reverse=True)

    for m in matches2:
        print(m)
