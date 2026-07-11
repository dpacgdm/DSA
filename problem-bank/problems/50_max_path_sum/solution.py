class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def max_path_sum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        L = max(0, gain(node.left))
        R = max(0, gain(node.right))
        best = max(best, node.val + L + R)
        return node.val + max(L, R)
    gain(root)
    return best
