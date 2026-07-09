# MODULE 6 RETENTION — HEAPS + ADVANCED ARRAY PATTERNS

**Purpose:** Cumulative retention grill for Module 6 teach blocks.  
**Sources:** `Heaps/Heaps & Priority Queues.md`, `Arrays/Advanced Patterns.md`  
**Also pulls:** Module 1 window/two-pointer basics (contrast), hashing counts where needed.  
**Rules:** No notes. Identify pattern → approach → code → complexity → edges.  
**Governance:** Dijkstra items marked **PREVIEW** — recognition only, no Module 8 credit.

---

# SECTION A: RAPID FIRE — CONCEPTS & COMPLEXITY

Answer in 1–3 sentences unless code is requested.

---

## A1. Heap property

State the min-heap order property and the shape property. Is a heap a BST?

---

## A2. Index arithmetic

For a 0-indexed heap array, give formulas for parent, left child, and right child of index `i`.

---

## A3. Complexities

Fill in:

| Op | Time |
|---|---|
| peek min | |
| heappush | |
| heappop | |
| heapify (Floyd) | |

Why is Floyd heapify **not** O(n log n)?

---

## A4. Python trap

Why does `heapq` have no max-heap? Show how to implement max-heap for integers in one line of push and one line of pop.

---

## A5. Tuple TypeError

This crashes when priorities tie. Fix it.

```python
heapq.heappush(h, (dist, node_object))
```

---

## A6. Top-K shape

To find the K **largest** numbers online, do you use a min-heap or max-heap of size K? Why?

---

## A7. Median stream

Describe the two-heap invariant (what each heap stores, size relationship, how to read the median).

---

## A8. Window mindset

For **longest** substring under a constraint vs **minimum window substring**, when do you update the answer relative to the shrink loop?

---

## A9. Exactly K distinct

How do you count substrings with **exactly** K distinct characters using an `at_most` helper?

---

## A10. Container water

In container-with-most-water, why do you advance the pointer at the **shorter** line?

---

## A11. Trap water formula

Water above index `i` equals what, in terms of left_max and right_max?

---

## A12. Dutch flag

State the low/mid/high invariant regions. After swapping a `2` with `high`, do you increment `mid`? Why/why not?

---

## A13. Product window

Why does sliding window work for "subarray product < k" when all nums ≥ 1? What if `k <= 1`?

---

## A14. PREVIEW

In one sentence: what does Dijkstra store in its heap, and why might you skip a popped entry?

---

## A15. Heap vs sort

When is a size-K heap better than sorting for top-K? When is sort simpler/fine?

---

# SECTION A — ANSWERS

### A1
Min-heap: every parent ≤ children; root is global min. Shape: complete binary tree (filled level-by-level left to right). **Not** a BST — no left/right ordering between siblings; not fully sorted.

### A2
`parent = (i-1)//2`, `left = 2*i+1`, `right = 2*i+2`.

### A3
Peek O(1); push O(log n); pop O(log n); heapify **O(n)**. Most nodes are near leaves and sift short distances; sum of heights is a geometric series O(n).

### A4
`heapq` only implements min-heap. Push `-x`; pop with `-heappop(h)`.

### A5
Add a unique counter: `(dist, counter, node_object)` so equal distances never compare node objects.

### A6
**Min-heap** of size K. Root is the smallest of the current top-K (the threshold). Larger newcomers replace the root; everything in the heap is among the K largest.

### A7
`lo` = max-heap (negated) of lower half; `hi` = min-heap of upper half. All in `lo` ≤ all in `hi`. `|lo| == |hi|` or `|lo| == |hi|+1`. Odd: median = max(lo); even: average of max(lo) and min(hi).

### A8
Longest: shrink when **invalid**; update when valid (typically after shrink). Min window: shrink while **still valid**; update **inside** the shrink loop to minimize.

### A9
`at_most(k) - at_most(k-1)`.

### A10
Width only shrinks inward. Height is capped by the shorter line, so no pair that keeps the shorter index and moves the other inward can beat the current area. Discard the bottleneck (shorter) pointer.

### A11
`max(0, min(left_max[i], right_max[i]) - height[i])`.

