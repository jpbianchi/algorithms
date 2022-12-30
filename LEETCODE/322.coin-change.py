# https://leetcode.com/problems/coin-change/
# @lc app=leetcode id=322 lang=python3
#
# [322] Coin Change
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (41.69%)	14901	344
# Tags
# dynamic-programming

# Companies
# Unknown

# You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

# Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

# You may assume that you have an infinite number of each kind of coin.

 

# Example 1:

# Input: coins = [1,2,5], amount = 11
# Output: 3
# Explanation: 11 = 5 + 5 + 1
# Example 2:

# Input: coins = [2], amount = 3
# Output: -1
# Example 3:

# Input: coins = [1], amount = 0
# Output: 0
 

# Constraints:

# 1 <= coins.length <= 12
# 1 <= coins[i] <= 231 - 1
# 0 <= amount <= 104
from typing import List 
# @lc code=start
class Solution:
    """ This is knapsack-y with repetition, where the sum is already given, but we  
         want a min. Also, the weights are the values here, but it's still the same thing.
        We still need to try all values up to the amount given, because when we
        add a coin, we need the min for amount - value of the coin.
        Beats 97% cpu, 62% memory
    """
    def coinChange(self, coins: List[int], amount: int) -> int:
        
        A = amount+1
        # M[v] = min coins to reach value v exactly (amount+1 = not possible)
        M = [0] + [A] * (A-1)       # 0 is possible by taking no coin
        
        for v in range(1,A):        # we assume index = value
            M[v] = min([A] + [M[v-c]+1 for c in coins if v>=c])
        
        best_min = M[-1]
                    
        return best_min if best_min < A else -1
                
# @lc code=end
assert Solution().coinChange([2], 3) == -1
assert Solution().coinChange([1,2,5], 11) == 3
print("TESTS PASSED")
