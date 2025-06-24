

import math
import os
import random
import re
import sys
import numpy

#this algo is correct but uses recursion and takes hours for even small lists (like 16 days)
def solve(profits):
    num_days = len(profits)
    # let's build a function that computes the best profit over
    # the previous lines but not for the last two algos
    # so we can use it recursively
    def max_profit_over_all(day, *exclude_algos): # first one is latest, 2nd one (if any) oldest
        max_profit = 0

        algo_list = list(x for x in range(4) if x not in exclude_algos)
        #if day != 0: print(day, list(profits[day][k] for k in range(4) if k in algo_list))
        # algo_list contains all algos that can be used, ie not used previous 2 days
        for i in algo_list:

            if day == 0:  # first day - recursivity ends here
                max_profit = max(list(profits[0][x] for x in algo_list))
            else:
                profit_day_before = max_profit_over_all(day - 1, i, exclude_algos[0])
                max_profit = max(max_profit, profit_day_before + profits[day][i])

        return max_profit

    #print(list(max_profit_over_all(num_days-1, algo) for algo in range(4)))
    best_profit = max(list(max_profit_over_all(num_days-1, algo) for algo in range(4)))
    return(best_profit)

def solve2(profits): #without recursion because it leads to O(n!) for large sets
    # since the same algo can be reused 3 days later, we can build an array with all combinations
    # for every day, ie  4 x 4 wide, so we don't have to recurse back to day 0 every day
    # profits_matrix [i][j] = maximum profit if algo i used yesterday and j the day before
    # and now we must edit it for the current day
    # for the first day, we ignore the profits_matrix since there is no 'day before'

    num_days = len(profits)
    for d in range(0, num_days):
        #profits_temp = [[0,0,0,0]]*4 #doesn't work because all 4 copies are linked together
        profits_temp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(4):
            for j in range(4):
                if j == i: # zero if we use same algo today and yesterday
                    profits_temp[i][j] = 0
                else: # zero profit if we used algo i two days earlier
                    algo_range = list(x for x in range(4) if x is not i)
                    profits_temp[i][j] = profits[d][i]
                    # for the first day, it's as if the profits_matrix of the day before is zero
                    if d != 0:  profits_temp[i][j] += max(profits_matrix[j][k] for k in algo_range)
        profits_matrix = profits_temp # let's save profits to use it for tomorrow

    best_profit = max(profits_matrix[i][j] for i in range(4) for j in range(4))
    return(best_profit)

profits = []
profits.append(list(map(int,[10,20,30,40])))
profits.append([60,70,80,110])
profits.append([80,120,90,200])
profits.append([50,300,20,30])
#print(profits)

print("Max profit possible: ", solve2(profits), "correct answer 600")

profits = []
profits.append(list(map(int,[10644862, 56520800, 55178337, 46934767])))
profits.append(list(map(int,[27810341, 939077, 48546321, 51791499])))
profits.append(list(map(int,[38618924, 41477251, 19945218, 89390306])))
profits.append(list(map(int,[9972799, 98576194, 93788097, 31641826])))
profits.append(list(map(int,[92502461, 83375778, 59042823, 67955426])))
#print(profits)
print("Max profit possible: ", solve2(profits), "correct answer  385536082")

### TEST ON SHORT SEQUENCES

input_file = open("Trading Profiles test input1.txt")
test_results = open("Trading Profiles test output1.txt")

queries = int(input_file.readline().strip())

for q_itr in range(queries):
    w = int(input_file.readline().strip())
    expected_result = int(test_results.readline().strip())

    profits = []

    for _ in range(w):
        input_list = list(map(int,(input_file.readline().strip().split())))
        profits.append(input_list)

    result = solve2(profits)

    print("Max profit possible: ", result, "correct answer ", expected_result, " match!!!" if result == expected_result else "NO MATCH")

input_file.close()
test_results.close()

#TEST WITH LONG SEQUENCES (TO DEBUG RECURSIVE IMPLEMENTATION)

input_file = open("Trading Profiles test input.txt")
test_results = open("Trading Profiles test output.txt")

queries = int(input_file.readline().strip())

for q_itr in range(queries):
    w = int(input_file.readline().strip())
    expected_result = int(test_results.readline().strip())

    profits = []

    for _ in range(w):
        input_list = list(map(int,(input_file.readline().strip().split())))
        profits.append(input_list)

    result = solve2(profits)

    print("Max profit possible: ", result, "correct answer ", expected_result, " match!!!" if result == expected_result else "NO MATCH")

input_file.close()
test_results.close()

