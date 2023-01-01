# https://leetcode.com/problems/min-stack/
# @lc app=leetcode id=155 lang=python3
#
# [155] Min Stack
#
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (52.01%)	10448	695
# Tags
# stack | design

# Companies
# amazon | bloomberg | google | snapchat | uber | zenefits

# Design a stack that supports push, pop, top, and retrieving 
# the minimum element in constant time.

# Implement the MinStack class:

# MinStack() initializes the stack object.
# void push(int val) pushes the element val onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.
# You must implement a solution with O(1) time complexity for each function.

# Example 1:

# Input
# ["MinStack","push","push","push","getMin","pop","top","getMin"]
# [[],[-2],[0],[-3],[],[],[],[]]

# Output
# [null,null,null,null,-3,null,0,-2]

# Explanation
# MinStack minStack = new MinStack();
# minStack.push(-2);
# minStack.push(0);
# minStack.push(-3);
# minStack.getMin(); // return -3
# minStack.pop();
# minStack.top();    // return 0
# minStack.getMin(); // return -2
 
# Constraints:
# -2^31 <= val <= 2^31 - 1
# Methods pop, top and getMin operations will always be called on 
# non-empty stacks.
# At most 3 * 104 calls will be made to push, pop, top, and getMin.

# @lc code=start
class MinStack:
    """ A list is ideal because we can pop and append in constant time.
        The min() function is O(n) time complexity but we can implement
        it in O(1) time complexity by keeping track of the minimum value
        along the way.
        Beats 73% cpu, and 56% memory. But leetcode accepted getMin() 
        using min() despite being O(n).
    """
    def __init__(self):
        self.stack = []
        self.min = [] # keep track of the minimum values at every step

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.min.append(val)  # works for the first element when list is empty
        if len(self.min) > 1:
            self.min[-1] = min(self.min[-2], val) 

    def pop(self) -> None:
        self.stack.pop()
        self.min.pop()
        
    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min[-1]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
# @lc code=end

