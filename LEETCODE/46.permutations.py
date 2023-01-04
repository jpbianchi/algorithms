# https://leetcode.com/problems/permutations/
# @lc app=leetcode id=46 lang=python3
#
# [46] Permutations
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (75.07%)	14178	241
# Tags
# backtracking

# Companies
# linkedin | microsoft

# Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

# Example 1:

# Input: nums = [1,2,3]
# Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
# Example 2:

# Input: nums = [0,1]
# Output: [[0,1],[1,0]]
# Example 3:

# Input: nums = [1]
# Output: [[1]]
 
# Constraints:

# 1 <= nums.length <= 6
# -10 <= nums[i] <= 10
# All the integers of nums are unique.
from typing import List
# @lc code=start
from itertools import permutations
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        return {tuple(perm) for perm in permutations(nums)}
        
# @lc code=end
assert Solution().permute([0,1]) == {(0,1),(1,0)}
assert Solution().permute([1,2,3]) == {(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)}

print("TESTS PASSED")
