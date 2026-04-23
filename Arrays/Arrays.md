# Scope Updated: Bitwise Operations Added

Adding as **Part 8: Bitwise Operations on Arrays** covering:
- Binary representation fundamentals
- AND, OR, XOR, NOT, Left Shift, Right Shift — what each does and why it exists
- XOR properties and tricks (single number, swap without temp, missing number)
- Bit masking (check, set, clear, toggle specific bits)
- Practical applications: even/odd check, power-of-2 check, counting set bits
- Interview problems that require bitwise thinking
- When bitwise is the RIGHT approach vs overkill

Now let's go.

---

# ARRAYS & STRINGS — THE COMPLETE LESSON

---

# PART 1: HOW ARRAYS ACTUALLY WORK

## Why You Need To Know This

Most courses say "an array stores elements" and move on. That's like saying "a car has wheels." It tells you nothing about **why** certain operations are fast, why others are slow, and **when** to choose an array over something else.

If you understand how arrays work at the memory level, you'll **intuitively** know:
- Why `arr[i]` is O(1) instead of having to memorize it
- Why inserting at the front is O(n) instead of having to memorize it
- Why arrays beat linked lists in practice even when Big O says they're the same
- How to make smart data structure choices in system design

---

## 1A: Memory Layout — What Contiguous Means

Your computer's memory (RAM) is like a massive row of numbered mailboxes. Each mailbox holds a small piece of data. Each mailbox has an **address** (a number).

```
Address:  1000  1001  1002  1003  1004  1005  1006  1007
Content:  [  ]  [  ]  [  ]  [  ]  [  ]  [  ]  [  ]  [  ]
```

When you create an array of 4 integers, the computer reserves **consecutive** (contiguous) mailboxes:

```
Address:  1000  1001  1002  1003
Content:  [ 10] [ 20] [ 30] [ 40]
```

The array knows:
- **Base address:** 1000 (where it starts)
- **Element size:** each integer takes 1 slot (simplified — real integers take 4 or 8 bytes)
- **Length:** 4

### Why Index Access Is O(1)

To find `arr[2]`, the computer does **one calculation:**

```
address of arr[2] = base_address + (index × element_size)
                  = 1000 + (2 × 1)
                  = 1002
```

Go directly to mailbox 1002. Read the value. **Done.** No scanning. No searching. Just arithmetic.

This works for `arr[0]`, `arr[999999]`, or `arr[any_number]`. One calculation, one memory access. That's why it's O(1). It doesn't matter how large the array is.

### Why Insertion At Front Is O(n)

You want to insert `5` at position 0 of `[10, 20, 30, 40]`:

```
Before:  [10] [20] [30] [40] [  ]
Step 1:  [10] [20] [30] [  ] [40]  ← move 40 right
Step 2:  [10] [20] [  ] [30] [40]  ← move 30 right
Step 3:  [10] [  ] [20] [30] [40]  ← move 20 right
Step 4:  [  ] [10] [20] [30] [40]  ← move 10 right
Step 5:  [ 5] [10] [20] [30] [40]  ← insert 5
```

**Every single element had to shift.** For n elements, that's n shifts. O(n). This is why `list.insert(0, x)` is O(n) in Python. The elements are contiguous — you can't just squeeze something in. Everything after the insertion point must move.

### Cache Locality — The Hidden Performance Advantage

Your CPU has a **cache** — a tiny, extremely fast memory right next to the processor. When you access `arr[0]`, the CPU doesn't just fetch that one element. It fetches a **chunk** of nearby memory into the cache.

Because array elements are **contiguous**, fetching `arr[0]` also pulls `arr[1]`, `arr[2]`, `arr[3]`... into the cache for free. When you access them next, they're already there. Blazingly fast.

A linked list has elements scattered **randomly** in memory. Each access is a cache miss — the CPU has to go all the way to RAM. This is why arrays are faster **in practice** than linked lists for sequential access, even though both are O(n) for traversal.

**When does this matter?**
- System design: choosing between array-based vs pointer-based structures for high-throughput systems
- CP: tight time limits where constant factors matter
- Interviews: if asked "why would you use an array here instead of a linked list?"

---

## 1B: Python Lists — The Truth

Python lists are **NOT** traditional arrays. They're **dynamic arrays of pointers.**

```
Python list: [10, "hello", True, 3.14]
```

In memory:

```
List object stores:
  - Array of POINTERS (references):
    [ptr_0] [ptr_1] [ptr_2] [ptr_3]
       ↓       ↓       ↓       ↓
     [10]  ["hello"] [True]  [3.14]
     (somewhere in memory, scattered)
```

The list itself is a contiguous array of **pointers.** Each pointer points to the actual object, which can be **anywhere** in memory.

**Consequences:**
- Index access is still O(1) — the pointer array is contiguous, so calculating pointer position is instant. Following the pointer to the object is one more step, but still O(1).
- You can mix types (int, string, bool) because the list just stores pointers, and each pointer can point to any type.
- Less cache-friendly than C arrays because the actual data is scattered.
- Each element has overhead (the pointer itself + the object's metadata).

**For interviews:** This rarely comes up directly. But knowing it shows depth. If an interviewer asks "how does a Python list work internally?" this answer impresses.

**For system design:** This is why Python isn't used for latency-critical systems. The indirection and memory overhead matter at scale.

---

## 1C: Static vs Dynamic Arrays

**Static Array:** Fixed size. Decided at creation. Cannot grow.

```python
# Python simulation of static array
arr = [0] * 10  # Fixed 10 slots. Conceptually "static."
```

**Dynamic Array:** Grows as needed. Python lists are dynamic.

```python
arr = []
arr.append(1)  # Grows
arr.append(2)  # Grows
arr.append(3)  # Grows
```

**How dynamic arrays grow:**

1. Start with small internal capacity (say 4 slots)
2. As you append, fill up slots
3. When full, allocate a **new array of ~2× the size**
4. Copy everything over
5. Continue

```
Capacity 4:   [1] [2] [3] [4]  ← FULL
Resize to 8:  [1] [2] [3] [4] [ ] [ ] [ ] [ ]  ← copied, now room
Append:       [1] [2] [3] [4] [5] [ ] [ ] [ ]
```

This is why append is **amortized O(1)** — most appends are O(1), but occasionally you pay O(n) for the copy. Averaged out, it's O(1) per append.

**When to pre-allocate:**

```python
# SLOW — grows dynamically, many resizes for large n
result = []
for i in range(1000000):
    result.append(0)

# FASTER — one allocation, no resizing
result = [0] * 1000000
```

Pre-allocating with `[0] * n` is faster when you know the size upfront. Use it when building a result array of known size (like prefix sums, DP tables, etc.).

---

## 1D: When Arrays Are The WRONG Choice

This is a **decision framework.** Before reaching for an array, ask these questions:

| Need | Array? | Better Choice | Why |
|---|---|---|---|
| Access element by index | ✅ Yes — O(1) | — | Arrays are built for this |
| Search for a specific value | ❌ Slow — O(n) | **Hash Set** — O(1) | Unsorted array requires full scan |
| Check if element exists | ❌ Slow — O(n) | **Hash Set** — O(1) | `x in list` is O(n), `x in set` is O(1) |
| Insert/delete at front | ❌ Slow — O(n) | **Deque** — O(1) | Shifting elements is expensive |
| Insert/delete at arbitrary position | ❌ Slow — O(n) | **Linked List** — O(1) if you have the node | Shifting required for arrays |
| Always need min or max | ❌ Slow — O(n) each time | **Heap** — O(log n) | Heap maintains order efficiently |
| Key-value lookup | ❌ Wrong structure | **Hash Map** — O(1) | Arrays don't map keys to values |
| Maintain sorted order with frequent inserts | ❌ Slow — O(n) per insert | **BST / SortedList** | Inserting into sorted array requires shifting |
| Sequential access / iteration | ✅ Yes — cache-friendly | — | Contiguous memory = fast traversal |

**The rule:** Arrays are excellent for **indexed access, sequential processing, and fixed collections.** They are poor for **searching, membership testing, and frequent insertion/deletion.**

---

## 1E: Strings as Arrays

In Python, a string is a **sequence of characters.** You can index it, slice it, iterate over it — just like an array.

```python
s = "hello"
s[0]      # 'h' — O(1)
s[1:3]    # 'el' — O(k) where k = slice length
len(s)    # 5 — O(1)
for c in s:  # iterates character by character — O(n)
    print(c)
```

### The Critical Difference: Immutability

```python
# Arrays (lists) are MUTABLE — you can change elements
arr = [1, 2, 3]
arr[0] = 99  # ✅ Works. arr is now [99, 2, 3]

# Strings are IMMUTABLE — you CANNOT change characters
s = "hello"
s[0] = "H"  # ❌ TypeError! Strings cannot be modified.
```

**Every "modification" to a string creates an entirely new string.**

```python
s = "hello"
s = s + " world"  # Creates brand new string "hello world"
                    # The old "hello" is abandoned in memory
```

### The Consequences You Must Internalize

**Consequence 1: Loop concatenation is O(n²)**

```python
# ❌ O(n²) — creates new string EACH iteration
result = ""
for word in words:
    result = result + word
# Iteration 1: copy 1 word
# Iteration 2: copy 2 words
# Iteration n: copy n words
# Total: 1 + 2 + ... + n = O(n²)
```

```python
# ✅ O(n) — builds list, joins once
result = "".join(words)
```

**Consequence 2: When you need to "modify" a string character by character, convert to list first**

```python
# Task: change 'hello' to 'Hello'

# ❌ Can't do s[0] = 'H' because immutable

# ✅ Convert to list, modify, convert back
chars = list(s)        # ['h', 'e', 'l', 'l', 'o'] — O(n)
chars[0] = 'H'         # O(1) — lists are mutable
s = "".join(chars)     # "Hello" — O(n)
```

Total: O(n). This is the standard pattern for character-level string manipulation in Python.

**Consequence 3: String slicing creates a copy**

```python
s = "hello world"
sub = s[0:5]  # "hello" — creates NEW string, O(5)
```

This means if you slice inside a loop, you're creating copies each time. Be aware of the cost.

### String Methods and Their Costs

```
METHOD                     TIME           WHAT IT DOES
──────────────────────────────────────────────────────
s.startswith(prefix)       O(p)           Checks first p characters
s.endswith(suffix)         O(p)           Checks last p characters
s.find(sub)                O(n × m)       Finds substring (n=len(s), m=len(sub))
s.replace(old, new)        O(n)           Creates new string with replacements
s.split(delimiter)         O(n)           Creates list of substrings
s.strip()                  O(n)           Creates new string without whitespace
s.lower() / s.upper()      O(n)           Creates new string with case change
s.isalpha() / s.isdigit()  O(n)           Checks every character
s.count(sub)               O(n)           Counts occurrences
"".join(list)              O(total)       Total length of all strings in list
chr(num) / ord(char)       O(1)           Convert between character and ASCII
```

**The critical tools you'll use constantly:**
- `ord(char)` — converts character to its ASCII number. `ord('a')` = 97
- `chr(num)` — converts number to character. `chr(97)` = 'a'
- Useful for: frequency counting, character math, mapping characters to indices

```python
# Using ord() to map characters to array indices
# 'a' → 0, 'b' → 1, ..., 'z' → 25
index = ord(char) - ord('a')
```

---

# PART 2: CORE ARRAY OPERATIONS & MANIPULATION

## 2A: Traversal Patterns

These seem basic. They're not. Knowing **which** traversal pattern to use is often the key to solving a problem.

### Forward Traversal

```python
# By index
for i in range(len(arr)):
    print(i, arr[i])

# By value
for num in arr:
    print(num)

# By both (PREFERRED in Python — cleaner, no index errors)
for i, num in enumerate(arr):
    print(i, num)
```

**When to use which:**
- Need index AND value → `enumerate`
- Need only value → `for num in arr`
- Need to modify in-place → `for i in range(len(arr))` (because you need the index to assign: `arr[i] = new_val`)

### Backward Traversal

```python
# By index
for i in range(len(arr) - 1, -1, -1):
    print(i, arr[i])

# By value (reversed)
for num in reversed(arr):
    print(num)
```

**When to use:** Problems that require processing from end to start — next greater element, suffix operations, certain DP problems.

### Simultaneous Traversal

```python
# Two arrays of SAME length
for a, b in zip(arr1, arr2):
    print(a, b)

# Two arrays — need indices too
for i, (a, b) in enumerate(zip(arr1, arr2)):
    print(i, a, b)
```

**When to use:** Comparing two arrays element by element, dot product, merging parallel data.

### Skip Traversal

```python
# Every other element
for i in range(0, len(arr), 2):
    print(arr[i])

# Every kth element
for i in range(0, len(arr), k):
    print(arr[i])
```

---

## 2B: In-Place Manipulation

**In-place** means modifying the original array without creating a new one. O(1) extra space. Interviewers love asking for in-place solutions.

### The Fundamental Operation: Swap

```python
# Python makes this elegant
arr[i], arr[j] = arr[j], arr[i]
```

This is O(1). It's the building block of almost every in-place algorithm.

### Reverse an Array In-Place

```python
def reverse(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

Time: O(n). Space: O(1). This is the **converging two-pointer** pattern.

Trace with `[1, 2, 3, 4, 5]`:
```
left=0, right=4: swap(1,5) → [5, 2, 3, 4, 1]
left=1, right=3: swap(2,4) → [5, 4, 3, 2, 1]
left=2, right=2: left not < right → stop
Result: [5, 4, 3, 2, 1] ✅
```

### Rotate an Array

**Problem:** Rotate `[1, 2, 3, 4, 5]` right by 2 → `[4, 5, 1, 2, 3]`

**Approach 1: Brute Force** — Rotate by 1, k times. O(n × k) time, O(1) space.

**Approach 2: Extra Array** — Copy elements to correct positions. O(n) time, O(n) space.

```python
def rotate_extra(arr, k):
    n = len(arr)
    k = k % n  # Handle k > n
    result = [0] * n
    for i in range(n):
        result[(i + k) % n] = arr[i]
    return result
```

**Approach 3: Three Reversals** — O(n) time, O(1) space. The elegant solution.

```python
def rotate_in_place(arr, k):
    n = len(arr)
    k = k % n

    def reverse(left, right):
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    reverse(0, n - 1)      # Reverse entire array
    reverse(0, k - 1)      # Reverse first k elements
    reverse(k, n - 1)      # Reverse remaining elements
```

Trace with `[1, 2, 3, 4, 5]`, k = 2:
```
Step 1 — reverse all:     [5, 4, 3, 2, 1]
Step 2 — reverse [0:1]:   [4, 5, 3, 2, 1]
Step 3 — reverse [2:4]:   [4, 5, 1, 2, 3] ✅
```

**Why does this work?** Think of it as: the last k elements need to come to the front. Reversing the whole array puts them at the front but in wrong internal order. The two sub-reversals fix the internal ordering.

**This problem demonstrates a crucial interview skill:** showing multiple approaches with different time/space tradeoffs. Present Approach 1 as brute force, mention Approach 2 as the time-optimal-but-uses-space solution, then deliver Approach 3 as the optimal in-place solution.

### Removing Elements In-Place (The Write Pointer Technique)

**Problem:** Remove all occurrences of `val` from `arr` in-place. Return the new length.

```python
def remove_element(arr, val):
    write = 0
    for read in range(len(arr)):
        if arr[read] != val:
            arr[write] = arr[read]
            write += 1
    return write
```

Trace with `arr = [3, 2, 2, 3], val = 3`:
```
read=0: arr[0]=3, equals val → skip
read=1: arr[1]=2, keep → arr[0]=2, write=1
read=2: arr[2]=2, keep → arr[1]=2, write=2
read=3: arr[3]=3, equals val → skip
Result: arr = [2, 2, ...], write = 2
```

**The pattern:** Two pointers — `read` scans every element, `write` only advances when we keep an element. Everything before `write` is the "cleaned" array.

Time: O(n). Space: O(1). This technique appears in **many** interview problems: remove duplicates, partition arrays, filter by condition.

---

## 2C: Subarray vs Subsequence vs Subset

These three terms describe different types of selections from an array. **Confusing them is a fatal interview error.** They lead to completely different problem families and techniques.

### Subarray (Contiguous)

A subarray is a **contiguous** slice of the array. Elements must be adjacent.

```
Array: [1, 2, 3, 4]

Subarrays:
[1], [2], [3], [4]
[1,2], [2,3], [3,4]
[1,2,3], [2,3,4]
[1,2,3,4]
```

**How many subarrays of length n?**
- Subarrays of length 1: n choices
- Subarrays of length 2: n-1 choices
- ...
- Subarrays of length n: 1 choice
- Total: n + (n-1) + ... + 1 = **n(n+1)/2 → O(n²)**

**Techniques for subarray problems:** Sliding window, prefix sums, Kadane's, two pointers.

### Subsequence (Ordered, Not Necessarily Contiguous)

A subsequence maintains the **relative order** but elements don't have to be adjacent.

```
Array: [1, 2, 3, 4]

Some subsequences:
[1], [2], [1,3], [1,4], [2,4], [1,3,4], [1,2,3,4]

NOT a subsequence:
[3, 1]  ← wrong order
```

**How many subsequences?** Each element is either included or not. 2 choices per element. **2ⁿ subsequences.**

**Techniques for subsequence problems:** Dynamic programming, recursion/backtracking.

### Subset (Unordered, Any Elements)

A subset is any collection of elements **regardless of order.**

```
Array: [1, 2, 3]

All subsets:
{}, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}
```

**How many subsets?** Same as subsequences: **2ⁿ.** (The difference is purely conceptual — subsets don't care about order.)

**Techniques for subset problems:** Backtracking, bit manipulation (each subset maps to a binary number).

### The Interview Decision

When you see a problem, **immediately classify it:**

| Problem Says | What It Means | Likely Technique |
|---|---|---|
| "contiguous subarray" | Subarray | Sliding window, prefix sums, Kadane's |
| "subarray of size k" | Fixed-size subarray | Fixed sliding window |
| "subsequence" | Ordered, gaps allowed | DP |
| "subset" / "combination" | Unordered selection | Backtracking, bit manipulation |
| "permutation" | Ordered arrangement of ALL elements | Backtracking |

---

# PART 3: THE FIVE CORE PATTERNS

This is the heart of array/string problem-solving. Each pattern is a **tool.** I'll teach you:
1. What the tool does
2. When to reach for it
3. The mechanical framework
4. Edge cases where it breaks

---

## Pattern 1: Two Pointers

### Why It Exists

Many array problems ask you to find pairs, compare elements from different positions, or process from both ends. The brute force is usually O(n²) — check every pair. Two pointers reduces this to **O(n)** by using the array's structure (often sorted order) to eliminate impossible pairs without checking them.

### Variant A: Converging (Opposite Direction)

**Setup:** One pointer at start, one at end. They move toward each other.

**The Framework:**

```python
def converging_two_pointers(arr):
    left = 0
    right = len(arr) - 1

    while left < right:
        # 1. Examine arr[left] and arr[right]
        # 2. Based on some condition:
        #    - Move left forward (left += 1)
        #    - Move right backward (right -= 1)
        #    - Or both
        pass
