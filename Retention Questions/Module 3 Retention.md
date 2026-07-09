# MODULE 3 RETENTION GRILL — Searching & Sorting

**Covers:** Binary Search (templates, bounds, bisect, BS-on-answer, rotated/peak/sqrt) + Sorting (Merge, Quick, Timsort, linear sorts, custom keys) + **Master Theorem** + Count of Range Sum (earned re-credit)

**Style:** Same as `Week 1.md` — questions with **full worked answers**.

**Rules for the student (when taking live):**
1. No notes for Section A.
2. Section C: struggle ≥ 15 min per problem before peeking.
3. Tag misses: knowledge-gap / misread / time-pressure / careless-slip.
4. Chat-guided solves = `drilled` only, not `timed-verified`.

---

# SECTION A: RAPID FIRE — COMPLEXITY & BINARY SEARCH BUGS

---

## A1.

```python
def func(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**What's wrong?** (Assume `arr` sorted ascending.)

### Answer

**Bug:** Loop condition is `lo < hi` while updates use **inclusive** `hi = mid - 1` / `lo = mid + 1`.

When one element remains (`lo == hi`), the loop **exits without testing** that element. If the target is at that last index, you return -1 incorrectly.

**Example:** `arr = [1, 3, 5]`, target = 5.

```
lo=0 hi=2 mid=1 arr[1]=3 < 5 → lo=2
lo=2 hi=2 → while lo < hi fails → return -1  ❌ should be index 2
```

**Fix:** Use `while lo <= hi` with this update style, **or** switch fully to exclusive-hi lower_bound style (`hi = mid`, loop `lo < hi`).

> **Error type if missed:** knowledge-gap (bound convention)

---

## A2.

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid
        else:
            hi = mid
    return lo
```

**Does this terminate? What's the complexity if it runs?**

### Answer

**Infinite loop risk:** When `arr[mid] < target` and `mid == lo` (window size 1: `hi = lo+1`, mid = lo), setting `lo = mid` does **not** shrink the interval → spin forever.

**Example:** `arr=[1,2]`, target=2.

```
lo=0 hi=2 mid=1 arr[1]=2 >= 2 → hi=1
lo=0 hi=1 mid=0 arr[0]=1 < 2 → lo = mid = 0  # NO PROGRESS
```

**Fix:** `lo = mid + 1` on the `<` branch (standard lower_bound).

If corrected: **O(log n)** time, **O(1)** space.

> **Time (buggy): may not halt. Fixed: O(log n), Space: O(1)**

---

## A3.

```python
def func(n):
    # binary search for floor(sqrt(n)), n >= 0
    lo, hi = 0, n
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if mid * mid <= n:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi
```

**Time complexity in terms of n? Space?**

### Answer

Search range size is O(n) initially (hi = n). Each step halves → **O(log n)** iterations.

Each iteration: arithmetic O(1) (Python big-ints: multiplying mid~√n is still treated as O(1) for interview DSA unless specified).

**Space:** O(1).

**Note:** Better bound hi = n for n<2 and n//2 otherwise — same asymptotics.

> **Time: O(log n), Space: O(1)**

---

## A4.

```python
def func(arr):
    arr = sorted(arr)
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == 0:
            return True
        if arr[mid] < 0:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

**Time? Space? Is the sort necessary if we only check membership of 0?**

### Answer

- `sorted(arr)` → **O(n log n)** time, **O(n)** space (new list).
- Binary search → O(log n).

**Dominant:** **O(n log n)** time, **O(n)** space.

**Sort is unnecessary for membership of a single value:** `return 0 in arr` is **O(n)** time, **O(1)** space — strictly better for this problem.

Sort+BS only wins when you do **many** queries on a static array (pay O(n log n) once, then O(log n) each).

> **Time: O(n log n), Space: O(n). Sort unnecessary for one query — linear scan O(n).**

---

## A5.

Merge sort recurrence: `T(n) = 2T(n/2) + Θ(n)`. Apply Master Theorem. State case and result.

### Answer

- a=2, b=2, f(n)=Θ(n^c) with c=1
- log_b(a) = log₂(2) = 1 = c → **Case 2**
- **T(n) = Θ(n log n)**

> **Case 2 → Θ(n log n)**

---

## A6.

```python
def T_sketch(n):
    if n <= 1:
        return
    T_sketch(n - 1)
    # Θ(n) work
    for i in range(n):
        pass
