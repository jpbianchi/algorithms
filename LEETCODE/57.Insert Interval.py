# https://leetcode.com/problems/insert-interval
# You are given an array of non-overlapping intervals intervals where intervals[
# i] = [starti, endi] represent the start and the end of the iᵗʰ interval and 
# intervals is sorted in ascending order by starti. You are also given an interval 
# newInterval = [start, end] that represents the start and end of another interval. 
# 
#  Insert newInterval into intervals such that intervals is still sorted in 
# ascending order by starti and intervals still does not have any overlapping 
# intervals (merge overlapping intervals if necessary). 
# 
#  Return intervals after the insertion. 
# 
#  
#  Example 1: 
# Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
# Output: [[1,5],[6,9]]
#  
# 
#  Example 2: 
# Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
# Output: [[1,2],[3,10],[12,16]]
# Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
#  
#  Constraints: 
# 
#  0 <= intervals.length <= 10⁴ 
#  intervals[i].length == 2 
#  0 <= starti <= endi <= 10⁵ 
#  intervals is sorted by starti in ascending order. 
#  newInterval.length == 2 
#  0 <= start <= end <= 10⁵ 
#  
#  Related Topics Array 👍 6399 👎 449

from typing import List
from collections import deque
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def insert1(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:

        if not intervals:
            return [newInterval]

        start, end = newInterval
        deque_intervals = deque(intervals)
        len_deque = len(intervals)
        rotations = 0
        # case when interval must be added at the end
        if start > deque_intervals[-1][1]:
            intervals.append(newInterval)
            return intervals
        # so now we know the newInterval has to be inserted/merged inside the list
        # so the rotations will not run forever for sure # TODO except if merge with the last...
        while True:
            s,e = deque_intervals[0]
            if end < s:
                deque_intervals.appendleft([start,end])
                break
            if start > e:
                deque_intervals.rotate(-1)
                rotations += 1
                continue
            # now, there's overlap, no more rotations
            # we pop and merge until we get end < s, insert the merged interval, and break
            start, end = min(s, start), max(e, end)

            # we must break if we rotated all elements, otherwise infinite loop
            # we're with the last element, so drop [start,end] and leave
            if rotations == len_deque - 1:
                deque_intervals[0] = [start, end]
                break

            # we pop the first element since it's been integrated into the new [start, end]
            deque_intervals.popleft()
            len_deque -= 1

        deque_intervals.rotate(rotations)
        return list(deque_intervals)

    def insert2(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        ''' It was not necessary to use a deque because in most cases we modify only
            a few elements in the list, and a deque will double the memory uses
            So, let's modify the list in place.

            Now, the time beats 84%, and 54% for memory (13% and 24% previously)
        '''
        if not intervals:
            return [newInterval]
        start, end = newInterval
        i = 0

        # let's look for the position to merge, bypass all the smaller intervals
        while i < len(intervals) and start > intervals[i][1]:
            i += 1
        # we may have reached the last element without merging capability
        if i == len(intervals):
            return intervals + [newInterval]

        # we may not need a merge, ie the newInterval fits right here
        if end < intervals[i][0]:
            intervals.insert(i, [start, end])
            return intervals

        # now we are sure we have a merge, let's find how long it goes
        start = min(intervals[i][0], start)  # we know start already
        end = max(intervals[i][1], end)  # temporary value in case we are at the end
        intervals.pop(i)
        # let's look for the last interval to merge with
        while i < len(intervals) and end >= intervals[i][0]:
            end = max(intervals[i][1], end)
            intervals.pop(i)
        intervals.insert(i, [start, end])

        return intervals

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        ''' It was not necessary to use a deque because in most cases we modify only
            a few elements in the list, and a deque will double the memory uses
            So, let's modify the list in place.

            Interestingly, the time beats 43%, and 25% for memory although it's basically
            the same code with the edge cases removed (so leetcode times are not reliable)
            I ran it several times and after 2 trials, I beat 78% of people...
        '''

        start, end = newInterval
        i = 0

        # let's look for the position to merge, bypass all the smaller intervals
        while i < len(intervals) and start > intervals[i][1]:
            i += 1

        # let's look for the last interval to merge with
        while i < len(intervals) and end >= intervals[i][0]:
            start = min(intervals[i][0], start)
            end = max(intervals[i][1], end)
            intervals.pop(i)
        intervals.insert(i, [start,end])

        return intervals

    def insert3(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # solution from another guy, he doesn't test for any edge cases !!!
        ans = []
        i = 0
        start, end = newInterval
        # append those strictly smaller than newInterval
        while i < len(intervals) and intervals[i][1] < start:
            ans.append(intervals[i])
            i += 1
        # merge with the rest: 1 ,2;| 3, 5; [4,8]; 8, 10
        while i < len(intervals) and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end   = max(end, intervals[i][1])
            i += 1
        ans.append([start,end])

        while i < len(intervals):
            ans.append(intervals[i])
            i += 1
        return ans
        
# leetcode submit region end(Prohibit modification and deletion)

assert Solution().insert([[1,5]], [0,0]) == [[0,0],[1,5]]
assert Solution().insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [17, 21]) == [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16], [17, 21]]
assert Solution().insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
assert Solution().insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [13,21]) == [[1,2],[3,5],[6,7],[8,10],[12,21]]
assert Solution().insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [9,21]) == [[1,2],[3,5],[6,7],[8,21]]
assert Solution().insert([[1,3],[6,9]], [2,5]) == [[1,5],[6,9]]

assert Solution().insert([], [5,7]) == [[5,7]]

print('TESTS PASSED')
