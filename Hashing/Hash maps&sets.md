# HASH MAPS & HASH SETS — THE COMPLETE LESSON

---

> **Lesson contract:** Read framework + patterns first. Cap in-lesson traces at a few exemplars; drill from Retention + Spine. Answers for retention live under `Retention Questions/keys/`.


# PART 1: HOW HASHING ACTUALLY WORKS

## 1A: The Problem Hashing Solves

You have an array of 1 million user IDs. Someone asks: "Is user ID 7294 in this array?"

**With an array (unsorted):** Scan every element. O(n). For 1 million elements, that's 1 million comparisons.

**With a sorted array + binary search:** O(log n). About 20 comparisons. Better. But you must keep it sorted — insertion becomes O(n).

**The dream:** Check if 7294 exists in **O(1).** One step. Regardless of whether you have 100 elements or 100 billion.

That's what hashing gives you. Not approximately O(1). Not O(1) most of the time. **O(1) average case** for lookup, insertion, and deletion by value.

The question is: **how?**

---

## 1B: Hash Functions — The Core Mechanism

A **hash function** takes any input and produces a **fixed-size integer** (called the hash or hash code).

```
hash("hello")   → 840651671246  (some large integer)
hash("world")   → 279837264891  (different large integer)
hash(42)         → 42            (Python hashes small ints to themselves)
hash((1, 2, 3)) → 529344067295497451
```

**Properties of a good hash function:**

1. **Deterministic:** Same input ALWAYS produces same output. `hash("hello")` returns the same number every time (within one program execution).

2. **Uniform distribution:** Different inputs should spread out across the output range as evenly as possible. If all inputs hash to the same number, the whole system breaks.

3. **Fast to compute:** The hash itself must be O(1) or close to it. If computing the hash takes O(n), you've lost the speed advantage.

**The simplest hash function — modulo:**

```
hash(key) = key % table_size
```

If table_size = 10:
```
hash(42)  = 42 % 10  = 2
hash(17)  = 17 % 10  = 7
hash(103) = 103 % 10 = 3
hash(52)  = 52 % 10  = 2    ← COLLISION! Same bucket as 42
```

For strings, Python computes a hash based on the characters:

```python
hash("abc")  # Some integer based on character values and positions
```

You don't need to know the exact formula. You need to know that:
- It exists
- It's fast (O(length of string) the first time, cached after)
- It produces an integer that determines where the data goes

---

## 1C: Hash Tables — The Complete Picture

A hash table is an **array of buckets.** The hash function determines which bucket to use.

**The complete path from key to storage:**

```
key → hash(key) → index = hash(key) % table_size → bucket[index]
```

Visual example with table_size = 8:

```
Step 1: hash("alice") = 2847261
Step 2: index = 2847261 % 8 = 5
Step 3: Store "alice" in bucket[5]

Buckets:
[0]: empty
[1]: empty
[2]: empty
[3]: empty
[4]: empty
[5]: "alice"    ← here
[6]: empty
[7]: empty
```

**Lookup works the same way:**

```
"Is alice in the table?"
Step 1: hash("alice") = 2847261
Step 2: index = 2847261 % 8 = 5
Step 3: Check bucket[5] → found "alice" ✅
```

No scanning. No searching. Direct jump to the right bucket. **O(1).**

**Insertion:**

```
"Add bob"
hash("bob") = 1938472
index = 1938472 % 8 = 0
Store "bob" in bucket[0]

Buckets:
[0]: "bob"
[1]: empty
[2]: empty
[3]: empty
[4]: empty
[5]: "alice"
[6]: empty
[7]: empty
```

**Deletion:**

```
"Remove alice"
hash("alice") = 2847261
index = 2847261 % 8 = 5
Clear bucket[5]
```

All three operations: compute hash (O(1)), compute index (O(1)), access bucket (O(1)). **O(1) total.**

---

## 1D: Collisions — The Inevitable Problem

What happens when two different keys hash to the **same bucket?**

```
hash("alice") % 8 = 5
hash("charlie") % 8 = 5    ← SAME BUCKET!
```

This WILL happen. It's mathematically guaranteed by the **pigeonhole principle:** if you have more possible keys than buckets (and you always do), some keys must share buckets.

Two main strategies to handle this:

### Strategy 1: Chaining

Each bucket holds a **linked list** (or any list) of all entries that hashed to that index.

```
Buckets:
[0]: bob → None
[1]: empty
[2]: empty
[3]: empty
[4]: empty
[5]: alice → charlie → None    ← Both live here
[6]: empty
[7]: empty
```

**Lookup with chaining:**
1. Compute index: O(1)
2. Walk the chain at that index, comparing keys: O(length of chain)

If the hash function distributes well and the table isn't overloaded, chains are short (average length ~1). **O(1) average.**

If everything hashes to the same bucket (worst case): one chain of length n. **O(n) worst case.** This is why hash table operations are O(1) **average**, not O(1) guaranteed.

### Strategy 2: Open Addressing

No chains. Each bucket holds exactly one entry. If a collision occurs, **probe** for the next empty bucket.

**Linear probing:** If bucket 5 is taken, try 6. If 6 is taken, try 7. And so on.

```
Insert "alice" → bucket 5
Insert "charlie" → bucket 5 taken → try 6 → empty → store at 6

Buckets:
[0]: bob
[1]: empty
[2]: empty
[3]: empty
[4]: empty
[5]: alice
[6]: charlie    ← probed here after collision
[7]: empty
```

**Problem: clustering.** Filled regions grow, making future probes longer. Performance degrades as the table fills up.

**Python's dict** uses a modified version of open addressing with a more sophisticated probing sequence to reduce clustering.

### Load Factor

```
load_factor = number_of_entries / table_size
```

When the load factor exceeds a threshold (typically 0.7), the table **resizes** — creates a new, larger table and rehashes all entries.

This is identical to how dynamic arrays resize on append. Occasional O(n) rehash, but amortized across many operations, the cost per operation stays O(1).

---

## 1E: When Hashing Fails

### Worst Case: All Keys Collide

If an adversary knows your hash function, they can craft inputs that ALL hash to the same bucket. Every operation becomes O(n).

**Where this matters:**

- **Competitive programming:** Some problems have adversarial test cases designed to break hash maps. Mitigations: use randomized hash functions, or use C++ `unordered_map` with custom hash.

