# https://leetcode.com/problems/binary-tree-level-order-traversal
# @lc app=leetcode id=102 lang=python3
#
# [102] Binary Tree Level Order Traversal
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (63.58%)	11869	232
# Tags
# Companies
# Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

# Example 1:

# Input: root = [3,9,20,null,null,15,7]
# Output: [[3],[9,20],[15,7]]
# Example 2:

# Input: root = [1]
# Output: [[1]]
# Example 3:

# Input: root = []
# Output: []


# Constraints:

# The number of nodes in the tree is in the range [0, 2000].
# -1000 <= Node.val <= 1000
from collections import deque
from typing import Optional, List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# @lc code=start

class Solution:
    def levelOrder1(self, root: Optional[TreeNode]) -> List[List[int]]:
        """ 
            We're going to go BFS into the tree since we want data level by level
            Beats 97% in time, 50% in memory
        """
        if root is None:
            return []
        else:
            ans = [[root.val]]
            
        nodes = deque([[root]])
        while nodes:
            levelvals = []
            levelnodes = []
            for node in nodes.popleft():
            
                # is there a left node
                if node.left is not None:
                    levelvals.append(node.left.val)
                    levelnodes.append(node.left)
                
                # is there a right node
                if node.right is not None:
                    levelvals.append(node.right.val)
                    levelnodes.append(node.right)
                
            if levelvals:
                nodes.append(levelnodes)
                ans.append(levelvals)
        print(ans)
        return ans
    
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """ 
            Since every level creates the next level of nodes, it was
            not necessary to put them in a list levelnodes, but simply in the queue.
            We just need to count them before we keep adding the next
            level to the same queue, so we process the queue layer by layer.
        """
        if root is None:
            return []
        else:
            ans = [[root.val]]
            
        nodes = deque([root])
        while nodes:
            levelvals = []
            n = len(nodes)  # nb of nodes at this level
            for _ in range(n):
            
                node = nodes.popleft()
                # is there a left node
                if node.left is not None:
                    levelvals.append(node.left.val)
                    nodes.append(node.left)
                
                # is there a right node
                if node.right is not None:
                    levelvals.append(node.right.val)
                    nodes.append(node.right)
                
            if levelvals:
                ans.append(levelvals)
        # print(ans)
        return ans
                
        
# @lc code=end

def p(tree: list) -> TreeNode:
    ''' Turns the list into a full tree, and returns the root '''
    
    if not tree:  # empty list?
        return None
    
    root = TreeNode(val=tree.pop(0))
    nodes = [root]
    cnt = 1
    while tree:
        node = nodes.pop(0)
        newval = tree.pop(0)

        # None means there is no branch, so we simply ignore those
        if newval is not None:
            node.left = TreeNode(val=newval)
            nodes.append(node.left)
            cnt += 1
        if tree:
            newval = tree.pop(0)
            if newval is not None:
                node.right = TreeNode(val=newval)
                nodes.append(node.right)
                cnt += 1
    print(f"Tree has {cnt} nodes")

    return root

assert Solution().levelOrder(p([3,9,20,None,None,15,7])) == [[3],[9,20],[15,7]]
assert Solution().levelOrder(p([1,2,3,4,None,None,5])) == [[1],[2,3],[4,5]]
assert Solution().levelOrder(p([1])) == [[1]]
assert Solution().levelOrder(p([])) == []
print("TESTS PASSED")