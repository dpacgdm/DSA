# SEGMENT TREES & FENWICK TREES — EXPOSURE ONLY

**Module:** 10 (Advanced Structures)  
**Depth label:** **EXPOSURE — NOT MASTERY**  
**Status:** `taught` at exposure level only — do **not** treat as interview-complete for segment/Fenwick construction under pressure  
**Language:** Python  
**Primary goal alignment:** FAANG-style **Interview DSA**. Full competitive-programming depth is **Phase B**.

---

# READ THIS FIRST (NON-NEGOTIABLE)

| Claim | Truth |
|---|---|
| "I must master segment trees for FAANG screens" | **False** for most companies. Rare as a required code-from-scratch topic. |
| "I should recognize the problem shape" | **True.** Interviewers may mention them; some companies (or follow-ups) expect the name + complexity. |
| "I should implement a production segment tree blind" | **Not a Phase A gate.** Optional stretch. |
| "Fenwick (BIT) for range sum + point update" | **Worth one clean implementation** so the idea is real, not buzzword-only. |
| Passing Module 10 | Tries + monotonic deep dive are the **weighted** half. This file is the **light** half. |

**If you only have time for one advanced structure family in Module 10: prioritize Tries + Monotonic. This lesson is secondary.**

---

# PART 1: WHAT PROBLEM DO THESE SOLVE?

## The Query Pattern

You have an array `A[0..n-1]` that **changes over time**, and you repeatedly need answers about **ranges**:

| Query type | Example |
|---|---|
| Range sum | `sum(A[L..R])` |
| Range min / max | `min(A[L..R])` |
| Range GCD / OR / other mergeable op | less common in interviews |
| Point update | `A[i] = x` or `A[i] += delta` |
| Range update | add `v` to all of `A[L..R]` (needs lazy — **beyond exposure**) |

### Why not prefix sums?

**Prefix sums** give O(1) range sum after O(n) build — but **updates are O(n)** (rebuild) or force a full recompute.

| Approach | Point update | Range sum |
|---|---|---|
| Naive array | O(1) | O(n) |
| Prefix sums | O(n) rebuild | O(1) |
| **Fenwick / Segment** | **O(log n)** | **O(log n)** |

**The rule:** Static array + many range sums → prefix sums. **Dynamic** array (updates interleaved with range queries) → Fenwick or segment tree.

### Real-World Intuition

Think of a live leaderboard of scores:

- One player's score updates (point update)
- You need total score of ranks `L..R` or sum of a segment of an array of values

You cannot rebuild a prefix array on every update if updates are frequent. Fenwick/segment keep a **tree of partial aggregates** so both update and query are logarithmic.

---

# PART 2: INTUITION — POINT UPDATE, RANGE QUERY

## Segment Tree (Conceptual)

A segment tree is a binary tree where:

- Each **leaf** = one array element
- Each **internal node** = merge of its children's ranges (sum, min, …)

```
Array: [2, 1, 5, 3]

                    [0,3] sum=11
                   /            \
            [0,1] sum=3      [2,3] sum=8
            /      \          /      \
        [0]=2    [1]=1    [2]=5    [3]=3
```

**Range query:** Walk O(log n) nodes whose ranges exactly cover `[L, R]` without going outside.  
**Point update:** Walk from leaf to root, O(log n) recomputing merges.

**Space:** ~4n nodes in typical array implementation.

**Interview talk:** "A segment tree stores aggregates on dyadic ranges. Update and query are O(log n) because you touch O(log n) nodes."

### What "mergeable" means

The operation ⊕ must be associatively combinable from children:

- Sum, min, max, GCD, bitwise OR/AND — yes
- Mode / majority — not from two child modes alone without extra data
- Distinct count — needs more than a single integer (or heavy tricks)

---

## Fenwick Tree / Binary Indexed Tree (BIT)

A Fenwick tree is a **compact structure specialized for prefix aggregates** (usually sums) with point updates.

**Mental model:** Index `i` stores the sum of a responsibility range ending at `i`. The length of that range is the **lowest set bit** of `i` (1-indexed).

