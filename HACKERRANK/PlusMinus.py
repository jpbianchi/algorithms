#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'plusMinus' function below.
#
# The function accepts INTEGER_ARRAY arr as parameter.
#

def plusMinus(arr):
    # Write your code here
    from collections import Counter
    def sign2(x):
        match x:
            case _ if x > 0:
                return 1
            case _ if x < 0:
                return -1
            case _ if x == 0:
                return 0

    def sign(x):
        return round(x/abs(x)) if x !=0 else 0

    cnt = Counter([sign(x) for x in arr])
    ratios = {n:cnt[n]/len(arr) for n in cnt}

    print(f"{ratios[1] if 1 in ratios else 0:.6f}")
    print(f"{ratios[-1] if -1 in ratios else 0:.6f}")
    print(f"{ratios[0] if 0 in ratios else 0:.6f}")


if __name__ == '__main__':
    # n = int(input().strip())
    #
    # arr = list(map(int, input().rstrip().split()))
    arr = [-4, 3, -9, 0, 4, 1]
    arr = [1, -2, -7, 9, 1, -8, -5]

    plusMinus(arr)

     # Given an array of integers, calculate the ratios of its elements that are positive, negative, and zero. Print the decimal value of each fraction on a new line with  places after the decimal.
    #
    # Note: This challenge introduces precision problems. The test cases are scaled to six decimal places, though answers with absolute error of up to  are acceptable.
    #
    # Example
    #
    # There are  elements, two positive, two negative and one zero. Their ratios are ,  and . Results are printed as:
    #
    # 0.400000
    # 0.400000
    # 0.200000
    # Function Description
    #
    # Complete the plusMinus function in the editor below.
    #
    # plusMinus has the following parameter(s):
    #
    # int arr[n]: an array of integers
    # Print
    # Print the ratios of positive, negative and zero values in the array. Each value should be printed on a separate line with  digits after the decimal. The function should not return a value.
    #
    # Input Format
    #
    # The first line contains an integer, , the size of the array.
    # The second line contains  space-separated integers that describe .
    #
    # Constraints
    #
    #
    #
    # Output Format
    #
    # Print the following  lines, each to  decimals:
    #
    # proportion of positive values
    # proportion of negative values
    # proportion of zeros
    # Sample Input
    #
    # STDIN           Function
    # -----           --------
    # 6               arr[] size n = 6
    # -4 3 -9 0 4 1   arr = [-4, 3, -9, 0, 4, 1]
    # Sample Output
    #
    # 0.500000
    # 0.333333
    # 0.166667
