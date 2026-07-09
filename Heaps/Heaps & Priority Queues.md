# HEAPS & PRIORITY QUEUES — THE COMPLETE LESSON

**Module:** 6 (Heaps + Advanced Array Patterns)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Language:** Python (`heapq`)  
**Prerequisite:** Arrays, Hashing, Recursion basics. Graphs/Dijkstra appear only as **PREVIEW**.

---

# PART 1: WHY HEAPS EXIST

## The Problem Heaps Solve

You repeatedly need the **smallest** or **largest** element in a changing collection.

| Need | Array / List | Sorted Array | Hash Set | Heap |
|---|---|---|---|---|
| Find min/max once | O(n) scan | O(1) at end | O(n) | O(1) peek |
| Insert, then find min again | O(n) each time | O(n) insert | O(n) | **O(log n)** insert + O(1) peek |
| Extract min repeatedly | O(n) each | O(n) shift | O(n) | **O(log n)** each |
| Membership / arbitrary delete | O(n) | O(log n) binary search | O(1) | O(n) find + O(log n) delete |

**The rule:** If your problem says "always give me the current best / worst / next-most-urgent," reach for a heap (priority queue). If you only need min/max **once**, a linear scan is enough. If you need sorted order of **everything**, sort once — don't use a heap as a slow sort unless you need online extraction.

### Real-World Intuition

Think of a hospital ER triage board:

- Patients arrive at arbitrary times (insert)
- The next patient treated is always the **highest priority** (extract-max / extract-min depending on convention)
- You do **not** re-sort the entire waiting room from scratch every arrival

A heap is that triage board: partially ordered so the top is always correct, and fixing the order after an insert/extract costs O(log n), not O(n).

### Priority Queue vs Heap

- **Priority queue** = the *abstract ADT*: insert with priority, extract highest/lowest priority.
- **Heap** = the *concrete structure* that implements a priority queue efficiently (binary heap is the interview default).

In Python interviews, "use a heap" and "use a priority queue" almost always mean: use `heapq` (binary min-heap).

---

# PART 2: THE HEAP PROPERTY & BINARY HEAP STRUCTURE

## 2A: The Heap Property

A **binary heap** is a binary tree that satisfies two constraints:

### 1. Shape property (complete binary tree)

Every level is completely filled except possibly the last, which is filled **left to right**.

```
VALID (complete):          INVALID (gap / right-heavy):

        1                          1
       / \                        / \
      3   5                      3   5
     / \                        /     \
    7   9                      7       9   ← hole under 3's right
```

Completeness is what lets us store a heap in a **flat array** with parent/child index arithmetic — no pointers required.

### 2. Heap-order property

**Min-heap:** every parent ≤ its children. Root = global minimum.  
**Max-heap:** every parent ≥ its children. Root = global maximum.

```
MIN-HEAP:                    MAX-HEAP:

        1                            9
       / \                          / \
      3   5                        7   5
     / \                          / \
    7   9                        3   1
```

**Critical:** Siblings are **not** ordered relative to each other. Left can be larger or smaller than right. Only parent–child relationships are constrained. A heap is **not** a BST and is **not** fully sorted.

### What the property buys you

- Peek min (min-heap): O(1) — look at index 0
- The rest of the tree is only "sorted enough" to restore the property after changes in O(log n)

---

## 2B: Array Representation

Store the complete tree level-order in a 0-indexed array:

```
Index:  0  1  2  3  4  5  6
Value: [1, 3, 5, 7, 9, 8, 6]

Tree:
            1          ← index 0
         /     \
        3       5      ← indices 1, 2
       / \     / \
      7   9   8   6    ← indices 3, 4, 5, 6
```

### Index formulas (memorize cold)

For node at index `i`:

```
parent(i)      = (i - 1) // 2
left_child(i)  = 2*i + 1
right_child(i) = 2*i + 2
```

```python
def parent(i): return (i - 1) // 2
def left(i):   return 2 * i + 1
def right(i):  return 2 * i + 2
```

**Why this works:** Completeness guarantees every index maps to a unique tree position with no holes in the array prefix `0..n-1`.

### Height of a heap

A complete binary tree with n nodes has height **⌊log₂ n⌋**.  
That is why bubble-up / bubble-down are O(log n): you walk at most one root-to-leaf path.

---

## 2C: Sift Up (Bubble Up) — After Insert

**When:** You append a new element at the end (next open leaf). It may violate heap order with its ancestors.

**How:** Swap with parent while the heap property is broken.

```python
def sift_up(heap, i):
    """Restore min-heap property by bubbling heap[i] upward."""
    while i > 0:
        p = (i - 1) // 2
        if heap[i] < heap[p]:
            heap[i], heap[p] = heap[p], heap[i]
            i = p
        else:
            break
```

**Trace — insert 2 into min-heap `[1, 3, 5, 7, 9]`:**

```
Before append: [1, 3, 5, 7, 9]
Append 2:      [1, 3, 5, 7, 9, 2]
                         ↑ index 5

i=5, parent=2: heap[5]=2 < heap[2]=5 → swap
               [1, 3, 2, 7, 9, 5]
i=2, parent=0: heap[2]=2 > heap[0]=1 → stop

Result: [1, 3, 2, 7, 9, 5]
```

**Complexity:** O(log n) comparisons/swaps. O(1) extra space.

---

## 2D: Sift Down (Bubble Down / Heapify Down) — After Extract

**When:** You remove the root. You move the last element into the root hole. It may be too large (min-heap) and must sink.

**How:** Swap with the **smaller** child (min-heap) while the property is broken.

