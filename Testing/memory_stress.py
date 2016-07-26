# -*- coding: utf-8 -*-
"""
@author: cecile
"""


import string
import random

#memory stress load

if __name__ == '__main__':
    d = {}
    i = 0;
    for i in range(0, 100000000):
        value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2)) # generate ramdom string of size 200
        d[i] = value
        if i % 10000 == 0:
            print (i)