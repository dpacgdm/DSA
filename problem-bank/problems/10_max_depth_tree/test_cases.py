PRIMARY = "max_depth"

def _d(sol, vals):
    return sol.max_depth(sol.tree_from_list(vals))

CASES = []

def test_example(sol):
    assert _d(sol, [3, 9, 20, None, None, 15, 7]) == 3

def test_skew(sol):
    assert _d(sol, [1, None, 2]) == 2

def test_empty(sol):
    assert _d(sol, []) == 0

def test_single(sol):
    assert _d(sol, [1]) == 1

TESTS = [test_example, test_skew, test_empty, test_single]
