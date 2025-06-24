# https://www.hackerrank.com/contests/moodys-analytics-2018-women-in-engineering/challenges/analytical-queries/problem

from termcolor import colored

import math
import os
import random
import re
import sys

def print_aligned(ll, colored=False):
    list_of_queries = [int(queries[i][0][:queries[i][0].index('_')]) for i in range(len(queries))]

    for j in ll:

        try:
            i = int(j[:j.index('_')])
        except:
            i = j

        if i < 0:
            print('-' * -i, end='')
        elif i == 0:
            print('  .', end='')
        elif i < 10:
            if colored and j in list_of_queries:
                print('  ' + '\033[92m' + '\033[1m' + str(i) + '\033[0m', end='')
            else:
                print('  ' + str(i), end='')
        elif i < 100:
            if (colored and j in list_of_queries) or i==85:
                print(' ' + '\033[92m' + '\033[1m' + str(i) + '\033[0m', end='')
            elif i == 94:  print(' ' + '\033[93m' + '\033[1m' + str(i) + '\033[0m', end='')
            elif i == 19: print(' ' + '\033[94m' + '\033[1m' + str(i) + '\033[0m', end='')
            else:
                print(' ' + str(i), end='')
        else:
            if colored:
                if i==100: print(' ', end='')
                if (j in list_of_queries) : print('\033[92m' + str(i) + '\033[0m', end='')
                elif not i % 2:             print(str(i), end='')
                else:                       print('\033[92m' + '   '  + '\033[0m', end='')
            else: print('' + str(i), end='')
    print('')

