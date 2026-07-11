# Answer Key — Module 10 Retention.md

**Source questions:** `Retention Questions/Module 10 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
**Answer:** `children` (char → node) and `is_end` (whether a word ends here). Without `is_end`, prefixes look like words.

---


<!-- answer block 2 -->
**Answer:** Both **O(L)**. Independent of how many other words exist for the walk (space depends on shared prefixes).

---


<!-- answer block 3 -->
**Answer:** Search **False** (`is_end` false at `p`). StartsWith **True** (path exists).

---


<!-- answer block 4 -->
**Answer:** Set answers "is this exact string present?" in O(L). Autocomplete needs **all strings with a prefix** — set forces scanning all words unless you also store every prefix (memory) or use a trie/sorted structure.

---


<!-- answer block 5 -->
**Answer:** DFS/backtrack: `.` tries **every** child; normal char follows one edge. Worst case O(b^L).

---


<!-- answer block 6 -->
**Answer:** Problem asks for the **shortest** root. First end along the path is the shortest prefix root.

---


<!-- answer block 7 -->
**Answer:** Each index pushed ≤ once and popped ≤ once → ≤ 2n stack operations.

---


<!-- answer block 8 -->
**Answer:** Number of subarrays for which `arr[i]` is the (uniquely attributed) minimum — via previous-smaller and next-smaller spans — then `arr[i] * left_span * right_span`.

---


<!-- answer block 9 -->
**Answer:** So each subarray's minimum is credited to **exactly one** index when ties exist. Both sides strict (or both non-strict) double-counts or drops.

---


<!-- answer block 10 -->
**Answer:** Keep digits in **non-decreasing** order when possible: pop larger peaks while `k > 0` and top > current digit. Strip leading zeros; if `k` left, pop from end.

---


<!-- answer block 11 -->
**Answer:** Decreasing `(price, span)` pairs (or indices). Previous days with price ≤ today are collapsed once; each day pushed/popped at most once across the stream.

---


<!-- answer block 12 -->
**Answer:** Max → **decreasing** deque (front = max). Min → **increasing** deque (front = min). Always store **indices** to expire by window left.

---


<!-- answer block 13 -->
**Answer:** Two pointers + **two** monotonic deques (max and min). Shrink left while `max - min > limit`.

---


<!-- answer block 14 -->
**Answer:** Chunk can end at `i` when `max(arr[0..i]) == i`. Count such positions.

---


<!-- answer block 15 -->
**Answer:** Both **O(log n)**. Static range sums without updates → prefer **prefix sums** O(1) query.

---


<!-- answer block 16 -->
**Answer:** No updates (use prefix); window max (use mono deque); tiny n (brute OK). Mention BIT/segtree when updates interleave with range queries.

---


<!-- answer block 17 -->
**Answer:** Root → `c`→`a`→(`t*`,`r*`); root → `d`→`o`→`g*`. Stars = `is_end`. `ca` shares the `c-a` path.

---


<!-- answer block 18 -->
**Answer:** At each step you only follow edges that are prefixes of **some** dictionary word. Dead board paths die early. A bare set still explores paths that aren't prefixes unless you separately check prefixes (reinventing a trie).

---


<!-- answer block 19 -->
**Answer (one valid strictness scheme):**  
Compute prev/next smaller distances; e.g. with common LC907-style spans, total = 3·1·1 + 1·2·2 + 2·1·1 = 3+4+2 = **9**.  
Verify by enumeration: [3]=3, [3,1]=1, [3,1,2]=1, [1]=1, [1,2]=1, [2]=2 → sum 9.

---


<!-- answer block 20 -->
**Answer:** Build increasing: pop 4 before 3, pop 3 before 2, pop 2 before 1 → `"1219"`. Leftmost peaks removed preferentially.

---


<!-- answer block 21 -->
**Answer:** Same monotonic idea. Offline next-greater scans with full array; stock span is **online** — stack holds unresolved previous prices and merges spans when a new high arrives.

---


<!-- answer block 22 -->
**Answer:** `prefix(R) - prefix(L-1)`. Copy stores current values so `update` can apply **delta = new - old** to the BIT (BIT stores sums, not absolute set-without-delta unless you rebuild).

---


<!-- answer block 23 -->
**Answer:** Both work: check all prefixes via set, or walk trie once. Trie is cleaner O(L) without generating all prefix strings; set of roots is fine for short words / interview speed if clear.

---


<!-- answer block 24 -->
**Answer:**

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self._walk(word)
        return bool(node and node.is_end)

    def startsWith(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
```

