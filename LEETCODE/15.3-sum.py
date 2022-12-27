# https://leetcode.com/problems/3sum/
#
# @lc app=leetcode id=15 lang=python3
#
# [15] 3Sum
# 3Sum
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (32.36%)	23165	2126
# Tags
# array | two-pointers

# Companies
# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

# Notice that the solution set must not contain duplicate triplets.

# Example 1:

# Input: nums = [-1,0,1,2,-1,-4]
# Output: [[-1,-1,2],[-1,0,1]]
# Explanation: 
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
# The distinct triplets are [-1,0,1] and [-1,-1,2].
# Notice that the order of the output and the order of the triplets does not matter.
# Example 2:

# Input: nums = [0,1,1]
# Output: []
# Explanation: The only possible triplet does not sum up to 0.
# Example 3:

# Input: nums = [0,0,0]
# Output: [[0,0,0]]
# Explanation: The only possible triplet sums up to 0.
 
# Constraints:

# 3 <= nums.length <= 3000
# -105 <= nums[i] <= 105
from typing import List
# @lc code=start
import numpy as np
import time
from itertools import combinations
class Solution:

    def threeSum1(self, nums: List[int]) -> List[List[int]]:
        """ However, let's try a different approach using powerful Numpy methods
            It works, but there are too many combinations for very large lists
        """
                
        triplets = np.array(list(combinations(nums,3)))
        zerosumsloc = np.where(triplets.sum(axis=1) == 0)[0]
        valid_triplets = triplets[zerosumsloc].tolist()
        # now we must remove the duplicates (beware diff order but identical)
        return list(list(s) for s in set(tuple(sorted(tr)) for tr in valid_triplets))
    
    def threeSum2(self, nums: List[int]) -> List[List[int]]:
        """ Let's try with a meshgrid, but it's worse because it
            can take several time the same element
        """
        mesh = np.array(np.meshgrid(nums, nums, nums))          # grows like O(n^3)
        zerosumsloc = np.array(np.where(mesh.sum(0) == 0)).T    # array([0,4,5],[3,1,1]...)
        # print(zerosumsloc)
        # we must eliminate those with the same position twice or thrice
        nps = np.unique(np.sort(zerosumsloc, axis=1), axis=0)
        # rows are sorted, so no need to test nps[:,0] == nps[:,2]
        duploc = np.any([nps[:,0] == nps[:,1], nps[:,1] == nps[:,2]], axis=0)
        
        valid_triplets = np.array(nums)[nps[~duploc]]
        # we removed duplicate positions but there still could be duplicate values
        return list(list(s) for s in set(tuple(sorted(tr)) for tr in valid_triplets))
            
    def threeSum3(self, nums: List[int]) -> List[List[int]]:
        """ Let's try with a meshgrid, but with indices to detect i==j, i==k upfront
            It doesn't solve the O(n^3) problem but it's more elegant to find a 
            mask of all invalid positions, and use it to set the corresponding
            sums to -1, just before extracting the positions of zero sums
        """
        N = len(nums)
        Nrange = np.arange(N)
        # here we use a meshgrid of indices, so we can create the mask
        mesh = np.array(np.meshgrid(Nrange, Nrange, Nrange))    # 3x6x6x6, grows like O(n^3)

        # the following mask is True at any position that doesn't have 3 different indices
        mask = np.any([mesh[0,:,:,]==mesh[1,:,:,:], 
                       mesh[0,:,:,]==mesh[2,:,:,:],
                       mesh[1,:,:,]==mesh[2,:,:,:]], axis=0)    # 6x6x6

        allsums = np.array(nums)[mesh].sum(axis=0)              # 6x6x6, all possible sums
        # let's remove the sums using 1 or 2 identical positions (i=j, i=j=k etc)
        allsums[mask] = -1  # -1 will be ignored by following test                                  
        zerosumsloc = np.array(np.where(allsums == 0)).T        # array([0,4,5],[3,1,1]...)

        valid_triplets = np.array(nums)[zerosumsloc]
        # we removed duplicate positions but there still could be duplicate values
        return list(list(s) for s in set(tuple(sorted(tr)) for tr in valid_triplets))            

    def threeSum4(self, nums: List[int]) -> List[List[int]]:
        """ If we sort the numbers, we can use dynamic programming
            to determine if a number at pos j can be zeroed by 2 numbers
            after it (after sorting).
        """
        nums.sort()
        N = len(nums)
        # print(f"List has {N} values")
        combos = set()
        for i in range(N-2):
            if (nums[i] + nums[i + 1] + nums[i + 2]) > 0:  # we're done
                # print(f'No need to scan anymore at i = {i}')
                break
            if (nums[i] + nums[N - 2] + nums[N - 1] < 0):
                # print(f'No combination for nums[{i}]')
                continue
                # print('Stopped at', i,nums2[i] + nums2[i + 1]+mx)
            j = i+1
            k = N-1
            while j < k:
                if nums[i] + nums[j] + nums[k] > 0:
                    k -= 1
                elif nums[i] + nums[j] + nums[k] < 0:
                    j += 1
                else:
                    combos.add(tuple([nums[i], nums[j], nums[k]]))
                    k -= 1
                    j += 1
        return list(combos)

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """ If we sort the numbers, we can use dynamic programming
            to determine if a number at pos j can be zeroed by 2 numbers
            after it (after sorting).
        """
        N = len(nums)
        combos = set()
        nums = sorted(nums)
        if (N >=3) and (min(nums) == 0) and (max(nums) == 0):
            return [[0,0,0]]

        for i in range(N-2):
            if (nums[i] + nums[i + 1] + nums[i+2]) > 0:  # we're done
                break
            if (nums[i] + nums[N-2] + nums[N-1] < 0):
                continue
            j = i+1
            k = N-1
            while j < k:
                if nums[i] + nums[j] + nums[k] > 0: 
                    k -= 1
                elif nums[i] + nums[j] + nums[k] < 0:
                    j += 1
                else:
                    combos.add(tuple([nums[i], nums[j], nums[k]]))
                    k -= 1
                    j += 1

        return [list(c) for c in combos]

    def threeSum99(self, nums: List[int]) -> List[List[int]]:
        """ One of the fastest solution on Leetcode
            It uses a previous problem (Two Sum) which finds all the
            couple of elements that add up to a target number.
            For every number, we use it to find two numbers after it
            that add up to its negative value.  
        """
        def twoSum(nums, target, ans):
            left, right = 0, len(nums) - 1
            while left < right:
                if nums[left] + nums[right] > target:
                    right -= 1
                elif nums[left] + nums[right] < target:
                    left += 1
                else:
                    ans.append([-target, nums[left], nums[right]])
                    right -= 1
                    left += 1
                    while left < right and nums[left] == nums[left-1]: left += 1
        
        nums.sort()

        ans = []
        for i in range(len(nums)):
            if nums[i] > 0: break
            if nums[i] == nums[i-1] and i > 0: continue

            twoSum(nums[i+1:], -nums[i], ans)
        return ans

# @lc code=end

print(Solution().threeSum([-1,0,1,2,-1,-4]))  # [[-1, 0, 1], [-1, -1, 2]]
print(Solution().threeSum([0,0,0,0]))         # [[0, 0, 0]]

from test_vectors.testvec_15_3sum import test1  # 3000 values, O(n^3) will explode
print(Solution().threeSum(test1[:200]))
start = time.perf_counter()
print(Solution().threeSum(test1))
print(f"CPU time = {time.perf_counter() - start:.2f} s")    # 2.7s

start = time.perf_counter()
print(Solution().threeSum99(test1))
print(f"CPU time = {time.perf_counter() - start:.2f} s")    # 1.9s

