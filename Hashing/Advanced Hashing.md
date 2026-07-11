# HASH MAPS & HASH SETS — THE COMPLETE LESSON

---

# PART 1: WHAT HASHING ACTUALLY IS

## The Problem Hashing Solves

You have data. You want to:
- **Check if something exists** — fast
- **Look up a value by key** — fast
- **Count occurrences** — fast
- **Group things** — fast

Arrays give O(1) access **by index.** But what if your key isn't a nice integer from 0 to n-1? What if your key is a string, a tuple, a large number?

Hashing converts **any key** into an **array index.** That's it. That's the entire idea.

```
Key: "hello"  →  hash function  →  integer  →  mod table_size  →  index 3
Key: "world"  →  hash function  →  integer  →  mod table_size  →  index 7

Internal array: [_, _, _, "hello"→val, _, _, _, "world"→val, _, _]
                             ↑                        ↑
                          index 3                  index 7
```

## The Hash Function

A hash function takes an input of any size and produces a **fixed-size integer.**

```python
hash("hello")    # Some large integer, e.g., 2314058222102390712
hash(42)         # 42 (small integers hash to themselves in CPython)
hash((1, 2, 3))  # Some integer

# Then: index = hash(key) % table_size
```

### Properties of a Good Hash Function

```
1. DETERMINISTIC:    Same input always produces same output
2. UNIFORM:          Distributes keys evenly across the table
3. FAST:             O(1) to compute (for fixed-size keys)
4. AVALANCHE:        Small change in input → big change in output
                     hash("hello") and hash("hellp") should be very different
```

**Why uniform distribution matters:** If all keys hash to the same index, everything chains at one position → lookups degrade to O(n). Uniform spread means each position holds roughly 1 element → O(1) lookups.

## The Hash Table Data Structure

```
╔═══════════════════════════════════════════════════╗
║              HASH TABLE INTERNALS                  ║
╠═══════════════════════════════════════════════════╣
║                                                    ║
║  1. An internal ARRAY of fixed size (the table)    ║
║  2. A HASH FUNCTION that maps keys to indices      ║
║  3. A COLLISION RESOLUTION strategy                ║
║  4. A LOAD FACTOR threshold for resizing           ║
║                                                    ║
║  Insert(key, value):                               ║
║    index = hash(key) % table_size                  ║
║    store (key, value) at table[index]              ║
║    handle collision if slot occupied                ║
║                                                    ║
║  Lookup(key):                                      ║
║    index = hash(key) % table_size                  ║
║    check table[index]                              ║
║    if key matches, return value                    ║
║    if collision chain, search through chain        ║
║                                                    ║
║  Delete(key):                                      ║
║    find the entry (same as lookup)                 ║
║    remove it                                       ║
║                                                    ║
╚═══════════════════════════════════════════════════╝
```

---

# PART 2: COLLISION RESOLUTION

## Why Collisions Happen

A hash table has finite size (say 8 slots). The universe of possible keys is infinite (all possible strings). By the **pigeonhole principle,** multiple keys must map to the same slot.

```python
hash("apple") % 8  = 3
hash("banana") % 8 = 3    # Collision! Both want slot 3.
```

## Method 1: Chaining (Separate Chaining)

Each slot holds a **linked list** (or any collection) of all entries that hash to that index.

```
Index 0: → []
Index 1: → [("dog", 5)]
Index 2: → []
Index 3: → [("apple", 1) → ("banana", 2)]    ← collision chain
Index 4: → [("cat", 3)]
Index 5: → []
Index 6: → [("fish", 4)]
Index 7: → []
```

**Lookup "banana":** hash → index 3 → scan the chain at index 3 → find "banana" → return 2.

**Performance:** If the chain at one index has length k, lookup is O(k). With a good hash function and reasonable load factor, chains stay short (expected length ≈ 1). **Average: O(1). Worst: O(n) if all keys collide.**

## Method 2: Open Addressing

No chains. Every entry lives directly in the table array. On collision, **probe** for the next open slot.