```

**When to use:**
- Array is **sorted** and you're looking for a pair with some property
- You're checking symmetry (palindromes)
- You need to squeeze toward an optimal answer from both ends

**Classic Example: Two Sum on Sorted Array**

Problem: Given a sorted array and a target sum, find two numbers that add up to the target.

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1      # Need bigger sum → move left forward
        else:
            right -= 1     # Need smaller sum → move right backward

    return []  # No pair found
```

**Why this works (the invariant):**

The array is sorted. If `arr[left] + arr[right] < target`, then `arr[left] + arr[anything_less_than_right]` is also too small. So we can safely skip left — it can't pair with any remaining right pointer positions to reach the target. Similarly for the other direction.

**Each step eliminates an entire row or column of the pair matrix.** That's why it's O(n) instead of O(n²).

Time: O(n). Space: O(1).

**Classic Example: Valid Palindrome**

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric characters
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

Checking symmetry from both ends. If any pair doesn't match, it's not a palindrome.

Time: O(n). Space: O(1).

---

### Variant B: Same Direction (Fast/Slow or Read/Write)

**Setup:** Both pointers start at or near the beginning. One moves faster or conditionally.

**The Framework:**

```python
def same_direction_two_pointers(arr):
    slow = 0

    for fast in range(len(arr)):
        if some_condition(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1

    return slow  # or arr[:slow]
```

**When to use:**
- Removing elements in-place
- Removing duplicates from sorted array
- Partitioning by condition (move all X to front/back)

**Classic Example: Remove Duplicates from Sorted Array**

```python
def remove_duplicates(arr):
    if len(arr) == 0:
        return 0

    write = 0

    for read in range(1, len(arr)):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]

    return write + 1
```

Trace with `[1, 1, 2, 2, 3]`:
```
write=0, read=1: arr[1]=1 == arr[0]=1 → skip
write=0, read=2: arr[2]=2 != arr[0]=1 → write=1, arr[1]=2
write=1, read=3: arr[3]=2 == arr[1]=2 → skip
write=1, read=4: arr[4]=3 != arr[1]=2 → write=2, arr[2]=3
Result: arr = [1, 2, 3, ...], length = 3
```

Time: O(n). Space: O(1).

**Classic Example: Move Zeroes**

Move all zeroes to end, maintaining order of non-zero elements.

```python
def move_zeroes(arr):
    write = 0

    for read in range(len(arr)):
        if arr[read] != 0:
            arr[write] = arr[read]
            write += 1

    # Fill remaining with zeroes
    while write < len(arr):
        arr[write] = 0
        write += 1
```

Same read/write pointer technique. Non-zero elements get compacted to the front, then zeroes fill the rest.

Time: O(n). Space: O(1).

---

### Variant C: Two Arrays, Two Pointers

**Setup:** One pointer per array. Advance based on comparison.

**The Framework:**

```python
def two_array_pointers(arr1, arr2):
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            # Process arr1[i]
            i += 1
        elif arr1[i] > arr2[j]:
            # Process arr2[j]
            j += 1
        else:
            # They're equal — process both
            i += 1
            j += 1

    # Handle remaining elements in whichever array isn't exhausted
```

**When to use:** Both arrays are **sorted.** You need to merge, intersect, or compare them.

**Classic Example: Merge Two Sorted Arrays**

```python
def merge_sorted(arr1, arr2):
    result = []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    # Append remaining
    result.extend(arr1[i:])
    result.extend(arr2[j:])

    return result
```

Time: O(a + b). Space: O(a + b) for the result.

This is the **merge step** of merge sort. You'll see it again in Week 3.

---

### Two Pointer Decision Framework

```
Is the array SORTED?
├── YES → Do you need pairs/triplets that satisfy a condition?
│         ├── YES → Converging two pointers (Variant A)
│         └── NO  → Do you need to merge/compare with another sorted array?
│                   ├── YES → Two-array pointers (Variant C)
│                   └── NO  → Maybe not two pointers
└── NO  → Do you need to remove/filter/partition IN-PLACE?
          ├── YES → Same-direction read/write pointers (Variant B)
          └── NO  → Probably not two pointers. Consider sliding window or hashing.
```

---

## Pattern 2: Sliding Window

### Why It Exists

Many problems ask about **contiguous subarrays** of some size or satisfying some condition. The brute force checks every subarray: O(n²) or O(n²k). Sliding window exploits the fact that adjacent subarrays **overlap** — when you slide the window one position right, you only add one element and remove one element.

### Variant A: Fixed-Size Window

**The problem type:** "Find max/min/average of ALL subarrays of size k."

**Brute Force:**
```python
# O(n × k) — recomputes sum from scratch each time
for i in range(n - k + 1):
    window_sum = sum(arr[i:i+k])
```

**Sliding Window:**
```python
def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k:
        return None

    # Build first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide: add right, remove left
    for i in range(k, n):
        window_sum += arr[i]        # Add new element entering window
        window_sum -= arr[i - k]    # Remove element leaving window
        max_sum = max(max_sum, window_sum)

    return max_sum
```

Trace with `arr = [2, 1, 5, 1, 3, 2]`, k = 3:
```
Initial window [2,1,5]: sum = 8, max = 8
Slide → [1,5,1]: add 1, remove 2 → sum = 7, max = 8
Slide → [5,1,3]: add 3, remove 1 → sum = 9, max = 9
Slide → [1,3,2]: add 2, remove 5 → sum = 6, max = 9
Answer: 9
```

Time: O(n). Space: O(1). Instead of recomputing the sum (O(k) each time), we **update** it in O(1).

### Variant B: Variable-Size Window

**The problem type:** "Find the smallest/longest subarray satisfying some condition."

This is harder. The window can grow and shrink.

