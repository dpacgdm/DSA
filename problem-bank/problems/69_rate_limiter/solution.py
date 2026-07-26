from collections import deque

class SlidingWindowLogLimiter:
    def __init__(self, limit: int, window_seconds: float, time_fn):
        self.limit = limit
        self.window = window_seconds
        self.time = time_fn
        self.q = deque()

    def allow(self) -> bool:
        now = self.time()
        while self.q and self.q[0] <= now - self.window:
            self.q.popleft()
        if len(self.q) >= self.limit:
            return False
        self.q.append(now)
        return True