**Complexity:** O(L) per op.

---


<!-- answer block 25 -->
**Answer:** Insert normal; search DFS as in lesson. Edge: `"."` on empty children → False; pattern longer than any word → False.

---


<!-- answer block 26 -->
**Answer:** Mono increasing for left/right spans + contribution; mod 10⁹+7. See lesson code. **Time O(n), Space O(n).**

**Edges:** all equal; single element; strictly sorted.

---


<!-- answer block 27 -->
**Answer:** Monotonic non-decreasing digit stack; strip zeros; return `"0"` if empty. O(n).

**Test:** `"10200", k=1` → `"200"`.

---


<!-- answer block 28 -->
**Answer:**

```python
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

---


<!-- answer block 29 -->
**Answer:** Dual mono deques + variable window (lesson code). O(n).

---


<!-- answer block 30 -->
**Answer:**

```python
def maxChunksToSorted(arr):
    chunks = mx = 0
    for i, x in enumerate(arr):
        mx = max(mx, x)
        if mx == i:
            chunks += 1
    return chunks
```

---


<!-- answer block 31 -->
**Answer:** Build trie of roots; for each sentence word walk until first `is_end` or fail. O(total characters).

---


<!-- answer block 32 -->
**Answer:** Fenwick `add` / `range_sum`; `update` uses delta. O(log n) per op. **Do not** require full segtree.

```python
# using Fenwick from exposure lesson
class NumArray:
    def __init__(self, nums):
        self.arr = nums[:]
        self.ft = Fenwick.from_array(nums)
    def update(self, i, val):
        self.ft.add(i, val - self.arr[i])
        self.arr[i] = val
    def sumRange(self, l, r):
        return self.ft.range_sum(l, r)
```

---


<!-- answer block 33 -->
**Answer:** Trie of words; DFS from each cell walking trie; mark board `#`; record at `is_end`; unmark; optional prune empty trie branches. Complexity O(R·C·4^L) worst with heavy pruning in practice.

---


<!-- answer block 34 -->
**Answer:** **False.** Monotonic deque is the interview solution. Segtree works but is overkill.

---


<!-- answer block 35 -->
**Answer:** **False.** Lazy is out of Phase A scope. Exposure = recognize + Fenwick sum optional.

---


<!-- answer block 36 -->
**Answer:** "Currently prefix sums. If we need point updates, I'd switch to Fenwick/segment tree for O(log n) update and query."

---


<!-- answer block 37 -->
**Answer:** Stack is the natural structure for prev/next smaller. Deque is for window extrema. Wrong tool if you force deque without a window.

---


<!-- answer block 38 -->
**Answer:** Usually no — walk to prefix node and DFS subtree. Precomputed top-k is a **design** optimization (space/time tradeoff), Phase C flavored.

---


<!-- answer block 39 -->
**Answer:** Daily temps usually offline array → distances to next warmer. Stock span is online consecutive ≤ days including today; stack merges spans.

---


<!-- answer block 40 -->
**Answer:** Yes — increasing stack for previous/next smaller. Module 10 builds on that for contribution problems.

---


<!-- answer block 41 -->
**Answer:** Prefix+hash: subarray problems on a **fixed** array (sum=k, etc.). Fenwick: **mutable** array with repeated range sums.

---


<!-- answer block 42 -->
**Answer:** Instant recovery of the full string without rebuilding characters on the path; easy dedupe by nulling `word` after find.

---


<!-- answer block 43 -->
**Answer:** Prevent reusing the same cell in one path; unmark = backtrack so other paths can use the cell.

---


<!-- answer block 44 -->
**Answer:** `2 * 3 = 6`.

---


<!-- answer block 45 -->
**Answer:** (sum of subarray maximums) − (sum of subarray minimums).

---


<!-- answer block 46 -->
**Answer:** No pops during scan; remaining `k` digits removed from the **end** (largest place values already optimal on the left).

