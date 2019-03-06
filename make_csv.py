#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 23:29:14 2018

@author: yui-sudo
"""

import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import csv

# drysrc directory
dry_dir = os.getcwd() + "/elements/"

df = pd.DataFrame()

total = 0
class1 = 0

with open('label.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["dir2", "total", "dir1", "class1", "class2"])
    dir1_list = os.listdir(dry_dir)
    dir1_list.sort()
    for dir1 in dir1_list:
        class2 = 0
        cur_dir = dry_dir + dir1        
        if os.path.isdir(cur_dir) == True:        
            dir2_list = os.listdir(cur_dir)
            dir2_list.sort()
            for dir2 in dir2_list:        
                print(dir1)
                print(dir2)
                writer.writerow([dir2, total, dir1, class1, class2])
                class2 += 1
                total += 1
            class1 += 1
        