```
index (1-based):  1   2   3   4   5   6   7   8
responsible for: [1] [1..2] [3] [1..4] [5] [5..6] [7] [1..8]
```

**Prefix sum `sum(1..i)`:** Add `tree[i]`, then move `i` down by clearing lowest set bit: `i -= i & -i`, until 0.  
**Point add at `i`:** Add delta to `tree[i]`, then move `i` up: `i += i & -i`, until > n.

**Range sum `sum(L..R)`** (0-based array mapped to 1-based BIT):

```
prefix(R+1) - prefix(L)   # careful with indexing
```

**Why interviews mention it:** Same asymptotic power as segment tree for **sum + point update**, less code, less general (awkward for arbitrary min with some updates unless you know variants).

---

# PART 3: SIMPLE FENWICK — PYTHON IMPLEMENTATION

**Convention:** 1-indexed internally. Array `A` is 0-indexed externally.

```python
class Fenwick:
    """Point add + prefix sum. Exposure-level implementation."""

    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        """Add delta to 0-based index i."""
        i += 1  # to 1-based
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix(self, i: int) -> int:
        """Sum of A[0..i] inclusive, 0-based i. If i < 0, return 0."""
        if i < 0:
            return 0
        i += 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, left: int, right: int) -> int:
        """Sum A[left..right] inclusive, 0-based."""
        return self.prefix(right) - self.prefix(left - 1)

    @classmethod
    def from_array(cls, arr):
        ft = cls(len(arr))
        for i, v in enumerate(arr):
            ft.add(i, v)
        return ft
```

### Why `i & -i`?

In two's complement, `i & -i` isolates the **lowest set bit** of `i`. That bit encodes the size of the responsibility block Fenwick uses for jumps.

**You do not need to derive this in an interview.** Saying "Fenwick jumps by lowest set bit for O(log n) prefix updates/queries" is enough at exposure level.

### Complexity

| Op | Time | Space |
|---|---|---|
| Build from n adds | O(n log n) | O(n) |
| `add` | O(log n) | |
| `prefix` / `range_sum` | O(log n) | |

---

# PART 4: ONE RANGE-SUM PROBLEM (WORKED)

## Problem: Range Sum Query — Mutable (LC 307)

Implement a class:

- `NumArray(nums)` — init
- `update(index, val)` — set `nums[index] = val`
- `sumRange(left, right)` — return sum of `nums[left..right]`

### Approach A (Exposure target): Fenwick

```python
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.arr = nums[:]  # keep values for update delta
        self.ft = Fenwick(self.n)
        for i, v in enumerate(nums):
            self.ft.add(i, v)

    def update(self, index: int, val: int) -> None:
        delta = val - self.arr[index]
        self.arr[index] = val
        self.ft.add(index, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self.ft.range_sum(left, right)
```

### Trace

```
nums = [1, 3, 5]
sumRange(0, 2) → 9
update(1, 2)   → array logically [1, 2, 5]
sumRange(0, 2) → 8
```

### Approach B (Also fine in interviews): Segment tree

Same API; more code. Prefer Fenwick for sum-only unless interviewer asks for min/max.

### Approach C (Often accepted for small constraints): Naive

If n and queries are tiny, O(n) sum is fine — **say the constraint-driven choice out loud**.

### Approach D: Sqrt decomposition

Blocks of size √n — another exposure name. Rarely required to code in screens.

---

# PART 5: WHEN OVERKILL VS WHEN MENTIONED

## Usually OVERKILL for Phase A screens

| Situation | Prefer instead |
|---|---|
| Static array, range sums | Prefix sums |
| Static array, range min with RMQ offline | Sparse table (CP) or just precompute if n small |
| Sliding window max | Monotonic deque (you already know) |
| "Kth something" online with updates | Often policy / heap / binary search on fenwick counts — advanced |
| One-off sum of whole array | Variable / `sum()` |

## When it IS reasonable to mention

1. Interviewer asks: "How would you support point updates and range sums efficiently?"  
   → "Fenwick or segment tree, O(log n) each."
2. Follow-up after prefix sums: "What if the array keeps changing?"  
   → Name Fenwick/segment; offer to sketch Fenwick if they want code.
