# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
#
# @lc app=leetcode id=3 lang=python
#
# [3] Longest Substring Without Repeating Characters
#
# @lc code=start
class Solution(object):
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Redid this problem on 26/12/22
        This is a typical dynamic programming problem, a bit
        similar to Longest Increasing Sequence (LIS)
        but with a substring and no repeat constraint
        The substring constraint allows us to consider that the new
        char follows the current max substring (or not)
        but we don't go all the way back to find a substring to attach
        to, otherwise we'd end up with a sequence.
        If it is already in it, at pos k, we can only start a new
        substring at pos+1.  MaxLen does not increase.  
        In the end, it works like a sliding window (because of substring
        contraint).
        This beats 95% in cpu time, and 50% in memory
        """
        maxStr = ""
        maxLen = 0
 
        for ch in s:
            if ch in maxStr:
                # we restart substring at pos+1 
                # so maxLen can not increase
                pos = maxStr.index(ch)
                maxStr = maxStr[pos+1:] + ch
            else:
                maxStr += ch
                maxLen = max(maxLen, len(maxStr))
        return maxLen


        
# @lc code=end

class Solution1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        ans = 0

        while ans <= len(s):
            ans += 1
            for i in range(len(s)-ans+1):
                if len(set(s[i:i+ans])) == ans:
                    break
            else:
                return ans - 1

                    
class Solution2:
    ''' For each position, let s try to find longest substring '''
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0: # s could be an empty string
            return 0
        ans = 1  
        lens = len(s)

        for i in range(lens):
            if i + ans >= lens:
                break # we won't find a longer substring
            for j in range(i+ans+1,lens+1): # j must reach lens since we do s[i:j]
                if len(set(s[i:j])) > ans:
                    ans = j-i
                    continue
                break
        return ans
    
class Solution3:

    def lengthOfLongestSubstring(self, s: str) -> int:
        ''' We can improve by not testing len(set) every time
            but only if s[j] is in s[i:i+ans]
        '''
        if len(s) == 0: # s could be an empty string
            return 0
        ans = 1
        lens = len(s)

        for i in range(lens):
            if i + ans >= lens:
                break # we won't find a longer substring
            stemp = set(s[i:i+ans])
            if len(stemp) < ans: # let's see if it's worth testing j's
                continue  # stemp has duplicates, so need to go further
            for j in range(i+ans,lens):
                if s[j] in stemp:
                    break
                else:
                    ans +=1
                    stemp.add(s[j])
                    continue
        return ans
    
class Solution4:

    def lengthOfLongestSubstring(self, s: str) -> int:
        ''' We can improve even more by moving i to right position when we find
            s[j] by using a mapping between letters and their position
            because of that, we will never have duplicates and we don't need to count
            only save the indices
        '''
        pos = {}
        ans = 0
        lens = len(s)
        i,j = 0,0
        while i + ans < lens and j < lens: # we won't find a longer substring
            # we assume all pos[s[i<=j]] are available since we're going to store all s[j]'s as we go

            if s[j] in pos and pos[s[j]] > i: # if we find that s[j] was before s[i], we only update s[j] index
                # let's move i straight after the previous occurrence of s[j] since anything in between
                # will produce a duplicate with s[j] obviously
                i = pos[s[j]]  # because we stored in s[j] the index of the next char
                # since we moved i, we could also jump j by ans positions but then we need all s[j]
                # so we keep incrementing j by 1, in the end it will be O(n) anyway, not more

            ans = max(ans, j - i + 1)  # recalculate ans after moving i or not

            pos[s[j]] = j+1  # j+1 is where we will put i when we detect a duplicate
            j += 1

        return ans
    
assert Solution().lengthOfLongestSubstring('abcabcbb') == 3
assert Solution().lengthOfLongestSubstring('') == 0
assert Solution().lengthOfLongestSubstring('bbbbb') == 1
assert Solution().lengthOfLongestSubstring('pwwkew') == 3
assert Solution().lengthOfLongestSubstring('abcdebede') == 5
print("TESTS PASSED")