- **System design:** HashDoS attacks send crafted HTTP parameters that all collide, turning your O(1) server into O(n). Mitigations: randomized hash seeds (Python does this by default since 3.3), rate limiting.

- **Interviews:** You should know this exists. When you say "O(1) average," an interviewer might ask "what's the worst case?" Answer: "O(n) due to hash collisions, but with a good hash function and reasonable load factor, this is extremely rare in practice."

### Python's Protection

Python randomizes hash seeds on each program start. `hash("hello")` gives different values each time you run the program. This prevents precomputed collision attacks.

```python
# Run 1: hash("hello") = 7382649172
# Run 2: hash("hello") = -2948571028
# Within one run: always the same
```

---

## 1F: Hash Function Rules for Python Types

**What can be hashed?**

The rule is: **only immutable objects are hashable.**

| Type | Hashable? | Why |
|---|---|---|
| `int` | ✅ Yes | Immutable |
| `float` | ✅ Yes | Immutable (but avoid as dict keys — precision issues) |
| `str` | ✅ Yes | Immutable |
| `bool` | ✅ Yes | Immutable (True hashes like 1, False like 0) |
| `None` | ✅ Yes | Immutable |
| `tuple` | ✅ If all elements are hashable | Immutable container |
| `frozenset` | ✅ Yes | Immutable set |
| `list` | ❌ No | Mutable — could change after hashing |
| `dict` | ❌ No | Mutable |
| `set` | ❌ No | Mutable |

**Why mutable objects can't be hashed:**

Imagine you hash a list `[1, 2, 3]` and store it at bucket 5. Then you modify the list to `[1, 2, 4]`. Its hash would now point to bucket 3. But the data is still at bucket 5. The table is **broken.** You can never find it again.

**The practical consequence:**

```python
# Need a list as a dict key? Convert to tuple.
d = {}
d[tuple([1, 2, 3])] = "value"    # ✅

# Need a set as a dict key? Convert to frozenset.
d[frozenset({1, 2, 3})] = "value"    # ✅

# Need a dict as a key? Convert to tuple of sorted items.
d[tuple(sorted(other_dict.items()))] = "value"    # ✅
```

These conversions appear constantly in interview problems, especially when hashing complex states.

---

# PART 2: PYTHON'S HASH-BASED DATA STRUCTURES

## 2A: Sets

A set is an **unordered collection of unique hashable elements**, backed by a hash table.

### Creation

```python
s = set()                    # Empty set
s = {1, 2, 3}               # Literal (NOT {} — that's an empty dict!)
s = set([1, 2, 2, 3, 3])    # From iterable → {1, 2, 3} (deduped)
s = set("hello")             # {'h', 'e', 'l', 'o'} (unique chars)
```

**Trap:** `{}` creates an empty **dict**, NOT a set. Use `set()` for empty sets.

### Core Operations

```python
s = {1, 2, 3}

s.add(4)            # {1, 2, 3, 4}     O(1) avg
s.remove(2)         # {1, 3, 4}         O(1) avg — KeyError if missing!
s.discard(99)       # {1, 3, 4}         O(1) avg — NO error if missing
s.pop()             # Removes arbitrary element  O(1)
3 in s              # True               O(1) avg
len(s)              # 3                  O(1)
s.clear()           # set()              O(1)
```

**`remove` vs `discard`:** Use `discard` when you're not sure if the element exists. Use `remove` when it should exist and absence is a bug.

### Set Algebra — The Power Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b     # Union:          {1, 2, 3, 4, 5, 6}    O(len(a) + len(b))
a & b     # Intersection:   {3, 4}                  O(min(len(a), len(b)))
a - b     # Difference:     {1, 2}                  O(len(a))
a ^ b     # Symmetric diff: {1, 2, 5, 6}            O(len(a) + len(b))
a <= b    # Subset check:   False                    O(len(a))
a >= b    # Superset check: False                    O(len(b))
```

**When set algebra is useful:**
- Finding common elements between two collections → intersection
- Finding elements in one but not another → difference
- Checking if all required items are present → subset

```python
# Example: Does the user have all required permissions?
required = {"read", "write", "execute"}
user_perms = {"read", "write", "execute", "admin"}
has_all = required <= user_perms    # True — required is subset of user_perms
```

### frozenset — The Immutable Set

```python
fs = frozenset([1, 2, 3])
# Can be used as dict key or set element
d = {fs: "some value"}          # ✅
s = {frozenset({1,2}), frozenset({3,4})}  # set of sets ✅
```

You need frozenset when you want to use a **set as a key.** Regular sets are mutable and unhashable.

---

## 2B: Dictionaries

A dict is a **key-value mapping** backed by a hash table. Keys must be hashable. Values can be anything.

### Creation

```python
d = {}                                    # Empty dict
d = {"name": "alice", "age": 25}         # Literal
d = dict(name="alice", age=25)           # Keyword args
d = {x: x**2 for x in range(5)}         # Comprehension: {0:0, 1:1, 2:4, 3:9, 4:16}
d = dict.fromkeys(["a", "b", "c"], 0)   # {"a": 0, "b": 0, "c": 0}
```

### Core Operations

```python
d = {"a": 1, "b": 2, "c": 3}

d["a"]              # 1                O(1) avg — KeyError if missing!
d.get("a")          # 1                O(1) avg — returns None if missing
d.get("z", 0)       # 0                O(1) avg — returns default if missing
d["d"] = 4          # Add/update       O(1) avg
del d["b"]          # Remove           O(1) avg — KeyError if missing
d.pop("c")          # Remove + return  O(1) avg — KeyError if missing
d.pop("z", None)    # Remove + return  O(1) avg — returns default if missing
"a" in d            # True             O(1) avg — checks KEYS, not values
len(d)              # 2                O(1)
```

**The cardinal rule: ALWAYS use `.get()` or check `in` before accessing.** Don't risk KeyError unless you're certain the key exists.

```python
# ❌ Dangerous
value = d[key]

# ✅ Safe options
value = d.get(key, default_value)

if key in d:
    value = d[key]
```

### Iteration

```python
d = {"a": 1, "b": 2, "c": 3}

# Keys (default iteration)
for key in d:
    print(key)              # "a", "b", "c"

# Values
for value in d.values():
    print(value)            # 1, 2, 3

# Both (MOST COMMON — use this)
for key, value in d.items():
    print(key, value)       # ("a", 1), ("b", 2), ("c", 3)
