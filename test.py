import sys

from sherlock.search import *
from sherlock.plugins import files, applications, calculator

query = sys.argv[1]

matches = []
matches.extend(get_matches(applications, query, min_score=80, max_results=10))
matches.extend(get_matches(files, query, min_score=80, max_results=10))
matches.extend(get_matches(calculator, query, min_score=80, max_results=10))

matches = sorted(matches, key=lambda x: x.score, reverse=True)

for m in matches:
    print(m)
