#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:07:48 2020

@author: satyaholla
"""
import copy

def formatPrint(a, l):
    b = str(a)
    if len(b) > l:
        raise ValueError("too big")
    c = ' '*(l - len(b))
    print(c + b, end = ' ')

def flip(a):
    b = copy.deepcopy(a)
    b.reverse()
    return b

def find_paths(length, width):
    if paths[length][width] != -1:
        return paths[length][width]
    if length == 0 or width == 0:
        paths[length][width] = 1
        return 1
    paths[length][width] = find_paths(length, width - 1) + find_paths(length - 1, width)
    return paths[length][width]

paths = [[-1 for x in range(21)] for y in range(21)]
print(find_paths(20,20))
paths[0][0] = 1
for lt in paths:
    for i in range(len(lt)):
        formatPrint(lt[i], len(str(paths[20][i])))
    print()
    