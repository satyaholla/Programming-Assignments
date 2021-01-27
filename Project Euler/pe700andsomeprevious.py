#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:29:59 2020

@author: satyaholla
"""

def find_num_factors(num):
    power = 0
    num_factors = 1
    m = num**0.5
    for factor in range(2,4):
        if num % factor == 0:
            while num % factor == 0:
                num //= factor
                power += 1
            num_factors *= power + 1
            
            m = num**0.5
            power = 0
    
    factor = 5
    while factor <= m:
        if num % factor == 0:
            while num % factor == 0:
                num //= factor
                power += 1
            num_factors *= power + 1
            if num == 1:
                break
            m = num**0.5
            power = 0
            
        factor += 2
        if num % factor == 0:
            while num % factor == 0:
                num //= factor
                power += 1
            num_factors *= power + 1
            if num == 1:
                break
            m = num**0.5
            power = 0
        factor += 4
    
    
    if num > 1:
        num_factors *= 2
    
    return num_factors

def find_first_tri(n):
    i = 0
    t = 0
    while True:
        i += 1
        t += i
        if find_num_factors(t) > 500:
            return t

def fast_gcd(a,b):
    e = 1
    if a % 2 == 0 and b % 2 == 0:
            a,b,e = a//2, b//2, 2*e
            
    while min(a,b) > 0:
        if a % 2 == 0:
            a //= 2
        elif b % 2 == 0:
            b //= 2
        elif a > b:
            a = a - b
        elif b > a:
            b = b - a
        else:
            a, e = 0, b
    return e

n = 4503599627370517
current_min = n
a = 1504170715041707
x = 0
tot = 0

while current_min != 258162:
    x += a
    if x > n:
        x -= n
    if x < current_min:
        diff = current_min - x
        while current_min > diff:
            current_min -= diff
            tot += current_min     
            print(current_min)
        x = n - current_min + diff
        
print(tot)

a = 4503599627370517
b = 1504170715041707
"""Try finding m and n such that am + bn = 1"""

# def find_coefficients(a,b):
#     """Given two coprime numbers, returns (m, n) such that am + bn = 1
#         Assumes a >= b"""
#     if b == 0:
#         return (1,0)
#     elif a > b:
#         m = a % b
#         c = a // b
#         d1, d2 = find_coefficients(b, m)
#         return (d2, d1-c*d2)
#     # we know b d1 + m d2 = 1, so b d1 + a d2 - c d2 b = 1
#     # now, we know that c*b + m = a, or m = a - c*b
    
# m,n = find_coefficients(a,b)

# tot = 0
# current_min = 3451657199285665
# for i in range(a):
#     m1 = m*i
#     n1 = n*i
    
#     x = m1//b
#     m1 = m1 - (x+1)*b
#     n1 = n1 + (x+1)*a
    
#     if n1 < current_min:
#         tot += i
#         current_min = n1

# print(tot)
    



    
    

    