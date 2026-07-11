CASES = []

def t1(sol):
    TN = sol.TreeNode
    assert sol.is_valid_bst(TN(2, TN(1), TN(3))) is True

def t2(sol):
    TN = sol.TreeNode
    r = TN(5, TN(1), TN(4, TN(3), TN(6)))
    assert sol.is_valid_bst(r) is False

def t3(sol):
    assert sol.is_valid_bst(None) is True

TESTS = [t1, t2, t3]
