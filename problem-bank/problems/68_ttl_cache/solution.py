class TTLCache:
    def __init__(self, capacity: int, time_fn):
        self.cap = capacity
        self.time = time_fn
        self.data = {}  # key -> (value, expire_at)

    def _alive(self, key) -> bool:
        if key not in self.data:
            return False
        _, exp = self.data[key]
        if self.time() >= exp:
            del self.data[key]
            return False
        return True

    def get(self, key):
        if not self._alive(key):
            return None
        return self.data[key][0]

    def put(self, key, value, ttl_seconds: float) -> None:
        now = self.time()
        if key not in self.data and len(self.data) >= self.cap:
            # purge expired first
            for k in list(self.data):
                self._alive(k)
            if key not in self.data and len(self.data) >= self.cap:
                oldest = next(iter(self.data))
                del self.data[oldest]
        self.data[key] = (value, now + ttl_seconds)