```

**Python 3.7+ guarantees insertion order.** Items iterate in the order they were inserted. This is a language guarantee, not an implementation detail.

### The Modification-During-Iteration Trap

```python
# ❌ CRASH — RuntimeError: dictionary changed size during iteration
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if d[key] < 2:
        del d[key]

# ✅ Iterate over a COPY of keys
for key in list(d.keys()):
    if d[key] < 2:
        del d[key]

# ✅ Or build a new dict
d = {k: v for k, v in d.items() if v >= 2}
```

**Why it crashes:** Deleting keys changes the internal hash table structure. The iterator loses its place. Python raises an error rather than producing undefined behavior.

---

## 2C: defaultdict — Auto-Initializing Dict

The most common annoyance with regular dicts:

```python
# ❌ Tedious pattern
d = {}
for item in items:
    key = item["category"]
    if key not in d:
        d[key] = []
    d[key].append(item)
```

`defaultdict` eliminates the `if key not in d` check:

```python
from collections import defaultdict

# ✅ Clean
d = defaultdict(list)
for item in items:
    d[item["category"]].append(item)
```

When you access a missing key, `defaultdict` automatically creates it using the factory function you provided.

**Common factories:**

```python
defaultdict(list)     # Missing key → []
defaultdict(int)      # Missing key → 0
defaultdict(set)      # Missing key → set()
defaultdict(float)    # Missing key → 0.0
defaultdict(lambda: "unknown")  # Missing key → "unknown"
```

**When to use `defaultdict` vs `.get()` vs `setdefault()`:**

```python
# Use defaultdict when: building up collections (lists, sets) per key
d = defaultdict(list)
d["fruits"].append("apple")

# Use .get() when: reading values with a fallback
count = d.get(key, 0) + 1

# Use setdefault when: one-off initialization (less common, defaultdict is cleaner)
d.setdefault(key, []).append(value)
```

---

## 2D: Counter — The Frequency Specialist

```python
from collections import Counter

# From iterable
c = Counter([1, 1, 2, 3, 3, 3])     # Counter({3: 3, 1: 2, 2: 1})
c = Counter("abracadabra")            # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# Access counts
c["a"]             # 5
c["z"]             # 0 (missing keys return 0, NOT KeyError!)

# Most common
c.most_common(2)   # [('a', 5), ('b', 2)] — top 2 most frequent

# Arithmetic
c1 = Counter("aab")    # {'a': 2, 'b': 1}
c2 = Counter("abc")    # {'a': 1, 'b': 1, 'c': 1}

c1 + c2    # Counter({'a': 3, 'b': 2, 'c': 1})
c1 - c2    # Counter({'a': 1})   ← only POSITIVE counts kept!
c1 & c2    # Counter({'a': 1, 'b': 1})   ← min of each
c1 | c2    # Counter({'a': 2, 'b': 1, 'c': 1})   ← max of each
```

**The Counter subtraction trap:**

```python
c1 = Counter({'a': 1})
c2 = Counter({'a': 3})
c1 - c2    # Counter()   ← 'a' would be -2, but negatives are DROPPED

# If you need negative counts:
c1.subtract(c2)
print(c1)  # Counter({'a': -2})   ← subtract() keeps negatives, - operator doesn't
```

**When to use Counter vs manual dict:**
- Counting frequencies → Counter (cleaner, has `.most_common()`)
- Need values other than counts → regular dict
- Need auto-initialization for non-count types → defaultdict

---

# PART 3: THE EIGHT CORE HASHING PATTERNS

For each pattern: WHY it exists, WHEN to use it, the FRAMEWORK, an example.

---

## Pattern 1: Existence Check / Deduplication

### Why It Exists

The most basic use of hashing: "Have I seen this before?" Checking `x in list` is O(n). Checking `x in set` is O(1). Converting your existence checks from list to set can transform an O(n²) algorithm into O(n).

### When To Use

- "Does the array contain duplicates?"
- "Find the first element that appears only once"
- "Find all unique elements"
- Any time you need to track what you've encountered

### The Framework

```python
def has_duplicates(arr):
    seen = set()
    for element in arr:
        if element in seen:
            return True     # Already seen — duplicate!
        seen.add(element)
    return False
```

### Classic Example: First Non-Repeating Character

```python
def first_unique_char(s):
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1

    for i, char in enumerate(s):
        if count[char] == 1:
            return i

    return -1
```

Why two passes? First pass counts everything. Second pass finds the first with count 1. We need the **first** by position, so we iterate the original string in order.

Time: O(n). Space: O(1) — at most 26 lowercase letters (bounded alphabet).

---

## Pattern 2: Frequency Counting

### Why It Exists

Many problems reduce to: "How many times does each thing appear?" Once you have the frequency map, the answer falls out.

### When To Use

- "Find the most/least frequent element"
- "Are these two strings anagrams?"
- "Find the majority element (appears > n/2 times)"
- "Top K frequent elements" (combines with heap later)

### The Framework

```python
from collections import Counter

def solve(arr):
    freq = Counter(arr)
    # Now freq[element] = count of that element
    # Use freq to answer the question
```

### Classic Example: Majority Element

Element that appears more than n/2 times. Guaranteed to exist.

```python
def majority_element(arr):
    counts = Counter(arr)
    for num, count in counts.items():
        if count > len(arr) // 2:
            return num
```

Time: O(n). Space: O(n).

**Note:** There's an O(1) space solution called **Boyer-Moore Voting Algorithm** — but it's a specialized trick. The hash map approach is the general tool.

### Classic Example: Valid Anagram

```python
def is_anagram(s, t):
    return Counter(s) == Counter(t)
```

One line. O(n) time. Counter comparison checks all keys and values.

The array-based version (from the Arrays lesson):

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    for c in t:
        count[ord(c) - ord('a')] -= 1
    return all(x == 0 for x in count)
```

**When to use which:** Counter is cleaner and works with any characters. The array version is slightly faster and impresses interviewers by showing you understand the optimization for fixed alphabets.

---

## Pattern 3: Two Sum Pattern (Value → Index Mapping)

### Why It Exists

This is **the** most famous interview problem. Given an unsorted array, find two elements that sum to a target. Brute force is O(n²). Sorting + two pointers is O(n log n). Hash map makes it **O(n).**

### When To Use

- "Find pair with property X" in **unsorted** data
- Need to know the **index** of the complement (not just its existence)
- More generally: need to map a value back to its position or metadata

