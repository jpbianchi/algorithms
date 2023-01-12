# https://leetcode.com/problems/minimum-window-substring  HARD
# @lc app=leetcode id=76 lang=python3
#
# [76] Minimum Window Substring
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Hard (40.77%)	14029	608
# Tags
# hash-table | two-pointers | string | sliding-window

# Companies
# facebook | linkedin | snapchat | uber

# Given two strings s and t of lengths m and n respectively, return the minimum 
# window substring of s such that every character in t (including duplicates) 
# is included in the window. If there is no such substring, return the empty string "".

# The testcases will be generated such that the answer is unique.

# Example 1:

# Input: s = "ADOBECODEBANC", t = "ABC"
# Output: "BANC"
# Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' 
# from string t.
# Example 2:

# Input: s = "a", t = "a"
# Output: "a"
# Explanation: The entire string s is the minimum window.
# Example 3:

# Input: s = "a", t = "aa"
# Output: ""
# Explanation: Both 'a's from t must be included in the window.
# Since the largest window of s only has one 'a', return empty string.
 
# Constraints:

# m == s.length
# n == t.length
# 1 <= m, n <= 105
# s and t consist of uppercase and lowercase English letters.
 
# Follow up: Could you find an algorithm that runs in O(m + n) time?
# @lc code=start
from helpers import timeit
from collections import Counter, defaultdict
class Solution:
    """ Pure dynamic programming 
    """
    
    def minWindow1(self, s: str, t: str) -> str:
        """ we use a dict key=chars from t, i=index until which we tested s
            value = min string in s[:i] for those chars, pos of last char
            Works but exceeds time limit
        """

        def sortstr(t):
            ''' 'abca' -> 'aabc' '''
            return ''.join(sorted(t))
        
        def minString(s2, t2):  
            """ adds possible substrings for t2 in s2 in dictionary
                We assume that minString(s2[:-1], t2) updates the dict correctly
                We must store all possible substrings because we don't know
                which one will win when we test for a specific character
            """
            # we start recording when len(t2) == 1 and t2 == s2[-1]
            # ie when we find one of chars of t2, then the recursion will
            # build for longer sequences of t2
            # we must keep all accurences because we don't know where 
            # the final sequence will start
            if len(t2) == 1 and len(s2) > 0:
                
                if t2 == s2[-1]:
                    pos = len(s2)-1
                    minstr.setdefault(t2,[]).extend([[t2, pos]])

                minString(s2[:-1], t2)  # t2 may occur again
                return
            
            if len(t2) == 0 or len(s2) < len(t2):  # no point trying 
                return 
            
            s3, lastchar = s2[:-1], s2[-1]
            if lastchar in t2:
                # we want sequences that end with one of chars of t2 obviously 
                
                idx = t2.index(lastchar)    # finds first occurence
                t3 = t2[:idx] + t2[idx+1:]  # removes the found char from t2
                
                minString(s3, t3)           # updates dict for s3, t3  
                # now we look for sequences that START with a char from t3
                
                # initialize dict with key = lastchar for all positions
                # we found a t3 sequence or more, so let's stretch 
                # it ALL existing sequences to the last char

                for seq, pos in minstr.get(t3,[]):
                    # seq is not useful, because it starts at pos
                    # except when we produce the answer
                
                    if pos + len(seq) - 1 < len(s2)-1:
                        # because we search for all occurences when len(t3)==1
                        # we can have occurences of t3 that start after s2
                        # don't stretch sequences that start after s2
                        # otherwise we'll get empty sequences
                        # we stretch the seq up until last char of s2
                        beststr2 = s2[pos:]
                    
                        minstr.setdefault(t2,[]).extend([[beststr2, pos]])
                
            minString(s3, t2)
                
            return
        
        minstr = {}
        
        # let's sort t so we can always assume that t2 is sorted
        tsorted = sortstr(t)
        minString(s, tsorted)
        ans = sorted(minstr[tsorted], key=lambda p: len(p[0])) if tsorted in minstr else [[""]]
        return ans[0][0]

    @timeit
    def minWindow2(self, s: str, t: str) -> str:
        """ The problem with the first solution is that if t = 'abcd'
            we scan for abc at every occurence of d, and then for ab
            at every occurence of c, and so on. 
            So, it quickly becomes exponential and costly with long t's.
            We can simply test if all letters of t are in the possible interval.
            Using counters and scanning from both ends, since the order doesn't matter.
            I still timeout... 
        """

        tcounter = Counter(t)
        sijcounter = Counter(s)
        if not ((sijcounter & tcounter) == tcounter):
            # no <= operator in python 3.7
            # not enough good chars in s
            return ""
        
        sett = set(t)
        ans = ""
        i = 0
        while i <= (len(s)-len(t)) :
            j = len(s)-1 # we scan from the end for each s[i]
            if s[i] not in sett: # we found a starting point
                i += 1
                continue
            sijcounter = Counter(s[i:])
            for j in range(len(s)-1, i+len(t)-2, -1):
                if s[j] not in sett:
                    j -= 1
                    continue
                # we have starting and ending points
                if (sijcounter & tcounter) == tcounter:
                    
                    if ans == "" or len(ans) > j-i+1:
                        ans = s[i:j+1]
                        
                    # counters keep elements with zero count which
                    # will wreck the comparison with tcounter
                    if sijcounter[s[j]] == 1:
                        del sijcounter[s[j]]
                    else:
                        sijcounter[s[j]] -= 1
                    
                    if not ((sijcounter & tcounter) == tcounter):
                        # match no more possible
                        break
                    
            i += 1
        return ans

    @timeit()
    def minWindow(self, s: str, t: str) -> str:
        """ Let's try to improve the previous solution even more
            We could avoid scanning from the end for each s[j]
            Better, we could scan to find out all the indices with chars in t
            so we avoid scanning indices with +1 
            Next, we start j from i and stop as soon as we find a solution since
            it will be the shortest one for sure for that (i,j) pair
            Next we move i, BUT we start from the current j.
            So, we move i and j without resetting j them = sliding window
            PASSES on Leetcode but beats ony 5% cpu and memory 
        """

        def counter_remove(cntr:Counter, key):
            # counters keep elements with zero count which
            # will wreck the comparison with tcounter
            if cntr[key] == 1:
                del cntr[key]
            else:
                cntr[key] -= 1

        tcounter = Counter(t)
        sijcounter = Counter(s)
        if not ((sijcounter & tcounter) == tcounter):
            # no <= operator in python 3.7
            # not enough good chars in s
            return ""

        indices = [i for i, c in enumerate(s) if c in t]
        
        # let's make sure there are at lest 2 indices to define a window
        if len(indices) == 1:
            
            if len(t) == 1:
                return s[indices[0]]
            else:
                return ""
        
        ans = ""
        i,j = 0, 1
        sijcounter = Counter(s[indices[i]:indices[j]+1])
        
        while (indices[i] <= (len(s)-len(t))) and (i<=j):

            # we have starting and ending points
            while j < len(indices):

                if (sijcounter & tcounter) == tcounter:
                    
                    if ans == "" or len(ans) > (indices[j]-indices[i]+1):
                        ans = s[indices[i]:indices[j]+1]
                            
                        # no need to increase j, the sequence will be longer for sure
                        # so we increase i, and look for the next j
                    break
                else:
                    # keep increasing j until we have a match
                    if j == len(indices)-1:
                        # no more match possible
                        return ans
                    j += 1
                    sijcounter[s[indices[j]]] += 1

            counter_remove(sijcounter, s[indices[i]])
            i += 1
            
        return ans    
    @timeit(4)
    def minWindow99(self, s: str, t: str) -> str:
        """ Solution from Leetcode: 86ms instead of my 3300ms !!!  """
        
        if len(s) < len(t):
            return ""
        
        needstr = defaultdict(int)
        
        for ch in t:
            needstr[ch] += 1
        needcnt = len(t)
        res = (0, float('inf'))
        start = 0
        for end, ch in enumerate(s):
            # expand the right boundary
            if needstr[ch] > 0:
                needcnt -= 1
            needstr[ch] -= 1
            if needcnt == 0:
                # shrink the left boundary
                while True:
                    tmp = s[start]
                    if needstr[tmp] == 0:
                        break
                    needstr[tmp] += 1
                    start += 1
                if end - start < res[1] - res[0]:
                    res = (start, end)
                # expand the right boundary
                needstr[s[start]] += 1
                needcnt += 1
                start += 1
        return '' if res[1] > len(s) else s[res[0]:res[1]+1]