### Linear Probing
Try slot hash(key), then hash(key)+1, then hash(key)+2, ...

```
Insert "apple" → index 3 → empty → store at 3
Insert "banana" → index 3 → occupied → try 4 → empty → store at 4
Insert "cherry" → index 3 → occupied → try 4 → occupied → try 5 → store at 5
```

**Problem: Clustering.** Consecutive filled slots create long probe sequences. One collision makes future collisions at nearby slots more likely.

### Quadratic Probing
Try slot hash(key), then hash(key)+1², then hash(key)+2², then hash(key)+3², ...

Reduces clustering compared to linear probing.

### Double Hashing
Use a second hash function to determine the probe step: hash(key) + i × hash2(key).

Most uniform, but more complex.

## What Python Uses

**Python `dict` uses open addressing** with a sophisticated probing strategy (perturbed hash probing). It's not simple linear probing — Python's probe sequence depends on **all bits** of the hash, not just the lower bits.

**Python `set` uses the same mechanism** — it's essentially a hash table storing only keys (no values).

You don't need to implement collision resolution. You need to understand it so you can:
1. Explain O(1) average / O(n) worst to an interviewer
2. Know why certain inputs can cause worst-case behavior
3. Understand why load factor matters

---

# PART 3: LOAD FACTOR AND RESIZING

## Load Factor

```
load_factor = number_of_entries / table_size
```

As load factor increases, collisions become more frequent, and performance degrades.

| Load Factor | Behavior |
|---|---|
| < 0.5 | Fast. Few collisions. |
| 0.5 - 0.7 | Good. Acceptable collision rate. |
| 0.7 - 1.0 | Slowing. Longer probe chains. |
| > 1.0 | Only possible with chaining. Performance degrades significantly. |

## Resizing (Rehashing)

When load factor exceeds a threshold, the table:
1. Allocates a **new, larger** array (typically 2x)
2. **Rehashes every existing entry** into the new array
3. Discards the old array

```
Old table (size 4, load 3/4 = 0.75):
[_, ("a",1), ("b",2), ("c",3)]

Resize to size 8, rehash all:
[_, _, ("a",1), _, _, ("b",2), ("c",3), _]
(positions change because hash(key) % 8 ≠ hash(key) % 4)
```

**Cost of resize: O(n)** — must touch every entry. But this happens rarely (every time size doubles). **Amortized over all insertions: O(1) per insert.** Same argument as dynamic array `.append()`.

Python dicts resize when load factor reaches about **2/3 (≈ 0.67).**

---

# PART 4: WHAT'S HASHABLE IN PYTHON

## The Rule

**Only immutable objects are hashable.** Because if an object changes after being inserted, its hash changes, and the table can't find it anymore.

```python
# ✅ HASHABLE (immutable)
hash(42)           # int
hash(3.14)         # float
hash("hello")      # str
hash((1, 2, 3))    # tuple (if all elements are hashable)
hash(True)         # bool
hash(frozenset({1,2}))  # frozenset
hash(None)         # NoneType

# ❌ NOT HASHABLE (mutable)
hash([1, 2, 3])    # TypeError: unhashable type: 'list'
hash({1, 2, 3})    # TypeError: unhashable type: 'set'
hash({"a": 1})     # TypeError: unhashable type: 'dict'
```

## Why This Matters for DSA

You'll often need to use **collections as dictionary keys** or **set elements.** The workarounds:

```python
# Want to use a list as a key?
# Convert to tuple
d = {}
d[tuple([1, 2, 3])] = "value"    # ✅

# Want to use a set as a key?
# Convert to frozenset
d[frozenset({1, 2})] = "value"   # ✅

# Want to use a dict as a key?
# Convert to tuple of sorted items
d[tuple(sorted({"a": 1, "b": 2}.items()))] = "value"  # ✅
```

