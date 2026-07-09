PRIMARY = "top_k_frequent"

def test_basic(sol):
    assert set(sol.top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}

def test_single(sol):
    assert sol.top_k_frequent([1], 1) == [1]

def test_all_unique(sol):
    assert set(sol.top_k_frequent([4, 5, 6], 2)).issubset({4, 5, 6})
    assert len(sol.top_k_frequent([4, 5, 6], 2)) == 2

def test_ties_ok(sol):
    got = sol.top_k_frequent([1, 2, 3, 1, 2, 3], 2)
    assert len(got) == 2
    assert set(got).issubset({1, 2, 3})

TESTS = [test_basic, test_single, test_all_unique, test_ties_ok]
CASES = []
