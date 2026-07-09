# MODULE 10 RETENTION — TRIES, MONOTONIC DEEP DIVE, FENWICK EXPOSURE

**With answers.** Blind first: cover answers, solve/speak, then check.

**Materials:**
- `Advanced/Tries & Monotonic.md`
- `Advanced/Segment & Fenwick Exposure.md` (**exposure only**)

**Cumulative light pull:** stacks/queues mono intro (M4), sliding window (M1/M6), hashing vs trie judgment, recursion/backtracking for wildcard / board+trie.

**Pass bar (suggested):** Rapid fire ≥ 80% · Conceptual teach-back solid · Problems ≥ 6/8 · Fenwick section = recognition + simple reasoning (not CP mastery). Tag misses.

**Label:** Fenwick/segment questions are **exposure**. Failing to hand-write a full segment tree does **not** fail Module 10 if tries + monotonic are strong and you can explain when BIT/segtree apply.

---

# SECTION A: RAPID FIRE

---

## A1. What two fields does every trie node need at minimum?

**Answer:** `children` (char → node) and `is_end` (whether a word ends here). Without `is_end`, prefixes look like words.

---

## A2. Time of insert and exact search for a word of length L?

**Answer:** Both **O(L)**. Independent of how many other words exist for the walk (space depends on shared prefixes).

---

## A3. `search("app")` after only inserting `"apple"` — True or False? `startsWith("app")`?

**Answer:** Search **False** (`is_end` false at `p`). StartsWith **True** (path exists).

---

## A4. Why is a hash set enough for exact dictionary membership but weak for autocomplete?

**Answer:** Set answers "is this exact string present?" in O(L). Autocomplete needs **all strings with a prefix** — set forces scanning all words unless you also store every prefix (memory) or use a trie/sorted structure.

---

## A5. Wildcard `.` in Word Dictionary — what changes in search?

**Answer:** DFS/backtrack: `.` tries **every** child; normal char follows one edge. Worst case O(b^L).

---

## A6. Replace words: why stop at the first `is_end` while walking?

**Answer:** Problem asks for the **shortest** root. First end along the path is the shortest prefix root.

---

## A7. Monotonic stack O(n) law?

**Answer:** Each index pushed ≤ once and popped ≤ once → ≤ 2n stack operations.

---

## A8. Sum of subarray minimums: what do you count per index?

**Answer:** Number of subarrays for which `arr[i]` is the (uniquely attributed) minimum — via previous-smaller and next-smaller spans — then `arr[i] * left_span * right_span`.

---

## A9. Why asymmetric strictness on left vs right spans for equal elements?

**Answer:** So each subarray's minimum is credited to **exactly one** index when ties exist. Both sides strict (or both non-strict) double-counts or drops.

---

## A10. Remove k digits for smallest number — stack invariant?

**Answer:** Keep digits in **non-decreasing** order when possible: pop larger peaks while `k > 0` and top > current digit. Strip leading zeros; if `k` left, pop from end.

---

## A11. Stock span: what does the stack store and why amortized O(1)?

**Answer:** Decreasing `(price, span)` pairs (or indices). Previous days with price ≤ today are collapsed once; each day pushed/popped at most once across the stream.

---

## A12. Sliding window max vs min — deque order?

**Answer:** Max → **decreasing** deque (front = max). Min → **increasing** deque (front = min). Always store **indices** to expire by window left.

---

## A13. Longest subarray with max−min ≤ limit — tools?

**Answer:** Two pointers + **two** monotonic deques (max and min). Shrink left while `max - min > limit`.

---

## A14. Max chunks (permutation 0..n-1) — one-line rule?

**Answer:** Chunk can end at `i` when `max(arr[0..i]) == i`. Count such positions.

---

## A15. Fenwick exposure: point update + range sum complexities?

**Answer:** Both **O(log n)**. Static range sums without updates → prefer **prefix sums** O(1) query.

---

## A16. When is Fenwick/segment overkill in an interview?

