# BINARY SEARCH — THE COMPLETE LESSON

**Module:** 3 — Searching & Sorting  
**Status target after this file:** `taught` (Binary Search track)  
**Language:** Python  
**Prerequisite:** Arrays (indexing, sorted order), Big O (log n intuition), Recursion (optional for recursive form)

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# SCOPE DOCUMENT

## In Scope (this lesson)

| Topic | Depth |
|---|---|
| Why binary search exists; sorted invariant | Full |
| Exact iterative template (lo / hi / mid) | Full — mechanical framework |
| Inclusive vs exclusive bounds | Full |
| Infinite-loop prevention; overflow-safe mid | Full |
| Exact find; lower_bound; upper_bound | Full |
| First / last occurrence; search insert position | Full |
| Binary search on answer (monotonic predicate) | Full |
| Rotated sorted array; peak element; integer sqrt / roots | Full |
| Python `bisect` (`bisect_left` / `bisect_right`) | Full deep dive |
| Off-by-one traps table | Full |
| Cheat sheets + interview communication | Full |
| 6+ worked problems with full traces | Full |

## Explicitly Deferred (named exclusions)

| Topic | Why deferred | Home module |
|---|---|---|
| Binary search on strings / suffix arrays | Needs string algorithms | Advanced Strings |
| Fractional / floating BS with epsilon craft | Needs numerical analysis care | Advanced / CP track |
| 2D matrix binary search variants beyond basics | Covered lightly; deep 2D → Arrays advanced | Arrays / Matrix |
| Ternary search on unimodal continuous functions | Separate pattern | Advanced Searching |
| Exponential search / unbounded arrays | Niche interview | Optional later |
| Parallel / cache-oblivious search | Systems, not interview DSA | Out of Phase A |

**Honest label after reading this file:** Binary Search is **covered for current scope** → status `taught`. Not `complete` until retention + timed verify.

---

# PART 0: WHY BINARY SEARCH EXISTS

## The Problem Binary Search Solves

You have a **sorted** collection. You need to find something — a value, a boundary, or the smallest/largest answer that satisfies a condition.

**Linear search** walks left to right: O(n). Fine for tiny n. Fatal when n is 10⁶ and you do this inside another loop.

**Binary search** exploits sorted order: each probe **halves** the remaining search space. O(log n) probes.

```
Unsorted: [7, 2, 9, 1, 5]  → must check everything → O(n)
Sorted:   [1, 2, 5, 7, 9]  → mid tells you which HALF to discard → O(log n)
```

### The Sorted Invariant (non-negotiable)

Binary search is not "guess the middle." It is:

> **If the array (or answer space) is ordered such that a predicate flips from false→true (or true→false) exactly once, you can discard half the space after each probe.**

That ordering is the **sorted invariant**. Break it and binary search lies.

| Situation | Binary search valid? |
|---|---|
| Strictly increasing array | ✅ |
| Non-decreasing (duplicates OK) with careful bounds | ✅ (use lower/upper bound) |
| Rotated sorted array | ✅ with modified compare |
| Unsorted array | ❌ — results are garbage |
| "Almost sorted" | ❌ unless you restore order or use a different algorithm |

**Interview line:** "Binary search requires a monotonic structure — sorted values or a monotonic predicate over the answer space."

---

## Why Interviews Love It

1. **O(log n)** is the expected upgrade from O(n) when sorted.
2. **Off-by-one bugs** separate people who memorized a loop from people who own a template.
3. **Binary search on answer** shows you can search a *space of answers*, not just an array index.
4. Python's `bisect` is fair game — knowing *when* to use it vs hand-rolling shows maturity.

---

# PART 1: THE MECHANICAL FRAMEWORK

## 1A: The Core Idea in One Picture

```
Search for target = 7 in [1, 3, 5, 7, 9, 11]

lo=0, hi=5
mid=2 → arr[2]=5 < 7 → discard left half including mid → lo = mid+1 = 3

lo=3, hi=5
mid=4 → arr[4]=9 > 7 → discard right half including mid → hi = mid-1 = 3

lo=3, hi=3
mid=3 → arr[3]=7 == 7 → FOUND
```

Each step: compare mid, throw away half. Remaining length ≈ n, n/2, n/4, … → ~log₂(n) steps.

---

## 1B: Inclusive Bounds Template (THE DEFAULT)

**Convention we use everywhere unless stated otherwise:**

- `lo` and `hi` are **inclusive** indices into the searchable range.
- Search space is `arr[lo … hi]` inclusive.
- Loop while `lo <= hi`.
- On `arr[mid] < target`: `lo = mid + 1`
- On `arr[mid] > target`: `hi = mid - 1`
- On equal: return mid (or continue for first/last variants)

