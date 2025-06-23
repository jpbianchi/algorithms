#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'formingMagicSquare' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY s as parameter.
#

def formingMagicSquare(s):
    # Write your code here
    ideal = [[6,1,8],[7,5,3],[2,9,4]]
    total = sum(ideal[0])
    
    def sumline(n):
        return sum(s[n]) == total
    def sumcol(n):
        return sum(s[0][i] for i in range(3)) == total
    def sumdiag():
        return sum(s[i][i] for i in range(3)) == total
    def sumdiag2():
        return sum(s[i][2-i] for i in range(3)) == total
    def summat(x):
        return sum(sum(x[i]) for i in range(3))
    def ismagic():
        return all([*[sumline(i) for i in range(3)],
                   *[sumcol(i) for i in range(3)],
                   sumdiag(), sumdiag2()])
    
    
    def rotate(m):
        return [[m[0][2],m[1][2],m[2][2]], 
                [m[0][1],m[1][1],m[2][1]], 
                [m[0][0],m[1][0],m[2][0]]]
    
    def flipV(m):
        return [m[2], m[1], m[0]]
    
    def flipH(m):
        return [m[0][::-1], m[1][::-1], m[2][::-1]]
    
    def diffmat(m1,m2):
        return sum(abs(m1[i][j]-m2[i][j]) for i in range(3) for j in range(3))
    
    def printm(m):
        for r in m:
            print(r)
    printm(s)
    dist = 30
    sol = s.copy()
    for _ in range(4):
        ideal = rotate(ideal)
        print("-"*50)
        printm(ideal)
        
        d = diffmat(s,ideal)
        if d < dist:
            sol = ideal.copy()
            print("rotation", d)
            printm(ideal)
            dist = d
            
        ideal1 = flipV(ideal)
        d = diffmat(s,ideal1)
        if d < dist:
            sol = ideal1.copy()
            print("flipV", d)
            printm(ideal1)
            dist = d
            
        ideal2 = flipH(ideal)
        d = diffmat(s,ideal2)
        
        if d < dist:
            sol = ideal2.copy()
            print("flipH", d)
            printm(ideal2)
            dist = d
            if d == 0:
                break
        
        if dist == 0:
            break
    printm(sol)
    return dist

    # we cannot approach this problem by trying to move numbers back and forth until we get a magic square,
    # it would be too complex... even if there are, say, 2 sixes, it doesn't mean that replacing one of them
    # will lead to a magic square.
    # a more general approach is to realize that, instead of calculating the difference of the positions changed,
    # we can calculate the difference of the whole matrix against an ideal magic square (the correct positions
    # give zero).  So, we could test our given matrix against all possible magic squares.  At 3x3, there aren't many,
    # since they are all derived from the ideal magic square, with rotations and swapping row or cols 1 & 3 
    
s1= [[5,3,4],[1,5,8],[6,4,2]]  # 7
s2= [[8,3,4],[1,5,9],[6,7,2]]  # 0
s3 =[[4,8,2],[4,5,7],[6,1,6]]  # 4
s4 =[[4,9,2],[3,5,7],[8,1,5]]  # 1
S = [s1,s2,s3,s4]
solutions = [7,0,4,1]
for s,sol in zip(S, solutions):
    assert sol == formingMagicSquare(s), f"Error for matrix s"
print("SUCCESS")

