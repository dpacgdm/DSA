CASES = []

def _ser(root):
    if not root:
        return None
    return [root.val, _ser(root.left), _ser(root.right)]

def t1(sol):
    TN = sol.TreeNode
    r = TN(4, TN(2, TN(1), TN(3)), TN(7, TN(6), TN(9)))
    out = sol.invert_tree(r)
    assert _ser(out) == [4, [7, [9, None, None], [6, None, None]], [2, [3, None, None], [1, None, None]]]

def t2(sol):
    assert sol.invert_tree(None) is None

TESTS = [t1, t2]
