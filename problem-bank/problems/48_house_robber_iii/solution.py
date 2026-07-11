class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def rob(root):
    def dfs(node):
        if not node:
            return 0, 0
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        return node.val + ls + rs, max(lr, ls) + max(rr, rs)
    return max(dfs(root))
