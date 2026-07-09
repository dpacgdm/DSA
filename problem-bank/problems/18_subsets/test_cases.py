PRIMARY = "subsets"

def _norm(lists):
    return sorted(tuple(sorted(x)) for x in lists)

def test_basic(sol):
    assert _norm(sol.subsets([1, 2, 3])) == _norm(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    )

def test_one(sol):
    assert _norm(sol.subsets([0])) == _norm([[], [0]])

def test_empty(sol):
    assert sol.subsets([]) == [[]]

def test_count(sol):
    assert len(sol.subsets([1, 2, 3, 4])) == 16

TESTS = [test_basic, test_one, test_empty, test_count]
CASES = []