3. Counting inversions / rank queries: "I could Fenwick frequencies while scanning" (classic CP; **optional** interview flex — only if comfortable).
4. Company/role known for harder DS (some quant / infrastructure teams) — still confirm; don't assume.

## When NOT to force it

- Don't rewrite a two-pointers problem as a segment tree.
- Don't start coding a 100-line segtree in a 45-minute screen unless they explicitly want that structure.
- Don't claim mastery on Module 10 completion — this file is **exposure**.

---

# PART 6: SEGMENT TREE — MINIMAL SKETCH (NO MASTERY EXPECTED)

Enough to recognize code in blogs / discuss tradeoffs:

```python
class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, v, tl, tr):
        if tl == tr:
            self.t[v] = arr[tl]
            return
        tm = (tl + tr) // 2
        self._build(arr, 2 * v, tl, tm)
        self._build(arr, 2 * v + 1, tm + 1, tr)
        self.t[v] = self.t[2 * v] + self.t[2 * v + 1]

    def _sum(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return (self._sum(2 * v, tl, tm, l, min(r, tm)) +
                self._sum(2 * v + 1, tm + 1, tr, max(l, tm + 1), r))

    def range_sum(self, l, r):
        return self._sum(1, 0, self.n - 1, l, r)

    # point update omitted for brevity — walk to leaf, update, fix parents
```

**Exposure bar:** Explain the picture + complexities. Coding this blind under timer is **not** a Phase A requirement.

**Lazy propagation / range updates:** Explicitly **out of scope** for Phase A. Phase B / CP.

---

# PART 7: FENWICK VS SEGMENT — CHEAT SHEET

| Dimension | Fenwick (BIT) | Segment Tree |
|---|---|---|
| Typical use | Prefix/range **sum**, point add | Any mergeable op; more general |
| Code length | Short | Longer |
| Range min + point set | Possible with care | Natural |
| Range add + range sum | Needs tricks / fenwick2 | Lazy segtree |
| Interview frequency | Low–medium as name | Low as full code |
| Phase A expectation | Recognize + one sum impl | Recognize only |

---

# PART 8: MINI DRILL (EXPOSURE CHECK)

Answer in your head, then check.

**Q1.** Static array, 10⁵ range-sum queries, no updates. Best tool?  
**A:** Prefix sums — O(n) build, O(1) query. Fenwick is unnecessary.

**Q2.** 10⁵ mixed point updates and range sums. Best tool?  
**A:** Fenwick or segment tree — O(log n) per op.

**Q3.** Sliding window maximum on a stream. Fenwick?  
**A:** No — monotonic deque is the right interview tool.

**Q4.** What does `i & -i` represent in Fenwick?  
**A:** Lowest set bit of `i`; jump size for responsibility ranges.

**Q5.** Is Module 10 "complete" if you can't write a segtree from scratch?  
**A:** Yes for Phase A **if** tries + monotonic are drilled/retention/timed and you can explain when Fenwick/segment apply. Segtree coding ≠ gate.

---

# PART 9: SCOPE BOUNDARIES (HONEST)

| In this file | Explicitly excluded |
|---|---|
| Problem shape: point update + range query | Lazy propagation |
| Fenwick sum implementation + LC 307 style | 2D Fenwick, fenwick for counting inversions mastery |
| Segment tree mental model + complexity | Persistent / Li Chao / merge-sort trees |
| Interview judgment: when overkill | Full CP contest fluency |

**Label to use in scoreboard / ledger:**

```
Segment/Fenwick — exposure only (not mastery)
Heat tracking: optional; do not block Phase A on segtree coding
```

**Status enum note:** Raising Module 10 to `complete` requires Tries + Monotonic retention/timed evidence. Fenwick exposure quiz can be part of Module 10 retention (light section) without demanding contest-level segment trees.

---

# PART 10: INTUITION DIAGRAMS (ASCII)

## 10A: Why prefix sums break under updates

```
Array:     [2, 1, 5, 3]
Prefix:  0  2  3  8 11     prefix[i] = sum of first i elements

sum(1..2) = prefix[3]-prefix[1] = 8-2 = 6  ✓  (1+5)

Update A[1] += 10  → array [2, 11, 5, 3]

Naive: must rebuild ALL prefix entries from index 1 onward → O(n)
Fenwick/Segment: touch O(log n) tree nodes only
```

