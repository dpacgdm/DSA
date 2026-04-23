# ARRAYS & STRINGS — THE COMPLETE LESSON

---

# PART 1: WHAT ARRAYS ACTUALLY ARE

## The Physical Reality

An array is a **contiguous block of memory** where elements are stored **side by side**. This isn't a metaphor — it's literally how your computer's RAM works.

```
Memory addresses:   [1000] [1008] [1016] [1024] [1032]
Array values:       [  10 ] [ 20 ] [ 30 ] [ 40 ] [ 50 ]
                     arr[0]  arr[1]  arr[2]  arr[3]  arr[4]
```

Each element occupies a fixed size (say 8 bytes). To find `arr[i]`, the computer calculates:

```
address of arr[i] = base_address + (i × element_size)
```

This is **one multiplication and one addition** — O(1) regardless of array size. This is **why array indexing is O(1).** It's not magic; it's arithmetic.

## Why This Matters

This physical layout has consequences:

| Property | Consequence |
|---|---|
| Contiguous memory | Cache-friendly — CPU loads nearby elements automatically. Arrays are **fast** in practice, not just in theory. |
| Fixed position by index | Random access is O(1) |
| Elements packed tightly | Inserting in the middle requires **shifting** everything after the insertion point |
| Size must be managed | Growing requires allocating new memory and copying everything |

## Python Lists Are NOT Traditional Arrays

Python `list` is a **dynamic array** — an array of **pointers** (references), not values.

```python
arr = [10, "hello", 3.14, True]  # This is legal in Python
```

In C/Java, an array holds values of one type directly in memory. A Python list holds **pointers to objects** scattered across memory:

```
List internal array:   [ptr] [ptr] [ptr] [ptr]
                        ↓     ↓     ↓     ↓
Objects in heap:       10  "hello" 3.14  True
```

**Implications:**
1. Python lists can hold mixed types (each pointer can point to anything)
2. Each access involves following a pointer — slightly slower than C arrays
3. The "array" part (the pointer array) is still contiguous → indexing is still O(1)
4. Element sizes vary, but pointer sizes are fixed → index math still works

For our purposes (DSA/CP/interviews), treat Python lists as arrays. The complexity guarantees are the same. Just know the underlying mechanics exist.

## Dynamic Resizing — How `.append()` Is O(1) Amortized

You learned amortized complexity in Big O. Here's the concrete mechanism:

```
Initial capacity: 4
arr = []

append(1): size=1, capacity=4  → fits, just store      O(1)
append(2): size=2, capacity=4  → fits                   O(1)
append(3): size=3, capacity=4  → fits                   O(1)
append(4): size=4, capacity=4  → fits                   O(1)
append(5): size=5, capacity=4  → FULL!
           Allocate new array of capacity 8
           Copy all 4 elements to new array              O(n)
           Store element 5                               O(1)
append(6): size=6, capacity=8  → fits                   O(1)
append(7): size=7, capacity=8  → fits                   O(1)
append(8): size=8, capacity=8  → fits                   O(1)
append(9): FULL! Allocate capacity 16, copy 8 elements  O(n)
...
```

Python grows by roughly **1.125x** (not 2x like textbooks often say). The exact growth factor is implementation-dependent, but the amortized analysis gives O(1) regardless of the exact factor (as long as it's multiplicative, not additive).

**Key insight:** The expensive O(n) copies are rare enough that averaged over all appends, each append costs O(1). This is why you can use `.append()` freely in loops without worrying about quadratic behavior.

---

# PART 2: THE COMPLETE OPERATIONS REFERENCE

## Python List Operations — Time Complexity

```
╔══════════════════════════════════════════════════════════════════╗
║                    PYTHON LIST OPERATIONS                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ACCESS / MODIFY                                                 ║
║  arr[i]                          O(1)     Index lookup           ║
║  arr[i] = x                     O(1)     Index assignment        ║
║  len(arr)                        O(1)     Stored as attribute    ║
║                                                                  ║
║  ADDING ELEMENTS                                                 ║
║  arr.append(x)                   O(1)*    Amortized              ║
║  arr.insert(i, x)               O(n)     Shifts elements right   ║
║  arr.insert(0, x)               O(n)     Worst case of insert    ║
║  arr.extend(other)              O(k)     k = len(other)          ║
║  arr + other                    O(n+k)   Creates new list        ║
║                                                                  ║
║  REMOVING ELEMENTS                                               ║
║  arr.pop()                       O(1)*    Remove last            ║
║  arr.pop(i)                      O(n)     Shifts elements left   ║
║  arr.pop(0)                      O(n)     Worst case of pop(i)   ║
║  arr.remove(x)                   O(n)     Search + shift         ║
║  del arr[i]                      O(n)     Same as pop(i)         ║
║  del arr[i:j]                    O(n)     Shift elements         ║
║                                                                  ║
║  SEARCHING                                                       ║
║  x in arr                        O(n)     Linear scan            ║
║  arr.index(x)                    O(n)     Linear scan            ║
║  arr.count(x)                    O(n)     Full scan              ║
║  min(arr), max(arr)              O(n)     Full scan              ║
║                                                                  ║
║  ORDERING                                                        ║
║  arr.sort()                      O(n log n)  In-place, Timsort   ║
║  sorted(arr)                     O(n log n)  Returns new list    ║
║  arr.reverse()                   O(n)        In-place            ║
║  reversed(arr)                   O(1)        Returns iterator    ║
║                                                                  ║
║  SLICING                                                         ║
║  arr[i:j]                        O(j-i)   Creates new list       ║
║  arr[:]                          O(n)     Full copy              ║
║  arr[::2]                        O(n/2)   Step slicing           ║
║                                                                  ║
║  COMPARISON                                                      ║
║  arr1 == arr2                    O(n)     Element-wise           ║
║                                                                  ║
║  MULTIPLICATION                                                  ║
║  arr * k                         O(n*k)   Creates new list       ║
║                                                                  ║
║  * = amortized                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

## The Operations That Trap You

### Trap 1: `insert(0, x)` and `pop(0)` Are O(n)

```python
# ❌ Building a list by prepending — O(n²) total
result = []
for x in data:          # n iterations
    result.insert(0, x) # O(n) each — shifts everything right

# ✅ Append and reverse — O(n) total
result = []
for x in data:
    result.append(x)    # O(1) each
result.reverse()        # O(n) once
```

If you need O(1) operations at **both ends**, use `collections.deque`:

```python
from collections import deque
d = deque()
d.appendleft(x)  # O(1)
d.popleft()       # O(1)
d.append(x)       # O(1)
d.pop()            # O(1)
```

### Trap 2: `x in list` Is O(n); `x in set` Is O(1)

```python
# ❌ O(n) lookup inside a loop — O(n²) total
for item in data:
    if item in other_list:    # O(n) each time
        process(item)

# ✅ Convert to set first — O(n) total
other_set = set(other_list)   # O(n) once
for item in data:
    if item in other_set:     # O(1) each time
        process(item)
```

### Trap 3: Repeated Concatenation Is O(n²)

```python
# ❌ O(n²) — creates new string each iteration
result = ""
for char in data:
    result += char      # O(len(result)) each time — copies entire string

# ✅ O(n) — join at the end
parts = []
for char in data:
    parts.append(char)  # O(1)
result = "".join(parts) # O(n) once

# ✅ Even simpler
result = "".join(data)
```

### Trap 4: Slicing Inside Loops

```python
# ❌ Hidden O(n) per iteration
for i in range(len(arr)):
    sub = arr[i:]        # O(n-i) — creates new list each time
    process(sub)         # Total slicing cost: O(n²)

# ✅ Use indices instead
for i in range(len(arr)):
    process(arr, i, len(arr))  # Pass indices, no copying
```

### Trap 5: `del arr[0]` in a Loop

```python
# ❌ O(n²) — shifting on every deletion
while arr:
    process(arr[0])
    del arr[0]         # O(n) each time

# ✅ Iterate with index or use deque
for item in arr:
    process(item)

# ✅ If you need to consume from front
from collections import deque
d = deque(arr)
while d:
    process(d.popleft())  # O(1)
```

---

# PART 3: STRINGS IN PYTHON — THE DEEP TRUTH

## Strings Are Immutable Arrays

A string in Python is an **immutable sequence of characters.** It supports indexing, slicing, and iteration — just like a list. But you **cannot modify it in place.**

```python
s = "hello"
s[0]        # 'h' — O(1) indexing ✅
s[1:4]      # 'ell' — O(k) slicing ✅
len(s)      # 5 — O(1) ✅

s[0] = 'H'  # TypeError: 'str' object does not support item assignment ❌
```

**Every "modification" creates a new string.** This is the single most important fact about Python strings for DSA.

```python
s = "hello"
s = "H" + s[1:]  # Creates brand new string "Hello"
                   # The old "hello" is now garbage
```

## String Operations — Time Complexity

```
╔═══════════════════════════════════════════════════════════════════╗
║                    PYTHON STRING OPERATIONS                       ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ACCESS                                                           ║
║  s[i]                            O(1)     Index lookup            ║
║  len(s)                          O(1)     Stored attribute        ║
║  s[i:j]                         O(j-i)   Creates new string       ║
║                                                                   ║
║  SEARCHING                                                        ║
║  c in s                          O(n)     Linear scan             ║
║  s.find(sub)                     O(n*m)   n=len(s), m=len(sub)    ║
║  s.index(sub)                    O(n*m)   Same, raises error      ║
║  s.count(sub)                    O(n*m)   Full scan               ║
║  s.startswith(pre)               O(k)     k=len(pre)              ║
║  s.endswith(suf)                 O(k)     k=len(suf)              ║
║                                                                   ║
║  BUILDING / MODIFYING (all create new strings)                    ║
║  s + t                           O(n+m)   Concatenation           ║
║  s * k                           O(n*k)   Repetition              ║
║  "".join(list)                   O(total) Sum of all lengths      ║
║  s.replace(old, new)             O(n)     Scans and rebuilds      ║
║  s.lower() / s.upper()          O(n)     New string               ║
║  s.strip()                       O(n)     New string              ║
║  s.split(sep)                    O(n)     Creates list of strings ║
║                                                                   ║
║  COMPARISON                                                       ║
║  s == t                          O(min(n,m))  Character by char   ║
║  s < t                           O(min(n,m))  Lexicographic       ║
║                                                                   ║
║  CHECKING                                                         ║
║  s.isdigit()                     O(n)                             ║
║  s.isalpha()                     O(n)                             ║
║  s.isalnum()                     O(n)                             ║
║                                                                   ║
║  ENCODING                                                         ║
║  ord('a')                        O(1)     Character → integer     ║
║  chr(97)                         O(1)     Integer → character     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

## The String ↔ List Dance

Since strings are immutable, many string problems require converting to a list, manipulating, then converting back:

```python
# Pattern: string → list → manipulate → string
s = "hello"
chars = list(s)        # ['h', 'e', 'l', 'l', 'o']  O(n)
chars[0] = 'H'         # Modify in place             O(1)
chars.reverse()        # In-place operations          O(n)
result = "".join(chars) # Back to string              O(n)
```

This is **the standard approach** when a problem says "modify a string." Interviewers know Python strings are immutable and expect this pattern.

## `ord()` and `chr()` — Character Math

Every character has a numeric code (ASCII / Unicode). You'll use this **constantly** in DSA:

```python
ord('a')  # 97
ord('z')  # 122
ord('A')  # 65
ord('Z')  # 90
ord('0')  # 48
ord('9')  # 57

chr(97)   # 'a'
chr(65)   # 'A'
```

**Pattern: Using characters as array indices**
```python
# Count frequency of lowercase letters
count = [0] * 26
for char in s:
    count[ord(char) - ord('a')] += 1
```

This maps 'a'→0, 'b'→1, ..., 'z'→25. It's O(1) space (fixed 26 slots) and O(n) time. This is faster than a dictionary for the common case of lowercase-only strings, though `Counter` is cleaner in practice.

**Pattern: Checking character ranges**
```python
def is_lowercase(c):
    return ord('a') <= ord(c) <= ord('z')

def is_digit(c):
    return ord('0') <= ord(c) <= ord('9')

# Or use built-in methods
c.islower()
c.isdigit()
```

---

# PART 4: FUNDAMENTAL ARRAY TECHNIQUES

## Technique 1: In-Place Manipulation

Modifying the array without creating a new one. Saves O(n) space.

### Swap

The most fundamental operation:

```python
arr[i], arr[j] = arr[j], arr[i]  # Python simultaneous swap
```

This is **O(1)** and doesn't need a temp variable (Python handles it internally).

### Reversal

Reverse a subarray from index `left` to `right`:

```python
def reverse(arr, left, right):
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

Time: O(right - left). Space: O(1).

Python shortcut: `arr[left:right+1] = arr[left:right+1][::-1]` — but this creates temporary copies. The manual version is truly in-place.

### Array Rotation

Rotate array right by k positions: `[1,2,3,4,5]` with k=2 → `[4,5,1,2,3]`

**The Three-Reverse Trick:**

```python
def rotate(arr, k):
    n = len(arr)
    k = k % n              # Handle k > n
    
    reverse(arr, 0, n - 1)     # Reverse entire array
    reverse(arr, 0, k - 1)     # Reverse first k elements
    reverse(arr, k, n - 1)     # Reverse remaining elements
```

```
[1, 2, 3, 4, 5]  k=2
Step 1: Reverse all      → [5, 4, 3, 2, 1]
Step 2: Reverse [0:2]    → [4, 5, 3, 2, 1]
Step 3: Reverse [2:5]    → [4, 5, 1, 2, 3] ✅
```

Time: O(n). Space: O(1). **This is a FAANG classic.** Memorize this technique.

### Dutch National Flag Partition (Three-Way Partition)

Partition array into three groups: elements < pivot, elements == pivot, elements > pivot.

```python
def three_way_partition(arr, pivot):
    low = 0                 # Everything before low is < pivot
    mid = 0                 # Current element being examined
    high = len(arr) - 1     # Everything after high is > pivot
    
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # Don't increment mid! The swapped element hasn't been examined
        else:
            mid += 1  # arr[mid] == pivot, already in place
```

Time: O(n). Space: O(1). Single pass.

**Why `mid` doesn't increment when swapping with `high`:** The element swapped from `high` to `mid` hasn't been examined yet — it could be less than, equal to, or greater than the pivot. When swapping with `low`, the element at `low` has already been examined (it was at `mid` earlier), so it's safe to move past it.

This is used in Quick Sort's partition and appears in FAANG interviews (often as "Sort Colors" on LeetCode).

---

## Technique 2: Prefix Sums

**The Problem:** Given an array, answer multiple range sum queries efficiently.

**Naive approach:** For each query `sum(arr[i:j+1])`, iterate from i to j. Each query is O(n). For q queries: O(n × q).

**Prefix sum approach:** Preprocess once, answer each query in O(1).

```python
def build_prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)  # prefix[0] = 0 (empty prefix)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    """Sum of arr[left..right] inclusive"""
    return prefix[right + 1] - prefix[left]
