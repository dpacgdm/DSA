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

### Worked trace — capacity + TTL (freeze clock)

`capacity=2`. Clock starts at `t=0`.

| Step | Op | Clock | Map after (key→(val, exp)) | Notes |
|---|---|---|---|---|
| 1 | `put(a,1,ttl=10)` | 0 | a→(1,10) | new key |
| 2 | `put(b,2,ttl=10)` | 0 | a→(1,10), b→(2,10) | full |
| 3 | `get(a)` | 0 | unchanged | hit 1 (`0 < 10`) |
| 4 | `put(c,3,ttl=10)` | 0 | b→(2,10), c→(3,10) | evict oldest `a` |
| 5 | `get(a)` | 0 | unchanged | miss |
| 6 | advance clock → 10 | 10 | — | — |
| 7 | `get(b)` | 10 | *(b deleted)* c→(3,10) | lazy expire: `10 >= 10` → miss |
| 8 | `put(b,9,ttl=5)` | 10 | c→(3,10), b→(9,15) | b reinserted |

**Say aloud:** eviction policy ≠ TTL. A live key can be evicted for capacity while another sits until touched after expiry.

### Upgrade path (speak, don’t overbuild)

1. + LRU order among live keys → hash + DLL like LC 146, expire check on get (**bank `73_ttl_lru_cache`** — implement next after plain TTL)  
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

### Worked trace — fixed window burst

`limit=2`, `window=10`. Bucket id = `floor(t / 10)`.

| t | allow? | bucket | count after | Why |
|---|---|---|---|---|
| 9.0 | yes | 0 | 1 | first in window [0,10) |
| 9.5 | yes | 0 | 2 | second |
| 9.9 | **no** | 0 | 2 | at limit |
| 10.0 | yes | 1 | 1 | **new bucket** — count reset |
| 10.1 | yes | 1 | 2 | |
| 10.2 | no | 1 | 2 | |

Across `t=9.5` and `t=10.1` you got **4** allows in ~0.6s of wall time — the classic fixed-window edge burst. Call this out before the interviewer does.

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

### Worked trace — sliding log (no edge burst)

`limit=2`, `window=10`. Queue holds timestamps of **allowed** events.

| t | q before prune | after prune | allow? | q after |
|---|---|---|---|---|
| 0 | [] | [] | yes | [0] |
| 5 | [0] | [0] | yes | [0,5] |
| 9 | [0,5] | [0,5] | **no** | [0,5] |
| 10 | [0,5] | [5] (`0 ≤ 0` dropped) | yes | [5,10] |

At `t=10`, only events with `ts > 0` remain — exactly “≤2 in any rolling 10s,” so the fixed-window double-burst cannot happen.

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

### Worked trace — token bucket

`rate=1 token/s`, `burst=2`, start `tokens=2` at `t=0`.

| t | refill math | tokens before cost | allow(1)? | tokens after |
|---|---|---|---|---|
| 0 | +0 | 2 | yes | 1 |
| 0 | +0 (same instant) | 1 | yes | 0 |
| 0 | +0 | 0 | **no** | 0 |
| 1.0 | +1.0 → min(2, 0+1)=1 | 1 | yes | 0 |
| 3.0 | +2.0 → min(2, 0+2)=2 | 2 | yes | 1 |

**Interview line:** “Burst up to `burst`, sustained `rate`. I’ll confirm cost-per-request and whether we reject or delay.”

---

# PART 4: CONCURRENCY — RACE + FIX

Phase A default is single-threaded. Netflix-style follow-up: **make the TTL cache thread-safe.**

## 4A: Concrete race (why a lock exists)

Shared lazy TTL map **without** synchronization:

```
map = {k: (value=42, exp=100)}
now = 50   # still valid
```

| Time | Thread A (`get(k)`) | Thread B (`put` / expire path) |
|---|---|---|
| 1 | reads entry; sees `now < exp` → “alive” | |
| 2 | | deletes `k` (expiry purge or overwrite) |
| 3 | returns `42` from a **stale local copy** or crashes if it re-reads a deleted slot | |

Worse variant: A checks alive, B replaces value, A returns old value after B’s write — lost update / dirty read.

**Invariant you need:** check-expiry + read (or write) of the same key is **one critical section**.

## 4B: Minimal fix — one lock around public API

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

Rules:
1. Same lock for **all** public methods that touch `inner`  
2. Do **not** call arbitrary user callbacks while holding the lock  
3. Prefer coarse lock first in interviews; strip-locking is a follow-up flex  

## 4C: What we still do not claim

- Lock-free designs, `concurrent.futures` pipelines, distributed Redis TTL  
- Formal linearizability proofs  

Bank `74_locked_ttl_cache` hammers the locked wrapper under threads — smoke for “no corruption / no crash,” not a proof.

---

# PART 5: TEACH-BACK

1. Lazy vs eager expiry — when does lazy leak memory?  
2. Why fixed windows double-burst at boundaries?  
3. Sliding log vs token bucket — which matches “≤N in any rolling second”?  
4. What do you ask before coding a weighted cache?  
5. Describe one get/put race without a lock; what does the lock make atomic?

---

# PART 6: PRACTICE

| Problem | Where |
|---|---|
| TTL cache | bank `68_ttl_cache` |
| TTL + LRU combined | bank `73_ttl_lru_cache` |
| Locked TTL (thread smoke) | bank `74_locked_ttl_cache` |
| Sliding rate limiter | bank `69_rate_limiter` |
| LRU (baseline) | bank `26_lru_cache` |
| TimeMap | Design lesson + spine |

**Spine:** Coverage § Design / Chill-Interview gap rows.