---


<!-- answer block 47 -->
**Answer:** Stock span is online (stream). Daily temps usually offline full array → distances to next warmer day.

---


<!-- answer block 48 -->
**Answer:** `maxq.popleft()` (same for `minq`) — expire indices outside the window.

---


<!-- answer block 49 -->
**Answer:** 3 — every prefix max equals index.

---


<!-- answer block 50 -->
**Answer:** `prefix(0) - prefix(-1) = A[0] - 0 = A[0]`.

---


<!-- answer block 51 -->
**Answer:** False — exposure only; tries + monotonic are the weighted half.

---


<!-- answer block 52 -->
**Answer:** `[5,10]` — `-5` dies against 10.

---


<!-- answer block 53 -->
**Answer:** Typically scan right-to-left maintaining candidates for the '3' and best '2' (`third`).

---


<!-- answer block 54 -->
**Answer:** `delta = new_val - old_val`, not the raw new value.

---


<!-- answer block 55 -->
**Answer:** Fixed lowercase a–z alphabet; slightly simpler indexing `ord(c)-97`.

---


<!-- answer block 56 -->
**Answer:** Force-flush remaining bars on the stack at the end / avoid empty-stack edge cases.

---


<!-- answer block 57 -->
**Answer:** Per row, maintain heights of consecutive 1s; run largest-rectangle-in-histogram.

---


<!-- answer block 58 -->
**Answer:** When current char is smaller **and** top appears again later (`last[top] > i`).

---


<!-- answer block 59 -->
**Answer:** False — length 3 pattern can't match length 2 word; also middle `.` needs a child that then has `a`.

---


<!-- answer block 60 -->
**Answer:** O(T) time and O(T) space worst case (no sharing).

---


<!-- answer block 61 -->
**Answer:** Increasing (front = current min index).

---


<!-- answer block 62 -->
**Answer:** Yes if constraints tiny (naive) or if you code segtree; Fenwick is the short exposure path. Say constraint-driven choice.

---


<!-- answer block 63 -->
**Answer:** Prefix = static; Fenwick = dynamic updates.

---


<!-- answer block 64 -->
**Answer:** Not directly — search demands `is_end`. You need a walk that ignores `is_end`, or store end differently.

---


<!-- answer block 65 -->
**Answer:** When you don't need distances or window expiry by index (e.g., some next-greater-value-only problems). Window problems need indices.

---


<!-- answer block 66 -->
**Answer:** Trie has `a-b-a*` and `b-a*`. From (0,0): a→b→a finds `aba`. From (0,1): b→a finds `ba`. Mark/unmark prevents using same `a` twice in one path incorrectly — for `aba` the two a's are different cells. Return both (order arbitrary).

---


<!-- answer block 67 -->
**Answer:** Enumeration: [1],[1,2],[1,2,1],[2],[2,1],[1] → mins 1,1,1,2,1,1 sum=7.  
Contribution must total 7. Middle `2` only owns subarrays where it's min — only `[2]` → contrib 2. The two `1`s split the rest via strictness rules.

---


<!-- answer block 68 -->
**Answer:** Last indices: a:3,b:4,c:5? `"bcabc"` → b:3,c:4,a:2 wait: indices b0 c1 a2 b3 c4. last={b:3,c:4,a:2}.  
Build increasing unique: b→bc→ a pops c (c appears later), pops b (b appears later) → a → ab → abc. Result `"abc"`.

---


<!-- answer block 69 -->
**Answer:** Need both max and min of current window in O(1). One deque only tracks one extremum.

---


<!-- answer block 70 -->
**Answer:** "Tree of partial sums keyed by lowest set bit. Point add updates O(log n) indices; prefix sum folds O(log n) blocks; range = prefix difference. I keep a mirror array for set-updates via deltas. Prefer this over segtree when only sums matter."

---


<!-- answer block 71 -->
**Answer:** Insert/search/startsWith as standard. Delete: clear `is_end`, prune upward while node has no children and not `is_end`. See Advanced lesson Part 7A.

---


<!-- answer block 72 -->
**Answer:** On insert, `delta = val - old`; add `delta` to `path_sum` on every node along the key. `sum(prefix)` = walk to prefix node, return `path_sum`.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.path_sum = 0