def solve(queries):
    # Write your code here
    # let's first try by putting the query number in a list at the position of it's beginning time
    # and filling the k positions ahead
    # we'll leave first position unused to we can use l[k] for kth algo to avoid +-1 all the time

    def _print():
        print_aligned([i for i in range(len(l[0]))])
        for i in l: print(i)
        wait = input("Type any key to continue")

    def one_more_line(l):
        #nonlocal cycles
        l += [[0] * len(l[0])]
        pass

    def stretch_all(num):
        for i in range(len(l)):
            l[i] += ([0] * num)
            if _print_debug: print([i for i in range(len(l[0]))])
        pass

    def avail_pos2(start, alloc):  # available positions on all rows, starting at start to start+incr (not included)
        if (start + alloc) > len(l[0]):
            end = len(l[0])
        else:
            end = start + alloc
        c = 0
        for li in l:
            c += li[start:end].count(0)
        return c >= k

    def avail_pos(start, latest):  # available positions on all rows, starting at start to start+incr (not included)
        c = 0
        for li in l:
            c += li[start:latest + 1].count(0)
        return c >= k

    def fill2(q, k):
        c = 0
        i = q
        while True:
            for li in l:  # we fill all lines in parallel
                if li[i] == 0:
                    li[i] = q
                    c += 1
                    if c == k: return
            i += 1

    def fill(q, latest):
        c = 0
        i = latest
        while True:
            for li in l:  # we fill all lines in parallel
                if li[i] == 0:
                    li[i] = q
                    c += 1
                    if c == k: return
            i -= 1  # we go backwards now, from latest

    def format(queries):
        '''This shifts all queries numbers starting with 1, to avoid high numbers creating long lines of zeroes.
            Here, the queries are still untouched, ie no additional info has been added to queries[0]'''
        min_q = min((queries[i][0]) for i in range(len(queries)))
        print(min_q)
        for i in range(len(queries)): queries[i][0] -= min_q - 1
        print(queries)

    def rename_queries(queries):
        '''We add _number to all queries to mark duplicates queries who can start at the same time'''
        id = 0
        for q in queries:
            q[0] = str(q[0]) + '_' + str(id)
            id +=1

    def push_latest():
        '''This creates enough lines to push all queries, starting from the left with the one who can be latest'''
        failure = True
        while failure:
            if _print_debug: print(queries)
            if _print_debug: _print()
            for query in queries:
                q = query[0]
                q0 = int(q[:q.index('_')])
                alloc = query[1]
                latest = q0 + alloc - 1
                if latest >= len(l[0]):  # lists not long enough for this new query, so stretch ALL lines to latest
                    stretch_all(latest + 1 - len(l[0]))
                    if _print_debug: _print()
                # from here, the lists are long enough, but do we have enough available computer power for new query
                if avail_pos(q0, latest):  # now we can fill the lists with q to book the time slots
                    fill(q, latest)
                    if _print_debug: _print()
                    if query == queries[-1]:  # we placed the last query, we're done, let's get outta here
                        failure = False
                        break# break will only break from the for loop, so we need to clear the failure flag too
                else:
                    one_more_line(l)
                    if _print_debug: _print()
                    # l = [[0] * len(l[0])]* len(l) # does not work, it creates linked rows FUCK
                    for ii in range(len(l)):
                        for kk in range(len(l[0])):
                            l[ii][kk] = 0
                    break
        return failure  # to better spread over more lines

    def find_room(q, num_cols, num_lines, reverse = False):
        '''This tries to find an empty cell to place q, starting from the left, going down in each 'column'
        except if reverse is True, then we look from the right'''
        q0 = int(q[0][:q[0].index('_')])
        end = q0 + q[1]  # q[0] + q[1] should never exceed num_cols
        if q0 + q[1] > num_cols: print("ERROR ERROR ERROR in finding room", q, q0, q[1], num_cols)
        rr = range(q0,end) if not reverse else list(range(q0, end))[::-1] #range(end, q0) is not the same
        for i in rr:
            for j in range(num_lines):
                if l[j][i] == 0:
                    return j, i
        return (0, 0)

    def find_q(q, num_cols, num_lines, reverse = False):
        '''This finds the first location of q, if any, starting from the right, going down in the column'''
        # no reverse here, we always start from the right
        q0 = int(q[0][:q[0].index('_')])
        end = min(q0 + q[1], num_cols) # q[0] + q[1] should never exceed num_cols, just a precaution
        rr = range(q0, end) if reverse else list(range(q0, end))[::-1]  # range(end, q0) is not the same
        for i in rr:  # we start from the back!!
            for j in range(num_lines):
                if l[j][i] == q[0]: return j, i
        return (0, 0)

    def remove_last_line():
        '''This tries to remove the last line by distributing its queries to previous lines'''
        last_line_number = len(l) - 1
        last_line = l[last_line_number]
        list_q = sorted([i for i in last_line if i != 0])

        # now let's move the smallest ones first to the utmost left
        for q in queries:
            while q[0] in list_q:
                new_loc = find_room(q, len(l[0]), last_line_number)
                if not new_loc == (0, 0):
                    list_q.pop(list_q.index(q[0]))  #empty list_q with one operation
                    l[new_loc[0]][new_loc[1]] = q[0]
                    l[last_line_number][last_line.index(q[0])] = 0
                else: # there's still values on lastline we can't place, so stop pushing everything to the left
                    break
        if last_line.count(0) == len(l[0]):  # we have successfully moved all queries from this line
            l.pop(-1)  # remove last line
            return True
        else:
            return False

    def shift_left(num_cols, num_lines):
        for q in queries:
            for i in range(k):
                loc = find_q(q, num_cols, num_lines) # we cannot pick further then q + alloc - 1
                if loc != (0,0):
                    new_loc = find_room(q, num_cols, num_lines - 1)
                    if new_loc != (0,0):
                        l[new_loc[0]][new_loc[1]] = q[0]
                        l[loc[0]][loc[1]] = 0
                    else: break
                else: break

    def shift_right(q,num_cols, num_lines):
        '''Not the same as shift_left, we just push occurrences of ONE query to the right'''
        # in reverse mode, num_lines is actually last_line, so we avoid filling the last line
        new_loc = find_room(q, num_cols, num_lines, reverse=True) # let's find the first avail position and unfold from there
        if new_loc == (0,0): return
        i, j = new_loc
        q0 = int(q[0][:q[0].index('_')])
        for n in range(0,k): # let's find all occurrences of q[0] and fill from new_loc
            loc = find_q(q, num_cols, num_lines, reverse=True)
            # reverse otherwise it always picks the same one
            # let's move the item we found to available location
            if (loc[0] >= i) and (loc[1] >= j): return # if true, we are moving moved q's, so exit, no more room
            l[loc[0]][loc[1]] = 0
            l[i][j] = q[0]
            # let's start from location we just filled and find next spot available
            while l[i][j] != 0:
                if (i + 1) < num_lines: i += 1
                elif j > q0:
                    i,j = 0, j-1
                else:
                    print('\033[95m' + '\033[1m' + "WE CAN'T SHIFT ALL ", q, '\033[0m')
                    return
                    if j == 0: print("ERROR ERROR ERROR in shifting right", q, q[0], q[1], num_cols)
        print('\033[93m' + '\033[1m' + "WE MOVED ", q, '\033[0m')
        check_correct(l)
        print_operations([len(l), l])
        pass



    def remove_last_line_while_pushing_right(queries):
        '''This tries to remove the last line by distributing its queries to previous lines BUT first we push
            to the right, all the queries that are bigger than the ones listed in last line, to make space'''
        # now try to pull as many higher values back to the right
        queries = sorted(queries, key=lambda q: int(q[0][:q[0].index('_')]) + q[1] - 1, reverse=True)
        print(queries)
        num_cols = len(l[0])
        last_line_number = len(l) - 1
        last_line = l[last_line_number]
        list_q = sorted([i for i in last_line if i != 0], reverse = True)
        for q in queries:
            if q[0] in list_q: print('\033[95m' + '\033[1m' + "WE'RE MOVING ", q, '\033[0m')
            while q[0] in list_q: # move last line values FIRST (since others are rightfully placed already)
                #loc = find_q(q, num_cols, last_line_number)
                new_loc = find_room(q, num_cols, last_line_number, reverse = True)
                if new_loc != (0, 0):
                    if new_loc[1] == 0: print("ERROR ERROR ERROR in finding room", q, q[0], q[1], num_cols)
                    l[new_loc[0]][new_loc[1]] = q[0]
                    list_q.pop(list_q.index(q[0]))
                    l[last_line_number][l[last_line_number].index(q[0])] = 0
                else:
                    print('\033[95m' + '\033[1m' + "We can't clear ", q, '\033[0m')
                    return False
            if list_q.count(0) != len(list_q):
                shift_right(q, num_cols, last_line_number)
                #print("WE HAVE SHIFTED ", q)
            else: break

        if last_line.count(0) == len(l[0]):  # we have successfully moved all queries from this line
            print('\033[95m' + '\033[1m' + "LINE IS GOING TO BE REMOVED NOW" + '\033[0m')
            check_correct(l)
            print_operations([len(l), l])
            l.pop(-1)  # remove last line
            return True
        else:
            return False

    def strategy1(queries):
        '''This tries to remove the last lines after all queries have been pushed into l by push_latest.
            It returns the max, but not optimal, number lines necessary.'''
        failure = push_latest()
        queries = sorted(queries, key=lambda q: int(q[0][:q[0].index('_')]) + q[1] - 1, reverse=True)  # start with ones that can start latest
        if _print_full_matrix:
            check_correct(l)
            print_operations([len(l), l])

        # at this point, we know the MAXIMUM number of lines, len(l)
        # we must test if we have taken too many lines, ie unused timeslots

        num_cols = len(l[0])
        queries = sorted(queries, key=lambda q: int(q[0][:q[0].index('_')]) + q[1] - 1, reverse=True) # if two queries start same time, start with the one with biggest alloc
        while remove_last_line() is True: pass

        # now we 'suck' the low q's to the left to open spaces for operations left on last line we couldn't move
        queries = sorted(queries, key=lambda q: [int(q[0][:q[0].index('_')]),q[1]]) # now we start with operations that can start early
        print(queries)
        num_lines = len(l)
        shift_left(num_cols, num_lines) # shift all values to the left, and try again removing lines

        while remove_last_line() is True: pass

        if _print_full_matrix:
            check_correct(l)
            print_operations([len(l), l])