```

```
arr    = [3, 1, 4, 1, 5, 9]
prefix = [0, 3, 4, 8, 9, 14, 23]

Sum of arr[1..4] = prefix[5] - prefix[1] = 14 - 3 = 11
Verify: 1 + 4 + 1 + 5 = 11 ✅
```

**Why it works:** `prefix[i]` = sum of elements before index i. The sum from index `left` to `right` is (sum of first right+1 elements) minus (sum of first left elements).

**Complexity:**
- Build: O(n) time, O(n) space
- Each query: O(1) time
- q queries after build: O(n + q) total

**When to use:** Any time you need multiple range sum queries. Also useful for:
- Running averages
- Finding if a subarray sums to a target
- 2D prefix sums (matrix region sums) — common in interviews

### 2D Prefix Sums (Matrix)

For a matrix of size m × n, compute prefix sums so any rectangular subregion sum is O(1):

```python
def build_2d_prefix(matrix):
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m):
        for j in range(n):
            prefix[i+1][j+1] = (matrix[i][j] 
                                + prefix[i][j+1] 
                                + prefix[i+1][j] 
                                - prefix[i][j])
    return prefix

def region_sum(prefix, r1, c1, r2, c2):
    """Sum of submatrix from (r1,c1) to (r2,c2) inclusive"""
    return (prefix[r2+1][c2+1] 
            - prefix[r1][c2+1] 
            - prefix[r2+1][c1] 
            + prefix[r1][c1])
