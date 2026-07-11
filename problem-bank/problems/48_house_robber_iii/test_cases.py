CASES = []

def t1(sol):
    TN = sol.TreeNode
    r = TN(3, TN(2, None, TN(3)), TN(3, None, TN(1)))
    assert sol.rob(r) == 7

def t2(sol):
    assert sol.rob(None) == 0

TESTS = [t1, t2]
