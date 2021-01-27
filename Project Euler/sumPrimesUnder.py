#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:59:42 2020

@author: satyaholla
"""

# print(sumPrimesUnder(2000000))

def sumPrimesUnder(m: int) -> int:
    if m < 3:
        return 0
    if m == 3:
        return 2
    if m < 6:
        return 5
    
    def isPrime(x: int) -> bool:
        if x == 1:
            return False
        if x == 2 or x == 3:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        index = 5
        m = x**.5
        while index <= m:
            if x % index == 0:
                return False
            if x % (index + 2) == 0:
                return False
            index += 6
        return True
    
    current_sum = 5
    index = 7
    while index < m:
        if isPrime(index - 2):
            current_sum += index - 2
        if isPrime(index):
            current_sum += index
        index += 6
    if index - 2 < m and isPrime(index - 2):
        current_sum += index - 2
        
    return current_sum

print(sumPrimesUnder(2000000))
            
        
