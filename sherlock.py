#! /usr/bin/env python3
# Sherlock

import sys

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
