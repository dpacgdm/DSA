def test_basic(sol):
    s = sol.RandomizedSet()
    assert s.insert(1) is True
    assert s.remove(2) is False
    assert s.insert(2) is True
    assert s.get_random() in {1, 2}
    assert s.remove(1) is True
    assert s.insert(2) is False
    assert s.get_random() == 2

def test_remove_last(sol):
    s = sol.RandomizedSet()
    s.insert(10)
    s.insert(20)
    assert s.remove(20) is True
    assert s.get_random() == 10
    assert s.remove(10) is True
    assert s.insert(10) is True

def test_swap_remove_middle(sol):
    s = sol.RandomizedSet()
    for v in (1, 2, 3):
        s.insert(v)
    assert s.remove(2) is True
    assert set(s.vals) == {1, 3}
    assert 2 not in s.idx

TESTS = [test_basic, test_remove_last, test_swap_remove_middle]
CASES = []
