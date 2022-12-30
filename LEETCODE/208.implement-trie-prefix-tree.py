# https://leetcode.com/problems/implement-trie-prefix-tree
# https://en.wikipedia.org/wiki/Trie
# @lc app=leetcode id=208 lang=python3
#
# [208] Implement Trie (Prefix Tree)
#

# 
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (61.21%)	8737	106
# Tags
# design | trie

# Companies
# A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

# Implement the Trie class:

# Trie() Initializes the trie object.
# void insert(String word) Inserts the string word into the trie.
# boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
# boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.
 

# Example 1:

# Input
# ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
# [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
# Output
# [null, null, true, false, true, null, true]

# Explanation
# Trie trie = new Trie();
# trie.insert("apple");
# trie.search("apple");   // return True
# trie.search("app");     // return False
# trie.startsWith("app"); // return True
# trie.insert("app");
# trie.search("app");     // return True
 

# Constraints:

# 1 <= word.length, prefix.length <= 2000
# word and prefix consist only of lowercase English letters.
# At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.


# @lc code=start
class Trie:
    """ Beats 72% cpu, 77% memory
    """
    def __init__(self):
        self.tree = {}


    def insert(self, word: str) -> None:
        node = self.tree
        for i in range(len(word)):
            wor = word[:i+1]
            # print(wor)
            if wor in node: 
                node = node[wor]
                continue
            node[wor] = {}
            node = node[wor]
        node['added'] = None # mark node as 'added'
            
            
    def __repr__(self) -> str:
        out = []
        nodes = [self.tree]
        while nodes:
          node = nodes.pop(0)
          for k,v in node.items():
              out.append(k)  
              if v:
                nodes.append(v)
        return "-".join(out)
        
        
    def search(self, word: str) -> bool:
        node = self.tree
        for i in range(len(word)):
            wor = word[:i+1]
            if wor in node:
                node = node[wor]
                # print(node)
            else:
                return False
        # if word was added, then it has 
        return 'added' in node

    def startsWith(self, prefix: str) -> bool:
        node = self.tree
        for i in range(len(prefix)):
            wor = prefix[:i+1]
            if wor in node:
                node = node[wor]
            else:
                return False
        # here we don't care if prefix is a leaf or not
        return True


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
# @lc code=end

# print(Trie().insert('apple'))
trie = Trie();
trie.insert("apple");
assert trie.search("apple") is True
# print(trie)
assert trie.search("app") is False
assert trie.startsWith("app") is True
trie.insert("app");
# print(trie)
assert trie.search("app") is True
print("TESTS PASSED")