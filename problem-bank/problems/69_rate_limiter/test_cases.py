CASES = []

class Clock:
    def __init__(self, t=0.0):
        self.t = t
    def __call__(self):
        return self.t

def t1(sol):
    clk = Clock(0)
    lim = sol.SlidingWindowLogLimiter(2, 10, clk)
    assert lim.allow() is True
    assert lim.allow() is True
    assert lim.allow() is False
    clk.t = 10
    assert lim.allow() is True

def t2(sol):
    clk = Clock(100)
    lim = sol.SlidingWindowLogLimiter(1, 5, clk)
    assert lim.allow() is True
    clk.t = 104
    assert lim.allow() is False
    clk.t = 105
    assert lim.allow() is True

TESTS = [t1, t2]
