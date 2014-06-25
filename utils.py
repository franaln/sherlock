# utils

import os
import re
import string
import time
import subprocess

try:
    import cPickle as pickle
except:
    import pickle

import config

#-------------#
# Cache utils #
#-------------#

cachedir = config.cache_dir

def get_cachefile(filename):
    """
    Return full path to filename within cache dir.
    """
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)
    return os.path.join(cachedir, filename)

def get_cached_data(name, data_func=None, max_age=60):
    """ Retrieve data from cache or re-generate and re-cache data if
    stale/non-existant. If max_age is 0, return cached data no
    matter how old.
    """
    cache_path = get_cachefile('%s.cache' % name)
    age = get_cached_data_age(name)
    if (age < max_age or max_age == 0) and os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    if not data_func:
        return None
    data = data_func()
    cache_data(name, data)
    return data

def cache_data(name, data):
    """ Save data to cache under name
    name: name of datastore
    data: data to store
    """
    cache_path = get_cachefile('%s.cache' % name)
    with open(cache_path, 'wb') as f:
        pickle.dump(data, f)

def cached_data_fresh(name, max_age):
    """ Is data cached at name less than max_age old?
    name: name of datastore
    max_age: maximum age of data in seconds
    returns True if data is less than max_age old, else False
    """
    age = get_cached_data_age(name)
    if not age:
        return False
    return age < max_age

def get_cached_data_age(name):
    """ Return age of data cached at name in seconds or 0 if
    cache doesn't exist
    name: name of datastore
    returns age of datastore in seconds
    """
    cache_path = get_cachefile('%s.cache' % name)
    if not os.path.exists(cache_path):
        return 0
    return time.time() - os.stat(cache_path).st_mtime

def clear_cache():
    """ Delete all files in cache directory."""
    if os.path.exists(get_cachedir()):
        for filename in os.listdir(get_cachedir()):
            path = os.path.join(get_cachedir(), filename)
            os.unlink(path)


#--------------#
# Filter utils #
#--------------#

# Match filter flags
MATCH_STARTSWITH = 1
MATCH_CAPITALS = 2
MATCH_ATOM = 4
MATCH_INITIALS_STARTSWITH = 8
MATCH_INITIALS_CONTAIN = 16
MATCH_INITIALS = 24
MATCH_SUBSTRING = 32
MATCH_ALLCHARS = 64
MATCH_ALL = 127

# Anchor characters in a name
INITIALS = string.ascii_uppercase + string.digits

# Split on non-letters, numbers
split_on_delimiters = re.compile('[^a-zA-Z0-9]').split