This comes up **constantly** in problems like Group Anagrams (you already used `tuple(sorted(s))` as a key — now you know exactly why it works and why `sorted(s)` alone wouldn't work as a key since it returns a list).

---

# PART 5: PYTHON DICT — COMPLETE REFERENCE

## Operations and Complexity

```
╔══════════════════════════════════════════════════════════════════╗
║                    PYTHON DICT OPERATIONS                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  CREATION                                                        ║
║  d = {}                          O(1)                            ║
║  d = dict(pairs)                 O(n)     From iterable          ║
║  d = {k: v for k, v in items}    O(n)     Dict comprehension     ║
║                                                                  ║
║  ACCESS                                                          ║
║  d[key]                          O(1)*    KeyError if missing     ║
║  d.get(key)                      O(1)*    Returns None if missing ║
║  d.get(key, default)             O(1)*    Returns default         ║
║  key in d                        O(1)*    Membership test         ║
║  len(d)                          O(1)     Stored attribute         ║
║                                                                  ║
║  MODIFICATION                                                    ║
║  d[key] = value                  O(1)*    Insert or update        ║
║  d.setdefault(key, default)      O(1)*    Insert if missing       ║
║  d.update(other)                 O(k)     k = len(other)          ║
║  del d[key]                      O(1)*    KeyError if missing     ║
║  d.pop(key)                      O(1)*    Remove and return       ║
║  d.pop(key, default)             O(1)*    No error if missing     ║
║  d.clear()                       O(n)     Remove all              ║
║                                                                  ║
║  ITERATION                                                       ║
║  d.keys()                        O(1)     Returns view object     ║
║  d.values()                      O(1)     Returns view object     ║
║  d.items()                       O(1)     Returns view object     ║
║  for k in d:                     O(n)     Iterates keys           ║
║  for k, v in d.items():          O(n)     Iterates pairs          ║
║                                                                  ║
║  COPY                                                            ║
║  d.copy()                        O(n)     Shallow copy            ║
║                                                                  ║
║  * = O(1) average, O(n) worst case due to hash collisions        ║
╚══════════════════════════════════════════════════════════════════╝
```

## The Four Ways to Handle Missing Keys

This comes up in **every** hash map problem. Know all four:

```python
# Method 1: Check first
if key not in d:
    d[key] = default_value
d[key] += 1

# Method 2: .get() with default
d[key] = d.get(key, 0) + 1

# Method 3: .setdefault()
d.setdefault(key, []).append(item)
# If key missing: inserts key with [] then appends
# If key exists: just appends

# Method 4: defaultdict (best for most DSA)
from collections import defaultdict
d = defaultdict(int)    # Missing key → 0
d[key] += 1             # No check needed

d = defaultdict(list)   # Missing key → []
d[key].append(item)     # No check needed

d = defaultdict(set)    # Missing key → set()
d[key].add(item)        # No check needed
```

**Which to use:**
- Quick one-off → `.get(key, default)`
- Repeated accumulation → `defaultdict`
- Interview: either is fine, but `defaultdict` is cleaner

## `Counter` — The Counting Specialist

```python
from collections import Counter

# Count from iterable
c = Counter("aabbbcccc")    # {'c': 4, 'b': 3, 'a': 2}
c = Counter([1, 2, 2, 3])   # {2: 2, 1: 1, 3: 1}

# Access
c['a']        # 2
c['z']        # 0 (no KeyError!)

# Most common
c.most_common(2)    # [('c', 4), ('b', 3)]

# Arithmetic
c1 = Counter("aab")     # {'a': 2, 'b': 1}
c2 = Counter("abb")     # {'a': 1, 'b': 2}
c1 + c2                  # {'a': 3, 'b': 3}
c1 - c2                  # {'a': 1}  (drops zero/negative)
c1 & c2                  # {'a': 1, 'b': 1}  (minimum of each)
c1 | c2                  # {'a': 2, 'b': 2}  (maximum of each)

# Total count
c.total()      # Python 3.10+: sum of all counts
sum(c.values())  # Works in all versions

# Check if one Counter is a "subset" of another
# (all counts ≤ corresponding counts in other)
all(c1[k] <= c2[k] for k in c1)
# Or: not (c1 - c2)  (subtraction drops positives; if empty, c1 ⊆ c2)
```

**Counter is your best friend for:**
- Character frequency problems
- Anagram checking (`Counter(s) == Counter(t)`)
- Finding top-k elements
- Multiset operations

---

# PART 6: PYTHON SET — COMPLETE REFERENCE

## What a Set Is

A set is a hash table that stores **only keys** (no values). It provides O(1) membership testing, insertion, and deletion.

## Operations and Complexity

```
╔══════════════════════════════════════════════════════════════════╗
║                    PYTHON SET OPERATIONS                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  CREATION                                                        ║
║  s = set()                       O(1)                            ║
║  s = {1, 2, 3}                   O(n)                            ║
║  s = set(iterable)               O(n)                            ║
║                                                                  ║
║  ELEMENT OPERATIONS                                              ║
║  x in s                          O(1)*    Membership test         ║
║  s.add(x)                        O(1)*    Add element             ║
║  s.remove(x)                     O(1)*    Remove (KeyError)       ║
║  s.discard(x)                    O(1)*    Remove (no error)       ║
║  s.pop()                         O(1)     Remove arbitrary         ║
║  len(s)                          O(1)                             ║
║                                                                  ║
║  SET OPERATIONS                                                  ║
║  s1 | s2     s1.union(s2)        O(n+m)   Union                  ║
║  s1 & s2     s1.intersection(s2) O(min(n,m)) Intersection        ║
║  s1 - s2     s1.difference(s2)   O(n)     Difference              ║
║  s1 ^ s2     s1.symmetric_difference(s2) O(n+m) Sym. diff.       ║
║                                                                  ║
║  SUBSET / SUPERSET                                               ║
║  s1 <= s2    s1.issubset(s2)     O(n)     n = len(s1)            ║
║  s1 >= s2    s1.issuperset(s2)   O(m)     m = len(s2)            ║
║  s1 < s2                         O(n)     Proper subset           ║
║                                                                  ║
║  IN-PLACE OPERATIONS                                             ║
║  s1 |= s2    s1.update(s2)      O(m)     Add all from s2         ║
║  s1 &= s2                       O(n)     Keep only common        ║
║  s1 -= s2                        O(m)     Remove all in s2        ║
║                                                                  ║
║  * = O(1) average, O(n) worst case                               ║
╚══════════════════════════════════════════════════════════════════╝
```

## When Set vs Dict

```
USE SET WHEN:
- You only care about EXISTENCE (is this element present?)
- Deduplication (unique elements)
- Set operations (union, intersection, difference)

USE DICT WHEN:
- You need to associate a VALUE with each key
- Counting (key → count)
- Grouping (key → list of items)
- Mapping (key → transformed value)
```

## `frozenset` — The Immutable Set

```python
# frozenset is to set what tuple is to list
fs = frozenset({1, 2, 3})
# Can be used as dict key or set element
d = {frozenset({1, 2}): "pair"}
s = {frozenset({1, 2}), frozenset({3, 4})}
```

---

# PART 7: THE HASH MAP PATTERNS

These are the **core patterns** that appear in 80% of hash map interview problems.

## Pattern 1: Counting / Frequency Map

**Signal:** "How many times does each element appear?" "Most frequent?" "Elements appearing more than k times?"

```python
def frequency_map(arr):
    count = {}
    for x in arr:
        count[x] = count.get(x, 0) + 1
    return count

# Or simply: Counter(arr)
```

### Example: First Unique Character in String

```python
def first_unique_char(s):
    count = Counter(s)
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    return -1
```

Time: O(n). Space: O(1) for bounded alphabet.

### Example: Top K Frequent Elements

```python
def top_k_frequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in count.most_common(k)]
```

Time: O(n + k log n) for `most_common`. Can be O(n) with bucket sort — see below.

**Bucket sort approach (truly O(n)):**

```python
def top_k_frequent(nums, k):
    count = Counter(nums)
    # Bucket: index = frequency, value = list of elements with that frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

Time: O(n). Space: O(n).

---

## Pattern 2: Complement Lookup (Two Sum Family)

**Signal:** "Find pair/group satisfying a condition." "Find complement." "Does x exist such that f(x) = target?"

The core idea: for each element, compute what you **need** (the complement), check if you've **seen** it.

```python
# Template
seen = {}
for i, x in enumerate(arr):
    complement = compute_complement(x, target)
    if complement in seen:
        process(seen[complement], i)
    seen[x] = i
```

### Two Sum (You've Done This)

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
```

### Variant: Count Pairs With Difference = k

```python
def count_pairs_diff_k(nums, k):
    count = 0
    seen = set()
    for num in nums:
        if num + k in seen:
            count += 1
        if num - k in seen:
            count += 1
        seen.add(num)
    return count
```

### Variant: Four Sum II (Two Arrays at a Time)

Given four arrays A, B, C, D, count tuples (i,j,k,l) where A[i]+B[j]+C[k]+D[l]=0.

```python
def four_sum_count(A, B, C, D):
    ab_sums = Counter()
    for a in A:
        for b in B:
            ab_sums[a + b] += 1
    
    count = 0
    for c in C:
        for d in D:
            count += ab_sums[-(c + d)]
    return count
```

Time: O(n²). Space: O(n²). Without hashing, this would be O(n⁴).

---

## Pattern 3: Grouping / Categorization

**Signal:** "Group by property." "Find all elements sharing a characteristic."

```python
# Template
groups = defaultdict(list)
for item in data:
    key = compute_key(item)
    groups[key].append(item)
```

### Group Anagrams (You've Done This)

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())
```

### Group by Frequency

```python
def group_by_frequency(nums):
    freq = Counter(nums)
    groups = defaultdict(list)
    for num, count in freq.items():
        groups[count].append(num)
    return dict(groups)
