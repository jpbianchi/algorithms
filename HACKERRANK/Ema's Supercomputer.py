#!/bin/python3

# https://www.hackerrank.com/challenges/two-pluses/problem


def twopluses(grid):

    from operator import itemgetter

    def sizeok(x, y, size, rows, cols):
        """True if star of size can be grown at x,y"""
        if (y + size) >= cols or (y - size) < 0 or (x + size) >= rows or (x - size) < 0: return False
        if (grid[x][y + size] == 'G' and grid[x][y - size] == 'G' and
                grid[x + size][y] == 'G' and grid[x - size][y] == 'G'):
            return True

    def list_stars():
        rows = len(grid)
        cols = len(grid[0])
        stars_dict = {}
        stars_list = []
        for i in range(rows):
            for j in range(cols):
                for side in range(0, 8):  # problem constraint
                    if sizeok(i, j, side, rows, cols):
                        size = side * 2 + 1
                        stars_dict.setdefault(size, []).append([i, j])
                        stars_list += [[i, j, size]]
                    else:
                        break
        return stars_dict, stars_list

    def star_dist(star1, star2):
        """ True is both stars can be placed on grid without colliding.
            star is a list with center coordinates and size (full length) of arms"""
        x1, y1, size1 = star1
        x2, y2, size2 = star2
        dist = abs(x2 - x1) + abs(y2 - y1)
        delta_min = min(abs(x2-x1), abs(y2-y1))
        sigma1 = size1 // 2  # sigma = length of arm of star
        sigma2 = size2 // 2
        if delta_min == 0:  # x's or y's on same line
            return dist > (sigma1 + sigma2)
        # if not on same line, stars can 'mix', so, after careful analysis, the condition for not colliding is
        return ((abs(y2-y1) > sigma1) or (abs(x2-x1) > sigma2)) and \
                ((abs(y2 - y1) > sigma2) or (abs(x2 - x1) > sigma1))
        # it is derived by expressing that the horizontal bar does not cross the other's vertical bar, and recipr.

    ds, ls = list_stars()
    # ds[1] = ds[1][1]  # let's keep only 1 for now, otherwise we get the list of all the G boxes
    for k, v in ds.items():  # let's use the dictionary to count how many of each star there are
        ds[k] = len(v)
    print(ds)
    # now we sort the stars to put the bigger first, then we look for the first combo that doesn't collide
    # max_size = max(ls, key=itemgetter(2))[2]
    ls = sorted(ls, key=itemgetter(2), reverse=True)
    print(ls)
    num_stars = len(ls)
    max_mult = 0
    for i in range(num_stars):
        for j in range(i, num_stars):
            if star_dist(ls[i], ls[j]):
                mult = (2 * ls[i][2] - 1) * (2 * ls[j][2] - 1)
                if mult > max_mult: print(ls[i], ls[j], "prod =", mult)
                max_mult = max(max_mult, mult)
    return max_mult


if __name__ == '__main__':

    INPUT_FILE = "Ema's Supercomputer test.txt"
    fin = open(INPUT_FILE, 'r')

    def print_grid():
        nm = fin.readline().split()

        n = int(nm[0])

        grid = []

        for _ in range(n):
            grid_item = list(fin.readline().split()[0])
            print(grid_item)
            grid.append(grid_item)

        fin.readline()
        print(twopluses(grid))


    print_grid()
    print_grid()
    print_grid()
    print_grid()
    print_grid()
    fin.close()

# SOME EXAMPLES
#   0 1 2 3 4 5 6 7 8 91011
#   ________________________
# 0|O O O O O O O O O O O O
# 1|O   O O               O
# 2|O   O O               O
# 3|O O O O O O O O O O O O
# 4|O O O O O O O O O O O O
# 5|O O O O O O O O O O O O
# 6|O O O O O O O O O O O O
# 7|O   O O               O
# 8|O   O O               O
# 9|O   O O               O
#10|O O O O O O O O O O O O
#11|O   O O               O
#[[3, 3, 7], [4, 3, 7], [5, 3, 7], [6, 3, 7],
#[3, 2, 5], [3, 3, 5], [4, 2, 5], [4, 3, 5], [5, 2, 5], [5, 3, 5],
#[6, 2, 5], [6, 3, 5],
#[3, 2, 3], [3, 3, 3], [4, 1, 3], [4, 2, 3], [4, 3, 3], [4, 4, 3],
#[4, 5, 3], [4, 6, 3], [4, 7, 3], [4, 8, 3], [4, 9, 3], [4, 10, 3],
#[5, 1, 3], [5, 2, 3], [5, 3, 3], [5, 4, 3], [5, 5, 3], [5, 6, 3],
#[5, 7, 3], [5, 8, 3], [5, 9, 3], [5, 10, 3], [6, 2, 3], [6, 3, 3],
#[10, 2, 3], [10, 3, 3],
#[3, 3, 7] [4, 7, 3]

