
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
