# https://leetcode.com/problems/validate-binary-search-tree/
# @lc app=leetcode id=98 lang=python3
#
# [98] Validate Binary Search Tree
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (31.82%)	13461	1097
# Tags
# tree | depth-first-search

# Companies
# amazon | bloomberg | facebook | microsoft

# Given the root of a binary tree, determine if it is a valid binary search tree (BST).

# A valid BST is defined as follows:

# The left subtree of a node contains only nodes with keys less than the node's key.
# The right subtree of a node contains only nodes with keys greater than the node's key.
# Both the left and right subtrees must also be binary search trees.
 
# Example 1:

# Input: root = [2,1,3]
# Output: true
# Example 2:

# Input: root = [5,1,4,null,null,3,6]
# Output: false
# Explanation: The root node's value is 5 but its right child's value is 4.
 
# Constraints:

# The number of nodes in the tree is in the range [1, 104].
# -231 <= Node.val <= 231 - 1

from typing import Optional
from collections import deque
# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ Beware, ALL nodes in a subtree must be higher/lower than the root node,
        not only its direct children. 
        This could be done with recursion, it's not difficult, so I prefer to try
        sthg else, ie propagate the max/min value of the left/right subtree so we
        can go down the tree in one pass.  How to pass those values is not obvious
        at all - see the comments in the code.
        Beats 82% cpu, 92% memory
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        queue = deque()
        # let's add a max and min attribute to each node
        # to propagate the max/min value of the left/right subtree
        root.maxx = float("-inf")
        root.minn = float("inf")
        queue.append(root)
        
        while queue:
            
            node = queue.popleft()
            
            if node.val is None:
                continue
            if node.left is not None:
                if node.left.val>= node.val or node.left.val <= node.maxx:
                    return False
            if node.right is not None:
                if node.right.val <= node.val or node.right.val >= node.minn:
                    return False
                
            if node.left is not None:
                # one has to draw the tree to understand why this works
                # the max of the left subtree is the previous maxx
                # the min of the left subtree is the previous node
                # basically, when we go left, we propagate only the previous maxx
                # and the current node value for the minn
                node.left.maxx = node.maxx
                node.left.minn = node.val 
                queue.append(node.left)
                
            if node.right is not None:
                node.right.maxx = node.val
                node.right.minn = node.minn
                queue.append(node.right)
            
        return True
        
    def isValidBST99(self, root: Optional[TreeNode]) -> bool:
        """ One of the best solution on Leetcode (a bit faster but recursive)
        """
        prev = None
        def dfs(node):
            if node is None: return None

            left = dfs(node.left)

            nonlocal prev
            if prev is not None and prev >= node.val:
                return False
            prev = node.val

            right = dfs(node.right)

            return left is not False and right is not False

        return dfs(root)
        
# @lc code=end
from helpers import build_tree

assert Solution().isValidBST(build_tree([3,1,5,0,2,4,6]))
assert Solution().isValidBST(build_tree([2,1,3]))
assert Solution().isValidBST(build_tree([5,4,6,None,None,3,7])) is False    # 5 > 3
assert Solution().isValidBST(build_tree([4,1,5,None,None,3,6])) is False    # 5 > 4
assert Solution().isValidBST(build_tree([4,1,6,None,None,5,7]))
assert Solution().isValidBST(build_tree([3,1,20,None,None,15,7])) is False  # 20 < 7
assert Solution().isValidBST(build_tree([3,1,20,None,None,15,27]))
assert Solution().isValidBST(build_tree([2,1,3,4,None,None,5])) is False    # 4 > 1
assert Solution().isValidBST(build_tree([120,70,140,50,100,130,160,20,55,75,109,119,135,150,200])) is False
assert Solution().isValidBST(build_tree([120,70,140,50,100,130,160,20,55,75,109,121,135,150,200]))
assert Solution().isValidBST(build_tree([1]))

print("TESTS PASSED")