```python
def sift_down(heap, i):
    """Restore min-heap property by sinking heap[i] downward."""
    n = len(heap)
    while True:
        smallest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and heap[l] < heap[smallest]:
            smallest = l
        if r < n and heap[r] < heap[smallest]:
            smallest = r
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
```

**Trace — extract-min from `[1, 3, 2, 7, 9, 5]`:**

```
Root 1 is the answer. Move last element 5 to root:
[5, 3, 2, 7, 9]   (popped the old last)

i=0: children 3 and 2 → smaller child is 2 (index 2)
     5 > 2 → swap → [2, 3, 5, 7, 9]
i=2: children? left=5, right=6 → out of range → stop

Heap is now [2, 3, 5, 7, 9]. Extracted value was 1.
```

**Complexity:** O(log n). Choosing the correct child each step is essential — always compare **both** children.

---

## 2E: Insert & Extract — Full Recipes

### Insert (push)

```
1. Append value at end of array          O(1)
2. sift_up from that index               O(log n)
Total: O(log n)
```

### Extract-min (pop)

```
1. Save heap[0] as answer                O(1)
2. Move heap[-1] into heap[0]            O(1)
3. Pop the last slot                     O(1)
4. sift_down from index 0                O(log n)
Total: O(log n)
Peek-min without extract: O(1) — just read heap[0]
```

### Build-heap / heapify (Floyd)

Given an unordered array, turn it into a heap **in-place**.

**Naive:** insert n elements one by one → O(n log n).

**Floyd's method:** sift_down from the **last non-leaf** down to the root:

```python
def heapify(arr):
    """In-place min-heapify. O(n)."""
    n = len(arr)
    # Last parent index = (n - 2) // 2
    for i in range((n - 2) // 2, -1, -1):
        sift_down(arr, i)
```

**Why O(n), not O(n log n)?** Most nodes are near the leaves and sift a short distance. Summing sift costs over all heights yields a geometric series bounded by **~2n** → **O(n)**.

```
Nodes at height h can sift at most h levels.
~ n/2 nodes at height 0 (leaves) → cost 0
~ n/4 nodes at height 1 → cost ≤ 1 each
~ n/8 nodes at height 2 → cost ≤ 2 each
...
Total ≤ n * Σ (h / 2^h) = O(n)
```

**Interview fact:** Building a heap is O(n). Sorting by repeatedly extracting is O(n log n) — heapsort.

---

## 2F: Complexity Cheat Card (Operations)

| Operation | Time | Notes |
|---|---|---|
| Peek min (min-heap) | O(1) | `heap[0]` |
| Insert (heappush) | O(log n) | append + sift up |
| Extract-min (heappop) | O(log n) | swap root/last + sift down |
| heapify (build) | **O(n)** | Floyd; not O(n log n) |
| heappushpop | O(log n) | push then pop, optimized |
| heapreplace | O(log n) | pop then push, optimized |
| Search arbitrary value | O(n) | heap is not a search tree |
| Delete arbitrary index | O(log n) after O(n) find | rare in interviews |
| Decrease-key | O(log n) if you have index | Python heapq has no built-in |

---

# PART 3: PYTHON `heapq` — DEEP DIVE

## 3A: The One Rule That Causes All Bugs

**`heapq` implements a min-heap only.** There is no `maxheapq`.

```python
import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
print(h[0])           # 1 — smallest
print(heapq.heappop(h))  # 1
```

Everything else is a **trick layered on top of min-heap**.

---

## 3B: Core API

```python
import heapq

heapq.heappush(h, x)       # insert x; O(log n)
heapq.heappop(h)           # remove and return smallest; O(log n)
h[0]                       # peek smallest; O(1) — do NOT pop
heapq.heapify(h)           # in-place transform list → heap; O(n)

heapq.heappushpop(h, x)    # push x, then pop smallest; O(log n)
                           # often faster than push+pop separately
heapq.heapreplace(h, x)    # pop smallest, then push x; O(log n)
                           # heap size stays constant; errors if empty

heapq.nlargest(k, iterable, key=None)  # k largest; uses heap internally
heapq.nsmallest(k, iterable, key=None) # k smallest
```

### `heappushpop` vs `heapreplace`

| Call | Meaning | Use when |
|---|---|---|
| `heappushpop(h, x)` | Push first, then pop min | You want the min **among old elements + x** |
| `heapreplace(h, x)` | Pop min first, then push x | Fixed-size heap; replace root with x |

```python
h = [1, 3, 5]
heapq.heapify(h)

heapq.heappushpop(h, 0)   # push 0 → [0,1,3,5], pop 0 → back to size 3 with min among rest
# vs
h = [1, 3, 5]
heapq.heapify(h)
heapq.heapreplace(h, 0)   # pop 1, push 0 → heap contains 0, not 1
```

---

## 3C: Max-Heap Tricks (Min-Heap Only)

### Trick 1: Negate numbers (most common)

Store `-x` instead of `x`. Smallest negated value ↔ largest original.

```python
import heapq

max_h = []
for x in [3, 1, 4, 1, 5]:
    heapq.heappush(max_h, -x)

largest = -heapq.heappop(max_h)  # 5
peek    = -max_h[0]              # next largest
```

**Works for:** ints, floats.  
**Fails for:** objects where negation is meaningless — use Trick 2/3.

### Trick 2: Tuple with inverted priority

```python
# Max-heap by score: store (-score, item)
heapq.heappush(h, (-score, item))
best_score, best_item = heapq.heappop(h)
best_score = -best_score
```

### Trick 3: `nlargest` / multiply by -1 for one-shot

```python
# One-shot "get k largest" — fine for interviews if k is the answer shape
heapq.nlargest(k, nums)
```

For **streaming / online** updates, maintain a heap yourself; don't rebuild with `nlargest` every time.

