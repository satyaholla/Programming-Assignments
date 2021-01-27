#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:17:58 2020

@author: satyaholla
"""

"""Project Euler Problems"""

import math
from itertools import combinations

# def primeList(n):
#     """Returns an ordered list of all primes under n"""
#     assert isinstance(n, (int, float))
#     if n <= 2:
#         return []
#     if type(n) == float:
#         n = int(n) + 1
    
#     #now, we know n is an integer greater than 2
#     primes = [2] #running list of primes
#     sieve = [True for x in range(n//2)]
#         # in this sieve, each value in the ith index represents the number 2*i + 1
#     sieve[0] = False
#     sqrtMax = int(n**.5)
#     for i in range((sqrtMax - 1)//2 + 1): # for all the indices under the sqrt in the sieve
#         if sieve[i]: # if it's a prime
#             r = 2*i + 1 # r is the actual value of the prime
#             for n in range(round((r**2 - 1)/2), len(sieve), r): # start at r**2's index
#                 sieve[n] = False
    
#     for i in range(len(sieve)):
#         if sieve[i]:
#             primes.append(2*i + 1)
    
#     return primes

# def isPrime(x):
#     """Returns the truth value of a number's primality"""
#     if x in memorized:
#         return True
#     if x <= 1:
#         return False
#     if x % 2 == 0 or x % 3 == 0:
#         return False
#     index = 5
#     m = x**.5
#     while index <= m:
#         if x % index == 0:
#             return False
#         if x % (index + 2) == 0:
#             return False
#         index += 6
#     memorized.add(x)
#     return True

# memorized = set()
# memorized.add(2)
# memorized.add(3)


# # Problem 27:
# # First, I will find all primes less than 1000, since b must be a positive prime
# primes = primeList(2000)
# possible = []
# b = 0
# while primes[b] <= 1000:
#     aPlusBPlusOne = 0
#     x = primes[b]
#     while primes[aPlusBPlusOne] <= 1001 + x:
#         possible.append((primes[aPlusBPlusOne] - 1 - x, x))
#         aPlusBPlusOne += 1
#     b += 1
    
# m = 0
# mElem = 0
# for elem in possible:
#     n = 4
#     while isPrime(round(n**2 + elem[0]*n + elem[1])):
#         n += 1
#     if n > m:
#         m = n
#         mElem = elem

# print(mElem[0],mElem[1])



# Problem 28:
# numbers = [1]
# n = 1
# i = 2
# while n != 1001**2:
#     for x in range(4):
#         n += i
#         numbers.append(n)
#     i += 2
    
# print(sum(numbers))



# Problem 27:
# powers = {}
# for a in range(2,101):
#     n = 2
#     while a**n <= 100:
#         if a**n not in powers:
#             powers[a**n] = a
#         n += 1
#     if n == 2:
#         break

# powers2 = {}
# for elem in powers:
#     if powers[elem] not in powers2:
#         powers2[powers[elem]] = 1
#     powers2[powers[elem]] += 1
    
# n = 0
# for elem in powers2:
#     sieve = [False for x in range(100*powers2[elem] + 1)]
#     for x in range(1, powers2[elem] + 1):
#         for y in range(0, min(len(sieve), 100*x), x):
#             sieve[y] = True
#     n += sieve[2:].count(True)
    
# for x in range(2,100):
#     if x not in powers and x not in powers2:
#         n += 99


# # Project Euler Problem 29:
# powers = set()
# bases = {}
# for x in range(2,101):
#     if x**2 > 100:
#         break
#     n = 1
#     if x in powers:
#         continue
#     while x**n <= 100:
#         powers.add(x**n)
#         n += 1
#     bases[x] = n - 1
    
# tot = 0
# for key in bases:
#     unique = set()
#     for i in range(1, bases[key] + 1):
#         for j in range(2, 101):
#             unique.add(i*j)
#     tot += len(unique)
    
# for x in range(2,101):
#     if x not in powers:
#         tot += 99

# # Project Euler Problem 30:
# x = 9**5
# n = 0
# while len(str(x*n)) >= n:
#     n += 1
    
# # Whatever n is now, we know that any solution cannot be an n-digit number.
# n -= 1
# solMax = x*n
# tot = 0
# for i in range(solMax + 1):
#     if i == sum([int(j)**5 for j in str(i)]) and len(str(i)) > 1:
#         tot += i



# Project Euler Problem 30:
# n = 200
# coins = (1,2,5,10,20,50,100,200)
# l = len(coins)

