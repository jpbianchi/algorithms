# https://leetcode.com/problems/rotting-oranges/
# @lc app=leetcode id=994 lang=python3
#
# [994] Rotting Oranges
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (52.64%)	9318	324
# Tags
# hash-table

# Companies
# Unknown

# You are given an m x n grid where each cell can have one of three values:

# 0 representing an empty cell,
# 1 representing a fresh orange, or
# 2 representing a rotten orange.
# Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

# Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

# Example 1:

# Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
# Output: 4
# Example 2:

# Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
# Output: -1
# Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.
# Example 3:

# Input: grid = [[0,2]]
# Output: 0
# Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.
 
# Constraints:

# m == grid.length
# n == grid[i].length
# 1 <= m, n <= 10
# grid[i][j] is 0, 1, or 2.
# @lc code=start
from typing import List
import numpy as np

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """ Run DFS and measure longest path
            It could be improved by truly simulating the rotting process, i.e.
            put in a queue all fresh oranges touching a rotten orange
            process them, ie remove them from the queue, and put in it 
            the next fresh oranges touching them
        """
        
        def dfs(i,j):
            
            def gokl(k,l):
                # we explore only if this path is shorter (a path from
                # another rotten orange may be shorter)
                # always explore a fresh orange
                if (grid[k][l] == 1) or (grid[i][j] + 1 < grid[k][l]):
                    # let's mark the next cell in advance because
                    # when we process it, we won't know where we came from
                    grid[k][l] = grid[i][j] + 1
                    
                    dfs(k,l)
            
            # propagate rotting in all 4 directions
            if (i > 0) and (grid[i-1][j] not in [0,2]): # skip empty cells or rotten oranges
                gokl(i-1,j)
                
            if (i < len(grid)-1) and (grid[i+1][j] not in [0,2]):
                gokl(i+1,j)
                
            if (j > 0) and (grid[i][j-1] not in [0,2]):
                gokl(i,j-1)
                
            if (j < len(grid[0])-1) and (grid[i][j+1] not in [0,2]):
                gokl(i,j+1)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    grid[i][j] = 3 # we reuse the grid to store path length, but we start at 3
                    # we found a rotten orange, let's spread the rot
                    dfs(i,j)
                    
        print(np.array(grid))
        # is there a fresh orange left?
        if any([1 in row for row in grid]):
            return -1;
        
        if sum([sum(row) for row in grid]) == 0:
            return 0;
        
        return max([max(row) for row in grid]) - 3
# @lc code=end

grid = [[2,1,0,2]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == 1

grid = [[0]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == 0

grid = [[0,2]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == 0

grid = [[2,1,1],[0,1,1],[1,0,1]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == -1

grid = [[2,1,1],[1,1,0],[0,1,1]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == 4

grid = [[1,2,1,1,1,1,2]]
print(np.array(grid))
assert Solution().orangesRotting(grid) == 2

print("TESTS PASSED")
