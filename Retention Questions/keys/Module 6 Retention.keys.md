# Answer Key — Module 6 Retention.md

**Source questions:** `Retention Questions/Module 6 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

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


> **Answer key:** `Retention Questions/keys/Module 6 Retention.keys.md` (block 1)

### C10

- **Goal:** Container maximizes area between two lines; Trap accumulates water above each index.  
- **Move rule:** Container always moves the shorter line; Trap moves the side with smaller height, updating that side's max.  
- **Formula:** Container `min(h[L],h[R])*(R-L)`; Trap `min(Lmax,Rmax)-h[i]` per index.  
- **Same tool:** two pointers converging; different invariants.

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