### A12
`[0..low)` = 0s; `[low..mid)` = 1s; `[mid..high]` unknown; `(high..n)` = 2s. After swapping a 2, **do not** mid++ — the value swapped in is unknown and must be examined.

### A13
Products are monotonic non-decreasing when expanding (all ≥ 1). If `k <= 1`, no positive product can be `< k` → return 0.

### A14
PREVIEW: min-heap of `(distance, node)`; skip if popped distance is worse than the known `dist[u]` (lazy outdated entry).

### A15
Heap better when K ≪ n → O(n log K). Sort fine when K ≈ n or code simplicity matters → O(n log n).

---

# SECTION B: HEAP DRILLS

---

## B1. Kth Largest Element

Find the Kth largest element in an unsorted array. **Required:** O(n log k) heap solution (not full sort).

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

---

## B2. Top K Frequent

Return the K most frequent elements (any order).

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

---

## B3. Last Stone Weight

Smash two heaviest until ≤1 stone remains. Return weight (0 if none).

```
Input: [2,7,4,1,8,1]
Output: 1
```

---

## B4. Merge K Sorted Lists

Merge into one sorted list. Heap solution required.

```
lists = [1→4→5, 1→3→4, 2→6]
Output: 1→1→2→3→4→4→5→6
```

---

## B5. Median Finder

Implement `addNum` / `findMedian` with two heaps. Trace adds: 1, 2, 3 and state medians after each.

---

## B6. K Closest to Origin

```
points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]] (any order)
```

Use distance². Size-K heap.

---

## B7. Reorganize String

```
Input: "aab" → "aba"
Input: "aaab" → ""
```

---

## B8. Task Scheduler

```
tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
```

Give **both** the formula answer and a one-line justification of the formula.

---

## B9. Meeting Rooms II

```
intervals = [[0,30],[5,10],[15,20]]
Output: 2
```

---

## B10. Identify the pattern

"You receive a stream of integers; after each insertion you must return the current median in O(log n) update / O(1) query."

Name the structure.

---

# SECTION B — ANSWERS

---

### B1

**Pattern:** Size-K min-heap.

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

**Trace:** After processing, h holds `[5,6]`, peek 5.

**Complexity:** O(n log k) time, O(k) space.

---

### B2

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

**Complexity:** O(n + u log k).

---

### B3

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
    return 0 if not h else -h[0]
```

**Trace:** 8 vs 7 → 1; … eventually 1.

**Complexity:** O(n log n).

---

### B4

```python
import heapq