class MapSum:
    def __init__(self):
        self.root = TrieNode()
        self.vals = {}

    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)
        self.vals[key] = val
        node = self.root
        for c in key:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
            node.path_sum += delta

    def sum(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return 0
            node = node.children[c]
        return node.path_sum
```

---


<!-- answer block 73 -->
**Answer:**

```python
def subArrayRanges(nums):
    def sum_ext(arr, want_max):
        n = len(arr)
        left, right = [0]*n, [0]*n
        stack = []
        for i in range(n):
            if want_max:
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
            else:
                while stack and arr[stack[-1]] >= arr[i]:
                    stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)
        stack = []
        for i in range(n-1, -1, -1):
            if want_max:
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
            else:
                while stack and arr[stack[-1]] > arr[i]:
                    stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)
        return sum(arr[i]*left[i]*right[i] for i in range(n))
    return sum_ext(nums, True) - sum_ext(nums, False)
```

**Time O(n), Space O(n).**

---


<!-- answer block 74 -->
**Answer:**

```python
def largestRectangleArea(heights):
    h = [0] + heights + [0]
    stack = []
    best = 0
    for i in range(len(h)):
        while stack and h[stack[-1]] > h[i]:
            height = h[stack.pop()]
            width = i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best
```

Trace `[2,4]` → with sentinels `[0,2,4,0]`: pop 4 width 1 area 4; pop 2 width 2 area 4; best=4.

---


<!-- answer block 75 -->
**Answer:** Row-by-row heights + `largestRectangleArea`. See lesson. O(R·C).

---


<!-- answer block 76 -->
**Answer:** Code in lesson Part 8F. Test `"cbacdcbc"` → `"acdb"`.

---


<!-- answer block 77 -->
**Answer:** `[10]` — 2 and -5 collide (2 dies), 10 and -5 collide (-5 dies).

```python
# full code in Advanced lesson P9
```

---


<!-- answer block 78 -->
**Answer:**

```python
def find132pattern(nums):
    stack = []
    third = float("-inf")
    for j in range(len(nums)-1, -1, -1):
        if nums[j] < third:
            return True
        while stack and stack[-1] < nums[j]:
            third = stack.pop()
        stack.append(nums[j])
    return False
```

---


<!-- answer block 79 -->
**Answer:** All increasing → spans `1,2,3,4,5` (each collapses all previous).

---


<!-- answer block 80 -->
**Answer:** Only equal elements windows. Dual deques still work; limit 0 means max==min.

---


<!-- answer block 81 -->
**Answer:** Initial sum=10. After A[2]=8, sum(2,3)=8+4=12. Fenwick add(2,5); range_sum uses prefixes.

---


<!-- answer block 82 -->
**Answer:** Any order OK unless specified. Dedupe with `nxt.word = None`.

---


<!-- answer block 83 -->
**Answer:** Trie DFS with `modified` budget 1, or brute compare all words length-equal with diff==1. See lesson P6.

---


<!-- answer block 84 -->
**Answer:** Maintain increasing stack of chunk max values; when a new smaller value arrives, merge chunks by popping until maxes consistent; push back the max of merged region. `len(stack)` = chunks.

---


<!-- answer block 85 -->
**Answer:** False — contiguous subarrays depend on positions; sorting destroys structure.

---


<!-- answer block 86 -->
**Answer:** False — search is boolean exact. Need prefix node + subtree enumeration.

---


<!-- answer block 87 -->
**Answer:** Using `>` (not `>=`) can leave equal bars; width accounting still works with care. Many solutions use `>=` when popping to treat equals as boundaries differently — know your formula. Sentinels simplify.

---


<!-- answer block 88 -->
**Answer:** Overkill for one word — plain DFS/backtracking on board is enough. Trie shines for **many** words (Word Search II).

---


<!-- answer block 89 -->
**Answer:** Not with the same simple prev/next smaller — GCD structure differs (need sparse table / segtree / other). Don't force mono stack.

---


<!-- answer block 90 -->
**Answer:** Yes one call can pop many; amortized O(1) across n calls. Say amortized in interviews.

---


<!-- answer block 91 -->
**Answer:** Unnecessary — prefix+hash is the right tool. Fenwick if array mutates between queries.

---


<!-- answer block 92 -->
**Answer:** Shared: monotonic decreasing stack of unresolved indices/prices. Temps: offline distances. Span: online merged spans.

---


<!-- answer block 93 -->
**Answer:** Second deque for min + variable shrink condition on `max-min`.

---


<!-- answer block 94 -->
**Answer:** Reduction layer: per-row heights of consecutive 1s.

---


<!-- answer block 95 -->
**Answer:** Tiny root set, short words, want less code — check prefixes against set. Large shared prefixes / interview asks for trie → trie.

---


<!-- answer block 96 -->
**Answer:** No for startsWith. Yes if you also need search.


<!-- answer block 97 -->
**Answer:** `"0"` (remove both; empty → `"0"`).


<!-- answer block 98 -->
**Answer:** `1`.


<!-- answer block 99 -->
**Answer:** `[3,3,-1,5,5,6,7]` (classic LC 239).


<!-- answer block 100 -->
**Answer:** Usually False unless empty inserted / root.is_end True.


<!-- answer block 101 -->
**Answer:** Prefix sums.

---


<!-- answer block 102 -->
**Answer:**

```python
class Node:
    def __init__(self):
        self.children = [None]*26
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = Node()
    def _idx(self, c):
        return ord(c) - 97
    def insert(self, word):
        node = self.root
        for c in word:
            i = self._idx(c)
            if not node.children[i]:
                node.children[i] = Node()
            node = node.children[i]
        node.is_end = True
    def search(self, word):
        node = self._walk(word)
        return bool(node and node.is_end)
    def startsWith(self, prefix):
        return self._walk(prefix) is not None
    def _walk(self, s):
        node = self.root
        for c in s:
            i = self._idx(c)
            if not node.children[i]:
                return None
            node = node.children[i]
        return node
