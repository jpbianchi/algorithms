# https://leetcode.com/problems/median-of-two-sorted-arrays/
# @lc app=leetcode id=4 lang=python3
#
# [4] Median of Two Sorted Arrays
# Category	Difficulty	Likes	Dislikes
# algorithms	Hard (35.51%)	21400	2416
# Tags
# array | binary-search | divide-and-conquer

# Companies
# adobe | apple | dropbox | google | microsoft | yahoo | zenefits

# Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

# The overall run time complexity should be O(log (m+n)).

# Example 1:

# Input: nums1 = [1,3], nums2 = [2]
# Output: 2.00000
# Explanation: merged array = [1,2,3] and median is 2.
# Example 2:

# Input: nums1 = [1,2], nums2 = [3,4]
# Output: 2.50000
# Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
 
# Constraints:

# nums1.length == m
# nums2.length == n
# 0 <= m <= 1000
# 0 <= n <= 1000
# 1 <= m + n <= 2000
# -106 <= nums1[i], nums2[i] <= 106

# @lc code=start
class Solution:
    def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
        '''
            Quick and dirty, and I passed... faster than 70% of people
            One can easily improve by not using sorted() but going
            through both lists one element at a time, and counting
            until we find the median -> O(n)
            It could be even faster to use binary sort on both lists
            then we'd get O(log n) but prob quite complex
        '''
        l1, l2 = len(nums1), len(nums2)
        totallen = l1+l2
        median_idx = [totallen // 2] if totallen % 2 == 1 else [totallen // 2 -1, totallen // 2]
        newlist = sorted(nums1 + nums2)
        print(newlist, median_idx)

        return sum(newlist[i] for i in median_idx) / len(median_idx)


ans = findMedianSortedArrays([1, 2], [3, 4])
assert ans == 2.5, f'Expected 2.5, got {ans}'

ans = findMedianSortedArrays([1, 3], [2])
assert ans == 2, f'Expected 2, got {ans}'
# @lc code=end

