#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'countingSort' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def countingSort(arr):
    # Write your code here
    zer = [0] * 100
    for n in arr:
        zer[n] += 1

    return zer


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # n = int(input().strip())

    # arr = list(map(int, input().rstrip().split()))
    inp = "63 54 17 78 43 70 32 97 16 94 74 18 60 61 35 83 13 56 75 52 70 12 24 37 17 0 16 64 34 81 82 24 69 2 30 61 83 37 97 16 70 53 0 61 12 17 97 67 33 30 49 70 11 40 67 94 84 60 35 58 19 81 16 14 68 46 42 81 75 87 13 84 33 34 14 96 7 59 17 98 79 47 71 75 8 27 73 66 64 12 29 35 80 78 80 6 5 24 49 82"
    arr = [int(x) for x in inp.split()]
    print("MAX value",max(arr))
    result = countingSort(arr)
    print(result)
    exp = [int(x) for x in "2 0 1 0 0 1 1 1 1 0 0 1 3 2 2 0 4 4 1 1 0 0 0 0 3 0 0 1 0 1 2 0 1 2 2 3 0 2 0 0 1 0 1 1 0 0 1 1 0 2 0 0 1 1 1 0 1 0 1 1 2 3 0 1 2 0 1 2 1 1 4 1 0 1 1 3 0 0 2 1 2 3 2 2 2 0 0 1 0 0 0 0 0 0 2 0 1 3 1 0".split()]
    print('Expected \n', exp)
    assert arr == exp, 'Wrong answer'
    # fptr.write(' '.join(map(str, result)))
    # fptr.write('\n')
    #
    # fptr.close()
