# ARRAYS — ADVANCED PATTERNS

**Module:** 6 (Heaps + Advanced Array Patterns)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Prerequisite:** `Arrays/Arrays.md` Module 1 — especially Two Pointers + Sliding Window basics  
**Language:** Python

---

# PART 0: HOW THIS DIFFERS FROM MODULE 1

Module 1 taught the **machinery**:

| Module 1 (basics) | Module 6 (this file) |
|---|---|
| Fixed window sum / average | Constraint windows with **frequency maps** and **deficit tracking** |
| Longest substring **without** repeating chars | Longest with **exactly / at most K distinct**; **minimum window covering** a requirement |
| Converging two pointers on sorted arrays | Geometry: **container with most water**, **trapping rain water** |
| Read/write partition (move zeroes, dedupe) | **Dutch National Flag** 3-way partition; general partition templates |
| Shrink while invalid (sum ≥ target, all positive) | Shrink while **valid** to minimize; product windows; hard covering constraints |

**Escalation rule:** Same `left`/`right` skeleton. Harder **window state**, harder **invariants**, and problems where the naive "expand then shrink" needs an extra data structure (counts, need/have, last-seen index).

If you cannot write Module 1 variable sliding window and converging two pointers cold, stop and redrill those first.

---

# PART 1: ADVANCED SLIDING WINDOW — UNIFIED FRAMEWORK

## 1A: The Skeleton (Unchanged)

```python
def variable_window(s):
    left = 0
    state = ...          # sum, product, Counter, need/have, distinct count, ...
    answer = ...

    for right in range(len(s)):
        # EXPAND: incorporate s[right] into state

        # SHRINK: while state violates constraint (or while we can tighten)
        while window_bad_or_can_shrink():
            # remove s[left] from state
            left += 1

        # UPDATE answer from window s[left:right+1]
    return answer
```

Both pointers only move forward → **O(n)** expansions + shrinks, if each update is O(1) amortized.

## 1B: What Changes at Advanced Level

The hard part is designing **state** and the **shrink condition**:

| Problem class | State | Shrink when |
|---|---|---|
| At most K distinct | `Counter` + `distinct` | `distinct > K` |
| Exactly K distinct | often: `at_most(K) - at_most(K-1)` | (derived) |
| Minimum window substring | `need` map + `have` / `formed` | window **valid** → shrink to minimize |
| Product < K | running `product` | `product >= K` |
| Longest with replacement / flips | counts + maxfreq | `window_len - maxfreq > K` |

## 1C: "At Most" vs "Minimum Covering" Mindset

```
MAXIMIZE length under a constraint
  → expand greedily; shrink only when INVALID
  → answer updated when window is valid (often every step after shrink)

MINIMIZE length under a covering constraint
  → expand until VALID; then shrink while STILL VALID
  → answer updated inside the shrink loop (every valid window)
```

This single distinction separates "longest substring with …" from "minimum window substring."

---

# PART 2: MINIMUM WINDOW SUBSTRING CLASS

## 2A: The Problem

Given strings `s` (haystack) and `t` (required characters, with multiplicity), find the **smallest** contiguous substring of `s` that covers every character in `t` (with at least those frequencies). Return `""` if impossible.

```
s = "ADOBECODEBANC", t = "ABC"
Answer: "BANC"
```

## 2B: Why Brute Force Dies

Every pair `(i, j)` → check if `s[i:j+1]` covers `t` → O(n² · Σ) with counting. Too slow.

## 2C: The Framework — need / have / formed

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)
    missing = len(need)          # how many unique chars still unsatisfied
    window = Counter()

    best_len = float('inf')
    best_start = 0
    left = 0

    for right, ch in enumerate(s):
        window[ch] += 1
        if ch in need and window[ch] == need[ch]:
            missing -= 1

        # Shrink while window is valid
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left

            left_ch = s[left]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                missing += 1
            left += 1

    return "" if best_len == float('inf') else s[best_start:best_start + best_len]
```

### Invariant

- `missing == 0` ⇔ current window satisfies all of `t`
- We only shrink when valid → every shrink candidate is a covering window
- Among covering windows ending at `right`, the one with largest `left` is the shortest for that `right`

### Trace

```
s = ADOBECODEBANC, t = ABC
need: A1 B1 C1, missing=3

