#! /usr/bin/env python3
# Sherlock

import sys

from main import Sherlock

def main():

    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True

    m = Sherlock(debug)
    m.run()
    return True

if __name__ == '__main__':
    sys.exit(main())
