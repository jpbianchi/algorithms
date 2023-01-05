# https://leetcode.com/problems/merge-intervals/
# @lc app=leetcode id=56 lang=python3
#
# [56] Merge Intervals
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (46.03%)	17504	609
# Tags
# array | sort

# Companies
# bloomberg | facebook | google | linkedin | microsoft | twitter | yelp

# Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

# Example 1:

# Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
# Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
# Example 2:

# Input: intervals = [[1,4],[4,5]]
# Output: [[1,5]]
# Explanation: Intervals [1,4] and [4,5] are considered overlapping.
 
# Constraints:

# 1 <= intervals.length <= 104
# intervals[i].length == 2
# 0 <= starti <= endi <= 104
from typing import List
from collections import deque
# @lc code=start
class Solution:
    def merge1(self, intervals: List[List[int]]) -> List[List[int]]:
        """ If we order the intervals by their start time, then we can merge
            the intervals in one pass.
            The algorithm is simple: we start from the first interval and
            merge all the overlapping intervals. We do this until we find a
            non-overlapping interval. Then we repeat the process starting from
            the new interval.
            Beats 45% in cpu
        """
        intervals = deque(sorted(intervals))
        ans = []
        s,e = intervals.popleft()
        while intervals:
            
            nexts, nexte = intervals.popleft() 
            if nexts <= e:
                e = max(e, nexte)
                continue
            ans.append([s,e])

            s,e = nexts, nexte 
            
        return ans + [[s,e]]
    
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """ Let's try to remove the deque and use a list instead
            No improvement but the faster algorithms do exactly the same
            as this.  Leetcode metrics are not reliable.  
        """
        intervals.sort()
        ans = []
        s,e = intervals[0]
        for nexts,nexte in intervals[1:]:
            
            if nexts <= e:
                e = max(e, nexte)
                continue
            ans.append([s,e])

            s,e = nexts, nexte 
            
        return ans + [[s,e]]
            
# @lc code=end
assert Solution().merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert Solution().merge([[1,4],[4,5]]) == [[1,5]]
assert Solution().merge([[1,3],[2,6],[4,5],[3,4]]) == [[1,6]]
assert Solution().merge([[1,3],[2,6],[4,5],[3,12]]) == [[1,12]]

print("TESTS PASSED")

