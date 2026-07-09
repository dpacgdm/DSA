PRIMARY = "lowest_common_ancestor"

# Tree: [6,2,8,0,4,7,9,None,None,3,5]
TREE = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]

def test_split(sol):
    root = sol.tree_from_list(TREE)
    assert sol.lowest_common_ancestor(root, 2, 8) == 6

def test_same_side(sol):
    root = sol.tree_from_list(TREE)
    assert sol.lowest_common_ancestor(root, 2, 4) == 2

def test_deeper(sol):
    root = sol.tree_from_list(TREE)
    assert sol.lowest_common_ancestor(root, 3, 5) == 4

def test_order_swap(sol):
    root = sol.tree_from_list(TREE)
    assert sol.lowest_common_ancestor(root, 5, 0) == 2

TESTS = [test_split, test_same_side, test_deeper, test_order_swap]
CASES = []