right A: window A1 → missing=2
right D: ...
right O: ...
right B: window B1 → missing=1
right E: ...
right C: window C1 → missing=0  VALID "ADOBEC"
  shrink: remove A → missing=1  stop
  best = "ADOBEC" (len 6) ... continue

... eventually
right C (last): window covers again
  shrink until invalid → best becomes "BANC" (len 4) ✅
```

### Complexity

Time O(|s| + |t|). Space O(Σ) alphabet / unique chars in t.

## 2D: Family Problems (Same Skeleton)

| Problem | Twist |
|---|---|
| Minimum Window Substring | classic need/have |
| Find All Anagrams in a String | fixed window length = \|p\|; compare counts (or "matches" counter) |
| Permutation in String | same as anagrams — bool instead of indices |
| Smallest Range Covering K Lists | heap version (Heaps lesson) — related covering idea |

### Fixed-window anagram template (contrast)

```python
from collections import Counter

def find_anagrams(s, p):
    need = Counter(p)
    window = Counter()
    left = 0
    matches = 0  # optional optimization
    res = []
    for right, ch in enumerate(s):
        window[ch] += 1
        if right - left + 1 > len(p):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        if right - left + 1 == len(p) and window == need:
            res.append(left)
    return res
```

**Difference from min-window:** window size is **fixed**; you never "shrink while valid to minimize" — you slide by one.

---

# PART 3: LONGEST SUBSTRING WITH K DISTINCT / AT MOST K

## 3A: At Most K Distinct Characters

Find length of longest substring with **at most K** distinct characters.

```
s = "eceba", k = 2 → 3 ("ece")
s = "aa", k = 1 → 2 ("aa")
```

### Framework

```python
from collections import defaultdict

def longest_at_most_k(s, k):
    if k <= 0:
        return 0
    count = defaultdict(int)
    left = 0
    distinct = 0
    best = 0

    for right, ch in enumerate(s):
        if count[ch] == 0:
            distinct += 1
        count[ch] += 1

        while distinct > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                distinct -= 1
            left += 1

        best = max(best, right - left + 1)

    return best
```

### Trace

```
s = eceba, k = 2

r=0 e: {e:1} d=1 best=1
r=1 c: {e:1,c:1} d=2 best=2
r=2 e: {e:2,c:1} d=2 best=3
r=3 b: {e:2,c:1,b:1} d=3 > 2
  shrink e→{e:1,c:1,b:1} d=3
  shrink c→{e:1,b:1} d=2
  best = max(3, 3-2+1=2) → 3
r=4 a: d=3 → shrink to {b:1,a:1} best stays 3
Answer 3 ✅
```

## 3B: Exactly K Distinct

**Trick:** number of substrings (or longest) with **exactly K** =

```
f(at most K) - f(at most K - 1)
```

For **longest** substring with exactly K distinct: you can also shrink until distinct == K and track max — but the subtraction trick is cleaner for **counting** substrings.

### Count substrings with exactly K distinct

```python
def at_most(s, k):
    count = defaultdict(int)
    left = 0
    distinct = 0
    total = 0
    for right, ch in enumerate(s):
        if count[ch] == 0:
            distinct += 1
        count[ch] += 1
        while distinct > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                distinct -= 1
            left += 1
        # all subarrays ending at right with start in [left, right] are valid
        total += right - left + 1
    return total

def exactly_k(s, k):
    return at_most(s, k) - at_most(s, k - 1)
```

**Why `total += right - left + 1`?**  
Once `[left, right]` is the longest valid window ending at `right`, every subwindow `[i, right]` for `i ∈ [left, right]` also has ≤ K distinct.

## 3C: Related — Longest Repeating Character Replacement

You may replace at most `k` characters. Maximize length of a window that can become all one character.

**Key insight:** window is OK while `window_len - max_freq_in_window ≤ k` (replacements needed).

```python
def character_replacement(s, k):
    count = defaultdict(int)
    left = 0
    max_freq = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
            # note: max_freq need not be decremented (safe upper bound)
        best = max(best, right - left + 1)
    return best
