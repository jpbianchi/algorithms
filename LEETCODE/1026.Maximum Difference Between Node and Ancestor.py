# Given the root of a binary tree, find the maximum value v for which there 
# exist different nodes a and b where v = |a.val - b.val| and a is an ancestor of b. 
# 
#  A node a is an ancestor of b if either: any child of a is equal to b or any 
# child of a is an ancestor of b. 
# Example 1: 
#  
#  
# Input: root = [8,3,10,1,6,null,14,null,null,4,7,13]
# Output: 7
# Explanation: We have various ancestor-node differences, some of which are 
# given below :
# |8 - 3| = 5
# |3 - 7| = 4
# |8 - 1| = 7
# |10 - 13| = 3
# Among all possible differences, the maximum value of 7 is obtained by |8 - 1| 
# = 7. 
# 
# Example 2: 
# Input: root = [1,null,2,null,0,3]
# Output: 3
#  
# Constraints: 
# 
#  
#  The number of nodes in the tree is in the range [2, 5000]. 
#  0 <= Node.val <= 10⁵ 
#
#  Related Topics Tree Depth-First Search Binary Tree 👍 3740 👎 88
from typing import Optional, Union
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxAncestorDiff1(self, root: Optional[TreeNode]) -> int:
        # we do breadth first search but we propagate the node roots downwards
        # we do not do by recurrence: it would be easier but it will put the whole tree in
        # memory so this solution should be easy on memory (in case they give a huge tree)
        # it beat 98% of people on leetcode on memory, but only 5% in speed

        def dropRoot(node: TreeNode, current_max: int) -> tuple[list[TreeNode], int]:
            # we calculate the distance between all the values in the node and it's two leafs
            # then we add its value in a list in both leafs (and repeat)
            # we have to assume that the node already has a list of values in val

            if isinstance(node.val, list):
                # after the root, all nodes.val is a list because we build it here
                node_val = node.val
            else:
                # the root will give an integer
                node_val = [node.val]

            if node.left is not None:

                left_maxs = [abs(v - node.left.val) for v in node_val]
                left_tree = [TreeNode(val=node_val + [node.left.val],
                                      left=node.left.left, right=node.left.right)]
            else:
                left_maxs, left_tree = [0], []

            if node.right is not None:
                right_maxs = [abs(v - node.right.val) for v in node_val]
                right_tree = [TreeNode(val=node_val + [node.right.val],
                                       left=node.right.left, right=node.right.right)]
            else:
                right_maxs, right_tree = [0], []

            return left_tree + right_tree, max(current_max, *left_maxs, *right_maxs)

        current_max = 0
        nodes = [root]

        while nodes:
            newnodes, current_max = dropRoot(nodes.pop(0), current_max)

            nodes += newnodes

        return current_max

    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:

        def dropRoot(node: TreeNode, current_max: int) -> tuple[list[TreeNode], int]:
            # the first version was calculating all the differences with the node.val
            # this is time consuming and useless since it will always be the distance
            # from the minimum or maximum values, so let's implement that
            # we already know that the distance between min and max has already been computed
            # since they are nodes 'from above' and if new node is in between, we can ignore it

            # NOW I HAVE TOP SPEED (4S went down to 60ms) and still beat 95% of people in memory

            def processSide(node: TreeNode, nodeleft: Union[TreeNode, int, None]) \
                    -> tuple[list[TreeNode], int]:

                # at some point, node.left will be, not a TreeNode, but a value of a leaf
                if nodeleft is not None:
                    # even leaves are TreeNodes
                    newmin = min([nodeleft.val, node.val[0]])
                    newmax = max([nodeleft.val, node.val[1]])
                    newval = [newmin, newmax]
                    left_max = newmax-newmin

                    left_tree = [TreeNode(val=newval, left=nodeleft.left, right=nodeleft.right)]

                else:
                    #  we reached a leaf, its val has already been processed, get out
                    left_max, left_tree = 0, []

                return left_tree, left_max

            left_tree, left_max = processSide(node, node.left)
            right_tree, right_max = processSide(node, node.right)

            return left_tree + right_tree, max(current_max, left_max, right_max)

        current_max = 0
        root.val = [root.val, root.val]  # to have same [min, max] format expected
        nodes = deque([root])

        while nodes:
            newnodes, current_max = dropRoot(nodes.popleft(), current_max)

            nodes += newnodes

        return current_max

    def maxAncestorDiff4(self, root: Optional[TreeNode]) -> int:
        # testing another guys's solution
        # it said it was running in 33ms, but now it takes 92 so it's slower than mine
        # and beats 19% and memory is horrible, it beats 28% of people
        self.max_diff = -1

        def dfs(root, max_val, min_val):
            if not root:
                return

            if max_val < root.val:
                max_val = root.val
            if min_val > root.val:
                min_val = root.val

            self.max_diff = max(self.max_diff, max_val - min_val)

            dfs(root.left, max_val, min_val)
            dfs(root.right, max_val, min_val)

        dfs(root, root.val, root.val)
        return self.max_diff

    def maxAncestorDiff5(self, root: Optional[TreeNode]) -> int:
        # testing another guys's GREAT solution
        # great result too: 68ms, and beats 95% in memory
        # so as we can see from code above, recursivity is bad for memory
        # this guy does what I did but better with collections.deque
        queue, res = deque([(root, root.val, root.val)]), 0

        while queue:
            p, maxs, mins = queue.popleft()
            res = max(res, maxs - mins)
            if p.left:
                queue.append((p.left, max(maxs, p.left.val), min(mins, p.left.val)))
            if p.right:
                queue.append((p.right, max(maxs, p.right.val), min(mins, p.right.val)))
        return res


# leetcode submit region end(Prohibit modification and deletion)

def p(tree: list) -> TreeNode:
    ''' Turns the list into a full tree, and returns the root '''
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

# leetcode tests use real nodetrees, but we are given a string for evaluation
assert Solution().maxAncestorDiff(p([8,3,10,1,6,None,14,None,None,4,7,13])) == 7
assert Solution().maxAncestorDiff(p([1,None,2,None,0,3])) == 3
print('TESTS PASSED')