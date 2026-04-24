

# SECTION A: RAPID FIRE — COMPLEXITY ANALYSIS

---

## A1.

```python
def func(arr):
    n = len(arr)
    result = 0
    for i in range(0, n, 3):
        for j in range(0, n, 3):
            result += arr[i] * arr[j]
    return result
```

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- Outer loop: `range(0, n, 3)` → runs ⌈n/3⌉ times
- Inner loop: `range(0, n, 3)` → runs ⌈n/3⌉ times per outer iteration
- Inside: `arr[i]` O(1), `arr[j]` O(1), multiplication O(1), addition O(1) → O(1)
- Nested with same input → multiply: (n/3) × (n/3) = n²/9

**STEP 4:** O(n²/9) = **O(n²)**

The step size of 3 is a constant. It reduces the iteration count by a constant factor (9x fewer iterations than step-1 nesting), but constant factors are dropped.

**STEP 5:** `result`, `i`, `j`, `n` → all scalars → **O(1)**

> **Time: O(n²), Space: O(1)**

---

## A2.

```python
def func(arr):
    n = len(arr)
    i = 1
    while i < n:
        j = 0
        while j < i:
            j += 1
        i *= 2
    return i
```

**The trap:** This looks like it might be O(n log n) or O(n²). Need to carefully count.

**Outer loop:** `i` doubles each iteration: 1, 2, 4, 8, ..., until i ≥ n. That's **log₂(n)** outer iterations.

**Inner loop:** For each outer iteration, the inner loop runs `i` times (j goes from 0 to i-1). The inner loop does j += 1, which is O(1) per step, running exactly `i` times.

**Total inner work across all outer iterations:**

$$1 + 2 + 4 + 8 + \ldots + 2^{\lfloor \log_2 n \rfloor}$$

This is a geometric series:

$$= 2^{(\lfloor \log_2 n \rfloor + 1)} - 1 \approx 2n - 1$$

**Total time: O(n)**

This is NOT O(n log n). Even though there's a doubling outer loop, the inner loop's total work is a geometric series dominated by its largest term. The last iteration alone does ~n/2 work, the second-to-last does ~n/4, etc. The sum converges to ~2n.

**STEP 5:** `i`, `j`, `n` → scalars → **O(1)**

> **Time: O(n), Space: O(1)**

---

## A3.

```python
def func(n):
    if n <= 1:
        return 1
    return func(n - 1) + func(n - 1)
```

**Recurrence:** T(n) = 2T(n-1) + O(1)

**Recursion tree:**
```
Level 0:    1 call                  → O(1)
Level 1:    2 calls                 → O(2)
Level 2:    4 calls                 → O(4)
...
Level k:    2^k calls               → O(2^k)
...
Level n-1:  2^(n-1) calls           → O(2^(n-1))
```

Depth = n-1 (subtracting 1 each time until reaching 1).

Total: 1 + 2 + 4 + ... + 2^(n-1) = 2ⁿ - 1

**Time: O(2ⁿ)**

**Space:** Maximum call stack depth = n (one path from root to leaf) → **O(n)**

**How this differs from Fibonacci:**

Fibonacci: `T(n) = T(n-1) + T(n-2) + O(1)`
This function: `T(n) = T(n-1) + T(n-1) + O(1) = 2T(n-1) + O(1)`

Both are O(2ⁿ), but for different reasons:
- Fibonacci has **unequal branches** (n-1 and n-2). Its exact base is φⁿ ≈ 1.618ⁿ, which is technically O(2ⁿ) but a smaller constant base.
- This function has **equal branches** — exactly 2 calls of n-1. Its exact count is precisely 2ⁿ - 1. It's a perfect binary tree, whereas Fibonacci's tree is lopsided.
- Fibonacci also has **overlapping subproblems** (fib(3) is computed from multiple paths), making it amenable to memoization/DP. This function has overlapping subproblems too, but since both calls are identical, you could simply compute `half = func(n-1); return half + half` to get **O(n)** — the same optimization trap as the mystery function from a previous problem set.

> **Time: O(2ⁿ), Space: O(n)**
> **Recurrence: T(n) = 2T(n-1) + O(1)**

---

## A4.

```python
def func(arr):
    n = len(arr)
    arr.sort()
    seen = set()
    for i in range(n):
        if arr[i] not in seen:
            seen.add(arr[i])
    return len(seen)
```

