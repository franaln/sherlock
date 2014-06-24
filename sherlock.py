#! /usr/bin/env python3
# Sherlock

import sys

from main import Sherlock

def main():
    m = Sherlock()
    m.run()
    return True

if __name__ == '__main__':
    sys.exit(main())
