#!/usr/bin/env python

import os
import time

def child():
    print('New child ', os.getpid())
    os._exit(0)

def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            time.sleep(3)
            os.waitpid(newpid, 0)


parent()