**The Framework:**

```python
def variable_sliding_window(arr):
    left = 0
    # Initialize window state (sum, count, frequency map, etc.)

    best_answer = ...  # Initialize based on problem (inf for minimum, 0 for maximum)

    for right in range(len(arr)):
        # EXPAND: Add arr[right] to window state

        # SHRINK: While window is invalid or can be optimized
        while window_is_invalid():
            # Remove arr[left] from window state
            left += 1

        # UPDATE: Check if current window is a better answer
        # Window is arr[left:right+1], size = right - left + 1
        best_answer = update(best_answer, right - left + 1)

    return best_answer
```

**The key insight:** The right pointer expands to explore. The left pointer shrinks to maintain validity. Both only move **forward.** Total pointer movements across the entire algorithm: at most 2n. **O(n) total.**

**Classic Example: Smallest Subarray With Sum ≥ Target**

```python
def min_subarray_len(target, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')

    for right in range(len(arr)):
        # EXPAND
        current_sum += arr[right]

        # SHRINK — while we meet the condition, try to minimize
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1

    return min_length if min_length != float('inf') else 0
```

Trace with `target = 7, arr = [2, 3, 1, 2, 4, 3]`:
```
right=0: sum=2, < 7
right=1: sum=5, < 7
right=2: sum=6, < 7
right=3: sum=8, ≥ 7 → min_len=4, shrink: remove 2→sum=6, left=1
right=4: sum=10, ≥ 7 → min_len=3, shrink: remove 3→sum=7, ≥ 7 → min_len=3, shrink: remove 1→sum=6, left=3
right=5: sum=9, ≥ 7 → min_len=3, shrink: remove 2→sum=7, ≥ 7 → min_len=2, shrink: remove 4→sum=3, left=5
Answer: 2 (subarray [4,3])
```

Time: O(n) — each element is added once and removed once. Space: O(1).

**Classic Example: Longest Substring Without Repeating Characters**

```python
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        # SHRINK — remove characters until no duplicate
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        # EXPAND
        char_set.add(s[right])

        # UPDATE
        max_length = max(max_length, right - left + 1)

    return max_length
```

Time: O(n). Space: O(min(n, alphabet_size)).

### When Sliding Window DOESN'T Work

Sliding window requires a **monotonic relationship** between window size and the condition:

- **Works when:** Expanding the window can only make the condition "more satisfied" (or stay same), and shrinking can only make it "less satisfied" (or stay same). Typically requires **all positive values** for sum-based problems, or a condition based on **counts/frequencies.**
- **Fails when:** Negative numbers are present in sum problems (expanding might decrease the sum, breaking the monotonic assumption). For max subarray sum with negatives, you need **Kadane's**, not sliding window.

---

## Pattern 3: Prefix Sums

### Why It Exists

You frequently need to compute the **sum of a subarray** from index i to j. Without preprocessing, each query takes O(j - i) time. If you have many queries, this becomes expensive.

Prefix sums precompute all cumulative sums so that **any range sum is O(1).**

This is the **precompute + query pattern** from the Big O lesson, applied to arrays.

### How It Works

**Build the prefix sum array:**

```python
def build_prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)  # One extra element at start
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix
```

For `arr = [3, 1, 4, 1, 5]`:

```
arr:    [3, 1, 4, 1, 5]
prefix: [0, 3, 4, 8, 9, 14]
         ↑
         Extra 0 at start makes the formula clean
```

`prefix[i]` = sum of first i elements of arr.

**Query any range sum in O(1):**

```python
def range_sum(prefix, left, right):  # inclusive both ends
    return prefix[right + 1] - prefix[left]
```

`sum(arr[1:4])` = `prefix[4] - prefix[1]` = 9 - 3 = 7. Check: 1 + 4 + 1 = 6. Wait — let me recount.

`arr[1] + arr[2] + arr[3]` = 1 + 4 + 1 = 6.
`prefix[4] - prefix[1]` = 9 - 3 = 6. ✅

**Build: O(n) time, O(n) space. Each query: O(1) time.**

### Classic Application: Subarray Sum Equals K

**Problem:** Count the number of subarrays that sum to exactly k.

**Brute force:** Check every subarray. O(n²) with prefix sums.

**Optimal:** Use a hash map to count prefix sums seen so far.

```python
def subarray_sum(arr, k):
    count = 0
    current_sum = 0
    prefix_counts = {0: 1}  # Empty prefix has sum 0, seen once

    for num in arr:
        current_sum += num

        # If (current_sum - k) was a previous prefix sum,
        # then the subarray between that point and here sums to k
        if current_sum - k in prefix_counts:
            count += prefix_counts[current_sum - k]

        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return count
```

**Why this works:**

If `prefix[j] - prefix[i] = k`, then the subarray from i+1 to j sums to k. So for each j, we look for how many previous prefix sums equal `prefix[j] - k`. The hash map stores these counts.

Time: O(n). Space: O(n).

**This is one of the most common FAANG interview questions.** It combines prefix sums with hashing. Make sure you understand the logic deeply.

### Pivot Index / Equilibrium Point

**Problem:** Find the index where the sum to the left equals the sum to the right.

```python
def pivot_index(arr):
    total = sum(arr)
    left_sum = 0

    for i in range(len(arr)):
        right_sum = total - left_sum - arr[i]
        if left_sum == right_sum:
            return i
        left_sum += arr[i]

    return -1
```

This uses the prefix sum **concept** without building the explicit array. Running left sum + total allows computing right sum in O(1).

Time: O(n). Space: O(1).

---

## Pattern 4: Kadane's Algorithm

### Why It Exists

**Problem:** Find the contiguous subarray with the maximum sum.

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Answer: [4, -1, 2, 1] → sum = 6
```

**Brute force:** Check every subarray. O(n³) naive, O(n²) with running sum.

Kadane's does it in **O(n), O(1) space.**

### The Intuition

At each element, you make a simple decision:

> "Should I **extend** the current subarray to include this element, or **start fresh** from this element?"

If the current running sum is negative, it can only **hurt** any future subarray. So you throw it away and start fresh.

### The Algorithm

```python
def max_subarray_sum(arr):
    current_sum = arr[0]
    max_sum = arr[0]

    for i in range(1, len(arr)):
        # Key decision: extend or start fresh
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum
```

Trace with `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

```
i=0: current=-2, max=-2
i=1: max(1, -2+1=-1) → current=1, max=1
i=2: max(-3, 1-3=-2) → current=-2, max=1
i=3: max(4, -2+4=2)  → current=4, max=4
i=4: max(-1, 4-1=3)  → current=3, max=4
i=5: max(2, 3+2=5)   → current=5, max=5
i=6: max(1, 5+1=6)   → current=6, max=6
i=7: max(-5, 6-5=1)  → current=1, max=6
i=8: max(4, 1+4=5)   → current=5, max=6
Answer: 6 ✅
```

Time: O(n). Space: O(1).

### When Kadane's Fails / Variations

**All negative array:** `[-5, -3, -1, -8]`. Kadane's correctly returns -1 (the least negative element). Some problem variants ask for the maximum sum subarray with at **least one element** — this handles it.

**Maximum product subarray:** You CAN'T just swap sum for product. Why? Because **two negatives multiply to a positive.** A very negative current product might become the maximum after multiplying by another negative. You need to track both the maximum AND minimum running product.

```python
def max_product_subarray(arr):
    max_prod = arr[0]
    min_prod = arr[0]  # Track minimum because negative × negative = positive
    result = arr[0]

    for i in range(1, len(arr)):
        if arr[i] < 0:
            max_prod, min_prod = min_prod, max_prod  # Swap before multiplying

        max_prod = max(arr[i], max_prod * arr[i])
        min_prod = min(arr[i], min_prod * arr[i])
        result = max(result, max_prod)

    return result
```

Time: O(n). Space: O(1).

---

## Pattern 5: Sorting-Based and Interval Patterns

### 5A: Sorting as Preprocessing

Sometimes sorting the input first makes the problem **dramatically** easier, even though it costs O(n log n).

**When sorting helps:**
- You need to find pairs/triplets (sorted arrays enable two pointers)
- You need to group similar elements
- You need to process elements in order
- You need to find closest values
- The problem says "regardless of order" (permutations are equivalent)

**Classic Example: Three Sum**

Find all unique triplets that sum to zero.

Brute force: O(n³). Check every triple.

With sorting + two pointers: O(n²).

```python
def three_sum(arr):
    arr.sort()  # O(n log n)
    result = []

    for i in range(len(arr) - 2):
        # Skip duplicates for i
        if i > 0 and arr[i] == arr[i-1]:
            continue

        # Two Sum with two pointers on remaining array
        left, right = i + 1, len(arr) - 1
        target = -arr[i]

        while left < right:
            current = arr[left] + arr[right]

            if current == target:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current < target:
                left += 1
            else:
                right -= 1

    return result
```

**The approach:** Fix one element (i). The remaining problem is Two Sum on a sorted subarray — solved with converging two pointers.

Time: O(n²) — the sort is O(n log n) which is dominated by the O(n²) nested loop.
Space: O(1) excluding output (O(n) for Timsort).

### 5B: Merge Intervals

**Problem:** Given a list of intervals `[[start, end], ...]`, merge all overlapping ones.

```
Input:  [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]
```

**The Pattern:**

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])  # Sort by start time

    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        current = intervals[i]
        last_merged = merged[-1]

        if current[0] <= last_merged[1]:
            # Overlapping — extend the end
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap — add new interval
            merged.append(current)

    return merged
```

**Why sort by start time?** After sorting, you only need to check if the current interval overlaps with the **last merged** one. No need to check all previous intervals.

**The overlap condition:** Two intervals [a, b] and [c, d] overlap if c ≤ b (the start of the second is before or at the end of the first).

Time: O(n log n) for sort. Space: O(n) for result.

**Variations:**
- Insert Interval: insert a new interval into a sorted list and merge
- Meeting Rooms: can a person attend all meetings? (check for ANY overlap)
- Meeting Rooms II: minimum rooms needed (more advanced — uses heap, covered in Week 6)

---

# PART 4: STRING-SPECIFIC PATTERNS

## 4A: Frequency Counting

Many string problems boil down to: "do these two strings have the same character frequencies?"

### The Tool: Dictionary / Counter

```python
from collections import Counter

def are_anagrams(s1, s2):
    return Counter(s1) == Counter(s2)
```

Time: O(n + m). Space: O(1) — because alphabet size is fixed (at most 26 lowercase letters).

**Wait — why O(1) space?** The hash map can have at most 26 entries (for lowercase English). That's a constant, regardless of string length. If the problem says "any Unicode character," then it's O(k) where k = unique characters.

### Fixed-Size Array as Frequency Counter

For lowercase English letters, you can use an array of size 26 instead of a hash map:

```python
def are_anagrams(s1, s2):
    if len(s1) != len(s2):
        return False

    count = [0] * 26

    for c in s1:
        count[ord(c) - ord('a')] += 1
    for c in s2:
        count[ord(c) - ord('a')] -= 1

    return all(x == 0 for x in count)
```

This is slightly faster in practice (array access vs hash overhead) and shows interviewers you understand the optimization.

### Group Anagrams

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # Anagrams have the same sorted form
        groups[key].append(s)
    return list(groups.values())
```

Time: O(n × k log k) where n = number of strings, k = max string length.
Alternative: use frequency tuple as key → O(n × k).

---

## 4B: Palindrome Techniques

### Two-Pointer (Already Covered)

Check from outside in. Covered in Pattern 1A.

### Expand Around Center

**Problem:** Find the longest palindromic substring.

**Brute force:** Check every substring. O(n³).

**Expand around center:** For each position, try to expand a palindrome outward. O(n²) but with excellent constants.

```python
def longest_palindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    result = ""
    for i in range(len(s)):
        # Odd length palindrome (center is s[i])
        odd = expand(i, i)
        # Even length palindrome (center is between s[i] and s[i+1])
        even = expand(i, i + 1)

        if len(odd) > len(result):
            result = odd
        if len(even) > len(result):
            result = even

    return result
```

**Why both odd and even?** "aba" has center at 'b'. "abba" has center between the two 'b's. You must check both.

Time: O(n²) — n centers, each expansion up to O(n). Space: O(1) ignoring output.

---

## 4C: Substring Search Patterns

### Brute Force

Check every starting position, compare character by character.

```python
def find_substring(text, pattern):
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            return i
    return -1
```

Time: O(n × m). Each slice + comparison is O(m), done O(n) times.