**Answer:** No updates (use prefix); window max (use mono deque); tiny n (brute OK). Mention BIT/segtree when updates interleave with range queries.

---

# SECTION B: CONCEPTUAL TEACH-BACK

---

## B1. Draw/describe a trie after inserting `cat`, `car`, `dog`. Where are `is_end` flags?

**Answer:** Root → `c`→`a`→(`t*`,`r*`); root → `d`→`o`→`g*`. Stars = `is_end`. `ca` shares the `c-a` path.

---

## B2. Explain Word Search II pruning: why trie + board DFS beats "DFS + set of words" alone?

**Answer:** At each step you only follow edges that are prefixes of **some** dictionary word. Dead board paths die early. A bare set still explores paths that aren't prefixes unless you separately check prefixes (reinventing a trie).

---

## B3. Derive contribution for sum of subarray mins on `[3,1,2]` (mod not needed). Walk spans.

**Answer (one valid strictness scheme):**  
Compute prev/next smaller distances; e.g. with common LC907-style spans, total = 3·1·1 + 1·2·2 + 2·1·1 = 3+4+2 = **9**.  
Verify by enumeration: [3]=3, [3,1]=1, [3,1,2]=1, [1]=1, [1,2]=1, [2]=2 → sum 9.

---

## B4. Remove k digits `"1432219"`, k=3 — narrate pops.

**Answer:** Build increasing: pop 4 before 3, pop 3 before 2, pop 2 before 1 → `"1219"`. Leftmost peaks removed preferentially.

---

## B5. Online stock span vs offline next greater — relationship?

**Answer:** Same monotonic idea. Offline next-greater scans with full array; stock span is **online** — stack holds unresolved previous prices and merges spans when a new high arrives.

---

## B6. Fenwick: what does range sum(L,R) reduce to? Why keep a copy of the array for LC307 updates?

**Answer:** `prefix(R) - prefix(L-1)`. Copy stores current values so `update` can apply **delta = new - old** to the BIT (BIT stores sums, not absolute set-without-delta unless you rebuild).

---

## B7. Trie vs dict of words for Replace Words — tradeoff?

**Answer:** Both work: check all prefixes via set, or walk trie once. Trie is cleaner O(L) without generating all prefix strings; set of roots is fine for short words / interview speed if clear.

---

# SECTION C: PROBLEM SOLVING (WITH ANSWERS)

---

## C1. Implement Trie (insert / search / startsWith)

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

## C2. WordDictionary with `.`

**Answer:** Insert normal; search DFS as in lesson. Edge: `"."` on empty children → False; pattern longer than any word → False.

---

## C3. Sum of Subarray Minimums

**Answer:** Mono increasing for left/right spans + contribution; mod 10⁹+7. See lesson code. **Time O(n), Space O(n).**

**Edges:** all equal; single element; strictly sorted.

---

## C4. Remove K Digits

**Answer:** Monotonic non-decreasing digit stack; strip zeros; return `"0"` if empty. O(n).

**Test:** `"10200", k=1` → `"200"`.

---

## C5. StockSpanner

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

## C6. Longest Subarray max−min ≤ limit

**Answer:** Dual mono deques + variable window (lesson code). O(n).

---

## C7. Max Chunks To Sorted (0..n-1 permutation)

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

## C8. Replace Words

**Answer:** Build trie of roots; for each sentence word walk until first `is_end` or fail. O(total characters).

---

## C9. [Exposure] NumArray mutable range sum via Fenwick

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

## C10. [Hard] Sketch Word Search II approach (code optional)

**Answer:** Trie of words; DFS from each cell walking trie; mark board `#`; record at `is_end`; unmark; optional prune empty trie branches. Complexity O(R·C·4^L) worst with heavy pruning in practice.

---

# SECTION D: TRICK / JUDGMENT

---

## D1. True/False: You need a segment tree for sliding window maximum.

**Answer:** **False.** Monotonic deque is the interview solution. Segtree works but is overkill.

---

## D2. True/False: Module 10 complete requires coding lazy segment trees.

