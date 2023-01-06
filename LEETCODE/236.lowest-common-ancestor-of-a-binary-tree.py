# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
# @lc app=leetcode id=236 lang=python3
#
# [236] Lowest Common Ancestor of a Binary Tree
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (58.25%)	13208	317
# Tags
# tree

# Companies
# amazon | apple | facebook | linkedin | microsoft

# Given a binary tree, find the lowest common ancestor (LCA) of two given nodes 
# in the tree.

# According to the definition of LCA on Wikipedia: “The lowest common ancestor 
# is defined between two nodes p and q as the lowest node in T that has both p and q 
# as descendants (where we allow a node to be a descendant of itself).”

# Example 1:

# Input: root = [3,5,1,6,2,0,8,None,None,7,4], p = 5, q = 1
# Output: 3
# Explanation: The LCA of nodes 5 and 1 is 3.
# Example 2:

# Input: root = [3,5,1,6,2,0,8,None,None,7,4], p = 5, q = 4
# Output: 5
# Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of 
# itself according to the LCA definition.
# Example 3:

# Input: root = [1,2], p = 1, q = 2
# Output: 1

# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
from collections import deque
class Solution:
    def lowestCommonAncestor1(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """ We must do DFS because we must find a path that has p and q, otherwise it's 
            the root.
            An interesting way to do this is to propagate the node value downstream
            Go through the tree and find the path to p and q. Then compare the
            paths and find the first node that is different.
            Beats 99% in cpu
        """
        if root.val in [p,q]:
            return root.val
    
        def ancestor(node,p,q):
            """ Returns ancestor of p and q on the left or right side of node
                When I meet p or q on my way up, I propagate -p or -q
                to be able to tell if I've met both p and q or only one of them
                It works except with zero, since -0 == 0
            """
            
            # first we dig to the bottom of tree
            # maybe we will cross p and q but if we don't track if we've met
            # one of them, we won't know if we've met both of them
            # so we must go to the leaves and then come back up
            ans1 = None
            if node.left is not None:
                ans1 = ancestor(node.left, p, q)
                if isinstance(ans1, str):
                    return ans1 # we found it, no need to go further
                # here, we're climbing back the tree after reaching the leaves
                if ans1 in [p,q]:
                    return str(ans1)
                if ans1 in [-p,-q] and node.left.val in [p,q]:
                    # we just met the 2nd number in the same subtree
                    return str(node.left.val) 
                elif ans1 not in [-p,-q] and node.left.val in [p,q]:
                    ans1 = -node.left.val

                
            ans2 = None
            if node.right is not None:
                ans2 = ancestor(node.right, p, q)
                if isinstance(ans2, str):
                    return ans2 
                if ans2 in [p,q]:
                    return str(ans2)
            
                if ans2 in [-p,-q] and node.right.val in [p,q]:
                    return str(node.right.val) 
                elif ans2 not in [-p,-q] and node.right.val in [p,q]:
                    ans2 = -node.right.val

            
            # if we get here, it means p and q may come from left and right subtrees
            if {ans1, ans2} == {-p,-q}:
                # we found both p and q, but in left and right subtrees
                return str(node.val)  # string to signal we found it
            
            if ans1 in [-p,-q]:
                # we already tested if node.val was p or q
                return ans1
            elif ans2 in [-p,-q]:
                return ans2
            return None
    
            
        return int(ancestor(root, p, q))

    def lowestCommonAncestor2(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """ Let's use DFS to find the paths from the root to p and q 
            This solution was totally created by Github Pilot and it worked straight away
            Now, let's do it on my own
        """
 
        def find_path(node, target, path):
            """ DFS to find the path from node to target """
            if node is None:
                return False
            path.append(node.val)
            if node.val == target:
                return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            path.pop()
            return False
        
        path_p = []
        path_q = []
        find_path(root, p, path_p)
        find_path(root, q, path_q)
        # print(path_p, path_q)
        for i in range(min(len(path_p), len(path_q))):
            if path_p[i] != path_q[i]:
                return path_p[i-1]
        return path_p[i]
    
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """ Let's use DFS to find the paths from the root to p and q 
            Beasts 92% cpu, 12% memory
        """
        
        def pathDFS(node: TreeNode, p: TreeNode, path):
            
            if node is None:
                # we reached a leaf without finding p
                return False 
            
            if node.val == p:   # replace by node.left is p for Leetcode
                path.append(node.val)
                # we found p, so let's roll back up now by returning True
                return True
            
            if pathDFS(node.left, p,path) or pathDFS(node.right, p, path):
                # p can only be in one path
                # node.right or node.left has already been added to the path
                # by if node.val == p: above, so we just add node.val
                path.append(node.val)
                return True
            else:
                return False
            
        pathp, pathq = [], []
        # we pass a mutable list so pathDFS can update it without having
        # to create new lists at every iteration
        foundp = pathDFS(root, p, pathp)
        foundq = pathDFS(root, q, pathq)
        
        if not foundp or not foundq:
            raise Exception("This should not happen: p or q not found")
        
        # let's find common ancestor by scanning the paths
        # which means finding the last node the have in common, 
        # before we meet p or q
        # keep in mind, the paths are in reverse order, pathp starts with p
        if q in pathp[1:]:
            return q
        if p in pathq[1:]:
            return p
        # now we know that p is not in pathq and q is not in pathp
        # lets find the first node that is in both paths
        # we can process only one path since we know the solution is in both
        # we could use the shortes path, but it's not worth the effort
        # since it happens only once at the end
        while pathp[0] not in pathq:
            pathp.pop(0)       
        
        return pathp[0]

    def lowestCommonAncestor99(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """ One of the best solution on Leetcode 64ms instead of my 77ms """
        if not root or root==p or root==q:
            return root
        l=self.lowestCommonAncestor(root.left,p,q)
        r=self.lowestCommonAncestor(root.right,p,q)
        if l and r:
            return root
        if l:
            return l
        return r
    
    def lowestCommonAncestor98(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """ One of the best solution on Leetcode 20MB instead of my 26MB  
            They didn't use paths, but one global variable 
            but they compute lcaRecurse for left and right nodes when it may not be necessary
            when p is ancestor of q, or vice versa 
        """
        global lca
        lca = None
        def lcaRecurse(root):
            global lca
            if not root or lca:
                return False
            left = lcaRecurse(root.left)
            right = lcaRecurse(root.right)
            if left and right or ((root.val == p.val or root.val == q.val) and (left or right)):
                lca = root
            return left or right or root.val == p.val or root.val == q.val
        lcaRecurse(root)
        return lca

    """ p and q are not integers but TREENODES... and we must return a TREENODE for Leetcode """
 

# @lc code=end
from helpers import build_tree as bt
# print(Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 6, 8)) # 5
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 5, 6) == 5
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 6, 5) == 5
# print(Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 5, 1)) # 3
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 5, 1) == 3
# print(Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 5, 4)) # 5
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,None,None,7,4]), 5, 4)
# print(Solution().lowestCommonAncestor(bt([1,2]), 1, 2)) # 1
assert Solution().lowestCommonAncestor(bt([1,2]), 1, 2) == 1
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,9,None,7,4,None,11,None,None,None,12]), 8, 12) == 3
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,9,None,7,4,None,11,None,None,None,12]), 4, 12) == 5
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,9,None,7,4,None,11,None,None,None,12]), 2, 12) == 5
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,9,None,7,4,None,11,None,None,None,12]), 12, 11) == 3
assert Solution().lowestCommonAncestor(bt([3,5,1,6,2,0,8,9,None,7,4,None,11,None,None,None,12]), 5, 0) == 3

print("TESTS PASSED")