# def waysToForm(n):
#     """returns the number of ways to make the value n with the coins"""
#     def dotProd(*tup):
#         return sum([coins[i]*tup[i] for i in range(l)])
#     tot = 0
#     for i8 in range(2):
#         for i7 in range(3):
#             if dotProd(0,0,0,0,0,0,i7,i8) > 200:
#                 break
#             for i6 in range(5):
#                 if dotProd(0,0,0,0,0,i6,i7,i8) > 200:
#                     break
#                 for i5 in range(11):
#                     if dotProd(0,0,0,0,i5,i6,i7,i8) > 200:
#                         break
#                     for i4 in range(21):
#                         if dotProd(0,0,0,i4,i5,i6,i7,i8) > 200:
#                             break
#                         for i3 in range(41):
#                             if dotProd(0,0,i3,i4,i5,i6,i7,i8) > 200:
#                                 break
#                             for i2 in range(101):
#                                 if dotProd(0,i2,i3,i4,i5,i6,i7,i8) <= 200:
#                                     tot += 1
#                                 else:
#                                     break
#     return tot
    
# print(waysToForm(n))


# # Project Euler Problem 43:
# numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# tot = 0
# for i1 in range(1,10):
#     for i2 in range(9):
#         for i3 in range(8):
#             for i4 in range(7):
#                 for i5 in range(6):
#                     for i6 in range(5):
#                         for i7 in range(4):
#                             for i8 in range(3):
#                                 for i9 in range(2):
#                                     numberscpy = numbers[:]
#                                     n = []
#                                     n.append(numberscpy[i1])
#                                     numberscpy.pop(i1)
#                                     n.append(numberscpy[i2])
#                                     numberscpy.pop(i2)
#                                     n.append(numberscpy[i3])
#                                     numberscpy.pop(i3)
#                                     n.append(numberscpy[i4])
#                                     numberscpy.pop(i4)
#                                     n.append(numberscpy[i5])
#                                     numberscpy.pop(i5)
#                                     n.append(numberscpy[i6])
#                                     numberscpy.pop(i6)
#                                     n.append(numberscpy[i7])
#                                     numberscpy.pop(i7)
#                                     n.append(numberscpy[i8])
#                                     numberscpy.pop(i8)
#                                     n.append(numberscpy[i9])
#                                     numberscpy.pop(i9)
#                                     n.append(numberscpy[0])
#                                     s = ''.join(n)
#                                     if int(s[3]) % 2 == 0 and\
#                                        int(s[2:5]) % 3 == 0 and\
#                                        int(s[5]) % 5 == 0 and\
#                                        int(s[4:7]) % 7 == 0 and\
#                                        int(s[5:8]) % 11 == 0 and\
#                                        int(s[6:9]) % 13 == 0 and\
#                                        int(s[7:10]) % 17 == 0:
#                                            tot += int(s)

# nums = [2,10000]
# for x in range(1000):
#     nums.append(nums[-2] + nums[-1])
    
# ratios = []
# for x in range(1, len(nums)):
#     ratios.append(nums[x]/nums[x-1])
    
# diffs = []
# for x in range(1,len(ratios)):
#     diffs.append(abs(ratios[x] - ratios[x-1]))

# for x in range(1, len(diffs)):
#     assert 2*diffs[x] <= diffs[x-1]

# Project Euler Problem 32:
# possible = {(1,4,4),(2,3,4)}
# answers = set()
# digits = [x for x in '123456789']

# def pandigitals():
#     numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
#     indices = [1 for x in range(8)]
#     for indices[0] in range(9):
#         for indices[1] in range(8):
#             for indices[2] in range(7):
#                 for indices[3] in range(6):
#                     for indices[4] in range(5):
#                         for indices[5] in range(4):
#                             for indices[6] in range(3):
#                                 for indices[7] in range(2):
#                                     numberscpy = numbers[:]
#                                     n = []
#                                     for i in range(8):
#                                         n.append(numberscpy[indices[i]])
#                                         numberscpy.pop(indices[i])
                                    
#                                     n.append(numberscpy[0])
#                                     s = ''.join(n)
#                                     yield s

# for x in pandigitals():
#     for y in possible:
#         a = int(x[:y[0]])
#         b = int(x[y[0]: y[0] + y[1]])
#         c = int(x[y[0] + y[1]:])
#         if a*b == c:
#             answers.add(c)



# Project Euler Problem 33:
# answers = set()
# for den in range(10,100):
#     for num in range(10,den):
#         d = str(den)
#         n = str(num)
#         same = []
#         for char in d:
#             if char in n:
#                 same.append(char)
#         if same == ['0']:
#             continue
#         for elem in same:
#             if d[0] == elem:
#                 d1 = int(d[1])
#             else:
#                 d1 = int(d[0])
#             if n[0] == elem:
#                 n1 = int(n[1])
#             else:
#                 n1 = int(n[0])
#             if n1*den == d1*num:
#                 answers.add((n1,d1))
                
# num = 1
# den = 1
# for k in answers:
#     num *= k[0]
#     den *= k[1]
# a = den//(math.gcd(num,den))

# Project Euler Problem 34:
# first, find the largest possible number which fits this description
# x = 1
# while math.factorial(9)*x >= 10**(x-1):
#     x+=1
# x -= 1
# m = math.factorial(9)*x
# answers = set()
# for y in range(3,m):
#     if y == sum([math.factorial(int(i)) for i in str(y)]):
#         answers.add(y)
# print(sum(answers))