#   0 1 2 3 4 5 6 7 8 910 1 2 3
#   __________________________
# 0[O O O O O O O O O O O O O O]
# 1[O O         O           O O]
# 2[O O         O           O O]
# 3[O O         O           O O]
# 4[O O 9 9 9 9 9 9 9 9 9 O O O]
# 5[O O O O O O 9 O O O O O O O]
# 6[O O O O O O 9 O O O O O O O]
# 7[O O O O O O 9 O O O O O O O]
# 8[O O         9           O O]
# 9[O O         O           O O]
#10[O O O O O O O O O O O O O O]
#11[O O         O           O O]
#12[O O         O           O O]
#13[O O O O O O O O O O O O O O]
#[6, 6, 13] [4, 1, 3] prod = 125
#[4, 6, 9] [10, 6, 7] prod = 221
#{1: 133, 3: 33, 5: 5, 7: 5, 9: 4, 11: 3, 13: 2}
#[[6, 6, 13], [7, 6, 13],
#[5, 6, 11], [6, 6, 11], [7, 6, 11],
#[4, 6, 9], [5, 6, 9], [6, 6, 9], [7, 6, 9],
#[4, 6, 7], [5, 6, 7], [6, 6, 7], [7, 6, 7], [10, 6, 7],
#[4, 6, 5], [5, 6, 5], [6, 6, 5], [7, 6, 5], [10, 6, 5], [4, 1, 3], [4, 6, 3], [4, 12, 3], [5, 1, 3], [5, 2, 3], [5, 3, 3], [5, 4, 3], [5, 5, 3], [5, 6, 3], [5, 7, 3], [5, 8, 3], [5, 9, 3], [5, 10, 3], [5, 11, 3], [5, 12, 3], [6, 1, 3], [6, 2, 3], [6, 3, 3], [6, 4, 3], [6, 5, 3], [6, 6, 3], [6, 7, 3], [6, 8, 3], [6, 9, 3], [6, 10, 3], [6, 11, 3], [6, 12, 3], [7, 1, 3], [7, 6, 3], [7, 12, 3], [10, 1, 3], [10, 6, 3], [10, 12, 3], [0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1], [0, 4, 1], [0, 5, 1], [0, 6, 1], [0, 7, 1], [0, 8, 1], [0, 9, 1], [0, 10, 1], [0, 11, 1], [0, 12, 1], [0, 13, 1], [1, 0, 1], [1, 1, 1], [1, 6, 1], [1, 12, 1], [1, 13, 1], [2, 0, 1], [2, 1, 1], [2, 6, 1], [2, 12, 1], [2, 13, 1], [3, 0, 1], [3, 1, 1], [3, 6, 1], [3, 12, 1], [3, 13, 1], [4, 0, 1], [4, 1, 1], [4, 2, 1], [4, 3, 1], [4, 4, 1], [4, 5, 1], [4, 6, 1], [4, 7, 1], [4, 8, 1], [4, 9, 1], [4, 10, 1], [4, 11, 1], [4, 12, 1], [4, 13, 1], [5, 0, 1], [5, 1, 1], [5, 2, 1], [5, 3, 1], [5, 4, 1], [5, 5, 1], [5, 6, 1], [5, 7, 1], [5, 8, 1], [5, 9, 1], [5, 10, 1], [5, 11, 1], [5, 12, 1], [5, 13, 1], [6, 0, 1], [6, 1, 1], [6, 2, 1], [6, 3, 1], [6, 4, 1], [6, 5, 1], [6, 6, 1], [6, 7, 1], [6, 8, 1], [6, 9, 1], [6, 10, 1], [6, 11, 1], [6, 12, 1], [6, 13, 1], [7, 0, 1], [7, 1, 1], [7, 2, 1], [7, 3, 1], [7, 4, 1], [7, 5, 1], [7, 6, 1], [7, 7, 1], [7, 8, 1], [7, 9, 1], [7, 10, 1], [7, 11, 1], [7, 12, 1], [7, 13, 1], [8, 0, 1], [8, 1, 1], [8, 6, 1], [8, 12, 1], [8, 13, 1], [9, 0, 1], [9, 1, 1], [9, 6, 1], [9, 12, 1], [9, 13, 1], [10, 0, 1], [10, 1, 1], [10, 2, 1], [10, 3, 1], [10, 4, 1], [10, 5, 1], [10, 6, 1], [10, 7, 1], [10, 8, 1], [10, 9, 1], [10, 10, 1], [10, 11, 1], [10, 12, 1], [10, 13, 1], [11, 0, 1], [11, 1, 1], [11, 6, 1], [11, 12, 1], [11, 13, 1], [12, 0, 1], [12, 1, 1], [12, 6, 1], [12, 12, 1], [12, 13, 1], [13, 0, 1], [13, 1, 1], [13, 2, 1], [13, 3, 1], [13, 4, 1], [13, 5, 1], [13, 6, 1], [13, 7, 1], [13, 8, 1], [13, 9, 1], [13, 10, 1], [13, 11, 1], [13, 12, 1], [13, 13, 1]]