---

## 3D: Tuples & Custom Objects in `heapq`

`heapq` compares entries with `<`. For tuples, comparison is **lexicographic** (first element, then second, …).

```python
# (priority, tie_breaker, payload)
heapq.heappush(h, (dist, node_id))
heapq.heappush(h, (freq, char))
```

### The TypeError trap

```python
# BAD — if two priorities equal, Python compares the payloads
heapq.heappush(h, (5, {"a": 1}))
heapq.heappush(h, (5, {"b": 2}))
# TypeError: '<' not supported between instances of 'dict' and 'dict'
```

**Fix:** add a unique monotonic counter so ties never compare payloads:

```python
counter = 0
def push(h, priority, item):
    global counter
    heapq.heappush(h, (priority, counter, item))
    counter += 1
```

### Custom classes

Either:
1. Store `(priority, counter, obj)` and never rely on `obj.__lt__`, or
2. Define `__lt__` on the class (interview-rare; be careful with equality).

```python
class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name
    def __lt__(self, other):
        return self.priority < other.priority  # min-heap by priority
```

**Interview preference:** tuples + counter. Clearer and avoids subtle class comparison bugs.

---

## 3E: "Delete" and Lazy Deletion

Python's `heapq` cannot delete an arbitrary element in O(log n) without the index.

**Lazy deletion pattern** (used in Dijkstra variants, sliding-window median hard versions, etc.):

```python
# Mark obsolete entries; skip them when they surface at the top
invalid = set()

def lazy_pop(h):
    while h and h[0] in invalid:  # or check id/version
        heapq.heappop(h)
    return heapq.heappop(h) if h else None
```

Or store `(value, version)` and ignore outdated versions when popped.

**For Module 6:** know that arbitrary delete is awkward; prefer redesigning so you only push/pop, or use lazy invalidation.

---

# PART 4: WHEN TO USE A HEAP — DECISION FRAMEWORK

```
Do you need the min or max of a DYNAMIC set repeatedly?
├── NO  → sort once, or scan once. Don't use a heap.
└── YES → Is the set size bounded by K (top-K style)?
          ├── YES → size-K heap (see Pattern Top-K)
          └── NO  → full heap / two-heap median / etc.

Do you need FULL sorted order of all n elements?
├── YES, offline → sorted(arr) is simpler O(n log n)
└── YES, online (extract one-by-one as new data arrives) → heap

Is this shortest path on a weighted graph?
└── PREVIEW: Dijkstra uses a min-heap of (dist, node) — Module 8
```

### Heap vs Sort vs Hash

| Situation | Prefer |
|---|---|
| Top K of n elements, K ≪ n | Size-K heap → O(n log K) |
| Top K, K ≈ n | Sort → O(n log n) (simpler, similar cost) |
| Running median in a stream | Two heaps |
| Frequency → "most frequent K" | Counter + heap (or bucket sort) |
| Merge K sorted lists | Min-heap of K pointers |
| Need O(1) membership | Hash — heap alone is wrong |

---

# PART 5: CORE PATTERNS

---

## Pattern 1: Top-K Elements

### The Idea

To find the **K largest**, keep a **min-heap of size K**. The root is the **smallest among the large ones** — the threshold to beat.

To find the **K smallest**, keep a **max-heap of size K** (via negation).

### Why min-heap for K largest?

If you kept a max-heap of everything, you'd store n elements.  
With a size-K min-heap of candidates:

- Root = weakest member of the current top-K
- New element > root → it deserves a spot → replace root
- New element ≤ root → discard

### Framework — K largest

```python
import heapq

def top_k_largest(nums, k):
    if k <= 0:
        return []
    h = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)          # min-heap
        elif x > h[0]:
            heapq.heapreplace(h, x)      # eject weakest
    return h  # unordered top-K; sort if needed
```

**Complexity:** O(n log K) time, O(K) space.  
Better than O(n log n) sort when K ≪ n.

### Framework — K smallest

```python
def top_k_smallest(nums, k):
    h = []  # max-heap via negation
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, -x)
        elif x < -h[0]:
            heapq.heapreplace(h, -x)
    return sorted(-x for x in h)
```

### Variant: Kth largest element

Same size-K min-heap; answer is `h[0]` after processing all.

```python
def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```

Equivalent: push all, pop n−k times — worse space if you materialize full heap; size-K is cleaner.

---

## Pattern 2: Merge K Sorted Lists

### The Idea

You have K sorted lists. Brute force: concatenate + sort → O(N log N) where N = total elements.  
Better: always take the global next-smallest head among K lists → min-heap of size K → **O(N log K)**.

### Framework

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            # (value, list_index, node) — list_index breaks ties
            heapq.heappush(h, (node.val, i, node))

    dummy = ListNode(0)
    cur = dummy
    while h:
        val, i, node = heapq.heappop(h)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```

**Why store `i`?** If two nodes have the same `val`, Python would try to compare `ListNode` objects → TypeError. The index is a unique tie-breaker.

**Complexity:** O(N log K) time, O(K) space for the heap.

**Same pattern:** merge K sorted arrays; smallest range covering elements from each list (harder variant).

---

## Pattern 3: Median from a Stream (Two Heaps)

### The Idea

Median needs the middle of a sorted order. Re-sorting each insert is O(n log n) per query.  

Maintain:

- **Max-heap `lo`** — lower half (negated min-heap). Largest of lower half at top.
- **Min-heap `hi`** — upper half. Smallest of upper half at top.

Invariant:

```
Every value in lo ≤ every value in hi
len(lo) == len(hi)  or  len(lo) == len(hi) + 1
```

Median:

- Odd total → `lo` has one extra → median = max of `lo`
- Even total → average of max(`lo`) and min(`hi`)

### Framework

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap via negation
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # Enforce ordering: max(lo) ≤ min(hi)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Balance sizes: lo may have at most one more
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0
```

