#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 19:04:25 2020

@author: satyaholla
"""

f = open('/Users/satyaholla/Desktop/p067_triangle.txt', 'r')
s = f.read()

nums = s.split('\n')
for i in range(len(nums)):
    nums[i] = nums[i].split(' ')

for l in nums:
    for i in range(len(l)):
        l[i] = int(l[i])

for row_number in range(len(nums)-2, -1, -1):
    for i in range(len(nums[row_number])):
        nums[row_number][i] += max(nums[row_number + 1][i], nums[row_number + 1][i+1])

print(nums[0][0])