### The Framework

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

### How It Works — Step By Step

For `arr = [2, 7, 11, 15], target = 9`:

```
i=0, num=2:  complement = 9-2 = 7
             7 in seen? No. seen = {2: 0}

i=1, num=7:  complement = 9-7 = 2
             2 in seen? YES → return [seen[2], 1] = [0, 1] ✅
```

**The insight:** For each element, we compute what number we **need** (the complement). If we've already seen that number, we have our pair. If not, we store the current number so future elements can find it as their complement.

We look backward, not forward. By the time we reach the second element of a pair, the first is already stored.

Time: O(n). Space: O(n).

### Why This Beats Sorting + Two Pointers

| Approach | Time | Space | Preserves Indices? |
|---|---|---|---|
| Brute force | O(n²) | O(1) | ✅ Yes |
| Sort + two pointers | O(n log n) | O(1) | ❌ No (sorting changes positions) |
| Hash map | O(n) | O(n) | ✅ Yes |

When the problem asks for **indices** (not values), hash map is the only O(n) approach that works directly. Sorting would require storing original indices alongside values, adding complexity.

---

## Pattern 4: Grouping / Bucketing

### Why It Exists

You have a collection of items and need to organize them by some shared property. Without hashing, you'd sort (O(n log n)) or nest loops (O(n²)). With a hash map, you group in **O(n).**

### When To Use

- "Group these items by category/property"
- "Group anagrams together"
- "Find all items that share characteristic X"

### The Framework

```python
from collections import defaultdict

def group_by_property(items):
    groups = defaultdict(list)
    for item in items:
        key = compute_group_key(item)
        groups[key].append(item)
    return groups
```

The critical decision: **what is the group key?** The key must be the same for all items that belong together, and different for items that don't.

### Classic Example: Group Anagrams

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))    # Anagrams have same sorted form
        groups[key].append(s)
    return list(groups.values())
```

`"eat"` and `"tea"` both sort to `('a', 'e', 't')` → same key → same group.

Time: O(n × k log k) where n = number of strings, k = max string length.

**Optimization:** Use character count tuple instead of sorting:

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)    # (1, 0, 0, ..., 1, ..., 1) for "eat"
        groups[key].append(s)
    return list(groups.values())
```

Time: O(n × k) — no sorting. The key is a tuple of 26 integers representing character frequencies. Anagrams always produce the same frequency tuple.

---

## Pattern 5: Prefix Sum + Hash Map

### Reinforcement From Arrays Lesson

You already know this pattern from Problem 4 of the arrays test. I'll teach the variations you haven't seen.

### Variation: Longest Subarray With Sum K

Instead of counting subarrays, find the **longest** one.

```python
def longest_subarray_sum_k(arr, k):
    prefix_sum = 0
    first_occurrence = {0: -1}    # prefix_sum → first index where it occurred
    max_length = 0

    for i, num in enumerate(arr):
        prefix_sum += num
        complement = prefix_sum - k

        if complement in first_occurrence:
            length = i - first_occurrence[complement]
            max_length = max(max_length, length)

        # Only store FIRST occurrence (we want longest, so earliest start)
        if prefix_sum not in first_occurrence:
            first_occurrence[prefix_sum] = i

    return max_length
```

**Key difference from counting version:** We store the **first** occurrence of each prefix sum (not the count). We want the longest subarray, which means the earliest start point. If we overwrote with later indices, we'd miss longer subarrays.

Time: O(n). Space: O(n).

### Variation: Contiguous Array (Equal 0s and 1s)

Find the longest subarray with equal numbers of 0s and 1s.

**The trick:** Replace every 0 with -1. Now "equal 0s and 1s" becomes "subarray sum = 0." Apply prefix sum + hash map.

```python
def find_max_length(arr):
    # Transform: 0 → -1
    prefix_sum = 0
    first_occurrence = {0: -1}
    max_length = 0

    for i, num in enumerate(arr):
        prefix_sum += 1 if num == 1 else -1

        if prefix_sum in first_occurrence:
            max_length = max(max_length, i - first_occurrence[prefix_sum])
        else:
            first_occurrence[prefix_sum] = i

    return max_length
```

When we see the **same prefix sum** at two different indices, the subarray between them has sum 0 → equal 0s and 1s.

Time: O(n). Space: O(n).

### The Pattern Recognition Framework

Whenever you see "subarray with sum equal to / divisible by / proportional to K":

```
1. Think prefix sums
2. Think hash map to store prefix information
3. The complement is always: current_prefix - target_condition
4. Decide: counting? → store frequency. Longest? → store first occurrence.
```

---

## Pattern 6: Sliding Window + Hash Map

### Reinforcement + New Problems

You've already implemented this pattern. Let me add the most important variation you haven't seen.

### Minimum Window Substring

Given strings `s` and `t`, find the minimum window in `s` that contains all characters of `t`.

```python
def min_window(s, t):
    if not t or not s:
        return ""

    target = Counter(t)
    required = len(target)    # Number of unique chars we need

    window_counts = {}
    formed = 0                 # How many unique chars in window meet target count

    left = 0
    best = (float('inf'), 0, 0)   # (length, left, right)

    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        # Check if this character's count now meets the target
        if char in target and window_counts[char] == target[char]:
            formed += 1

        # Try to shrink from left
        while formed == required:
            # Update best
            window_size = right - left + 1
            if window_size < best[0]:
                best = (window_size, left, right)

            # Remove leftmost character
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target and window_counts[left_char] < target[left_char]:
                formed -= 1
            left += 1

    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]
```

**The key optimization:** Instead of comparing full frequency maps each time (O(26) or O(k)), we track `formed` — the count of unique characters meeting their target. We only expand/shrink this count when a character crosses the threshold. This makes each step truly O(1).

Time: O(n + m) where n = len(s), m = len(t). Space: O(m) for the target counter.

This is one of the **hardest** sliding window problems and appears frequently at FAANG.

---

## Pattern 7: Hash Map as Cache / Memoization

### Why It Exists

If you're computing the same thing multiple times, store the result and look it up instead of recomputing.

### The Framework

```python
cache = {}

def expensive_function(input):
    if input in cache:
        return cache[input]

    result = compute(input)    # Some expensive computation
    cache[input] = result
    return result
```

### Example: Fibonacci Without Redundant Work