**Answer:** **False.** Lazy is out of Phase A scope. Exposure = recognize + Fenwick sum optional.

---

## D3. For static array range sums, interviewer asks to optimize updates later — what do you say?

**Answer:** "Currently prefix sums. If we need point updates, I'd switch to Fenwick/segment tree for O(log n) update and query."

---

## D4. Can contribution technique for subarray mins use a deque instead of stack?

**Answer:** Stack is the natural structure for prev/next smaller. Deque is for window extrema. Wrong tool if you force deque without a window.

---

## D5. Autocomplete: is storing top-k at every trie node required for LC?

**Answer:** Usually no — walk to prefix node and DFS subtree. Precomputed top-k is a **design** optimization (space/time tradeoff), Phase C flavored.

---

# SECTION E: CUMULATIVE PULL (LIGHT)

---

## E1. Daily temperatures (M4) vs stock span — one difference?

**Answer:** Daily temps usually offline array → distances to next warmer. Stock span is online consecutive ≤ days including today; stack merges spans.

---

## E2. Histogram largest rectangle — still mono stack?

**Answer:** Yes — increasing stack for previous/next smaller. Module 10 builds on that for contribution problems.

---

## E3. Prefix sum + hash vs Fenwick — when each?

**Answer:** Prefix+hash: subarray problems on a **fixed** array (sum=k, etc.). Fenwick: **mutable** array with repeated range sums.

---

# SECTION F: SELF-AUDIT

| Check | Done? |
|---|---|
| Trie insert/search/prefix/`is_end` cold | |
| Wildcard + replace words reasoning | |
| Contribution / remove k digits / stock span / dual deque | |
| Fenwick: when + O(log n) + delta update idea | |
| Did not confuse exposure with mastery | |
| Ledger + scoreboard updated | |
| Timed verify for M10 patterns still required for `complete` | |

---

# SECTION G: EXPANDED RAPID FIRE (A17–A40)

---

## A17. What does storing `word` on a trie terminal buy you in Word Search II?

**Answer:** Instant recovery of the full string without rebuilding characters on the path; easy dedupe by nulling `word` after find.

---

## A18. Why mark board cells `#` and unmark after DFS?

**Answer:** Prevent reusing the same cell in one path; unmark = backtrack so other paths can use the cell.

---

## A19. Contribution: if `left[i]=2` and `right[i]=3`, how many subarrays have `arr[i]` as exclusive min?

**Answer:** `2 * 3 = 6`.

---

## A20. Sum of subarray ranges = ?

**Answer:** (sum of subarray maximums) − (sum of subarray minimums).

---

## A21. Remove k digits on an already non-decreasing number — what happens?

**Answer:** No pops during scan; remaining `k` digits removed from the **end** (largest place values already optimal on the left).

---

## A22. Stock span vs daily temperatures — online vs offline?

**Answer:** Stock span is online (stream). Daily temps usually offline full array → distances to next warmer day.

---

## A23. Dual deque window: what do you do when `left` advances past `maxq[0]`?

**Answer:** `maxq.popleft()` (same for `minq`) — expire indices outside the window.

---

## A24. Max chunks permutation: `arr=[0,1,2]` chunks?

**Answer:** 3 — every prefix max equals index.

---

## A25. Fenwick `range_sum(0,0)` equals?

**Answer:** `prefix(0) - prefix(-1) = A[0] - 0 = A[0]`.

---

## A26. True/False: Segment tree is required for Phase A complete.

**Answer:** False — exposure only; tries + monotonic are the weighted half.

---

## A27. Asteroid collision: `[5,10,-5]` result?

**Answer:** `[5,10]` — `-5` dies against 10.

---

## A28. 132 pattern: need i < j < k with nums[i] < nums[k] < nums[j]. Mono direction?

**Answer:** Typically scan right-to-left maintaining candidates for the '3' and best '2' (`third`).

---

## A29. Map Sum: overwrite key — what do you add along the path?

**Answer:** `delta = new_val - old_val`, not the raw new value.

---

## A30. Trie children as `list[26]` vs `dict` — when list?

