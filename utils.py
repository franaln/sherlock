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

cachedir = os.path.expanduser(config.cache_dir)

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

# Anchor characters in a name
INITIALS = string.ascii_uppercase + string.digits

# Split on non-letters, numbers
split_on_delimiters = re.compile('[^a-zA-Z0-9]').split

def distance(str1, str2):
    """ return the Levenshtein distance
    between two strings """

    d = dict()
    for i in range(len(str1)+1):
        d[i] = dict()
        d[i][0] = i

    for i in range(len(str2)+1):
        d[0][i] = i

    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1,
                          d[i-1][j-1]+(not str1[i-1] == str2[j-1]))

    return d[len(str1)][len(str2)]


def filter(query, items, min_score=0, max_results=0):
    """ search filter. Returns list of items that match query.
    * query: query to test items against
    * items: iterable of items to test (list or tuple)
    * key: function to get comparison key from items. Must return a
    unicode string. The default simply returns the item.
    """
    results = {}
    query = query.lower()
    querylen = len(query)
    queryset = set(query)

    # Build pattern: include all characters
    #pattern = []
    #for c in query:
    #    pattern.append('.*?{0}'.format(re.escape(c)))
    #pattern = ''.join(pattern)
    #search = re.compile(pattern, re.IGNORECASE).search

    # Loop over items
    for i, item in enumerate(items):
        score = 0
        value = item.key
        valuelen = len(value)

        if item.no_filter:
            score = 100.0
        else:
            # pre-filter any items that do not contain all characters of 'query'
            # to save on running several more expensive tests
            if not queryset <= set(value.lower()):
                continue

        # item starts with query (case-insensitive)
        if value.lower().startswith(query):
            score = 101.0 - (valuelen / querylen)

        if not score:
            # query matches capitalised letters in item,
            # e.g. of = OmniFocus
            initials = ''.join([c for c in value if c in INITIALS])
            if initials.lower().startswith(query):
                score = 98.0 - (len(initials) / querylen)

        if not score:
            # split the item into "atoms", i.e. words separated by
            # spaces or other non-word characters
            atoms = [s.lower() for s in split_on_delimiters(value)]
            # print('atoms : %s  -->  %s' % (value, atoms))
            # initials of the atoms
            initials = ''.join([s[0] for s in atoms if s])

            # is 'query' one of the atoms in item?
            # similar to substring, but scores more highly, as it's
            # a word within the item
            if query in atoms:
                score = 97.0 - (valuelen / querylen)

        if not score:
            # 'query' matches start (or all) of the initials of the
            # atoms, e.g. 'himym' matches 'How I Met Your Mother'
            # *and* 'how i met your mother' (the capitals rule only
            # matches the former)
            if initials.startswith(query):
                score = 96.0 - (len(initials) / querylen)

            # 'query' is a substring of initials, e.g. 'doh' matches
            # 'The Dukes of Hazzard'
            elif query in initials:
                score = 95.0 - (len(initials) / querylen)

        if not score:
            # 'query' is a substring of item
            if query in value.lower():
                score = 94.0 - (valuelen / querylen)

        # if not score:
        #     # finally, assign a score based on how close together the
        #     # characters in query are in item.
        #     match = search(value)
        #     if match:
        #         score = 85.0 / ((1 + match.start()) *
        #                          (match.end() - match.start() + 1))

        if min_score and score < min_score:
            continue

        if score > 0:
            # use "reversed" score (i.e. highest becomes lowest) and
            # value as sort key. This means items with the same score
            # will be sorted in alphabetical not reverse alphabetical order
            #results[(100.0 / score, value.lower(), i)] = (item, round(score, 2))
            item.score = round(score, 2)
            results[(100.0/score, value.lower(), i)] = item

    # sort on keys, then discard the keys
    keys = sorted(results.keys(), reverse=False)
    results = [results.get(k) for k in keys]

    if max_results and len(results) > max_results:
        results = results[:max_results]

    # return list of ordered items
    return results


#-------------#
# Other utils #
#-------------#

def get_selection():
    """ get clipboard content """
    return subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]

def run_cmd(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    subprocess.call(cmd)

def get_cmd_output(cmd_list):
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
