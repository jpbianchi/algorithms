# https://leetcode.com/problems/product-of-array-except-self/
# @lc app=leetcode id=238 lang=python3
#
# [238] Product of Array Except Self
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (64.84%)	15833	881
# Tags
# array

# Companies
# amazon | apple | facebook | linkedin | microsoft

# Given an integer array nums, return an array answer such that answer[i] 
# is equal to the product of all the elements of nums except nums[i].

# The product of any prefix or suffix of nums is guaranteed to fit in a 
# 32-bit integer.

# You must write an algorithm that runs in O(n) time and without using the 
# division operation.

# Example 1:

# Input: nums = [1,2,3,4]
# Output: [24,12,8,6]
# Example 2:

# Input: nums = [-1,1,0,-3,3]
# Output: [0,0,9,0,0]

# Constraints:

# 2 <= nums.length <= 105
# -30 <= nums[i] <= 30
# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
 
# Follow up: Can you solve the problem in O(1) extra space complexity? 
# (The output array does not count as extra space for space complexity analysis.)

from typing import List 

# @lc code=start
from math import log2
from functools import reduce
import operator
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """ Beats 66%, 13%
        """
        
        if 0 in nums:
            idx0 = nums.index(0)
            if 0 in nums[:idx0]+nums[idx0+1:]:
                # there are 2 zeros -> return all zeros
                return [0] * len(nums)
            else:
                #there is 1 zero -> all zero but 1
                ans = [0] * len(nums)
                ans[idx0] = reduce(operator.mul,nums[:idx0]+nums[idx0+1:])
                return ans
        
        lognums = [log2(abs(n)) for n in nums]
        sumnegsigns = sum(n<0 for n in nums)  # how many neg numbers
        logmul = sum(lognums)
        signs = [-1 if (sumnegsigns - (num<0))%2 else 1 for num in nums]
        
        return [round(2**(logmul-lognum)) * sign for sign,lognum in zip(signs,lognums)]
    
    def productExceptSelf99(self, nums: List[int]) -> List[int]:
        """ Good solution from leetcode, runs 220ms instead of my 270ms because no logs
            Very smart: first pass calculates the multiplications from 0 to i but i
                        second pass calculates the multiplications from n to i but i * the
                        first pass mults, so the result is the product of all except i
                        BUT it's O(n^2), my solution is O(n)
            However, this solution is O(1) in space since it uses only the output array
            while my solution is O(n) in space (in reality the output counts as space)
        """
        res = [1] * len(nums)

        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *= nums[i]

        postfix = 1
        for i in range(len(nums)-1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        
        return res
        
# @lc code=end

assert Solution().productExceptSelf([1,-2,3,4]) == [-24,12,-8,-6]
assert Solution().productExceptSelf([1,-2,3,-4]) == [24,-12,8,-6]
assert Solution().productExceptSelf([1,2,3,4]) == [24,12,8,6]
assert Solution().productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0]
assert Solution().productExceptSelf([-1,1,0,-3,0]) == [0,0,0,0,0]
    
print("TESTS PASSED")