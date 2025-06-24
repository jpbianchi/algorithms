

import math
import os
import random
import re
import sys
import timeit
import cProfile


# for 2^n = 2.2.2.2.2.... n times, so it's a matter of combining the sequence
# S(2^n) is number of possible combinations
# digit 1 is forbidden, so the combinations can only be with the numbers 2, 4 and 8
# each new number has n+1 2's in the sequence, so for there are S(2^(n-1)) numbers
# starting with a 2, S(2^(n-2) numbers starting with a 4, and S(2^(n-1)) starting with 8
# so S(ai) = S(ai-1) + S(ai-2) + S(ai-3)... tribonacci sequence: 1 2 4 7 13 24 44 etc


def tribo(n):
    if n == 1: return 1
    if n == 2: return 2
    if n == 3: return 4

    t = [1, 2, 4]
    for i in range(4, n + 1):
        t.append(sum(t))
        t.pop(0)
    return t[2]

def solve2(a): # works but too slow for big numbers

    ls = sorted(a)
    len_ls = len(ls)
    total = pos = 0
    t = [0,0,1]
    modu = 7 + pow(10,9) #to avoid computing it thousands of times
    for i in range(1,max(ls)+1):
        t.append(sum(t) % modu)  #use modu value otherwise big big numbers
        t.pop(0)
        while pos < len_ls and i == ls[pos]: # in case a number appears several times
            total += t[2]
            pos += 1
    return total % modu

def solve3(a): # works but too slow for big numbers
    ls = sorted(a)
    len_ls = len(ls)
    total = pos = 0
    first = second = 0
    third = 1
    modu = 7 + pow(10,9) #to avoid computing it thousands of times
    maximum_range = max(ls)+1
    for i in range(1,maximum_range):
        first, second, third = second, third, (first + second + third) % modu
        while pos < len_ls and i == ls[pos]:  # in case a number appears several times
            total += third
            pos += 1

    return total % modu

def solve(a):
    'Here, we use a matrix multiplication approach: T(n) = M^n T(0)'

    def mult_31(m,c): #multiplies a 3x3 matrix with a 3x1 column to generate T(n)
                        # returns value in c, ready for next iteration
        c0 = m[0][0] * c[0] + m[0][1] * c[1] + m[0][2] * c[2]
        c1 = m[1][0] * c[0] + m[1][1] * c[1] + m[1][2] * c[2]
        c2 = m[2][0] * c[0] + m[2][1] * c[1] + m[2][2] * c[2]
        c[0], c[1], c[2] = c0 % modu, c1 % modu, c2 % modu

    ls = a
    len_ls = len(ls)
    nmax = math.trunc(math.log(max(ls)) / math.log(2)) # this algo is O(log)
    modu = 7 + pow(10, 9)
    mi = [[[1, 1, 1], [1, 0, 0], [0, 1, 0]]]
    # let's create all powers of mi: mi[r] = mi[0]^(2^r) = mi[r-1]^2
    # element [0] of product of mi[i] with [1,0,0] will give tribonacci(2^i)
    # so mi[n][0][0] = tribonacci(2^n)
    for r in range(1, nmax + 2):
        mi.append([[0, 0, 0], [0, 0, 0], [0, 0, 0]])  # now mi[r] exists
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    mi[r][i][j] += mi[r - 1][i][k] * mi[r - 1][k][j]
                mi[r][i][j] = mi[r][i][j] % modu

    def tribo(nn):  # works but not used because of differential optimization below
        bin_n = str(bin(nn))[2:]
        # print(bin_n[::-1])
        i_index = 0
        t = [1, 0, 0]
        for i in bin_n[::-1]:
            if i == '1':
                mult_31(mi[i_index + 1], t)
                t_i = mi[i_index + 1][0][0]
                # print(i_index, "  ", t_i, "  ", t)
            i_index += 1
        return t[0]

    pos = 0
    sum_ls = 0
    t = [1, 0, 0]
    while pos < len_ls:
        # here we know next number is bigger, so let's compute the differential matrix
        # to avoid having to recompute the whole tribonacci number
        # t is vector of multiplication of various mi[i]'s and [1,0,0] so let's not recompute that
        # we just need to take the difference between next and last value, and calc mi[1]^diff*t
        # so we just need to use mult_31 again on t depending on binary value of diff
        diff = ls[0] if pos == 0 else ls[pos] - ls[pos - 1]
        # lets convert diff in binary, and invert it so index('1') gives mi to use
        bin_diff = str(bin(diff))[::-1] # no need to remove '0b'
        # let's list the powers of two in bin_diff, to know which mi's to use
        list_ones = list(i for i in range(len(bin_diff)) if bin_diff[i] == '1')
        # now we just need to multiply t with all mi[k] with k in list_ones
        for i in list_ones: mult_31(mi[i], t)
        # t won't change for consecutive numbers, so in all cases we can do the following
        sum_ls = (sum_ls + t[0]) % modu
        pos += 1

    return sum_ls

if __name__ == "__main__":

    print(list(map(tribo, list(range(1,20)))))

    S = list(map(int,"873 297 23 796 895 22 922 740 285 392".split()))
    print(solve3(S), " expected 199709257")

    S = list(map(int,"1 3 10 2 3 4 8 10 5 3".split()))
    print(solve3(S), " expected 664")

    print("new way", solve3([500]), "old way", solve([500]))

    test_string = []
    for line in open("Combination of Digits - long test.txt", 'r'):
        test_string = test_string + list(map(int,line.strip().split()))
    expected_result = int(test_string[0])
    test_string.pop(0)
    num_of_numbers = test_string[0]
    test_string.pop(0) #take the number of elements out of test_string

    test_string = sorted(test_string)
    #print(test_string[:10])
    #print(test_string[-11:-1][::-1])
    print("List with ", num_of_numbers, " numbers, the biggest ones being:")
    print(test_string[-11:-1][::-1])
    #print(solve3(test_string[:5000]))
    cProfile.run('print(solve(test_string[:]), " expected ", expected_result)')

    #print(solve(test_string), " expected ", expected_result)