### Sliding Window for Fixed-Length Matching

If you need to check all substrings of length m against some condition (like anagram), use a sliding window with a frequency counter instead of comparing strings directly.

```python
def find_anagram_indices(s, p):
    """Find all starting indices where anagram of p exists in s."""
    if len(p) > len(s):
        return []

    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []

    if window_count == p_count:
        result.append(0)

    for i in range(len(p), len(s)):
        # Add new character
        window_count[s[i]] += 1
        # Remove old character
        old = s[i - len(p)]
        window_count[old] -= 1
        if window_count[old] == 0:
            del window_count[old]

        if window_count == p_count:
            result.append(i - len(p) + 1)

    return result
```

Time: O(n × 26) = O(n) for fixed alphabet. The Counter comparison is O(26) = O(1).

### Rabin-Karp (Exposure Level)

Uses hashing to compare substrings in O(1) instead of O(m). Instead of comparing characters, compute a **rolling hash** that can be updated in O(1) as the window slides.

**Core idea:** Hash("abc") can be updated to Hash("bcd") by removing 'a's contribution and adding 'd's contribution.

You don't need to implement this from scratch for interviews, but know it exists. Useful for:
- Multiple pattern matching
- 2D pattern matching
- When you need O(n) average case substring search

---

## 4D: String Building Patterns

**The rule in Python: NEVER build strings with `+=` in a loop.**

**Pattern 1: List accumulation + join**

```python
parts = []
for item in data:
    parts.append(process(item))
result = "".join(parts)
```

**Pattern 2: List comprehension + join**

```python
result = "".join(process(item) for item in data)
```

**Pattern 3: f-strings for formatting (not for bulk building)**

```python
# Good for single formatted strings
s = f"Name: {name}, Age: {age}"

# BAD for loop building — still creates new string each time
result = ""
for item in data:
    result = f"{result}{item}"  # Still O(n²)!
```

---

# PART 5: MATRIX (2D ARRAY) FUNDAMENTALS

## 5A: Traversal Patterns

A matrix is an array of arrays. `grid[r][c]` = element at row r, column c.

### Row-Major Traversal (Most Common)

```python
for r in range(rows):
    for c in range(cols):
        print(grid[r][c])
```

Time: O(r × c). Visits every cell. This is the default traversal.

### Column-Major Traversal

```python
for c in range(cols):
    for r in range(rows):
        print(grid[r][c])
```

Same time complexity, different order. Used when you need to process columns before rows.

### Diagonal Traversal

```python
# Main diagonal (top-left to bottom-right)
for i in range(min(rows, cols)):
    print(grid[i][i])

# All diagonals — elements on same diagonal have same (r - c)
from collections import defaultdict
diagonals = defaultdict(list)
for r in range(rows):
    for c in range(cols):
        diagonals[r - c].append(grid[r][c])
```

### Spiral Traversal

```python
def spiral_order(matrix):
    if not matrix:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Right across top
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        # Down along right
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        # Left across bottom (if rows remain)
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        # Up along left (if cols remain)
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```

Time: O(r × c). Space: O(1) excluding output.

This looks complex but the pattern is simple: maintain four boundaries (top, bottom, left, right), traverse each edge, then shrink the boundaries.

---

## 5B: In-Place Matrix Operations

### Rotate Matrix 90° Clockwise

**The trick:** Transpose + Reverse each row.

```python
def rotate_90(matrix):
    n = len(matrix)

    # Step 1: Transpose (swap [i][j] with [j][i])
    for i in range(n):
        for j in range(i + 1, n):  # Only upper triangle to avoid double-swap
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

Why `j in range(i + 1, n)` and not `range(n)`? If you swap both [i][j] and [j][i], you'd swap twice — ending up back where you started. Only swap each pair once.

Time: O(n²). Space: O(1).

### Set Matrix Zeroes

**Problem:** If any element is 0, set its entire row and column to 0.

**Trap:** You can't set them as you find them — that would create new zeroes that cascade.

**O(1) space approach:** Use the first row and first column as markers.

```python
def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))

    # Mark zeroes in first row/col
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Zero out based on marks
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    # Handle first row and column
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
```

Time: O(r × c). Space: O(1).

---

## 5C: The 2D Array Python Trap

**This will bite you if you don't know it:**

```python
# ❌ WRONG — all rows share the SAME list object
grid = [[0] * cols] * rows

grid[0][0] = 1
print(grid)
# [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  ← ALL rows changed!
```

`[[0] * cols] * rows` creates one row list and makes rows references to it. They're all the **same object.**

```python
# ✅ CORRECT — each row is an independent list
grid = [[0] * cols for _ in range(rows)]

grid[0][0] = 1
print(grid)
# [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  ← Only first row changed ✅
```

**Memorize this.** It will save you hours of debugging.

---

# PART 6: EDGE CASES & INTERVIEW SKILLS

## 6A: The Edge Case Checklist

Before submitting ANY array/string solution, test these mentally:

```
ARRAYS:
□ Empty array []
□ Single element [5]
□ Two elements [1, 2]
□ All identical elements [3, 3, 3, 3]
□ Already sorted [1, 2, 3, 4, 5]
□ Reverse sorted [5, 4, 3, 2, 1]
□ Negative numbers [-5, -1, -3]
□ Mix of positive and negative [-2, 1, -3, 4]
□ Contains zeroes [0, 1, 0, 3, 12]
□ Very large input (10⁵ — complexity check)
□ k > n for rotation/window problems
□ Duplicate elements [1, 2, 2, 3, 3, 3]

STRINGS:
□ Empty string ""
□ Single character "a"
□ All same character "aaaa"
□ Already a palindrome "racecar"
□ Spaces and punctuation "A man, a plan"
□ Mixed case "AbCd"
□ All spaces "   "
□ Unicode / special characters (ask interviewer)
```

## 6B: The Interview Workflow

When you get an array/string problem in an interview:

**Step 1: Clarify (2 minutes)**
Ask before coding:
- Is the array sorted?
- Can there be duplicates?
- Can there be negative numbers?
- What's the input size range? (determines target complexity)
- Should I modify in-place or return a new array?
- What should I return for empty input?

**Step 2: Examples (2 minutes)**
Walk through 1-2 examples on paper/whiteboard. Make sure you understand the problem.

**Step 3: Brute Force (1 minute)**
State the brute force approach and its complexity. Don't code it. Just say it.

> "The brute force would be to check every pair, which is O(n²). I think we can do better with two pointers since the array is sorted."

**Step 4: Optimal Approach (3 minutes)**
Explain your optimized approach. State the time and space complexity BEFORE coding.

> "I'll use two pointers converging from both ends. This gives O(n) time, O(1) space."

**Step 5: Code (10-15 minutes)**
Write clean code. Use meaningful variable names. Add brief comments for tricky parts.

**Step 6: Test (3-5 minutes)**
Walk through your code with an example. Then check edge cases mentally.

---

# PART 7: BITWISE OPERATIONS

## Why Bitwise Matters

Computers represent everything in **binary** — 0s and 1s. Bitwise operations work directly on these bits. They're:
- **Extremely fast** — single CPU instruction, faster than arithmetic
- **Space-efficient** — can store/check multiple flags in one integer
- **Required** for certain problems that have no elegant non-bitwise solution
- **Tested** in FAANG interviews, particularly at Google

## Binary Representation

Every integer is stored as a sequence of bits:

```
Decimal  Binary
0        0000
1        0001
2        0010
3        0011
4        0100
5        0101
6        0110
7        0111
8        1000
9        1001
10       1010
15       1111
16       10000
```

**How to read binary:** Each position represents a power of 2, from right to left.

```
Binary: 1 0 1 1
        ↓ ↓ ↓ ↓
        2³ 2² 2¹ 2⁰
        8  4  2  1

1011 = 8 + 0 + 2 + 1 = 11
```

**Python tools:**

```python
bin(10)      # '0b1010' — decimal to binary string
int('1010', 2)  # 10 — binary string to decimal
```

---

## The Six Bitwise Operators

### AND ( & ) — Both bits must be 1

```
  1 0 1 1  (11)
& 1 1 0 1  (13)
─────────
  1 0 0 1  (9)
```

Each bit position: only 1 if BOTH inputs are 1.

**Use cases:**
- **Check if a bit is set:** `n & (1 << k)` — checks if bit at position k is 1
- **Even/odd check:** `n & 1` — if result is 0, n is even. If 1, n is odd. Why? The last bit is 1 only for odd numbers.

```python
def is_even(n):
    return (n & 1) == 0

# Faster than n % 2 == 0 (single bit operation vs division)
```

- **Clear bits:** AND with a mask of 0s where you want to clear

### OR ( | ) — Either bit can be 1

```
  1 0 1 1  (11)
| 1 1 0 1  (13)
─────────
  1 1 1 1  (15)
```

Each bit position: 1 if EITHER (or both) inputs are 1.

**Use cases:**
- **Set a bit:** `n | (1 << k)` — forces bit at position k to 1
- **Combine flags:** `READ | WRITE | EXECUTE` in permission systems

### XOR ( ^ ) — Bits must differ

```
  1 0 1 1  (11)
^ 1 1 0 1  (13)
─────────
  0 1 1 0  (6)
