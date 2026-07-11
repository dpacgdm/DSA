PRIMARY = "pacific_atlantic"
def t1(sol):
    h = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    got = sol.pacific_atlantic(h)
    exp = [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    assert sorted(got)==exp
def t2(sol):
    assert sol.pacific_atlantic([[1]]) == [[0,0]]
TESTS = [t1,t2]
