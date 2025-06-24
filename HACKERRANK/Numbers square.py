
# this is exercise 1 from the challenge "Moody's Analytics Women in Engineering Hackathon 2018"
# 181013

import math
import os
import random
import re
import sys

#
# Complete the 'numbersSquare' function below.
#
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER s
#

# let's use a n x n list of lists of numbers

def numbersSquare(n, s):

    Sq = []
    num = s
    for i in range(n):

        #let's add a row, and then fill the positions related to step i
        # do not use an 'empty_row' list because then you will edit all lines
        # when you think you edit only one
        Sq.append(list(range(n)))

        #fill horizontal portion
        for j in range(i+1):
            Sq[j][i] = num

            num += 1

        #fill vertical portion
        for k in range(i):
            Sq[i][i-k-1] = num

            num += 1

    for l in range(n):
        for m in range(n):
            print(Sq[l][m], end=' ')
        print('')


numbersSquare(5, 1)

numbersSquare(10, 4)