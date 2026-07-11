PRIMARY = "find_order"
def t1(sol):
    got = sol.find_order(2, [[1,0]])
    assert got == [0,1]
def t2(sol):
    got = sol.find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    assert got in ([0,1,2,3],[0,2,1,3])
def t3(sol):
    assert sol.find_order(2, [[0,1],[1,0]]) == []
TESTS = [t1,t2,t3]
