# https://leetcode.com/problems/clone-graph
# @lc app=leetcode id=133 lang=python3
#
# [133] Clone Graph
#
# Category	    Difficulty	   Likes	Dislikes
# algorithms	Medium (51.11%)	7162	2927
# Tags
# Companies
# Given a reference of a node in a connected undirected graph.

# Return a deep copy (clone) of the graph.

# Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

# class Node {
#     public int val;
#     public List<Node> neighbors;
# }
 
# Test case format:

# For simplicity, each node's value is the same as the node's index (1-indexed). For example, the 
# first node with val == 1, the second node with val == 2, and so on. The graph is represented in 
# the test case using an adjacency list.

# An adjacency list is a collection of unordered lists used to represent a finite graph. Each list 
# describes the set of neighbors of a node in the graph.

# The given node will always be the first node with val = 1. You must return the copy of the given 
# node as a reference to the cloned graph.

# Example 1:

# Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
# Output: [[2,4],[1,3],[2,4],[1,3]]
# Explanation: There are 4 nodes in the graph.
# 1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
# 2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
# 3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
# 4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
# Example 2:


# Input: adjList = [[]]
# Output: [[]]
# Explanation: Note that the input contains one empty list. The graph consists of only one node 
# with val = 1 and it does not have any neighbors.
# Example 3:

# Input: adjList = []
# Output: []
# Explanation: This an empty graph, it does not have any nodes.
 
# Constraints:

# The number of nodes in the graph is in the range [0, 100].
# 1 <= Node.val <= 100
# Node.val is unique for each node.
# There are no repeated edges and no self-loops in the graph.
# The Graph is connected and all nodes can be visited starting from the given node.

# @lc code=start
from typing import List
from collections import deque
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph1(self, node: 'Node') -> 'Node':
        """ Since each node comes with its adjList, we explore that list while creating
            new nodes along the way.  We need a dictionary to keep track of created nodes.
            We will keep passing nodes by reference to easily update them inside the dictionary.
            Beats 90% in time, 26% in memory
        """
        if node is None:
            return None
        origin = node.val
        
        nodes = {node.val:Node(node.val)}
        adjnodes = deque([(nodes[node.val], node.neighbors)])
        
        # we will follow this pattern: save a new node with val, and its neighbors
        # so we can assume that the node already exists when we pop the queue
        # and we have to create fresh neighbors if they don't already exist
        while adjnodes:
            node, neighbors = adjnodes.popleft()
    
            for neighbor in neighbors:
                
                # create nodes for neighbors if they don't exist
                if neighbor.val not in nodes:
                    nodes[neighbor.val] = Node(val=neighbor.val)
                    adjnodes.append((nodes[neighbor.val], neighbor.neighbors))
                
                # now we must add the neighbor to the node if it doesn't exist yet
                if nodes[neighbor.val] not in node.neighbors:
                    node.neighbors.append(nodes[neighbor.val])

        return nodes[origin]
        
        
    def cloneGraph2(self, node: 'Node') -> 'Node':
        """ We don't need to use node.val as a key, we could use a node since a class is hashable
            Let's try to use another dict {oldnode:newnode}
        """
        if node is None:
            return None
        
        nodes = {node:Node(node.val)}
        adjnodes = deque([(nodes[node], node.neighbors)])
        root = nodes[node]
        
        while adjnodes:
            node, neighbors = adjnodes.popleft()
    
            for neighbor in neighbors:
                
                # create nodes for neighbors if they don't exist
                if neighbor not in nodes:
                    nodes[neighbor] = Node(val=neighbor.val)
                    adjnodes.append((nodes[neighbor], neighbor.neighbors))
                
                # now we must add the neighbor to the node if it doesn't exist yet
                if nodes[neighbor] not in node.neighbors:
                    node.neighbors.append(nodes[neighbor])

        return root
    
    
    def cloneGraph(self, node: 'Node') -> 'Node':
        """ Let's try DFS
            Beats 75% cpu, 25% memory
        """
        if node is None:
            return None
        
        nodes = {}  # oldNode:newNode
        
        def DFS(node):
            """ Here, we create the new node if it doesn't exist, then
                we explore the neighbors recursively (=DFS)
            """
            if node not in nodes:
                nodes[node] = Node(val=node.val)
                
            if not node.neighbors:
                # we reached a leaf, nothing more to do
                return
            
            for neighbor in node.neighbors:
                
                if neighbor not in nodes:
                    # if neighbord was not visited, explore it (DFS)
                    DFS(neighbor)   # will create nodes[neighbor]
                    
                if nodes[neighbor] not in nodes[node].neighbors:
                    nodes[node].neighbors.append(nodes[neighbor])

        DFS(node)
        return nodes[node]
        
# @lc code=end

# NO TESTS because too much work to build a graph from a given list, then build the adjList from the solution
# It passed on Leetcode at first try

                
                
            