# @lc code=end

assert Solution().minWindow("a", "a") == "a"

# print(Solution().minWindow("ADOBECODEBANC", "ABC"))
assert Solution().minWindow("ADOBECODEBANC", "ABC") == "BANC"
assert Solution().minWindow("ADOBECODEBANC", "AAN") == "ADOBECODEBAN"
assert Solution().minWindow("ADOBECODEBANC", "AEB") == "EBA"
assert Solution().minWindow("ADOBECODEBANC", "CCEO") == "CODEBANC"

assert Solution().minWindow("ADOBECODEBANC", "OBOB") == "OBECODEB"

# print(Solution().minWindow("cabwefgewcwaefgcf", "cae"))
assert Solution().minWindow("cabwefgewcwaefgcf", "cae") == "cwae"

s = "tkopjjgknziznmfwvkgospwkujjklzugjiwvuefhepiteppbzyptplekwnwjmqqybovvsccyrnuxclyclnvbaznxojgdzydcmyxhacftpbrrnrvyftbfuoelxlozjtbyrbftdkoumhnbzlzgeblarslpdbqoutmnwrgzexvsejtfwulcxzcprqgwrykorxboqkpwhnonyjvuggwdfauyqauiafyseziwjztsojimvdiblegrhdrxdmhetfyxfitqjolaytmtyxwjdeckhuingptbxtyedtumihmgcbbayxkbdomliwyqnrrkmropllbvsqbvtexrdjugyirierzsksewktlxepsyhvvabttecpkayejevkyiedeqwsncjhascwudrnjteuwcahhxtffxkmoggdkpllhpjbvcqevuatzaaiyvpftarjixmtoxgxnraitsoqnpkormwpilxbnomwoypcwvclocvhvlxkajaswwjejghzxtvltmprjrcxwzetldfnnffjdrpoxynurkhmwxefqieoikhvooibvqmyhdpgbcdunkgljktatxqdiaywoizkynkhqzqretntftepgxrzvjcdjcbykcklpwufykycfnvngzcmzvnwerzotcogearvwncuaayfptsvvwkwtzsyrtokveqbgjwexyzxazepvzmqvymryeppxfbuluvrdtvcrwbtwikthwjevxvvdmmcrnyehvvnotrhrvcndmgkirofqkavwmzqcxwluuyinsrentuqfccqwqvocykbmltolpafjaqyshfhbbzidbybuwqwuczgnsxykxgvxwusdbbgcbrfcpjwnzvhbuqqpnrzmxujtqdyrfhvgydkpmjdlemoacgprzqdwnprfssxzz"
t = "ufzxqojzrufekhitzcsphr"
ans = "zcprqgwrykorxboqkpwhnonyjvuggwdfauyqauiafyseziwjztsojimvdiblegrh"
# print("First version:", timeit(Solution().minWindow1)(s,t))  # never ends, dont run it
# assert Solution().minWindow2(s,t) == ans  # 4.5s
assert Solution().minWindow(s,t) == ans  # 0.016s
assert Solution().minWindow99(s,t) == ans  # 0.0008s
print("TESTS PASSED")