### Trace

```
add 1:  lo=[-1], hi=[]           median 1
add 2:  push to lo → lo=[-2,-1]; move 2 to hi → lo=[-1], hi=[2]
        balance ok               median (1+2)/2 = 1.5
add 3:  lo gets 3 → rebalance → lo=[-2,-1], hi=[3]
        wait — follow code carefully:

add 3:
  push -3 to lo → lo = [-3,-1,-2]  (heap order)
  move -pop(lo)=3 to hi → hi=[2,3], lo=[-1,-2]
  len(hi)=2 > len(lo)=2? equal after move... 
  Actually after push to hi: lo size 2, hi size 2.
  len(hi) > len(lo)? No.
  median = (-lo[0] + hi[0]) / 2 = (1+2)/2 = 1.5

Hmm need cleaner step-by-step for add sequence 1,2,3:

Start: lo=[], hi=[]
add(1):
  lo=[-1]
  move to hi: lo=[], hi=[1]
  len(hi)>len(lo) → move back: lo=[-1], hi=[]
  median=1

add(2):
  lo=[-2,-1]
  move to hi: lo=[-1], hi=[2]
  sizes equal → stop
  median=(1+2)/2=1.5

add(3):
  lo=[-3,-1]
  move to hi: lo=[-1], hi=[2,3]
  len(hi)=2 > len(lo)=1 → move: lo=[-2,-1], hi=[3]
  median=2
```

**Complexity:** add O(log n), find median O(1).

**Interview signal:** "running median" / "median in a stream" → two heaps almost always.

---

## Pattern 4: K Closest Points

### The Idea

K closest to origin (or to a query point) = Top-K by distance, inverted.

**Size-K max-heap by distance:** keep the K closest seen so far; eject the farthest when a closer point arrives.

```python
import heapq

def k_closest(points, k):
    # Max-heap of size k by distance² (avoid sqrt)
    # Store (-dist2, x, y) so largest distance sits at top of min-heap-of-negatives
    h = []
    for x, y in points:
        dist2 = x * x + y * y
        if len(h) < k:
            heapq.heappush(h, (-dist2, x, y))
        elif dist2 < -h[0][0]:
            heapq.heapreplace(h, (-dist2, x, y))
    return [[x, y] for (_, x, y) in h]
```

**Complexity:** O(n log K).  
**Alternative:** sort by distance O(n log n) — fine if K ≈ n.  
**Alternative:** Quickselect O(n) average — advanced; mention if asked to optimize further.

Use **distance squared** to avoid floats and `sqrt`.

---

## Pattern 5: Task Scheduler

### Problem Shape

Tasks with cooldowns: same letter needs `n` units gap between runs. Find minimum intervals to finish all tasks (idle time allowed).

### Heap Insight

Always schedule the **most frequent remaining** task that is legally available. Frequency map + max-heap of counts.

```python
import heapq
from collections import Counter, deque

def least_interval(tasks, n):
    freq = Counter(tasks)
    # max-heap of remaining counts
    h = [-c for c in freq.values()]
    heapq.heapify(h)

    time = 0
    cooldown = deque()  # entries: (ready_time, neg_count)

    while h or cooldown:
        time += 1
        if h:
            cnt = heapq.heappop(h) + 1  # less negative = one fewer remaining
            if cnt != 0:
                cooldown.append((time + n, cnt))
        if cooldown and cooldown[0][0] == time:
            heapq.heappush(h, cooldown.popleft()[1])

    return time
```

### Math shortcut (also know this)

```
max_freq = max(counts)
num_max = count of tasks with max_freq
answer = max(len(tasks), (max_freq - 1) * (n + 1) + num_max)
```

Heap simulation teaches the pattern; formula is faster if constraints allow. Interviews often accept either if you explain correctly.

**Complexity (heap sim):** O(T log 26) ≈ O(T) since at most 26 letters — still speak "heap of frequencies."

---

## Pattern 6: Reorganize String

### Problem Shape

Rearrange string so no two adjacent characters are equal. Return `""` if impossible.

### Heap Insight

Always place the **most frequent remaining** character that is **not** the same as the previous placed character.

```python
import heapq
from collections import Counter

def reorganize_string(s):
    freq = Counter(s)
    if max(freq.values()) > (len(s) + 1) // 2:
        return ""  # impossible — optional early exit

    h = [(-c, ch) for ch, c in freq.items()]
    heapq.heapify(h)
    result = []

    while len(h) >= 2:
        c1, ch1 = heapq.heappop(h)
        c2, ch2 = heapq.heappop(h)
        result.append(ch1)
        result.append(ch2)
        if c1 + 1 < 0:  # still remaining (c1 is negative)
            heapq.heappush(h, (c1 + 1, ch1))
        if c2 + 1 < 0:
            heapq.heappush(h, (c2 + 1, ch2))

    if h:
        c, ch = h[0]
        if c < -1:  # more than one left → would adjacent-duplicate
            return ""
        result.append(ch)

    return "".join(result)
```

**Greedy invariant:** pairing the two highest frequencies each step prevents the hottest character from clustering.

**Related:** Task Scheduler, rearrange string k distance apart — same "max-heap of counts + cooldown" family.

---

## Pattern 7: PREVIEW — Dijkstra's Algorithm

> **PREVIEW — no mastery credit until Graphs II (Module 8).**  
> You only need to recognize the heap's role here.

Dijkstra finds shortest paths from a source in a **weighted graph with non-negative weights**.

The heap stores `(distance, node)`:

