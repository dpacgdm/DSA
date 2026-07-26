# Locked TTL Cache (thread-safe wrapper)

Implement:
1. `TTLCache` — same lazy TTL + capacity semantics as bank `68` (inject `time_fn`).
2. `LockedTTLCache` — wraps a `TTLCache` with one `threading.Lock`; all `get`/`put` take the lock.

## API

```python
class TTLCache:
    def __init__(self, capacity: int, time_fn): ...
    def get(self, key): ...
    def put(self, key, value, ttl_seconds: float) -> None: ...

class LockedTTLCache:
    def __init__(self, capacity: int, time_fn): ...
    def get(self, key): ...
    def put(self, key, value, ttl_seconds: float) -> None: ...
```

Multi-threaded tests will hammer `LockedTTLCache` and assert no exceptions / sane reads.