```python
# ❌ O(2ⁿ) — recomputes same values exponentially
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# ✅ O(n) — each value computed once, stored in cache
def fib_memo(n, cache={}):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib_memo(n-1, cache) + fib_memo(n-2, cache)
    return cache[n]
```

Without memoization: fib(50) takes **minutes** (2⁵⁰ calls).
With memoization: fib(50) takes **microseconds** (50 calls, each computed once).

**This is a preview of Dynamic Programming.** When we get to DP in Weeks 8-9, memoization is one of the two core techniques (the other being tabulation). The hash map is the underlying tool.

### System Design Connection: Caching

The same principle at scale:

```
User requests profile for user_id=12345
  → Check cache: is user_id=12345 in our hash map?
  → YES: return cached result (O(1), no database hit)
  → NO: query database, store result in cache, return result

Next request for user_id=12345
  → Cache hit! Return instantly.
```

This is how **Redis**, **Memcached**, and every CDN works. A hash map from key → cached response.

---

## Pattern 8: Coordinate / State Hashing

### Why It Exists

Some problems involve tracking positions, coordinates, or complex states. You need to ask: "Have I been in this state before?" Tuples make any combination of values hashable.

### When To Use

- Grid/coordinate problems ("have I visited this cell?")
- State-space search ("have I seen this configuration?")
- Geometric problems ("how many points have this distance?")

### The Framework

```python
# Hashing coordinates
visited = set()
visited.add((row, col))
if (row, col) in visited:
    ...

# Hashing complex states
seen_states = set()
state = (player_pos, box_pos, keys_collected)  # tuple of values
seen_states.add(state)
```

### Example: Robot Return to Origin

A robot starts at (0,0) and receives movement commands. Does it return to origin?

```python
def judge_circle(moves):
    x, y = 0, 0
    for move in moves:
        if move == 'U': y += 1
        elif move == 'D': y -= 1
        elif move == 'L': x -= 1
        elif move == 'R': x += 1
    return x == 0 and y == 0
```

This one doesn't even need a hash map — just track coordinates. But the pattern extends:

### Example: Number of Boomerangs

Given n points, find number of tuples (i, j, k) where distance(i,j) == distance(i,k).

```python
def number_of_boomerangs(points):
    count = 0
    for i in range(len(points)):
        dist_map = defaultdict(int)
        for j in range(len(points)):
            if i == j:
                continue
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist = dx*dx + dy*dy    # Don't sqrt — avoid floats
            dist_map[dist] += 1

        for freq in dist_map.values():
            count += freq * (freq - 1)    # Pick 2 from freq points: P(freq, 2)

    return count
```

**Key insight:** We hash the **squared distance** (avoiding float precision issues with sqrt). For each anchor point, we group other points by distance. If `freq` points are equidistant, the number of ordered pairs is freq × (freq - 1).

Time: O(n²). Space: O(n).

### Example: Detecting Cycle in State Space

When would you visit the same state twice? Many simulation problems:

```python
def has_cycle(initial_state):
    seen = set()
    state = initial_state

    while state not in seen:
        seen.add(state)
        state = next_state(state)    # Some transition function

    return True  # We revisited a state — cycle detected
```

This pattern appears in: linked list cycle detection (Week 4), graph cycle detection (Week 7), and various simulation problems.

---

# PART 4: DESIGN PROBLEMS

## 4A: Design a Hash Set

This is a **real FAANG interview question** (LeetCode 705). Build it from scratch.

### The Design

```python
class MyHashSet:
    def __init__(self):
        self.size = 1000                    # Number of buckets
        self.buckets = [[] for _ in range(self.size)]  # Array of lists (chaining)

    def _hash(self, key):
        return key % self.size              # Simple modulo hash

    def add(self, key):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        if key not in bucket:               # Avoid duplicates
            bucket.append(key)

    def remove(self, key):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        return key in bucket
```

### How It Works

```
add(5):     5 % 1000 = 5     → buckets[5].append(5)
add(1005):  1005 % 1000 = 5  → buckets[5].append(1005)  ← COLLISION! Same bucket.
contains(5): buckets[5] = [5, 1005] → 5 in [5, 1005] → True
remove(5):   buckets[5] = [5, 1005] → remove 5 → [1005]
```

### Complexity

- `add`: O(1) average (O(n/size) for the `in` check on the chain, but chains are short with good hash)
- `remove`: O(1) average
- `contains`: O(1) average
- Space: O(size + n) where n = number of stored elements

### What An Interviewer Would Push On

- "What if you need to handle millions of elements?" → Discuss **resizing** when load factor exceeds threshold. Double the bucket array and rehash everything.
- "Can you make the worst case better?" → Instead of lists for chains, use **balanced BST** (when a chain gets too long, convert it to a tree for O(log n) worst case on that chain). Java's HashMap does this.
- "How would you choose the initial size?" → Prime numbers as table size distribute hashes more uniformly. 1000 isn't ideal — 1009 (prime) would be better.

---

## 4B: Design a Hash Map

Extension of the hash set — store key-value pairs instead of just keys.

```python
class MyHashMap:
    def __init__(self):
        self.size = 1009                    # Prime number for better distribution
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def put(self, key, value):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)    # Update existing
                return
        bucket.append((key, value))         # Insert new

    def get(self, key):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        for k, v in bucket:
            if k == key:
                return v
        return -1                           # Not found

    def remove(self, key):
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

**Key difference from hash set:** Each bucket stores `(key, value)` tuples. On `put`, we must check if the key already exists to update instead of duplicating.

---

## 4C: LRU Cache

**LRU = Least Recently Used.** A cache with a maximum capacity. When full, evict the item that hasn't been accessed the longest.

This is one of the **most commonly asked** FAANG design questions (LeetCode 146).

### The Ideal Solution

Requires **O(1)** for both `get` and `put`. This needs:
- Hash map: O(1) lookup by key
- Doubly linked list: O(1) removal and insertion at ends to track recency order

We haven't covered linked lists yet (Week 4). When we do, we'll implement the full version. For now, here's the concept and the Python shortcut:

### Python's OrderedDict Solution

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)    # Mark as recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove OLDEST (front of order)
```

### How It Works

```
capacity = 2

put(1, "A"):  cache = {1: "A"}
put(2, "B"):  cache = {1: "A", 2: "B"}
get(1):       cache = {2: "B", 1: "A"}  ← 1 moved to end (recently used)
put(3, "C"):  cache is full! Remove oldest (2).
              cache = {1: "A", 3: "C"}
get(2):       returns -1 (evicted)
```

