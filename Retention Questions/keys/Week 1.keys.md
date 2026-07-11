# Answer Key — Week 1.md

**Source questions:** `Retention Questions/Week 1.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
**Solution A: O(n log n) time, O(1) space vs Solution B: O(n) time, O(n) space**

**Specific scenarios where A is better:**

**Scenario 1: Memory-constrained embedded system.**
You're writing firmware for a device with 256KB of RAM processing a sensor data stream of 1 million readings. O(n) space means allocating ~4MB for an auxiliary array — impossible on this hardware. O(1) space means processing in-place with whatever memory the input already occupies. The extra log factor in time is acceptable because the device has plenty of time but no spare memory.

**Scenario 2: Input is so large it barely fits in memory.**
You're processing a 30GB file on a machine with 32GB RAM. The input is memory-mapped and takes up nearly all available RAM. Allocating O(n) additional space would cause swapping to disk, which is orders of magnitude slower than RAM. The O(n log n) in-place solution stays in RAM and runs faster in practice despite the worse theoretical time complexity. The O(n) solution's O(n) space causes disk thrashing that dominates any time savings.

**Scenario 3: Cache performance matters more than operation count.**
The O(1) space solution works in-place, keeping data in CPU cache. The O(n) space solution jumps between two large arrays that don't both fit in cache, causing cache misses. For moderate n (say 10⁵ to 10⁶), the cache-friendly O(n log n) solution with small constants can actually be faster wall-clock than the cache-unfriendly O(n) solution. This is common in sorting: in-place heapsort vs. merge sort.

---


<!-- answer block 2 -->
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


<!-- answer block 3 -->
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


<!-- answer block 4 -->
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


<!-- answer block 5 -->
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


<!-- answer block 6 -->
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