```

---

## Pattern 4: Existence / Seen Before

**Signal:** "Have we encountered this before?" "Any duplicates?" "First repeated element?"

```python
def has_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

### Contains Duplicate II (Within Distance k)

```python
def contains_nearby_duplicate(nums, k):
    seen = {}  # value → most recent index
    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i
    return False
```

### Longest Consecutive Sequence

Given unsorted array, find the length of the longest consecutive element sequence. **Must be O(n).**

```python
def longest_consecutive(nums):
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # Only start counting from the BEGINNING of a sequence
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            max_length = max(max_length, length)
    
    return max_length
```

**Why this is O(n) and not O(n²):** The `if num - 1 not in num_set` check ensures we only start the while loop at the **beginning** of each sequence. Each element is visited by the while loop at most once (as part of exactly one sequence). Total while loop iterations across all outer iterations = n.

This is a **FAANG classic.** The "only start from the beginning" trick is the key insight.

---

## Pattern 5: Prefix Sum + Hash Map

**Signal:** "Subarray with sum = k." "Number of subarrays satisfying condition."

You used this in the Retention Grill (C1). Here's the general pattern:

```python
def subarray_sum_equals_k(nums, k):
    prefix_count = {0: 1}  # prefix_sum → count of occurrences
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        complement = current_sum - k
        if complement in prefix_count:
            count += prefix_count[complement]
        prefix_count[current_sum] = prefix_count.get(current_sum, 0) + 1
    
    return count
```