```python
def binary_search_exact(arr, target):
    """
    Inclusive [lo, hi] template.
    Returns index of target, or -1 if absent.
    Assumes arr is sorted ascending.
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2   # overflow-safe; see §1D
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Why `lo <= hi` (not `lo < hi`)

With inclusive bounds, when `lo == hi` there is still **one** element left to check. If you use `lo < hi`, you exit before testing that last element — classic miss.

### Why `mid + 1` / `mid - 1`

You already compared `arr[mid]`. It cannot be the answer (for exact find when unequal). Including mid again risks an **infinite loop** when the window shrinks to size 1 incorrectly.

---

## 1C: Exclusive Upper Bound Template (ALTERNATE)

Some codebases (and C++ `lower_bound` style) use:

- `lo` inclusive, `hi` **exclusive**
- Search space is `arr[lo … hi)` 
- Loop while `lo < hi`
- Mid computation same
- On `arr[mid] < target`: `lo = mid + 1`
- Else: `hi = mid`  (mid might still be answer — do NOT do mid-1)

```python
def binary_search_exact_exclusive(arr, target):
    """Exclusive hi: search in [lo, hi)."""
    lo, hi = 0, len(arr)
    found = -1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            found = mid
            break  # or continue narrowing for first occurrence
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return found
```

**Rule:** Pick ONE convention per function and never mix mid-updates from the other. Mixing inclusive `lo<=hi` with exclusive `hi=mid` is how infinite loops are born.

| Convention | Loop | Too small | Too big | Empty check |
|---|---|---|---|---|
| Inclusive [lo,hi] | `lo <= hi` | `lo = mid+1` | `hi = mid-1` | start with `hi = n-1` |
| Exclusive [lo,hi) | `lo < hi` | `lo = mid+1` | `hi = mid` | start with `hi = n` |

---

## 1D: Mid Calculation — Avoid Overflow and Infinite Loops

### The Python-safe formula

```python
mid = lo + (hi - lo) // 2
```

In Python 3, integers are arbitrary precision — classic C overflow (`(lo+hi)/2` overflowing INT_MAX) does **not** happen. Still write the safe form:

1. Interviewers recognize it (shows C/Java awareness).
2. Habit transfers to languages where overflow is real.
3. It is clearer: "halfway from lo toward hi."

### The infinite-loop mid bug

```python
# DANGEROUS with exclusive-style updates
mid = (lo + hi) // 2
# if you then do hi = mid when lo == mid, and condition doesn't advance lo → spin forever
```

**Guarantee progress:** every iteration must either return, or strictly shrink `(hi - lo)`.

Checklist when debugging a hang:

1. Does `mid` always satisfy `lo <= mid <= hi` (inclusive) or `lo <= mid < hi` (exclusive)?
2. After the branch, is the new interval strictly smaller?
3. For size-1 windows, do you terminate?

---

## 1E: The Decision Framework (before coding)

```
1. Is the data / answer space MONOTONIC?
   NO  → binary search is the wrong tool
   YES → continue

2. What am I searching FOR?
   a) Exact value in sorted array          → exact template
   b) First position where condition true → lower_bound / first True
   c) First position where condition false after Trues → upper_bound style
   d) Smallest / largest FEASIBLE answer  → binary search on answer
   e) Structure is rotated / bitonic      → modified compare or peak find

3. Pick bound convention (inclusive default) and STICK TO IT.

4. Write the predicate / compare in ONE place. Trace on n=1, n=2, duplicates.
```

---

# PART 2: CORE VARIANTS

## 2A: Exact Find (already above)

Returns any index where `arr[i] == target`, or -1.

**Duplicates:** any matching index is correct for "exists?" problems. For "first" or "last", use §2B–2C.

---

## 2B: Lower Bound — First Index Where `arr[i] >= target`

Also called: leftmost insertion point, first not-less-than.

```python
def lower_bound(arr, target):
    """
    Smallest index i such that arr[i] >= target.
    If all elements < target, returns len(arr).
    Inclusive-style implemented via exclusive hi (cleanest for bounds).
    """
    lo, hi = 0, len(arr)  # hi exclusive
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            # arr[mid] >= target → mid could be the answer
            hi = mid
    return lo
