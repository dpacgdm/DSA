# Answer Key — Module 3 Retention.md

**Source questions:** `Retention Questions/Module 3 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
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


<!-- answer block 2 -->
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


<!-- answer block 3 -->
### Answer

Search range size is O(n) initially (hi = n). Each step halves → **O(log n)** iterations.

Each iteration: arithmetic O(1) (Python big-ints: multiplying mid~√n is still treated as O(1) for interview DSA unless specified).

**Space:** O(1).

**Note:** Better bound hi = n for n<2 and n//2 otherwise — same asymptotics.

> **Time: O(log n), Space: O(1)**

---


<!-- answer block 4 -->
### Answer

- `sorted(arr)` → **O(n log n)** time, **O(n)** space (new list).
- Binary search → O(log n).

**Dominant:** **O(n log n)** time, **O(n)** space.

**Sort is unnecessary for membership of a single value:** `return 0 in arr` is **O(n)** time, **O(1)** space — strictly better for this problem.

Sort+BS only wins when you do **many** queries on a static array (pay O(n log n) once, then O(log n) each).

> **Time: O(n log n), Space: O(n). Sort unnecessary for one query — linear scan O(n).**

---


<!-- answer block 5 -->
### Answer

- a=2, b=2, f(n)=Θ(n^c) with c=1
- log_b(a) = log₂(2) = 1 = c → **Case 2**
- **T(n) = Θ(n log n)**

> **Case 2 → Θ(n log n)**

---


<!-- answer block 6 -->
### Answer

Recurrence: `T(n) = T(n-1) + Θ(n)`.

**MT does not apply** — size shrinks by subtraction, not division by constant b.

Unroll: T(n) = Θ(n) + Θ(n-1) + … + Θ(1) = **Θ(n²)**.

> **MT fails. T(n) = Θ(n²)**

---


<!-- answer block 7 -->
### Answer

- `bisect_left` → **1** (first index where a[i] >= 2; first 2)
- `bisect_right` → **4** (first index where a[i] > 2)
- Count = 4 - 1 = **3**

> **left=1, right=4, count=3**

---


<!-- answer block 8 -->
### Answer

Every partition puts pivot at the end with empty right / full left (or vice versa depending on `<=`): sizes n-1 and 0.

`T(n) = T(n-1) + Θ(n) = Θ(n²)`.

> **Θ(n²)**

---


<!-- answer block 9 -->
### Answer

Binary search requires that the search space is ordered so a predicate (or comparisons against a target) lets you **discard half** after each probe. Equivalently: there is a single transition false→true (or true→false) across the ordered domain.

**Valid BS-on-answer:** Minimum eating speed k such that `hours(k) ≤ h`. If k works, k+1 works → monotonic → search min k.

**Invalid:** "Find any k where `f(k) == 0`" when f oscillates (multiple roots, non-monotonic). Halving can discard the only root.

---


<!-- answer block 10 -->
### Answer

**Merge:** When left and right heads are equal, take from the **left** first. Equal elements keep their prior relative order → stable.

**Quicksort:** Partition swaps elements across the pivot based on `<`/`>` tests; equal keys can be reordered arbitrarily relative to each other → unstable.

---


<!-- answer block 11 -->
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


<!-- answer block 12 -->
### Answer

- **Timsort** (merge-sort family with run detection)
- **Stable**
- Best **O(n)** (already sorted runs), worst **O(n log n)**
- Extra space **O(n)** worst case

**Hand-implement merge/quick when:** interviewer asks you to write a sort; you need a modified merge (inversions, range sum); you must show partition skill (quickselect).

---


<!-- answer block 13 -->
### Answer

**Appropriate:** Integer keys in a small range 0..K with K = O(n) or acceptable vs n; need stable linear-ish sort.

**Disaster:** K ≫ n (e.g. arbitrary large IDs) — O(n+K) time/space blows up; or non-integer keys without a compact ranking.

---


<!-- answer block 14 -->
### Answer

| | Inclusive | Exclusive |
|---|---|---|
| Init hi | n-1 | n |
| Loop | `lo <= hi` | `lo < hi` |
| Too big | `hi = mid - 1` | `hi = mid` |

**Mixing** (e.g. `lo <= hi` with `hi = mid`) → mid can stick, **infinite loop**, or skip the answer.

---


<!-- answer block 15 -->
### Answer

**Sort first** if order unlocks a better algorithm (binary search, two pointers on sorted data, greedy by key, merge intervals) and the O(n log n) cost is acceptable.

**Don't sort** if hash membership already O(n) total for one-shot queries; if you only need min/max/kth (heap/quickselect); if you must preserve online/streaming constraints.

Example sort-yes: merge intervals.  
Example sort-no: "is target in unsorted array once?" → linear or hash.

---


<!-- answer block 16 -->
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


<!-- answer block 17 -->
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


<!-- answer block 18 -->
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


<!-- answer block 19 -->
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


<!-- answer block 20 -->
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


<!-- answer block 21 -->
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


<!-- answer block 22 -->
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


<!-- answer block 23 -->
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


<!-- answer block 24 -->
### Answer

**False.** Sort+BS is O(n log n) preprocess + O(log n)/query. Hash set is expected O(n) build + O(1)/query for membership, and does not need order. Sort+BS wins when you need **order** (bounds, closest, ranges), not raw membership.

---


<!-- answer block 25 -->
### Answer

1. `T(n)=T(n-1)+n` (subtractive)  
2. `T(n)=T(n/3)+T(2n/3)+n` (unequal sizes)  
3. `T(n)=2T(n/2)+n/log n` (f not polynomial Θ(n^c) in basic form)

---


<!-- answer block 26 -->
### Answer

Merge sort or Timsort. "Θ(n log n) time, O(n) auxiliary space, stable because equal elements prefer the left run on merge."

---


<!-- answer block 27 -->
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