**Answer:** Fixed lowercase a–z alphabet; slightly simpler indexing `ord(c)-97`.

---

## A31. Histogram sentinels of height 0 — why?

**Answer:** Force-flush remaining bars on the stack at the end / avoid empty-stack edge cases.

---

## A32. Maximal rectangle in binary matrix — reduction?

**Answer:** Per row, maintain heights of consecutive 1s; run largest-rectangle-in-histogram.

---

## A33. Remove duplicate letters: when may you pop the stack top?

**Answer:** When current char is smaller **and** top appears again later (`last[top] > i`).

---

## A34. Word Dictionary: search `"a.a"` with only `"aa"` inserted?

**Answer:** False — length 3 pattern can't match length 2 word; also middle `.` needs a child that then has `a`.

---

## A35. Complexity of building trie from words with total characters T?

**Answer:** O(T) time and O(T) space worst case (no sharing).

---

## A36. Sliding window minimum deque order?

**Answer:** Increasing (front = current min index).

---

## A37. LC 307 without Fenwick — acceptable?

**Answer:** Yes if constraints tiny (naive) or if you code segtree; Fenwick is the short exposure path. Say constraint-driven choice.

---

## A38. Prefix sums vs Fenwick one-liner?

**Answer:** Prefix = static; Fenwick = dynamic updates.

---

## A39. Can `startsWith` be implemented using `search`?

**Answer:** Not directly — search demands `is_end`. You need a walk that ignores `is_end`, or store end differently.

---

## A40. Monotonic stack storing values not indices — when OK?

**Answer:** When you don't need distances or window expiry by index (e.g., some next-greater-value-only problems). Window problems need indices.

---

# SECTION H: MORE CONCEPTUAL TEACH-BACKS

---

## B8. Walk Word Search II on a 1×3 board `a b a` with words `["aba","ba"]`.

**Answer:** Trie has `a-b-a*` and `b-a*`. From (0,0): a→b→a finds `aba`. From (0,1): b→a finds `ba`. Mark/unmark prevents using same `a` twice in one path incorrectly — for `aba` the two a's are different cells. Return both (order arbitrary).

---

## B9. Derive sum of subarray mins for `[1,2,1]` with asymmetric spans. Show enumeration.

**Answer:** Enumeration: [1],[1,2],[1,2,1],[2],[2,1],[1] → mins 1,1,1,2,1,1 sum=7.  
Contribution must total 7. Middle `2` only owns subarrays where it's min — only `[2]` → contrib 2. The two `1`s split the rest via strictness rules.

---

## B10. Explain remove duplicate letters on `"bcabc"`.

**Answer:** Last indices: a:3,b:4,c:5? `"bcabc"` → b:3,c:4,a:2 wait: indices b0 c1 a2 b3 c4. last={b:3,c:4,a:2}.  
Build increasing unique: b→bc→ a pops c (c appears later), pops b (b appears later) → a → ab → abc. Result `"abc"`.

---

## B11. Why dual deques for max−min constraint, not one?

**Answer:** Need both max and min of current window in O(1). One deque only tracks one extremum.

---

## B12. Fenwick interview 60-second pitch.

**Answer:** "Tree of partial sums keyed by lowest set bit. Point add updates O(log n) indices; prefix sum folds O(log n) blocks; range = prefix difference. I keep a mirror array for set-updates via deltas. Prefer this over segtree when only sums matter."

---

# SECTION I: FULL PROBLEM SET (WITH COMPLETE ANSWERS)

---

## C11. Implement Trie — with delete (optional stretch)

**Answer:** Insert/search/startsWith as standard. Delete: clear `is_end`, prune upward while node has no children and not `is_end`. See Advanced lesson Part 7A.

---

## C12. MapSum

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

## C13. Sum of Subarray Ranges — full code

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

## C14. Largest Rectangle in Histogram — full code + trace `[2,4]`

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

## C15. Maximal Rectangle

**Answer:** Row-by-row heights + `largestRectangleArea`. See lesson. O(R·C).

---

