CASES = []

class Clock:
    def __init__(self, t=0.0):
        self.t = t
    def __call__(self):
        return self.t

def t1(sol):
    clk = Clock(0)
    c = sol.TTLCache(2, clk)
    c.put("a", 1, 10)
    c.put("b", 2, 10)
    assert c.get("a") == 1
    c.put("c", 3, 10)  # evicts a
    assert c.get("a") is None
    assert c.get("b") == 2
    assert c.get("c") == 3

def t2(sol):
    clk = Clock(0)
    c = sol.TTLCache(2, clk)
    c.put("a", 1, 5)
    clk.t = 5  # expired
    assert c.get("a") is None
    c.put("a", 9, 5)
    assert c.get("a") == 9

def t3(sol):
    clk = Clock(0)
    c = sol.TTLCache(1, clk)
    c.put("x", 1, 100)
    clk.t = 50
    assert c.get("x") == 1
    c.put("y", 2, 100)  # evict x
    assert c.get("x") is None and c.get("y") == 2

TESTS = [t1, t2, t3]
