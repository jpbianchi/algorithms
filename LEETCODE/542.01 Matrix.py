# https://leetcode.com/problems/01-matrix/
#
# Given an m x n binary matrix mat, return the distance of the nearest 0 for 
# each cell. 
# 
#  The distance between two adjacent cells is 1. 
# 
#  
#  Example 1: 
# Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
# Output: [[0,0,0],[0,1,0],[0,0,0]]
#  
# 
#  Example 2: 
# Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
# Output: [[0,0,0],[0,1,0],[1,2,1]]
#  
#  Constraints: 
# 
#  m == mat.length 
#  n == mat[i].length 
#  1 <= m, n <= 10⁴ 
#  1 <= m * n <= 10⁴ 
#  mat[i][j] is either 0 or 1. 
#  There is at least one 0 in mat. 
#  
# 
#  Related Topics Array Dynamic Programming Breadth-First Search Matrix 👍 6162 
# 👎 301

from typing import List
# leetcode submit region begin(Prohibit modification and deletion)
import numpy as np
from collections import deque

class Solution:
    """ I solve this problem with dynamic programming.
        I set the value for all 1's surrouned by 1, to 2
        then I set all 2's surrounded by 2 to 3 etc
        In the final solution, I found an original way to use
        numpy.vectorize to avoid testing the surrounding cells one by one.  
    """
    
    def updateMatrix1(self, mat: List[List[int]]) -> List[List[int]]:

        if len(mat) == 1 and mat[0][-1] == 0 and sum(mat[0][:-1]) == len(mat[0])-1:
            # in case we have 1 1 1 1 1 ... 1 1 0, this method would take too long
            return [list(range(len(mat[0])-1, -1, -1))]

        print(np.array(mat))

        npmat = np.array(mat)
        if npmat.sum() == 0:  # only zeroes
            return mat

        m,n = npmat.shape
        npmat = np.pad(npmat, 1,
                       mode='constant',
                       constant_values=m*n+1) # make sure constant > 1 if m=n=1, no path will ever be equal to m*n+1
        npwx, npwy = np.where(npmat == 1)  # gets 1's coords
        # because of padding, there are always two coordinates
        mat='a'  # save memory if matrix is very big

        coords = deque(zip(npwx, npwy))  # deque for fast removal

        def processBorder(coords, n):
            ''' Finds all the 1's with a 0 neighbor, set the rest to 2
                then all the 2's with a 1 neighbor, set the rest to 3 etc
            '''
            for x,y in coords.copy():
                if n in [npmat[x-1,y], npmat[x+1,y],
                         npmat[x,y-1], npmat[x,y+1]]:
                    coords.remove((x,y))
            # now we can set all the rest to n+2 at once
            # to avoid looping through all of them
            # one test case has a thousand 1 and 1 zero
            if coords:
                npcoords = np.array(coords)
                npmat[npcoords[:,0], npcoords[:,1]] = n + 2
            return

        # I could do recursion but it will fill the stack
        # not necessary to simplify the thinking here either
        n = 0
        while coords:
            processBorder(coords, n)
            n += 1

        print('')
        print(npmat[1:-1,1:-1])
        return npmat[1:-1,1:-1].tolist() # unpad


    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        """ Let's try to vectorize the previous method
            I went from beating 5% to 85% !!! but memory still at 5%
        """
        if len(mat) == 1 and mat[0][-1] == 0 and sum(mat[0][:-1]) == len(mat[0]) - 1:
            # in case we have 1 1 1 1 1 ... 1 1 0, this method would take too long
            return [list(range(len(mat[0]) - 1, -1, -1))]

        npmat = np.array(mat)
        m, n = npmat.shape

        print(npmat)
        if npmat.sum() == 0:  # only zeroes
            return mat
        mat = 'a'  # save memory if matrix is very big

        # make sure constant > 1 if m=n=1, no path will ever be equal to m*n+1
        npmat = np.pad(npmat, 1, mode='constant',
                       constant_values=m*n+1) # so we can rotate and not mess with getBorder

        def getBorder(a,b,c,d,e,n):
            """ Finds all the cells = n surrounded by others = n
                So, for instance, all the 1 surrounded by 1 are the next
                border that must be set to 2 etc
            """
            if a == n and min(b, c, d, e) == n:
                return n+1
            else:
                return a

        gB = np.vectorize(getBorder)

        n = 1
        while True:
            npmati1j = np.roll(npmat,1,0)
            npmati_1j = np.roll(npmat,-1,0)
            npmatij1 = np.roll(npmat,1,1)
            npmatij_1 = np.roll(npmat,-1,1)

            npmat = gB(npmat, npmati1j, npmati_1j, npmatij1, npmatij_1, n)
            if npmat[1:-1,1:-1].max() == n:  # nothing was modified = we're done
                break
            n += 1
            print(npmat[1:-1,1:-1])

        return npmat[1:-1,1:-1].tolist()


# leetcode submit region end(Prohibit modification and deletion)
print('\n')

assert Solution().updateMatrix([[0],[0],[0],[0],[0]]) == [[0],[0],[0],[0],[0]]
assert Solution().updateMatrix([[0,0,0,1],[0,0,1,1],[0,1,1,1],[0,1,1,1]]) == [[0,0,0,1], [0,0,1,2], [0 ,1,2,3], [0,1,2,3]]
assert Solution().updateMatrix([[0,0,0],[0,1,0],[0,0,0]]) == [[0,0,0],[0,1,0],[0,0,0]]
assert Solution().updateMatrix([[0,0,0],[0,1,0],[1,1,1]]) == [[0,0,0],[0,1,0],[1,2,1]]
assert Solution().updateMatrix([[1,1,1,1,1,1,1,1,1,1,0]]) == [[10,9,8,7,6,5,4,3,2,1,0]]

# the following case is where my method doesn't shine compared to nested for loops
# since it requires 9999 iterations
assert Solution().updateMatrix([[1]*9999 + [0]]) == [list(range(9999,-1,-1))]

print('TESTS PASSED')
