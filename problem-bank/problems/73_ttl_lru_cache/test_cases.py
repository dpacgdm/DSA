CASES = []


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def t_lru_order(sol):
    """get refreshes MRU; put of new key evicts LRU."""
    clk = Clock(0)
    c = sol.TTLLRUCache(2, clk)
    c.put("a", 1, 100)
    c.put("b", 2, 100)
    assert c.get("a") == 1  # a becomes MRU; b is LRU
    c.put("c", 3, 100)  # evicts b
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3


def t_ttl_expire(sol):
    clk = Clock(0)
    c = sol.TTLLRUCache(2, clk)
    c.put("a", 1, 5)
    c.put("b", 2, 100)
    clk.t = 5
    assert c.get("a") is None  # expired
    c.put("c", 3, 100)  # capacity free after expire; should not need to evict b
    assert c.get("b") == 2
    assert c.get("c") == 3


def t_expire_then_evict_lru(sol):
    """At capacity with all live: evict LRU. Expired do not count."""
    clk = Clock(0)
    c = sol.TTLLRUCache(2, clk)
    c.put("a", 1, 10)
    c.put("b", 2, 10)
    clk.t = 10
    # both expired; put should purge and insert without keeping ghosts
    c.put("c", 3, 10)
    assert c.get("a") is None and c.get("b") is None
    assert c.get("c") == 3


def t_update_refreshes_ttl_and_mru(sol):
    clk = Clock(0)
    c = sol.TTLLRUCache(2, clk)
    c.put("a", 1, 5)
    c.put("b", 2, 100)
    c.put("a", 9, 100)  # refresh a → MRU, long TTL
    clk.t = 5
    assert c.get("a") == 9  # still alive due to refreshed TTL
    c.put("c", 3, 100)  # evict LRU = b
    assert c.get("b") is None
    assert c.get("a") == 9


TESTS = [t_lru_order, t_ttl_expire, t_expire_then_evict_lru, t_update_refreshes_ttl_and_mru]
