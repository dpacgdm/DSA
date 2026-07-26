# Answer Key — Chill Interview Gaps Retention.md

**Source questions:** `Retention Questions/Chill Interview Gaps Retention.md`  
Attempt the questions file first.

---

# SECTION A — ANSWERS

### A1
**Lazy:** on `get`/`put`, if `now >= expire_at`, delete and miss. **Eager:** background/heap pops expiries without waiting for access. Lazy leaks memory for keys never touched after expiry.

### A2
Yes — capacity eviction can remove a still-valid key when inserting a new one at capacity. TTL and capacity are separate policies.

### A3
Window id resets at the boundary, so counts near the end of window N and start of window N+1 both reset — up to `limit` in each, ≈ `2*limit` in a short wall-clock span.

### A4
Sliding-window **log** (timestamps in a deque). Token bucket smooths average rate with burst, not a hard count in every rolling window (unless parameterized carefully).

### A5
`""` / `"."` → skip; `".."` → pop if non-empty; else push name.

### A6
After computing intersection, advance the interval that **ends first** (`if A[i].end < B[j].end: i++ else j++`).

### A7
Edges only go to **strictly larger** values → no cycles. Memoize `dfs(r,c)` = longest increasing path **starting at** that cell.

### A8
`get`’s expiry check + read (and `put`) must hold the same lock so another thread cannot interleave. Mistake: releasing lock between expire-check and return; or calling slow user code while holding the lock.

---

# SECTION B — ANSWERS

### B1
Assume lesson **plain TTLCache** (evict oldest **insertion** order; `get` does not reorder):

| Op | Returns | Keys in map |
|---|---|---|
| put(a,1,10) | — | {a} |
| put(b,2,10) | — | {a,b} |
| get(a) | 1 | {a,b} |
| put(c,3,10) | — | {b,c} (evicted **a**) |
| clock=10; get(b) | None | {c} (b lazy-expired) |

If using **TTL+LRU** (`73`): `get(a)` makes `a` MRU, so `put(c)` evicts **b** instead; map becomes {a,c}.

### B2
t=0 yes; t=5 yes; t=9 no; t=10 yes (0 drops out of window).

### B3
`/c`

### B4
(0) A[1,5] B[2,6] → lo,hi=2,5 emit; advance A (ends 5<6)  
(1) A[8,12] B[2,6] → 8,6 no; advance B  
(2) A[8,12] B[10,14] → 10,12 emit; advance A → done.  
Result: `[[2,5],[10,12]]`

### B5
Length **4**. One path: `3→4→5→6` (e.g. (0,0)→(0,1)→(0,2)→(1,2)).

---

# SECTION C — ANSWERS

### C1
```
node = map.get(key)
if not node or now >= node.exp: delete if present; return None
unlink node; insert at MRU; return node.val
```

### C2
```
now = time()
while q and q[0] <= now - W: popleft
if len(q) >= limit: return False
q.append(now); return True
```

### C3
“Always advance the interval with the smaller end so you never skip a possible overlap with the other list’s next interval.”