## 10B: Segment tree shape (n=8 conceptual)

```
                         [0,7]
                    /              \
               [0,3]                [4,7]
              /     \              /     \
          [0,1]     [2,3]      [4,5]     [6,7]
          /  \      /  \       /  \      /  \
        [0] [1]  [2] [3]    [4] [5]   [6] [7]
```

**Range sum [2,5] cover:** node[2,3] + node[4,5] — two nodes, not eight leaves.

**Point update index 3:** leaf[3] → [2,3] → [0,3] → [0,7] — O(log n) ancestors.

## 10C: Fenwick responsibility (1-based)

```
i   binary   lowest set bit   responsibility
1   0001     1                [1]
2   0010     2                [1..2]
3   0011     1                [3]
4   0100     4                [1..4]
5   0101     1                [5]
6   0110     2                [5..6]
7   0111     1                [7]
8   1000     8                [1..8]
```

**Prefix sum(1..6):**  
`bit[6] (5..6) + bit[4] (1..4)` → jump `6 → 4 → 0`.

**Add delta at index 5:**  
`bit[5], bit[6], bit[8]` → jump `5 → 6 → 8`.

```
prefix(6):  6 ──(-lowbit)──► 4 ──► 0
add(5):     5 ──(+lowbit)──► 6 ──► 8 ──► done
```

---

# PART 11: FENWICK FULL WALKTHROUGH WITH UPDATES

## 11A: Build from array `[1, 3, 5]`

```
n=3, bit = [0,0,0,0]  (1-based indices 1..3)

add(0,1): i=1
  bit[1]+=1 → [0,1,0,0]; i=1+1=2
  bit[2]+=1 → [0,1,1,0]; i=2+2=4 >3 stop

add(1,3): i=2
  bit[2]+=3 → [0,1,4,0]; i=4 stop

add(2,5): i=3
  bit[3]+=5 → [0,1,4,5]; i=3+1=4 stop

bit = [0, 1, 4, 5]
Meaning:
  bit[1]=1 → A[0]
  bit[2]=4 → A[0]+A[1] = 1+3
  bit[3]=5 → A[2]
```

## 11B: Queries

```
prefix(0) = sum A[0..0]:
  i=1 → s+=bit[1]=1 → i=0 → 1

prefix(1) = A[0]+A[1]:
  i=2 → s+=4 → i=0 → 4

prefix(2) = all:
  i=3 → s+=5 → i=2 → s+=4 → i=0 → 9

range_sum(0,2)=9
range_sum(1,2)=prefix(2)-prefix(0)=9-1=8  (3+5)
```

## 11C: update(1, 2) meaning set A[1]=2 (was 3)

```
delta = 2-3 = -1
add(1, -1): i=2
  bit[2]+=-1 → [0,1,3,5]; i=4 stop

Now logically A=[1,2,5]
prefix(2)= bit[3]+bit[2]=5+3=8 ✓
```

## 11D: Second update update(0, 7) set A[0]=7 (was 1)

```
delta=6
add(0,6): i=1
  bit[1]+=6 → 7; i=2
  bit[2]+=6 → 9; i=4 stop

A=[7,2,5], total=14
prefix(2)=bit[3]+bit[2]=5+9=14 ✓
```

## 11E: Manual dry-run checklist (use in interviews)

1. Keep `self.arr` mirror for deltas  
2. Never forget `i += 1` when going 0-based → 1-based  
3. `range_sum(l,r) = prefix(r) - prefix(l-1)` with `prefix(-1)=0`  
4. Build = n times `add` (O(n log n)) — fine for exposure  

---

# PART 12: SEGMENT TREE CONCEPTUAL BUILD

## 12A: What you must be able to say (exposure bar)

1. Leaves hold array values  
2. Internal node = merge(left, right) — for sums, `+`  
3. Query decomposes `[L,R]` into O(log n) canonical nodes  
4. Point update fixes leaf then recomputes ancestors  
5. Space ~4n in array heap layout (`t[v], left=2v, right=2v+1`)