```python
# PREVIEW SKETCH — not Module 6 drill material
import heapq

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    h = [(0, source)]  # min-heap by distance

    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue  # lazy outdated entry
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist
```

**Why a heap?** Always expand the closest unsettled node next — same "extract current best" theme as priority queues.

**Module 6 takeaway:** Dijkstra = BFS where the queue is a **min-heap of distances**, not a FIFO deque. Full correctness proofs, decrease-key, and dense-graph variants wait for Module 8.

---

# PART 6: RELATED CLASSICS (SHORT FORMS)

## Meeting Rooms II (min rooms)

Sort starts/ends; or: sort intervals by start, keep a **min-heap of end times**. If earliest ending room is free (`heap[0] ≤ start`), reuse (pop); else allocate (push). Heap size = rooms in use.

```python
def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    intervals.sort()
    h = []
    for start, end in intervals:
        if h and h[0] <= start:
            heapq.heappop(h)
        heapq.heappush(h, end)
    return len(h)
```

## Ugly Number II / Super Ugly

Min-heap generate candidates in order; dedupe with a set. Classic "merge K increasing sequences" in disguise.

## Find Median / Sliding Window Median

Two heaps + lazy deletion for the sliding variant (hard). Core two-heap idea is Module 6; sliding version is stretch.

---

# PART 7: EDGE CASES & INTERVIEW WORKFLOW

## Edge Case Checklist

| Case | What to watch |
|---|---|
| Empty input | `heappop` on `[]` → IndexError |
| K > n | Top-K: return all, or clamp K |
| K = 0 | Return `[]` |
| All equal | Heap still correct; ties need counter for objects |
| Negatives | Negation max-heap trick still works |
| Duplicates in merge-K | Tie-break with index |
| Single list / K = 1 | Merge-K and Top-K degenerate cleanly |
| Impossible reorganize | Early frequency check |

## Interview Workflow

```
1. Restate: dynamic min/max? top-K? stream median? merge sorted streams?
2. Name the pattern + heap type (min vs max-via-negation)
3. State size of heap (K vs n) and complexity O(...)
4. Mention tuple ordering / counter if storing objects
5. Code push/pop carefully — peek is h[0], not heappop
6. Trace one example; hit empty / K>n edges
```

---

# PART 8: CONSOLIDATED CHEAT SHEETS

## Pattern → Heap Shape

| Problem cue | Heap setup |
|---|---|
| K largest / Kth largest | Min-heap size K |
| K smallest / Kth smallest | Max-heap size K (negate) |
| Merge K sorted | Min-heap size K of heads |
| Running median | Max-heap lo + Min-heap hi |
| K closest | Max-heap size K by distance |
| Task scheduler / reorganize | Max-heap of frequencies |
| Meeting rooms II | Min-heap of end times |
| Dijkstra (PREVIEW) | Min-heap of (dist, node) |

## Complexity Summary

| Pattern | Time | Space |
|---|---|---|
| Top-K | O(n log K) | O(K) |
| Kth largest | O(n log K) | O(K) |
| Merge K lists | O(N log K) | O(K) |
| Median stream (per op) | O(log n) add, O(1) query | O(n) |
| K closest | O(n log K) | O(K) |
| Reorganize string | O(n log Σ) | O(Σ) alphabet |
| heapify build | O(n) | O(1) extra |
| heapsort | O(n log n) | O(1) extra |

## `heapq` Snips to Memorize

```python
import heapq

# min-heap
heapq.heappush(h, x)
heapq.heappop(h)
heapq.heapify(h)

# max-heap numbers
heapq.heappush(h, -x)
x = -heapq.heappop(h)

# safe object entries
heapq.heappush(h, (priority, counter, obj))

# fixed-size replace
if len(h) < k: heapq.heappush(h, x)
elif x > h[0]: heapq.heapreplace(h, x)
```

## Decision Tree (One Glance)

```
Need repeated best element from changing set?
└── YES → HEAP
     Need only K best? → size-K heap
     Need median? → two heaps
     Need merge sorted streams? → heap of K heads
     Need schedule by frequency? → max-heap of counts
Need full static sort once? → sorted() / .sort()
Need membership? → hash, not heap
Need shortest path? → PREVIEW Dijkstra (Module 8)
```

---

# PART 9: WORKED PROBLEMS WITH TRACES

---

# Problem 1: Kth Largest Element in an Array

## Pattern Identification

**Pattern: Size-K min-heap (Top-K).**  
We need the Kth largest, not a full sort. Maintain the K largest seen; the smallest of those is the Kth largest.

## Solution

```python
import heapq

def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```

## Trace

```
nums = [3, 2, 1, 5, 6, 4], k = 2

x=3: h=[3]
x=2: h=[2,3]
x=1: h=[1,3,2] → size 3 > 2 → pop 1 → h=[2,3]
x=5: h=[2,3,5] → pop 2 → h=[3,5]
x=6: h=[3,5,6] → pop 3 → h=[5,6]
x=4: h=[4,6,5] → pop 4 → h=[5,6]

h[0]=5 → 2nd largest is 5 ✅
```

## Edge Cases

- `k == 1` → answer is max; heap size 1 always holds current max of processed prefix of "largest"
- `k == n` → answer is min of array
- duplicates: fine — heap compares values only

## Complexity

Time O(n log k), Space O(k).

---

# Problem 2: Top K Frequent Elements

## Pattern Identification

**Pattern: Hash count + size-K heap** (or bucket sort).  
Count frequencies O(n), then K most frequent via min-heap on frequency.

## Solution

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    h = []
    for num, freq in count.items():
        heapq.heappush(h, (freq, num))
        if len(h) > k:
            heapq.heappop(h)
    return [num for freq, num in h]