### Why This Matters For System Design

Every web server, database, CDN uses LRU caching:
- Browser cache: recently viewed pages stay, old ones evicted
- Database query cache: recent queries cached, stale ones removed
- Operating system page cache: recently accessed memory pages stay in RAM

The O(1) get/put requirement is why hash map + linked list is the standard implementation.

### What We'll Add In Week 4

When we cover linked lists, we'll implement the full version:
- Doubly linked list where head = oldest, tail = newest
- Hash map: key → linked list node
- `get`: find node via map, move to tail. O(1).
- `put`: if exists, update + move to tail. If new + at capacity, remove head, add at tail. O(1).

---

# PART 5: ADVANCED HASHING CONCEPTS

## 5A: Rolling Hash

A rolling hash updates in O(1) when a window slides, instead of recomputing from scratch.

### The Concept

For a string window of length m, compute a hash:

```
hash("abc") = a × p² + b × p¹ + c × p⁰
```

Where p is a prime base (like 31) and values are character codes.

When the window slides from "abc" to "bcd":

```
new_hash = (old_hash - a × p²) × p + d × p⁰
```

Remove the contribution of the leaving character, shift everything, add the new character. **O(1) per slide.**

### When Rolling Hash Is Used

- **Rabin-Karp string matching:** Compare hash of pattern to hash of each window in text. O(n) average instead of O(n × m).
- **Finding duplicate substrings:** Hash all substrings of length k, check for collisions.
- **Longest duplicate substring:** Binary search on length + rolling hash.

### Implementation Sketch

```python
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    base = 31
    mod = 10**9 + 7    # Large prime to avoid collisions

    # Compute pattern hash
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod

    # Compute first window hash
    window_hash = 0
    for c in text[:m]:
        window_hash = (window_hash * base + ord(c)) % mod

    # Precompute base^m % mod (for removing leftmost character)
    power = pow(base, m, mod)

    if window_hash == pattern_hash and text[:m] == pattern:
        return 0

    # Slide
    for i in range(m, n):
        # Remove leftmost, add new character
        window_hash = (window_hash * base + ord(text[i]) - ord(text[i-m]) * power) % mod

        if window_hash == pattern_hash and text[i-m+1:i+1] == pattern:
            return i - m + 1

    return -1
```

**Note:** We still do the string comparison (`text[...] == pattern`) on hash matches because different strings can have the same hash (collision). The hash is a **filter** — it eliminates most non-matches cheaply, and we only do the expensive character comparison on the rare hash matches.

Time: O(n) average, O(n × m) worst case (many hash collisions).

You don't need to memorize this implementation. Know the concept: rolling hash enables O(1) window hash updates.

---

## 5B: Hash Map Tradeoffs & Decision Framework

### When Hash Map Is Overkill

```python
# ❌ Overkill for counting 26 lowercase letters
freq = {}
for c in s:
    freq[c] = freq.get(c, 0) + 1

# ✅ Better — fixed-size array
freq = [0] * 26
for c in s:
    freq[ord(c) - ord('a')] += 1
```

Array is faster (direct index access vs hash computation), uses less memory (no hash overhead), and more cache-friendly.

**Rule of thumb:** If the key space is small, fixed, and maps naturally to integers (like characters → 0-25), use an array. If the key space is large, unknown, or non-integer (strings, tuples, complex keys), use a hash map.

### Hash Map vs Sorted Structure

| Need | Hash Map | Sorted Structure (BST, sorted array) |
|---|---|---|
| Lookup by exact key | **O(1)** ✅ | O(log n) |
| Insert | **O(1)** ✅ | O(log n) |
| Delete | **O(1)** ✅ | O(log n) |
| Find min/max | O(n) ❌ | **O(log n)** or **O(1)** ✅ |
| Range query (all keys in [a, b]) | O(n) ❌ | **O(log n + k)** ✅ |
| Iterate in sorted order | O(n log n) (must sort) ❌ | **O(n)** ✅ |
| Memory overhead | Higher (hash table) | Lower (tree nodes) |

**Decision:** Use hash map when you need pure lookup speed and don't care about ordering. Use sorted structure when you need min/max, range queries, or sorted iteration.

### Memory Overhead

A Python dict entry stores: key object + value object + hash value + internal pointers. Rough estimate: ~60-100 bytes per entry.

For 1 million entries: ~60-100 MB. That's significant. In memory-constrained environments (embedded, mobile), consider alternatives.

---

## 5C: Hashing In System Design

### Caching (Already Covered in LRU)

Key → cached value. O(1) lookup before hitting expensive backend.

### Database Indexing

```
Table: users
Columns: id, name, email

Hash index on email:
  hash("alice@example.com") → row pointer → direct access to Alice's row

Without index: full table scan O(n)
With hash index: O(1) lookup
```

**Tradeoff:** Hash index uses O(n) extra space and slows down writes (must update index). But reads become O(1).

### Consistent Hashing (For Load Balancing)

Problem: You have 5 servers. Request comes in for user_id=12345. Which server handles it?

Simple approach: `server = hash(user_id) % 5`

But what if server 3 dies? Now you mod by 4. **Almost every user** maps to a different server. All caches invalidated. Massive thundering herd.

**Consistent hashing** solves this: arrange servers on a ring. Each key maps to the nearest server clockwise. When a server dies, only its keys remap — to the next server on the ring. Minimal disruption.

Used by: Amazon DynamoDB, Apache Cassandra, CDNs.

We'll explore this deeper in Week 11 (System Design).

### Rate Limiting

```python
# Track request counts per user
request_counts = defaultdict(list)  # user_id → list of timestamps

def is_rate_limited(user_id, max_requests, window_seconds):
    now = time.time()
    timestamps = request_counts[user_id]

    # Remove timestamps outside the window
    while timestamps and timestamps[0] < now - window_seconds:
        timestamps.pop(0)

    if len(timestamps) >= max_requests:
        return True

    timestamps.append(now)
    return False
```

Hash map: user_id → their request history. O(1) lookup per user.

### Bloom Filters (Exposure Level)

A **probabilistic** set. Uses very little memory. Can tell you:
- "Definitely NOT in the set" (100% accurate)
- "Probably in the set" (might be wrong — false positive)

