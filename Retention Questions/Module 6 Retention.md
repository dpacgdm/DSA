<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 6 Retention.keys.md -->
> **Blind mode:** Section answer blocks moved to `keys/Module 6 Retention.keys.md`.


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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 6 Retention.keys.md`

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
