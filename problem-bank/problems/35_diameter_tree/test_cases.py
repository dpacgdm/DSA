CASES = []

def t1(sol):
    TN = sol.TreeNode
    r = TN(1, TN(2, TN(4), TN(5)), TN(3))
    assert sol.diameter(r) == 3

def t2(sol):
    assert sol.diameter(sol.TreeNode(1)) == 0

TESTS = [t1, t2]
