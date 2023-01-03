# https://leetcode.com/problems/combination-sum/
# @lc app=leetcode id=39 lang=python3
#
# [39] Combination Sum
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (68.00%)	14553	290
# Tags
# array | backtracking

# Companies
# snapchat | uber

# Given an array of distinct integers candidates and a target integer target, 
# return a list of all unique combinations of candidates where the chosen numbers 
# sum to target. You may return the combinations in any order.

# The same number may be chosen from candidates an unlimited number of times. Two 
# combinations are unique if the frequency of at least one of the chosen numbers is different.

# The test cases are generated such that the number of unique combinations that sum up 
# to target is less than 150 combinations for the given input.

# Example 1:

# Input: candidates = [2,3,6,7], target = 7
# Output: [[2,2,3],[7]]
# Explanation:
# 2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
# 7 is a candidate, and 7 = 7.
# These are the only two combinations.
# Example 2:

# Input: candidates = [2,3,5], target = 8
# Output: [[2,2,2,2],[2,3,3],[3,5]]
# Example 3:

# Input: candidates = [2], target = 1
# Output: []
 
# Constraints:

# 1 <= candidates.length <= 30
# 2 <= candidates[i] <= 40
# All elements of candidates are distinct.
# 1 <= target <= 40
from typing import List
from tabulate import tabulate

# @lc code=start
class Solution:
    """ This is knapsack with repetitions"""
    
    def combinationSum1(self, candidates: List[int], target: int) -> List[List[int]]:
        """ This is slow because it's not exactly knapsack because the max 
            is already given, so we 
        """
        seqs = [[[]]]  # seqs[b] is the list of sequences that sum to b
            
        for b in range(1,target+1):
            seqs += [[]]
            for c in candidates:
                if c > b:
                    continue

                seqs[b] += [sorted(seq + [c]) for seq in seqs[b-c]]
        
        # print(tabulate(seqs))
        winners = seqs[target]
        # eliminate duplicates
        ans = [seq for i, seq in enumerate(winners) if seq not in winners[:i]]
        return ans
 
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """ Let's try to sort only at the end to gain time, and use append instead of +=
            append is supposed to be faster
            It didn't make a difference on Leetcode, I'm still 100 times slower.  
            
            The issue is my 2D array, which makes it slower to access.  
        """
        seqs = [[[]]]  # seqs[b] is the list of sequences that sum to b
        
        for b in range(1,target+1):
            seqs += [[]]
            for c in candidates:
                if c > b:
                    continue

                for seq in seqs[b-c]:
                    seqs[b].append(seq + [c])

    def combinationSum3(self, candidates: List[int], target: int) -> List[List[int]]:
        """ Let's try with dictionaries.  Same result.
        """
        seqs = {0:[[]]}  # seqs[b] is the list of sequences that sum to b
        
        for b in range(1,target+1):
            seqs[b] = []
            for c in candidates:
                if c > b:
                    continue

                for seq in seqs[b-c]:
                    seqs[b].append(seq + [c])
        
        print(tabulate(seqs))

        winners = [sorted(seq) for seq in seqs[target]]
        # eliminate duplicates
        ans = [seq for i, seq in enumerate(winners) if seq not in winners[:i]]
        return ans
    
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """ Let's try to scan the numbers first, so we don't generate duplicates
            and we can use a 1D array instead of a 2D array.
            The number of loops is the same, so we'll see if the slowness came from
            the 2D array.  
            CPU time collapsed by 80 from 6000 ms to 80... so the 2D array was the issue.
        """
        seqs = [[] for _ in range(target + 1)]  # seqs[b] is the list of sequences that sum to b
        seqs[0] = [[]] # initialize the first element otherwise seqs[b-c] is empty when b==c
        
        for c in candidates:
            for b in range(1,target+1):
            
                if c > b:
                    continue

                for seq in seqs[b-c]:
                    seqs[b].append(seq + [c])
        
        print(tabulate(seqs))

        return seqs[target]
    
    def combinationSum99(self, candidates: List[int], target: int) -> List[List[int]]:
        """ One of the fastest solutions on leetcode 
            they also have a nested loop, and update dp[i-c] combinations, like
            I do with seqs[b-c] above, but they don't sort the combinations.
            This solution is 100 times faster than mine (except the last one).
            
            If we scan the numbers first, we're assured to never generate duplicates, so I
            need more memory for sure, but it still doesn't explain the speed difference, 
            except maybe the access to a 2D array is slower.
        """
        dp = [[] for _ in range(target+1)]
        for c in candidates:
            for i in range(c, target+1):
                if i == c: 
                    dp[i].append([c])
                for comb in dp[i-c]: 
                    dp[i].append(comb + [c])
        return dp[-1]
        
# @lc code=end

# print(Solution().combinationSum([2,3,6,7], 7))
# print(Solution().combinationSum([2,3,5], 8))
assert Solution().combinationSum([2,3,6,7], 7) == [[2,2,3],[7]]
assert Solution().combinationSum([2,3,5], 8) == [[2,2,2,2],[2,3,3],[3,5]]
assert Solution().combinationSum([2], 1) == []

print("TESTS PASSED")
      