```

## Trace

```
nums = [1,1,1,2,2,3], k = 2
count = {1:3, 2:2, 3:1}

push (3,1): h=[(3,1)]
push (2,2): h=[(2,2),(3,1)]
push (1,3): h=[(1,3),(3,1),(2,2)] → pop (1,3) → h=[(2,2),(3,1)]

Answer: [2, 1] (order not required) ✅
```

## Complexity

Time O(n + u log k) where u = unique count. Space O(u + k).

**Stretch:** bucket sort by frequency → O(n) time.

---

# Problem 3: Merge K Sorted Lists

## Pattern Identification

**Pattern: Min-heap of K heads.**

## Solution

(See Pattern 2 framework above.)

## Trace

```
lists: [1→4→5], [1→3→4], [2→6]

Init heap: (1,0,n0), (1,1,n1), (2,2,n2)

pop (1,0) → emit 1, push 4 from list0
pop (1,1) → emit 1, push 3 from list1
pop (2,2) → emit 2, push 6 from list2
pop (3,1) → emit 3, push 4 from list1
pop (4,0) → emit 4, push 5 from list0
pop (4,1) → emit 4, list1 done
pop (5,0) → emit 5, list0 done
pop (6,2) → emit 6, done

Result: 1→1→2→3→4→4→5→6 ✅
```

## Complexity

O(N log K) time, O(K) space.

---

# Problem 4: K Closest Points to Origin

## Pattern Identification

**Pattern: Size-K max-heap by distance².**

## Solution

(See Pattern 4.)

## Trace

```
points = [[1,3],[-2,2]], k = 1

(1,3): dist2=10 → h=[(-10,1,3)]
(-2,2): dist2=8 < 10 → replace → h=[(-8,-2,2)]

Answer: [[-2,2]] ✅
```

## Complexity

O(n log k).

---

# Problem 5: Find Median from Data Stream

## Pattern Identification

**Pattern: Two heaps.**

## Solution

(See Pattern 3 `MedianFinder`.)

## Trace

```
add(40), add(10), add(20), add(30)  [using the framework]

After 40:          median 40
After 10,40:       median 25
After 10,20,40:    median 20
After 10,20,30,40: median 25
```

Verify with code mentally: lo holds lower half as negatives; hi upper half.

## Complexity

O(log n) per add, O(1) median.

---

# Problem 6: Reorganize String

## Pattern Identification

**Pattern: Max-heap of character frequencies + greedy placement.**

## Solution

(See Pattern 6.)

## Trace

```
s = "aab"
freq a:2 b:1
h = [(-2,'a'), (-1,'b')]

pop a,b → append "ab", push a back with count 1
h = [(-1,'a')]
append "a" → "aba" ✅
```

```
s = "aaab"
max freq 3 > (4+1)//2 = 2 → impossible → "" ✅
```

## Complexity

O(n log Σ).

---

# Problem 7: Task Scheduler (Simulation)

## Pattern Identification

**Pattern: Max-heap of frequencies + cooldown queue.**

## Trace (formula cross-check)

```
tasks = ["A","A","A","B","B","B"], n = 2
max_freq=3, num_max=2
formula: max(6, (3-1)*(2+1)+2) = max(6, 8) = 8
Schedule example: A B idle A B idle A B ✅
```

## Complexity

O(T log Σ) simulation; O(Σ) formula.

---

# Problem 8: Meeting Rooms II

## Pattern Identification

**Pattern: Min-heap of end times.**

## Trace

```
intervals = [[0,30],[5,10],[15,20]]
sorted same

[0,30]: h=[30] rooms=1
[5,10]: 30 > 5 → push 10 → h=[10,30] rooms=2
[15,20]: 10 ≤ 15 → pop 10, push 20 → h=[20,30] rooms=2

Answer: 2 ✅
```

---

# PART 10: TEST PROBLEMS (SOLO)

**Rules:** Identify pattern first. Then code. Then complexity. Trace one example.

### T1. Last Stone Weight

Stones with weights. Smash two heaviest: if equal both destroy; else push difference. Return last stone weight (or 0).

### T2. Smallest Range Covering Elements from K Lists

You have K sorted lists. Find the smallest range that includes at least one number from each list.

### T3. Sort Characters By Frequency

Return string sorted by decreasing character frequency. Ties any order.

### T4. Kth Smallest Element in a Sorted Matrix

Matrix rows and columns sorted ascending. Find Kth smallest. Prefer heap or binary search on value — justify.

### T5. Maximum Performance of a Team

(LeetCode-style) Pick at most k engineers maximizing `sum(speed) * min(efficiency)`. Hint: sort by efficiency desc; maintain heap of speeds.

### T6. Single-Threaded CPU

Tasks with enqueue time and processing time. Simulate CPU with a min-heap of available tasks by processing time.

### T7. PREVIEW Recognition Only

Explain in 4 sentences why Dijkstra uses a min-heap and what an outdated heap entry means. Do **not** implement full Dijkstra for Module 6 credit.

---

# PART 11: SOLUTIONS TO TEST PROBLEMS

---

## T1. Last Stone Weight

**Pattern:** Max-heap (negate).

```python
import heapq

def last_stone_weight(stones):
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        y = -heapq.heappop(h)
        x = -heapq.heappop(h)
        if y != x:
            heapq.heappush(h, -(y - x))
    return -h[0] if h else 0
```

**Trace:** `[2,7,4,1,8,1]` → smash 8,7 → push 1 → … → last 1.

**Complexity:** O(n log n).

---

## T2. Smallest Range Covering Elements from K Lists

**Pattern:** Min-heap of current heads + track global max among those heads. Advance the list that produced the current min.

```python
import heapq

