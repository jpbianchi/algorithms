from typing import List
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
def build_tree(tree: list, verbose=False) -> TreeNode:
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
    if verbose:
        print(f"Tree has {cnt} nodes")

    return root


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
def linked_to_list(head: ListNode) -> List[int]:
    ''' Turns a linked list into a list '''
    lst = []
    while head.next is not None:
        lst.append(head.val)
        head = head.next
    lst.append(head.val)
    return lst

def list_to_linked(lst: List[int]) -> ListNode:
    ''' Turns a list into a linked list '''
    head = ListNode(val=lst.pop(0))
    node = head
    while lst:
        node.next = ListNode(val=lst.pop(0))
        node = node.next
    return head

if __name__ == "__main__":

    assert linked_to_list(list_to_linked([1,2,3])) == [1,2,3]