```

**Subtlety:** not shrinking `max_freq` is OK for **maximizing** length — stale `max_freq` only makes the while-condition more conservative incorrectly? Actually the classic proof: `max_freq` is the max frequency seen in any window considered; for max-length answer it's acceptable. For interviews, state this clearly or recompute max in window if unsure.

---

# PART 4: SUBARRAYS WITH PRODUCT LESS THAN K

## 4A: Problem

Count contiguous subarrays where product of elements is **strictly less than** `k`. All `nums[i] ≥ 1`.

```
nums = [10, 5, 2, 6], k = 100
Valid: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6] → 8
```

## 4B: Why Sliding Window Works

All elements ≥ 1 ⇒ expanding **never decreases** product. Monotonicity holds (same reason positive-sum windows work).

If zeros or fractions appear, the pattern breaks — different problem.

## 4C: Framework

```python
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0  # products of positives ≥ 1 never < 1; k<=0 also 0
    left = 0
    prod = 1
    ans = 0
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]
            left += 1
        ans += right - left + 1
    return ans
```

### Trace

```
[10,5,2,6], k=100

r0: prod=10 < 100 → ans += 1 → 1
r1: prod=50 < 100 → ans += 2 → 3
r2: prod=100 >= 100 → divide 10 → prod=10, left=1
    still 10<100; ans += 2 → 5   windows [5,2], [2]
r3: prod=60 < 100 → ans += 3 → 8  windows [5,2,6],[2,6],[6]
✅
```

### Complexity

O(n) time, O(1) space.

### Contrast with Module 1 sum window

| | Sum ≥ target (min length) | Product < k (count) |
|---|---|---|
| Shrink when | sum still ≥ target (minimize) | product ≥ k (restore validity) |
| Answer update | inside shrink / when valid min | `+= window_size` each right |
| Requires | positives for classic SW | positives (here ≥ 1) |

---

# PART 5: CONTAINER WITH MOST WATER (DEEP)

## 5A: Problem

Heights `height[i]` are vertical lines. Choose two lines `i < j` to form a container with the x-axis. Area = `min(height[i], height[j]) * (j - i)`. Maximize area.

```
height = [1,8,6,2,5,4,8,3,7]
Answer: 49  (indices 1 and 8: min(8,7)*7 = 49)
```

## 5B: Brute Force

Try all pairs O(n²). Correct but too slow for interview n ~ 10⁵.

## 5C: Two-Pointer Greedy — The Framework

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])
        best = max(best, h * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
```

## 5D: WHY Moving the Shorter Line Is Safe

This is the part Module 1 never proved.

**Claim:** Suppose `height[left] ≤ height[right]`. Any container using `left` and an index `k` with `left < k < right` has width `< right - left` and height `≤ height[left]`. So area `≤ height[left] * (right - left - ε) < height[left] * (right - left)` **unless** the height could increase — but height is capped by `height[left]` when pairing with `left`. Therefore **no better area can use this `left` with a narrower partner**. Discard `left` (move it forward). Symmetric if right is shorter.

```
Width only shrinks as pointers move inward.
The only way to beat current area is a taller limiting height.
The taller line might still be useful later; the shorter one is the bottleneck → advance the bottleneck.
```

### Trace

```
[1,8,6,2,5,4,8,3,7]
 L                 R
min=1, area=1*8=8 → move L (shorter)
   L               R
min=7, area=7*7=49 → move R (8>7? height[L]=8, height[R]=7 → move R)
   L             R
min=3, area=3*6=18 → move R
... continue ...
best = 49 ✅
```

### Complexity

O(n) time, O(1) space.

### Common Bugs

- Moving **both** pointers each step — loses candidates
- Moving the **taller** line — incorrect; can miss optimal
- Using `max` instead of `min` for water height — wrong physics

---

# PART 6: TRAPPING RAIN WATER (DEEP)

## 6A: Problem

Elevation map `height[i]`. How much water can be trapped after raining?

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]
Answer: 6
```

Water above index `i` = `max(0, min(left_max[i], right_max[i]) - height[i])`  
where `left_max[i]` = tallest bar to the left (or at i), `right_max` similarly.

## 6B: Approach 1 — Prefix / Suffix Arrays (Clearest)

```python
def trap(height):
    n = len(height)
    if n == 0:
        return 0
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water
```

**Complexity:** O(n) time, O(n) space.  
**Interview value:** Shows you understand the formula. Then optimize.

## 6C: Approach 2 — Two Pointers O(1) Space (Expected at Advanced)

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water
```

### Why This Works

At any moment, the side with **smaller height** is limited by that side's max — because the other side has a bar at least as tall as `height[left]` or `height[right]` (the comparison), so water on the smaller side cannot spill over the larger side's current edge.

```
If height[left] < height[right]:
  water at left is determined by left_max
  (right side is "tall enough" to hold it)
```

