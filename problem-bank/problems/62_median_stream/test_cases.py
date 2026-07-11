def t1(sol):
    m=sol.MedianFinder()
    m.add_num(1); m.add_num(2)
    assert m.find_median()==1.5
    m.add_num(3)
    assert m.find_median()==2.0
TESTS=[t1]
