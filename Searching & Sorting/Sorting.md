# SORTING — THE COMPLETE LESSON

**Module:** 3 — Searching & Sorting  
**Status target after this file:** `taught` (Sorting + **Master Theorem** track)  
**Language:** Python  
**Prerequisite:** Arrays, Recursion (call stack, recursion trees, recurrence *setup*), Binary Search (optional but helpful)

> **Governance:** This file is the **single source of truth for Master Theorem mastery**. Recursion.md only previewed MT. Do not mark MT `complete` from Module 2 alone. See `Handoff Doc.md`.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# SCOPE DOCUMENT

## In Scope

| Topic | Depth |
|---|---|
| Why sorting exists; comparison model | Full |
| Merge Sort — implementation, stability, space, recurrence | Full |
| Quick Sort — Lomuto + Hoare, worst case, randomized, space | Full |
| **Master Theorem — full treatment** | **Full (home module)** |
| MT on merge / quick / binary search; when MT fails | Full |
| Heap sort (mention) vs Timsort (Python's `sort`) | Full enough for interviews |
| Counting / radix / bucket — when applicable | Full decision-level |
| Custom sort keys in Python | Full |
| Interview: when to sort first | Full |
| Cheat sheets + worked examples | Full |
| **Count of Range Sum** (PREVIEW re-credit) | Full earned solution |

## Explicitly Deferred

| Topic | Home |
|---|---|
| External sort / disk-based merge | Systems |
| Suffix array construction sorting tricks | Advanced Strings |
| Parallel sort / GPU sort | Systems |
| Formal proof of Timsort galloping | CPython internals curiosity |
| Quickselect deep dive beyond partition reuse | Already touched Week 1; heaps module for selection alternatives |
| Inversion count as standalone LC only | Covered as cousin of Range Sum |

---

# PART 0: WHY SORTING EXISTS

## What Sorting Buys You

Once data is sorted, a family of problems collapses from hard to easy:

| After sorting you can… | Typical gain |
|---|---|
| Binary search | O(n) → O(log n) membership |
| Two pointers on ends | Two-sum variants, pair sums |
| Sweep line / merge intervals | O(n²) → O(n log n) |
| Greedy "take next in order" | Correctness often requires order |
| Deduplicate consecutive equals | O(n) after sort |
| Median / order statistics (offline) | Direct index access |

**Cost:** comparison sorts need **Ω(n log n)** in the worst case (comparison model). You pay that once; then you harvest O(n) or O(log n) passes.

## The Comparison Model (interview depth)

Any algorithm that sorts by comparing pairs of elements can be modeled as a **decision tree**. Each comparison has 2 outcomes. To distinguish n! possible permutations you need height at least log₂(n!) ≈ n log n by Stirling.

**Bottom line you must say in interviews:**

> "Any general comparison-based sort is Ω(n log n) in the worst case. Counting/radix escape this by not being pure comparison sorts — they need integer/digit structure."

---

# PART 1: MERGE SORT — THE RELIABLE O(n log n)

## 1A: Why Merge Sort Exists

You want **guaranteed** O(n log n), **stable** ordering, and a clean divide-and-conquer story. Merge sort delivers. It is not in-place (classic form uses O(n) extra memory). Python's Timsort is a highly optimized mergesort cousin — knowing merge sort explains Timsort's stability and space.

## 1B: The Idea

1. Split array into two halves.
2. Recursively sort each half.
3. **Merge** two sorted halves into one sorted array in O(n).

```
[38, 27, 43, 3, 9, 82, 10]
          /                \
   [38,27,43,3]         [9,82,10]
      /      \            /     \
  [38,27]  [43,3]      [9,82]  [10]
   /  \     /  \        /  \     |
[38][27] [43][3]     [9][82]   [10]
   \  /     \  /        \  /     |
  [27,38]  [3,43]      [9,82]  [10]
      \      /            \     /
   [3,27,38,43]        [9,10,82]
          \                /
   [3, 9, 10, 27, 38, 43, 82]
```

## 1C: Full Implementation (index-based, interview-grade)

```python
def merge_sort(arr):
    """Stable O(n log n) sort. Returns new list; original unchanged."""
    n = len(arr)
    if n <= 1:
        return arr[:]
    aux = [0] * n
    a = arr[:]
    _merge_sort(a, aux, 0, n)
    return a


def _merge_sort(a, aux, lo, hi):
    """Sort a[lo:hi] in place using aux. hi exclusive."""
    if hi - lo <= 1:
        return
    mid = lo + (hi - lo) // 2
    _merge_sort(a, aux, lo, mid)
    _merge_sort(a, aux, mid, hi)
    _merge(a, aux, lo, mid, hi)


def _merge(a, aux, lo, mid, hi):
    # Copy current range to aux
    for k in range(lo, hi):
        aux[k] = a[k]

    i, j = lo, mid
    for k in range(lo, hi):
        if i >= mid:
            a[k] = aux[j]
            j += 1
        elif j >= hi:
            a[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            # take from right only when STRICTLY smaller → STABILITY
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1
```

### Stability — the critical compare

When `aux[i] == aux[j]`, we take from the **left** (`else` branch). Equal elements keep their original relative order → **stable**.

If you write `aux[j] <= aux[i]` when taking right, you **break** stability.

## 1D: Simpler Teaching Version (slicing — clearer, more allocation)

```python
def merge_sort_simple(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_simple(arr[:mid])
    right = merge_sort_simple(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])  # stability: equals from left first
            i += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Interview note:** Slicing creates many temporary arrays. Mention O(n log n) extra allocation pressure; prefer index+aux form for "production" discussion.

## 1E: Complexity

**Recurrence:** `T(n) = 2T(n/2) + O(n)`  
(two halves + linear merge)

**Master Theorem:** Case 2 → **Θ(n log n)** (see Part 3).

**Space:** O(n) auxiliary + O(log n) recursion stack → **O(n)**.

**Best = Average = Worst:** Θ(n log n). No pivot lottery.

## 1F: Trace of Merge Only

```
left  = [3, 27, 38, 43]
right = [9, 10, 82]
merge:

compare 3 vs 9 → take 3
compare 27 vs 9 → take 9
compare 27 vs 10 → take 10
compare 27 vs 82 → take 27
compare 38 vs 82 → take 38
compare 43 vs 82 → take 43
right remains → take 82

result = [3, 9, 10, 27, 38, 43, 82]
```

---

# PART 2: QUICK SORT — FAST AVERAGE, DANGEROUS WORST

## 2A: Why Quick Sort Exists

In practice, good cache behavior + in-place partition often beats merge sort on arrays. Average O(n log n), small constants. Worst case O(n²) if pivots are adversarial — **randomize** or use median-of-three.

Python's `list.sort` is **not** quicksort (it's Timsort). Still asked constantly in interviews.

## 2B: The Idea

1. Pick a **pivot**.
2. **Partition:** elements < pivot left, > pivot right (equals policy varies).
3. Recursively sort left and right. Pivot is already in final position.

## 2C: Lomuto Partition

Simple. Pivot = last element. One scan pointer.

```python
def partition_lomuto(arr, lo, hi):
    """
    Partition arr[lo..hi] inclusive. Pivot = arr[hi].
    Returns final index of pivot.
    """
    pivot = arr[hi]
    store = lo
    for i in range(lo, hi):
        if arr[i] <= pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    return store


def quick_sort_lomuto(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    p = partition_lomuto(arr, lo, hi)
    quick_sort_lomuto(arr, lo, p - 1)
    quick_sort_lomuto(arr, p + 1, hi)
```

### Lomuto Trace: `arr = [3, 7, 1, 4, 2]`, pivot = 2 (last)

```
i=0: 3 <= 2? No
i=1: 7 <= 2? No
i=2: 1 <= 2? Yes → swap arr[0] and arr[2] → [1,7,3,4,2], store=1
i=3: 4 <= 2? No
swap pivot to store: swap arr[1] and arr[4] → [1,2,3,4,7]
pivot index = 1 ✅
```

Wait, let's re-trace carefully with store moves:

```
Start: [3, 7, 1, 4, 2], lo=0, hi=4, pivot=2, store=0
i=0: 3<=2? F
i=1: 7<=2? F
i=2: 1<=2? T → swap(arr[0],arr[2]) → [1,7,3,4,2], store=1
i=3: 4<=2? F
Final swap(arr[1],arr[4]) → [1,2,3,4,7], return 1 ✅
Left of pivot: [1], right: [3,4,7]
```

## 2D: Hoare Partition

Two pointers from ends. Usually fewer swaps. Pivot typically `arr[lo]`.

```python
def partition_hoare(arr, lo, hi):
    pivot = arr[lo]
    i = lo - 1
    j = hi + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_hoare(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    p = partition_hoare(arr, lo, hi)
    # NOTE: Hoare returns j such that both sides include boundary carefully
    quick_sort_hoare(arr, lo, p)
    quick_sort_hoare(arr, p + 1, hi)
```

**Interview warning:** Lomuto and Hoare have **different** recursion index conventions. Do not mix. Lomuto is easier to get right under pressure; say that out loud.

## 2E: Worst Case and Randomization

**Worst case:** Already sorted (or reverse) + always pick last/first as pivot → partitions of size 0 and n-1 → `T(n) = T(n-1) + O(n) = O(n²)`.

**Fix — randomized pivot:**

```python
import random

def partition_lomuto_randomized(arr, lo, hi):
    r = random.randint(lo, hi)
    arr[r], arr[hi] = arr[hi], arr[r]
    return partition_lomuto(arr, lo, hi)
```

Expected time with random pivots: **O(n log n)**. Still theoretically O(n²) with tiny probability — mention "with high probability O(n log n)" in strong interviews.

**Median-of-three:** pivot = median of first, mid, last — practical heuristic.

## 2F: Space and Stability

| Property | Quick Sort (typical in-place) |
|---|---|
| Extra space | O(log n) stack average; O(n) stack worst |
| Stable? | **No** (swaps across equals) |
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n²) |

## 2G: Quick Sort vs Merge Sort (decision)

| Need | Prefer |
|---|---|
| Guaranteed O(n log n) | Merge |
| Stability | Merge / Timsort |
| In-place + average speed on arrays | Quick |
| Linked lists | Merge (no random access needed) |
| Interview default "implement a sort" | Either; state tradeoffs |

---

# PART 3: MASTER THEOREM — FULL TREATMENT (HOME MODULE)

## 3A: What Problem MT Solves

You have a divide-and-conquer recurrence:

$$T(n) = a\, T\!\left(\frac{n}{b}\right) + f(n)$$

- **a ≥ 1** — number of subproblems  
- **b > 1** — factor by which input size shrinks  
- **f(n)** — work outside the recursive calls (divide + combine)

You want asymptotic T(n) **without** drawing the full recursion tree every time.

**Prerequisite you already have (Module 2):** setting up the recurrence and drawing trees. MT is the **lookup / case analysis** on top.

## 3B: The Three Cases (standard CLRS-style, polynomial f)

Assume \( f(n) = \Theta(n^{c}) \) for simplicity first (most interview recurrences).

Compute the **critical exponent**:

$$\log_b a$$

Compare to \( c \):

```
CASE 1 — Recursion dominates (leaf-heavy)
  If log_b(a) > c          i.e. f(n) = O(n^{log_b(a) - ε}) for some ε > 0
  Then T(n) = Θ( n^{log_b(a)} )

CASE 2 — Balanced work per level
  If log_b(a) = c          i.e. f(n) = Θ( n^{log_b(a)} )
  Then T(n) = Θ( n^{log_b(a)} · log n )
  (more precisely Θ(n^{log_b a} log n) for the basic equal case)

CASE 3 — Root / combine dominates
  If log_b(a) < c          i.e. f(n) = Ω(n^{log_b(a) + ε}) for some ε > 0
  AND regularity: a f(n/b) ≤ k f(n) for some k < 1 and large n
  Then T(n) = Θ( f(n) )
```

### Intuition via tree levels

Number of levels ≈ log_b(n).  
Level i has a^i subproblems of size n/b^i.  
Work at level i ≈ a^i · f(n/b^i).

- Case 1: work **grows** toward the leaves → total ~ leaf work  
- Case 2: work **same** each level → (work per level) × (number of levels)  
- Case 3: work **shrinks** toward leaves → total ~ root work f(n)

## 3C: Extended Case 2 (log factors in f)

If \( f(n) = \Theta(n^{\log_b a} \log^k n) \) for k ≥ 0:

$$T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$$

Example: \( T(n) = 2T(n/2) + n \log n \) → log_b a = 1, f has extra log¹ → T = Θ(n log² n).

**Interview:** Basic three cases cover 95% of asks. Mention extended case 2 if f has a log.

## 3D: Mechanical Recipe (memorize this)

```
STEP 1: Write T(n) = a T(n/b) + f(n). Identify a, b, f.
STEP 2: Compute log_b(a).
STEP 3: Write f as Θ(n^c) or note extra logs / non-poly.
STEP 4: Compare log_b(a) vs c → pick case.
STEP 5: If Case 3, sanity-check regularity (usually holds for n^c, c>0).
STEP 6: State Θ(...). Spot-check with a tiny recursion tree if unsure.
```

## 3E: Applications — Merge Sort

$$T(n) = 2T(n/2) + \Theta(n)$$

- a=2, b=2, f(n)=Θ(n¹) → c=1  
- log₂(2) = 1 = c → **Case 2**  
- **T(n) = Θ(n log n)** ✅

Tree check: log n levels, Θ(n) per level → Θ(n log n).

## 3F: Applications — Binary Search

$$T(n) = T(n/2) + \Theta(1)$$

- a=1, b=2, f(n)=Θ(n⁰) → c=0  
- log₂(1) = 0 = c → **Case 2**  
- **T(n) = Θ(log n)** ✅

## 3G: Applications — Naive Quick Sort (balanced assumption)

If every partition is perfect:

$$T(n) = 2T(n/2) + \Theta(n) \Rightarrow \Theta(n \log n)$$

**But** real quicksort recurrence depends on pivot. Average-case analysis is **not** a single MT application — it's an expectation over pivot ranks. Say:

> "MT gives Θ(n log n) for the *balanced* recurrence. Worst case T(n)=T(n-1)+Θ(n) is **outside** MT's divide-by-b form → solve by summation = Θ(n²)."

## 3H: Applications — Strassen

$$T(n) = 7T(n/2) + \Theta(n^2)$$

- log₂(7) ≈ 2.807 > 2 → **Case 1**  
- **T(n) = Θ(n^{log₂ 7}) ≈ Θ(n^{2.807})**

## 3I: Applications — Binary Tree Traversal Shape

$$T(n) = 2T(n/2) + \Theta(1)$$

- log₂(2)=1 > 0 → **Case 1** → **Θ(n)**

## 3J: When Master Theorem FAILS (must know)

> **Demoted for FAANG screens:** Know the three cases as *awareness* for merge/quick analysis. Do not gate Phase A on drilling Master Theorem proofs. Prefer stability, `key=`, and BS-on-answer reps.


| Situation | Example | What to do instead |
|---|---|---|
| Unequal subproblem sizes | T(n)=T(n/3)+T(2n/3)+Θ(n) | Recursion tree / Akra–Bazzi |
| Subtractive, not divisive | T(n)=T(n-1)+Θ(n) | Unroll / summation → Θ(n²) |
| f not polynomial-ish | T(n)=2T(n/2)+n/log n | Tree or extended methods; MT basic form fails |
| a or b not constant | weird | Don't force MT |
| Variable number of subproblems | some algorithms | Tree / induction |

### Worked failure: Quick Sort worst case

$$T(n) = T(n-1) + \Theta(n)$$

Not of form aT(n/b)+f. Unroll:

$$T(n) = \Theta(n) + \Theta(n-1) + \cdots + \Theta(1) = \Theta(n^2)$$

### Worked failure: Unequal split merge-like

$$T(n) = T(n/3) + T(2n/3) + \Theta(n)$$

Tree: depth Θ(log n), cost per level Θ(n) → still Θ(n log n), but **MT as stated doesn't apply** because subproblems differ. Use tree argument.

## 3K: Master Theorem Cheat Sheet

```
T(n) = a T(n/b) + Θ(n^c)

Compare log_b(a) ? c

  >  → Θ(n^{log_b a})           Case 1
  =  → Θ(n^c log n)             Case 2
  <  → Θ(n^c)                   Case 3 (+ regularity)

MEMORIZE ANCHORS:
  Merge sort / balanced quick: Case 2 → n log n
  Binary search:               Case 2 → log n
  Tree traverse 2T(n/2)+1:     Case 1 → n
  Strassen:                    Case 1 → n^2.807
```

## 3L: Drill — Classify These (answers)

1. `T(n)=3T(n/2)+n²` → log₂3≈1.58 < 2 → Case 3 → **Θ(n²)**  
2. `T(n)=8T(n/2)+n³` → log₂8=3=c → Case 2 → **Θ(n³ log n)**  
   (f = n³ and n^{log_b a} = n³ → equal exponents → Case 2)  
3. `T(n)=9T(n/3)+n` → log₃9=2 > 1 → Case 1 → **Θ(n²)**  
4. `T(n)=T(n/2)+n` → log₂1=0 < 1 → Case 3 → **Θ(n)**  
5. `T(n)=2T(n-1)+1` → **MT fails** (subtractive) → Θ(2ⁿ)

---

## 3M: Recursion Tree — Seeing Why Case 2 Is `n log n`

Merge sort tree for n=8:

```
Level 0:  [-------- n=8 --------]     work Θ(8)
Level 1:  [---4---] [---4---]         work Θ(4)+Θ(4)=Θ(8)
Level 2:  [2][2]  [2][2]              work Θ(8)
Level 3:  1 1 1 1 1 1 1 1             work Θ(8)
```

- Levels = log₂(n) = 3 (plus root → 4 levels of work, Θ(log n) levels)
- Cost per level = Θ(n)
- Total = Θ(n) × Θ(log n) = Θ(n log n)

**Case 1 picture** (`T(n)=3T(n/2)+Θ(1)` style leaf-heavy): costs grow as you go down; sum dominated by bottom level → Θ(n^{log_b a}).

**Case 3 picture** (`T(n)=T(n/2)+Θ(n)`): top level Θ(n), next Θ(n/2), … geometric → dominated by root → Θ(n).

## 3N: Regularity Condition (Case 3) — When Interviewers Dig

For Case 3 you also need: exists k < 1 such that `a f(n/b) ≤ k f(n)` for large n.

For f(n)=n^c with c > log_b(a):

`a (n/b)^c = a / b^c · n^c`. Since c > log_b(a), we have a/b^c < 1. Pick k with a/b^c ≤ k < 1. ✅

**When regularity fails (rare in interviews):** weird f that oscillates. Say "I'd fall back to the recursion tree."

## 3O: Substitution Method Cross-Check (optional rigor)

Guess T(n) ≤ cn log n for merge sort. Inductive step:

T(n) = 2T(n/2) + dn ≤ 2(c(n/2)log(n/2)) + dn = cn log n - cn + dn.

Choose c ≥ d so -cn + dn ≤ 0 → T(n) ≤ cn log n. ✅

Use this when MT feels like magic — substitution proves the guess.

---

# PART 3P: MASTER THEOREM ONE-PAGE POSTER

```
┌─────────────────────────────────────────────────────────────┐
│  T(n) = a T(n/b) + f(n),   f(n)=Θ(n^c)                      │
│  Compute L = log_b(a)                                       │
│                                                             │
│  L > c  →  Θ(n^L)           leaves win                      │
│  L = c  →  Θ(n^L log n)     levels tie                      │
│  L < c  →  Θ(n^c)           root wins (+ regularity)        │
│                                                             │
│  FAILS: unequal splits | T(n-1) | non-poly f | var. a,b     │
│  THEN:  recursion tree / unroll / Akra-Bazzi                │
└─────────────────────────────────────────────────────────────┘
```

---

# PART 4: HEAP SORT VS TIMSORT (PYTHON)

## 4A: Heap Sort (mention-level mastery)

1. Build a max-heap: O(n)  
2. Repeatedly extract max to the end: n × O(log n)

**Total:** O(n log n) guaranteed. **In-place.** **Not stable.**

Interview: "Heap sort gives guaranteed n log n and O(1) extra, but larger constants and poor cache locality vs quicksort; also unstable."

Full heap mechanics → **Module 6 (Heaps)**.

## 4B: Timsort — What `list.sort` / `sorted` Actually Do

CPython uses **Timsort**:

- Detects already-sorted **runs**
- Merges runs using a stack strategy (merge sort family)
- **Stable**
- Best case **O(n)** on sorted / nearly sorted data
- Worst **O(n log n)**
- Extra space **O(n)** in worst case

```python
arr.sort()          # in-place, stable, Timsort
new = sorted(arr)   # returns new list, same algorithm
```

**Interview gold:**

> "Python's sort is Timsort — stable, O(n log n) worst, O(n) best on sorted input, O(n) auxiliary. I wouldn't implement Timsort in an interview; I'd implement merge or quick and mention Timsort as the runtime."

---

# PART 5: LINEAR-TIME SORTS (WHEN COMPARISON LOWER BOUND DOESN'T APPLY)

## 5A: Counting Sort

**When:** Keys are integers in a **small range** 0..K (or mappable to that).

```python
def counting_sort(arr, K):
    """Stable counting sort for values in 0..K inclusive."""
    count = [0] * (K + 1)
    for x in arr:
        count[x] += 1
    for v in range(1, K + 1):
        count[v] += count[v - 1]
    out = [0] * len(arr)
    for x in reversed(arr):          # reverse → stability
        count[x] -= 1
        out[count[x]] = x
    return out
```

**Time:** O(n + K). **Space:** O(n + K). **Stable** (with the reverse pass).

**Fails when:** K ≫ n (e.g. arbitrary 64-bit ids) — memory and time explode.

## 5B: Radix Sort

Sort by digits (LSD or MSD), using a stable counting sort per digit.

**When:** Integers / fixed-length strings; word size w digits.

**Time:** O(w(n + σ)) with alphabet σ. For 32-bit ints with base 256, w is small → practical O(n).

## 5C: Bucket Sort

Distribute into buckets, sort each (often insertion), concatenate.

**When:** Keys roughly **uniform** in a known range (classic: floats in [0,1)).

**Average:** O(n). **Worst:** O(n²) if all land in one bucket.

## 5D: Decision Table

| Data | Algorithm |
|---|---|
| General comparable objects | Timsort / merge / quick |
| Need stable general sort | Merge / Timsort |
| Integers, tiny range K | Counting |
| Integers, large but digit structure | Radix |
| Uniform real distribution | Bucket |
| Nearly sorted | Timsort shines |

---

# PART 6: CUSTOM SORT KEYS IN PYTHON

## 6A: `key=` is the tool

```python
# Sort by absolute value
arr.sort(key=abs)

# Sort strings by length then lexicographically
words.sort(key=lambda w: (len(w), w))

# Sort intervals by end time
intervals.sort(key=lambda x: x[1])

# Descending numeric
arr.sort(reverse=True)
# Or: arr.sort(key=lambda x: -x) for numbers only
```

**Decorate-Sort-Undecorate** under the hood: compute keys once (O(n)), then Timsort compares keys.

## 6B: Comparator vs key (Python 3)

Python 3 removed `cmp`. Use `key`, or:

```python
from functools import cmp_to_key
arr.sort(key=cmp_to_key(lambda a, b: ...))
```

Prefer `key` — faster and clearer. Use `cmp_to_key` only for truly pairwise logic (rare).

## 6C: Stability matters with multi-key sorts

```python
# Sort by grade descending, then name ascending — ONE key tuple:
students.sort(key=lambda s: (-s.grade, s.name))

# OR two stable passes (last pass = primary key):
students.sort(key=lambda s: s.name)       # secondary
students.sort(key=lambda s: s.grade, reverse=True)  # primary
```

Because Timsort is stable, multi-pass works. Tuple key is cleaner.

## 6D: Trap — sorting with mutable / expensive keys

```python
# BAD: key does heavy work AND depends on changing state
arr.sort(key=lambda x: expensive(x))
```

Precompute if needed. Never use a key that mutates global state.

---

# PART 7: INTERVIEW — WHEN TO SORT FIRST

## Framework

```
Ask: Does order unlock a better algorithm?

YES if you need:
  - binary search afterward
  - greedy by size/time/deadline
  - two pointers on sorted data
  - merge intervals / sweep
  - "next greater in sorted order" offline

NO / CAREFUL if:
  - hash set already solves membership in O(n)
  - you destroy needed original indices (keep pairs (value, index))
  - n is huge and you only need min/max/kth (heap / quickselect)
  - input is streaming (can't store all)
```

**Complexity honesty:** Sorting first costs O(n log n). The rest must make that worthwhile vs an O(n) hash approach.

**Classic line:** "I'll sort a copy / sort indices to preserve original positions."

```python
idx = sorted(range(n), key=lambda i: arr[i])
```

---

# PART 8: CHEAT SHEETS

## 8A: Algorithm Comparison

| Algo | Best | Avg | Worst | Space | Stable | Notes |
|---|---|---|---|---|---|---|
| Merge | n log n | n log n | n log n | O(n) | Yes | Guaranteed |
| Quick | n log n | n log n | n² | O(log n) | No | Randomize |
| Heap | n log n | n log n | n log n | O(1) | No | Module 6 |
| Timsort | n | n log n | n log n | O(n) | Yes | Python default |
| Counting | n+K | n+K | n+K | O(n+K) | Yes | Small K |
| Radix | wn | wn | wn | O(n+σ) | Yes | Digits |
| Insertion | n | n² | n² | O(1) | Yes | Tiny / nearly sorted |

## 8B: Recurrence Anchors

| Algo | Recurrence | MT / result |
|---|---|---|
| Merge | 2T(n/2)+O(n) | Case 2 → n log n |
| Balanced Quick | 2T(n/2)+O(n) | Case 2 → n log n |
| Worst Quick | T(n-1)+O(n) | MT fails → n² |
| Binary Search | T(n/2)+O(1) | Case 2 → log n |

## 8C: Stability One-Liner

> Stable = equal keys keep original order. Needed for multi-key sorts and radix. Merge/Timsort/counting(with care) yes; quick/heap no.

---

# PART 9: WORKED EXAMPLES

---

## Example 1: Merge Sort Full Trace

`arr = [4, 2, 7, 1]`

```
_merge_sort(0,4)
  mid=2
  _merge_sort(0,2)
    mid=1
    _merge_sort(0,1) → [4]
    _merge_sort(1,2) → [2]
    merge → [2,4]
  _merge_sort(2,4)
    merge [7] and [1] → [1,7]
  merge [2,4] and [1,7]:
    1,2,4,7
Result: [1,2,4,7]
```

---

## Example 2: Quick Sort Lomuto Trace

`arr = [5, 3, 8, 4, 2]`, sort in place.

```
Partition on 2: → [2,3,8,4,5], p=0
  Left empty; sort right [3,8,4,5]
Partition on 5: ... → eventually [2,3,4,5,8]
```

(Student should hand-simulate one full partition in retention.)

---

## Example 3: Custom Key

Sort words by frequency descending, then alpha ascending:

```python
from collections import Counter
def freq_sort(words):
    cnt = Counter(words)
    return sorted(words, key=lambda w: (-cnt[w], w))
```

---

# PART 10: COUNT OF RANGE SUM — EARNED FULL SOLUTION

> **Re-credit:** Week 2 Problem 11 was **PREVIEW**. After this module, it is an **earned** Sorting / modified-merge problem. Re-queue on timed verify for gate credit.

## 10A: Problem

Given `nums`, integers `lower` and `upper`, count the number of range sums `S(i,j) = nums[i]+…+nums[j]` (i ≤ j) such that `lower ≤ S(i,j) ≤ upper`.

## 10B: Brute → Insight

Brute: all O(n²) ranges — too slow.

**Prefix sums:** Let `prefix[0]=0`, `prefix[k] = nums[0]+…+nums[k-1]`.

Then `S(i,j) = prefix[j+1] - prefix[i]`.

Count pairs `(i, j)` with `0 ≤ i < j ≤ n` and:

$$\text{lower} \le \text{prefix}[j] - \text{prefix}[i] \le \text{upper}$$

i.e.

$$\text{prefix}[j]-\text{upper} \le \text{prefix}[i] \le \text{prefix}[j]-\text{lower}$$

## 10C: Why Modified Merge Sort

Same family as **counting inversions**: during merge of two sorted halves, count cross pairs in O(n), then merge in O(n). Total O(n log n).

For each `prefix[j]` in the **right** half (already sorted among themselves after recursion), count how many `prefix[i]` in the **left** half fall in `[prefix[j]-upper, prefix[j]-lower]`.

Because the left half is sorted, two pointers (`lo`, `hi`) advance only forward as `j` increases → O(n) per merge level.

## 10D: Full Correct Implementation

```python
def count_range_sum(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    def sort_count(lo, hi):
        """
        Sort prefix[lo:hi] (hi exclusive) and return count of
        valid pairs (i,j) with lo <= i < j < hi.
        """
        if hi - lo <= 1:
            return 0

        mid = lo + (hi - lo) // 2
        count = sort_count(lo, mid) + sort_count(mid, hi)

        # Count cross pairs: i in [lo, mid), j in [mid, hi)
        # left and right halves are each sorted by value now
        j_lo = j_hi = mid
        for i in range(lo, mid):
            # For fixed left prefix[i], find right values in
            # [prefix[i]+lower, prefix[i]+upper]
            while j_lo < hi and prefix[j_lo] < prefix[i] + lower:
                j_lo += 1
            while j_hi < hi and prefix[j_hi] <= prefix[i] + upper:
                j_hi += 1
            count += j_hi - j_lo

        # Standard stable merge into prefix[lo:hi]
        merged = []
        p, q = lo, mid
        while p < mid and q < hi:
            if prefix[q] < prefix[p]:
                merged.append(prefix[q])
                q += 1
            else:
                merged.append(prefix[p])
                p += 1
        merged.extend(prefix[p:mid])
        merged.extend(prefix[q:hi])
        prefix[lo:hi] = merged

        return count

    return sort_count(0, len(prefix))
```

### Equivalent right-centric counting (matches Week 2 sketch)

```python
        lo_ptr = hi_ptr = lo
        for j in range(mid, hi):
            while lo_ptr < mid and prefix[lo_ptr] < prefix[j] - upper:
                lo_ptr += 1
            while hi_ptr < mid and prefix[hi_ptr] <= prefix[j] - lower:
                hi_ptr += 1
            count += hi_ptr - lo_ptr
```

Both are valid if pointers only move forward and halves are sorted. Use **one** consistently.

## 10E: Full Trace — `nums = [-2, 5, -1]`, `lower = -2`, `upper = 2`

Valid ranges:
- `[-2]` = -2  
- `[-2,5,-1]` = 2  
- `[-1]` = -1  
→ **3**

```
prefix = [0, -2, 3, 2]   # indices 0..3

sort_count(0,4):
  mid=2
  Using right-centric cross count (same as Week 2 / Retention C7):
  For each j in right half, count i in left with
  prefix[j]-upper ≤ prefix[i] ≤ prefix[j]-lower.

  sort_count(0,2) on [0,-2]:
    mid=1; leaves return 0
    j val=-2, left=[0]:
      need i ∈ [-4, 0] → 0 fits → +1   # S = -2-0 = -2 ✅
    merge → [-2, 0]; returns 1

  sort_count(2,4) on [3,2]:
    mid=3; leaves return 0
    j val=2, left=[3]:
      need i ∈ [0, 4] → 3 fits → +1   # S = 2-3 = -1 ✅
    merge → [2, 3]; returns 1

  Now prefix = [-2, 0, 2, 3]
  Cross left[-2,0] vs right[2,3]:
    j val=2: need i ∈ [0, 4] → {0} → +1   # S = 2-0 = 2 ✅
    j val=3: need i ∈ [1, 5] → none → +0
  cross = 1

  Total = 1+1+1 = 3 ✅
  merge → [-2, 0, 2, 3]
```

## 10F: Edge Cases

| Case | Result |
|---|---|
| `nums=[]` | prefix=[0], no pairs → 0 |
| `nums=[0], lower=0, upper=0` | 1 |
| All sums outside `[lower,upper]` | 0 |
| Negative numbers | Fine — prefix handles |

## 10G: Complexity

Same as merge sort: O(n) work per level × O(log n) levels.

> **Time: O(n log n), Space: O(n)**

## 10H: Interview Communication

1. "Range sum → prefix difference."  
2. "Count pairs with value in a window → modified merge / CDQ divide-conquer."  
3. "During merge, two pointers on sorted halves in O(n)."  
4. "I'll be careful: count **before** merging destroys order — actually we count using already-sorted halves from recursion, then merge."  

---

# PART 11: MORE WORKED PROBLEMS

## Problem A: Count Inversions (cousin of Range Sum)

Count pairs i < j with arr[i] > arr[j]. During merge, when taking from right, add `(mid - i)`.

```python
def count_inversions(arr):
    a = arr[:]
    aux = [0] * len(a)

    def sort_count(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = lo + (hi - lo) // 2
        inv = sort_count(lo, mid) + sort_count(mid, hi)
        i, j = lo, mid
        for k in range(lo, hi):
            aux[k] = a[k]
        k = lo
        i, j = lo, mid
        while i < mid and j < hi:
            if aux[j] < aux[i]:
                a[k] = aux[j]
                inv += mid - i
                j += 1
            else:
                a[k] = aux[i]
                i += 1
            k += 1
        while i < mid:
            a[k] = aux[i]; i += 1; k += 1
        while j < hi:
            a[k] = aux[j]; j += 1; k += 1
        return inv

    return sort_count(0, len(a))
```

---

## Problem B: Sort Colors / Dutch National Flag (not comparison sort)

Three-way partition — O(n) related to quicksort partition ideas. Mention as "partition thinking without full sort."

---

## Problem C: Merge Intervals (sort first)

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    out = []
    for s, e in intervals:
        if not out or s > out[-1][1]:
            out.append([s, e])
        else:
            out[-1][1] = max(out[-1][1], e)
    return out
```

> **Time: O(n log n), Space: O(n)**

---

# PART 12: MASTER THEOREM — EXTENDED DRILLS (HOMEWORK INSIDE THE LESSON)

Work these cold. Answers below each.

## Drill 1

`T(n) = 4T(n/2) + n`

**Answer:** a=4,b=2,c=1; log₂4=2 > 1 → Case 1 → **Θ(n²)**

## Drill 2

`T(n) = 4T(n/2) + n²`

**Answer:** log₂4=2=c → Case 2 → **Θ(n² log n)**

## Drill 3

`T(n) = 4T(n/2) + n³`

**Answer:** 2 < 3 → Case 3 → **Θ(n³)** (regularity: 4·(n/2)³ = 4·n³/8 = n³/2 ≤ k n³)

## Drill 4

`T(n) = T(9n/10) + n`

**Answer:** a=1,b=10/9; log_{10/9}(1)=0 < 1 → Case 3 → **Θ(n)**

## Drill 5

`T(n) = 2T(n/4) + √n`

**Answer:** f(n)=n^{1/2}, log₄2=1/2=c → Case 2 → **Θ(√n log n)**

## Drill 6 — failure

`T(n) = T(n/2) + T(n/4) + T(n/8) + n`

**Answer:** Not equal-size `a T(n/b)`. Use recursion tree / Akra–Bazzi. Tree still Θ(n) dominated by root-ish geometric — but **do not force basic MT**.

## Drill 7 — quicksort average (conceptual)

Why can't you just write `T(n)=2T(n/2)+n` as the definition of quicksort?

**Answer:** That assumes perfect pivots every time. Real quicksort's cost is a random variable; average-case analysis averages over pivot ranks. The balanced recurrence is an *approximation / best-case shape*, not the literal algorithm recurrence.

---

# PART 13: INVERSION COUNT — FULL WORKED (MERGE PATTERN FAMILY)

**Inversion:** pair i < j with arr[i] > arr[j].

This is the training-wheels version of Count of Range Sum.

```python
def count_inversions(arr):
    a = arr[:]
    aux = [0] * len(a)

    def sort_count(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = lo + (hi - lo) // 2
        inv = sort_count(lo, mid) + sort_count(mid, hi)
        for k in range(lo, hi):
            aux[k] = a[k]
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if aux[j] < aux[i]:
                a[k] = aux[j]
                inv += mid - i   # all remaining left elems form inversions
                j += 1
            else:
                a[k] = aux[i]
                i += 1
            k += 1
        while i < mid:
            a[k] = aux[i]; i += 1; k += 1
        while j < hi:
            a[k] = aux[j]; j += 1; k += 1
        return inv

    return sort_count(0, len(a))
```

### Trace: `[2, 4, 1, 3, 5]`

Inversions: (2,1), (4,1), (4,3) → 3

```
Merge [2,4] and [1,3,5]:
  take 1 (<2): inv += 2 (2 and 4) → inv=2
  take 2
  take 3 (<4): inv += 1 (4) → inv=3
  take 4, take 5
Total 3 ✅
```

> **Time: O(n log n), Space: O(n)**

**Bridge to Range Sum:** Inversions count `arr[i] > arr[j]`. Range Sum counts `lower ≤ prefix[j]-prefix[i] ≤ upper`. Same merge skeleton; different cross-condition.

---

# PART 14: QUICKSELECT CONNECTION (SORT-ADJACENT)

You saw QuickSelect in Week 1. After Lomuto, restate:

- Full quicksort sorts both sides.
- Quickselect recurses into **one** side → average O(n).
- Worst O(n²) same as quicksort; randomize.

**Interview line:** "If I only need the k-th element, sorting is overkill — quickselect / heap depending on k and mutability."

---

# PART 15: STABILITY — MULTI-KEY SORT DEEP DIVE

Scenario: sort students by grade desc, then name asc.

### Method A — tuple key (preferred)

```python
students.sort(key=lambda s: (-s.grade, s.name))
```

### Method B — two stable passes

```python
students.sort(key=lambda s: s.name)                 # secondary first
students.sort(key=lambda s: s.grade, reverse=True)  # primary last
```

**Why Method B needs stability:** The second sort must not scramble equal-grade students' name order from the first sort. Timsort/merge: OK. Unstable quicksort: **broken**.

### Method C — decorate

```python
decorated = [(-s.grade, s.name, s) for s in students]
decorated.sort()
students[:] = [s for _, _, s in decorated]
```

---

# PART 16: INTERVIEW — "IMPLEMENT A SORT" RUBRIC

What strong candidates do:

1. Ask: stable? in-place? input size? already nearly sorted? key type?
2. Pick merge (safe) or quick (in-place) and **state tradeoffs**.
3. Write correct partition/merge with edge cases n=0,1.
4. Give recurrence + MT or tree.
5. Mention Python's Timsort if asked "what does `.sort` do?"

What weak candidates do:

- Bubble sort without irony
- Claim quicksort is always O(n log n)
- Forget stability when the problem needs it
- Can't explain merge's O(n) space

---

# PART 17: WHEN SORTING IS THE WRONG FIRST MOVE

| Problem shape | Better first tool |
|---|---|
| Membership only, one shot | Scan / hash |
| Running median stream | Two heaps (Module 6) |
| Dynamic insert + order | BST / SortedList |
| Graph distances | BFS/Dijkstra — sorting edges is Kruskal-specific |
| Already need random access pattern | Maybe hash + array, not sort |

**Cost reminder:** Sorting is O(n log n). Don't pay it to enable an O(n²) follow-up that hashing would make O(n).

---

# PART 18: COUNTING / RADIX — WORKED MICRO-EXAMPLES

## Counting sort trace

`arr = [3, 1, 3, 0, 1]`, K=3

```
count raw:    [1, 2, 0, 2]   # 0×1, 1×2, 2×0, 3×2
prefix count: [1, 3, 3, 5]   # ending positions
Place from right (stable):
  1 → count[1]=2 → out[2]=1
  0 → out[0]=0
  3 → out[4]=3
  1 → out[1]=1
  3 → out[3]=3
out = [0,1,1,3,3] ✅
```

## Radix LSD sketch (base 10)

`[170, 45, 75, 90, 802, 24, 2, 66]`

```
Sort by 1's digit → ...
Sort by 10's digit → ...
Sort by 100's digit → sorted
Each pass stable counting sort.
```

---

# PART 19: SPACE COMPLEXITY — HONEST TABLE

| Algorithm | Auxiliary | Stack | Notes |
|---|---|---|---|
| Merge (aux buffer) | O(n) | O(log n) | Dominated by aux |
| Merge (slicing naive) | O(n log n) alloc churn | O(log n) | Avoid in interviews |
| Quick in-place | O(1) | O(log n) avg / O(n) worst | Tail recursion / iterate to help |
| Heap sort | O(1) | O(1) | Later module |
| Timsort | O(n) | O(1) | Run stack small |
| Counting | O(n+K) | O(1) | |

---

# PART 20: FULL INTERVIEW SCRIPT — COUNT OF RANGE SUM

> "I'll convert to prefix sums so a range sum is a difference of two prefixes.  
> I need the number of pairs i < j with lower ≤ P[j]-P[i] ≤ upper.  
> That's a classic modified merge sort: sort halves, count cross pairs with two pointers in linear time because both halves are sorted, then merge.  
> Recurrence same as merge sort → O(n log n) time, O(n) space.  
> I'll trace [-2,5,-1] with [-2,2] to show total 3.  
> Edge cases: empty array, single element, negative prefixes."

---

# PART 21: SELF-CHECK

Without notes:

1. Why comparison sorts are Ω(n log n).  
2. Merge sort recurrence + MT case.  
3. Lomuto partition in 5 lines + stability of quicksort.  
4. Three MT cases + one failure example.  
5. Why Python sort is stable and what Timsort optimizes.  
6. When counting sort beats comparison sorts.  
7. Count of Range Sum: prefix + why merge counts cross pairs in O(n).  
8. Inversion count: when you add `(mid - i)`.  
9. Classify `T(n)=4T(n/2)+n²` instantly.  
10. Two-pass multi-key sort: which pass runs last, and why stability matters.

---

# STATUS & EXCLUSIONS

| Item | After this lesson |
|---|---|
| Merge / Quick / Timsort / linear sorts / keys | `taught` |
| **Master Theorem** | `taught` (home module) |
| Count of Range Sum | earned for drill / re-credit timed |
| Heap internals | deferred Module 6 |
| Retention / timed | not yet |

**Next:** `Retention Questions/Module 3 Retention.md` — full grill with answers.
