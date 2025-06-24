

# https://www.hackerrank.com/challenges/encryption/problem

#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the encryption function below.
def encryption(s):

    s = ''.join(s.split())
    len_s = len(s)
    row = math.floor(math.sqrt(len_s))
    columns = math.ceil(len_s / row)
    if (row+1) * (columns-1) > row * columns:  # we want row * columns maximum
        row = row+1
        columns = columns-1
    print(row, columns)
    word_list = []
    for i in range(row):
        word = s[i*columns:(i+1)*columns]
        word_list.append(word)
    #print('\n'.join(word_list))

    encrypted_list = []
    for i in range(columns):
        word = ''
        for j in range(row):
            try:
                word = word + word_list[j][i]
            except:
                pass
        print(word)
        encrypted_list.append(word)

    return ' '.join(encrypted_list)

if __name__ == '__main__':

    s = 'if man was meant to stay on the ground god would have given us roots'
            # should give 'imtgdvs fearwer mayoogo anouuio ntnnlvt wttddes aohghn sseoau'

    print(encryption(s))

    print(encryption('chillout'))  # -> 'clu hlt io'

