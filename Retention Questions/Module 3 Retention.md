<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 3 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 3 Retention.keys.md`. Attempt first, then grade.

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


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 1)

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


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 2)

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


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 3)

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


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 4)

## A5.

Merge sort recurrence: `T(n) = 2T(n/2) + Θ(n)`. Apply Master Theorem. State case and result.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 5)

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


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 6)

## A7.

`bisect.bisect_left(a, x)` vs `bisect.bisect_right(a, x)` on `a = [1, 2, 2, 2, 3]`, `x = 2`.  
Also: how many 2's?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 7)

## A8.

Quick sort with Lomuto, always pivot = last element, input already sorted ascending. Worst-case time?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 8)

# SECTION B: CONCEPTUAL

---

## B1.

Explain the **sorted / monotonic invariant** required for binary search. Give one valid and one invalid scenario for "binary search on answer."


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 9)

## B2.

Why is merge sort **stable** with the standard merge, and why is classic in-place quicksort **not**?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 10)

## B3.

State the three Master Theorem cases for `T(n) = a T(n/b) + Θ(n^c)`. Then classify:

1. `T(n) = 7T(n/2) + n²`
2. `T(n) = T(n/2) + 1`
3. `T(n) = 2T(n/2) + n log n` (say what changes)


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 11)

## B4.

Python `list.sort` — algorithm family, stability, best/worst time, extra space. When would you still implement merge sort by hand in an interview?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 12)

## B5.

When is **counting sort** appropriate? When is it a disaster?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 13)

## B6.

Inclusive `[lo,hi]` vs exclusive `[lo,hi)` binary search: give the loop condition and the "too big" update for each. What happens if you mix them?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 14)

## B7.

"Should I sort first?" — give the decision rule and one example each way.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 15)

# SECTION C: PROBLEM SOLVING (ESCALATING)

---

## C1: First Bad Version (BS on answer / lower_bound)

API: `isBadVersion(v) -> bool`. Versions `1..n`. All bad versions come after all good. Find first bad.

### Approach

Monotonic: once bad, all later are bad. Find minimum v with `isBadVersion(v) == True`.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 16)

## C2: Search a 2D Matrix (LC 74 style)

`matrix` rows sorted left→right; first of each row > last of previous. Find target.

### Approach

Treat as virtual 1D sorted array of length m*n. Map `mid → (mid//cols, mid%cols)`.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 17)

## C3: Find Minimum in Rotated Sorted Array (distinct)


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 18)

## C4: Koko Eating Bananas

`piles`, `h` hours. Min integer speed.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 19)

## C5: Implement Merge Sort + Prove Complexity via MT

Write index-based merge sort. State recurrence and MT case.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 20)

## C6: Lomuto Partition + Quick Sort Worst Case Fix

(a) Implement Lomuto.  
(b) Show sorted input → n².  
(c) Add randomized pivot swap.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 21)

## C7: Count of Range Sum — EARNED RE-CREDIT

> Formerly Week 2 PREVIEW #11. Now earned Module 3 credit.

**Problem:** Count ranges whose sum ∈ `[lower, upper]`.

### Approach

Prefix sums. Count pairs i < j with `lower ≤ prefix[j]-prefix[i] ≤ upper` via modified merge sort: O(n) cross counting per level on sorted halves.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 22)

## C8: Sort + Two Pointers — 3Sum Count Sketch

Given nums, count triplets i < j < k with nums[i]+nums[j]+nums[k] = 0. (Interview sketch; careful with duplicates if returning unique triplets.)

### Approach

Sort O(n log n). For each i, two pointers on i+1..n-1. O(n²).


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 23)

# SECTION D: SYNTHESIS / TRAPS (SHORT)

---

## D1.

True or false: "Binary search is always O(log n), so sorting then binary searching membership is always better than a hash set."


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 24)

## D2.

Name three situations where Master Theorem does **not** apply.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 25)

## D3.

You need a **stable** O(n log n) sort and must explain space. What do you pick and say?


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 26)

## C9: Aggressive Cows / Magnetic Force Between Balls (BS on answer)

Place `m` balls in sorted positions `position` to **maximize** the minimum distance between any two balls.

### Approach

`feasible(d)`: Can I place m balls with each consecutive pair ≥ d apart? Greedy left-to-right. Monotonic: if d works, d-1 works. Search **maximum** d.


> **Answer key:** `Retention Questions/keys/Module 3 Retention.keys.md` (block 27)

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
