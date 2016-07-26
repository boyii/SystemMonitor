# -*- coding: utf-8 -*-
"""
@author: cecile
"""

from multiprocessing import Pool
from multiprocessing import cpu_count

#CPU stress load
def f(x):
    while True:
        x*x

if __name__ == '__main__':
    processes = cpu_count()
    print ('utilizing %d cores\n' % processes)
    pool = Pool(processes)
    pool.map(f, range(processes))