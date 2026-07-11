class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

class Codec:
    def serialize(self, root):
        vals = []
        def dfs(node):
            if not node:
                vals.append('#'); return
            vals.append(str(node.val))
            dfs(node.left); dfs(node.right)
        dfs(root)
        return ','.join(vals)
    def deserialize(self, data):
        tokens = iter(data.split(','))
        def dfs():
            v = next(tokens)
            if v == '#':
                return None
            node = TreeNode(int(v))
            node.left = dfs(); node.right = dfs()
            return node
        return dfs()
