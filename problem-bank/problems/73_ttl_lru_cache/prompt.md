# TTL + LRU Cache

Capacity-limited cache that is **both**:
1. **LRU** among currently stored keys (get/put refresh recency)
2. **TTL** per entry (lazy expiry on access)

## Rules

- `get(key)` → value or `None` if missing **or** expired (delete on expire).
- Successful `get` marks key as most-recently-used.
- `put(key, value, ttl_seconds)` inserts/updates value and expiry `now+ttl`.
- Update of existing key refreshes value, TTL, **and** MRU position.
- If inserting a **new** key and at capacity: first purge expired keys; if still full, evict **LRU** among remaining.
- Inject `time_fn` for deterministic tests.

## API

```python
class TTLLRUCache:
    def __init__(self, capacity: int, time_fn): ...
    def get(self, key) -> object | None: ...
    def put(self, key, value, ttl_seconds: float) -> None: ...
```
