class TTLLRUCache:
    """LRU order + per-key TTL (lazy expiry)."""

    class _Node:
        __slots__ = ("key", "val", "exp", "prev", "next")

        def __init__(self, key=0, val=0, exp=0.0):
            self.key = key
            self.val = val
            self.exp = exp
            self.prev = None
            self.next = None

    def __init__(self, capacity: int, time_fn):
        self.cap = capacity
        self.time = time_fn
        self.map = {}
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_mru(self, node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _alive(self, node) -> bool:
        if self.time() >= node.exp:
            self._remove(node)
            del self.map[node.key]
            return False
        return True

    def _purge_expired(self) -> None:
        for key in list(self.map):
            node = self.map.get(key)
            if node is not None:
                self._alive(node)

    def get(self, key):
        node = self.map.get(key)
        if node is None or not self._alive(node):
            return None
        self._remove(node)
        self._add_mru(node)
        return node.val

    def put(self, key, value, ttl_seconds: float) -> None:
        now = self.time()
        exp = now + ttl_seconds
        if key in self.map:
            node = self.map[key]
            if self._alive(node):
                node.val = value
                node.exp = exp
                self._remove(node)
                self._add_mru(node)
                return

        self._purge_expired()
        if len(self.map) >= self.cap:
            lru = self.tail.prev
            if lru is not self.head:
                self._remove(lru)
                del self.map[lru.key]

        node = self._Node(key, value, exp)
        self.map[key] = node
        self._add_mru(node)