#  0 1 2 3 4 5 6 7 8 9
# _____________________
#0[          O O   O O]
#1[O O O O O 9 O O 3 O]
#2[O O O O O 9 O 3 3 3]
#3[          9 O   3 O]
#4[          9 O   O O]
#5[O O 9 9 9 9 9 9 9 9]
#6[          9 O   O O]
#7[O O O O O 9 O O O O]
#8[          9 O   O O]
#9[O O O O O 9 O O O O]
#{1: 70, 3: 12, 5: 6, 7: 2, 9: 1}
#[[5, 5, 9],
#[5, 5, 7], [5, 6, 7],
#[2, 5, 5], [2, 6, 5], [5, 5, 5], [5, 6, 5], [7, 5, 5], [7, 6, 5],
#[1, 5, 3], [1, 6, 3], [1, 8, 3], [2, 5, 3], [2, 6, 3], [2, 8, 3], [5, 5, 3], [5, 6, 3], [5, 8, 3], [7, 5, 3], [7, 6, 3], [7, 8, 3],
#[0, 5, 1], [0, 6, 1], [0, 8, 1], [0, 9, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 3, 1], [1, 4, 1], [1, 5, 1], [1, 6, 1], [1, 7, 1], [1, 8, 1], [1, 9, 1], [2, 0, 1], [2, 1, 1], [2, 2, 1], [2, 3, 1], [2, 4, 1], [2, 5, 1], [2, 6, 1], [2, 7, 1], [2, 8, 1], [2, 9, 1], [3, 5, 1], [3, 6, 1], [3, 8, 1], [3, 9, 1], [4, 5, 1], [4, 6, 1], [4, 8, 1], [4, 9, 1], [5, 0, 1], [5, 1, 1], [5, 2, 1], [5, 3, 1], [5, 4, 1], [5, 5, 1], [5, 6, 1], [5, 7, 1], [5, 8, 1], [5, 9, 1], [6, 5, 1], [6, 6, 1], [6, 8, 1], [6, 9, 1], [7, 0, 1], [7, 1, 1], [7, 2, 1], [7, 3, 1], [7, 4, 1], [7, 5, 1], [7, 6, 1], [7, 7, 1], [7, 8, 1], [7, 9, 1], [8, 5, 1], [8, 6, 1], [8, 8, 1], [8, 9, 1], [9, 0, 1], [9, 1, 1], [9, 2, 1], [9, 3, 1], [9, 4, 1], [9, 5, 1], [9, 6, 1], [9, 7, 1], [9, 8, 1], [9, 9, 1]]
#81