def filter(query, items, key=lambda x: x, ascending=False,
           include_score=True, min_score=0, max_results=0,
           match_on=MATCH_ALL ^ MATCH_ALLCHARS):
    """ search filter. Returns list of items that match query.
    (Taken from Alfred workflow)

    * query: query to test items against
    * items: iterable of items to test (list or tuple)
    * key: function to get comparison key from items. Must return a
    unicode string. The default simply returns the item.
    * ascending: True to get worst matches first
    * min_score: Ignore results with a score lower than this if is non-zero
    * max_results
    * match_on: Filter option flags.

    Matching rules
    --------------
    By default, filter uses all of the following flags in this order
    1. MATCH_STARTSWITH: Item search key startswith query (case-insensitive).
    2. MATCH_CAPITALS: The list of capital letters in item search key starts with query (query may be lower-case). E.g., of would match OmniFocus, gc would match Google Chrome
    3. MATCH_ATOM: Search key is split into "atoms" on non-word characters (.,-,' etc.). Matches if query is one of these atoms (case-insensitive).
    4. MATCH_INITIALS_STARTSWITH: Initials are the first characters of the above-described "atoms" (case-insensitive).
    5. MATCH_INITIALS_CONTAIN: query is a substring of the above-described initials.
    6. MATCH_INITIALS: Combination of (4) and (5).
    7. MATCH_SUBSTRING: Match if query is a substring of item search key (case-insensitive).
    8. MATCH_ALLCHARS: Matches if all characters in query appear in item search key in the same order (case-insensitive).
    9. MATCH_ALL: Combination of all the above. The default.
    """

    results = {}
    query = query.lower()
    queryset = set(query)

    # Build pattern: include all characters
    pattern = []
    for c in query:
        pattern.append('.*?{0}'.format(re.escape(c)))
    pattern = ''.join(pattern)
    search = re.compile(pattern, re.IGNORECASE).search

    for i, item in enumerate(items):
        rule = None
        score = 0
        value = key(item)

        # pre-filter any items that do not contain all characters of 'query'
        # to save on running several more expensive tests
        if not queryset <= set(value.lower()):
            continue

        # item starts with query
        if (match_on & MATCH_STARTSWITH and
                value.lower().startswith(query)):
            score = 100.0 - (len(value) / len(query))

        if not score and match_on & MATCH_CAPITALS:
            # query matches capitalised letters in item,
            # e.g. of = OmniFocus
            initials = ''.join([c for c in value if c in INITIALS])
            if initials.lower().startswith(query):
                score = 100.0 - (len(initials) / len(query))

        if not score:
            if (match_on & MATCH_ATOM or
                    match_on & MATCH_INITIALS_CONTAIN or
                    match_on & MATCH_INITIALS_STARTSWITH):
                # split the item into "atoms", i.e. words separated by
                # spaces or other non-word characters
                atoms = [s.lower() for s in split_on_delimiters(value)]
                # print('atoms : %s  -->  %s' % (value, atoms))
                # initials of the atoms
                initials = ''.join([s[0] for s in atoms if s])

            if match_on & MATCH_ATOM:
                # is 'query' one of the atoms in item?
                # similar to substring, but scores more highly, as it's
                # a word within the item
                if query in atoms:
                    score = 100.0 - (len(value) / len(query))

        if not score:
            # 'query' matches start (or all) of the initials of the
            # atoms, e.g. 'himym' matches 'How I Met Your Mother'
            # *and* 'how i met your mother' (the capitals rule only
            # matches the former)
            if (match_on & MATCH_INITIALS_STARTSWITH and
                    initials.startswith(query)):
                score = 100.0 - (len(initials) / len(query))

            # 'query' is a substring of initials, e.g. 'doh' matches
            # 'The Dukes of Hazzard'
            elif (match_on & MATCH_INITIALS_CONTAIN and
                    query in initials):
                score = 95.0 - (len(initials) / len(query))

        if not score:
            # 'query' is a substring of item
            if match_on & MATCH_SUBSTRING and query in value.lower():
                    score = 90.0 - (len(value) / len(query))

        if not score:
            # finally, assign a score based on how close together the
            # characters in query are in item.
            if match_on & MATCH_ALLCHARS:
                match = search(value)
                if match:
                    score = 100.0 / ((1 + match.start()) *
                                     (match.end() - match.start() + 1))
                    rule = MATCH_ALLCHARS

        if min_score and score < min_score:
            continue

        if score > 0:
            # use "reversed" score (i.e. highest becomes lowest) and
            # value as sort key. This means items with the same score
            # will be sorted in alphabetical not reverse alphabetical order

            results[(100.0 / score, value.lower(), i)] = (item, round(score, 2))

    # sort on keys, then discard the keys
    keys = sorted(results.keys(), reverse=ascending)
    results = [results.get(k) for k in keys]

    if max_results and len(results) > max_results:
        results = results[:max_results]

    # return list of (item, score)
    return results


#-------------#
# Other utils #
#-------------#

def get_selection():
    """ get clipboard content """
    return subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]

def check_output(cmd_list):
    try:
        output = subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf8').strip()

def is_running(name):
    processes = str(subprocess.check_output(('ps', '-u', os.environ['USER'], '-o', 'comm',
                                             '--no-headers')), encoding='utf8').rstrip('\n').split('\n')

    if name in processes:
        return True

    return False

# def xselSetClipboard(text):
#     p = Popen(['xsel', '-i'], stdin=PIPE)
#     try:
#         # works on Python 3 (bytes() requires an encoding)
#         p.communicate(input=bytes(text, 'utf-8'))
#     except TypeError:
#         # works on Python 2 (bytes() only takes one argument)
#         p.communicate(input=bytes(text))


# def xselGetClipboard():
#     p = Popen(['xsel', '-o'], stdin=PIPE)
#     stdout, stderr = p.communicate()
#     return bytes.decode(stdout)