```

### Trace: `arr = [1, 3, 3, 5, 7]`, target = 3

```
lo=0, hi=5
mid=2, arr[2]=3 >= 3 → hi=2
lo=0, hi=2
mid=1, arr[1]=3 >= 3 → hi=1
lo=0, hi=1
mid=0, arr[0]=1 < 3 → lo=1
lo=1, hi=1 → stop
return 1  ✅ first 3
```

### Trace: target = 4 (absent)

```
... ends at lo=3 (arr[3]=5) — insertion point for 4 ✅
```

### Trace: target = 0 (smaller than all)

```
Always arr[mid] >= 0 → hi shrinks to 0 → return 0 ✅
```

### Trace: target = 100 (larger than all)

```
Always arr[mid] < 100 → lo grows to 5 → return 5 == len(arr) ✅
```

---

## 2C: Upper Bound — First Index Where `arr[i] > target`

```python
def upper_bound(arr, target):
    """Smallest index i such that arr[i] > target. Else len(arr)."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

### Relationship

| Need | Formula |
|---|---|
| First occurrence of target | `lb = lower_bound(arr, target)`; valid if `lb < n and arr[lb]==target` |
| Last occurrence of target | `ub = upper_bound(arr, target); last = ub - 1` (check `last>=0 and arr[last]==target`) |
| Count of target | `upper_bound - lower_bound` |
| Insert to keep sorted (any equal OK) | either bound; Python `bisect_left` / `bisect_right` choose policy |

---

## 2D: First and Last Occurrence (explicit)

```python
def first_occurrence(arr, target):
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            ans = mid
            hi = mid - 1          # keep hunting left
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def last_occurrence(arr, target):
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            ans = mid
            lo = mid + 1          # keep hunting right
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans
```

**Interview communication:** "When I find a match, I record it and continue searching the half that might contain an earlier/later match."

---

## 2E: Search Insert Position

LeetCode 35: return index if found; else index where it would be inserted to keep sorted order.

**This is exactly `lower_bound`.**

```python
def search_insert(arr, target):
    return lower_bound(arr, target)
```

---

# PART 3: BINARY SEARCH ON ANSWER

## 3A: Why This Exists

Sometimes you are not searching an array index. You are searching the **answer itself**.

Classic shape:

> Find the **minimum** `x` such that `feasible(x)` is True  
> (or maximum `x` such that `feasible(x)` is True)

**Requirement:** `feasible` is **monotonic**.

```
x:        1  2  3  4  5  6  7  8  9
feasible: F  F  F  T  T  T  T  T  T   ← flips once F→T
```

If it flips more than once, binary search on answer is invalid.

### Framework

```python
def binary_search_on_answer(lo, hi, feasible):
    """
    Finds minimum x in [lo, hi] with feasible(x) True.
    Assumes: if feasible(x) then feasible(x+1)... (monotonic).
    If none feasible, returns hi+1 (or handle as problem requires).
    """
    ans = hi + 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            ans = mid
            hi = mid - 1      # try smaller
        else:
            lo = mid + 1      # need larger
    return ans
```

For **maximum** feasible:

```python
        if feasible(mid):
            ans = mid
            lo = mid + 1      # try larger
        else:
            hi = mid - 1
```

### How to invent `feasible`

1. State the answer type (integer capacity, days, distance, …).
2. Write a checker: "If I am allowed answer = mid, can I satisfy the constraints?" — usually O(n) or O(n log n).
3. Prove monotonicity in one sentence: "If I can finish in `d` days, I can finish in `d+1` days."
4. Bound `lo`/`hi` tightly (min possible answer … max possible answer).

**Total complexity:** O( (log (hi-lo)) × cost(feasible) ).

---

## 3B: Mini Example — Koko Eating Bananas (shape only)

Piles of bananas, `h` hours. Speed `k` bananas/hour. Can she finish?

- `feasible(k)` = total hours needed at speed k ≤ h
- Monotonic: larger k → fewer hours
- Search minimum k in `[1, max(piles)]`

Full worked version in Part 8 (Problem 4).

---

# PART 4: STRUCTURED ARRAY VARIANTS

## 4A: Rotated Sorted Array — Find Target

Array was sorted ascending, then rotated at unknown pivot:

```
Original: [0,1,2,4,5,6,7]
Rotated:  [4,5,6,7,0,1,2]
```

**Key insight:** At least one of the two halves `[lo…mid]` or `[mid…hi]` is **strictly sorted**. Identify which, then decide if target lies in that sorted half.

```python
def search_rotated(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid

        # Left half sorted?
        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # Right half sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

### Trace: `arr = [4,5,6,7,0,1,2]`, target = 0

```
lo=0, hi=6, mid=3, arr[3]=7 ≠ 0
arr[0]=4 <= 7 → left sorted. Is 4 <= 0 < 7? No → lo = 4

lo=4, hi=6, mid=5, arr[5]=1 ≠ 0
arr[4]=0 <= 1 → left sorted. Is 0 <= 0 < 1? Yes → hi = 4

lo=4, hi=4, mid=4, arr[4]=0 → FOUND ✅
```

### Duplicates trap

If `arr[lo] == arr[mid] == arr[hi]`, you cannot tell which half is sorted. Shrink carefully (`lo += 1` or `hi -= 1`) — worst case O(n). Mention this in interviews when the problem allows duplicates (LC 81).

---

## 4B: Find Minimum in Rotated Sorted Array

```python
def find_min_rotated(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] > arr[hi]:
            # min is strictly to the right of mid
            lo = mid + 1
        else:
            # mid could be the min
            hi = mid
    return arr[lo]
```

**Why compare to `arr[hi]`?** The right end is a reliable reference for rotation. If mid is greater than hi, the break point (minimum) is to the right.

---

## 4C: Peak Element

A peak is an index `i` where `arr[i] > arr[i-1]` and `arr[i] > arr[i+1]` (with sentinels -∞ at ends in the LC definition).

**Why binary search works:** From mid, if the slope goes up to the right (`arr[mid] < arr[mid+1]`), a peak exists on the right (unimodal argument / "there is always a peak in that direction"). Similarly left.

```python
def find_peak(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo  # index of a peak
```

---

## 4D: Integer Square Root / Integer Roots

Find floor(√x) — largest integer `m` with `m*m <= x`.

```python
def integer_sqrt(x):
    if x < 2:
        return x
    lo, hi = 1, x // 2
    ans = 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        sq = mid * mid
        if sq == x:
            return mid
        elif sq < x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans
```

**Generalization:** largest `m` with `m^k <= x` — same template, change the predicate.

**Overflow note:** In fixed-width ints, compare `mid <= x // mid` instead of `mid * mid <= x`.

---

## 4E: Search in Rotated Sorted Array II (duplicates) — LC 81

```python
def search_rotated_duplicates(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return True
        # Ambiguous: cannot tell which half is sorted
        if arr[lo] == arr[mid] == arr[hi]:
            lo += 1
            hi -= 1
            continue
        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

**Complexity:** Average still strong; **worst O(n)** when all equal (must shrink by 1 each time). Say this out loud.

## 4F: Find Minimum in Rotated Array II (duplicates)

Same ambiguity: when `nums[mid] == nums[hi]`, do `hi -= 1` (safe shrink). Worst O(n).

```python
def find_min_rotated_dup(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1  # nums[mid] == nums[hi]; drop hi
    return nums[lo]
```

---

# PART 5: PYTHON `bisect` MODULE — DEEP DIVE

```python
import bisect
```

Python's list has no tree. `bisect` binary-searches a **sorted list** and returns insertion indices. It does **not** keep the list sorted for you after inserts in the middle (insert is still O(n) due to shifting).

## 5A: `bisect_left` vs `bisect_right`

| Function | Meaning | Equals `...` |
|---|---|---|
| `bisect_left(a, x)` | Insertion point **before** any existing `x` | `lower_bound` (≥ x) |
| `bisect_right(a, x)` | Insertion point **after** any existing `x` | `upper_bound` (> x) |
| `bisect(a, x)` | Alias of `bisect_right` | — |

```python
a = [1, 3, 3, 5]
bisect.bisect_left(a, 3)   # 1
bisect.bisect_right(a, 3)  # 3
bisect.bisect_left(a, 4)   # 3
bisect.bisect_right(a, 4)  # 3
```

### When to use which

| Goal | Use |
|---|---|
| First index of x / insert before equals | `bisect_left` |
| Count of x | `bisect_right(a,x) - bisect_left(a,x)` |
| "How many elements ≤ x?" | `bisect_right(a, x)` |
| "How many elements < x?" | `bisect_left(a, x)` |
| "How many elements > x?" | `len(a) - bisect_right(a, x)` |
| Maintain sorted inserts (small n) | `bisect.insort_left` / `insort_right` |

## 5B: `insort`

```python
bisect.insort_left(a, x)   # insert at bisect_left position
bisect.insort_right(a, x)
```

**Complexity:** O(n) for the insert (memmove), O(log n) for the search. Fine for n ≲ few thousand in interviews if you say the complexity out loud. For heavy insert+order workloads, mention `SortedList` (sortedcontainers) or a balanced BST / fenwick — deferred modules.

## 5C: Key / lo / hi parameters

```python
bisect.bisect_left(a, x, lo=0, hi=len(a))
# Python 3.10+: key= callable — careful, key is applied to a[i], not always to x the same way
```

Prefer precomputing a keys array if the problem is hot path / interview clarity.

## 5D: Interview etiquette

- Using `bisect` is **allowed** and often preferred for clarity.
- Still must explain: "This is lower_bound — first index with value ≥ target."
- If the interviewer wants the algorithm, write the loop; if they want production Python, use `bisect`.

---

# PART 6: OFF-BY-ONE TRAPS TABLE

| Trap | Symptom | Fix |
|---|---|---|
| `while lo < hi` with inclusive `hi = mid-1` | Misses last element | Match convention: inclusive uses `lo <= hi` |
| `while lo <= hi` with exclusive `hi = mid` | Infinite loop when lo==mid | Exclusive uses `lo < hi` and `hi = mid` |
| `mid = (lo + hi) // 2` then `lo = mid` when `arr[mid] < t` | Infinite loop on size-2 | Use `lo = mid + 1` when mid is eliminated |
| Returning `lo` vs `hi` after loop | Off-by-one insert index | For lower_bound exclusive template, answer is `lo` |
| Forgetting `len(arr)==0` | IndexError on `hi = -1` | Guard empty; or exclusive hi=0 works naturally |
| Duplicates + "any index" vs "first" | Wrong LC answer | Use first/last or bisect_left |
| Rotated + duplicates | Wrong half chosen | Shrink ends when `arr[lo]==arr[mid]==arr[hi]` |
| `feasible` not monotonic | Random WA | Prove F→T single flip before coding |
| Using float mid for integer answers | Precision bugs | Keep integer mid; BS on ints |
| Comparing `mid*mid` in 32-bit | Overflow | Use `mid <= x // mid` |
| Assuming sorted input | Silent wrong | Confirm or sort first (cost O(n log n)) |
| `bisect` on unsorted list | Undefined nonsense | Sort first or don't use bisect |

---

# PART 7: CHEAT SHEETS

## 7A: Template Cheat Sheet

```
EXACT (inclusive):
  lo, hi = 0, n-1
  while lo <= hi:
    mid = lo + (hi-lo)//2
    if arr[mid] == t: return mid
    if arr[mid] < t: lo = mid+1
    else: hi = mid-1
  return -1

LOWER_BOUND (>= t):
  lo, hi = 0, n
  while lo < hi:
    mid = lo + (hi-lo)//2
    if arr[mid] < t: lo = mid+1
    else: hi = mid
  return lo

UPPER_BOUND (> t):
  same but if arr[mid] <= t: lo = mid+1 else hi = mid

ON ANSWER (min feasible):
  while lo <= hi:
    mid = ...
    if feasible(mid): ans, hi = mid, mid-1
    else: lo = mid+1

ROTATED SEARCH:
  identify sorted half via arr[lo] <= arr[mid]
  ask if target in that half; shrink accordingly
```

## 7B: Complexity Cheat Sheet

| Algorithm | Time | Space |
|---|---|---|
| Binary search on array | O(log n) | O(1) iterative / O(log n) recursive |
| Lower/upper bound | O(log n) | O(1) |
| BS on answer | O(log R · F) | depends on feasible |
| Rotated search (distinct) | O(log n) | O(1) |
| Rotated with duplicates | O(n) worst | O(1) |
| `bisect_*` | O(log n) | O(1) |
| `insort_*` | O(n) | O(1) extra |

## 7C: Interview Communication Script

1. "I'll confirm the array/answer space is monotonic."
2. "I'll use inclusive bounds / lower_bound style — here's why."
3. "Mid is `lo + (hi-lo)//2` to avoid overflow habits."
4. "Edge cases: empty, one element, all equal, target outside range."
5. "Complexity: O(log n) compares, O(1) extra space."

---

# PART 8: WORKED PROBLEMS (FULL TRACES)

---

## Problem 1: Exact Search + Missing Target

**Prompt:** Implement exact binary search. Trace both a hit and a miss.

```python
def binary_search_exact(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Trace A — Hit: `arr = [2, 4, 6, 8, 10, 12, 14]`, target = 10

```
lo=0 hi=6 mid=3 arr[3]=8 < 10 → lo=4
lo=4 hi=6 mid=5 arr[5]=12 > 10 → hi=4
lo=4 hi=4 mid=4 arr[4]=10 == 10 → return 4 ✅
```

### Trace B — Miss: target = 5

```
lo=0 hi=6 mid=3 arr[3]=8 > 5 → hi=2
lo=0 hi=2 mid=1 arr[1]=4 < 5 → lo=2
lo=2 hi=2 mid=2 arr[2]=6 > 5 → hi=1
lo=2 hi=1 → stop → return -1 ✅
```

### Edge cases

| Case | Result |
|---|---|
| `[]` | hi=-1, loop skipped, -1 |
| `[7]`, t=7 | return 0 |
| `[7]`, t=3 | return -1 |

> **Time: O(log n), Space: O(1)**

---

## Problem 2: First and Last Position in Sorted Array (LC 34)

**Prompt:** Given sorted `nums` and `target`, return `[first, last]` indices, or `[-1,-1]`.

```python
def search_range(nums, target):
    def first():
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                ans = mid
                hi = mid - 1
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    def last():
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                ans = mid
                lo = mid + 1
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    return [first(), last()]
```

### Trace: `nums = [5,7,7,8,8,10]`, target = 8

**First:**
```
lo=0 hi=5 mid=2 nums[2]=7 < 8 → lo=3
lo=3 hi=5 mid=4 nums[4]=8 → ans=4, hi=3
lo=3 hi=3 mid=3 nums[3]=8 → ans=3, hi=2
lo=3 hi=2 stop → first=3 ✅
```

**Last:**
```
lo=0 hi=5 mid=2 nums[2]=7 < 8 → lo=3
lo=3 hi=5 mid=4 nums[4]=8 → ans=4, lo=5
lo=5 hi=5 mid=5 nums[5]=10 > 8 → hi=4
lo=5 hi=4 stop → last=4 ✅
```

Return `[3,4]`.

### Alternative with bisect

```python
import bisect
def search_range_bisect(nums, target):
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]
```

> **Time: O(log n), Space: O(1)**

---

## Problem 3: Search Insert Position (LC 35)

```python
def search_insert(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

### Trace: `nums = [1,3,5,6]`, target = 5 → 2  
### Trace: target = 2

```
lo=0 hi=4 mid=2 nums[2]=5 >= 2 → hi=2
lo=0 hi=2 mid=1 nums[1]=3 >= 2 → hi=1
lo=0 hi=1 mid=0 nums[0]=1 < 2 → lo=1
return 1 ✅
```

> **Time: O(log n), Space: O(1)**

---

## Problem 4: Koko Eating Bananas (LC 875) — BS on Answer

**Prompt:** piles of bananas, `h` hours. Min speed `k` so Koko finishes.

```python
import math

def min_eating_speed(piles, h):
    def hours_needed(k):
        return sum((p + k - 1) // k for p in piles)  # ceil(p/k)

    lo, hi = 1, max(piles)
    ans = hi
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if hours_needed(mid) <= h:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

### Trace: `piles = [3,6,7,11]`, `h = 8`

```
max pile = 11. Search k in [1,11]

k=6: hours = ceil(3/6)+ceil(6/6)+ceil(7/6)+ceil(11/6) = 1+1+2+2 = 6 ≤ 8 → try smaller
k=3: 1+2+3+4 = 10 > 8 → need larger
k=4: 1+2+2+3 = 8 ≤ 8 → try smaller
k=5: ... eventually ans settles at 4

Verify k=4: 8 hours exactly ✅
k=3: 10 > 8 ❌
```

**Monotonicity:** If speed `k` works, `k+1` works. We want minimum k.

> **Time: O(n log M)** where M = max(piles), **Space: O(1)**

---

## Problem 5: Search in Rotated Sorted Array (LC 33)

Use `search_rotated` from §4A.

### Trace: `arr = [4,5,6,7,0,1,2]`, target = 3 (absent)

```
lo=0 hi=6 mid=3 val=7
left sorted [4..7]. 4<=3<7? No → lo=4
lo=4 hi=6 mid=5 val=1
left sorted [0,1]. 0<=3<1? No → lo=6
lo=6 hi=6 mid=6 val=2 ≠ 3 → lo=7
return -1 ✅
```

> **Time: O(log n), Space: O(1)**

---

## Problem 6: Find Peak Element (LC 162)

```python
def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

### Trace: `nums = [1,2,1,3,5,6,4]`

```
lo=0 hi=6 mid=3 nums[3]=3 < nums[4]=5 → lo=4
lo=4 hi=6 mid=5 nums[5]=6 > nums[6]=4 → hi=5
lo=4 hi=5 mid=4 nums[4]=5 < nums[5]=6 → lo=5
lo=5 hi=5 → return 5 (value 6) ✅ peak
```

> **Time: O(log n), Space: O(1)**

---

## Problem 7: Sqrt(x) Integer (LC 69)

Use `integer_sqrt` from §4D.

### Trace: x = 8

```
lo=1 hi=4
mid=2, 4 < 8 → ans=2, lo=3
mid=3, 9 > 8 → hi=2
lo>hi stop → return 2 ✅ (floor sqrt 8)
```

### Trace: x = 1 → return 1 (early)

> **Time: O(log x), Space: O(1)**

---

## Problem 8: Capacity To Ship Packages Within D Days (LC 1011)

**BS on answer** — minimum ship capacity.

```python
def ship_within_days(weights, days):
    def can_ship(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
            if d > days:
                return False
        return True

    lo, hi = max(weights), sum(weights)
    ans = hi
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can_ship(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

### Trace sketch: `weights=[1,2,3,4,5,6,7,8,9,10]`, `days=5`

```
lo = 10 (max weight), hi = 55 (sum)
feasible(cap) monotonic in cap
Binary search finds minimum cap = 15 ✅
```

> **Time: O(n log S)**, S = sum(weights), **Space: O(1)**

---

# PART 9: RECURSIVE BINARY SEARCH (OPTIONAL FORM)

```python
def binary_search_rec(arr, target, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = lo + (hi - lo) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_rec(arr, target, mid + 1, hi)
    return binary_search_rec(arr, target, lo, mid - 1)
```

**Space:** O(log n) stack. Prefer iterative in interviews unless recursion is requested.

**Master Theorem preview (full treatment in Sorting.md):**  
`T(n) = T(n/2) + O(1)` → Case 2 → **O(log n)**.

---

# PART 10: WHEN BINARY SEARCH IS THE WRONG TOOL

| Situation | Better approach |
|---|---|
| Unsorted, need membership many times | Hash set O(1) |
| Unsorted, one-time search | Linear O(n) — sorting first costs O(n log n) |
| Need all matches in unsorted data | Scan / hash |
| Non-monotonic feasible | Ternary search only if unimodal; else other methods |
| Need dynamic inserts + order stats | Balanced BST / SortedList (later modules) |

**Decision line:** "Is there a monotonic predicate I can evaluate cheaply? If yes, BS. If not, don't force it."

---

# PART 11: COMMON INTERVIEW FOLLOW-UPS

1. **Why not `mid = (lo+hi)//2`?** Overflow in fixed-width languages; Python OK but habit matters.
2. **Duplicates?** Specify first/last/any; adjust template.
3. **Overflow in `mid*mid`?** Use division form.
4. **Can you do it without the array?** BS on answer / math bounds.
5. **Time if we sort then search?** O(n log n + log n) = O(n log n) — sometimes still right vs O(n) hash if you need order.

---

# PART 12: PREDICATE DESIGN — THE HIDDEN SKILL

Most BS-on-answer failures are not off-by-one. They are **wrong predicates**.

## 12A: Recipe for inventing `feasible(mid)`

1. **Name the answer.** "I am searching for the minimum X such that …"
2. **Freeze mid as a candidate answer.** Pretend the interviewer gave you X = mid. Can you verify in O(n) or O(n log n)?
3. **Write `feasible(mid) -> bool` in plain English first**, then code.
4. **Prove monotonicity in one sentence.** "If X works, X+1 also works because …"
5. **Bound the search.** `lo` = smallest conceivable answer, `hi` = largest. Wrong bounds → WA or TLE.
6. **Decide min-feasible vs max-feasible.** That flips which side you shrink when True.

## 12B: Common predicate mistakes

| Mistake | Example | Fix |
|---|---|---|
| Searching the wrong quantity | Searching days when problem asks capacity | Re-read "return the minimum ___ " |
| Non-monotonic checker | "exactly h hours" instead of "≤ h" | Feasible must be prefix-closed |
| Off-by-one in checker | Using `<` instead of `<=` in capacity fill | Trace checker on tiny input alone |
| Bounds too tight | `hi = sum//days` without proof | Start loose; tighten only with proof |
| Floating answers | Using float mid for integer LC | Keep integer domain; BS ints |

## 12C: Worked predicate — Split Array Largest Sum (LC 410)

**Problem:** Split array into `m` non-empty continuous subarrays; minimize the **largest** subarray sum.

**Answer type:** the minimized largest sum (an integer).

**feasible(cap):** Can I split into ≤ m parts so each part sums ≤ cap?

```python
def split_array(nums, m):
    def can(cap):
        pieces, cur = 1, 0
        for x in nums:
            if x > cap:
                return False
            if cur + x > cap:
                pieces += 1
                cur = x
                if pieces > m:
                    return False
            else:
                cur += x
        return True

    lo, hi = max(nums), sum(nums)
    ans = hi
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

**Monotonicity:** If capacity `cap` works, `cap+1` works.

**Trace:** `nums=[7,2,5,10,8]`, m=2

```
lo=10, hi=32
mid=21: parts [7,2,5]=14, [10,8]=18 → 2 parts ≤2 → feasible → try smaller
...
settles at 18: [7,2,5]=14 and [10,8]=18 ✅
```

> **Time: O(n log S), Space: O(1)**

---

# PART 13: MORE WORKED PROBLEMS

---

## Problem 9: Time-Based Key-Value Store (bisect pattern)

Store `(timestamp, value)` per key. `get(key, t)` → value with largest timestamp ≤ t.

```python
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)  # key -> sorted (time, value) by time

    def set(self, key, value, timestamp):
        # Problem guarantees timestamps are non-decreasing per key
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        arr = self.store.get(key, [])
        lo, hi, ans = 0, len(arr) - 1, ""
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if arr[mid][0] <= timestamp:
                ans = arr[mid][1]   # candidate; try later times
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
```

**Interview point:** This is "last occurrence where time ≤ t" — upper_bound style, keep the best and search right.

**With bisect** (parallel times array):

```python
import bisect
i = bisect.bisect_right(times, timestamp) - 1
return values[i] if i >= 0 else ""
```

---

## Problem 10: Median of Two Sorted Arrays (LC 4) — HARD transfer

**Goal:** O(log(min(m,n))) without merging.

**Idea:** Binary search the partition point on the shorter array so that
`max(left_part) ≤ min(right_part)` across both arrays.

```python
def find_median_sorted_arrays(A, B):
    if len(A) > len(B):
        A, B = B, A
    m, n = len(A), len(B)
    lo, hi = 0, m
    half = (m + n + 1) // 2

    while lo <= hi:
        i = lo + (hi - lo) // 2          # cut in A
        j = half - i                       # cut in B
        Aleft = A[i - 1] if i > 0 else float("-inf")
        Aright = A[i] if i < m else float("inf")
        Bleft = B[j - 1] if j > 0 else float("-inf")
        Bright = B[j] if j < n else float("inf")

        if Aleft <= Bright and Bleft <= Aright:
            if (m + n) % 2 == 1:
                return float(max(Aleft, Bleft))
            return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.0
        elif Aleft > Bright:
            hi = i - 1
        else:
            lo = i + 1
```

### Trace sketch: A=[1,3], B=[2]

```
half = 2
i=1 → j=1; Aleft=1, Aright=3, Bleft=2, Bright=inf
1<=inf and 2<=3 → odd total → median max(1,2)=2 ✅
```

> **Time: O(log(min(m,n))), Space: O(1)**

**Why it's still binary search:** You search the cut index; the predicate "Aleft ≤ Bright" guides shrink direction. Monotonic in the cut.

---

## Problem 11: Find K Closest Elements (LC 658)

Sorted arr; find k closest to x. Return in ascending order.

```python
def find_closest_elements(arr, k, x):
    # Binary search the leftmost index of the window of size k
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = lo + (hi - lo) // 2
        # window [mid, mid+k). Compare distances of endpoints to x
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return arr[lo:lo + k]
```

**Invariant:** Among windows of length k, search the best starting index. The comparison is monotonic in `mid`.

> **Time: O(log(n-k) + k), Space: O(1) excluding output**

---

## Problem 12: Single Element in a Sorted Array (LC 540)

Every element appears twice except one. O(log n), O(1) space.

```python
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if mid % 2 == 1:
            mid -= 1  # align to even index (pair start)
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return nums[lo]
```

**Insight:** Before the single element, pairs sit at (even,odd) indices. After, pairing is shifted. Binary search on that pattern.

---

# PART 14: EDGE CASE CATALOG (MEMORIZE)

| Input | Exact find | Lower bound | BS on answer |
|---|---|---|---|
| Empty array | -1 / False | 0 | define problem |
| One element hit | 0 | 0 | lo=hi=answer |
| One element miss | -1 | 0 or 1 | — |
| All equal to target | any / first / last | 0 | — |
| Target < all | -1 | 0 | — |
| Target > all | -1 | n | — |
| Duplicates | specify policy | left edge | — |
| Negatives | fine if sorted | fine | checker must handle |
| INT_MAX mid*mid | overflow in C/Java | use div form | — |
| Rotated duplicates | may degrade O(n) | — | — |

**Always test in interview narration:** empty, n=1, all equal, target outside.

---

# PART 15: DEBUGGING PLAYBOOK (WHEN YOUR BS IS WRONG)

1. **Print (lo, hi, mid, arr[mid])** for 5 iterations on a failing case.
2. Check: does `(hi-lo)` strictly decrease every iteration?
3. Check: on exit, is `lo` the lower_bound you intended? Hand-compute expected index.
4. Separate bugs: is the **search** wrong or the **feasible** wrong? Unit-test `feasible` alone.
5. Re-derive updates from the convention table — don't "fix by flipping mid±1 randomly."

---

# PART 16: INTERVIEW COMMUNICATION — FULL SCRIPT

> "I'll confirm the array is sorted / the answer space is monotonic.  
> I'm using an inclusive lo/hi template with `mid = lo + (hi-lo)//2`.  
> For first occurrence I'll keep searching left after a hit.  
> Edge cases: empty, single element, duplicates, target outside range.  
> Complexity: O(log n) time, O(1) extra space.  
> If this were production Python for bounds, I'd use `bisect_left` and explain it as lower_bound."

For BS-on-answer add:

> "My feasible(mid) checks [one sentence]. It's monotonic because [one sentence].  
> I search [min/max] mid in [lo, hi] = […]. Total time O(F log R)."

---

# PART 17: PATTERN → PROBLEM MAP

| Pattern | Landmark problems |
|---|---|
| Exact / lower / upper | LC 35, 34, 704 |
| BS on answer (min feasible) | LC 875, 1011, 410, 1482 |
| Rotated sorted | LC 33, 81, 153, 154 |
| Peak / bitonic | LC 162, 852 |
| Integer root | LC 69 |
| Partition / median | LC 4 |
| Bisect on timeline | LC 981 |
| Pair-index parity | LC 540 |

---

# PART 18: SELF-CHECK (before retention grill)

Explain without notes:

1. Inclusive vs exclusive bound updates — one example each.
2. Why `lo = mid` can infinite-loop.
3. Lower vs upper bound in one sentence each.
4. One BS-on-answer problem: state `feasible` and monotonicity.
5. Rotated array: how you know which half is sorted.
6. `bisect_left` vs `bisect_right` on `[1,2,2,2,3]` for x=2.
7. Why LC 410's `can(cap)` is monotonic.
8. Walk median-of-two-arrays cut condition in one sentence.

If any answer is fuzzy → re-read that part. Do not mark Binary Search `drilled` until you can code lower_bound and BS-on-answer cold.

---

# STATUS & EXCLUSIONS SUMMARY

| Item | Status after this lesson |
|---|---|
| Binary Search core + variants + bisect | `taught` |
| Retention / timed | not yet |
| Advanced string BS, ternary, unbounded | **Deferred** (named above) |

**Next in Module 3:** `Sorting.md` — Merge Sort, Quick Sort, **Master Theorem (home module)**, Timsort, Count of Range Sum re-credit.