```

---


<!-- answer block 103 -->
**Answer:**

```python
class WordDictionary:
    def __init__(self):
        self.root = {}
    def addWord(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True
    def search(self, word):
        def dfs(i, node):
            if i == len(word):
                return "$" in node
            c = word[i]
            if c == ".":
                return any(dfs(i+1, nxt) for k,nxt in node.items() if k != "$")
            if c not in node:
                return False
            return dfs(i+1, node[c])
        return dfs(0, self.root)
```

---


<!-- answer block 104 -->
**Answer:** Trie preferred for O(L). Hash alternate:

```python
def replaceWords(dictionary, sentence):
    roots = set(dictionary)
    def rep(w):
        for i in range(1, len(w)+1):
            if w[:i] in roots:
                return w[:i]
        return w
    return " ".join(rep(w) for w in sentence.split())
```

---


<!-- answer block 105 -->
**Answer:**

```python
def sumSubarrayMins(arr):
    MOD = 10**9+7
    n = len(arr)
    left, right = [0]*n, [0]*n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    return sum(arr[i]*left[i]*right[i] for i in range(n)) % MOD
```

Trace `[11,81,94,43,3]` mentally: 3 dominates many subarrays as min — large contribution.

---


<!-- answer block 106 -->
**Answer:** Stack builds; pops to remove; strip zeros → `"0"`.

---


<!-- answer block 107 -->
**Answer:** Spans `1,2,3` (≤ allows equals to collapse).

---


<!-- answer block 108 -->
**Answer:** Window `[1,2,4,7]` has max−min=6>5; best length 3 e.g. `[2,4,7]`? 7-2=5 OK length 3; `[1,2,4]` length 3. Answer 3? Actually `[1,2,4,7]` invalid; check `[2,4,7]`=5 OK. LC answer often 3.

Full code dual deque from lesson.

---


<!-- answer block 109 -->
**Answer:** 4 — see lesson trace.

---


<!-- answer block 110 -->
**Answer:** Mono increasing + sentinels; area 10.

---


<!-- answer block 111 -->
**Answer:** `[]` — equal size both explode.

---


<!-- answer block 112 -->
**Answer:** False / True (`1,4,2`).

---


<!-- answer block 113 -->
**Answer:** See exposure lesson LC307; delta update; range_sum via prefix diff.

---


