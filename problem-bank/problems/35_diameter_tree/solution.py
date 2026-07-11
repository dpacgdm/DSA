class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        L, R = height(node.left), height(node.right)
        best = max(best, L + R)
        return 1 + max(L, R)
    height(root)
    return best