def smallest_range(nums):
    h = []
    cur_max = float('-inf')
    for i, arr in enumerate(nums):
        heapq.heappush(h, (arr[0], i, 0))
        cur_max = max(cur_max, arr[0])

    best = float('-inf'), float('inf')

    while True:
        val, i, j = heapq.heappop(h)
        if cur_max - val < best[1] - best[0]:
            best = val, cur_max
        if j + 1 == len(nums[i]):
            break
        nxt = nums[i][j + 1]
        heapq.heappush(h, (nxt, i, j + 1))
        cur_max = max(cur_max, nxt)

    return list(best)
```

**Complexity:** O(N log K) where N = total elements.

---

## T3. Sort Characters By Frequency

```python
import heapq
from collections import Counter

def frequency_sort(s):
    count = Counter(s)
    h = [(-freq, ch) for ch, freq in count.items()]
    heapq.heapify(h)
    out = []
    while h:
        freq, ch = heapq.heappop(h)
        out.append(ch * (-freq))
    return "".join(out)
```

Or: `"".join(ch * freq for ch, freq in count.most_common())`.

---

## T4. Kth Smallest in Sorted Matrix

**Heap approach:** start with first column (or first row); pop min, push next in that row.

```python
import heapq

def kth_smallest(matrix, k):
    n = len(matrix)
    h = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(h)
    for _ in range(k):
        val, r, c = heapq.heappop(h)
        if c + 1 < n:
            heapq.heappush(h, (matrix[r][c + 1], r, c + 1))
    return val
```

**Complexity:** O(k log n). Binary search on value is O(n log(max−min)) — mention as alternative.

---

## T5. Maximum Performance of a Team

```python
import heapq

def max_performance(n, speed, efficiency, k):
    MOD = 10**9 + 7
    people = sorted(zip(efficiency, speed), reverse=True)
    h = []
    speed_sum = 0
    best = 0
    for eff, spd in people:
        heapq.heappush(h, spd)
        speed_sum += spd
        if len(h) > k:
            speed_sum -= heapq.heappop(h)
        best = max(best, speed_sum * eff)
    return best % MOD
```

**Why:** Sorting by efficiency means current `eff` is the team's min efficiency. Heap keeps top speeds under that constraint.

---

## T6. Single-Threaded CPU

```python
import heapq

def get_order(tasks):
    indexed = sorted((e, p, i) for i, (e, p) in enumerate(tasks))
    h = []
    time = 0
    i = 0
    n = len(tasks)
    order = []

    while len(order) < n:
        while i < n and indexed[i][0] <= time:
            e, p, idx = indexed[i]
            heapq.heappush(h, (p, idx))
            i += 1
        if h:
            p, idx = heapq.heappop(h)
            time += p
            order.append(idx)
        else:
            time = indexed[i][0]  # jump to next enqueue

    return order
```

---

## T7. PREVIEW Answer Key (Recognition)

Dijkstra always expands the node with the **smallest known distance** next — a min-heap of `(dist, node)` gives O(log V) extract-min. When a shorter path is found, a new entry is pushed rather than deleting the old one (Python has no decrease-key). Outdated larger-distance entries are skipped when popped if `d > dist[u]`. Full algorithm mastery is Module 8.

---

# PART 12: HEAPSORT (CONNECTION TO SORTING)

Heapsort: heapify O(n), then extract-min n times → O(n log n). In-place variant builds a max-heap and swaps root with end repeatedly.

```python
def heapsort_ascending(arr):
    """Educational — Python's Timsort is faster in practice; know heapsort for interviews."""
    import heapq
    h = arr[:]
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]
```

**Interview talking point:** Heapsort is O(n log n) worst-case (unlike quicksort's O(n²) worst), but poor cache locality vs quicksort; Python uses Timsort. You rarely code heapsort in interviews — you use `heapq` for priority-queue patterns.

---

# PART 13: DECREASE-KEY, INDEXED HEAPS & LAZY DELETION (DEPTH)

## Why interviews care

Dijkstra textbooks assume **decrease-key** in O(log n). Python `heapq` has no decrease-key. Two responses:

### Strategy A — Lazy insertion (standard with heapq)

Push a new `(new_dist, node)` without removing the old entry. When popping, ignore if `dist > best_known[node]`.

**Space tradeoff:** O(E) heap entries in worst case, not O(V).

### Strategy B — Indexed heap (rare to implement live)

Maintain `position[node] = index in heap array` and sift after updating key. Error-prone in a 20-minute interview — mention, don't implement unless asked.

### Lazy deletion for "remove arbitrary"

```python
# Example: delayed removal of values
from collections import Counter
import heapq

class LazyMinHeap:
    def __init__(self):
        self.h = []
        self.dead = Counter()

    def push(self, x):
        heapq.heappush(self.h, x)

    def remove(self, x):
        self.dead[x] += 1  # mark; physically remove later

    def _clean(self):
        while self.h and self.dead[self.h[0]] > 0:
            self.dead[self.h[0]] -= 1
            heapq.heappop(self.h)

    def pop(self):
        self._clean()
        return heapq.heappop(self.h)

    def peek(self):
        self._clean()
        return self.h[0]
