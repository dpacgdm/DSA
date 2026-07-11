PRIMARY = "three_sum"
def t1(sol):
    got = sol.three_sum([-1,0,1,2,-1,-4])
    assert frozenset(tuple(x) for x in got) == frozenset([(-1,-1,2),(-1,0,1)])
def t2(sol):
    assert sol.three_sum([0,1,1]) == []
def t3(sol):
    assert sol.three_sum([0,0,0]) == [[0,0,0]]
TESTS = [t1, t2, t3]