## C16. Remove Duplicate Letters

**Answer:** Code in lesson Part 8F. Test `"cbacdcbc"` → `"acdb"`.

---

## C17. Asteroid Collision — `"10,2,-5"` 

**Answer:** `[10]` — 2 and -5 collide (2 dies), 10 and -5 collide (-5 dies).

```python
# full code in Advanced lesson P9
```

---

## C18. Find 132 Pattern

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

## C19. Online Stock Span — implement + stream `[31,41,48,59,79]`

**Answer:** All increasing → spans `1,2,3,4,5` (each collapses all previous).

---

## C20. Longest subarray max−min ≤ 0

**Answer:** Only equal elements windows. Dual deques still work; limit 0 means max==min.

---

## C21. [Exposure] Fenwick — count of range sum queries after updates

**Prompt:** Start `[1,2,3,4]`; `sum(0,3)`; `add(2,+5)`; `sum(2,3)`.

**Answer:** Initial sum=10. After A[2]=8, sum(2,3)=8+4=12. Fenwick add(2,5); range_sum uses prefixes.

---

## C22. Word Search II — return order

**Answer:** Any order OK unless specified. Dedupe with `nxt.word = None`.

---

## C23. Magic Dictionary (one edit)

**Answer:** Trie DFS with `modified` budget 1, or brute compare all words length-equal with diff==1. See lesson P6.

---

## C24. Max Chunks II (general) — explain stack of maxima

**Answer:** Maintain increasing stack of chunk max values; when a new smaller value arrives, merge chunks by popping until maxes consistent; push back the max of merged region. `len(stack)` = chunks.

---

# SECTION J: TRICK BANK (EXPANDED)

---

## D6. True/False: For sum of subarray mins, sorting the array first helps.

**Answer:** False — contiguous subarrays depend on positions; sorting destroys structure.

---

## D7. True/False: `search` can be used to implement autocomplete listing.

**Answer:** False — search is boolean exact. Need prefix node + subtree enumeration.

---

## D8. You pop from mono stack when `heights[stack[-1]] > h` (histogram). What if equal heights?

**Answer:** Using `>` (not `>=`) can leave equal bars; width accounting still works with care. Many solutions use `>=` when popping to treat equals as boundaries differently — know your formula. Sentinels simplify.

---

## D9. Interviewer: "Optimize Word Search I (single word) with a trie?"

**Answer:** Overkill for one word — plain DFS/backtracking on board is enough. Trie shines for **many** words (Word Search II).

---

## D10. Can contribution technique compute sum of subarray GCDs easily?

**Answer:** Not with the same simple prev/next smaller — GCD structure differs (need sparse table / segtree / other). Don't force mono stack.

---

## D11. StockSpanner: is worst-case single `next` O(n)?

**Answer:** Yes one call can pop many; amortized O(1) across n calls. Say amortized in interviews.

---

## D12. Fenwick for "subarray sum equals k" on static array?

**Answer:** Unnecessary — prefix+hash is the right tool. Fenwick if array mutates between queries.

---

# SECTION K: CUMULATIVE INTEGRATION (M4–M10)

---

## K1. Daily temperatures + stock span: write both signatures and one shared insight.

**Answer:** Shared: monotonic decreasing stack of unresolved indices/prices. Temps: offline distances. Span: online merged spans.

---

## K2. Sliding window max (M4) → longest max−min ≤ limit (M10). What was added?

**Answer:** Second deque for min + variable shrink condition on `max-min`.

---

## K3. Histogram (M4) → maximal rectangle (M10). What was added?

**Answer:** Reduction layer: per-row heights of consecutive 1s.

---

## K4. Hash set dictionary vs trie replace-words — when hash wins?

**Answer:** Tiny root set, short words, want less code — check prefixes against set. Large shared prefixes / interview asks for trie → trie.

---

## K5. Prefix+hash subarray sum vs Fenwick — classify three prompts.

| Prompt | Tool |
|---|---|
| Count subarrays sum=k, array fixed | Prefix+hash |
| Mutable array, sum ranges | Fenwick |
| Max in sliding window | Mono deque |

