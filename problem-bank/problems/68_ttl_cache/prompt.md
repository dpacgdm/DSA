# TTL Cache (expiring key-value)

Implement a capacity-limited cache with per-key TTL (seconds).
`get` returns the value or `None` if missing/expired (lazy expiry).
`put` inserts/updates; if inserting a **new** key at capacity, evict the oldest inserted still-present key (dict insertion order).
Updating an existing key refreshes value + TTL and does **not** change insertion order for eviction (simple rule for this bank).

Time is injectable via `time_fn` on the constructor for tests.

## API
```python
class TTLCache:
    def __init__(self, capacity: int, time_fn=...): ...
    def get(self, key) -> object | None: ...
    def put(self, key, value, ttl_seconds: float) -> None: ...
```
