#
# @lc app=leetcode id=2 l1ng=python3
#
# [2] Add Two Numbers
# Category	Difficulty	Likes	Dislikes
# algorithms	Medium (39.95%)	23427	4524
# Tags
# linked-list | math

# Companies
# adobe | airbnb | amazon | bloomberg | microsoft

# You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

# You may assume the two numbers do not contain any leading zero, except the number 0 itself.

# Example 1:

# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]
# Explanation: 342 + 465 = 807.
# Example 2:

# Input: l1 = [0], l2 = [0]
# Output: [0]
# Example 3:

# Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
# Output: [8,9,9,9,0,0,0,1]
 
# Constraints:

# The number of nodes in each linked list is in the range [1, 100].
# 0 <= Node.val <= 9
# It is guaranteed that the list represents a number that does not have leading zeros.

# @lc code=start
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
from typing import Optional

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """ The fact that the numbers are stored in reverse order makes it
            easier to add them. We can just go down the linked list and do an
            addition. If the sum is greater than 10, we need to carry over.
            To save memory, we'll store the result in one of the chain.
            We could try to find out the longer one, but instead we will link
            the shorter one to the rest of the longer one if we picked the wrong one.
            I even delete l2 nodes as we go along to save memory.
            Linking l1 and l2 is not obvious but it happens only once so it's ok.
        """
        # store the head of the list to return it
        l1_modified = l1
        
        # first process until the end of the shorter list (which we don't know)
        while l1.next is not None and l2.next is not None:
            # we must exit the loop with l1 or l2 still pointing to the last
            # elements otherwise we won't be able to connect to the longer list
            
            suml1l2 = l1.val + l2.val
            carry = suml1l2 // 10
            
            l1.val = suml1l2 % 10
            
            if l1.next is not None:
                l1.next.val += carry # carry over
                # we leave the carry for the next step
            
            l2temp = l2
            l1, l2 = l1.next, l2.next
            del l2temp # free memory
            
        # now process the rest of the longer list
        # there may be a carry left over from the previous step inside l1.val
        # then, we link l1 to the rest of l2 if l2 was longer
        
        # we still havent performed the last addition (l1 and l2 are not null here)
        carry = (l1.val + l2.val) // 10
        l1.val = (l1.val + l2.val) % 10
        
        if l1.next is None:
            if l2.next is None: # both lists are the same length
                if carry > 0:
                    l1.next = ListNode(val=carry)
                return l1_modified
            else: # l2 is longer
                l1.next = l2.next  # link l1 to the rest of l2
        
        # now we can propagate the carry
        l1 = l1.next # drop l1.val since we have processed it
        l1.val += carry
        
        # stop when we reach end of list or no more carry
        while l1 is not None and l1.val >= 10:
            carry = l1.val // 10
            
            if l1.next is None and carry > 0:
                l1.next = ListNode(val=0)
                
            l1.next.val += carry
            l1.val %= 10
            l1 = l1.next

        return l1_modified
        
        
# @lc code=end
from helpers import list_to_linked, linked_to_list

assert linked_to_list(Solution().addTwoNumbers(list_to_linked([2,4,3]), list_to_linked([5,6,4]))) == [7,0,8]
assert linked_to_list(Solution().addTwoNumbers(list_to_linked([2,4,3]), list_to_linked([5,6,9]))) == [7,0,3,1]
assert linked_to_list(Solution().addTwoNumbers(list_to_linked([0]), list_to_linked([0]))) == [0]
assert linked_to_list(Solution().addTwoNumbers(list_to_linked([9,9,9,9,9,9,9]), list_to_linked([9,9,9,9]))) == [8,9,9,9,0,0,0,1]
# print(linked_to_list(Solution().addTwoNumbers(list_to_linked([9,9,9,9]), list_to_linked([9,9,9,9,9,9,9]))))
assert linked_to_list(Solution().addTwoNumbers(list_to_linked([9,9,9,9]), list_to_linked([9,9,9,9,9,9,9]))) == [8,9,9,9,0,0,0,1]

print("TESTS PASSED")