```

This uses the **inclusion-exclusion** principle. Build is O(m × n). Each query is O(1).

---

## Technique 3: Kadane's Algorithm (Maximum Subarray Sum)

**The Problem:** Find the contiguous subarray with the largest sum.

```python
def max_subarray(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**The Intuition:** At each element, we decide: should I extend the current subarray, or start a new one here? If the current running sum is negative, it can only drag down future sums, so we start fresh.

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: current=-2, max=-2
i=1: max(1, -2+1)=1,     max=1
i=2: max(-3, 1-3)=-2,    max=1
i=3: max(4, -2+4)=4,     max=4
i=4: max(-1, 4-1)=3,     max=4
i=5: max(2, 3+2)=5,      max=5
i=6: max(1, 5+1)=6,      max=6       ← answer is subarray [4,-1,2,1]
i=7: max(-5, 6-5)=1,     max=6
i=8: max(4, 1+4)=5,      max=6

Answer: 6 ✅
```

Time: O(n). Space: O(1). **This is a top 10 most-asked FAANG problem.**

### Variant: Return the Subarray, Not Just the Sum

```python
def max_subarray_with_indices(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum = current_sum + arr[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, arr[start:end+1]
```

---

## Technique 4: Working With Subarrays and Subsequences

### Definitions — Get These Right

```
SUBARRAY (contiguous subsequence):
  Elements must be ADJACENT in the original array.
  [1,2,3,4,5] → subarrays include [2,3,4] but NOT [2,4]

SUBSEQUENCE:
  Elements maintain RELATIVE ORDER but need not be adjacent.
  [1,2,3,4,5] → subsequences include [1,3,5] and [2,4]

SUBSET:
  No order requirement. Just a selection of elements.
  [1,2,3] → subsets include {3,1} (order doesn't matter)
```

### Counting

```
Array of length n:
  Number of subarrays:    n(n+1)/2      = O(n²)
  Number of subsequences: 2ⁿ            = O(2ⁿ)
  Number of subsets:      2ⁿ            = O(2ⁿ)
```

This tells you: if a problem asks for "all subarrays," any solution must be at least O(n²). If it asks for "all subsequences," at least O(2ⁿ).

### Generating All Subarrays

```python
def all_subarrays(arr):
    n = len(arr)
    result = []
    for start in range(n):
        for end in range(start + 1, n + 1):
            result.append(arr[start:end])
    return result
```

Time: O(n³) — O(n²) subarrays, each slice costs up to O(n).
With just printing/counting (no slicing): O(n²).

---

## Technique 5: Matrix Operations

### Traversal Patterns

```python
# Row by row (standard)
for i in range(rows):
    for j in range(cols):
        process(matrix[i][j])

# Column by column
for j in range(cols):
    for i in range(rows):
        process(matrix[i][j])

# Diagonal (top-left to bottom-right)
for i in range(min(rows, cols)):
    process(matrix[i][i])

# Anti-diagonal
for i in range(min(rows, cols)):
    process(matrix[i][cols - 1 - i])
```

### Matrix Transpose

```python
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]
```

For a **square** matrix, in-place:
```python
def transpose_inplace(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

### Matrix Rotation (90° Clockwise)

**Transpose + Reverse each row:**

```python
def rotate_90_clockwise(matrix):
    n = len(matrix)
    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

```
Original:       Transpose:      Reverse rows:
1 2 3           1 4 7           7 4 1
4 5 6    →      2 5 8    →      8 5 2
7 8 9           3 6 9           9 6 3
```

Time: O(n²). Space: O(1). **Another FAANG classic.**

### Spiral Order Traversal

```python
def spiral_order(matrix):
    result = []
    if not matrix:
        return result
    
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Right across top
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # Down right side
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # Left across bottom (if rows remain)
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        # Up left side (if columns remain)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result
```

Time: O(m × n). Space: O(1) excluding output.

---

# PART 5: FUNDAMENTAL STRING TECHNIQUES

## Technique 1: Character Frequency Counting

Three approaches, each with tradeoffs:

```python
# Method 1: Fixed array (when charset is known and small)
count = [0] * 26  # lowercase only
for c in s:
    count[ord(c) - ord('a')] += 1
# O(n) time, O(1) space (26 is constant)

# Method 2: Dictionary
count = {}
for c in s:
    count[c] = count.get(c, 0) + 1
# O(n) time, O(k) space where k = unique characters

# Method 3: Counter (most Pythonic)
from collections import Counter
count = Counter(s)
# O(n) time, O(k) space
# Bonus: count.most_common(k) gives top k in O(k log k)
```

**When to use which:**
- Fixed array: when you need raw speed and know the charset (competitive programming)
- Dictionary: when charset is unknown or large
- Counter: interviews (clean, readable, shows Python fluency)

## Technique 2: Anagram Detection

Two strings are anagrams if they have the same character frequencies.

```python
# Method 1: Sort both (simple but slower)
def is_anagram(s, t):
    return sorted(s) == sorted(t)
# O(n log n) time, O(n) space

# Method 2: Count and compare (optimal)
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
# O(n) time, O(k) space

# Method 3: Single count array (most efficient)
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    return all(c == 0 for c in count)
# O(n) time, O(1) space
```

## Technique 3: Palindrome Checking

```python
# Method 1: Two pointers (optimal)
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
# O(n) time, O(1) space

# Method 2: Reverse comparison (simple but uses space)
def is_palindrome(s):
    return s == s[::-1]
# O(n) time, O(n) space (creates reversed copy)
```

For problems that say "ignore non-alphanumeric characters and case":

```python
def is_palindrome_clean(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

## Technique 4: String Building Patterns

```python
# ❌ NEVER do this
result = ""
for item in data:
    result += str(item) + ","

# ✅ Use join
result = ",".join(str(item) for item in data)

# ✅ Use list accumulation
parts = []
for item in data:
    parts.append(str(item))
result = ",".join(parts)

# ✅ For complex building, use io.StringIO
from io import StringIO
buffer = StringIO()
for item in data:
    buffer.write(str(item))
    buffer.write(",")
result = buffer.getvalue()
```

## Technique 5: Substring Search Patterns

```python
# Check if substring exists
if "abc" in s:           # O(n*m) worst case, but CPython optimizes

# Find first occurrence
pos = s.find("abc")     # Returns index or -1
pos = s.index("abc")    # Returns index or raises ValueError

# Find all occurrences
def find_all(s, sub):
    positions = []
    start = 0
    while True:
        pos = s.find(sub, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions
```

---

# PART 6: TWO POINTERS

## What It Is

Two pointers is a technique where you maintain **two index variables** that move through the data structure, typically an array or string. The pointers move based on conditions, reducing what would be O(n²) brute force to O(n).

## When To Use It

```
USE TWO POINTERS WHEN:
1. Array/string is SORTED (or has a property that lets you 
   decide which pointer to move)
2. You're looking for a PAIR or SUBARRAY satisfying a condition
3. You need to COMPARE/MERGE elements from two ends or two arrays
4. You need to PARTITION or REMOVE elements in-place
```

## Sub-Pattern A: Opposite Direction (Left-Right)

Two pointers start at opposite ends and move toward each other.

### Framework

```python
def opposite_pointers(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        if condition_met(arr, left, right):
            record_result(arr, left, right)
            left += 1       # or right -= 1, or both
        elif need_bigger:
            left += 1       # Move left to increase value
        else:
            right -= 1      # Move right to decrease value
```

### Example: Two Sum on Sorted Array

Given a **sorted** array and target, find two numbers that sum to target.

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1       # Need bigger sum → move left pointer right
        else:
            right -= 1      # Need smaller sum → move right pointer left
    
    return [-1, -1]  # No pair found
```

**Why it works:** Array is sorted. If sum is too small, increasing `left` (smaller element) increases the sum. If sum is too big, decreasing `right` (larger element) decreases the sum. We never miss a valid pair because any pair we skip was guaranteed to be too big or too small.

Time: O(n). Space: O(1).

**Compare to brute force:**
```python
# Brute force: O(n²)
for i in range(n):
    for j in range(i + 1, n):
        if arr[i] + arr[j] == target:
            return [i, j]
```

### Example: Container With Most Water

Given heights array, find two lines that form a container holding the most water.

```python
def max_area(heights):
    left, right = 0, len(heights) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        max_water = max(max_water, width * height)
        
        if heights[left] < heights[right]:
            left += 1      # Left is the limiting factor, try taller
        else:
            right -= 1     # Right is limiting, try taller
    
    return max_water
```

**Why move the shorter side?** Width always decreases as pointers converge. The only way to get more water is to find a taller line. Moving the **taller** side can never help — the height is limited by the shorter side, and the width shrinks. Moving the **shorter** side might find something taller.

Time: O(n). Space: O(1).

### Example: Trapping Rain Water

```python
def trap(heights):
    if not heights:
        return 0
    
    left, right = 0, len(heights) - 1
    left_max, right_max = heights[left], heights[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, heights[left])
            water += left_max - heights[left]
        else:
            right -= 1
            right_max = max(right_max, heights[right])
            water += right_max - heights[right]
    
    return water
```

**Why it works:** Water at any position = `min(max_left, max_right) - height`. When `left_max < right_max`, we know the water at `left` is determined by `left_max` (because there's definitely something ≥ `right_max` on the right). So we can safely compute water at `left` and advance.

Time: O(n). Space: O(1).

---

## Sub-Pattern B: Same Direction (Fast-Slow)

Both pointers start at the same end. One moves faster or conditionally.

### Framework

```python
def same_direction(arr):
    slow = 0
    
    for fast in range(len(arr)):
        if should_keep(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1
    
    return slow  # New length of valid portion
```

### Example: Remove Duplicates from Sorted Array (In-Place)

```python
def remove_duplicates(arr):
    if not arr:
        return 0
    
    slow = 0
    
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    
    return slow + 1  # Length of unique portion
```

```
arr = [1, 1, 2, 2, 3]

fast=1: arr[1]=1 == arr[0]=1, skip
fast=2: arr[2]=2 != arr[0]=1, slow=1, arr[1]=2 → [1,2,2,2,3]
fast=3: arr[3]=2 == arr[1]=2, skip
fast=4: arr[4]=3 != arr[1]=2, slow=2, arr[2]=3 → [1,2,3,2,3]

Return slow+1 = 3. First 3 elements: [1,2,3] ✅
```

Time: O(n). Space: O(1).

### Example: Remove Element (In-Place)

Remove all occurrences of `val`:

```python
def remove_element(arr, val):
    slow = 0
    
    for fast in range(len(arr)):
        if arr[fast] != val:
            arr[slow] = arr[fast]
            slow += 1
    
    return slow
```

### Example: Move Zeroes

Move all zeroes to the end, maintaining order of non-zero elements:

```python
def move_zeroes(arr):
    slow = 0
    
    for fast in range(len(arr)):
        if arr[fast] != 0:
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1
```

Note: we **swap** instead of overwrite because we want to preserve the zeroes (just move them to the end).

### Example: Linked List Cycle Detection (Floyd's Algorithm)

Slow pointer moves 1 step, fast pointer moves 2 steps. If there's a cycle, they'll meet.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

We'll explore this deeply in Week 4 (Linked Lists).

---

## Sub-Pattern C: Two Arrays/Strings

One pointer per array, both moving forward.

### Example: Merge Two Sorted Arrays

```python
def merge_sorted(arr1, arr2):
    result = []
    i = j = 0
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

Time: O(n + m). Space: O(n + m) for result.

### Example: Is Subsequence

Is `s` a subsequence of `t`? (Characters of `s` appear in `t` in order, not necessarily adjacent.)

```python
def is_subsequence(s, t):
    i = 0  # pointer for s
    j = 0  # pointer for t
    
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1  # Matched this character of s
        j += 1      # Always advance in t
    
    return i == len(s)  # Did we match all of s?
```

Time: O(n + m). Space: O(1).

---

## Two Pointer Decision Framework

```
╔═══════════════════════════════════════════════════════════════╗
║              WHICH TWO-POINTER PATTERN?                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Is the array SORTED or do you need to compare from both      ║
║  ends?                                                        ║
║    YES → Opposite Direction (left/right)                      ║
║                                                               ║
║  Do you need to FILTER or PARTITION in-place?                 ║
║    YES → Same Direction (slow/fast)                           ║
║                                                               ║
║  Are you processing TWO arrays/strings simultaneously?        ║
║    YES → Two Arrays pattern (one pointer each)                ║
║                                                               ║
║  Is it a LINKED LIST problem about cycles or middle nodes?    ║
║    YES → Fast/Slow pointers                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

# PART 7: SLIDING WINDOW

## What It Is

A sliding window maintains a **contiguous subarray/substring** that expands and contracts as you scan through the array. Instead of re-examining all elements in each subarray, you update the window **incrementally** — adding one element and removing another.

## Why It's Powerful

**Brute force:** Check every subarray → O(n²) or O(n³).
**Sliding window:** Each element enters and leaves the window at most once → O(n).

## Sub-Pattern A: Fixed-Size Window

Window size is constant. Slide it across the array.

### Framework

```python
def fixed_window(arr, k):
    # Initialize window with first k elements
    window_value = compute(arr[0:k])
    best = window_value
    
    for i in range(k, len(arr)):
        # Add new element (entering from right)
        window_value = add(window_value, arr[i])
        # Remove old element (leaving from left)
        window_value = remove(window_value, arr[i - k])
        # Update answer
        best = update(best, window_value)
    
    return best
```

### Example: Maximum Sum of Subarray of Size k

```python
def max_sum_subarray(arr, k):
    # Initialize: sum of first k elements
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i]        # Add new element
        window_sum -= arr[i - k]    # Remove old element
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

```
arr = [2, 1, 5, 1, 3, 2], k = 3

Window [2,1,5]: sum=8, max=8
Slide: add 1, remove 2 → [1,5,1]: sum=7, max=8
Slide: add 3, remove 1 → [5,1,3]: sum=9, max=9
Slide: add 2, remove 5 → [1,3,2]: sum=6, max=9

Answer: 9 ✅
```

Time: O(n). Space: O(1).

### Example: Find All Anagrams in String

Given string `s` and pattern `p`, find all starting indices in `s` where an anagram of `p` begins.

```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    
    result = []
    p_count = [0] * 26
    s_count = [0] * 26
    
    for c in p:
        p_count[ord(c) - ord('a')] += 1
    
    for i in range(len(s)):
        # Add new character
        s_count[ord(s[i]) - ord('a')] += 1
        
        # Remove character that fell off the window
        if i >= len(p):
            s_count[ord(s[i - len(p)]) - ord('a')] -= 1
        
        # Compare
        if s_count == p_count:
            result.append(i - len(p) + 1)
    
    return result
```

Time: O(n × 26) = O(n) since comparing two 26-length arrays is O(26) = O(1).
Space: O(1) — two fixed-size arrays.

**Optimization:** Instead of comparing full arrays each time, maintain a `matches` counter tracking how many of the 26 characters currently have equal counts. When `matches == 26`, it's an anagram. This makes each step truly O(1).

---

## Sub-Pattern B: Variable-Size Window

Window expands and contracts based on conditions. This is the more powerful (and trickier) pattern.

### Framework: The Expand-Contract Template

```python
def variable_window(arr):
    left = 0
    window_state = initial_state()
    best = initial_best()
    
    for right in range(len(arr)):
        # EXPAND: Add arr[right] to window
        update_state(window_state, arr[right])
        
        # CONTRACT: Shrink from left while window is invalid
        while window_is_invalid(window_state):
            remove_from_state(window_state, arr[left])
            left += 1
        
        # UPDATE: Window is valid, update answer
        best = update_best(best, left, right)
    
    return best
```

**The key insight:** The `right` pointer always moves forward (one step per iteration). The `left` pointer only moves forward (never backward). Total movement of both pointers ≤ 2n. **This is why it's O(n), not O(n²).** Each element is added once (when `right` reaches it) and removed at most once (when `left` passes it).

### Example: Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s):
    char_index = {}  # Last seen index of each character
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1  # Jump left past the duplicate
        
        char_index[s[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

```
s = "abcabcbb"

right=0: 'a', window="a", max=1
right=1: 'b', window="ab", max=2
right=2: 'c', window="abc", max=3
right=3: 'a' seen at 0, left=1, window="bca", max=3
right=4: 'b' seen at 1, left=2, window="cab", max=3
right=5: 'c' seen at 2, left=3, window="abc", max=3
right=6: 'b' seen at 4, left=5, window="cb", max=3
right=7: 'b' seen at 6, left=7, window="b", max=3

Answer: 3 ✅
```

Time: O(n). Space: O(min(n, alphabet_size)).

### Example: Minimum Window Substring

Find the smallest substring of `s` that contains all characters of `t`.

```python
def min_window(s, t):
    if not t or not s:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)     # Number of unique characters needed
    formed = 0                   # How many unique characters we have enough of
    window_counts = {}
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        # EXPAND
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # CONTRACT
        while formed == required:
            # Update answer
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove from left
            leaving = s[left]
            window_counts[leaving] -= 1
            if leaving in t_count and window_counts[leaving] < t_count[leaving]:
                formed -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

Time: O(n + m). Space: O(n + m) for the counters.

**This is a HARD LeetCode problem and a FAANG favorite.** The key insight: expand until valid, then contract to find minimum. The `formed` counter avoids re-scanning the entire frequency map each time.

### Example: Longest Substring With At Most K Distinct Characters

```python
def longest_k_distinct(s, k):
    char_count = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # Expand
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Contract while too many distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

Time: O(n). Space: O(k).

---

## Sub-Pattern C: Window With Auxiliary Data Structures

Sometimes the window needs more complex tracking.

### Example: Sliding Window Maximum (Preview — Uses Monotonic Deque)

Find the maximum element in every window of size k. We'll cover the monotonic deque solution in Week 6. For now, know this exists:

```python
from collections import deque

def max_sliding_window(arr, k):
    dq = deque()  # Stores indices, front is always the max
    result = []
    
    for i in range(len(arr)):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (they'll never be the max)
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result
```

Time: O(n). Space: O(k).

---

## Sliding Window Decision Framework

```
╔═══════════════════════════════════════════════════════════════╗
║              WHICH SLIDING WINDOW PATTERN?                    ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  "Find max/min/average of ALL subarrays of size k"            ║
║    → Fixed window                                             ║
║                                                               ║
║  "Find longest/shortest subarray where [condition]"           ║
║    → Variable window                                          ║
║    → Expand right, contract left                              ║
║                                                               ║
║  "Find longest with at most k [something]"                    ║
║    → Variable window, contract when > k                       ║
║                                                               ║
║  "Find shortest that contains all [something]"                ║
║    → Variable window, contract when valid                     ║
║                                                               ║
║  "Find number of subarrays where [condition]"                 ║
║    → Variable window, count at each step                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

# PART 8: COMMON INTERVIEW PATTERNS CHEAT SHEET

```
╔═══════════════════════════════════════════════════════════════════╗
║               ARRAYS & STRINGS PATTERN MATCHER                    ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  "Find pair with sum = target"                                    ║
║    Sorted → Two pointers (opposite)                O(n)           ║
║    Unsorted → Hash map                             O(n)           ║
║                                                                   ║
║  "Find subarray with sum = target"                                ║
║    All positive → Sliding window                   O(n)           ║
║    Mixed → Prefix sum + hash map                   O(n)           ║
║                                                                   ║
║  "Maximum/minimum subarray"                                       ║
║    Sum → Kadane's algorithm                        O(n)           ║
║    Product → Track max AND min (negatives flip)    O(n)           ║
║                                                                   ║
║  "Longest substring with condition"                               ║
║    → Sliding window (variable)                     O(n)           ║
║                                                                   ║
║  "All anagrams / permutation match"                               ║
║    → Sliding window (fixed) + frequency count      O(n)           ║
║                                                                   ║
║  "Remove / deduplicate in-place"                                  ║
║    → Two pointers (same direction)                 O(n)           ║
║                                                                   ║
║  "Merge sorted arrays"                                            ║
║    → Two pointers (two arrays)                     O(n+m)         ║
║                                                                   ║
║  "Rotate array/matrix"                                            ║
║    Array → Three-reverse trick                     O(n)           ║
║    Matrix → Transpose + reverse rows               O(n²)          ║
║                                                                   ║
║  "Range sum queries"                                              ║
║    → Prefix sums                                   O(1) per query ║
║                                                                   ║
║  "Partition array by condition"                                   ║
║    Two groups → Two pointers                       O(n)           ║
║    Three groups → Dutch National Flag              O(n)           ║
║                                                                   ║
║  "Is palindrome"                                                  ║
║    → Two pointers (opposite)                       O(n)           ║
║                                                                   ║
║  "String matching / substring search"                             ║
║    Simple → Built-in or sliding window             O(n)           ║
║    Advanced → KMP / Rabin-Karp (Week 10)           O(n)           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

# PART 9: PYTHON-SPECIFIC TOOLS AND TRICKS

## List Comprehensions

```python
# Filtering
evens = [x for x in arr if x % 2 == 0]

# Transformation
squares = [x**2 for x in arr]

# Flattening 2D
flat = [x for row in matrix for x in row]

# Creating 2D arrays
matrix = [[0] * cols for _ in range(rows)]
# ❌ NEVER: matrix = [[0] * cols] * rows  ← all rows share same reference!
```

### The 2D Array Trap — This Will Bite You

```python
# ❌ WRONG — all rows are the SAME object
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # [[1,0,0], [1,0,0], [1,0,0]]  ← ALL rows changed!

# ✅ RIGHT — each row is independent
matrix = [[0] * 3 for _ in range(3)]
matrix[0][0] = 1
print(matrix)  # [[1,0,0], [0,0,0], [0,0,0]]  ✅
```

`[[0] * 3] * 3` creates **one** list `[0,0,0]` and makes three references to it. Mutating through any reference mutates the shared object. The list comprehension creates **three separate** list objects.

## Useful Built-ins

```python
# enumerate — index and value
for i, val in enumerate(arr):
    print(i, val)

# zip — parallel iteration
for a, b in zip(arr1, arr2):
    print(a, b)

# zip with index
for i, (a, b) in enumerate(zip(arr1, arr2)):
    print(i, a, b)

# any / all
any(x > 0 for x in arr)   # True if ANY element > 0
all(x > 0 for x in arr)   # True if ALL elements > 0

# map
result = list(map(int, ["1", "2", "3"]))  # [1, 2, 3]

# sorted with key
sorted(arr, key=lambda x: x[1])         # Sort by second element
sorted(arr, key=lambda x: (-x[0], x[1])) # Sort by first desc, second asc

# Infinity
float('inf')   # Positive infinity
float('-inf')  # Negative infinity
```

## `collections` Module

```python
from collections import Counter, defaultdict, deque

# Counter
c = Counter("aabbc")  # {'a': 2, 'b': 2, 'c': 1}
c.most_common(2)       # [('a', 2), ('b', 2)]
c['d']                 # 0 (doesn't raise KeyError)

# defaultdict
d = defaultdict(list)
d['key'].append(1)     # No need to check if 'key' exists

d = defaultdict(int)
d['key'] += 1          # No need to initialize to 0

# deque
dq = deque([1, 2, 3])
dq.appendleft(0)       # O(1)
dq.popleft()           # O(1)
dq.append(4)           # O(1)
dq.pop()               # O(1)
```

---

# PART 10: TEST PROBLEMS

---

### Problem 1: Rotate Array

Given an array and integer k, rotate the array to the right by k steps. **Do it in-place with O(1) extra space.**

```
Input: arr = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
```

---

### Problem 2: Two Sum (Unsorted)

Given an unsorted array and target, return the **indices** of two numbers that sum to target. Assume exactly one solution exists.

```
Input: arr = [2,7,11,15], target = 9
Output: [0, 1]
```

**Do NOT sort.** Optimal solution required.

---

### Problem 3: Maximum Subarray (Kadane's)

Find the contiguous subarray with the largest sum. Return the sum.

```
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6 (subarray [4, -1, 2, 1])
```

Also return the start and end indices of the subarray.

---

### Problem 4: Move Zeroes

Move all zeroes to the end while maintaining the relative order of non-zero elements. **In-place, minimize operations.**

```
Input: [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```

---

### Problem 5: Container With Most Water

Given array `heights` where each element represents the height of a vertical line, find two lines that together with the x-axis form a container that holds the most water.

```
Input: [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```

Prove why your approach doesn't miss the optimal pair.

---

### Problem 6: Longest Substring Without Repeating Characters

Given a string, find the length of the longest substring without repeating characters.

```
Input: "abcabcbb"
Output: 3 ("abc")
```

---

### Problem 7: Find All Anagrams in a String

Given string `s` and pattern `p`, find all start indices of `p`'s anagrams in `s`.

```
Input: s = "cbaebabacd", p = "abc"
Output: [0, 6]
```

---

### Problem 8: Trapping Rain Water

Given an array of non-negative integers representing elevation heights, compute how much water can be trapped after raining.

```
Input: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6
```

---

### Problem 9: Rotate Image (Matrix 90° Clockwise)

Rotate an n×n matrix 90 degrees clockwise. **In-place.**

```
Input:
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]

Output:
[[7, 4, 1],
 [8, 5, 2],
 [9, 6, 3]]
```

---

### Problem 10: Minimum Window Substring

Given strings `s` and `t`, find the minimum length substring of `s` that contains **all** characters of `t` (including duplicates).

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

---

**Solve all 10. For each problem:**
1. **Identify the pattern** (which technique from this lesson)
2. **Write the solution**
3. **Trace through the given example**
4. **Edge cases** (at least 2)
5. **Full complexity analysis** (time and space)
6. **For Problems 5 and 8:** Prove correctness of the two-pointer approach — explain why no valid answer is skipped.

# Problem 1: Rotate Array

## Pattern Identification

**Pattern: Three Reverses**

Why? Rotating right by k means the last k elements move to the front. The trick: reversing the whole array puts those last k elements at the front but in wrong order. Then reverse the first k and last n-k portions individually to fix the order. Three O(n) in-place reverses = O(n) total, O(1) space.

## Solution

```python
def rotate(arr, k):
    n = len(arr)
    k = k % n  # handle k > n

    def reverse(left, right):
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    reverse(0, n - 1)       # reverse entire array
    reverse(0, k - 1)       # reverse first k elements
    reverse(k, n - 1)       # reverse remaining elements
```

## Why `k = k % n`

If k = n, we rotate a full cycle back to the original. If k = n + 3, that's the same as rotating by 3. Modulo handles all cases where k ≥ n.

## Trace Through Main Example

```
arr = [1, 2, 3, 4, 5, 6, 7], k = 3
n = 7, k = 3 % 7 = 3

Step 1 — Reverse entire array:
[1, 2, 3, 4, 5, 6, 7] → [7, 6, 5, 4, 3, 2, 1]

Step 2 — Reverse first 3 elements [7, 6, 5]:
[7, 6, 5, 4, 3, 2, 1] → [5, 6, 7, 4, 3, 2, 1]

Step 3 — Reverse remaining 4 elements [4, 3, 2, 1]:
[5, 6, 7, 4, 3, 2, 1] → [5, 6, 7, 1, 2, 3, 4]

Output: [5, 6, 7, 1, 2, 3, 4] ✅
```

## Why This Works — Intuitive Proof

Original: `[A₁ A₂ ... Aₙ₋ₖ | B₁ B₂ ... Bₖ]`

We want: `[B₁ B₂ ... Bₖ | A₁ A₂ ... Aₙ₋ₖ]`

Step 1 — Reverse all: `[Bₖ ... B₂ B₁ | Aₙ₋ₖ ... A₂ A₁]` (both halves are in the right position but internally reversed)

Step 2 — Reverse first k: `[B₁ B₂ ... Bₖ | Aₙ₋ₖ ... A₂ A₁]` (first half fixed)

Step 3 — Reverse last n-k: `[B₁ B₂ ... Bₖ | A₁ A₂ ... Aₙ₋ₖ]` (second half fixed) ✅

## Edge Cases

**Edge case 1: k = 0 (or k = n)**
```
arr = [1, 2, 3], k = 0
k = 0 % 3 = 0
Reverse all: [3, 2, 1]
Reverse first 0: nothing (left=0, right=-1, while fails)
Reverse remaining 3: [1, 2, 3]
Output: [1, 2, 3] ✅ (unchanged)
```

**Edge case 2: k > n**
```
arr = [1, 2], k = 5
k = 5 % 2 = 1
Reverse all: [2, 1]
Reverse first 1: [2, 1] (single element, no change)
Reverse remaining: [2, 1] → [2, 1]... 

Wait, let me retrace:
Reverse all: [2, 1]
Reverse first 1 (index 0 to 0): [2, 1] (single element, unchanged)
Reverse remaining (index 1 to 1): [2, 1] (single element, unchanged)
Output: [2, 1] ✅ (rotate right by 1)
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- `reverse(0, n-1)`: n/2 swaps → O(n)
- `reverse(0, k-1)`: k/2 swaps → O(k)
- `reverse(k, n-1)`: (n-k)/2 swaps → O(n-k)

**STEP 4:** O(n) + O(k) + O(n-k) = O(2n) = **O(n)**

**STEP 5:**
- `left`, `right` pointers → O(1)
- Everything is in-place

> **Time: O(n), Space: O(1)**

---

# Problem 2: Two Sum (Unsorted)

## Pattern Identification

**Pattern: Hash Map for Complement Lookup**

Why? Array is unsorted — can't use two pointers (that needs sorted input). For each element, the complement is `target - num`. A hash map gives O(1) lookup to check if the complement has been seen before and at what index.

## Solution

```python
def two_sum(arr, target):
    seen = {}  # value → index
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## Trace Through Main Example

```
arr = [2, 7, 11, 15], target = 9

i=0, num=2: complement = 9-2 = 7
            7 in {}? NO → seen = {2: 0}

i=1, num=7: complement = 9-7 = 2
            2 in {2: 0}? YES → return [0, 1] ✅
```

## Edge Cases

**Edge case 1: Same value used twice**
```
arr = [3, 3], target = 6
i=0, num=3: comp=3, not in {} → seen={3: 0}
i=1, num=3: comp=3, 3 in {3: 0} → return [0, 1] ✅
(Check before store prevents self-pairing)
```

**Edge case 2: Answer at the end**
```
arr = [1, 5, 8, 2], target = 3
i=0: comp=2, not found. seen={1:0}
i=1: comp=-2, not found. seen={1:0, 5:1}
i=2: comp=-5, not found. seen={1:0, 5:1, 8:2}
i=3: comp=1, 1 in seen → return [0, 3] ✅
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:** Single loop, n iterations, O(1) per iteration (dict ops) → O(n)

**STEP 5:** `seen` → at most n entries → O(n)

> **Time: O(n), Space: O(n)**

---

# Problem 3: Maximum Subarray (Kadane's) With Indices

## Pattern Identification

**Pattern: Kadane's Algorithm (Dynamic Programming / Greedy)**

Why? At each position, the decision is: extend the current subarray, or start fresh. We extend if the running sum is positive (helps), start fresh if it's negative (hurts). To track indices, we maintain the current subarray's start and update the best start/end when we find a new global maximum.

## Solution

```python
def max_subarray(arr):
    max_current = arr[0]
    max_global = arr[0]

    current_start = 0
    best_start = 0
    best_end = 0

    for i in range(1, len(arr)):
        if max_current + arr[i] < arr[i]:
            # Starting fresh is better
            max_current = arr[i]
            current_start = i
        else:
            # Extending is better
            max_current = max_current + arr[i]

        if max_current > max_global:
            max_global = max_current
            best_start = current_start
            best_end = i

    return max_global, best_start, best_end
```

## Why Separate `if/else` Instead of `max()`

Using `max(arr[i], max_current + arr[i])` works for the sum, but we need to know WHICH choice was made to update `current_start`. The explicit if/else lets us reset `current_start = i` exactly when we start fresh.

## Trace Through Main Example

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

max_current=-2, max_global=-2, current_start=0, best=(0,0)

i=1, arr[1]=1:
  -2+1=-1 < 1 → START FRESH. max_current=1, current_start=1
  1 > -2 → max_global=1, best=(1,1)

i=2, arr[2]=-3:
  1+(-3)=-2 ≥ -3 → EXTEND. max_current=-2
  -2 < 1 → no update

i=3, arr[3]=4:
  -2+4=2 < 4 → START FRESH. max_current=4, current_start=3
  4 > 1 → max_global=4, best=(3,3)

i=4, arr[4]=-1:
  4+(-1)=3 ≥ -1 → EXTEND. max_current=3
  3 < 4 → no update

i=5, arr[5]=2:
  3+2=5 ≥ 2 → EXTEND. max_current=5
  5 > 4 → max_global=5, best=(3,5)

i=6, arr[6]=1:
  5+1=6 ≥ 1 → EXTEND. max_current=6
  6 > 5 → max_global=6, best=(3,6)

i=7, arr[7]=-5:
  6+(-5)=1 ≥ -5 → EXTEND. max_current=1
  1 < 6 → no update

i=8, arr[8]=4:
  1+4=5 ≥ 4 → EXTEND. max_current=5
  5 < 6 → no update

return 6, start=3, end=6 ✅
Subarray: arr[3:7] = [4, -1, 2, 1], sum = 6
```

## Edge Cases

**Edge case 1: All negative**
```
arr = [-5, -2, -8]
max_current=-5, max_global=-5, best=(0,0)
i=1: -5+(-2)=-7 < -2 → fresh. max_current=-2, current_start=1
     -2 > -5 → max_global=-2, best=(1,1)
i=2: -2+(-8)=-10 < -8 → fresh. max_current=-8, current_start=2
     -8 < -2 → no update
return -2, start=1, end=1 ✅ (best single element)
```

**Edge case 2: Single element**
```
arr = [42]
Loop doesn't run. return 42, start=0, end=0 ✅
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:** Single loop, n-1 iterations, O(1) per iteration → O(n)

**STEP 5:** Five scalar variables → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 4: Move Zeroes

## Pattern Identification

**Pattern: Two Pointers (Read/Write)**

Why? We need in-place modification maintaining relative order of non-zeros. One pointer (`write`) marks where the next non-zero should go. Another (`read`) scans through the array. Every non-zero element gets placed at the write position, then we fill remaining spots with zeros.

## Solution

```python
def move_zeroes(arr):
    write = 0

    # Pass 1: Move all non-zero elements forward
    for read in range(len(arr)):
        if arr[read] != 0:
            arr[write] = arr[read]
            write += 1

    # Pass 2: Fill remaining positions with zeros
    while write < len(arr):
        arr[write] = 0
        write += 1
```

## Why Two Passes Instead of Swapping

Swapping works too (`arr[write], arr[read] = arr[read], arr[write]`), but the two-pass approach minimizes total operations. In the swap version, if the array starts with many zeros, we do unnecessary swap operations. The two-pass version does exactly `n` assignments total (n-z writes + z zero-fills, where z = number of zeros).

## Trace Through Main Example

```
arr = [0, 1, 0, 3, 12]
write = 0

read=0: arr[0]=0 → skip
read=1: arr[1]=1 ≠ 0 → arr[0]=1, write=1
read=2: arr[2]=0 → skip
read=3: arr[3]=3 ≠ 0 → arr[1]=3, write=2
read=4: arr[4]=12 ≠ 0 → arr[2]=12, write=3

After pass 1: arr = [1, 3, 12, 3, 12], write=3

Pass 2: fill from write=3:
arr[3] = 0, arr[4] = 0

Final: [1, 3, 12, 0, 0] ✅
```

## Edge Cases

**Edge case 1: No zeros**
```
arr = [1, 2, 3]
write moves in lockstep with read, overwriting each position with itself.
Pass 2: write=3, already at end, no zeros filled.
Output: [1, 2, 3] ✅
```

**Edge case 2: All zeros**
```
arr = [0, 0, 0]
Pass 1: nothing written. write stays 0.
Pass 2: fill all 3 positions with 0.
Output: [0, 0, 0] ✅
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- Pass 1: n iterations → O(n)
- Pass 2: at most n iterations (if all zeros) → O(n)

**STEP 4:** O(n) + O(n) = **O(n)**

**STEP 5:** `write`, `read` → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 5: Container With Most Water

## Pattern Identification

**Pattern: Two Pointers — Opposite Ends**

Why? Brute force checks all pairs: O(n²). With pointers at opposite ends, we start with maximum width. Water = min(height[left], height[right]) × (right - left). We move the pointer with the **shorter** height inward, because that's the only way to potentially find a taller line that could increase the area.

## Solution

```python
def max_area(heights):
    left = 0
    right = len(heights) - 1
    best = 0

    while left < right:
        width = right - left
        h = min(heights[left], heights[right])
        area = width * h
        best = max(best, area)

        if heights[left] <= heights[right]:
            left += 1
        else:
            right -= 1

    return best
```

## Proof of Correctness: Why No Optimal Pair Is Skipped

**Claim:** When we move a pointer inward, every pair we skip cannot be the optimal answer.

**Proof:** Suppose `heights[left] ≤ heights[right]`. We move `left` inward. The pairs we skip are (left, right-1), (left, right-2), ..., (left, left+1).

For any skipped pair (left, j) where j < right:
- Width = j - left < right - left (width decreased)
- The limiting height is still ≤ heights[left] (because min(heights[left], heights[j]) ≤ heights[left])
- So area = min(heights[left], heights[j]) × (j - left) ≤ heights[left] × (right - left)

But we already computed heights[left] × (right - left) (actually min(heights[left], heights[right]) × width, and since heights[left] ≤ heights[right], this equals heights[left] × width).

**Every skipped pair has both smaller-or-equal height AND smaller width, so its area CANNOT exceed the current area.** No optimal pair is missed.

**The key insight:** The shorter line is the bottleneck. Keeping it and trying smaller widths can only make things worse. The only hope for improvement is finding a taller line, which requires moving the short pointer.

## Trace Through Main Example

```
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
           0  1  2  3  4  5  6  7  8

left=0, right=8: h=min(1,7)=1, w=8, area=8.  best=8
  heights[0]=1 ≤ heights[8]=7 → left=1

left=1, right=8: h=min(8,7)=7, w=7, area=49. best=49
  heights[1]=8 > heights[8]=7 → right=7

left=1, right=7: h=min(8,3)=3, w=6, area=18. best=49
  heights[1]=8 > heights[7]=3 → right=6

left=1, right=6: h=min(8,8)=8, w=5, area=40. best=49
  heights[1]=8 ≤ heights[6]=8 → left=2

left=2, right=6: h=min(6,8)=6, w=4, area=24. best=49
  heights[2]=6 ≤ heights[6]=8 → left=3

left=3, right=6: h=min(2,8)=2, w=3, area=6.  best=49
  heights[3]=2 ≤ heights[6]=8 → left=4

left=4, right=6: h=min(5,8)=5, w=2, area=10. best=49
  heights[4]=5 ≤ heights[6]=8 → left=5

left=5, right=6: h=min(4,8)=4, w=1, area=4.  best=49
  heights[5]=4 ≤ heights[6]=8 → left=6

left=6, right=6: not left < right → stop

return 49 ✅ (lines at indices 1 and 8, heights 8 and 7, width 7)
```

## Edge Cases

**Edge case 1: Two elements**
```
heights = [1, 1]
left=0, right=1: area = min(1,1) × 1 = 1. best=1.
Move left (equal, move left). left=1, stop.
return 1 ✅
```

**Edge case 2: Ascending array**
```
heights = [1, 2, 3, 4]
left=0, right=3: min(1,4)×3=3. best=3. left=1
left=1, right=3: min(2,4)×2=4. best=4. left=2
left=2, right=3: min(3,4)×1=3. best=4. left=3. Stop.
return 4 ✅
```

## Complexity Analysis

**STEP 1:** `heights` → n = len(heights)

**STEP 3:** Each iteration either left moves right or right moves left. They start n-1 apart, converge → at most n-1 iterations. O(1) per iteration. → **O(n)**

**STEP 5:** `left`, `right`, `best`, `width`, `h`, `area` → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 6: Longest Substring Without Repeating Characters

## Pattern Identification

**Pattern: Variable Sliding Window + Hash Map**

Why? "Longest substring" with a uniqueness constraint. Expand right to grow the window, contract left when a duplicate enters. A hash map tracks each character's most recent index, enabling O(1) jump of the left pointer directly past the duplicate.

## Solution

```python
def length_of_longest_substring(s):
    seen = {}       # char → most recent index
    left = 0
    max_len = 0

    for right in range(len(s)):
        char = s[right]
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

## Why `seen[char] >= left`

The character might exist in `seen` from a position **before** the current window. If `seen['a'] = 2` but `left = 5`, that 'a' is no longer in our window. We only react to duplicates **within** the current window.

## Trace Through Main Example

```
s = "abcabcbb"
seen = {}, left = 0, max_len = 0

right=0, 'a': not in seen → seen={'a':0}, len=1, max=1
right=1, 'b': not in seen → seen={'a':0,'b':1}, len=2, max=2
right=2, 'c': not in seen → seen={'a':0,'b':1,'c':2}, len=3, max=3
right=3, 'a': in seen, seen['a']=0 ≥ left=0 → left=1
              seen={'a':3,'b':1,'c':2}, len=3-1+1=3, max=3
right=4, 'b': in seen, seen['b']=1 ≥ left=1 → left=2
              seen={'a':3,'b':4,'c':2}, len=4-2+1=3, max=3
right=5, 'c': in seen, seen['c']=2 ≥ left=2 → left=3
              seen={'a':3,'b':4,'c':5}, len=5-3+1=3, max=3
right=6, 'b': in seen, seen['b']=4 ≥ left=3 → left=5
              seen={'a':3,'b':6,'c':5}, len=6-5+1=2, max=3
right=7, 'b': in seen, seen['b']=6 ≥ left=5 → left=7
              seen={'a':3,'b':7,'c':5}, len=7-7+1=1, max=3

return 3 ✅
```

## Edge Cases

**Edge case 1: Empty string**
```
s = ""
Loop doesn't run → return 0 ✅
```

**Edge case 2: All unique characters**
```
s = "abcde"
Window just grows. Never contracts. max_len = 5 ✅
```

## Complexity Analysis

**STEP 1:** `s` → n = len(s)

**STEP 3:** Single pass, n iterations, O(1) per iteration (dict ops) → O(n). Left pointer only moves forward → no repeated work.

**STEP 5:** `seen` → at most min(n, charset_size) entries. For ASCII: O(128) = O(1). → **O(min(n, m))**

> **Time: O(n), Space: O(min(n, m))** where m = charset size
> Practically: **O(n) time, O(1) space**

---

# Problem 7: Find All Anagrams in a String

## Pattern Identification

**Pattern: Fixed Sliding Window + Frequency Count**

Why? An anagram = same character frequencies. We slide a window of size len(p) across s, maintaining a frequency map. Instead of comparing entire maps each time (O(26)), we track a `matches` counter that counts how many of the 26 characters currently have equal frequencies — enabling O(1) validity checks.

## Solution

```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []

    p_count = {}
    w_count = {}
    result = []

    for char in p:
        p_count[char] = p_count.get(char, 0) + 1

    # Build first window
    for i in range(len(p)):
        char = s[i]
        w_count[char] = w_count.get(char, 0) + 1

    if w_count == p_count:
        result.append(0)

    # Slide
    for i in range(len(p), len(s)):
        # Add entering character
        add = s[i]
        w_count[add] = w_count.get(add, 0) + 1

        # Remove leaving character
        rem = s[i - len(p)]
        w_count[rem] -= 1
        if w_count[rem] == 0:
            del w_count[rem]

        if w_count == p_count:
            result.append(i - len(p) + 1)

    return result
```

## Trace Through Main Example

```
s = "cbaebabacd", p = "abc"
p_count = {'a':1, 'b':1, 'c':1}

First window s[0..2] = "cba":
w_count = {'c':1, 'b':1, 'a':1} == p_count → result = [0]

i=3: add 'e', remove 'c'
  w_count = {'b':1, 'a':1, 'e':1} ≠ p_count

i=4: add 'b', remove 'b'
  w_count = {'b':1, 'a':1, 'e':1} ≠ p_count

i=5: add 'a', remove 'a'
  w_count = {'b':1, 'a':1, 'e':1} ≠ p_count

i=6: add 'b', remove 'e'
  w_count = {'b':2, 'a':1} ≠ p_count

i=7: add 'a', remove 'b'
  w_count = {'b':1, 'a':2} ≠ p_count

i=8: add 'c', remove 'a'
  w_count = {'b':1, 'a':1, 'c':1} == p_count → result.append(8-3+1=6)

i=9: add 'd', remove 'b'
  w_count = {'a':1, 'c':1, 'd':1} ≠ p_count

return [0, 6] ✅
```

## Edge Cases

**Edge case 1: p longer than s**
```
s = "ab", p = "abc" → guard returns [] ✅
```

**Edge case 2: Entire string is one anagram**
```
s = "cba", p = "abc"
First window matches → result = [0]. No sliding. return [0] ✅
```

## Complexity Analysis

**STEP 1:** `s` → n = len(s), `p` → k = len(p)

**STEP 3:**
- Build p_count: O(k)
- Build first window: O(k)
- Sliding: (n-k) iterations, O(1) per iteration for dict ops, O(26)=O(1) for dict comparison
- Total: **O(n)**

**STEP 5:** `p_count`, `w_count` → at most 26 keys each → O(1). `result` → at most O(n) entries.

> **Time: O(n), Space: O(n)** (output), **O(1)** auxiliary

---

# Problem 8: Trapping Rain Water

## Pattern Identification

**Pattern: Two Pointers — Opposite Ends**

Why? Water at each position = min(max_left, max_right) - height[i]. We could precompute max_left and max_right arrays (O(n) space), but two pointers achieve O(1) space. The insight: we process from whichever side has the shorter maximum, because that side is the bottleneck.

## Solution

```python
def trap(height):
    if len(height) < 3:
        return 0

    left = 0
    right = len(height) - 1
    left_max = height[left]
    right_max = height[right]
    water = 0

    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water
```

## Proof of Correctness: Why This Works

**Key invariant:** When `left_max <= right_max`, the water at position `left` is determined by `left_max`, regardless of what's on the right.

**Why?** Water at any position = `min(max_left, max_right) - height[pos]`.

When we process the left pointer with `left_max <= right_max`:
- `left_max` is the true maximum from the left edge to position `left`
- `right_max` is the maximum we've seen from the right edge so far, but the TRUE maximum to the right of `left` might be even taller (we haven't scanned everything)
- **But it doesn't matter!** We know `right_max` exists somewhere to the right, and the true right maximum ≥ `right_max` ≥ `left_max`
- So `min(true_left_max, true_right_max) = left_max` guaranteed
- Water at this position = `left_max - height[left]` — exactly what we compute

The same logic applies symmetrically when `right_max < left_max`.

**No position is miscounted because whichever side is the bottleneck is always known with certainty when we process it.**

## Trace Through Main Example

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
          0  1  2  3  4  5  6  7  8  9 10 11

left=0, right=11, left_max=0, right_max=1, water=0

left_max(0) ≤ right_max(1):
  left=1, left_max=max(0,1)=1, water+=1-1=0. water=0

left_max(1) ≤ right_max(1):
  left=2, left_max=max(1,0)=1, water+=1-0=1. water=1

left_max(1) ≤ right_max(1):
  left=3, left_max=max(1,2)=2, water+=2-2=0. water=1

right_max(1) < left_max(2):
  right=10, right_max=max(1,2)=2, water+=2-2=0. water=1

left_max(2) ≤ right_max(2):
  left=4, left_max=max(2,1)=2, water+=2-1=1. water=2

left_max(2) ≤ right_max(2):
  left=5, left_max=max(2,0)=2, water+=2-0=2. water=4

left_max(2) ≤ right_max(2):
  left=6, left_max=max(2,1)=2, water+=2-1=1. water=5

left_max(2) ≤ right_max(2):
  left=7, left_max=max(2,3)=3, water+=3-3=0. water=5

right_max(2) < left_max(3):
  right=9, right_max=max(2,1)=2, water+=2-1=1. water=6

right_max(2) < left_max(3):
  right=8, right_max=max(2,2)=2, water+=2-2=0. water=6

right_max(2) < left_max(3):
  right=7. left=7, right=7 → not left<right → stop.

return 6 ✅
```

## Edge Cases

**Edge case 1: Flat surface**
```
height = [1, 1, 1]
left=0, right=2. left_max=1, right_max=1.
left_max ≤ right_max: left=1, left_max=1, water+=1-1=0.
left=1, right=2: not left<right... wait, 1<2.
left_max(1) ≤ right_max(1): left=2. left=2, right=2, stop.
return 0 ✅ (no dips to hold water)
```

**Edge case 2: Single valley**
```
height = [3, 0, 3]
left=0, right=2. left_max=3, right_max=3.
left_max ≤ right_max: left=1, left_max=max(3,0)=3, water+=3-0=3.
left=1, right=2. left_max(3) > right_max(3)? No, equal.
left_max ≤ right_max: left=2. Stop.
return 3 ✅
```

## Complexity Analysis

**STEP 1:** `height` → n = len(height)

**STEP 3:** Each iteration moves left or right. They start n-1 apart, converge → n-1 iterations. O(1) per iteration. → **O(n)**

**STEP 5:** `left`, `right`, `left_max`, `right_max`, `water` → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 9: Rotate Image

## Pattern Identification

**Pattern: Transpose + Reverse Rows**

Why? 90° clockwise rotation decomposes into two simple in-place operations:
1. Transpose (swap `matrix[i][j]` with `matrix[j][i]`)
2. Reverse each row

Both are O(n²) in-place, no extra matrix needed.

## Solution

```python
def rotate(matrix):
    n = len(matrix)

    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

## Trace Through Main Example

```
Original:
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]

Step 1 — Transpose:
  swap(0,1)↔(1,0): 2↔4
  swap(0,2)↔(2,0): 3↔7
  swap(1,2)↔(2,1): 6↔8

[[1, 4, 7],
 [2, 5, 8],
 [3, 6, 9]]

Step 2 — Reverse each row:
  [1,4,7] → [7,4,1]
  [2,5,8] → [8,5,2]
  [3,6,9] → [9,6,3]

[[7, 4, 1],
 [8, 5, 2],
 [9, 6, 3]] ✅
```

## Edge Cases

**Edge case 1: 1×1 matrix**
```
[[5]]
Transpose: inner loop range(1,1) → nothing.
Reverse: [5] → [5].
Output: [[5]] ✅
```

**Edge case 2: 2×2 matrix**
```
[[1,2],[3,4]]
Transpose: swap(0,1)↔(1,0): 2↔3 → [[1,3],[2,4]]
Reverse rows: [3,1],[4,2] → [[3,1],[4,2]]
✅ (90° clockwise of [[1,2],[3,4]])
```

## Complexity Analysis

**STEP 1:** `matrix` → n×n, n = number of rows

**STEP 3:**
- Transpose: n(n-1)/2 swaps → O(n²)
- Reverse: n rows × O(n) each → O(n²)

**STEP 4:** O(n²) + O(n²) = **O(n²)**

**STEP 5:** Swap uses temp variable → O(1). `row.reverse()` in-place → O(1). All in-place.

> **Time: O(n²), Space: O(1)**

O(n²) is optimal — must touch all n² cells at least once.

---

# Problem 10: Minimum Window Substring

## Pattern Identification

**Pattern: Variable Sliding Window (Expand/Contract) + Frequency Tracking with Formed Counter**

Why? We need the smallest window in `s` containing all of `t`'s characters. Expand right until valid, contract left to minimize while still valid. A `formed` counter tracks how many character requirements are fully satisfied, enabling O(1) validity checks instead of O(26) dict comparisons.

## Solution

```python
def min_window(s, t):
    if not t or not s:
        return ""

    t_count = {}
    for char in t:
        t_count[char] = t_count.get(char, 0) + 1

    required = len(t_count)
    formed = 0
    w_count = {}

    min_len = float('inf')
    min_start = 0
    left = 0

    for right in range(len(s)):
        # Expand
        char = s[right]
        w_count[char] = w_count.get(char, 0) + 1

        if char in t_count and w_count[char] == t_count[char]:
            formed += 1

        # Contract
        while formed == required:
            window_size = right - left + 1
            if window_size < min_len:
                min_len = window_size
                min_start = left

            left_char = s[left]
            w_count[left_char] -= 1
            if left_char in t_count and w_count[left_char] < t_count[left_char]:
                formed -= 1
            left += 1

    return "" if min_len == float('inf') else s[min_start:min_start + min_len]
```

## Why `formed` Instead of Dict Comparison

If we compared `w_count` vs `t_count` every time, that's O(unique chars in t) per check. With `formed`, we only increment/decrement when a character's count **crosses the threshold** — exactly equals or drops below. This makes each check O(1).

## Trace Through Main Example

```
s = "ADOBECODEBANC", t = "ABC"
t_count = {'A':1, 'B':1, 'C':1}, required = 3

left=0, formed=0

right=0 'A': w={'A':1}, A meets req → formed=1
right=1 'D': w={'A':1,'D':1}
right=2 'O': w={...'O':1}
right=3 'B': w={...'B':1}, B meets req → formed=2
right=4 'E': w={...'E':1}
right=5 'C': w={...'C':1}, C meets req → formed=3 ✓

  Contract: window "ADOBEC" len=6, min_len=6, min_start=0
  Remove 'A': w['A']=0 < 1 → formed=2. left=1. Stop.

right=6 'O': formed=2
right=7 'D': formed=2
right=8 'E': formed=2
right=9 'B': w['B']=2, 2≠1 so no formed change
right=10 'A': w['A']=1, meets req → formed=3 ✓

  Contract from left=1:
  Remove 'D': not in t_count. left=2. len=10-2+1=9 > 6.
  Remove 'O': not in t_count. left=3. len=8 > 6.
  Remove 'B': w['B']=1, still ≥1, formed stays 3. left=4. len=7 > 6.
  Remove 'E': not in t_count. left=5. len=6. Equals min, no update.
  Remove 'C': w['C']=0 < 1 → formed=2. left=6. Stop.

right=11 'N': formed=2
right=12 'C': w['C']=1, meets req → formed=3 ✓

  Contract from left=6:
  Remove 'O': not in t. left=7. len=12-7+1=6. Equals min.
  Remove 'D': not in t. left=8. len=5. 5<6! min_len=5, min_start=8.
  Remove 'E': not in t. left=9. len=4. 4<5! min_len=4, min_start=9.
  Remove 'B': w['B']=0 < 1 → formed=2. left=10. Stop.

return s[9:13] = "BANC" ✅
```

## Edge Cases

**Edge case 1: No valid window**
```
s = "abc", t = "z"
Right scans entire string, formed never reaches required.
min_len stays inf → return "" ✅
```

**Edge case 2: t has duplicate characters**
```
s = "aa", t = "aa"
t_count = {'a': 2}, required = 1
right=0: w['a']=1, 1≠2. formed=0
right=1: w['a']=2, 2==2 → formed=1 ✓
  Contract: window "aa" len=2. min=2.
  Remove s[0]='a': w['a']=1 < 2 → formed=0. Stop.
return "aa" ✅
```

## Complexity Analysis

**STEP 1:** `s` → n = len(s), `t` → m = len(t)

**STEP 3:**
- Build t_count: O(m)
- `right` pointer: n iterations
- `left` pointer: total moves across all iterations ≤ n (only moves forward, never resets)
- Each operation: O(1) (dict ops, formed counter)
- Total: **O(n + m)**

**STEP 5:**
- `t_count` → at most min(m, 26) keys → O(1) for bounded alphabet
- `w_count` → at most 26 keys → O(1)
- Scalar variables → O(1)
- Final slice → O(min_len) for output

> **Time: O(n + m), Space: O(1)** with bounded alphabet
> More precisely: **O(n + m) time, O(m) space**
