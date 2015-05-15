import os
import time

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
