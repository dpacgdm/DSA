PRIMARY = "reverse_list"

def _rev(sol, arr):
    head = sol.list_from_array(arr)
    return sol.array_from_list(sol.reverse_list(head))

CASES = []

def test_basic(sol):
    assert _rev(sol, [1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]

def test_two(sol):
    assert _rev(sol, [1, 2]) == [2, 1]

def test_one(sol):
    assert _rev(sol, [1]) == [1]

def test_empty(sol):
    assert _rev(sol, []) == []

TESTS = [test_basic, test_two, test_one, test_empty]
