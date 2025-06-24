#!/bin/python3

# https://www.hackerrank.com/challenges/common-child/problem
# see https://en.wikipedia.org/wiki/Longest_common_subsequence_problem for big hint
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm

"""TRY TO IMPROVE SPEED BY WRITING C LIBRARY TO ACCESS MATRICES
# MAYBE BY WRITING A LIBRARY WHO DOES ONLY THAT, I'LL BE ABLE TO
# GO QUICKER FOR VERY LARGE STRINGS"""

import multiprocessing, random


def common_child(s1, s2):
    global breakpoint_stop

    common_string = s1 + '\n' + s2
    len_s = len(s1)
    tree = {0}  # initialize so we can always call max, even if the search gives nada

    def find_common2(i, j, level=1):
        """ Works for short words, otherwise takes much too long because of recursivity"""
        nonlocal tree
        if i >= len_s or j >= len_s:  # one index reached the end, we're done
            return  # we leave, there's nothing to do anymore, no lower level from here
        else:
            if s1[i] == s2[j]:  # we found a common starting character, hence a new branch leading to new level
                tree.add(level)
                find_common2(i+1, j+1, level+1)
            else:
                # there are two scenarii and we must test both
                find_common2(i, j + 1, level)
                find_common2(i + 1, j, level)

    def find_common1(i, j):
        """ We don't need to save more than 2 line of the matrix
            But we saved all the possible solutions and the lists grow exponentially
            even if we keep only the last 2.  """

        matrix = []
        len_s = len(s1)
        print(len_s)
        limit = 20
        for i in range(0,min(limit, len_s)):
            matrix.append([])
            m_i = min(i, 1)  # we always work on last line because we store only 2 lines max
            for j in range(0,len_s):
                matrix[m_i].append([s1[j]] if s1[j] == s2[i] else [])
                if s1[j] == s2[i]:
                    matrix_to_append = matrix[max(m_i - 1, 0)][max(j - 1, 0)]
                    if len(matrix_to_append):
                        matrix[m_i][j] = [pair+s2[i] for pair in matrix_to_append]
                else:
                    combo_set = set()
                    if j>=1: combo_set.update(set(matrix[m_i][j-1]))  # eliminate identical elements
                    if i>=1: combo_set.update(set(matrix[0][j]))   # eliminate identical elements
                    matrix[m_i][j] = list(combo_set) if len(combo_set) > 0 else []
            if len(matrix) == 2: # remove first line, useless now, the info has been encoded in next line
                del(matrix[0])

        #for i in range(len_s): print(matrix[i])
        # print(sum([len(l) for l in matrix[1]]))
        all_combos = matrix[0][len_s-1]
        maxx = max(map(len, all_combos)) if len(all_combos) else 0

        return maxx  #, [x for x in all_combos if len(x) == maxx]

    def find_common4():
        """ We don't need to save more than 2 line of the matrix.
            Here, at each step, we store only the LCS at every step
            to avoid exponential growth of the list holding all the
            possibilities in previous versions.
            We add a row and column of zeros for ease."""

        len_s = len(s1)
        matrix = [[0] * (len_s + 1)]  # first line full of zeros to avoid testing indices
        for i in range(0,len_s):
            matrix.append([0])  # let's fill the first column with zeros for same reason
            for j in range(0, len_s):  # in the matrix, we are at i+1,j+1
                if s1[j] == s2[i]: matrix[1].append(matrix[0][j] + 1) # value in [0][j] holds the lcs
                else: matrix[1].append(max(matrix[1][j], matrix[0][j+1]))  # max of lcs of 2 previous str
            del (matrix[0]) # remove first line, useless now, the info has been encoded in next line

        return matrix[0][len_s]

    def find_common():
        """ We don't need to save more than 2 line of the matrix.
            Here, at each step, we store only the LCS at every step
            to avoid exponential growth of the list holding all the
            possibilities in previous versions.
            We add a row and column of zeros for ease.
            To save time and space, let's use always the same 2 lines,
            ie avoid creating and deleting matrix rows.
            We saved 50% compared to creating new row and deleting one at every i.
            Apparently, max() uses an iterator protocol, so it is slower.
            Multiply that by len_s ** 2, and it makes a difference.
            I tried using a Numpy array, it is MUCH slower."""

        """ NOW TRY TO WRITE C LIBRARY TO CREATE AN ARRAY AND GO THROUGH IT
            TO SEE IF I CAN'T MAKE IT EVEN FASTER BY LIMITING THE NUMBER OF
            FUNCTIONS AVAILABLE TO creation, access, len().
            IF ANYTHING IT WILL BE A GREAT EXERCISE
        """

        len_s = len(s1)
        matrix = [[0] * (len_s + 1)] + [[0] * (len_s + 1)]  # first line full of zeros to avoid testing indices
        m_1 = 0
        for i in range(0,len_s):
            m_1 = 1 - m_1
            for j in range(0, len_s):  # in the matrix, we are at i+1,j+1
                if s1[j] == s2[i]: matrix[m_1][j+1] = matrix[1 - m_1][j] + 1 # value in [0][j] holds the lcs
                #else: matrix[m_1][j+1] = max(matrix[m_1][j], matrix[m_0][j+1])  # max of lcs of 2 previous str
                # I gained 20% simply by rewriting the above line like this
                elif matrix[m_1][j] > matrix[1 - m_1][j+1]: matrix[m_1][j+1] = matrix[m_1][j]
                else: matrix[m_1][j+1] = matrix[1 - m_1][j+1]
        return matrix[m_1][len_s]

    maxx = find_common()
    print(common_string, 'Result:  ', sep='\n', end='')
    return maxx


if __name__ == '__main__':

    INPUT_FILE = "Common Child tests.txt"
    fin = open(INPUT_FILE, 'r')
    import time

    def timer(func):
        """Print the runtime of the decorated function"""

        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()  # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()  # 2
            run_time = end_time - start_time  # 3
            print(f"Finished {func.__name__!r} in {run_time:.4f} secs\n")
            return value

        return wrapper_timer

    @timer
    def get_result():

        s1 = fin.readline().strip()
        s2 = fin.readline().strip()

        shouldbe = fin.readline()  # correct answer

        print(common_child(s1, s2), shouldbe, sep='\n')

    p = multiprocessing.Process(target=get_result, name="get_result", args=(10,))
    #p.start()  # we want to stop execution when recursion takes too long

    def execute(n):
        for i in range(n):
            #time.sleep(2)
            get_result()
            if p.is_alive(): p.terminate

    execute(8)

    fin.close()

    n = 10
    while n < 5:

        s1 = 'A' + ''.join(map(chr, [random.randint(ord('A'), ord('Z')) for k in range(n)]))
        s2 = 'A' + ''.join(map(chr, [random.randint(ord('A'), ord('Z')) for k in range(n)]))

        start_time = time.perf_counter()

        lcs = common_child(s1, s2)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3

        print(f"{n} char : in {run_time:.4f} secs\n")

        n = int(n * 1.3)