Cannot tell you: "Definitely in the set."

Used for:
- Spell checkers: "Is this word definitely NOT in the dictionary?"
- Database query optimization: "Is this key definitely NOT in this database file?"
- Web crawlers: "Have I definitely NOT visited this URL before?"

How it works: multiple hash functions, each sets a bit in a bit array. To check membership, all bits must be set. False positives occur when bits are set by different keys that happen to cover the same positions.

You don't need to implement this. Know it exists and its tradeoff: space efficiency at the cost of false positives.

---

# PART 6: EDGE CASES & TRAPS

## 6A: The Gotcha Checklist

```
PYTHON-SPECIFIC:
□ {} creates empty DICT, not set. Use set() for empty sets.
□ Modifying dict/set while iterating → RuntimeError
  Fix: iterate over list(d.keys()) or build new dict
□ Lists are NOT hashable — convert to tuple for dict keys
□ Sets are NOT hashable — convert to frozenset for dict keys
□ Counter subtraction drops negative counts (use .subtract() to keep them)
□ Float keys: 0.1 + 0.2 != 0.3 — avoid floats as keys
□ (1, [2, 3]) is NOT hashable — tuple containing list
□ Counter("abc")["z"] returns 0, not KeyError
□ dict["missing_key"] raises KeyError — use .get(key, default)

ALGORITHMIC:
□ Hash operations are O(1) AVERAGE, O(n) WORST CASE
□ Hash maps use O(n) extra space — always account for this
□ When key space is small and fixed (26 letters), array is better than dict
□ Insertion order preserved in Python 3.7+ but don't rely on it for algorithms
  that need sorted order
□ Two items can be equal but hash differently across runs
  (Python randomizes hash seeds)
```

## 6B: When NOT To Use Hashing

| Situation | Why Not Hash | Use Instead |
|---|---|---|
| Need elements in sorted order | Hash table has no inherent order | Sorted array or BST |
| Need min/max frequently | O(n) to scan hash table | Heap |
| Need range queries | No efficient way to find "all keys between 5 and 10" | BST or sorted array + binary search |
| Key space is tiny and fixed | Unnecessary overhead | Array |
| Memory is extremely limited | Each entry has ~60-100 bytes overhead | Array or bit manipulation |
| Need worst-case O(1), not average | Hash collisions break O(1) guarantee | Balanced BST gives O(log n) guaranteed |

---

# PART 7: CONSOLIDATED REFERENCE

## Pattern Decision Tree

```
WHAT DO YOU NEED?
│
├── "Have I seen this before?"
│   └── PATTERN 1: Set for existence check
│
├── "How many times does each X appear?"
│   └── PATTERN 2: Counter / frequency dict
│
├── "Find pair with target sum/property" (unsorted)
│   └── PATTERN 3: Value → index hash map (Two Sum)
│
├── "Group items by shared property"
│   └── PATTERN 4: defaultdict(list) grouping
│
├── "Count/find subarrays with sum property"
│   └── PATTERN 5: Prefix sum + hash map
│
├── "Substring/subarray with frequency constraint"
│   └── PATTERN 6: Sliding window + hash map
│
├── "Avoid recomputing expensive results"
│   └── PATTERN 7: Hash map as cache/memoization
│
├── "Track coordinates/states/configurations"
│   └── PATTERN 8: Tuple keys in set/dict
│
└── "Need O(1) get/put with eviction"
    └── LRU CACHE: OrderedDict or hash map + linked list
```

## Operations Cheat Sheet

```
SET OPERATIONS                    TIME
──────────────────────────────────────
add(x)                            O(1) avg
remove(x)                         O(1) avg (KeyError if missing)
discard(x)                        O(1) avg (no error)
x in s                            O(1) avg
len(s)                            O(1)
s1 | s2 (union)                   O(len(s1) + len(s2))
s1 & s2 (intersection)            O(min(len(s1), len(s2)))
s1 - s2 (difference)              O(len(s1))
s1 <= s2 (subset)                 O(len(s1))

DICT OPERATIONS                   TIME
──────────────────────────────────────
d[key]                            O(1) avg (KeyError if missing)
d.get(key, default)               O(1) avg (safe)
d[key] = value                    O(1) avg
del d[key]                        O(1) avg
key in d                          O(1) avg
len(d)                            O(1)
d.items() / .keys() / .values()   O(1) to create view, O(n) to iterate

COUNTER OPERATIONS                TIME
──────────────────────────────────────
Counter(iterable)                  O(n)
c[key]                            O(1) (returns 0 for missing, not KeyError)
c.most_common(k)                  O(n log k) or O(n) if k not given
c1 + c2                           O(n)
c1 - c2                           O(n) (drops non-positive!)
```

---

# PART 8: TRACED EXEMPLARS (CAP = 3)

**Craft rule:** In-lesson solutions stop at **3** full traces. Rest → Retention + Spine + problem-bank.

Attempt blind. Answers for exemplars follow the prompts.

---

### Problem 1: Warm-Up — Contains Duplicate

Given an integer array, return `True` if any value appears at least twice.

```
Input: [1, 2, 3, 1]
Output: True
```

---

### Problem 2: Two Sum (Unsorted)

Given an array and a target, return indices of two numbers that add up to target. Exactly one solution exists.

```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

---

### Problem 3: Group Anagrams

Group strings that are anagrams of each other.

```
Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

---


---

# ANSWER KEY — EXEMPLARS ONLY

# Problem 1: Contains Duplicate

## Pattern Identification

**Pattern: Hash Set for Existence Tracking**

Why? We need to know if any value appears more than once. A hash set gives O(1) lookup — as we iterate, we check if we've seen the current element before. If yes, return True. If we finish without finding a duplicate, return False.

Alternative: Sort first, then check adjacent elements. O(n log n) time, O(1) space. But the hash set approach is O(n) time at the cost of O(n) space.

## Solution

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

## Trace Through Main Example

```
nums = [1, 2, 3, 1]

num=1: 1 in {}? NO → seen = {1}
num=2: 2 in {1}? NO → seen = {1, 2}
num=3: 3 in {1, 2}? NO → seen = {1, 2, 3}
num=1: 1 in {1, 2, 3}? YES → return True ✅
```

## Edge Cases

**Edge case 1: No duplicates**
```
nums = [1, 2, 3, 4]
Iterate through all — never find a match.
return False ✅
```