def merge_k_lists(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(h, (node.val, i, node))
    dummy = cur = ListNode(0)
    while h:
        val, i, node = heapq.heappop(h)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```

**Complexity:** O(N log K).

---

### B5

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []
        self.hi = []

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0
```

**Trace:**
- add 1 → median 1.0  
- add 2 → median 1.5  
- add 3 → median 2.0  

---

### B6

```python
import heapq

def k_closest(points, k):
    h = []
    for x, y in points:
        d = x*x + y*y
        if len(h) < k:
            heapq.heappush(h, (-d, x, y))
        elif d < -h[0][0]:
            heapq.heapreplace(h, (-d, x, y))
    return [[x, y] for _, x, y in h]
```

**Complexity:** O(n log k).

---

### B7

```python
import heapq
from collections import Counter

def reorganize_string(s):
    freq = Counter(s)
    if max(freq.values()) > (len(s) + 1) // 2:
        return ""
    h = [(-c, ch) for ch, c in freq.items()]
    heapq.heapify(h)
    out = []
    while len(h) >= 2:
        c1, a = heapq.heappop(h)
        c2, b = heapq.heappop(h)
        out.append(a)
        out.append(b)
        if c1 + 1:
            heapq.heappush(h, (c1 + 1, a))
        if c2 + 1:
            heapq.heappush(h, (c2 + 1, b))
    if h:
        c, ch = h[0]
        if c < -1:
            return ""
        out.append(ch)
    return "".join(out)
```

`"aab"` → `"aba"`; `"aaab"` early-exit `""`.

---

### B8

Formula: `max(len(tasks), (max_freq - 1) * (n + 1) + num_max)`  
= `max(6, (3-1)*(3)+2) = max(6,8) = 8`.

**Why:** `(max_freq-1)` full frames of size `(n+1)` for the most frequent task(s), plus the final occurrences of all tasks that share max frequency; if tasks fill more than that skeleton, answer is just `len(tasks)`.

---

### B9

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort()
    h = []
    for start, end in intervals:
        if h and h[0] <= start:
            heapq.heappop(h)
        heapq.heappush(h, end)
    return len(h)
```

**Trace:** ends heap grows to size 2.

**Complexity:** O(n log n).

---

### B10

Two heaps (max-heap lower half + min-heap upper half) / running median pattern.

---

# SECTION C: ADVANCED WINDOW & TWO POINTERS

---

## C1. Minimum Window Substring

```
s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

Implement need/have (or missing-count) solution. Trace until best becomes BANC.

---

## C2. Longest Substring with At Most K Distinct

```
s = "eceba", k = 2
Output: 3
```

---

## C3. Subarrays with Product Less Than K

```
nums = [10,5,2,6], k = 100
Output: 8
```

---

## C4. Container With Most Water

```
height = [1,8,6,2,5,4,8,3,7]
Output: 49
```

Code + 3-sentence proof of pointer move.

---

## C5. Trapping Rain Water

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

Give **O(1) space** two-pointer solution.

---

## C6. Sort Colors

```
nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]
```

Dutch National Flag only (no `sort()`, no counting-array-only as primary).

---

## C7. Character Replacement

```
s = "AABABBA", k = 1
Output: 4
```

---

## C8. Max Consecutive Ones III

```
nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
```

---

## C9. Exactly K Distinct (count)

```
s = "pqpqs", k = 2
```

Compute via `at_most`. Show the formula application (you may compute `at_most` values by hand).

---

## C10. Trap vs Container — contrast

In 4 bullets: same tools (two pointers), different goals, different move rules, different formulas.

---

# SECTION C — ANSWERS

---

### C1

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(need)
    window = Counter()
    best = float('inf')
    start = 0
    left = 0
    for right, ch in enumerate(s):
        window[ch] += 1
        if ch in need and window[ch] == need[ch]:
            missing -= 1
        while missing == 0:
            if right - left + 1 < best:
                best = right - left + 1
                start = left
            c = s[left]
            window[c] -= 1
            if c in need and window[c] < need[c]:
                missing += 1
            left += 1
    return "" if best == float('inf') else s[start:start+best]
```

**Key moment:** when right hits final `C`, shrink past `B A N C` boundaries until invalid; best length 4 `"BANC"`.

**Complexity:** O(|s|+|t|).

---

### C2

```python
from collections import defaultdict

def longest_at_most_k(s, k):
    if k <= 0:
        return 0
    count = defaultdict(int)
    left = distinct = best = 0
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

**Trace:** `"ece"` length 3 is best.

---

### C3

```python
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0
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

**Trace:** ans accumulates 1+2+2+3 = 8.

---

### C4

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
```

**Proof:** (1) Inward moves only decrease width. (2) Area with the current shorter line is capped by that height. (3) Any narrower pair keeping the shorter index cannot improve, so advance the shorter pointer.

---

### C5

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
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

**Complexity:** O(n) time, O(1) space. Answer 6.

---

### C6

```python
def sort_colors(nums):
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

---

### C7

```python
from collections import defaultdict

def character_replacement(s, k):
    count = defaultdict(int)
    left = max_freq = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

### C8

```python
def longest_ones(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best
```

Window of six 1s with two flips in the middle region → 6.

---

### C9

`exactly(k) = at_most(k) - at_most(k-1)`.

```
s = "pqpqs"
at_most(1) = 5
at_most(2) = 12
exactly(2) = 12 - 5 = 7
```

**Answer: 7.**

(Total substrings = 15; those with ≥3 distinct = 3, e.g. `pqs`, `qpqs`, `pqpqs`; those with exactly 1 distinct = 5; 15 − 3 − 5 = 7.)

---

### C10

- **Goal:** Container maximizes area between two lines; Trap accumulates water above each index.  
- **Move rule:** Container always moves the shorter line; Trap moves the side with smaller height, updating that side's max.  
- **Formula:** Container `min(h[L],h[R])*(R-L)`; Trap `min(Lmax,Rmax)-h[i]` per index.  
- **Same tool:** two pointers converging; different invariants.

---

# SECTION D: MIXED IDENTIFICATION (NO PATTERN LABEL)

For each: name the pattern in ≤8 words, then give time complexity of the optimal approach taught in Module 6.

---

## D1
Find Kth largest in unsorted array.

## D2
Smallest substring of `s` containing all chars of `t` (with multiplicity).

## D3
Max water two lines can hold.

## D4
Merge 50 sorted linked lists into one.

## D5
Count subarrays whose product is < 100.

## D6
Sort an array known to contain only 0/1/2 in one pass in-place.

## D7
Running median as numbers arrive.

## D8
Longest subarray with at most 2 distinct values (fruit baskets).

## D9
Minimum meeting rooms for intervals.

## D10
PREVIEW: shortest path in weighted graph, non-negative edges.

---

# SECTION D — ANSWERS

| # | Pattern | Complexity |
|---|---|---|
| D1 | Size-K min-heap (top-K) | O(n log k) |
| D2 | Min covering sliding window | O(n) |
| D3 | Converging TP, move shorter | O(n) |
| D4 | Min-heap of K list heads | O(N log K) |
| D5 | Variable window on product | O(n) |
| D6 | Dutch National Flag | O(n) |
| D7 | Two heaps median | O(log n)/add |
| D8 | At most K=2 distinct window | O(n) |
| D9 | Min-heap of end times | O(n log n) |
| D10 | PREVIEW Dijkstra min-heap of dist | O((V+E) log V) typical binary heap |

---

# SECTION E: DEBUG THE BUG

---

## E1

```python
def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, -x)  # max-heap of all
    for _ in range(k - 1):
        heapq.heappop(h)
    return -h[0]
```

This works but what is the complexity vs size-K min-heap? When does it matter?

---

## E2

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            right -= 1   # BUG?
        else:
            left += 1
    return best
```

What is wrong? Give a counterexample.

---

## E3

```python
def min_window(s, t):
    need = Counter(t)
    window = Counter()
    left = 0
    best = float('inf')
    start = 0
    for right, ch in enumerate(s):
        window[ch] += 1
        while window covers need:  # conceptually
            best = min(best, right - left + 1)
            start = left
            window[s[left]] -= 1
            left += 1
    return s[start:start+best]
```

Even if `covers` is implemented correctly, name two bugs in the update / return logic.

---

## E4

```python
def sort_colors(nums):
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            mid += 1  # BUG?
```

Why is `mid += 1` on the `else` branch wrong? Show a failing array.

---

# SECTION E — ANSWERS

### E1
Works: O(n + k log n) with full heapify O(n) then k pops — actually this builds heap of **n** via n pushes = O(n log n), then k pops. Size-K min-heap is O(n log k). Matters when k ≪ n (memory and speed).

### E2
Moves the **taller** side (when left shorter, it decrements right). Counterexample: `[1,8,6,2,5,4,8,3,7]` — algorithm can miss 49 and return smaller (e.g., fails to keep the tall left `8` paired with far right `7`). Correct action when `height[left] < height[right]` is `left += 1`.

### E3
(1) Updates `start` every shrink step even when length is **not** better — should only update when `right-left+1 < best`. (2) If no window found, still slices with `best=inf` — must return `""` when never covered. Also shrinking must re-check coverage after each remove (the while condition handles that if written properly).

### E4
After swapping a `2`, `nums[mid]` is an unknown (could be 0,1,2). Incrementing `mid` skips examining it. Fail case: `[1,2,0]` can end unsorted if mid advances over the swapped `0`.

---

# SECTION F: INTEGRATION / TRANSFER

---

## F1. Design choice

You need the 100 largest of 10 million scores. Heap or sort? Complexity of each?

---

## F2. Combine

"Find the K most frequent words; return them sorted by frequency desc, ties lexicographically ascending."

Outline: hash + heap (or sort). What do you store in the heap tuple to get tie-breaking right with `heapq`?

---

## F3. Contrast Module 1

Module 1: longest substring **without repeating** characters.  
Module 6: longest with **at most K distinct**.  

What is the same? What changes in the shrink condition?

---

## F4. Trap water — three approaches

Name three approaches and their space costs. Which is Module 6 primary interview target?

---

## F5. PREVIEW boundary

A problem says: "Cheapest flights within K stops." Is that Module 6 heap drill credit? What do you answer in an interview before Graphs?

---

# SECTION F — ANSWERS

### F1
Size-100 **min-heap**: O(n log 100) ≈ O(n). Full sort O(n log n) and O(n) memory for sorted copy — heap wins clearly.

### F2
`Counter` frequencies. For heap of size K: store `(-freq, word)` so higher freq comes first in min-heap-of-negatives… For "K most frequent" with lex ties: careful — use `(-freq, word)` in a max-frequency extraction, or sort `(-freq, word)` fully if K large. With min-heap of size K keeping best: push `(freq, word)` wrong for lex — use `(-freq, word)` in max-heap style or store `(freq, word)` in min-heap of size K where smaller freq ejects — ties: when freqs equal, eject lexicographically **larger** word if we want to keep lex-smaller among frequent… Interview-safe: `sorted(counter.keys(), key=lambda w: (-counter[w], w))[:k]`.

Heap tuple for size-K min-heap by "worse is smaller": `(freq, -ord_tie, word)` is messy; prefer sort for tie rules unless required.

### F3
Same: variable window + set/counter, O(n). Change: shrink when `distinct > K` instead of when current char already in set (K=window uniqueness unlimited vs K distinct budget). No-repeat is **not** exactly `at_most(∞)` — it's at most 1 of each char (frequency ≤1), a stronger constraint than distinct count alone… Actually no-repeat = all frequencies ≤ 1, equivalent to window size == distinct count. Related but shrink condition differs: shrink while `s[right]` still in set / freq>1.

### F4
Prefix/suffix arrays O(n) space; two pointers O(1) space; monotonic stack O(n) space. **Primary Module 6 interview target:** two pointers O(1) after explaining the formula.

### F5
**PREVIEW / Graphs** — not Module 6 mastery credit. Say: "This is Bellman-Ford or Dijkstra-with-stops / BFS-on-states; I know heaps extract min dist, but full graph shortest-path is a later module."

---

# SECTION G: TIMED SET BLUEPRINT (FOR LATER `timed-verified`)

Use only after `drilled`. Blind, no pattern labels. 45–60 min.

| # | Problem | Approx LC |
|---|---|---|
| 1 | Kth largest | 215 |
| 2 | Top K frequent | 347 |
| 3 | Min window substring | 76 |
| 4 | Container with most water | 11 |
| 5 | Trap rain water | 42 |
| 6 | Sort colors | 75 |
| 7 | Product less than K | 713 |
| 8 | Reorganize string / task scheduler (pick one) | 767 / 621 |

**Gate reminder:** Chat-guided solves = `drilled` only. This section is the template for blind timed evidence.

---

# SECTION H: SELF-SCORE CARD

Mark each ✓/✗ after attempting closed-book:

| Skill | Pass? |
|---|---|
| Heap index formulas + complexities | |
| Max-heap via negation | |
| Safe heap tuples with counter | |
| Top-K / Kth largest | |
| Merge K lists | |
| Two-heap median | |
| Frequency max-heap (reorganize/scheduler) | |
| Min window need/have | |
| At most / exactly K distinct | |
| Product < K | |
| Container water + proof | |
| Trap water O(1) | |
| Dutch flag | |
| PREVIEW Dijkstra recognition only | |

**Retention pass guideline:** ≥90% Section A correct, ≥80% of B+C coded correctly without notes, all E bugs identified. Failures → heat `weak` on ledger, re-teach, shorter next-due.

---

# SECTION I: SPACED LEDGER HOOKS (copy into `Metrics/Retention Ledger.md`)

| Subskill | Heat after grill | Notes |
|---|---|---|
| Heap property / heapify O(n) | | |
| heapq max-heap tricks | | |
| Top-K patterns | | |
| Two-heap median | | |
| Merge K / meeting rooms | | |
| Min window substring | | |
| K distinct windows | | |
| Product window | | |
| Container + trap water | | |
| Dutch flag | | |

---

*End of Module 6 Retention — full answers included above.*
