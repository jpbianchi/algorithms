#
# @lc app=leetcode id=200 lang=python3
#
# [200] Number of Islands
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (56.52%)	18367	408
# Tags
# depth-first-search | breadth-first-search | union-find

# Companies
# amazon | facebook | google | microsoft | zenefits

# Given an m x n 2D binary grid grid which represents a map of '1's 
# (land) and '0's (water), return the number of islands.

# An island is surrounded by water and is formed by connecting 
# adjacent lands horizontally or vertically. You may assume all 
# four edges of the grid are all surrounded by water.

# Example 1:

# Input: grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]
# Output: 1
# Example 2:

# Input: grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# Output: 3
 
# Constraints:

# m == grid.length
# n == grid[i].length
# 1 <= m, n <= 300
# grid[i][j] is '0' or '1'.


from typing import List
import numpy as np
# @lc code=start
class Solution:
    """ This is connected components problem.  
        We simply scan the grid and if we find a node that is not visited 
        and is a land, we mark it with a number incrementally, except if
        it's connected to a cell above with a lower number.
    """
    def numIslands1(self, grid: List[List[str]]) -> int:
        """ This solution works but it is not optimal.
            I beat only 50% in cpu, and 5% in memory
        """
        nb_islands = 0
        nb_islands_merged = 0 
        # let's pad it so we don't have to worry about borders with i-1, j-1
        # let's try to save memory by reusing grid
        grid = np.pad(np.array(grid, dtype=int), 1, 'constant', constant_values=0)
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i,j] == 1:
                    
                    # beginning of a new island (until we find a connection)
                    if grid[i-1,j] == 0 and grid[i,j-1] == 0:
                        nb_islands+=1
                        grid[i,j] = nb_islands
                        continue
                    
                     # the cell touches a previous island on left OR above, but not both
                    if (grid[i-1,j] == 0) ^ (grid[i,j-1] == 0):
                        # attach to the only island there is
                        grid[i,j] = max(grid[i,j-1], grid[i-1,j])
                        continue
                   
                    # the cell touches both islands on the right and above, what do we do?
                    if grid[i-1,j] == grid[i,j-1]:
                        # no merge if it's the same island 
                        grid[i,j] = grid[i-1,j]
                        continue

                    # take smallest island number
                    # we can't just decrement nb_islands because this pattern can repeat
                    # when two islands touch on several cells in a row
                    min_nb = min(grid[i,j-1],grid[i-1,j])
                    
                    # cell attaches to the smallest island it can find, or none
                    grid[i,j] = min_nb

                    # we connect the two islands
                    # change other island nb to the smallest one
                    grid[grid == max(grid[i,j-1],grid[i-1,j])] = min_nb
                    nb_islands_merged += 1
                
                                    
        print(grid[1:-1,1:-1])
        return nb_islands - nb_islands_merged
    
    def numIslands(self, grid: List[List[str]]) -> int:
        """ If you think about it, an island is like a connected component.
            We can use a DFS to find all the connected components in the grid.
            Imagine we start on the top left corner and 'go down' the graph.
            We need to make sure that we explore all 4 directions in case an island
            'goes up' or 'goes left'. 
            We will mark every visited node to avoid doing DFS again on it.
            Now, we beat 84% in cpu but still 5% in memory ?? 
            I don't get why since we just modify the grid, except for recursive calls but data
            passed is minimal to say the least.
        """

        def dfs(i,j):
            # let's mark the node as visited with its island number
            grid[i][j] = nb_islands
            
            # propagate nb_islands in all 4 directions
            if i > 0 and grid[i-1][j] == '1':
                dfs(i-1,j)
                
            if i < len(grid)-1 and grid[i+1][j] == '1':
                dfs(i+1,j)
                
            if j > 0 and grid[i][j-1] == '1':
                dfs(i,j-1)
                
            if j < len(grid[0])-1 and grid[i][j+1] == '1':
                dfs(i,j+1)
                
        nb_islands = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    # we found an island, let's explore it
                    nb_islands += 1
                    dfs(i,j)
                    
        print(np.array(grid))
        return nb_islands
        
        
# @lc code=end
grid = [["1","1","1","1","1","0","1","1","1","1"],
        ["1","0","1","0","1","1","1","1","1","1"],
        ["0","1","1","1","0","1","1","1","1","1"],
        ["1","1","0","1","1","0","0","0","0","1"],
        ["1","0","1","0","1","0","0","1","0","1"],
        ["1","0","0","1","1","1","0","1","0","0"],
        ["0","0","1","0","0","1","1","1","1","0"],
        ["1","0","1","1","1","0","0","1","1","1"],
        ["1","1","1","1","1","1","1","1","0","1"],
        ["1","0","1","1","1","1","1","1","1","0"]]
print(np.array(grid, dtype=int))
assert Solution().numIslands(grid) == 2


grid = [["1","0","1","1","1"],
        ["1","0","1","0","1"],
        ["1","1","1","0","1"]]
print(np.array(grid, dtype=int))
assert Solution().numIslands(grid) == 1

grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]  ]
assert Solution().numIslands(grid) == 3

grid = [["1","1","1"],
        ["0","1","0"],
        ["1","1","1"]]
print(np.array(grid, dtype=int))
assert Solution().numIslands(grid) == 1

grid = [["1","1","1","0"],
        ["0","1","0","0"],
        ["1","1","1","0"],
        ["1","0","0","0"]]
print(np.array(grid, dtype=int))
assert Solution().numIslands(grid) == 1

print("TESTS PASSED")