## 12B: Build walkthrough `arr=[2,1,5,3]`

```
_build v=1 range[0,3]:
  mid=1
  _build v=2 [0,1]:
    _build v=4 [0,0]: t[4]=2
    _build v=5 [1,1]: t[5]=1
    t[2]=2+1=3
  _build v=3 [2,3]:
    _build v=6 [2,2]: t[6]=5
    _build v=7 [3,3]: t[7]=3
    t[3]=5+3=8
  t[1]=3+8=11
```

## 12C: Query sum[1,2]

```
Need indices 1 and 2 (values 1 and 5)

From root [0,3]:
  left child [0,1] partially overlaps → go deeper
    [0,0] no overlap with [1,2]
    [1,1] exact → return 1
  right child [2,3] partially overlaps
    [2,2] exact → return 5
    [3,3] no overlap
Total 1+5=6
```

## 12D: Point set index 2 to 10

```
Leaf t[6] was 5 → 10
Parent t[3] = 10+3 = 13
Root t[1] = 3+13 = 16
```

## 12E: Minimal point-update code (recognition)

```python
def _update(self, v, tl, tr, pos, new_val):
    if tl == tr:
        self.t[v] = new_val
        return
    tm = (tl + tr) // 2
    if pos <= tm:
        self._update(2*v, tl, tm, pos, new_val)
    else:
        self._update(2*v+1, tm+1, tr, pos, new_val)
    self.t[v] = self.t[2*v] + self.t[2*v+1]

def update(self, pos, new_val):
    self._update(1, 0, self.n-1, pos, new_val)
```

**Exposure bar:** Read and explain. Blind-coding under 45 min is **not** required for Phase A gates.

## 12F: Segment vs Fenwick — when each (expanded)

| Need | Prefer |
|---|---|
| Range sum + point add | Fenwick (shorter) |
| Range min + point set | Segment tree |
| Range add + range sum | Lazy segment (**out of scope**) |
| Static RMQ | Sparse table (CP) / precompute |
| Interview time pressure | Name both; code Fenwick if forced |

---

# PART 13: INTERVIEW Q&A BANK (EXPOSURE)

**Q1. "How do you support point updates and range sums?"**  
A: Fenwick or segment tree, O(log n) each. Prefix sums if no updates.

**Q2. "What's the difference between Fenwick and segment tree?"**  
A: Fenwick is compact for prefix/sum style ops. Segment tree is more general for any associative merge (min/max/gcd) and extends to lazy range updates.

**Q3. "Why 1-based indexing in Fenwick?"**  
A: Lowest-set-bit arithmetic is cleanest when index 0 isn't used; `i & -i` on 0 is a footgun.

**Q4. "Can Fenwick do range minimum?"**  
A: Not as naturally as segment tree for arbitrary point *sets*. Some variants exist with restrictions; I'd use a segment tree for RMQ + updates.

**Q5. "Is this needed for FAANG screens?"**  
A: Rarely as a must-code. Often as a follow-up name-drop after prefix sums. Tries/monotonic matter more in Module 10.

**Q6. "How does `i & -i` work?"**  
A: Isolates lowest set bit in two's complement. That's the jump size. I use it as a known Fenwick primitive; I can implement from the template.

**Q7. "Build complexity?"**  
A: O(n log n) via n adds, or O(n) specialized builds exist — O(n log n) is fine to state.

**Q8. "2D Fenwick?"**  
A: Exists for matrices; Phase B / CP. Not Phase A.

**Q9. "Count inversions with Fenwick?"**  
A: Map values to ranks; scan right-to-left or left-to-right adding frequencies — classic CP flex. Optional interview mention only if fluent.

**Q10. "Sliding window maximum — Fenwick?"**  
A: No. Monotonic deque.

**Q11. "What is lazy propagation?"**  
A: Deferred range updates stored on nodes and pushed down when needed. Out of Phase A scope.

**Q12. "Memory?"**  
A: Fenwick ~n; segment tree ~4n.

---

# PART 14: MORE PRACTICE (EXPOSURE DRILLS)

## Drill 1 — Hand-simulate

