
# https://www.hackerrank.com/challenges/repeated-string/problem
# Easy

import math
import os
import random
import re
import sys

from collections import Counter

# Complete the repeatedString function below.
def repeatedString(s, n):

    num_a_in_s = Counter(s)['a']
    print(num_a_in_s)
    short_s = s[0: n % len(s)]
    num_a_in_short = Counter(short_s)['a']
    print(num_a_in_short)

    return num_a_in_s * (n // len(s)) + num_a_in_short


if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = 'aba'

    n = 10

    result = repeatedString(s, n)

    print(result)

    #fptr.write(str(result) + '\n')

    #fptr.close()