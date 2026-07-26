# CHILL INTERVIEW GAPS — RETENTION

**Sources:**
- `Design/TTL Cache & Rate Limiter.md`
- `Stacks & Queues/Stacks & Queues.md` (Simplify Path)
- `Intervals/Intervals & Sweep Line.md` (Intersection)
- `Matrix/Matrix & Grid Patterns.md` (Longest Increasing Path)

**Rules:** Blind first. Grade via `Retention Questions/keys/Chill Interview Gaps Retention.keys.md`.  
Tag misses: `knowledge-gap` / `misread` / `careless-slip` / `time-pressure`.

---

# SECTION A: RAPID FIRE

Answer in 1–3 sentences (or short code sketch where asked).

## A1.
Lazy vs eager TTL expiry — what does each do on `get`? When does lazy leak memory?

## A2.
Capacity eviction vs TTL — can a non-expired key be removed? Give one sentence.

## A3.
Fixed-window rate limiter: why can you briefly exceed `2 * limit` near a boundary?

## A4.
Sliding-window **log** vs token bucket — which enforces “≤N events in any rolling W seconds”?

## A5.
Simplify Path: stack effect of tokens `""`, `"."`, `".."`, `"foo"`.

## A6.
Interval intersection: when do you advance pointer `i` vs `j`?

## A7.
Longest Increasing Path: why is the cell graph a DAG? What do you memoize?

## A8.
Thread-safe TTL cache: what must be atomic? Name one mistake with locking.

---

# SECTION B: TRACE / APPLY

## B1. TTL capacity trace
`cap=2`. Ops at `t=0`: `put(a,1,10)`, `put(b,2,10)`, `get(a)`, `put(c,3,10)`.  
Then clock → `10`, `get(b)`.  
For each step: map keys remaining + return value of gets.

## B2. Sliding limiter
`limit=2`, `window=10`. `allow` at t=0,5,9,10. Which succeed?

## B3. Simplify Path
Canonicalize `/a/./b/../../c/`.

## B4. Intersection
Intersect `A=[[1,5],[8,12]]` and `B=[[2,6],[10,14]]`. Show lo/hi each step.

## B5. LIP
On `[[3,4,5],[3,2,6],[2,2,1]]`, give one longest path (values) and its length.

---

# SECTION C: CODE SKETCH (NO EDITOR)

## C1.
Sketch `TTLLRUCache.get` including expiry + MRU move (pseudocode OK).

## C2.
Sketch sliding-window log `allow()`.

## C3.
One-liner invariant for interval intersection advance rule.

---

# SECTION D: BANK FOLLOW-UPS

After grading, implement or re-solve blind:

| Bank | Focus |
|---|---|
| `68_ttl_cache` | Lazy TTL + capacity |
| `73_ttl_lru_cache` | TTL + LRU combined |
| `69_rate_limiter` | Sliding log |
| `70_simplify_path` | Path stack |
| `71_interval_intersection` | Two pointers |
| `72_longest_increasing_path` | DFS memo |
