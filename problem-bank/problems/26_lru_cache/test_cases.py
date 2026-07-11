def _script(sol):
    C = sol.LRUCache
    c = C(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

def _cap1(sol):
    C = sol.LRUCache
    c = C(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2

def _update(sol):
    C = sol.LRUCache
    c = C(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(1) == 10

TESTS = [_script, _cap1, _update]