### Trace (abbreviated)

```
[0,1,0,2,1,0,1,3,2,1,2,1]
L                     R
0<1 → left_max=0, L++
...
Eventually accumulate 6 ✅
```

## 6D: Approach 3 — Monotonic Stack (PREVIEW link)

Index stack of decreasing heights; when a taller bar arrives, pop and compute trapped water between. Full monotonic stack mastery is Module 10; know it exists as a third solution.

## 6E: Edge Cases

| Case | Result |
|---|---|
| Strictly increasing | 0 water |
| Strictly decreasing | 0 water |
| Flat | 0 |
| Single / empty | 0 |
| `[2,0,2]` | 2 |

---

# PART 7: DUTCH NATIONAL FLAG & PARTITION PATTERNS

## 7A: Dutch National Flag (Sort Colors)

Array with only `0, 1, 2`. Sort in-place in one pass — **not** counting sort only (interviewers often want the 3-way partition).

### Invariant

```
[0, low-1]   = 0s
[low, mid-1] = 1s
[mid, high]  = unknown
[high+1, n)  = 2s
```

### Framework

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # do NOT mid += 1 — swapped value unknown
```

### Trace

```
[2,0,2,1,1,0]
 L
 M           H

mid=2 → swap with high → [0,0,2,1,1,2], high=4
mid=0 → swap with low → [0,0,2,1,1,2], low=1, mid=1
mid=0 → swap → [0,0,2,1,1,2], low=2, mid=2
mid=2 → swap with high → [0,0,1,1,2,2], high=3
mid=1 → mid=3
mid=1 → mid=4
mid > high stop
✅ [0,0,1,1,2,2]
```

### Complexity

O(n) time, O(1) space. One pass.

## 7B: General Partition (Quickselect / Quicksort pivot)

```python
def partition(nums, lo, hi, pivot_idx):
    pivot = nums[pivot_idx]
    nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
    store = lo
    for i in range(lo, hi):
        if nums[i] < pivot:
            nums[store], nums[i] = nums[i], nums[store]
            store += 1
    nums[store], nums[hi] = nums[hi], nums[store]
    return store  # final pivot index
```

**Use:** Quickselect for Kth largest (alternative to heap), 3-sum prep after sort, "move all odds before evens," etc.

## 7C: Partition by Predicate (Read/Write Escalation)

Module 1: move zeroes. Advanced: multiple categories or stable vs unstable requirements.

```python
# Unstable partition: all elements satisfying pred to front
def partition_pred(arr, pred):
    write = 0
    for read in range(len(arr)):
        if pred(arr[read]):
            arr[write], arr[read] = arr[read], arr[write]
            write += 1
    return write
```

**Stable partition** needs extra space or more complex algorithms — say so in interviews if order must be preserved.

## 7D: Related Problems

| Problem | Pattern |
|---|---|
| Sort Colors | Dutch flag |
| Move Zeroes | 2-way partition / read-write |
| Remove Element | read-write |
| Partition Array / Wiggle Sort prep | pivot partition |
| Kth Largest via Quickselect | partition + recurse (avg O(n)) |

---

# PART 8: TWO POINTERS — GEOMETRY & TRAPPING FAMILY MAP

```
Need area between two lines?
└── Container With Most Water → converge, move shorter

Need water above each index?
└── Trapping Rain Water → left/right max formula
    ├── O(n) space prefix/suffix (clear)
    └── O(1) two pointers (optimal interview)
    └── monotonic stack (Module 10)

Need 3-way in-place classify?
└── Dutch National Flag

Need pair/triplet sum on sorted array?
└── Module 1 converging + (for 3sum) fix one + two pointer
```

---

# PART 9: EDGE CASES & INTERVIEW WORKFLOW

## Edge Case Checklist (Advanced Window / TP)

| Case | Applies to |
|---|---|
| `k == 0` / `k > len` | distinct-K, product, replacements |
| Empty `s` or `t` | min window |
| `t` longer than `s` | min window → `""` |
| All chars same | distinct, reorganize-adjacent (heaps), water=0 |
| No water possible | monotonic heights |
| Product overflow | use care; Python int OK; other languages use long / shrink early |
| Window never valid | min window return `""`; min size return 0 |

## Interview Workflow

```
1. Contiguous? → window or prefix. Pair from ends? → two pointers.
2. Maximize vs minimize vs count? → pick update location
3. State: Counter? product? left_max? low/mid/high?
4. Prove monotonicity (why shrink is safe)
5. Complexity: O(n) pointers + O(Σ) maps
6. Trace + edges
```

---

# PART 10: CONSOLIDATED CHEAT SHEETS

## Pattern Decision Tree

```
Contiguous subarray/substring problem?
├── Covering requirement (must include all of t) → Min Window (need/have)
├── At most / exactly K distinct → Counter window (+ subtraction for exactly)
├── Product / sum with positives + count or min length → classic variable SW
├── Replace ≤ K to make uniform → window_len - maxfreq ≤ K
└── Not contiguous → NOT sliding window

