import threading

CASES = []


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def t_single_thread(sol):
    clk = Clock(0)
    c = sol.LockedTTLCache(2, clk)
    c.put("a", 1, 10)
    c.put("b", 2, 10)
    assert c.get("a") == 1
    c.put("c", 3, 10)
    assert c.get("a") is None
    assert c.get("c") == 3


def t_thread_hammer(sol):
    """Many threads get/put; must not raise; final key readable."""
    clk = Clock(0)
    c = sol.LockedTTLCache(32, clk)
    errors = []

    def worker(i):
        try:
            for j in range(50):
                c.put(f"k{i % 16}", i + j, 1000)
                _ = c.get(f"k{i % 16}")
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors
    # something should be present under long TTL
    assert any(c.get(f"k{i}") is not None for i in range(16))


def t_lock_present(sol):
    clk = Clock(0)
    c = sol.LockedTTLCache(1, clk)
    assert hasattr(c, "_lock") or hasattr(c, "lock")


TESTS = [t_single_thread, t_thread_hammer, t_lock_present]