**Edge case 2: Single element**
```
nums = [5]
num=5: 5 in {}? NO → seen = {5}
Loop ends → return False ✅
```

**Edge case 3: All identical**
```
nums = [7, 7]
num=7: 7 in {}? NO → seen = {7}
num=7: 7 in {7}? YES → return True ✅
(Catches it on the second element immediately)
```

## Complexity Analysis

**STEP 1:** `nums` → n = len(nums)

**STEP 3:**
- Loop runs at most n times (could exit early)
- Inside: `num in seen` → set lookup → O(1). `seen.add(num)` → O(1)
- Cost per iteration: O(1)
- Worst case (no duplicates, or duplicate is last): O(n)

**STEP 5:**
- `seen` → set, worst case all unique → n elements → **O(n)**

> **Time: O(n), Space: O(n)**

---

# Problem 2: Two Sum (Unsorted)

## Pattern Identification

**Pattern: Hash Map for Complement Lookup**

Why? The array is **unsorted**, so the two-pointer approach from before doesn't apply (that required sorted input). For each element, we need its complement (target - num). A hash map lets us check in O(1) whether the complement exists and where it is.

We could sort first and use two pointers, but that changes indices. The hash map approach preserves original indices and runs in O(n).

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

## Why We Store BEFORE vs AFTER the Check

We check for the complement **before** storing the current number. This prevents an element from pairing with itself. If we stored first, then `nums = [3], target = 6` could incorrectly match 3 with itself.

## Trace Through Main Example

```
nums = [2, 7, 11, 15], target = 9

i=0, num=2: complement = 9-2 = 7
            7 in {}? NO → seen = {2: 0}

i=1, num=7: complement = 9-7 = 2
            2 in {2: 0}? YES → return [0, 1] ✅
```

## Edge Cases

**Edge case 1: Complement is at the end**
```
nums = [3, 5, 8, 1], target = 4
i=0, num=3: comp=1, not found. seen={3:0}
i=1, num=5: comp=-1, not found. seen={3:0, 5:1}
i=2, num=8: comp=-4, not found. seen={3:0, 5:1, 8:2}
i=3, num=1: comp=3, 3 in seen → return [0, 3] ✅
```

**Edge case 2: Same value used twice**
```
nums = [3, 3], target = 6
i=0, num=3: comp=3, 3 in {}? NO → seen={3:0}
i=1, num=3: comp=3, 3 in {3:0}? YES → return [0, 1] ✅
(Works correctly — the first 3 was stored, the second finds it)
```

## Complexity Analysis

**STEP 1:** `nums` → n = len(nums)

**STEP 3:**
- Loop: at most n iterations
- Inside: arithmetic O(1), dict lookup O(1), dict assignment O(1)
- O(n)

**STEP 5:**
- `seen` → dict, at most n entries → **O(n)**

> **Time: O(n), Space: O(n)**

---

# Problem 3: Group Anagrams

## Pattern Identification

**Pattern: Hash Map with Canonical Key (Frequency Signature)**

Why? Two strings are anagrams if they have the same character frequencies. We need a way to group them. If we sort each string, all anagrams produce the same sorted string — that becomes our hash map key. Alternatively, we can use a character frequency tuple as the key (avoids sorting cost per string).

I'll use the sorted approach for clarity, then note the optimization.

## Solution

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

## Why `tuple(sorted(s))` and Not Just `sorted(s)`

`sorted(s)` returns a list. Lists are **unhashable** in Python — they can't be dictionary keys. `tuple()` converts it to an immutable, hashable type.

## Trace Through Main Example

```
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

"eat" → sorted: ['a','e','t'] → key: ('a','e','t')
        groups = {('a','e','t'): ["eat"]}

"tea" → sorted: ['a','e','t'] → key: ('a','e','t')
        groups = {('a','e','t'): ["eat", "tea"]}

"tan" → sorted: ['a','n','t'] → key: ('a','n','t')
        groups = {('a','e','t'): ["eat", "tea"], ('a','n','t'): ["tan"]}

"ate" → sorted: ['a','e','t'] → key: ('a','e','t')
        groups = {('a','e','t'): ["eat", "tea", "ate"], ('a','n','t'): ["tan"]}

"nat" → sorted: ['a','n','t'] → key: ('a','n','t')
        groups = {('a','e','t'): ["eat", "tea", "ate"], ('a','n','t'): ["tan", "nat"]}

"bat" → sorted: ['a','b','t'] → key: ('a','b','t')
        groups = {..., ('a','b','t'): ["bat"]}

return [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]] ✅
```

## Edge Cases

**Edge case 1: Empty strings**
```
strs = ["", ""]
"" → sorted: [] → key: ()
Both map to same key → [["", ""]] ✅
```

**Edge case 2: Single character strings**
```
strs = ["a", "b", "a"]
"a" → ('a',), "b" → ('b',), "a" → ('a',)
→ [["a", "a"], ["b"]] ✅
```

## Complexity Analysis

**STEP 1:** `strs` → n = len(strs). Let k = maximum length of any string.

**STEP 3:**
- Loop: n iterations
- Inside each iteration:
  - `sorted(s)` → ⚠️ **O(k log k)** — sorting a string of length up to k
  - `tuple(...)` → O(k) — creating tuple from k elements
  - Dict operations with tuple key → hashing the tuple is O(k), lookup O(k) average
  - `groups[key].append(s)` → O(1)
- Cost per iteration: **O(k log k)**
- Total loop: **O(n × k log k)**

**STEP 4:** O(n × k log k)

**STEP 5:**
- `groups` → stores all n strings across all groups. Total strings stored: n. Each string up to length k. → **O(n × k)**
- `key` → single tuple per iteration, max size k → O(k) transient

> **Time: O(n × k log k), Space: O(n × k)**

**Optimization note:** We can use a frequency count tuple instead of sorting:

```python
key = tuple(count[c] for c in 'abcdefghijklmnopqrstuvwxyz')
```

This makes the key in O(k + 26) = O(k) per string instead of O(k log k). Total becomes **O(n × k)**. Worth mentioning in an interview.

---


---

## Rest of the old in-lesson bank

Drill via Retention Questions + `Practice Spines/Phase A MVP Spines.md` + `problem-bank/`. Do not paste full solutions back into this lesson.

## Teach-back

Explain the core frameworks from earlier parts without notes, then open Retention (questions-only).