```

Each bit position: 1 only if the bits are DIFFERENT.

**XOR is the most important bitwise operator for interviews.** It has magical properties:

```
Property 1:  a ^ a = 0        (anything XOR itself is 0)
Property 2:  a ^ 0 = a        (anything XOR zero is itself)
Property 3:  a ^ b = b ^ a    (commutative — order doesn't matter)
Property 4:  (a ^ b) ^ c = a ^ (b ^ c)  (associative — grouping doesn't matter)
```

**Why these properties matter — Single Number Problem:**

Given an array where every element appears twice EXCEPT one, find the single one.

```python
def single_number(arr):
    result = 0
    for num in arr:
        result ^= num
    return result
```

Trace with `[4, 1, 2, 1, 2]`:
```
result = 0
0 ^ 4 = 4
4 ^ 1 = 5
5 ^ 2 = 7
7 ^ 1 = 6    (1 ^ 1 cancels out somewhere in the bits)
6 ^ 2 = 4    (2 ^ 2 cancels out)
Result: 4 ✅
```

All pairs cancel out (Property 1). Only the single number remains (Property 2). Order doesn't matter (Properties 3 & 4).

Time: O(n). Space: **O(1).** No hash set needed. This is the optimal solution.

**Swap without temporary variable:**

```python
a = a ^ b
b = a ^ b    # b = (a ^ b) ^ b = a ^ (b ^ b) = a ^ 0 = a
a = a ^ b    # a = (a ^ b) ^ a = (a ^ a) ^ b = 0 ^ b = b
```

Neat trick. In practice, Python's tuple swap (`a, b = b, a`) is cleaner, but interviewers may ask about this.

### NOT ( ~ ) — Flip all bits

```
~ 0000 1011  (11)
= 1111 0100  (-12 in two's complement)
```

In Python: `~n = -(n + 1)`. Flips every bit.

Less commonly used in interview problems. Main use: creating bitmasks with all bits set except certain ones.

### Left Shift ( << ) — Multiply by 2ᵏ

```
5 << 1  =  10    (0101 → 1010)  — multiply by 2
5 << 2  =  20    (0101 → 10100) — multiply by 4
5 << 3  =  40    (0101 → 101000) — multiply by 8
```

`n << k` = n × 2ᵏ

**Use cases:**
- Creating bitmasks: `1 << k` creates a number with only bit k set
- Fast multiplication by powers of 2

### Right Shift ( >> ) — Divide by 2ᵏ (floor)

```
20 >> 1  =  10   (10100 → 1010)  — divide by 2
20 >> 2  =  5    (10100 → 101)   — divide by 4
```

`n >> k` = n // 2ᵏ

**Use cases:**
- Fast division by powers of 2
- Extracting specific bits
- Finding midpoint: `(left + right) >> 1` instead of `(left + right) // 2`

---

## Bit Manipulation Toolkit

### Check if bit k is set

```python
def is_bit_set(n, k):
    return (n >> k) & 1 == 1
    # Or equivalently: return n & (1 << k) != 0
```

### Set bit k to 1

```python
def set_bit(n, k):
    return n | (1 << k)
```

### Clear bit k to 0

```python
def clear_bit(n, k):
    return n & ~(1 << k)
```

### Toggle bit k (flip it)

```python
def toggle_bit(n, k):
    return n ^ (1 << k)
```

### Count number of set bits (1s)

```python
def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Python shortcut:
bin(n).count('1')
```

**Brian Kernighan's trick (faster — only loops once per set bit):**

```python
def count_bits(n):
    count = 0
    while n:
        n = n & (n - 1)  # Clears the lowest set bit
        count += 1
    return count
```

Why `n & (n - 1)` clears the lowest set bit:

```
n     = 1 0 1 0 0  (20)
n - 1 = 1 0 0 1 1  (19)
n & (n-1) = 1 0 0 0 0  (16)  ← lowest set bit cleared
```

Subtracting 1 flips the lowest set bit and all bits below it. AND-ing with original clears exactly the lowest set bit.

### Check if n is a power of 2

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

Why? A power of 2 has exactly ONE set bit: `1000...0`. So `n & (n-1)` = 0.

```
n = 8:    1000
n - 1 = 7: 0111
n & (n-1): 0000 ✅ → power of 2

n = 6:    0110
n - 1 = 5: 0101
n & (n-1): 0100 ≠ 0 → NOT power of 2
```

---

## Classic Bitwise Interview Problems

### Missing Number

Array of n numbers containing 0 to n with one missing. Find it.

**Approach 1: Math** — Expected sum minus actual sum. O(n) time, O(1) space. But can overflow for huge n in other languages.

**Approach 2: XOR** — XOR all numbers 0 to n with all array elements. Pairs cancel, missing number remains.

```python
def missing_number(arr):
    n = len(arr)
    result = n  # Start with n (since array has indices 0 to n-1)
    for i in range(n):
        result ^= i ^ arr[i]
    return result
```

Trace with `[3, 0, 1]` (missing 2):
```
n = 3, result = 3
i=0: result = 3 ^ 0 ^ 3 = 0
i=1: result = 0 ^ 1 ^ 0 = 1
i=2: result = 1 ^ 2 ^ 1 = 2
Answer: 2 ✅
```

Time: O(n). Space: O(1). No hash set, no sum overflow risk.

### Single Number II — Every Element Appears Three Times Except One

This is harder. XOR alone doesn't work because `a ^ a ^ a ≠ 0`.

**Approach:** Count bits. For each bit position, count how many numbers have that bit set. If the count isn't divisible by 3, the single number has that bit set.

```python
def single_number_ii(arr):
    result = 0
    for bit in range(32):
        bit_count = 0
        for num in arr:
            if num & (1 << bit):
                bit_count += 1
        if bit_count % 3 != 0:
            result |= (1 << bit)
    return result
```

Time: O(32n) = O(n). Space: O(1).

### Subsets Using Bitmasks

Remember from Part 2C: an array of n elements has 2ⁿ subsets. Each subset maps to a binary number from 0 to 2ⁿ - 1, where each bit indicates whether to include that element.

```python
def all_subsets(arr):
    n = len(arr)
    result = []

    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if bit i is set
                subset.append(arr[i])
        result.append(subset)

    return result
```

For `arr = [1, 2, 3]`:
```
mask=000 (0): []
mask=001 (1): [1]
mask=010 (2): [2]
mask=011 (3): [1,2]
mask=100 (4): [3]
mask=101 (5): [1,3]
mask=110 (6): [2,3]
mask=111 (7): [1,2,3]
```

Time: O(n × 2ⁿ). Space: O(n × 2ⁿ) for all subsets.

This is the **bitmask enumeration** technique. It's foundational for:
- Subset problems
- DP with bitmask states (Week 9)
- Competitive programming combinatorial problems

---

## When Bitwise Is The RIGHT Approach

```
PROBLEM TYPE                           TECHNIQUE
────────────────────────────────────────────────────
Find unique element (others paired)    XOR all elements
Find missing number                    XOR or bit counting
Check even/odd                         n & 1
Check power of 2                       n & (n-1) == 0
Count set bits                         Brian Kernighan's
Generate all subsets                   Bitmask enumeration
Swap without temp                      XOR swap
Multiply/divide by 2^k                Shift left/right
Store multiple boolean flags           Bitmask with AND/OR
Problems saying "O(1) space"           Often hints at bitwise
  where hash set would use O(n)
```

---

# PART 8: CONSOLIDATED REFERENCE SHEETS

## Array Pattern Decision Tree

```
WHAT TYPE OF PROBLEM?
│
├── Finding pairs/triplets with condition?
│   ├── Array is sorted → TWO POINTERS (converging)
│   └── Array is unsorted → HASH MAP or SORT FIRST
│
├── Contiguous subarray optimization?
│   ├── Fixed size → FIXED SLIDING WINDOW
│   ├── Variable size, all positive → VARIABLE SLIDING WINDOW
│   ├── Max/min sum, has negatives → KADANE'S
│   └── Range sum queries → PREFIX SUMS
│
├── Remove/filter/partition in-place?
│   └── TWO POINTERS (same direction, read/write)
│
├── Overlapping intervals?
│   └── SORT BY START + MERGE
│
├── Unique element / missing element?
│   └── XOR / BITWISE
│
├── Substring matching / anagram?
│   └── SLIDING WINDOW + FREQUENCY MAP
│
├── Palindrome?
│   ├── Check if palindrome → TWO POINTERS (converging)
│   └── Find longest palindromic substring → EXPAND AROUND CENTER
│
├── Generate all subsets/combinations?
│   └── BITMASK or BACKTRACKING
│
└── Sorted + search?
    └── BINARY SEARCH (Week 3)
```

## Complexity Summary of All Patterns

```
PATTERN                    TIME         SPACE      WHEN TO USE
──────────────────────────────────────────────────────────────
Two Pointers (converge)    O(n)         O(1)       Sorted, pairs, palindrome
Two Pointers (same dir)    O(n)         O(1)       In-place filter/partition
Two Pointers (two arrays)  O(a+b)       O(a+b)     Merge sorted arrays
Fixed Sliding Window       O(n)         O(1)       Subarray of size k
Variable Sliding Window    O(n)         O(1)*      Min/max subarray with condition
Prefix Sum (build)         O(n)         O(n)       Range sum queries
Prefix Sum (query)         O(1)         —          After build
Kadane's                   O(n)         O(1)       Max subarray sum
Sort + Process             O(n log n)   O(n)**     When order enables solution
Merge Intervals            O(n log n)   O(n)       Overlapping ranges
Frequency Counting         O(n)         O(1)***    Anagrams, char matching
Expand Around Center       O(n²)        O(1)       Palindromic substrings
XOR trick                  O(n)         O(1)       Find unique/missing element
Bitmask enumeration        O(n × 2ⁿ)   O(2ⁿ)      Generate all subsets

*  Plus hash set/map if tracking elements: O(k)
** Timsort uses O(n) auxiliary space
*** O(1) for fixed alphabet (26 letters), O(k) for arbitrary characters
```

---

# PART 9: EDGE CASE MASTER LIST

## Arrays

```
□ Empty array: []
□ Single element: [5]
□ Two elements: [1, 2]
□ All identical: [3, 3, 3, 3]
□ Already sorted: [1, 2, 3, 4, 5]
□ Reverse sorted: [5, 4, 3, 2, 1]
□ All negative: [-5, -3, -1, -8]
□ Mix positive/negative: [-2, 1, -3, 4]
□ Contains zeroes: [0, 1, 0, 3, 12]
□ Very large input (10⁵+) — check complexity
□ k > n for rotation/window problems
□ Duplicates: [1, 2, 2, 3, 3, 3]
□ All elements same sign
□ Overflow potential (sum of large numbers)
□ Matrix: single row, single column, 1×1
□ Matrix: non-square (rows ≠ cols)
```

## Strings

```
□ Empty string: ""
□ Single character: "a"
□ All same character: "aaaa"
□ Already palindrome: "racecar"
□ Spaces: "hello world"
□ Punctuation: "A man, a plan, a canal: Panama"
□ Mixed case: "AbCdEf"
□ All spaces: "   "
□ Digits in string: "abc123"
□ Pattern longer than text (substring search)
□ Pattern equals text
□ No match exists
```

---

# PART 10: TEST PROBLEMS

**Rules:**
- Show your **pattern identification** first: which pattern and why
- Then show the solution with complexity analysis
- Test against at least 2 edge cases mentally

---

### Problem 1: Warm-Up

Given a sorted array, remove duplicates **in-place** and return the new length. Each element should appear at most once.

```
Input: [1, 1, 2, 2, 2, 3, 4, 4, 5]
Output: 5 (array becomes [1, 2, 3, 4, 5, ...])
```

---

### Problem 2: Fixed Sliding Window

Given an array of integers and a number k, find the maximum sum of any contiguous subarray of size k.

```
Input: arr = [2, 1, 5, 1, 3, 2], k = 3
Output: 9 (subarray [5, 1, 3])
```

---

### Problem 3: Two Pointers on Sorted Array

Given a sorted array and a target, find two numbers that sum to the target. Return their indices.

```
Input: arr = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

---

### Problem 4: Prefix Sum Application

Given an array of integers and a target k, count the number of contiguous subarrays whose sum equals k.

```
Input: arr = [1, 1, 1], k = 2
Output: 2 (subarrays: [1,1] starting at index 0, [1,1] starting at index 1)
```

---

### Problem 5: Kadane's

Find the contiguous subarray with the maximum sum. Return the sum.

```
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6 (subarray [4, -1, 2, 1])
```

---

### Problem 6: Variable Sliding Window

Find the length of the longest substring without repeating characters.

```
Input: "abcabcbb"
Output: 3 ("abc")
```

---

### Problem 7: Bitwise

Given an array where every element appears twice except one, find the single element. **Solve in O(1) space.**

```
Input: [4, 1, 2, 1, 2]
Output: 4
```

---

### Problem 8: Merge Intervals

Given a list of intervals, merge all overlapping intervals.

```
Input: [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]
```

---

### Problem 9: String Frequency + Sliding Window

Given strings `s` and `p`, find all start indices of `p`'s anagrams in `s`.

```
Input: s = "cbaebabacd", p = "abc"
Output: [0, 6]
```

---

### Problem 10: The Boss — Multi-Pattern

Given an array of integers, find all unique triplets that sum to zero.

```
Input: [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
```

**This requires:** sorting + two pointers + duplicate handling. Show the full approach.

---

### Problem 11: Matrix

Rotate an n×n matrix 90 degrees clockwise **in-place.**

```
Input:  [[1,2,3],
         [4,5,6],
         [7,8,9]]

Output: [[7,4,1],
         [8,5,2],
         [9,6,3]]
```

---

### Problem 12: Integration Challenge

Given an array of meeting time intervals `[[start, end], ...]`, determine if a person can attend ALL meetings (no overlaps).

Then: determine the **minimum number of meeting rooms** required.

*Note: The second part is harder and hints at heap usage (Week 6). Solve what you can. If you can only solve part 1, that's fine — acknowledge what you'd need for part 2.*

---

# Problem 1: Remove Duplicates In-Place

## Pattern Identification

**Pattern: Two Pointers (Read/Write Pointer)**

Why? The array is **sorted**, so duplicates are adjacent. We need to modify in-place, which means we can't create a new array. The classic approach: one pointer reads through the array, another marks where to write the next unique element. The sorted property guarantees we only need to compare adjacent elements.

## Solution

```python
def remove_duplicates(arr):
    if len(arr) == 0:
        return 0

    write = 0
    for read in range(1, len(arr)):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]

    return write + 1
```

## Trace Through Main Example

```
arr = [1, 1, 2, 2, 2, 3, 4, 4, 5]
       w
          r

write=0, read=1: arr[1]=1 == arr[0]=1 → skip
write=0, read=2: arr[2]=2 != arr[0]=1 → write=1, arr[1]=2
write=1, read=3: arr[3]=2 == arr[1]=2 → skip
write=1, read=4: arr[4]=2 == arr[1]=2 → skip
write=1, read=5: arr[5]=3 != arr[1]=2 → write=2, arr[2]=3
write=2, read=6: arr[6]=4 != arr[2]=3 → write=3, arr[3]=4
write=3, read=7: arr[7]=4 == arr[3]=4 → skip
write=3, read=8: arr[8]=5 != arr[3]=4 → write=4, arr[4]=5

arr = [1, 2, 3, 4, 5, 3, 4, 4, 5]
                      ^ don't care about these
return write + 1 = 5 ✅
```

## Edge Cases

**Edge case 1: Empty array**
```
arr = []
→ return 0 ✅ (handled by the guard clause)
```

**Edge case 2: All same elements**
```
arr = [7, 7, 7, 7]
write=0, read=1: 7==7 skip
write=0, read=2: 7==7 skip
write=0, read=3: 7==7 skip
return 0 + 1 = 1 ✅
arr = [7, 7, 7, 7] (unchanged, first element is the unique one)
```

**Edge case 3: Already unique**
```
arr = [1, 2, 3]
write=0, read=1: 2!=1 → write=1, arr[1]=2
write=1, read=2: 3!=2 → write=2, arr[2]=3
return 3 ✅ (no changes needed)
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr). Single input.

**STEP 2:** Guard clause + one for loop.

**STEP 3:**
- Guard clause: O(1)
- Loop runs n - 1 times
- Inside: one comparison O(1), at most one assignment O(1), one increment O(1)
- Cost per iteration: O(1)
- Loop total: O(n)

**STEP 4:** O(1) + O(n) = **O(n)**

**STEP 5:**
- `write`, `read` → single variables → O(1)
- No extra data structures created (in-place!)
- **O(1) space**

> **Time: O(n), Space: O(1)**

---

# Problem 2: Fixed Sliding Window

## Pattern Identification

**Pattern: Fixed-Size Sliding Window**

Why? We need the maximum sum of a **contiguous** subarray of **fixed** size k. Brute force would recompute the sum for every window from scratch — O(n×k). But when we slide the window one position right, we only lose one element on the left and gain one on the right. We can update the sum in O(1) instead of recomputing it.

## Solution

```python
def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k:
        return None

    # Build the first window
    window_sum = 0
    for i in range(k):
        window_sum += arr[i]

    max_sum = window_sum

    # Slide the window
    for i in range(k, n):
        window_sum += arr[i]        # add new element entering window
        window_sum -= arr[i - k]    # remove element leaving window
        max_sum = max(max_sum, window_sum)

    return max_sum
```

## Trace Through Main Example

```
arr = [2, 1, 5, 1, 3, 2], k = 3

Build first window: arr[0]+arr[1]+arr[2] = 2+1+5 = 8
max_sum = 8

i=3: window_sum = 8 + arr[3] - arr[0] = 8 + 1 - 2 = 7
     max_sum = max(8, 7) = 8

i=4: window_sum = 7 + arr[4] - arr[1] = 7 + 3 - 1 = 9
     max_sum = max(8, 9) = 9

i=5: window_sum = 9 + arr[5] - arr[2] = 9 + 2 - 5 = 6
     max_sum = max(9, 6) = 9

return 9 ✅ (window [5, 1, 3])
```

## Edge Cases

**Edge case 1: k equals array length**
```
arr = [3, 1, 2], k = 3
First window: 3+1+2 = 6. Sliding loop doesn't run (range(3,3) is empty).
return 6 ✅ (only one window possible)
```

**Edge case 2: All negative numbers**
```
arr = [-3, -1, -5, -2], k = 2
First window: -3 + -1 = -4. max_sum = -4
i=2: -4 + (-5) - (-3) = -6. max_sum = -4
i=3: -6 + (-2) - (-1) = -7. max_sum = -4
return -4 ✅ (window [-3, -1], the "least negative")
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr). `k` is a number parameter.

**STEP 3:**
- First loop: runs k times, O(1) per iteration → O(k)
- Second loop: runs (n - k) times, O(1) per iteration → O(n - k)

**STEP 4:** O(k) + O(n - k) = O(n)

**STEP 5:**
- `window_sum`, `max_sum`, `i`, `n` → all single variables → O(1)
- No extra data structures.

> **Time: O(n), Space: O(1)**

---

# Problem 3: Two Pointers on Sorted Array

## Pattern Identification

**Pattern: Two Pointers — Opposite Ends**

Why? Array is **sorted**. If we place a pointer at each end:
- If the sum is too small → move left pointer right (increases sum)
- If the sum is too big → move right pointer left (decreases sum)
- If equal → found it

The sorted property gives us **directional guarantees** about how moving each pointer affects the sum. This eliminates the need for a hash map or brute force.

## Solution

```python
def two_sum_sorted(arr, target):
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []  # no pair found
```

## Trace Through Main Example

```
arr = [2, 7, 11, 15], target = 9
left = 0, right = 3

Iteration 1: sum = arr[0] + arr[3] = 2 + 15 = 17
             17 > 9 → right = 2

Iteration 2: sum = arr[0] + arr[2] = 2 + 11 = 13
             13 > 9 → right = 1

Iteration 3: sum = arr[0] + arr[1] = 2 + 7 = 9
             9 == 9 → return [0, 1] ✅
```

## Edge Cases

**Edge case 1: Target requires last two elements**
```
arr = [1, 2, 3, 10], target = 13
left=0, right=3: 1+10=11 < 13 → left=1
left=1, right=3: 2+10=12 < 13 → left=2
left=2, right=3: 3+10=13 == 13 → return [2, 3] ✅
```

**Edge case 2: No valid pair**
```
arr = [1, 2, 3], target = 100
left=0, right=2: 1+3=4 < 100 → left=1
left=1, right=2: 2+3=5 < 100 → left=2
left=2, right=2: left < right false → exit
return [] ✅
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr). Single input.

**STEP 3:**
- Each iteration either `left` moves right or `right` moves left
- They start n-1 apart and converge — at most n iterations total before they meet
- Inside: arithmetic O(1), comparison O(1)
- O(n)

**STEP 5:**
- `left`, `right`, `current_sum` → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 4: Prefix Sum Application

## Pattern Identification

**Pattern: Prefix Sum + Hash Map**

Why? We need to count subarrays that sum to k. A brute force approach (check all subarrays) is O(n²). The key insight:

If `prefix[j] - prefix[i] == k`, then the subarray from i+1 to j sums to k. Rearranging: `prefix[i] = prefix[j] - k`. So at each position j, we ask: "How many previous prefix sums equal `current_prefix - k`?" A hash map counting prefix sum frequencies answers this in O(1).

## Solution

```python
def subarray_sum(arr, k):
    prefix_counts = {0: 1}  # empty prefix has sum 0, seen once
    current_sum = 0
    count = 0

    for num in arr:
        current_sum += num
        complement = current_sum - k
        if complement in prefix_counts:
            count += prefix_counts[complement]
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return count
```

## Why `{0: 1}` Is Needed

If a subarray starting from index 0 sums to k, then `current_sum == k` and `complement = k - k = 0`. We need to find "how many times has prefix sum 0 appeared?" — it appeared once: the empty prefix before the array starts. Without this initialization, we'd miss subarrays that start at index 0.

## Trace Through Main Example

```
arr = [1, 1, 1], k = 2
prefix_counts = {0: 1}, current_sum = 0, count = 0

num=1: current_sum = 1
       complement = 1 - 2 = -1
       -1 not in prefix_counts → skip
       prefix_counts = {0: 1, 1: 1}

num=1: current_sum = 2
       complement = 2 - 2 = 0
       0 in prefix_counts → count += 1 → count = 1
       (subarray [1,1] from index 0 to 1)
       prefix_counts = {0: 1, 1: 1, 2: 1}

num=1: current_sum = 3
       complement = 3 - 2 = 1
       1 in prefix_counts → count += 1 → count = 2
       (subarray [1,1] from index 1 to 2)
       prefix_counts = {0: 1, 1: 1, 2: 1, 3: 1}

return 2 ✅
```

## Edge Cases

**Edge case 1: Single element equals k**
```
arr = [5], k = 5
current_sum=5, complement=0, 0 in {0:1} → count=1
return 1 ✅
```

**Edge case 2: Negative numbers**
```
arr = [1, -1, 1], k = 1
prefix_counts = {0: 1}

num=1: sum=1, comp=-1, not found. counts={0:1, 1:1}
num=-1: sum=0, comp=-2, not found. counts={0:2, 1:1}
   (sum=0 appeared before, so now 0 has count 2)
num=1: sum=1, comp=-1, not found... wait.
   comp = 1 - 1 = 0. 0 in counts with value 2 → count += 2 → count=2
   
Subarrays summing to 1: [1] (index 0), [1,-1,1] (index 0-2), [1] (index 2)
Wait, let me recheck. Actually comp for last element: sum=1, comp=1-1=0, prefix_counts[0]=2, so count+=2.

Total count = 0 + 0 + 2 = 2. But the actual subarrays summing to 1:
- [1] starting at index 0 (prefix 1 - prefix 0 = 1) ✓
- [1, -1, 1] from index 0-2 (prefix 1 - prefix 0 = 1) ✓  
- [1] starting at index 2 (prefix 1 - prefix 0 at position 1 = 1) ✓

Hmm, that's 3. Let me retrace more carefully.

num=1: sum=1, comp=0, 0 in {0:1} → count=1. prefix_counts={0:1, 1:1}
num=-1: sum=0, comp=-1, not found. prefix_counts={0:2, 1:1}
num=1: sum=1, comp=0, 0 in counts with value 2 → count+=2 → count=3

return 3 ✅ 
Three subarrays: [1] at index 0, [1,-1,1] from 0-2, [1] at index 2.
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr). `k` is a number.

**STEP 3:**
- Loop runs n times
- Inside: arithmetic O(1), dict lookup (`in`) O(1), dict get O(1), dict assignment O(1)
- All O(1) operations per iteration
- O(n)

**STEP 5:**
- `prefix_counts` → dict that stores prefix sums. Worst case all n+1 prefix sums are unique → **O(n)**
- `current_sum`, `count`, `complement` → O(1)

> **Time: O(n), Space: O(n)**

---

# Problem 5: Kadane's Algorithm

## Pattern Identification

**Pattern: Kadane's Algorithm (Dynamic Programming / Greedy)**

Why? We need the maximum sum contiguous subarray. The key insight: at each position, we make a binary choice — either **extend** the current subarray, or **start fresh** from the current element. We extend if the running sum is positive (it helps). We start fresh if it's negative (it hurts).

This is technically a DP where `max_ending_here[i] = max(arr[i], max_ending_here[i-1] + arr[i])`, but it only needs O(1) space since we only look one step back.

## Solution

```python
def max_subarray(arr):
    max_current = arr[0]
    max_global = arr[0]

    for i in range(1, len(arr)):
        max_current = max(arr[i], max_current + arr[i])
        max_global = max(max_global, max_current)

    return max_global
```

## Trace Through Main Example

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

max_current = -2, max_global = -2

i=1: max_current = max(1, -2+1) = max(1, -1) = 1
     max_global = max(-2, 1) = 1

i=2: max_current = max(-3, 1+(-3)) = max(-3, -2) = -2
     max_global = max(1, -2) = 1

i=3: max_current = max(4, -2+4) = max(4, 2) = 4     ← START FRESH
     max_global = max(1, 4) = 4

i=4: max_current = max(-1, 4+(-1)) = max(-1, 3) = 3  ← EXTEND
     max_global = max(4, 3) = 4

i=5: max_current = max(2, 3+2) = max(2, 5) = 5       ← EXTEND
     max_global = max(4, 5) = 5

i=6: max_current = max(1, 5+1) = max(1, 6) = 6       ← EXTEND
     max_global = max(5, 6) = 6

i=7: max_current = max(-5, 6+(-5)) = max(-5, 1) = 1  ← EXTEND
     max_global = max(6, 1) = 6

i=8: max_current = max(4, 1+4) = max(4, 5) = 5       ← EXTEND
     max_global = max(6, 5) = 6

return 6 ✅ (subarray [4, -1, 2, 1])
```

## Edge Cases

**Edge case 1: All negative**
```
arr = [-3, -1, -4]
max_current = -3, max_global = -3
i=1: max_current = max(-1, -3+(-1)) = max(-1, -4) = -1
     max_global = max(-3, -1) = -1
i=2: max_current = max(-4, -1+(-4)) = max(-4, -5) = -4
     max_global = max(-1, -4) = -1
return -1 ✅ (best single element)
```

**Edge case 2: Single element**
```
arr = [5]
max_current = 5, max_global = 5
Loop doesn't run (range(1,1) is empty)
return 5 ✅
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- Single loop, n-1 iterations
- Inside: two `max()` calls — each compares two numbers → O(1)
- O(n)

**STEP 5:**
- `max_current`, `max_global` → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 6: Variable Sliding Window

## Pattern Identification

**Pattern: Variable-Size Sliding Window (Expand/Contract)**

Why? We need the **longest** substring without repeating characters. "Longest substring" with a constraint screams sliding window. The window size isn't fixed — it grows when we can, shrinks when we must (when a duplicate enters). We need a set or map to track what's currently in the window.

## Solution

```python
def length_of_longest_substring(s):
    seen = {}         # char → most recent index
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

## Why `seen[char] >= left` Matters

Without this check, we'd react to characters that are in the dictionary but **no longer in our current window.** If we previously saw 'a' at index 2 but our window starts at index 5, that 'a' is irrelevant. The `>= left` check ensures we only contract for duplicates **within the current window.**

## Trace Through Main Example

```
s = "abcabcbb"

seen = {}, left = 0, max_len = 0

right=0, char='a': not in seen → seen={'a':0}, len=1, max=1
right=1, char='b': not in seen → seen={'a':0,'b':1}, len=2, max=2
right=2, char='c': not in seen → seen={'a':0,'b':1,'c':2}, len=3, max=3
right=3, char='a': in seen, seen['a']=0 >= left=0 → left=1
         seen={'a':3,'b':1,'c':2}, len=3, max=3
         window is now "bca" → wait, [1..3] = "bca"... "bcab"? 
         
Let me be more careful. After left=1:
         window = s[1..3] = "bca", len = 3-1+1 = 3, max=3

right=4, char='b': in seen, seen['b']=1 >= left=1 → left=2
         seen={'a':3,'b':4,'c':2}, len=4-2+1=3, max=3
         window = s[2..4] = "cab"

right=5, char='c': in seen, seen['c']=2 >= left=2 → left=3
         seen={'a':3,'b':4,'c':5}, len=5-3+1=3, max=3
         window = s[3..5] = "abc"

right=6, char='b': in seen, seen['b']=4 >= left=3 → left=5
         seen={'a':3,'b':6,'c':5}, len=6-5+1=2, max=3
         window = s[5..6] = "cb"

right=7, char='b': in seen, seen['b']=6 >= left=5 → left=7
         seen={'a':3,'b':7,'c':5}, len=7-7+1=1, max=3
         window = s[7..7] = "b"

return 3 ✅
```

## Edge Cases

**Edge case 1: Empty string**
```
s = ""
Loop doesn't run. return 0 ✅
```

**Edge case 2: All same characters**
```
s = "aaaa"
right=0: 'a' not in seen → seen={'a':0}, max=1
right=1: 'a' in seen, 0>=0 → left=1, seen={'a':1}, len=1, max=1
right=2: 'a' in seen, 1>=1 → left=2, seen={'a':2}, len=1, max=1
right=3: 'a' in seen, 2>=2 → left=3, seen={'a':3}, len=1, max=1
return 1 ✅
```

## Complexity Analysis

**STEP 1:** `s` → n = len(s)

**STEP 3:**
- Single loop, n iterations
- Inside: dict lookup O(1), dict assignment O(1), comparison O(1), max O(1)
- **The `left` pointer only moves forward, never backward** — this is the same non-resetting pointer pattern from Problem 9 in the previous set
- Cost per iteration: O(1)
- O(n)

**STEP 5:**
- `seen` → dict storing at most 26 lowercase letters (or at most the character set size). For ASCII: O(1). For arbitrary Unicode: O(min(n, charset_size))
- `left`, `max_len` → O(1)
- Practically: **O(1)** (bounded character set). Technically: **O(min(n, m))** where m = charset size

> **Time: O(n), Space: O(min(n, m))** where m = character set size
> Practically for lowercase English: **O(n) time, O(1) space**

---

# Problem 7: Bitwise — Single Number

## Pattern Identification

**Pattern: XOR Bit Manipulation**

Why? Every element appears twice except one. We need O(1) space, which rules out hash sets. The key property of XOR:
- `a ^ a = 0` (any number XOR itself is zero)
- `a ^ 0 = a` (any number XOR zero is itself)
- XOR is commutative and associative (order doesn't matter)

So if we XOR all elements together, the pairs cancel out, leaving only the single element.

## Solution

```python
def single_number(arr):
    result = 0
    for num in arr:
        result ^= num
    return result
```

## Trace Through Main Example

```
arr = [4, 1, 2, 1, 2]
result = 0

result = 0 ^ 4 = 4        (binary: 000 ^ 100 = 100)
result = 4 ^ 1 = 5        (binary: 100 ^ 001 = 101)
result = 5 ^ 2 = 7        (binary: 101 ^ 010 = 111)
result = 7 ^ 1 = 6        (binary: 111 ^ 001 = 110)
result = 6 ^ 2 = 4        (binary: 110 ^ 010 = 100)

return 4 ✅

What happened: 4 ^ (1^1) ^ (2^2) = 4 ^ 0 ^ 0 = 4
```

## Edge Cases

**Edge case 1: Single element array**
```
arr = [7]
result = 0 ^ 7 = 7 ✅
```

**Edge case 2: Zero is the single number**
```
arr = [3, 3, 0]
result = 0 ^ 3 = 3, then 3 ^ 3 = 0, then 0 ^ 0... wait, that's wrong.
arr has 3 elements: [3, 3, 0]
result = 0 ^ 3 = 3
result = 3 ^ 3 = 0
result = 0 ^ 0 = 0
return 0 ✅ (zero is correctly identified)
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- Single loop, n iterations
- Inside: one XOR operation → O(1)
- O(n)

**STEP 5:**
- `result` → single integer → O(1)

> **Time: O(n), Space: O(1)**

---

# Problem 8: Merge Intervals

## Pattern Identification

**Pattern: Sort + Linear Scan (Interval Merging)**

Why? To detect overlaps efficiently, we need intervals ordered by start time. Once sorted, overlapping intervals are **adjacent.** We make one pass, merging as we go: if the current interval's start ≤ the previous interval's end, they overlap and we merge. Otherwise, we start a new group.

## Solution

```python
def merge_intervals(intervals):
    if len(intervals) == 0:
        return []

    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        current = intervals[i]
        last_merged = merged[-1]

        if current[0] <= last_merged[1]:
            # Overlapping — extend the end
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap — start new interval
            merged.append(current)

    return merged
```

## Trace Through Main Example

```
intervals = [[1,3], [2,6], [8,10], [15,18]]

After sort (already sorted by start): [[1,3], [2,6], [8,10], [15,18]]

merged = [[1,3]]

i=1: current=[2,6], last=[1,3]
     2 <= 3? YES → overlap → last[1] = max(3, 6) = 6
     merged = [[1,6]]

i=2: current=[8,10], last=[1,6]
     8 <= 6? NO → no overlap → append
     merged = [[1,6], [8,10]]

i=3: current=[15,18], last=[8,10]
     15 <= 10? NO → no overlap → append
     merged = [[1,6], [8,10], [15,18]]

return [[1,6], [8,10], [15,18]] ✅
```

## Edge Cases

**Edge case 1: Completely nested intervals**
```
intervals = [[1,10], [2,3], [4,5]]
sorted: [[1,10], [2,3], [4,5]]
merged = [[1,10]]
i=1: 2 <= 10? YES → max(10,3) = 10. merged = [[1,10]]
i=2: 4 <= 10? YES → max(10,5) = 10. merged = [[1,10]]
return [[1,10]] ✅ (inner intervals absorbed)
```

**Edge case 2: Unsorted with overlap**
```
intervals = [[3,5], [1,4]]
sorted: [[1,4], [3,5]]
merged = [[1,4]]
i=1: 3 <= 4? YES → max(4,5) = 5. merged = [[1,5]]
return [[1,5]] ✅
```

## Complexity Analysis

**STEP 1:** `intervals` → n = len(intervals)

**STEP 3:**
- `intervals.sort()` → **O(n log n)**
- Loop runs n-1 times, O(1) per iteration (comparison, max, append/modify) → **O(n)**

**STEP 4:** O(n log n) + O(n) = **O(n log n)**

**STEP 5:**
- `merged` → worst case no overlaps → n intervals → **O(n)**
- `current`, `last_merged` → O(1)

> **Time: O(n log n), Space: O(n)**

---

# Problem 9: String Frequency + Sliding Window

## Pattern Identification

**Pattern: Fixed Sliding Window + Frequency Count**

Why? An anagram of `p` is any permutation — same character frequencies, different order. We slide a window of size `len(p)` across `s`. Instead of sorting each window (O(k log k) per position), we maintain a **frequency count** that we update in O(1) as the window slides. We compare frequency counts to detect anagrams.

## Solution

```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []

    p_count = {}
    w_count = {}
    result = []

    # Build frequency map for p
    for char in p:
        p_count[char] = p_count.get(char, 0) + 1

    # Build first window
    for i in range(len(p)):
        char = s[i]
        w_count[char] = w_count.get(char, 0) + 1

    if w_count == p_count:
        result.append(0)

    # Slide the window
    for i in range(len(p), len(s)):
        # Add new character entering window
        add_char = s[i]
        w_count[add_char] = w_count.get(add_char, 0) + 1

        # Remove character leaving window
        remove_char = s[i - len(p)]
        w_count[remove_char] -= 1
        if w_count[remove_char] == 0:
            del w_count[remove_char]

        if w_count == p_count:
            result.append(i - len(p) + 1)

    return result
```

## A Note On `w_count == p_count`

Comparing two dictionaries in Python checks if they have the same keys and values. This costs O(number of unique keys). Since we're dealing with characters, the max unique keys is 26 (lowercase English). So this comparison is **O(26) = O(1)** in practice. For arbitrary alphabets of size m, it's O(m).

## Trace Through Main Example

```
s = "cbaebabacd", p = "abc"

p_count = {'a':1, 'b':1, 'c':1}

Build first window s[0..2] = "cba":
w_count = {'c':1, 'b':1, 'a':1}
w_count == p_count? YES → result = [0]

i=3: add 'e', remove s[0]='c'
     w_count = {'c':0→del, 'b':1, 'a':1, 'e':1} = {'b':1, 'a':1, 'e':1}
     != p_count

i=4: add 'b', remove s[1]='b'
     add: {'b':2, 'a':1, 'e':1}
     remove: {'b':1, 'a':1, 'e':1}
     != p_count

i=5: add 'a', remove s[2]='a'
     add: {'b':1, 'a':2, 'e':1}
     remove: {'b':1, 'a':1, 'e':1}
     != p_count

i=6: add 'b', remove s[3]='e'
     add: {'b':2, 'a':1, 'e':1}
     remove e: {'b':2, 'a':1}
     != p_count

i=7: add 'a', remove s[4]='b'
     add: {'b':2, 'a':2}
     remove: {'b':1, 'a':2}
     != p_count

i=8: add 'c', remove s[5]='a'
     add: {'b':1, 'a':2, 'c':1}
     remove: {'b':1, 'a':1, 'c':1}
     == p_count? YES → result.append(8-3+1 = 6)

i=9: add 'd', remove s[6]='b'
     w_count = {'a':1, 'c':1, 'd':1}
     != p_count

return [0, 6] ✅
```

## Edge Cases

**Edge case 1: p longer than s**
```
s = "ab", p = "abc"
Guard clause returns [] ✅
```

**Edge case 2: Entire string is one anagram**
```
s = "bca", p = "abc"
First window "bca": counts match → result = [0]
No sliding (len(p) == len(s))
return [0] ✅
```

## Complexity Analysis

**STEP 1:**
- `s` → n = len(s)
- `p` → k = len(p)
- Two independent inputs.

**STEP 3:**
- Build p_count: k iterations × O(1) = **O(k)**
- Build first window: k iterations × O(1) = **O(k)**
- Dict comparison: O(26) = **O(1)** (bounded alphabet)
- Sliding loop: (n - k) iterations
  - Inside: dict operations O(1), dict comparison O(1) (bounded alphabet)
  - Per iteration: O(1)
  - Total: **O(n - k)**

**STEP 4:** O(k) + O(k) + O(n - k) = **O(n)**

**STEP 5:**
- `p_count` → at most 26 keys → **O(1)** (bounded alphabet)
- `w_count` → at most 26 keys → **O(1)**
- `result` → worst case every position is an anagram → O(n - k) entries → **O(n)**

> **Time: O(n), Space: O(n)**
> (where the O(n) space is from the output list; auxiliary space is O(1) due to bounded alphabet)

---

# Problem 10: The Boss — 3Sum

## Pattern Identification

**Pattern: Sort + Two Pointers + Duplicate Skipping**

Why? Brute force checks all triplets: O(n³). We can do better:
1. **Sort** the array → O(n log n)
2. **Fix one element** (iterate with `i`) → reduces to a two-sum problem
3. **Two pointers** on the remaining portion to find pairs that sum to `-arr[i]`
4. **Skip duplicates** at every level to avoid duplicate triplets

The sort enables both the two-pointer technique and easy duplicate detection (duplicates are adjacent).

## Solution

```python
def three_sum(arr):
    arr.sort()
    n = len(arr)
    result = []

    for i in range(n - 2):
        # Skip duplicate values for i
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Early termination: if smallest possible value > 0, no more triplets
        if arr[i] > 0:
            break

        target = -arr[i]
        left = i + 1
        right = n - 1

        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == target:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates for left
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                # Skip duplicates for right
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return result
```

## Why Each Deduplication Step Is Necessary

1. **`if i > 0 and arr[i] == arr[i-1]: continue`** — If we already used -1 as the fixed element, using -1 again would produce the same triplets. Skip.
2. **`while arr[left] == arr[left+1]: left += 1`** — After finding a valid triplet, if the next left value is the same, it would create a duplicate triplet with the same `arr[i]` and `arr[right]`. Skip.
3. **`while arr[right] == arr[right-1]: right -= 1`** — Same logic for right pointer.

## Trace Through Main Example

```
arr = [-1, 0, 1, 2, -1, -4]
sorted: [-4, -1, -1, 0, 1, 2]
         0    1    2   3  4  5

i=0: arr[0]=-4, target=4
  left=1, right=5: -1+2=1 < 4 → left=2
  left=2, right=5: -1+2=1 < 4 → left=3
  left=3, right=5: 0+2=2 < 4 → left=4
  left=4, right=5: 1+2=3 < 4 → left=5
  left=5, right=5: not < → done
  No triplets with -4.

i=1: arr[1]=-1, target=1
  i>0 and arr[1]==arr[0]? -1==-4? NO → proceed
  left=2, right=5: -1+2=1 == 1 → FOUND [-1, -1, 2]
    skip dup left: arr[2]==arr[3]? -1==0? NO → stop
    skip dup right: arr[5]==arr[4]? 2==1? NO → stop
    left=3, right=4
  left=3, right=4: 0+1=1 == 1 → FOUND [-1, 0, 1]
    skip dup left: arr[3]==arr[4]? 0==1? NO
    skip dup right: arr[4]==arr[3]? 1==0? NO
    left=4, right=3
  left=4, right=3: not left < right → done

i=2: arr[2]=-1
  i>0 and arr[2]==arr[1]? -1==-1? YES → SKIP (dedup!)

i=3: arr[3]=0, 0 > 0? No. target=0
  left=4, right=5: 1+2=3 > 0 → right=4
  left=4, right=4: not < → done

return [[-1, -1, 2], [-1, 0, 1]] ✅
```

## Edge Cases

**Edge case 1: Array too small**
```
arr = [1, 2]
n=2, range(n-2) = range(0) → loop doesn't run
return [] ✅
```

**Edge case 2: All zeros**
```
arr = [0, 0, 0, 0]
sorted: [0, 0, 0, 0]
i=0: target=0, left=1, right=3: 0+0=0 → FOUND [0,0,0]
  skip dups left: arr[1]==arr[2]? yes → left=2. arr[2]==arr[3]? yes → left=3
  skip dups right: arr[3]==arr[2]? yes → right=2
  left=4, right=1 → done
i=1: arr[1]==arr[0]? yes → SKIP
i=2: arr[2]==arr[1]? yes → SKIP
return [[0,0,0]] ✅ (only one triplet, no duplicates)
```

## Complexity Analysis

**STEP 1:** `arr` → n = len(arr)

**STEP 3:**
- `arr.sort()` → **O(n log n)**
- Outer loop: runs at most n-2 times (with skips, potentially fewer)
- For each i, the two-pointer scan: left and right start at opposite ends of the remaining portion and converge. At most O(n) work per i.
- The duplicate-skipping while loops are subsumed within the pointer movements — left and right still only move forward/backward and can't exceed O(n) total moves per outer iteration.
- Outer × inner: n × O(n) = **O(n²)**

**STEP 4:** O(n log n) + O(n²) = **O(n²)** (n² dominates)

**STEP 5:**
- Sorting: O(1) or O(n) depending on sort implementation (Python's Timsort uses O(n) auxiliary)
- `result` → worst case? The maximum number of unique triplets from n elements. This is bounded by O(n²) triplets. → **O(n²)** worst case
- `left`, `right`, `target` → O(1)

> **Time: O(n²), Space: O(n²)** for output
> Auxiliary space (excluding output): **O(n)** for sorting

---

# Problem 11: Matrix Rotation

## Pattern Identification

**Pattern: Transpose + Reverse (Matrix Manipulation)**

Why? Rotating 90° clockwise can be decomposed into two simple operations:
1. **Transpose** the matrix (swap rows and columns: `matrix[i][j] ↔ matrix[j][i]`)
2. **Reverse each row**

This avoids the complex index math of doing the rotation directly, and both operations are easy to do in-place.

**Why does Transpose + Reverse = 90° Clockwise Rotation?**

An element at position (i, j) in the original:
- After transpose: goes to (j, i)
- After reversing row j: goes to (j, n-1-i)

Original (i, j) → Final (j, n-1-i). That's exactly the 90° clockwise rotation formula.

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

Step 1 — Transpose (swap across diagonal):
  swap (0,1)↔(1,0): 2↔4
  swap (0,2)↔(2,0): 3↔7
  swap (1,2)↔(2,1): 6↔8

After transpose:
[[1, 4, 7],
 [2, 5, 8],
 [3, 6, 9]]

Step 2 — Reverse each row:
  [1, 4, 7] → [7, 4, 1]
  [2, 5, 8] → [8, 5, 2]
  [3, 6, 9] → [9, 6, 3]

Final:
[[7, 4, 1],
 [8, 5, 2],
 [9, 6, 3]] ✅
```

## Edge Cases

**Edge case 1: 1×1 matrix**
```
[[5]]
Transpose: j range(1,1) → nothing happens
Reverse: [5] → [5]
Result: [[5]] ✅
```

**Edge case 2: 2×2 matrix**
```
[[1, 2],
 [3, 4]]

Transpose: swap (0,1)↔(1,0): 2↔3
[[1, 3],
 [2, 4]]

Reverse rows:
[[3, 1],
 [4, 2]] ✅

Verify: original top-right 2 should go to bottom-right → position [1][1] = 2? 
No wait: 90° clockwise of [[1,2],[3,4]] should be [[3,1],[4,2]]. ✅
```

## Complexity Analysis

**STEP 1:** `matrix` → n×n matrix. n = number of rows = number of columns.

**STEP 3:**

*Transpose:*
- Outer loop: n iterations
- Inner loop: for each i, j runs from i+1 to n-1 → (n-1-i) iterations
- Total iterations: (n-1) + (n-2) + ... + 0 = n(n-1)/2
- Inside: one swap → O(1)
- Transpose total: **O(n²)**

*Reverse each row:*
- Outer loop: n rows
- `row.reverse()` → O(n) per row (reverses n elements in-place)
- Reverse total: n × O(n) = **O(n²)**

**STEP 4:** O(n²) + O(n²) = **O(n²)**

**STEP 5:**
- `i`, `j` → O(1)
- The swap uses a temporary variable internally → O(1)
- `row.reverse()` is in-place → O(1) extra
- **Everything is in-place!**

> **Time: O(n²), Space: O(1)**

Note: O(n²) is optimal here — we must touch all n² cells at least once.

---

# Problem 12: Meeting Rooms

## Part 1: Can a Person Attend All Meetings?

### Pattern Identification

**Pattern: Sort + Linear Scan (Overlap Detection)**

Why? If meetings are sorted by start time, a conflict exists if and only if some meeting starts before the previous one ends. One pass after sorting detects this.

### Solution

```python
def can_attend_all(intervals):
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True
```

### Trace

```
intervals = [[0,30], [5,10], [15,20]]
sorted: [[0,30], [5,10], [15,20]]

i=1: intervals[1][0]=5 < intervals[0][1]=30? YES → return False ✅
(Meeting [5,10] starts before [0,30] ends)
```

```
intervals = [[1,5], [6,10], [11,15]]
sorted: [[1,5], [6,10], [11,15]]

i=1: 6 < 5? NO
i=2: 11 < 10? NO
return True ✅
```

### Edge Cases

**Edge case 1: Exact boundary (one ends when another starts)**
```
intervals = [[1,5], [5,10]]
i=1: 5 < 5? NO → return True ✅
(Back-to-back is not an overlap — meeting ends at 5, next starts at 5)
```

**Edge case 2: Single meeting**
```
intervals = [[1,5]]
Loop doesn't run (range(1,1))
return True ✅
```

### Complexity

> **Time: O(n log n)** (dominated by sort)
> **Space: O(1)** (or O(n) depending on sort implementation)

---

## Part 2: Minimum Number of Meeting Rooms

### Pattern Identification

**Pattern: Event Timeline (Sweep Line) or Min-Heap**

This is fundamentally harder than Part 1. We need to find the **maximum number of meetings overlapping at any point in time.** Two main approaches:

### Approach A: Sweep Line (What I Can Build Now)

**Insight:** Instead of thinking about intervals, think about **events.** Each meeting creates two events: a **start** (+1 room needed) and an **end** (-1 room freed). If we process all events in chronological order, the running count of rooms tells us how many are needed at each moment.

```python
def min_meeting_rooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))    # +1: meeting starts
        events.append((end, -1))     # -1: meeting ends

    events.sort()  # sort by time; ties: ends (-1) before starts (+1)

    current_rooms = 0
    max_rooms = 0

    for time, event_type in events:
        current_rooms += event_type
        max_rooms = max(max_rooms, current_rooms)

    return max_rooms
```

**Why the sort handles ties correctly:** When we sort tuples, `(5, -1)` comes before `(5, 1)`. This means if a meeting **ends** at time 5 and another **starts** at time 5, the end is processed first — the room is freed before the new meeting claims one. This matches the convention that back-to-back meetings don't overlap.

### Trace

```
intervals = [[0,30], [5,10], [15,20]]

events: [(0,1), (30,-1), (5,1), (10,-1), (15,1), (20,-1)]
sorted: [(0,1), (5,1), (10,-1), (15,1), (20,-1), (30,-1)]

(0,  +1): rooms=1, max=1    ← meeting [0,30] starts
(5,  +1): rooms=2, max=2    ← meeting [5,10] starts (overlaps with [0,30])
(10, -1): rooms=1, max=2    ← meeting [5,10] ends
(15, +1): rooms=2, max=2    ← meeting [15,20] starts (overlaps with [0,30])
(20, -1): rooms=1, max=2    ← meeting [15,20] ends
(30, -1): rooms=0, max=2    ← meeting [0,30] ends

return 2 ✅
```

### Edge Cases

**Edge case 1: No overlaps**
```
intervals = [[1,2], [3,4], [5,6]]
events sorted: [(1,1),(2,-1),(3,1),(4,-1),(5,1),(6,-1)]
rooms: 1,0,1,0,1,0 → max = 1 ✅
```

**Edge case 2: All overlap**
```
intervals = [[1,10], [2,10], [3,10]]
events sorted: [(1,1),(2,1),(3,1),(10,-1),(10,-1),(10,-1)]
rooms: 1,2,3,2,1,0 → max = 3 ✅
```

### Complexity

**STEP 1:** `intervals` → n = len(intervals)

**STEP 3:**
- Building events list: n iterations, O(1) each → **O(n)**. Produces 2n events.
- Sorting 2n events: **O(2n log 2n) = O(n log n)**
- Scanning events: 2n iterations, O(1) each → **O(n)**

**STEP 4:** O(n) + O(n log n) + O(n) = **O(n log n)**

**STEP 5:**
- `events` → 2n tuples → **O(n)**
- `current_rooms`, `max_rooms` → O(1)

> **Time: O(n log n), Space: O(n)**

### Approach B: Min-Heap (Acknowledged)

The heap approach is more commonly taught for this problem:
1. Sort intervals by start time
2. Maintain a min-heap of end times (one per active room)
3. For each meeting: if the earliest-ending room ends before this meeting starts, reuse it (pop from heap). Otherwise, allocate a new room.
4. Push the current meeting's end time onto the heap.
5. Answer = max size the heap ever reaches.

This requires a **heap data structure** (Week 6 material). The complexity is the same: **O(n log n) time, O(n) space.** The sweep line approach I used above is equally valid and arguably more elegant — it extends naturally to problems with weighted events and more complex overlapping queries.