Two indices forming geometry / water?
├── Max area container → move shorter line
└── Trap rain water → min(Lmax,Rmax) - h[i]

In-place classify 2 or 3 values?
└── 2-way read/write or Dutch 3-way
```

## Complexity Summary

| Pattern | Time | Space |
|---|---|---|
| Min window substring | O(n) | O(Σ) |
| At most K distinct | O(n) | O(Σ) |
| Exactly K (count) | O(n) | O(Σ) |
| Product < K | O(n) | O(1) |
| Container most water | O(n) | O(1) |
| Trap water (2 ptr) | O(n) | O(1) |
| Trap water (arrays) | O(n) | O(n) |
| Dutch flag | O(n) | O(1) |

## Shrink Condition Cheat Card

| Goal | Shrink when |
|---|---|
| Longest valid | invalid |
| Shortest valid | still valid (tighten) |
| Count valid endings | after restoring validity |
| Product < k | `prod >= k` |
| At most K distinct | `distinct > K` |
| Min window | `missing == 0` (while valid) |

## Module 1 → Module 6 Escalation Map

| You knew | Now add |
|---|---|
| Longest no-repeat | At most K / exactly K / replacement |
| Min sum ≥ target | Min window covering multiset `t` |
| Fixed anagram window | Variable covering window |
| Two sum sorted | Container water + trap water |
| Move zeroes | Dutch flag + pivot partition |

---

# PART 11: WORKED PROBLEMS WITH TRACES

---

# Problem 1: Minimum Window Substring

## Pattern Identification

**Minimum covering variable window** — need/have/missing.

## Solution

(See Part 2 framework.)

## Trace

```
s=ADOBECODEBANC t=ABC → BANC
```

Full character-by-character shrink sequence as in Part 2.

## Edge Cases

- `t = ""` → `""` or policy-defined
- `s = "a"`, `t = "aa"` → `""`
- duplicate requirement in t: `t="AABC"` needs two A's

## Complexity

O(n) time, O(Σ) space.

---

# Problem 2: Longest Substring with At Most K Distinct

## Pattern Identification

Variable window + distinct counter.

## Solution

(See Part 3A.)

## Trace

`eceba`, k=2 → 3.

## Complexity

O(n).

---

# Problem 3: Subarray Product Less Than K

## Pattern Identification

Variable window on product; count with `+= width`.

## Solution

(See Part 4.)

## Trace

`[10,5,2,6]`, k=100 → 8.

## Edge Cases

`k <= 1` → 0.

---

# Problem 4: Container With Most Water

## Pattern Identification

Converging two pointers; move shorter.

## Solution

(See Part 5.)

## Trace

`[1,8,6,2,5,4,8,3,7]` → 49.

## Complexity

O(n).

---

# Problem 5: Trapping Rain Water

## Pattern Identification

Two-pointer water with running left_max/right_max.

## Solution

(See Part 6C.)

## Trace

`[0,1,0,2,1,0,1,3,2,1,2,1]` → 6.

## Complexity

O(n) time, O(1) space.

---

# Problem 6: Sort Colors (Dutch Flag)

## Pattern Identification

3-way partition.

## Solution

(See Part 7A.)

## Trace

`[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`.

---

# Problem 7: Longest Repeating Character Replacement

## Pattern Identification

Window where `len - maxfreq <= k`.

## Solution

(See Part 3C.)

## Trace

```
s = "AABABBA", k = 1
Answer 4 ("ABBA" with one replace, or "AABA")
```

---

# Problem 8: Count Substrings with Exactly K Distinct

## Pattern Identification

`at_most(k) - at_most(k-1)`.

## Trace

```
s = "pqpqs", k = 2
Use formula; verify small s by enumeration.
```

---

# PART 12: TEST PROBLEMS (SOLO)

### T1. Minimum Window Substring

Implement from scratch without looking. Trace `s="bba"`, `t="ab"`.

### T2. Max Consecutive Ones III

Flip at most `k` zeros; longest 1s window. (Same family as character replacement.)

### T3. Fruit Into Baskets

At most **2** distinct — special case of at most K.

### T4. Trapping Rain Water

Solve twice: prefix arrays, then two pointers.

### T5. Container With Most Water

Implement + prove in 3 sentences why you move the shorter line.

### T6. Sort Colors

Dutch flag; then write the counting-sort alternative and compare.

### T7. Subarrays with Product < K

Implement; explain why `k <= 1` returns 0.

### T8. Number of Substrings Containing All Three Characters

Count substrings of `abc`-only string that contain at least one a, b, and c. Hint: last-seen indices or window.

---

# PART 13: SOLUTIONS TO TEST PROBLEMS

---

## T1. Min Window — Trace `bba` / `ab`

```
need a1 b1, missing=2
r0 b: b ok, missing=1
r1 b: 
r2 a: missing=0, window "bba"
  shrink b → still valid "ba"
  shrink b → missing b → invalid
best = "ba" ✅
```

---

## T2. Max Consecutive Ones III

```python
def longest_ones(nums, k):
    left = 0
    zeros = 0
    best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

## T3. Fruit Into Baskets

`longest_at_most_k(fruits, 2)` with fruits as the array.

---

## T4. Trap — Both Solutions

Use Part 6B and 6C; verify same answer on `[4,2,0,3,2,5]` → 9.

---

## T5. Proof (Short)

Area is limited by the shorter line. All pairs that keep the current shorter index but move the other inward have smaller width and height still ≤ shorter → cannot improve. So advance the shorter index.

---

## T6. Counting Sort Alternative

```python
def sort_colors_count(nums):
    c0, c1, c2 = nums.count(0), nums.count(1), nums.count(2)
    nums[:] = [0]*c0 + [1]*c1 + [2]*c2
```

Two or three passes vs Dutch one-pass in-place swaps. Both O(n). Dutch shows partition skill.

---

## T7. Product

See Part 4. `k <= 1`: every product ≥ 1 for nums[i] ≥ 1.

---

## T8. Substrings Containing a,b,c

```python
def number_of_substrings(s):
    last = {'a': -1, 'b': -1, 'c': -1}
    ans = 0
    for i, ch in enumerate(s):
        last[ch] = i
        ans += 1 + min(last.values())
        # if any missing, min is -1 → add 0
    return ans
```

**Why:** For each right endpoint `i`, once `a`,`b`,`c` have all been seen, every start index in `0 .. min(last.values())` inclusive forms a valid substring ending at `i`. Count added = `min(last) + 1`. If any char never seen, `min` is `-1` → add `0`.

---

# PART 14: MORE WORKED TRACES (INTERVIEW DEPTH)

---

## W1: Min Window — Full Trace `ADOBECODEBANC` / `ABC`

```
need={A:1,B:1,C:1} missing=3

r0 A: win A1  missing=2
r1 D: 
r2 O:
r3 B: win B1  missing=1
r4 E:
r5 C: win C1  missing=0  VALID [0..5]="ADOBEC" len6
     shrink A: win A0 missing=1  left=1  best=6 start=0
r6 O:
r7 D:
r8 E:
r9 B: still missing A
r10 A: win A1 missing=0 VALID [1..10]="DOBECODEBA" len10
     shrink while valid:
       D,O,B,E,C,O,D,E → when remove C missing++ … 
     (implementation shrinks until invalid; best may update if shorter found)
r11 N:
r12 C: missing=0 VALID … shrink to left at B of "BANC"
     best_len=4 start→ index of B → "BANC" ✅
```

**Interview line:** "I expand until `missing==0`, then shrink from the left while still covered, recording every valid window's length."

---

## W2: Product < K — Why `+= right-left+1`

When `[left, right]` is the longest window ending at `right` with product < k, every subarray that **ends at `right`** and **starts at `i` for `i ∈ [left, right]`** also has product < k (subarray of positives has smaller or equal product).

There are exactly `right - left + 1` such start positions → add that many.

---

## W3: Trap Water Two-Pointer — Full Micro-Trace `[4,2,0,3,2,5]`

```
L=0 R=5  hL=4 hR=5  4<5 → left_max=4, L→1
L=1 R=5  hL=2 <5 → 2<left_max → water+=4-2=2, L→2
L=2 R=5  hL=0 → water+=4-0=4 (total6), L→3
L=3 R=5  hL=3 → water+=4-3=1 (total7), L→4
L=4 R=5  hL=2 → water+=4-2=2 (total9), L→5
L==R stop → 9 ✅
```

---

## W4: Dutch Flag — Why Not mid++ on 2

```
nums = [1, 2, 0], low=0, mid=0, high=2

mid sees 1 → mid=1
mid sees 2 → swap with high → [1, 0, 2], high=1
  if mid++ here → mid=2, mid>high stop
  array = [1,0,2] ❌ WRONG

Correct: after swap, mid stays 1, sees 0 → swap with low → [0,1,2] ✅
```

---

## W5: At Most K vs No-Repeat (Module 1 bridge)

| | No-repeat (M1) | At most K distinct (M6) |
|---|---|---|
| Constraint | each char freq ≤ 1 | number of keys ≤ K |
| State | set or last-index map | Counter + distinct |
| Shrink | while `s[right]` duplicate | while `distinct > K` |

No-repeat is **not** `at_most(n)`; it is a frequency cap of 1 per character.

---

# PART 15: ADDITIONAL SOLO PROBLEMS + ANSWERS

---

### S1. Find All Anagrams

`s = "cbaebabacd"`, `p = "abc"` → `[0, 6]`

```python
from collections import Counter

def find_anagrams(s, p):
    need, n = Counter(p), len(p)
    win = Counter()
    res, left = [], 0
    for right, ch in enumerate(s):
        win[ch] += 1
        if right - left + 1 > n:
            win[s[left]] -= 1
            if win[s[left]] == 0:
                del win[s[left]]
            left += 1
        if win == need:
            res.append(left)
    return res
```

Fixed window — contrast with variable min-window.

---

### S2. Permutation in String

Same as anagrams; return `bool(res)` or early `True` when counts match.

---

### S3. Longest Substring with Exactly K Distinct (length, not count)

```python
def longest_exactly_k(s, k):
    # longest with at most k, but force distinct == k when updating
    from collections import defaultdict
    def longest_at_most(kk):
        count = defaultdict(int)
        left = distinct = best = 0
        best_exact = 0
        for right, ch in enumerate(s):
            if count[ch] == 0: distinct += 1
            count[ch] += 1
            while distinct > kk:
                count[s[left]] -= 1
                if count[s[left]] == 0: distinct -= 1
                left += 1
            best = max(best, right - left + 1)
            if distinct == k:  # only when calling with kk==k
                best_exact = max(best_exact, right - left + 1)
        return best, best_exact
    return longest_at_most(k)[1]
```

Or: compute longest at_most(k) windows and only record when distinct==k after shrink.

---

### S4. 3Sum Closest (two pointers refresh + escalate)

After sorting, fix `i`, two-pointer on remainder toward target — Module 1 skill used inside advanced sets.

---

### S5. Trapping Rain Water II (PREVIEW)

2D height map — priority queue / BFS from borders. **Heap + graph thinking** — label PREVIEW; not required for Module 6 array credit.

---

# PART 16: COMMON INTERVIEW MISTAKES

| Mistake | Fix |
|---|---|
| Using sliding window with negatives for product/sum | Monotonicity dies — different algorithm |
| Min window: update best outside shrink only once | Update every valid tightened window |
| Container: move both pointers | Move one — the shorter |
| Trap: confuse with container | Different formula and move rule |
| Dutch: mid++ after swapping 2 | Leave mid to retest |
| Exactly K: only write at_most(k) | Subtract at_most(k-1) for counts |
| Comparing dicts each step in anagram without care | OK for small Σ; or maintain `matches` int |

---

# PART 17: MODULE 6 ARRAYS ADVANCED — SELF-CHECK

- [ ] Explain maximize vs minimize window update locations
- [ ] Code min window need/have from scratch
- [ ] at_most K and exactly K via subtraction
- [ ] Product < K counting trick
- [ ] Prove container water pointer move
- [ ] Trap water O(1) space
- [ ] Dutch flag invariants without notes

**Companion file:** `Heaps/Heaps & Priority Queues.md`  
**Retention:** `Retention Questions/Module 6 Retention.md`

---

*End of Arrays — Advanced Patterns lesson.*