```

Can you apply the basic Master Theorem? What is T(n)?

### Answer

Recurrence: `T(n) = T(n-1) + Θ(n)`.

**MT does not apply** — size shrinks by subtraction, not division by constant b.

Unroll: T(n) = Θ(n) + Θ(n-1) + … + Θ(1) = **Θ(n²)**.

> **MT fails. T(n) = Θ(n²)**

---

## A7.

`bisect.bisect_left(a, x)` vs `bisect.bisect_right(a, x)` on `a = [1, 2, 2, 2, 3]`, `x = 2`.  
Also: how many 2's?

### Answer

- `bisect_left` → **1** (first index where a[i] >= 2; first 2)
- `bisect_right` → **4** (first index where a[i] > 2)
- Count = 4 - 1 = **3**

> **left=1, right=4, count=3**

---

## A8.

Quick sort with Lomuto, always pivot = last element, input already sorted ascending. Worst-case time?

### Answer

Every partition puts pivot at the end with empty right / full left (or vice versa depending on `<=`): sizes n-1 and 0.

`T(n) = T(n-1) + Θ(n) = Θ(n²)`.

> **Θ(n²)**

---

# SECTION B: CONCEPTUAL

---

## B1.

Explain the **sorted / monotonic invariant** required for binary search. Give one valid and one invalid scenario for "binary search on answer."

### Answer

Binary search requires that the search space is ordered so a predicate (or comparisons against a target) lets you **discard half** after each probe. Equivalently: there is a single transition false→true (or true→false) across the ordered domain.

**Valid BS-on-answer:** Minimum eating speed k such that `hours(k) ≤ h`. If k works, k+1 works → monotonic → search min k.

**Invalid:** "Find any k where `f(k) == 0`" when f oscillates (multiple roots, non-monotonic). Halving can discard the only root.

---

## B2.

Why is merge sort **stable** with the standard merge, and why is classic in-place quicksort **not**?

### Answer

**Merge:** When left and right heads are equal, take from the **left** first. Equal elements keep their prior relative order → stable.

**Quicksort:** Partition swaps elements across the pivot based on `<`/`>` tests; equal keys can be reordered arbitrarily relative to each other → unstable.

---

## B3.

State the three Master Theorem cases for `T(n) = a T(n/b) + Θ(n^c)`. Then classify:

1. `T(n) = 7T(n/2) + n²`
2. `T(n) = T(n/2) + 1`
3. `T(n) = 2T(n/2) + n log n` (say what changes)

### Answer

**Cases:**
1. log_b(a) > c → Θ(n^{log_b a})
2. log_b(a) = c → Θ(n^c log n)
3. log_b(a) < c → Θ(n^c) (with regularity)

**Classify:**
1. log₂7 ≈ 2.807 > 2 → Case 1 → **Θ(n^{log₂ 7})**
2. a=1,b=2,c=0; log₂1=0=c → Case 2 → **Θ(log n)**
3. Basic poly form fails / extended Case 2: f(n)=Θ(n log n) with log_b a = 1 → **Θ(n log² n)**

---

## B4.

Python `list.sort` — algorithm family, stability, best/worst time, extra space. When would you still implement merge sort by hand in an interview?

### Answer

- **Timsort** (merge-sort family with run detection)
- **Stable**
- Best **O(n)** (already sorted runs), worst **O(n log n)**
- Extra space **O(n)** worst case

**Hand-implement merge/quick when:** interviewer asks you to write a sort; you need a modified merge (inversions, range sum); you must show partition skill (quickselect).

---

## B5.

When is **counting sort** appropriate? When is it a disaster?

### Answer

**Appropriate:** Integer keys in a small range 0..K with K = O(n) or acceptable vs n; need stable linear-ish sort.

**Disaster:** K ≫ n (e.g. arbitrary large IDs) — O(n+K) time/space blows up; or non-integer keys without a compact ranking.

---

## B6.

Inclusive `[lo,hi]` vs exclusive `[lo,hi)` binary search: give the loop condition and the "too big" update for each. What happens if you mix them?

### Answer

| | Inclusive | Exclusive |
|---|---|---|
| Init hi | n-1 | n |
| Loop | `lo <= hi` | `lo < hi` |
| Too big | `hi = mid - 1` | `hi = mid` |

**Mixing** (e.g. `lo <= hi` with `hi = mid`) → mid can stick, **infinite loop**, or skip the answer.

---

## B7.

"Should I sort first?" — give the decision rule and one example each way.

### Answer

**Sort first** if order unlocks a better algorithm (binary search, two pointers on sorted data, greedy by key, merge intervals) and the O(n log n) cost is acceptable.

**Don't sort** if hash membership already O(n) total for one-shot queries; if you only need min/max/kth (heap/quickselect); if you must preserve online/streaming constraints.

Example sort-yes: merge intervals.  
Example sort-no: "is target in unsorted array once?" → linear or hash.

---

# SECTION C: PROBLEM SOLVING (ESCALATING)

---

## C1: First Bad Version (BS on answer / lower_bound)

API: `isBadVersion(v) -> bool`. Versions `1..n`. All bad versions come after all good. Find first bad.

### Approach

Monotonic: once bad, all later are bad. Find minimum v with `isBadVersion(v) == True`.

### Solution

```python
def first_bad_version(n):
    lo, hi = 1, n
    ans = n
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if isBadVersion(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

### Trace: n=5, bad from 4

```
lo=1 hi=5 mid=3 good → lo=4
lo=4 hi=5 mid=4 bad → ans=4, hi=3
lo>hi → return 4 ✅
```

### Complexity

> **Time: O(log n) API calls, Space: O(1)**

---

## C2: Search a 2D Matrix (LC 74 style)

`matrix` rows sorted left→right; first of each row > last of previous. Find target.

### Approach

Treat as virtual 1D sorted array of length m*n. Map `mid → (mid//cols, mid%cols)`.

### Solution

```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

### Trace: `[[1,3,5],[7,9,11]]`, target=9

```
len=6, mid=2 val=5 < 9 → lo=3
mid=4 val=9 → True ✅
```

> **Time: O(log(mn)), Space: O(1)**

---

## C3: Find Minimum in Rotated Sorted Array (distinct)

### Solution

```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```

### Trace: `[4,5,6,7,0,1,2]`

```
mid=3 val=7 > hi=2 → lo=4
mid=5 val=1 < hi=2 → hi=5
mid=4 val=0 < hi=1 → hi=4
lo=hi=4 → return 0 ✅
```

> **Time: O(log n), Space: O(1)**

---

## C4: Koko Eating Bananas

`piles`, `h` hours. Min integer speed.

### Solution

```python
def min_eating_speed(piles, h):
    def ok(k):
        return sum((p + k - 1) // k for p in piles) <= h

    lo, hi, ans = 1, max(piles), max(piles)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if ok(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

### Monotonicity

Larger k → fewer hours → if mid feasible, try smaller.

### Trace sketch: piles=[30,11,23,4,20], h=6 → answer 23

> **Time: O(n log M), M=max(piles), Space: O(1)**

---

## C5: Implement Merge Sort + Prove Complexity via MT

Write index-based merge sort. State recurrence and MT case.

### Solution

```python
def merge_sort(arr):
    a = arr[:]
    aux = [0] * len(a)

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = lo + (hi - lo) // 2
        sort(lo, mid)
        sort(mid, hi)
        for k in range(lo, hi):
            aux[k] = a[k]
        i, j = lo, mid
        for k in range(lo, hi):
            if i >= mid:
                a[k] = aux[j]; j += 1
            elif j >= hi:
                a[k] = aux[i]; i += 1
            elif aux[j] < aux[i]:
                a[k] = aux[j]; j += 1
            else:
                a[k] = aux[i]; i += 1

    sort(0, len(a))
    return a
```

**Recurrence:** T(n)=2T(n/2)+Θ(n) → MT Case 2 → **Θ(n log n)**. Space **O(n)**.

---

## C6: Lomuto Partition + Quick Sort Worst Case Fix

(a) Implement Lomuto.  
(b) Show sorted input → n².  
(c) Add randomized pivot swap.

### Solution

```python
import random

def partition(arr, lo, hi):
    pivot = arr[hi]
    store = lo
    for i in range(lo, hi):
        if arr[i] <= pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    return store


def quick_sort(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    r = random.randint(lo, hi)
    arr[r], arr[hi] = arr[hi], arr[r]
    p = partition(arr, lo, hi)
    quick_sort(arr, lo, p - 1)
    quick_sort(arr, p + 1, hi)
```

**(b)** Sorted + fixed last pivot → T(n)=T(n-1)+Θ(n)=Θ(n²).  
**(c)** Random pivot → expected O(n log n).

---

## C7: Count of Range Sum — EARNED RE-CREDIT

> Formerly Week 2 PREVIEW #11. Now earned Module 3 credit.

**Problem:** Count ranges whose sum ∈ `[lower, upper]`.

### Approach

Prefix sums. Count pairs i < j with `lower ≤ prefix[j]-prefix[i] ≤ upper` via modified merge sort: O(n) cross counting per level on sorted halves.

### Solution

```python
def count_range_sum(nums, lower, upper):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    def sort_count(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = lo + (hi - lo) // 2
        count = sort_count(lo, mid) + sort_count(mid, hi)

        lo_ptr = hi_ptr = lo
        for j in range(mid, hi):
            while lo_ptr < mid and prefix[lo_ptr] < prefix[j] - upper:
                lo_ptr += 1
            while hi_ptr < mid and prefix[hi_ptr] <= prefix[j] - lower:
                hi_ptr += 1
            count += hi_ptr - lo_ptr

        merged = []
        p, q = lo, mid
        while p < mid and q < hi:
            if prefix[q] < prefix[p]:
                merged.append(prefix[q]); q += 1
            else:
                merged.append(prefix[p]); p += 1
        merged.extend(prefix[p:mid])
        merged.extend(prefix[q:hi])
        prefix[lo:hi] = merged
        return count

    return sort_count(0, len(prefix))
```

### Full Trace: nums=`[-2,5,-1]`, lower=-2, upper=2

```
prefix = [0, -2, 3, 2]

Left [0,-2]: cross counts pair (0,-2) → sum -2 ✅ → +1; merge [-2,0]
Right [3,2]: cross counts (3,2) → sum -1 ✅ → +1; merge [2,3]
Cross left[-2,0] vs right[2,3]:
  j=2: i with i ∈ [0,4] → {0} → +1 (sum 2) ✅
  j=3: none
Total 3 ✅
```

### Edge Cases

- Empty nums → 0  
- Single 0 with [0,0] → 1  

> **Time: O(n log n), Space: O(n)**

### Why two pointers are O(n) per level

Right half sorted ascending in j; thresholds `prefix[j]-upper` and `prefix[j]-lower` non-decreasing → `lo_ptr`/`hi_ptr` only advance.

---

## C8: Sort + Two Pointers — 3Sum Count Sketch

Given nums, count triplets i < j < k with nums[i]+nums[j]+nums[k] = 0. (Interview sketch; careful with duplicates if returning unique triplets.)

### Approach

Sort O(n log n). For each i, two pointers on i+1..n-1. O(n²).

### Solution (count all index triplets, allowing duplicate values)

```python
def three_sum_count(nums):
    nums.sort()
    n = len(nums)
    count = 0
    for i in range(n):
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                count += 1
                lo += 1
                hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return count
```

**Note:** LC 15 asks unique triplets — after a hit, skip duplicate `lo`/`hi`/`i` values. Sorting was the enabling step.

> **Time: O(n²), Space: O(1) / O(n) sort**

---

# SECTION D: SYNTHESIS / TRAPS (SHORT)

---

## D1.

True or false: "Binary search is always O(log n), so sorting then binary searching membership is always better than a hash set."

### Answer

**False.** Sort+BS is O(n log n) preprocess + O(log n)/query. Hash set is expected O(n) build + O(1)/query for membership, and does not need order. Sort+BS wins when you need **order** (bounds, closest, ranges), not raw membership.

---

## D2.

Name three situations where Master Theorem does **not** apply.

### Answer

1. `T(n)=T(n-1)+n` (subtractive)  
2. `T(n)=T(n/3)+T(2n/3)+n` (unequal sizes)  
3. `T(n)=2T(n/2)+n/log n` (f not polynomial Θ(n^c) in basic form)

---

## D3.

You need a **stable** O(n log n) sort and must explain space. What do you pick and say?

### Answer

Merge sort or Timsort. "Θ(n log n) time, O(n) auxiliary space, stable because equal elements prefer the left run on merge."

---

## C9: Aggressive Cows / Magnetic Force Between Balls (BS on answer)

Place `m` balls in sorted positions `position` to **maximize** the minimum distance between any two balls.

### Approach

`feasible(d)`: Can I place m balls with each consecutive pair ≥ d apart? Greedy left-to-right. Monotonic: if d works, d-1 works. Search **maximum** d.

### Solution

```python
def max_min_distance(position, m):
    position.sort()
    def can(d):
        count, last = 1, position[0]
        for p in position[1:]:
            if p - last >= d:
                count += 1
                last = p
                if count >= m:
                    return True
        return False

    lo, hi, ans = 0, position[-1] - position[0], 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can(mid):
            ans = mid
            lo = mid + 1   # maximize
        else:
            hi = mid - 1
    return ans
```

### Trace: position=`[1,2,3,4,7]`, m=3

```
d=3: place at 1,4,7 → ok → try larger
d=4: 1, then need ≥5 → 7; only 2 balls → fail
ans=3 ✅
```

> **Time: O(n log n + n log D)**, D = max-min position, **Space: O(1)** besides sort

---

## C10: Master Theorem Speed Round (write only the Θ)

| # | Recurrence | Answer |
|---|---|---|
| 1 | 2T(n/2)+n | Θ(n log n) |
| 2 | 2T(n/2)+1 | Θ(n) |
| 3 | T(n/2)+1 | Θ(log n) |
| 4 | 3T(n/3)+n | Θ(n log n) |
| 5 | 8T(n/2)+n² | Θ(n³)  (Case 1: log₂8=3>2 → n³) |
| 6 | T(n-2)+1 | MT fails → Θ(n) |

**Note on #5:** a=8,b=2,c=2; L=3>2 → Case 1 → Θ(n³).  
**Note on #6:** subtractive; T(n)=T(n-2)+1 → ~n/2 steps → Θ(n).

---

# SCORING GUIDE (for self / tutor)

| Section | Pass bar |
|---|---|
| A (8) | ≥ 7 correct with right complexity/bug |
| B (7) | ≥ 6 conceptually solid |
| C (10) | ≥ 7 solved with correct complexity; **C7 required** for Module 3 sort credit; C10 ≥ 5/6 |
| D (3) | ≥ 2 |

**Fail any required:** C7 wrong algorithm family → re-teach modified merge on prefixes before advancing.

**After pass:** Update `Metrics/Retention Ledger.md` subskills (BS templates, lower/upper, BS-on-answer, merge, quick+MT, Timsort, Range Sum) → heat `strong`/`shaky`. Then schedule **timed verify** (blind 45–60 min) before status `timed-verified`.

---

# ANSWER KEY QUICK INDEX

| ID | Verdict summary |
|---|---|
| A1 | `lo < hi` with inclusive updates skips last element |
| A2 | `lo = mid` infinite loop; need `lo = mid+1` |
| A3 | O(log n) / O(1) |
| A4 | O(n log n); sort unnecessary for one membership |
| A5 | Case 2, Θ(n log n) |
| A6 | MT fails, Θ(n²) |
| A7 | 1, 4, count 3 |
| A8 | Θ(n²) |
| C7 | Prefix + modified merge; O(n log n); trace total 3 |

---

**Module 3 retention file complete.** Pair with:

- `Searching & Sorting/Binary Search.md`
- `Searching & Sorting/Sorting.md`
