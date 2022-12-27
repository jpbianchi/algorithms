# https://leetcode.com/problems/maximum-subarray
# Given an integer array nums, find the subarray which has the largest sum and 
# return its sum. 
#
#  Example 1: 
# Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
# Output: 6
# Explanation: [4,-1,2,1] has the largest sum = 6.
#
#  Example 2: 
#
# Input: nums = [1]
# Output: 1

#  Example 3:
# Input: nums = [5,4,-1,7,8]
# Output: 23

#  Constraints:#  
#  1 <= nums.length <= 10⁵ 
#  -10⁴ <= nums[i] <= 10⁴ 
#  
#  Follow up: If you have figured out the O(n) solution, try coding another 
# solution using the divide and conquer approach, which is more subtle. 
# 
#  Related Topics Array Divide and Conquer Dynamic Programming 👍 26742 👎 1201


# leetcode submit region begin(Prohibit modification and deletion)
from typing import List

class Solution:
    def maxSubArray1(self, nums: List[int]) -> int:
        # we can add the positives in sequence together, store intermediate sums
        # a negative will 'block' a sequence if its abs value is > sum of pos before, so
        # we keep a negative only if it's smaller than the sum of positives before
        # otherwise it doesn't make sense to include both numbers in a sequence
        # sum them and repeat
        last_sum = nums[0]
        max_sum = last_sum

        for i in range(1, len(nums)):
            # if the sequence starts with negatives (or is only negatives)
            if last_sum <= 0 and nums[i] <= 0:
                last_sum = max(last_sum, nums[i])  # keep the highest negative
                max_sum = max(last_sum, max_sum)
                continue

            last_sum = max(0, last_sum)  # reset if previous ones were negs

            # if we ever get here we are sure to start with a positive
            if nums[i] >= 0:
                last_sum += nums[i]

            elif last_sum > -nums[i]:
                # we met a negative whose abs < last_sum
                # store last_sum but continue
                last_sum += nums[i]

            else:
                # this negative blocks the sequence
                # remove it and next ones if any
                last_sum = 0  # we start over

            max_sum = max(last_sum, max_sum)

        return max_sum

    def maxSubArray(self, nums: List[int]) -> int:
        # for some reason, this one is much slower and takes more memory ???
        # although it's much simpler and also scans the list in one swoop
        last_sum = nums[0]
        max_sum = last_sum

        for n in nums[1:]:

            if last_sum < 0:
                # when last_sum has decreased below 0, no need to continue adding
                # n could be a positive, so keep it
                # but it could be a sequence of negatives, so use max to keep highest

                # replacing max() with if else decreased the time
                # last_sum = max(n, last_sum)
                last_sum = n if n > last_sum else last_sum
            else:
                last_sum = last_sum + n

            # replacing max() with if else decreased the time
            # max_sum = max(last_sum, max_sum)
            max_sum = last_sum if last_sum > max_sum else max_sum

        return max_sum

    def maxSubArray3(self, nums: List[int]) -> int:
        # solution on Leetcode with minimum memory
        # however, I reran it and it was not anymore ??? but it's clever

        for i in range(1, len(nums)):
            nums[i] = max(nums[i], nums[i] + nums[i - 1])
        return max(nums)



# leetcode submit region end(Prohibit modification and deletion)

test_vectors = [
    ([-1,-2], -1), ([-2,-1], -1), ([-2,1,-3,4,-1,2,1,-5,4], 6), ([5,4,-1,7,8], 23)
]

def test_all(fn):
    for vector, sol in test_vectors:
        assert fn(vector) == sol, f"vector {vector}, answer {fn(vector)} != {sol}"


test_all(Solution().maxSubArray)
print('TESTS PASSED')