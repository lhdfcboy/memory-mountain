#!/usr/bin/env python

# note that this script is written for python2, but it should be
# straightforward to port it to python3

import numpy as np
from multiprocessing import Process
import os 
import subprocess

# repeat execution for this number of times, and only keep the median
# value. (simplistic way to reduce noise)
count = 20


for mag in range(10,27): # from 2^10 (1kB) to 2^27 (64MB)
    size = 2**mag
    for stride in range(1,30,2):

        results = []
        for repeat in range(count):
            #log=subprocess.check_output(["x64\Release\moutain.exe",str(size),str(stride)]);
            p = subprocess.Popen("./benchmark %s %s " % (str(size),str(stride)), shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
            p.wait()
            result_lines = p.stdout.readlines()
            for line in result_lines:
                print(line.strip())
                if "MB/s" in line:
                    results.append( float(line[ line.find('=')+1: line.find('MB/s') ]) ) 

        print( size,stride,np.median(results))
        with open('results.txt', 'a+') as f :
            f.write('%d %d %d\n' % (size,stride,np.median(results)))