**Why `{0: 1}`?** A prefix sum of 0 means the subarray from index 0 to the current position sums to `current_sum`. If `current_sum == k`, we need to find `complement = k - k = 0` in the map. The initial `{0: 1}` accounts for this "empty prefix" case.

**Why store count, not just existence?** If the same prefix sum appears multiple times, each occurrence represents a different starting point for a valid subarray.

```
arr = [1, 1, 1], k = 2

prefix sums: 0, 1, 2, 3
At sum=2: complement=0, found once → 1 subarray [1,1]
At sum=3: complement=1, found once → 1 subarray [1,1] starting at index 1

But consider arr = [0, 0, 0], k = 0:
prefix sums: 0, 0, 0, 0
At first 0: complement=0, found 1 time → 1 subarray
At second 0: complement=0, found 2 times → 2 subarrays
At third 0: complement=0, found 3 times → 3 subarrays
Total: 6 subarrays (all 6 subarrays of [0,0,0] sum to 0)
```

---

## Pattern 6: Index Mapping

**Signal:** "Find positions where condition holds." "Map values back to their original indices."

```python
def two_sum_indices(nums, target):
    index_map = {}  # value → index
    for i, num in enumerate(nums):
        if target - num in index_map:
            return [index_map[target - num], i]
        index_map[num] = i
```