---

# SECTION L: BLINDED MINI TIMED SET (ANSWERS)

Do in 40 min, then check.

### L1. Implement startsWith only (no search) — still need is_end?  
**Answer:** No for startsWith. Yes if you also need search.

### L2. Remove k digits `"10"`, k=2 →  
**Answer:** `"0"` (remove both; empty → `"0"`).

### L3. Sum subarray mins `[1]` →  
**Answer:** `1`.

### L4. Window max nums=`[1,3,-1,-3,5,3,6,7]`, k=3 →  
**Answer:** `[3,3,-1,5,5,6,7]` (classic LC 239).

### L5. Trie after insert `"a"`, search `""` →  
**Answer:** Usually False unless empty inserted / root.is_end True.

### L6. Exposure: static 1e5 range sums — structure?  
**Answer:** Prefix sums.

---

# SECTION M: SCORING RUBRIC FOR THIS GRILL

| Band | Meaning |
|---|---|
| ≥90% A + solid B + ≥10/14 C | Strong — proceed to timed verify |
| 75–89% | Shaky topics → ledger downgrade + drill |
| <75% | Re-teach weak half (trie vs mono) before timed |

**Fenwick subsection:** Score separately as exposure — missing segtree code ≠ fail Module 10.

---

*End of Module 10 Retention (expanded).*

---

# SECTION O: ADDITIONAL FULL-ANSWER PROBLEMS (C25–C36)

---

## C25. Implement Trie — array[26] children variant

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

## C26. WordDictionary — full code

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

## C27. Replace Words — hash-prefix alternate + trie compare

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

## C28. Sum of Subarray Minimums — full code again with MOD

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

## C29. Remove K Digits — `"10001"`, k=4

**Answer:** Stack builds; pops to remove; strip zeros → `"0"`.

---

## C30. StockSpanner stream `[71,71,71]`

**Answer:** Spans `1,2,3` (≤ allows equals to collapse).

---

## C31. Longest subarray max−min ≤ limit — `[10,1,2,4,7]`, limit=5

**Answer:** Window `[1,2,4,7]` has max−min=6>5; best length 3 e.g. `[2,4,7]`? 7-2=5 OK length 3; `[1,2,4]` length 3. Answer 3? Actually `[1,2,4,7]` invalid; check `[2,4,7]`=5 OK. LC answer often 3.

Full code dual deque from lesson.

---

## C32. Max Chunks `[1,0,2,3,4]`

**Answer:** 4 — see lesson trace.

---

## C33. Histogram `[2,1,5,6,2,3]` → 10

**Answer:** Mono increasing + sentinels; area 10.

---

## C34. Asteroids `[8,-8]`

**Answer:** `[]` — equal size both explode.

---

## C35. 132 pattern `[1,2,3,4]` / `[3,1,4,2]`

**Answer:** False / True (`1,4,2`).

---

## C36. Fenwick NumArray — implement class

**Answer:** See exposure lesson LC307; delta update; range_sum via prefix diff.

---

# SECTION P: ORAL TEACH-BACK RUBRIC (M10)

Score yourself 1–5 on each:

| Topic | 1–5 |
|---|---|
| Trie is_end vs startsWith | |
| Wildcard DFS | |
| Word Search II prune | |
| Contribution + ties | |
| Remove k digits greedy | |
| Stock span amortized | |
| Dual deque window | |
| Fenwick when/why (exposure) | |

Average ≥4 before timed verify.

---

# SECTION Q: ERROR-TAG PRACTICE

For each wrong answer in this grill, force a tag:

| Miss | Tag | Fix |
|---|---|---|
| Forgot is_end | knowledge-gap | Re-draw trie |
| Off-by-one window | careless-slip | Trace left/right |
| Used segtree for window max | knowledge-gap | Mono deque drill |
| Ran out of time on SOASM | time-pressure | Span drills first |
| Misread shortest vs longest root | misread | Restate ritual |

---

*End of Module 10 Retention (expanded).*