```

Used in hard sliding-window median / "show current min after deletes" problems.

---

# PART 14: FREQUENCY HEAP FAMILY — UNIFIED RECIPE

Many problems are the same skeleton:

```
1. Count frequencies (Counter)
2. Push (-freq, item) into heap  # max-heap by frequency
3. Repeatedly pop the "most urgent" item(s)
4. Optionally push back with decremented frequency after a cooldown
```

| Problem | Step 3 detail |
|---|---|
| Top K frequent | Keep size-K min-heap on freq instead of max-heap of all |
| Reorganize string | Pop two different chars, append, push back if remaining |
| Task scheduler | Pop one, park in cooldown queue for n steps |
| Sort by frequency | Pop all, emit `char * freq` |
| Reduce array size to half | Pop largest freq bags until half elements covered |

**Recognition cue:** "rearrange / schedule / most frequent / cooldown / no two adjacent."

---

# PART 15: WORKED PROBLEM — FULL TRACE: TOP K FREQUENT WORDS (TIE RULES)

Problem: K most frequent words; higher freq first; ties → lexicographically smaller word first.

```python
import heapq
from collections import Counter

def top_k_frequent_words(words, k):
    count = Counter(words)
    # Min-heap of size k ordered by "worse first":
    # worse = lower freq, or same freq but lexicographically LARGER word
    # Python compares tuples left-to-right; we want to eject worse.
    # Store: (freq, word) in min-heap — WRONG for lex (ejects small words first).
    # Store custom: use (-freq) via sorting for clarity when ties matter:

    # Interview-clean approach:
    return sorted(count.keys(), key=lambda w: (-count[w], w))[:k]

    # Pure heap approach (size k) with inverted lex for min-heap ejection:
    # h stores (freq, word) where we want the "least valuable" at root to eject.
    # least valuable = small freq, or equal freq and lex-large word.
    # So push (freq, word) does NOT work for lex-large ejection.
    # Trick: push (freq, NegStr(word)) or just sort — prefer sort for ties.
```

**Teaching point:** When tie-breaking is non-numeric, **sorted with key** is often clearer than fighting `heapq` tuple order. Use heap when the ordering is a simple numeric priority.

---

# PART 16: WORKED PROBLEM — FULL TRACE: MERGE K SORTED ARRAYS

```python
import heapq

def merge_k_arrays(arrays):
    h = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(h, (arr[0], i, 0))
    out = []
    while h:
        val, i, j = heapq.heappop(h)
        out.append(val)
        if j + 1 < len(arrays[i]):
            heapq.heappush(h, (arrays[i][j + 1], i, j + 1))
    return out
```

**Trace**

```
arrays = [[1,4,7],[2,5,8],[3,6,9]]
init h: (1,0,0),(2,1,0),(3,2,0)
pop 1 → push 4
pop 2 → push 5
pop 3 → push 6
pop 4 → push 7
...
out = [1,2,3,4,5,6,7,8,9]
```

Same pattern as merge K lists — arrays instead of linked list nodes.

---

# PART 17: WORKED PROBLEM — FULL TRACE: TWO HEAPS MEDIAN

```
ops: add 41, add 35, add 62, add 5, find, add 97, find

After 41:   lo=[-41]              med=41
After 35:   lo=[-35], hi=[41]     med=38
After 62:   lo=[-41,-35], hi=[62] med=41
After 5:    lo=[-35,-5], hi=[41,62] med=38
After 97:   lo=[-41,-35,-5], hi=[62,97] med=41
```

Re-derive with the `addNum` code until muscle memory: always push to lo, move to hi, rebalance.

---

# PART 18: COMPLEXITY PROOFS WORTH SAYING OUT LOUD

### Why size-K top-K is O(n log K)

Each of n elements does at most one push/replace on a heap of size ≤ K → O(log K) each → O(n log K).

### Why merge-K is O(N log K)

N pops, each O(log K); N pushes of successors, each O(log K).

### Why Floyd heapify is O(n)

Let h = height = ⌊log₂ n⌋.  
Cost ≤ Σ_{i=0..h} (n/2^{i+1}) · i = O(n).

### Why naive n×insert is O(n log n)

Each insert into a heap of size i costs O(log i); Σ log i = log(n!) = Θ(n log n) by Stirling.

---

# PART 19: EDGE CASE MASTER LIST (HEAPS)

| Case | Handling |
|---|---|
| Empty heap pop | Guard / return sentinel |
| K = 0 | Return `[]` |
| K > n | Clamp to n or return all |
| All equal values | Heap still correct; median either value |
| Single element stream | Median = that element |
| Negative numbers + negation max-heap | Works for ints/floats |
| Objects without `__lt__` | Use `(priority, counter, obj)` |
| Duplicate priorities in Dijkstra PREVIEW | Counter or node id tie-break |
| Cooldown empty but tasks remain | Jump time / idle count |
| Impossible reorganize | `max_freq > (n+1)//2` |

---

# PART 20: INTERVIEW SCRIPT (60 SECONDS)

> "This needs repeated access to the current best element under inserts — that's a priority queue. In Python I'll use `heapq` as a min-heap. For max-heap I'll negate. For top-K I'll keep a size-K min-heap so the root is the threshold. Complexity O(n log K). I'll store `(priority, tie_id, payload)` so ties don't compare payloads. Edge cases: empty, K>n, duplicates."

Practice saying this until automatic.

---

# PART 21: MODULE 6 HEAP — SELF-CHECK

Before retention:

- [ ] Explain min-heap property + array indexing without notes
- [ ] State insert / extract / heapify complexities and why heapify is O(n)
- [ ] Write max-heap via negation without hesitation
- [ ] Push `(priority, counter, obj)` safely
- [ ] Implement top-K, merge-K, two-heap median from scratch
- [ ] Recognize task scheduler / reorganize as frequency max-heap
- [ ] Explain lazy deletion / why no decrease-key in heapq
- [ ] Label Dijkstra as PREVIEW only

**Next file in Module 6:** `Arrays/Advanced Patterns.md` (escalated sliding window + two pointers).  
**Retention:** `Retention Questions/Module 6 Retention.md`

---

*End of Heaps & Priority Queues lesson.*