### Intersection of Two Arrays (with indices)

```python
def intersect_with_counts(nums1, nums2):
    count = Counter(nums1)
    result = []
    for num in nums2:
        if count[num] > 0:
            result.append(num)
            count[num] -= 1
    return result
```

---

## Pattern 7: Design / Custom Hash

**Signal:** "Design a data structure that supports X in O(1)." "Implement LRU cache." "Insert/delete/getRandom in O(1)."

### Insert Delete GetRandom O(1)

```python
import random

class RandomizedSet:
    def __init__(self):
        self.val_to_index = {}  # value → index in list
        self.values = []        # dynamic array
    
    def insert(self, val):
        if val in self.val_to_index:
            return False
        self.val_to_index[val] = len(self.values)
        self.values.append(val)
        return True
    
    def remove(self, val):
        if val not in self.val_to_index:
            return False
        # Swap with last element, then pop
        idx = self.val_to_index[val]
        last = self.values[-1]
        self.values[idx] = last
        self.val_to_index[last] = idx
        self.values.pop()
        del self.val_to_index[val]
        return True
    
    def getRandom(self):
        return random.choice(self.values)
```

**The trick:** Array gives O(1) random access (for getRandom). Dict gives O(1) lookup (for insert/remove). To delete from the array in O(1), **swap with the last element and pop** — avoids shifting.

This is a common FAANG design problem.

---

# PART 8: ADVANCED HASHING CONCEPTS

## Designing Hash Keys

When the problem requires grouping or deduplication of **complex objects,** you need to design a canonical hash key.

```python
# Anagram grouping: sorted characters
key = tuple(sorted(word))

# Frequency-based grouping: frequency tuple
key = tuple(Counter(word).values())  # ❌ Not unique! Order matters
key = tuple(sorted(Counter(word).items()))  # ✅

# Even better for character frequency:
count = [0] * 26
for c in word:
    count[ord(c) - ord('a')] += 1
key = tuple(count)  # ✅ O(k) instead of O(k log k)

# Grid state in BFS (like puzzle games):
key = tuple(tuple(row) for row in grid)

# Point set:
key = frozenset(points)

# Sorted pair:
key = (min(a, b), max(a, b))
```

**Design principle:** The key must be the **same for equivalent inputs** and **different for non-equivalent inputs.** It must also be **hashable** (immutable).

## Hash Collisions in Competitive Programming

In CP, adversarial test cases can be designed to make hash maps degrade to O(n) per operation:

**The attack:** If the hash function is known, craft inputs where all keys hash to the same bucket. Python's `dict` uses predictable hashing for integers.

**Defense strategies:**
1. **Randomized hash salt** — add a random offset to keys before hashing
2. **Use `sorted` for ordering-dependent operations** — avoid hash maps when deterministic performance is needed
3. **In Python:** integer hashing is `hash(x) = x` for small integers. For CP, if you need guaranteed O(n) total, consider sorting-based approaches instead of hash-based when the constant factor matters

For FAANG interviews, this rarely matters. For CP at the highest level, it can.

---

# PART 9: COMMON TRAPS AND PITFALLS

## Trap 1: Mutating While Iterating

