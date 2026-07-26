# TTL / EXPIRING CACHE + RATE LIMITER (CODING)

**Module:** Coverage — Netflix/Meta product-coding gap close  
**Status:** `content-delivered`  
**Language:** Python  
**Prerequisite:** Hash maps, heaps (optional), LRU (`Design/Design Data Structures.md` Part 15)  
**Out of scope:** Full distributed rate limiting / Redis — this is **phone-screen coding**, not Phase C system design.

> **Lesson contract:** Framework + ≤3 traced exemplars. Drill via spine + problem-bank. Teach-back before retention.

---

# PART 1: WHY THESE SHOW UP

Netflix/Meta-style screens often ask **mini products**, not LC 146 verbatim:

| Prompt flavor | What they want |
|---|---|
| “Cache with TTL / auto-expire” | Hash map + time; lazy or proactive eviction |
| “Weighted / size-limited cache” | Capacity by bytes/weight, not just entry count |
| “Rate limiter” | Allow N events per window; exact semantics stated |
| “Thread-safe LRU” | Same structure + lock discipline (mention; code optional) |

**DSA under the hoodie:** hash map, ordered structure or heap of expiries, sliding/fixed window counters.

---

# PART 2: TTL / EXPIRING KEY-VALUE CACHE

## API (typical)

```python
class TTLCache:
    def __init__(self, capacity: int): ...
    def put(self, key, value, ttl_seconds: float) -> None: ...
    def get(self, key): ...  # return value or None if missing/expired
```

Wall clock: inject `time_fn` (default `time.time`) so tests can freeze time.

## Framework

```
STATE:  map[key] -> (value, expire_at)
CAPACITY: on put, if new key and full → evict (LRU or arbitrary — ASK)
GET:    if missing or now >= expire_at → miss (and delete lazy)
PUT:    store expire_at = now + ttl; may refresh TTL on update (ASK)
```

### Lazy vs eager expiry

| Style | How | Interview default |
|---|---|---|
| **Lazy** | Check on `get`/`put` | Prefer — simple, O(1) |
| **Eager** | Background / heap of expiries | Mention for “always reclaim memory” follow-up |

### Worked: lazy TTL map (no LRU — capacity by count, FIFO/arbitrary eviction)

```python
import time

class TTLCache:
    def __init__(self, capacity: int, time_fn=time.time):
        self.cap = capacity
        self.time = time_fn
        self.data: dict = {}  # key -> (value, expire_at)

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
            # eviction policy — state it: here arbitrary/oldest insertion order (Py3.7+ dict)
            oldest = next(iter(self.data))
            del self.data[oldest]
        self.data[key] = (value, now + ttl_seconds)
```

**Interview line:** “Lazy expiry on access; capacity eviction separate from TTL; I’ll confirm whether `put` refreshes TTL and which key to evict.”

### Upgrade path (speak, don’t overbuild)

1. + LRU order among live keys → hash + DLL like LC 146, expire check on get  
2. + expiry heap `(expire_at, key)` for eager purge  
3. + weight capacity → track `total_weight`, evict until fits  

---

# PART 3: RATE LIMITER (CODING)

Clarify **before** code:

1. Fixed window vs sliding window vs token bucket?  
2. Per-user or global?  
3. `allow()` returns bool, or also retry-after?

## A — Fixed window (simplest)

```python
class FixedWindowLimiter:
    def __init__(self, limit: int, window_seconds: float, time_fn=time.time):
        self.limit, self.window, self.time = limit, window_seconds, time_fn
        self.bucket_id = None
        self.count = 0

    def allow(self) -> bool:
        now = self.time()
        bid = int(now // self.window)
        if bid != self.bucket_id:
            self.bucket_id, self.count = bid, 0
        if self.count >= self.limit:
            return False
        self.count += 1
        return True
```

**Trap:** burst at window boundaries (2× limit across edge). Say it out loud.

## B — Sliding window log (exact, memory O(limit))

```python
from collections import deque

class SlidingWindowLogLimiter:
    def __init__(self, limit: int, window_seconds: float, time_fn=time.time):
        self.limit, self.window, self.time = limit, window_seconds, time_fn
        self.q = deque()  # timestamps of allowed events

    def allow(self) -> bool:
        now = self.time()
        while self.q and self.q[0] <= now - self.window:
            self.q.popleft()
        if len(self.q) >= self.limit:
            return False
        self.q.append(now)
        return True
```

## C — Token bucket (smooth)

```python
class TokenBucket:
    def __init__(self, rate: float, burst: float, time_fn=time.time):
        self.rate, self.burst, self.time = rate, burst, time_fn
        self.tokens = burst
        self.updated = time_fn()

    def allow(self, cost: float = 1.0) -> bool:
        now = self.time()
        elapsed = now - self.updated
        self.updated = now
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True
```

---

# PART 4: CONCURRENCY NOTE (SPEAKABLE, SHORT)

Phase A stays single-threaded by default. If asked for **thread-safe LRU/TTL**:

1. One `threading.Lock` (or `RLock`) around all public methods  
2. Do not call user code while holding the lock  
3. TTL check + read must be atomic w.r.t. writers  

```python
import threading

class LockedTTLCache:
    def __init__(self, inner: TTLCache):
        self.inner = inner
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            return self.inner.get(key)

    def put(self, key, value, ttl_seconds: float):
        with self.lock:
            self.inner.put(key, value, ttl_seconds)
```

**Not required for Phase A gates** unless the timed set labels it. Still worth 90 seconds of talk track for Netflix-style screens.

---

# PART 5: TEACH-BACK

1. Lazy vs eager expiry — when does lazy leak memory?  
2. Why fixed windows double-burst at boundaries?  
3. Sliding log vs token bucket — which matches “≤N in any rolling second”?  
4. What do you ask before coding a weighted cache?

---

# PART 6: PRACTICE

| Problem | Where |
|---|---|
| TTL cache | bank `68_ttl_cache` |
| Sliding rate limiter | bank `69_rate_limiter` |
| LRU (baseline) | bank `26_lru_cache` |
| TimeMap | Design lesson + spine |

**Spine:** Coverage § Design / Chill-Interview gap rows.
