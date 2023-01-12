from typing import List
import time

def timeit(prec=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end-start:.{prec}f} seconds")
            return result
        return wrapper
    return decorator

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
        # there is already a None in the node left or right because
        # it was initialized that way
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

def tree_to_list(root: TreeNode, DEBUG: bool = False) -> List[int]:

    def p(lst: List, msg: str = 'Q:'):
        print(msg, [node.val if node is not None else None for node in lst])
        
        
    def ansappend(node):
        ans.append(node)
        if DEBUG:
            print('ans:', ans)
            
    ans = []
    
    queue = [root]
    if DEBUG:
        p(queue)

    while queue and sum([1 for node in queue if node is not None]):
        # we stop if there are only None nodes in the queue

        node = queue.pop(0)
        if DEBUG:
            p(queue)
        
        if node is None:
            # when we pop a None, we have to honor it
            # it's when we put a None in the queue, that we must check
            # if there are any non-None nodes in the queue
            ansappend(None)
            continue
        else:
            ansappend(node.val)
            queue += [node.left, node.right]
        if DEBUG:
            print('Node:', ans[-1])
            
    return ans
            

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
    
    # print(tree_to_list(build_tree([3,5,1,None,2]), DEBUG=True))
    assert tree_to_list(build_tree([3,5,1,None,2])) == [3,5,1,None,2]
                 
    # print(tree_to_list(build_tree([3,5,1,6,2,0,8,None,None,7,4]), DEBUG=True))                                                      
    assert tree_to_list(build_tree([3,5,1,6,2,0,8,None,None,7,4])) == [3,5,1,6,2,0,8,None,None,7,4]
    
    print("TESTS PASSED")