```python
# ❌ RuntimeError: dictionary changed size during iteration
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    if d[key] < 2:
        del d[key]

# ✅ Iterate over a copy of keys
for key in list(d.keys()):
    if d[key] < 2:
        del d[key]

# ✅ Or build a new dict
d = {k: v for k, v in d.items() if v >= 2}
```

## Trap 2: Default Mutable Argument

```python
# ❌ DANGEROUS — shared across all calls
def add_to_dict(key, value, d={}):
    d[key] = value
    return d

# ✅ Use None as sentinel
def add_to_dict(key, value, d=None):
    if d is None:
        d = {}
    d[key] = value
    return d
```

## Trap 3: Counter Subtraction Drops Non-Positive

```python
c1 = Counter({'a': 3, 'b': 1})
c2 = Counter({'a': 1, 'b': 5})
c1 - c2  # Counter({'a': 2})  — 'b' is GONE, not -4
```

If you need to keep negative counts, subtract manually:
```python
for k in c2:
    c1[k] -= c2[k]
```

## Trap 4: `dict` Preserves Insertion Order (Python 3.7+)

Since Python 3.7, dictionaries maintain **insertion order.** This is guaranteed by the language spec. You can rely on it in interviews and CP.

```python
d = {'b': 1, 'a': 2, 'c': 3}
list(d.keys())  # ['b', 'a', 'c'] — insertion order preserved
```

Before 3.7, dicts were unordered. `OrderedDict` from `collections` was needed. Now `OrderedDict` is only useful if you need `move_to_end()` or `popitem(last=True/False)` functionality (relevant for LRU cache).

## Trap 5: Hashing Floats

```python
hash(1.0) == hash(1)  # True! 1.0 == 1 in Python
d = {1: "int"}
d[1.0]  # Returns "int"! Because 1.0 == 1, same hash
```

Don't mix ints and floats as dict keys unless you're aware of this.

---

# PART 10: HASH MAP PATTERN DECISION FRAMEWORK

```
╔═══════════════════════════════════════════════════════════════════╗
║               HASH MAP PATTERN SELECTOR                           ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  "Count / frequency of elements"                                  ║
║    → Counter or defaultdict(int)                                  ║
║                                                                   ║
║  "Find pair / complement"                                         ║
║    → Single-pass with seen dict (value → index)                   ║
║                                                                   ║
║  "Group elements by property"                                     ║
║    → defaultdict(list) with canonical key                         ║
║                                                                   ║
║  "Any duplicates? / Seen before?"                                 ║
║    → Set                                                          ║
║                                                                   ║
║  "Subarray sum = k"                                               ║
║    → Prefix sum + hash map                                        ║
║                                                                   ║
║  "Longest consecutive sequence"                                   ║
║    → Set + start-of-sequence check                                ║
║                                                                   ║
║  "Design O(1) data structure"                                     ║
║    → Dict + array (value ↔ index mapping)                         ║
║                                                                   ║
║  "Sliding window with frequency tracking"                         ║
║    → Dict/Counter as window state                                 ║
║                                                                   ║
║  "Check if two things are equivalent"                             ║
║    → Hash both with same canonical key, compare                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

# PART 11: TRACED EXEMPLARS (CAP = 3)

**Craft rule:** In-lesson solutions stop at **3** full traces. Rest → Retention + Spine + problem-bank.

Attempt blind. Answers for exemplars follow the prompts.

---

### Problem 1: Two Sum (Hash Map — Warm-Up)

Given an array and target, return indices of two numbers that sum to target. Each input has exactly one solution. You may not use the same element twice.

```
Input: nums = [3, 2, 4], target = 6
Output: [1, 2]
```

*(Yes, you've done this before. Do it again from memory — prove retention.)*

---

### Problem 2: Longest Consecutive Sequence

Given an unsorted array of integers, find the length of the longest consecutive elements sequence. **Must run in O(n) time.**

```
Input: [100, 4, 200, 1, 3, 2]
Output: 4 (sequence: [1, 2, 3, 4])
```

---

### Problem 3: Subarray Sum Equals K

Given an array of integers and an integer k, return the **total number** of subarrays whose sum equals k.

```
Input: nums = [1, 1, 1], k = 2
Output: 2
```

---


---

# ANSWER KEY — EXEMPLARS ONLY

# Problem 1: Two Sum (From Memory)

## Solution

```python
def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## Trace