Array `[4, 2, 6, 3]`. Build Fenwick by successive adds. Compute `range_sum(1,3)`. Then `update(2, 1)` (set). Recompute `range_sum(0,2)`.

<details>
<summary>Answer sketch</summary>

A=[4,2,6,3], total=15.  
range_sum(1,3)=2+6+3=11.  
set A[2]=1 → delta=-5; A=[4,2,1,3].  
range_sum(0,2)=4+2+1=7.

</details>

## Drill 2 — Choose the tool

| Scenario | Tool |
|---|---|
| 1e5 static range sum queries | Prefix |
| 1e5 mixed updates + sums | Fenwick/Seg |
| Window max stream | Mono deque |
| Range min updates | Segtree |
| Subarray sum = k on fixed array | Prefix+hash |

## Drill 3 — Explain without code

Draw Fenwick jumps for `prefix(13)` on n≥13. List indices added.

```
13 (1101) → 12 (1100) → 8 (1000) → 0
Adds bit[13]+bit[12]+bit[8]
```

---

# PART 15: EXPANDED CHEAT SHEET

```
STATIC range sum          → prefix sums
DYNAMIC point add + sum   → Fenwick
DYNAMIC + min/max/gcd     → segment tree
RANGE update              → lazy segtree (NOT Phase A)
WINDOW max/min            → monotonic deque
SUBARRAY sum = k (fixed)  → prefix + hash
```

### Fenwick API (memorize)

```
add(i, delta)      # 0-based i
prefix(i)          # sum A[0..i]
range_sum(l, r)    # prefix(r)-prefix(l-1)
```

### Segment API (recognize)

```
build / update(pos,val) / query(l,r)
merge = +  or  min  or  max
```

### Complexity card

| Structure | Update | Query | Space |
|---|---|---|---|
| Naive | O(1) | O(n) | O(n) |
| Prefix | O(n) rebuild | O(1) | O(n) |
| Fenwick | O(log n) | O(log n) | O(n) |
| Segtree | O(log n) | O(log n) | O(n) |

---

# PART 16: HONEST SCOPE REMINDER (READ AGAIN)

| You SHOULD | You need NOT |
|---|---|
| Explain the problem shape | Code lazy segtree |
| Implement Fenwick sum once | Win CF with segtrees |
| Name complexities | Memorize every variant |
| Know when overkill | Use BIT on window-max |

**Label on scoreboard:** `Segment/Fenwick — exposure only (not mastery)`

---

*End of Segment & Fenwick Exposure (expanded). Remember: exposure ≠ mastery.*

---

# PART 17: EXTENDED FENWICK TRACE (n=8)

Array A = `[1,2,3,4,5,6,7,8]` (0-based). After building:

Conceptual bit responsibilities (1-based values):
```
bit[1]=1
bit[2]=1+2=3
bit[3]=3
bit[4]=1+2+3+4=10
bit[5]=5
bit[6]=5+6=11
bit[7]=7
bit[8]=1+...+8=36
```

`range_sum(2,6)` = sum A[2..6]=3+4+5+6+7=25  
= prefix(6)-prefix(1) = (1+…+7)-(1+2)=28-3=25 ✓

Update: add +10 to index 3 (A[3] 4→14):
touches bit[4], bit[8] (1-based i=4).

---

# PART 18: SEGMENT TREE QUERY DECOMPOSITION EXAMPLES

Query [1,6] on n=8:
Possible cover: [1,1]+[2,3]+[4,5]+[6,6] — O(log n) nodes.

Point update index 5: leaf → parents up to root, ~3–4 merges.

**Say in interview:** "Any range decomposes into O(log n) disjoint node ranges already stored in the tree."

---

# PART 19: COMMON IMPLEMENTATION BUGS (EXPOSURE)

| Bug | Symptom |
|---|---|
| Forgot 1-based convert | Wrong sums / infinite loop on i=0 |
| `prefix(l-1)` when l=0 without guard | Wrong / negative index |
| Update set without delta | Double-counted values |
| Segtree array size n not 4n | IndexError / corruption |
| Query l>r not handled | Garbage |

---

*End of Segment & Fenwick Exposure (expanded). Remember: exposure ≠ mastery.*
