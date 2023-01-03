# https://leetcode.com/problems/search-in-rotated-sorted-array/
# @lc app=leetcode id=33 lang=python3
#
# [33] Search in Rotated Sorted Array
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (38.79%)	19197	1149
# Tags
# array | binary-search

# Companies
# bloomberg | facebook | linkedin | microsoft | uber

# There is an integer array nums sorted in ascending order (with distinct values).

# Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

# Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

# You must write an algorithm with O(log n) runtime complexity.

# Example 1:

# Input: nums = [4,5,6,7,0,1,2], target = 0
# Output: 4
# Example 2:

# Input: nums = [4,5,6,7,0,1,2], target = 3
# Output: -1
# Example 3:

# Input: nums = [1], target = 0
# Output: -1
 

# Constraints:

# 1 <= nums.length <= 5000
# -104 <= nums[i] <= 104
# All values of nums are unique.
# nums is an ascending array that is possibly rotated.
# -104 <= target <= 104
from typing import List
from bisect import bisect_left
# @lc code=start
class Solution:
    """ This is binary search with a twist
        When we split the list in 2, one of the 2 lists is always sorted
        and we can know which one by comparing the first and last element.
        So, even if the list has been rotated, we can still use binary search.
        If the target is in that sorted list, we discard the other one.
        If we keep the other one, then the pattern is the same: one half is sorted,
        the other not. 
        We have to keep track of the position when we keep the 2nd half
        Beats 90% cpu, 90% memory although at times numbers are much lower.
        
        Another solution would be to find the pivot point so we have two sorted halves
        and then do binary search in one of them.
    """
    def search(self, nums: List[int], target: int) -> int:
        
        pos = 0
        while nums:
            idx = len(nums) // 2
            if idx == 0:
                return pos if nums[0] == target else -1
            
            # let's find the indices a,b of the sorted part
            # I use <= for the case idx=1
            a,b = (0, idx-1) if nums[0] <= nums[idx-1] else (idx, len(nums)-1)
            # c,d are the indices of the other part
            c,d = (idx, len(nums)-1) if nums[0] <= nums[idx-1] else (0, idx-1)

            # if the target is in the sorted part, we can discard the other one
            if nums[a] <= target <= nums[b]:
                nums = nums[a:b+1]
                pos += a
            else:
                nums = nums[c:d+1]
                pos += c
        return pos
            
# @lc code=end
assert Solution().search([3,5,1], 1) == 2
assert Solution().search([1,3,5], 5) == 2
assert Solution().search([1,3], 3) == 1
assert Solution().search([4,5,6,7,0,1,2], 0) == 4
assert Solution().search([4,5,6,7,0,1,2], 3) == -1
assert Solution().search([1], 0) == -1

print("TESTS PASSED")
