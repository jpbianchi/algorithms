#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'timeConversion' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def timeConversion(s):
    # Write your code here
    from datetime import datetime
    dt = datetime.strptime(s, "%I:%M:%S%p")
    return(dt.strftime("%H:%M:%S"))

if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # s = input()
    s = "07:05:45PM"

    result = timeConversion(s)
    print(result)
    # fptr.write(result + '\n')
    #
    # fptr.close()

    # https://www.hackerrank.com/challenges/one-week-preparation-kit-time-conversion/problem?isFullScreen=true&h_l=interview&playlist_slugs%5B%5D=preparation-kits&playlist_slugs%5B%5D=one-week-preparation-kit&playlist_slugs%5B%5D=one-week-day-one
    # Given a time in -hour AM/PM format, convert it to military (24-hour) time.
    #
    # Note: - 12:00:00AM on a 12-hour clock is 00:00:00 on a 24-hour clock.
    # - 12:00:00PM on a 12-hour clock is 12:00:00 on a 24-hour clock.
    #
    # Example
    #
    #
    # Return '12:01:00'.
    #
    #
    # Return '00:01:00'.
    #
    # Function Description
    #
    # Complete the timeConversion function in the editor below. It should return a new string representing the input time in 24 hour format.
    #
    # timeConversion has the following parameter(s):
    #
    # string s: a time in  hour format
    # Returns
    #
    # string: the time in  hour format
    # Input Format
    #
    # A single string  that represents a time in -hour clock format (i.e.:  or ).
    #
    # Constraints
    #
    # All input times are valid
    # Sample Input
    #
    # 07:05:45PM
    # Sample Output
    #
    # 19:05:45