### MAKE SURE THIS SORTING IS OK

        while remove_last_line_while_pushing_right(queries) is True: pass

        if _print_full_matrix:
            check_correct(l)
            print_operations([len(l), l])

    format(queries) # brings all queries starting at 1 since they could have big values = lots of zeroes at beginning

    l = [[]]  # every line corresponds to a 'new CPU', ie we need one more instruction/s to fit all queries
    # sorted(queries, key= lambda q: q[1]) #let's start with lower ones, fill lists, and see if we can add next ones
    #list_of_queries = [queries[i][0] for i in range(len(queries))]
    queries = sorted(queries, key=lambda q: q[0] + q[1] - 1, reverse=True)  # start with ones that can start latest
    print(queries)
    _print_debug = False
    _print_full_matrix = True

    rename_queries(queries) # be careful, now the queries are modified, with _123 added to it
    strategy1(queries)

    return len(l),l

process_all = -9;  # if neg, process only that number, otherwise all

if __name__ == '__main__':

    HEADER = '\033[95m' # purple
    OKBLUE = '\033[94m' # blue
    OKGREEN = '\033[92m' # green
    WARNING = '\033[93m'  # orange
    FAIL = '\033[91m'  # red
    ENDC = '\033[0m'  # must use it to stop coloring
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    input_file = open("Analytical Queries test input.txt")

    queries_total = int(input_file.readline().strip())
    print(queries_total)

    def check_correct(result):  # LET'S MAKE SURE WE DIDN'T LOSE ANY OPERATION
        ll = []
        for line in result: ll += line # let's flatten ll to ease counting occurrences of q's
        llo = sorted([i for i in ll if i != 0]) # let's get rid of zeros right here
        no_error = True
        q_list = []
        while True:
            c = llo.count(llo[0])
            if c != k:
                print('\033[91m' + '\033[1m' "FAILURE - WE LOST OPERATIONS FOR : " + llo[0]+ " only " + str(c)
                      + " occurrences instead of k = " + str(k) + '\033[0m')
                no_error = False
                q_list += [[llo[0]]]
            llo = llo[c:]
            if llo == []: break

        if no_error:
            print('\033[92m' + "SUCCESS - NO MISSING OPERATIONS" + '\033[0m')
        #else:
        #    print('\033[91m' + '\033[1m' "FAILURE - WRONG NUMBER OF OPERATIONS: " + str(q_list) + '\033[0m')

    def print_operations(result):
        print("Number of needed cycles/s:", colored(result[0], 'yellow'), "expected", colored(cycles, 'yellow'),
              '\033[92m' + "SUCCESS" + '\033[0m' if result[0] == cycles else colored("FAILURE", 'red'))
        print_aligned([i for i in range(len(result[1][0]))], colored=True)
        print_aligned([-3 * len(result[1][0])])
        for line in result[1]:
            print_aligned(line)
        print('\n' + '###' * len(result[1][0]) + '\n')

    for q_itr in range(queries_total):


        n, k, cycles = input_list = list(map(int, (input_file.readline().strip().split())))
        if process_all < 0 and q_itr == -process_all: print(n, k, cycles)
        queries = []

        for _ in range(n):
                input_list = list(map(int, (input_file.readline().strip().split())))
                queries.append(input_list)

        if process_all > 0 or q_itr == -process_all:

            result = solve(queries)

            correct = check_correct(result[1])

            print(sorted(queries, key=lambda q: q[1]))
            print_operations(result)

    input_file.close()

''' Use the following when submitting code, hackerrank didn't seem to bother to provide it
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        n,k = list(map(int, input().rstrip().split()))

        queries = []

        for _ in range(n):
            queries.append(list(map(int, input().rstrip().split())))

        result = solve(queries)

        fptr.write(str(result) + '\n')

    fptr.close()
'''
