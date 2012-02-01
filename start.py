#!/usr/bin/env python
from manager import Manager

if __name__ == '__main__':
    m = Manager()
    m.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        m.end()
