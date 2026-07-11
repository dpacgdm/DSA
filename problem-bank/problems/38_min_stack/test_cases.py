def t1(sol):
    m = sol.MinStack()
    m.push(-2); m.push(0); m.push(-3)
    assert m.get_min() == -3
    m.pop()
    assert m.top() == 0
    assert m.get_min() == -2
TESTS = [t1]
