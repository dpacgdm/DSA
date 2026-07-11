CASES = []

def t1(sol):
    TN = sol.TreeNode
    r = TN(1, TN(2), TN(3))
    assert sol.max_path_sum(r) == 6

def t2(sol):
    TN = sol.TreeNode
    r = TN(-10, TN(9), TN(20, TN(15), TN(7)))
    assert sol.max_path_sum(r) == 42

TESTS = [t1, t2]
