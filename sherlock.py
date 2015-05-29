#! /usr/bin/env python
# Sherlock

import os
import sys

# Don't import ./sherlock.py when running an installed binary at /usr/.../sherlock.py
if __file__[:4] == '/usr' :
    sys.path.remove(os.path.dirname(__file__))

from sherlock.main import Sherlock

def main():

    debug = False
    if '--debug' in sys.argv:
        debug = True

    m = Sherlock(debug)
    m.run()
    return True

if __name__ == '__main__':
    sys.exit(main())