```
nums = [3, 2, 4], target = 6

i=0, num=3: comp=3, 3 in {}? NO → seen={3:0}
i=1, num=2: comp=4, 4 in {3:0}? NO → seen={3:0, 2:1}
i=2, num=4: comp=2, 2 in {3:0, 2:1}? YES → return [1, 2] ✅
```

## Edge Cases

**Same value twice:** `nums=[3,3], target=6` → i=0 stores 3:0, i=1 finds comp=3 at index 0 → [0,1] ✅

**Negative numbers:** `nums=[-1, 5], target=4` → i=0 comp=5 not found, i=1 comp=-1 found → [0,1] ✅

## Complexity

> **Time: O(n), Space: O(n)**

---

# Problem 2: Longest Consecutive Sequence

## Pattern: Hash Set + Sequence Start Detection

## Solution

```python
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            longest = max(longest, length)

    return longest
```

## Trace

```
nums = [100, 4, 200, 1, 3, 2]
num_set = {100, 4, 200, 1, 3, 2}

num=100: 99 not in set → start! 101 not in set → length=1. longest=1
num=4: 3 in set → SKIP (not a start)
num=200: 199 not in set → start! 201 not in set → length=1. longest=1
num=1: 0 not in set → start!
       2 in set → length=2, 3 in set → length=3, 4 in set → length=4
       5 not in set → stop. longest=4
num=3: 2 in set → SKIP
num=2: 1 in set → SKIP

return 4 ✅
```

## Edge Cases

**Empty array:** `nums=[]` → loop doesn't run → return 0 ✅

**Duplicates:** `nums=[1,2,2,3]` → set={1,2,3}. Start at 1, count 1→2→3 = length 3 ✅

## Complexity

Total while loop iterations across all outer iterations = n (each element is extended through at most once).

> **Time: O(n), Space: O(n)**

---

# Problem 3: Subarray Sum Equals K

## Pattern: Prefix Sum + Hash Map (Frequency Count)

## Solution

```python
def subarray_sum(nums, k):
    prefix_counts = {0: 1}
    current_sum = 0
    count = 0

    for num in nums:
        current_sum += num
        complement = current_sum - k
        if complement in prefix_counts:
            count += prefix_counts[complement]
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return count
```

## Trace

```
nums = [1, 1, 1], k = 2
prefix_counts = {0: 1}, current_sum = 0, count = 0

num=1: sum=1, comp=-1, not found. prefix_counts={0:1, 1:1}
num=1: sum=2, comp=0, found(1) → count=1. prefix_counts={0:1, 1:1, 2:1}
num=1: sum=3, comp=1, found(1) → count=2. prefix_counts={0:1, 1:1, 2:1, 3:1}

return 2 ✅ ([1,1] at index 0-1, [1,1] at index 1-2)
```

## Edge Cases

**Single element equals k:** `nums=[5], k=5` → sum=5, comp=0, found → count=1 ✅

**Negatives:** `nums=[1,-1,0], k=0` → sums: 1,0,0. At sum=0 (i=1): comp=0, found once → count=1. At sum=0 (i=2): comp=0, found twice (0 appeared at index -1 and index 1) → count=3. Subarrays: [1,-1], [1,-1,0], [0] ✅

## Complexity

> **Time: O(n), Space: O(n)**

---


---

## Rest of the old in-lesson bank

Drill via Retention Questions + `Practice Spines/Phase A MVP Spines.md` + `problem-bank/`. Do not paste full solutions back into this lesson.

## Teach-back

Explain the core frameworks from earlier parts without notes, then open Retention (questions-only).

