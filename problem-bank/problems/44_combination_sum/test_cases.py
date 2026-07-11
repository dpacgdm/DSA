PRIMARY = "combination_sum"
def t1(sol):
    got = sol.combination_sum([2,3,6,7], 7)
    assert frozenset(tuple(x) for x in got) == frozenset([(2,2,3),(7,)])
def t2(sol):
    got = sol.combination_sum([2,3,5], 8)
    assert frozenset(tuple(x) for x in got) == frozenset([(2,2,2,2),(2,3,3),(3,5)])
TESTS = [t1, t2]