**Block by block:**
- `arr.sort()` → **O(n log n)**
- Loop: n iterations, set operations O(1) each → **O(n)**

**Total time: O(n log n) + O(n) = O(n log n)**

**The dominant cost is the sort.** The loop is O(n), strictly less than the sort.

**What's redundant:** The **sort is entirely unnecessary.** The loop with the set already finds all unique elements — a set inherently handles deduplication. The sort adds O(n log n) cost for zero benefit. Without the sort, the function would be O(n).

In fact, the entire function is equivalent to `return len(set(arr))`, which is O(n).

**Space:** `seen` → at most n elements → **O(n)** (plus O(n) for sort's internal storage).

> **Time: O(n log n), Space: O(n)**
> **Dominant cost: sort. The sort is redundant — removing it makes this O(n).**

---

## A5.

```python
def func(s):
    result = ""
    for i in range(len(s)):
        result = s[i] + result
    return result
```

**What this does:** Builds the reverse of `s` by prepending each character.

**The two hidden costs:**

**Hidden cost 1: `s[i] + result` — string concatenation**
Strings are immutable in Python. `s[i] + result` creates an **entirely new string** of length `1 + len(result)`. This copies all characters of `result` plus the new character into a new string object.

At iteration i, `result` has length i, so the concatenation costs O(i).

**Hidden cost 2: `result = s[i] + result` — the left-side prepend**
This is the same concatenation, but I want to emphasize: even though we're "prepending," there's no O(1) prepend for strings. The entire string is rebuilt from scratch. There is no difference in cost between `result = result + s[i]` and `result = s[i] + result` — both are O(len(result)).

Total work across all iterations:

$$1 + 2 + 3 + \ldots + n = \frac{n(n+1)}{2} = O(n^2)$$

**Space:**
- `result` grows to length n → O(n) for the final string
- But at each iteration, a **new** string is created and the old one is garbage collected. Peak memory: old result (length i-1) + new result (length i) ≈ O(n) simultaneously.

> **Time: O(n²), Space: O(n)**
> **Hidden cost 1: String concatenation creates a new string each iteration — O(len(result)) per concat**
> **Hidden cost 2: The prepend `s[i] + result` is the same cost as append — no O(1) prepend for immutable strings**

**Fix:** `return s[::-1]` or `return "".join(reversed(s))` — both O(n).

---

# SECTION B: CONCEPTUAL QUESTIONS

---

## B1.

**`arr.pop()` — Remove from end — O(1):**

A Python list is backed by a **dynamic array** — a contiguous block of memory. The list internally tracks its length. Removing the last element simply decrements the length counter by 1. The element is logically gone. No other elements need to move. The memory slot still exists but is now considered "past the end." Essentially just updating an integer — **O(1).**

**`arr.pop(0)` — Remove from front — O(n):**

Removing the first element leaves a hole at index 0. But a dynamic array requires elements to be contiguous starting from index 0 (that's how `arr[i]` can compute the memory address as `base + i × element_size` in O(1)). So every element from index 1 through n-1 must **shift left by one position** to fill the gap:

```
Before: [A, B, C, D, E]    remove A
         ↑  need to shift ←
After:  [B, C, D, E, _]    n-1 = 4 shifts
```

Every remaining element is copied one position to the left. That's n-1 copy operations — **O(n).**

The same logic applies to `arr.insert(0, x)` — every element shifts right to make room. And to `arr.pop(k)` for any k — O(n-k) shifts.

---

## B2.

**Recurrence: T(n) = T(n/2) + T(n/2) + O(n) = 2T(n/2) + O(n)**

The teammate says it's O(n log n), same as merge sort. **The teammate is correct.**

This IS merge sort's recurrence. Let me verify with the recursion tree:

```
Level 0:    1 problem of size n          → O(n) work
Level 1:    2 problems of size n/2       → O(n) work total
Level 2:    4 problems of size n/4       → O(n) work total
...
Level k:    2^k problems of size n/2^k   → O(n) work total
...
Level log n: n problems of size 1        → O(n) work total
```

Each level does O(n) total work. There are log₂(n) levels. Total: **O(n log n).**

Master Theorem confirmation: a=2, b=2, f(n)=O(n). log_b(a) = log₂(2) = 1. f(n) = O(n¹). Case 2: **T(n) = O(n log n).** ✅

**Where someone might get confused:** If the recurrence were `T(n) = T(n/2) + T(n/2) + O(1)` (constant work instead of O(n) per level), that would be the mystery function from Problem 9 — the geometric series gives O(n). But with O(n) work per level, each level contributes equally, giving n log n.

---

## B3.

**Why the left pointer never moves backward:**

The left pointer represents the start of the current valid window (no repeating characters). It advances in only two situations:

1. We encounter a character that's already in the window → left jumps past the previous occurrence
2. This jump is always **forward** (to a higher index than left's current position) because the previous occurrence is somewhere inside the current window, which starts at `left`

**Left can never move backward because moving backward would re-include a character we already excluded.** If we excluded a character by moving left past it, that character was causing a duplicate. Re-including it would violate the uniqueness constraint. There's never a reason to revisit positions we've already processed — any window starting at an earlier left position has already been considered.

**Why this guarantees O(n):**

The right pointer moves forward exactly n times (one per iteration of the for loop). The left pointer also only moves forward, and it can move at most n times total (it can't go past index n-1). So the total number of pointer movements is at most n + n = 2n.

Each movement does O(1) work (hash map lookup/update). Total: O(2n) = **O(n).**

This is the **amortized two-pointer principle**: when both pointers only move forward through the same array and each does at most n total moves, the algorithm is O(n) regardless of how the inner pointer's movement distributes across outer iterations.

---

## B4.

**The mathematical property of double reversal:**

Reversing a sequence is an **involution** — applying it twice returns to the original: `reverse(reverse(S)) = S`.

But the three-reverse trick uses something deeper: **reversal is an anti-homomorphism with respect to concatenation.** Meaning:

$$\text{reverse}(A \| B) = \text{reverse}(B) \| \text{reverse}(A)$$

Reversing a concatenation reverses the order of the parts AND reverses each part internally.

Now, our array is `[A | B]` where A = first n-k elements, B = last k elements. We want `[B | A]`.

**Step 1:** Reverse the whole thing:

$$\text{reverse}(A \| B) = \text{reverse}(B) \| \text{reverse}(A) = B^R \| A^R$$

We now have the blocks in the right order (B before A) but each block is internally reversed.

**Step 2:** Reverse the first block:

$$\text{reverse}(B^R) \| A^R = B \| A^R$$

**Step 3:** Reverse the second block:

$$B \| \text{reverse}(A^R) = B \| A$$

This is exactly what we wanted. The mathematical property that makes it work is that **full reversal swaps block order while internally reversing each block, and sub-reversals fix the internal order without changing block positions.**

---

## B5.

**Solution A: O(n log n) time, O(1) space vs Solution B: O(n) time, O(n) space**

**Specific scenarios where A is better:**

**Scenario 1: Memory-constrained embedded system.**
You're writing firmware for a device with 256KB of RAM processing a sensor data stream of 1 million readings. O(n) space means allocating ~4MB for an auxiliary array — impossible on this hardware. O(1) space means processing in-place with whatever memory the input already occupies. The extra log factor in time is acceptable because the device has plenty of time but no spare memory.

**Scenario 2: Input is so large it barely fits in memory.**
You're processing a 30GB file on a machine with 32GB RAM. The input is memory-mapped and takes up nearly all available RAM. Allocating O(n) additional space would cause swapping to disk, which is orders of magnitude slower than RAM. The O(n log n) in-place solution stays in RAM and runs faster in practice despite the worse theoretical time complexity. The O(n) solution's O(n) space causes disk thrashing that dominates any time savings.

**Scenario 3: Cache performance matters more than operation count.**
The O(1) space solution works in-place, keeping data in CPU cache. The O(n) space solution jumps between two large arrays that don't both fit in cache, causing cache misses. For moderate n (say 10⁵ to 10⁶), the cache-friendly O(n log n) solution with small constants can actually be faster wall-clock than the cache-unfriendly O(n) solution. This is common in sorting: in-place heapsort vs. merge sort.

---

# SECTION C: PROBLEM SOLVING

---

## C1: The Trap — Is This Sliding Window?

### Before Coding: Can Sliding Window Work?

**For the first example `[2, 3, 1, 2, 4, 3], target = 7` — all positive integers:**
Sliding window WORKS when all elements are positive. Why? Because:
- Expanding the window (moving right) **always increases** the sum
- Contracting the window (moving left) **always decreases** the sum
- This monotonic relationship means we know exactly when to expand vs contract

**For the second example `[1, -1, 5, -2, 3], target = 3` — contains negatives:**
Sliding window **DOES NOT WORK** with negative numbers. Why? Because:
- Adding a negative number **decreases** the sum — expanding can make things worse
- Removing a negative number **increases** the sum — contracting can make things better
- The sum is no longer monotonic with window size
- We lose the invariant that tells us which pointer to move

**Example of failure:** `arr = [1, -1, 5, -2, 3], target = 3`
If our window is `[1, -1, 5]` with sum=5 > 3, sliding window would contract from left. But the optimal answer might be `[3]` at the end, or `[5, -2]` in the middle. Contracting doesn't reliably move toward the answer.

### Approach for Mixed (Positive + Negative)

For positive-only: standard sliding window, O(n).
For mixed: we need **prefix sum + hash map** to handle the general case.

The problem asks for **shortest subarray with exact sum = target.** With negatives, we need:
- Track prefix sums
- For each position j, we need the **closest** i before j where `prefix[j] - prefix[i] = target`, i.e., `prefix[i] = prefix[j] - target`
- Store the **most recent** index for each prefix sum value (to minimize subarray length)

### Solution (General Case — Handles Negatives)

```python
def shortest_subarray_sum(arr, target):
    prefix_map = {0: -1}  # prefix_sum → most recent index
    current_sum = 0
    min_len = float('inf')

    for i in range(len(arr)):
        current_sum += arr[i]
        complement = current_sum - target

        if complement in prefix_map:
            length = i - prefix_map[complement]
            min_len = min(min_len, length)

        # Store/UPDATE to most recent index (for shortest subarray)
        prefix_map[current_sum] = i

    return min_len if min_len != float('inf') else -1
```

### Critical Difference from "Count Subarrays"

In the "count subarrays equal to k" problem, we stored the **first** occurrence of each prefix sum (actually, we stored frequency counts). Here, we want the **shortest** subarray, so we store the **most recent** index and **overwrite** on each occurrence. This gives the smallest `i - prefix_map[complement]` for any given `i`.

### Trace Through Example 1

```
arr = [2, 3, 1, 2, 4, 3], target = 7
prefix_map = {0: -1}, current_sum = 0, min_len = ∞

i=0, num=2: sum=2, comp=2-7=-5
            -5 not in map → skip
            prefix_map = {0:-1, 2:0}

i=1, num=3: sum=5, comp=5-7=-2
            -2 not in map → skip
            prefix_map = {0:-1, 2:0, 5:1}

i=2, num=1: sum=6, comp=6-7=-1
            -1 not in map → skip
            prefix_map = {0:-1, 2:0, 5:1, 6:2}

i=3, num=2: sum=8, comp=8-7=1
            1 not in map → skip
            prefix_map = {0:-1, 2:0, 5:1, 6:2, 8:3}

i=4, num=4: sum=12, comp=12-7=5
            5 in map at index 1 → length = 4-1 = 3
            min_len = 3
            prefix_map = {..., 12:4}

i=5, num=3: sum=15, comp=15-7=8
            8 in map at index 3 → length = 5-3 = 2
            min_len = 2
            prefix_map = {..., 15:5}

return 2 ✅ (subarray [4, 3])
```

### Trace Through Example 2

```
arr = [1, -1, 5, -2, 3], target = 3
prefix_map = {0: -1}, sum = 0, min_len = ∞

i=0, num=1: sum=1, comp=1-3=-2. Not found. map={0:-1, 1:0}

i=1, num=-1: sum=0, comp=0-3=-3. Not found.
             map={0:1, 1:0}  ← OVERWRITE: 0 now maps to index 1

i=2, num=5: sum=5, comp=5-3=2. Not found. map={..., 5:2}

i=3, num=-2: sum=3, comp=3-3=0. 
             0 in map at index 1 → length = 3-1 = 2. min_len=2
             map={..., 3:3}

i=4, num=3: sum=6, comp=6-3=3.
            3 in map at index 3 → length = 4-3 = 1. min_len=1
            map={..., 6:4}

return 1 ✅ (subarray [3])
```

### Edge Cases

**Edge case 1: No valid subarray**
```
arr = [1, 2], target = 10
Prefix sums: 1, 3. Complements: -9, -7. Never found.
return -1 ✅
```

**Edge case 2: Single element equals target**
```
arr = [7], target = 7
sum=7, comp=0, 0 in {0:-1} → length = 0-(-1) = 1
return 1 ✅
```

### Complexity Analysis

**Time:** Single pass, n iterations, O(1) per iteration → **O(n)**
**Space:** `prefix_map` → at most n+1 entries → **O(n)**

> **Time: O(n), Space: O(n)**

---

## C2: QuickSelect — K-th Smallest Element

### Pattern Identification

**Pattern: Divide and Conquer (Partition-Based Selection)**

Like QuickSort, we pick a pivot and partition the array. But unlike QuickSort, we only recurse into **one** side — the side containing the k-th element. This reduces average work from O(n log n) to O(n).

### Solution

```python
def quick_select(arr, k):
    # k is 1-indexed: k=1 means smallest
    return _select(arr, 0, len(arr) - 1, k - 1)  # convert to 0-indexed

def _select(arr, left, right, k_index):
    if left == right:
        return arr[left]

    pivot_pos = partition(arr, left, right)

    if k_index == pivot_pos:
        return arr[pivot_pos]
    elif k_index < pivot_pos:
        return _select(arr, left, pivot_pos - 1, k_index)
    else:
        return _select(arr, pivot_pos + 1, right, k_index)

def partition(arr, left, right):
    pivot = arr[right]  # choose last element as pivot
    store = left

    for i in range(left, right):
        if arr[i] <= pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1

    arr[store], arr[right] = arr[right], arr[store]
    return store
```

### How Partition Works

The partition function rearranges elements around a pivot:
- All elements ≤ pivot end up to the left of the pivot's final position
- All elements > pivot end up to the right
- The pivot itself is placed at its correct sorted position
- Returns that position

`store` tracks where the next "small" element should go. Every element ≤ pivot gets swapped into the `store` position.

### Trace Through Main Example

```
arr = [3, 2, 1, 5, 6, 4], k = 2 → k_index = 1

_select(arr, 0, 5, 1):
  partition(arr, 0, 5):
    pivot = arr[5] = 4, store = 0
    i=0: arr[0]=3 ≤ 4 → swap(0,0), store=1. arr=[3,2,1,5,6,4]
    i=1: arr[1]=2 ≤ 4 → swap(1,1), store=2. arr=[3,2,1,5,6,4]
    i=2: arr[2]=1 ≤ 4 → swap(2,2), store=3. arr=[3,2,1,5,6,4]
    i=3: arr[3]=5 > 4 → skip
    i=4: arr[4]=6 > 4 → skip
    swap(store=3, right=5): arr=[3,2,1,4,6,5]
    return 3

  pivot_pos = 3. k_index = 1.
  1 < 3 → recurse LEFT: _select(arr, 0, 2, 1)

_select(arr, 0, 2, 1):
  partition(arr, 0, 2):
    pivot = arr[2] = 1, store = 0
    i=0: arr[0]=3 > 1 → skip
    i=1: arr[1]=2 > 1 → skip
    swap(store=0, right=2): arr=[1,2,3,4,6,5]
    return 0

  pivot_pos = 0. k_index = 1.
  1 > 0 → recurse RIGHT: _select(arr, 1, 2, 1)

_select(arr, 1, 2, 1):
  partition(arr, 1, 2):
    pivot = arr[2] = 3, store = 1
    i=1: arr[1]=2 ≤ 3 → swap(1,1), store=2
    swap(store=2, right=2): no change
    return 2

  pivot_pos = 2. k_index = 1.
  1 < 2 → recurse LEFT: _select(arr, 1, 1, 1)

_select(arr, 1, 1, 1):
  left == right → return arr[1] = 2

return 2 ✅
```

### Average Case Analysis

**Recurrence:** On average, the pivot lands near the middle, splitting the array roughly in half. We only recurse on ONE side:

$$T(n) = T(n/2) + O(n)$$

The O(n) comes from the partition step (scanning all elements in the current range).

**Solving:**
```
T(n) = T(n/2) + n
     = T(n/4) + n/2 + n
     = T(n/8) + n/4 + n/2 + n
     ...
     = n + n/2 + n/4 + n/8 + ... + 1
     = n(1 + 1/2 + 1/4 + ...) 
     ≤ 2n
```

This is a geometric series converging to 2n. **Average case: O(n).**

Master Theorem: a=1, b=2, f(n)=O(n). log_b(a) = 0. f(n) = O(n¹) = O(n^(0+1)). Case 3: T(n) = O(f(n)) = **O(n).** ✅

### Worst Case Analysis

**Recurrence:** If the pivot is always the smallest or largest element (worst partition), we eliminate only 1 element each time:

$$T(n) = T(n-1) + O(n)$$

**Solving:**
```
T(n) = T(n-1) + n
     = T(n-2) + (n-1) + n
     = n + (n-1) + (n-2) + ... + 1
     = n(n+1)/2
     = O(n²)
```

**When the worst case occurs:**
- Array is already sorted (ascending or descending) AND we always pick the last element as pivot
- The pivot is always the extreme value, so one partition has 0 elements and the other has n-1
- Every partition does O(n) work but only eliminates 1 element

**Mitigation:** Use randomized pivot selection (`random.randint(left, right)`) or median-of-three. Randomization makes worst case astronomically unlikely — expected time is always O(n).

### Edge Cases

**Edge case 1: k = 1 (minimum)**
```
arr = [5, 3, 1], k = 1
After enough partitions, find the smallest element = 1 ✅
```

**Edge case 2: k = n (maximum)**
```
arr = [5, 3, 1], k = 3
After enough partitions, find the largest element = 5 ✅
```

### Complexity

> **Average: O(n) time, O(log n) space** (stack depth with balanced partitions)
> **Worst: O(n²) time, O(n) space** (stack depth with degenerate partitions)

---

## C3: Three Sum

### Pattern Identification

**Pattern: Sort + Two Pointers + Duplicate Skipping**

Sort the array, fix one element, use two pointers on the remainder to find pairs summing to the negation of the fixed element. Skip duplicates at every level.

### Solution

```python
def three_sum(arr):
    arr.sort()
    n = len(arr)
    result = []

    for i in range(n - 2):
        # Skip duplicate fixed elements
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Early termination
        if arr[i] > 0:
            break

        target = -arr[i]
        left = i + 1
        right = n - 1

        while left < right:
            s = arr[left] + arr[right]
            if s == target:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1

    return result
```

### How Duplicates Are Handled — Three Levels

**Level 1: Fixed element (i).**
`if i > 0 and arr[i] == arr[i-1]: continue` — If we already processed -1 as the fixed element, processing another -1 would produce the exact same two-pointer search over the same remaining range, yielding duplicate triplets. Skip.

**Level 2: Left pointer after finding a match.**
`while arr[left] == arr[left+1]: left += 1` — After finding triplet [-1, -1, 2], if the next left value is also -1, pairing it with the same right pointer gives the same triplet. Skip all consecutive duplicates.

**Level 3: Right pointer after finding a match.**
Same logic for the right side. If arr[right] == arr[right-1], skip to avoid duplicate triplets.

### Trace Through Main Example

```
arr = [-1, 0, 1, 2, -1, -4]
sorted: [-4, -1, -1, 0, 1, 2]

i=0, arr[0]=-4, target=4:
  left=1, right=5: -1+2=1 < 4 → left++
  left=2, right=5: -1+2=1 < 4 → left++
  left=3, right=5: 0+2=2 < 4 → left++
  left=4, right=5: 1+2=3 < 4 → left++
  left=5, done.

i=1, arr[1]=-1, target=1:
  left=2, right=5: -1+2=1 == 1 → FOUND [-1,-1,2]
    No dup skips needed (arr[2]=-1 ≠ arr[3]=0, arr[5]=2 ≠ arr[4]=1)
    left=3, right=4
  left=3, right=4: 0+1=1 == 1 → FOUND [-1,0,1]
    left=4, right=3, done.

i=2, arr[2]=-1: arr[2]==arr[1] → SKIP (duplicate)

i=3, arr[3]=0: 0 > 0? No. target=0.
  left=4, right=5: 1+2=3 > 0 → right--
  left=4, right=4, done.

return [[-1,-1,2], [-1,0,1]] ✅
```

### Edge Cases

**Edge case 1: All zeros**
```
arr = [0,0,0,0]
sorted: [0,0,0,0]
i=0: target=0, left=1,right=3: 0+0=0 → FOUND [0,0,0]
  dup skip left: arr[1]==arr[2] yes, left=2; arr[2]==arr[3] yes, left=3.
  left=4, right=2. Done.
i=1: arr[1]==arr[0] → SKIP
return [[0,0,0]] ✅
```

**Edge case 2: No valid triplet**
```
arr = [1, 2, 3]
sorted: [1,2,3]
i=0: arr[0]=1 > 0 → BREAK
return [] ✅
```

### Complexity

**Time:**
- Sort: O(n log n)
- Outer loop: O(n) iterations
- Each iteration: two pointers do at most O(n) work
- Total: O(n²)
- O(n log n) + O(n²) = **O(n²)**

**Space:**
- Sorting: O(n) or O(1) depending on implementation
- `result`: at most O(n²) triplets worst case
- Auxiliary: **O(1)** (excluding output and sort space)

> **Time: O(n²), Space: O(n²)** for output, **O(1)** auxiliary

---

## C4: Group Anagrams

### Pattern Identification

**Pattern: Hash Map with Canonical Key**

Group strings by a key that's identical for all anagrams. Two options:
- **Sorted string** as key: sort each string, anagrams produce the same sorted result
- **Frequency tuple** as key: count character frequencies, anagrams have identical frequency profiles

### Grouping Key Choice

I'll use **sorted tuple** for clarity. The key for "eat" is `('a', 'e', 't')`. "tea" → same key. "ate" → same key. Different anagram groups produce different keys.

**Why this key is optimal:** It's the simplest canonical form — O(k log k) per string where k is string length. The frequency tuple alternative is O(k + 26) = O(k), which is technically better but involves more code. Both are valid in interviews.

### Solution

```python
def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = tuple(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
    return list(groups.values())
```

### Trace Through Main Example

```
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

"eat" → ('a','e','t') → groups = {('a','e','t'): ["eat"]}
"tea" → ('a','e','t') → groups = {('a','e','t'): ["eat","tea"]}
"tan" → ('a','n','t') → groups = {..., ('a','n','t'): ["tan"]}
"ate" → ('a','e','t') → groups = {('a','e','t'): ["eat","tea","ate"], ...}
"nat" → ('a','n','t') → groups = {..., ('a','n','t'): ["tan","nat"]}
"bat" → ('a','b','t') → groups = {..., ('a','b','t'): ["bat"]}

return [["eat","tea","ate"], ["tan","nat"], ["bat"]] ✅
```

### Edge Cases

**Edge case 1: Empty strings**
```
strs = ["", ""]
"" → sorted → () → both map to same key
return [["", ""]] ✅
```

**Edge case 2: No anagrams**
```
strs = ["abc", "def"]
Different sorted keys → separate groups
return [["abc"], ["def"]] ✅
```

### Complexity

**STEP 1:** `strs` → n = len(strs), k = maximum string length

**STEP 3:**
- Loop: n iterations
- Inside: `sorted(s)` → O(k log k). `tuple()` → O(k). Dict ops with tuple key: hashing O(k), lookup O(k).
- Per iteration: O(k log k)

**Total: O(n × k log k)**

**Space:**
- `groups` → stores all n strings → O(n × k) total characters

> **Time: O(n × k log k), Space: O(n × k)**

---

## C5: Longest Substring With At Most K Distinct Characters

### Pattern Identification

**Pattern: Variable Sliding Window + Frequency Map**

Expand right freely. Contract left when distinct characters exceed k. Track character frequencies to know when to contract and what the distinct count is.

### Solution (Length Only)

```python
def longest_k_distinct(s, k):
    if k == 0 or not s:
        return 0

    char_count = {}
    left = 0
    max_len = 0

    for right in range(len(s)):
        char = s[right]
        char_count[char] = char_count.get(char, 0) + 1

        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```

### Modified Solution (Returns Actual Substring)

```python
def longest_k_distinct_with_substring(s, k):
    if k == 0 or not s:
        return 0, ""

    char_count = {}
    left = 0
    max_len = 0
    best_start = 0

    for right in range(len(s)):
        char = s[right]
        char_count[char] = char_count.get(char, 0) + 1

        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            left += 1

        if right - left + 1 > max_len:
            max_len = right - left + 1
            best_start = left

    return max_len, s[best_start:best_start + max_len]
```

The only change: track `best_start` whenever we find a new maximum length. At the end, extract the substring with a single slice.

### Trace Through Example 1

```
s = "eceba", k = 2

right=0 'e': count={'e':1}, len=1 ≤ 2. max=1. Window: "e"

right=1 'c': count={'e':1,'c':1}, len=2 ≤ 2. max=2. Window: "ec"

right=2 'e': count={'e':2,'c':1}, len=2 ≤ 2. max=3. Window: "ece"
             best_start=0

right=3 'b': count={'e':2,'c':1,'b':1}, len=3 > 2!
  Contract: remove s[0]='e', count['e']=1. len=3 > 2.
  Contract: remove s[1]='c', count['c']=0 → del. left=2.
  count={'e':1,'b':1}, len=2 ≤ 2.
  Window: "eb", length=2. 2 < 3, no update.

right=4 'a': count={'e':1,'b':1,'a':1}, len=3 > 2!
  Contract: remove s[2]='e', count['e']=0 → del. left=3.
  count={'b':1,'a':1}, len=2 ≤ 2.
  Window: "ba", length=2. 2 < 3, no update.

return 3, "ece" ✅
```

### Edge Cases

**Edge case 1: k = 0**
```
Guard returns 0, "" ✅
```

**Edge case 2: k ≥ unique characters**
```
s = "abc", k = 5
Window grows to full string, never contracts.
return 3, "abc" ✅
```

### Complexity

**Time:** Right pointer: n moves. Left pointer: at most n total moves. O(1) per move. → **O(n)**

**Space:** `char_count` → at most k+1 entries → **O(k)**. Final slice: O(max_len).

> **Time: O(n), Space: O(k)**

---

## C6: Complexity Debugging

### The Original Code

```python
def find_duplicates(arr):
    result = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in result:
                result.append(arr[i])
    return result
```

### 1. Actual Time Complexity

**Three cost layers:**

**Layer 1: The nested loops.**
Outer: n iterations. Inner: for each i, runs n-i-1 iterations.
Total iterations: n-1 + n-2 + ... + 1 + 0 = n(n-1)/2 = **O(n²)**

**Layer 2: `arr[i] == arr[j]` — comparison.**
O(1) per iteration (assuming integer/simple type comparison). No hidden cost here.

**Layer 3: `arr[i] not in result` — ⚠️ THIS IS THE KILLER.**
`result` is a **list.** `x not in list` scans the entire list — **O(len(result)).**

In the worst case, `result` grows to hold many elements. How many? At most O(n) unique duplicates. For each of the O(n²) inner iterations, we potentially scan a list of up to O(n) elements.

**Worst case total: O(n²) iterations × O(n) membership check = O(n³)**

Even in a generous analysis where the `not in result` check short-circuits due to `and` evaluation: the `arr[i] == arr[j]` check happens first. If it's True, then `not in result` runs. In the worst case (many duplicates), this check runs O(n²) times, each scanning a growing list.

**Actual complexity: O(n³)** worst case, **O(n²)** best case (no duplicates found, `not in result` rarely executed due to short-circuit).

### 2. Why the Colleague Might Have Thought O(n)

The colleague likely:
- Saw one meaningful "action" per element (finding whether it's a duplicate)
- Thought of the algorithm as "check each element once"
- Didn't recognize that `for j` is a second nested loop making it O(n²)
- Didn't know that `x not in list` is O(n), adding a third hidden loop
- Confused the **intent** (find duplicates = simple task) with the **implementation** (three nested scans)

### 3. O(n) Fix

```python
def find_duplicates(arr):
    seen = set()
    duplicates = set()

    for num in arr:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)

    return list(duplicates)
```

**Why this is O(n):**
- Single loop: n iterations
- `num in seen` → **set** lookup → O(1) ✅ (not list!)
- `seen.add(num)` → O(1)
- `duplicates.add(num)` → O(1)
- `list(duplicates)` at the end → O(d) where d = number of duplicates ≤ n
- Total: **O(n)**

**Space:** `seen` → O(n), `duplicates` → O(n). Total: **O(n)**

**What changed:**
1. Eliminated the nested loop entirely — single pass instead of all pairs
2. Used `set` instead of `list` for membership checks — O(1) instead of O(n)
3. Used a second set for deduplication of results — O(1) add instead of O(n) scan

> **Original: O(n³) worst case. Fixed: O(n) time, O(n) space.**
