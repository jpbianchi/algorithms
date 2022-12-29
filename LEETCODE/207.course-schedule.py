# https://leetcode.com/problems/course-schedule
# @lc app=leetcode id=207 lang=python3
#
# [207] Course Schedule
#
# Tags
# depth-first-search | breadth-first-search | graph | topological-sort

# Companies
# apple | uber | yelp | zenefits

# There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
# Return true if you can finish all courses. Otherwise, return false.

# Example 1:

# Input: numCourses = 2, prerequisites = [[1,0]]
# Output: true
# Explanation: There are a total of 2 courses to take. 
# To take course 1 you should have finished course 0. So it is possible.
# Example 2:

# Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
# Output: false
# Explanation: There are a total of 2 courses to take. 
# To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
 
# Constraints:

# 1 <= numCourses <= 2000
# 0 <= prerequisites.length <= 5000
# prerequisites[i].length == 2
# 0 <= ai, bi < numCourses
# All the pairs prerequisites[i] are unique.

from typing import List 
# @lc code=start
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """ If we create a graph, it should be acyclical for a schedule to exist
            Let's just follow a path from any node with DFS.
            If we end up with an already visited node, there's a cycle.
            This solution does not use topological ordering, so no need of numCourses
            Beats 65% cpu, 65% memory
        """
        # let's create the adjency list
        adjL = {}  # course:[prerequisites]
        
        for course, prereq in prerequisites:
            adjL.setdefault(course,[]).append(prereq)
            
        courses = list(adjL.keys())
        visited = []
        
        def DFS(c):
 
            if c not in adjL:
                return False  # no cycle found/possible for this path
            
            if c in visited:
                return True  # found cycle            
            
            # we will follow all paths from c, so we can flag it as visited
            # so that we can detect a cycle if we end up on c again
            
            visited.append(c)

            for pre in adjL[c]:
                
                if DFS(pre):
                    return True
            
            # here, none of the edges from this course led back to it, 
            # so we can remove it since a cycle would use one of those edges
            # it allows for the first test 'if c not in adjL' to work since
            # a new search may end up on a node that was already processed
            del adjL[c]            

            return False
                
        while courses:
                     
            if DFS(courses[-1]):    # take last one, it's faster to pop 
                return False        # found a cycle 
            
            courses.pop()
        
        return True


# @lc code=end

assert Solution().canFinish(2, [[1,0],[0,1]]) is False
assert Solution().canFinish(4, [[3,0],[2,0],[1,2]]) is True
assert Solution().canFinish(4, [[3,0],[2,0],[1,2],[0,1]]) is False
assert Solution().canFinish(6, [[3,0],[0,1],[1,2],[1,4],[4,5]]) is True
assert Solution().canFinish(6, [[3,0],[0,1],[1,2],[1,4],[4,5],[5,3]]) is False

print("TESTS PASSED")
