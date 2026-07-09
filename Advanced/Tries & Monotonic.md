# TRIES & MONOTONIC STRUCTURES — THE COMPLETE LESSON

**Module:** 10 (Advanced Structures — interview-weighted)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisites:** Hashing, Recursion/backtracking skeleton, Stacks & Queues (Module 4 monotonic **intro**), Sliding Window (Modules 1 & 6)  
**Relationship to Module 4:** Module 4 (`Stacks & Queues/Stacks & Queues.md`) taught next-greater, daily temps, histogram, sliding-window max. This lesson is the **deep dive**: more problem families, contribution technique, online queries, digit/greedy hybrids, and interview judgment. Ownership map: `QA/Monotonic Ownership.md`.

---

# PART 1: TRIES — PREFIX TREES

## Why Tries Exist

A **trie** (prefix tree) stores strings so that **shared prefixes share a path**.

| Need | Hash set of words | Sorted list + bisect | Trie |
|---|---|---|---|
| Exact word lookup | O(L) average | O(L log n) | O(L) |
| "Any word with this prefix?" | Scan all → O(total chars) | Bisect range → O(L log n + output) | **O(L)** walk |
| Autocomplete top-k | Scan all | Range scan | Walk prefix node → DFS/BFS subtree |
| Replace root word with shortest root | Hash of roots + scan prefixes | Similar | Walk trie while reading sentence |

**L** = length of the query string. **n** = number of stored words.

**The rule:** If the problem is about **prefixes**, **dictionary of words**, **autocomplete**, or **shortest root replacement**, a trie is the natural structure. If you only need exact membership, a `set` is simpler and usually enough.

### Real-World Intuition

Think of a phone contacts search:

- Typing `jo` should not re-scan every contact from scratch as a bag of strings
- Contacts sharing `jo` (`John`, `Jordan`, `Joanna`) live under the same path `j → o`
- The node after `o` is the **prefix node** — everything below it is a candidate completion

A trie is that contact index: one edge per character, one path per word, shared prefixes shared for free.

---

## 1A: Structure

Each node typically holds:

```
children: dict char → TrieNode   (or array[26] for lowercase a–z)
is_end: bool                     (a word ends here)
# optional for problems:
# count: how many words pass through / end here
# word: the full word string (for easy recovery)
```

```
Insert: "cat", "car", "dog"

        root
       /    \
      c      d
      |      |
      a      o
     / \     |
    t*  r*   g*
```

`*` marks `is_end = True`.

**Critical:** `is_end` is required. Without it, inserting `"app"` then searching `"ap"` would falsely succeed if you only check "path exists."

### Array[26] vs dict

| Choice | When |
|---|---|
| `children = [None]*26` | Only lowercase English letters; slightly faster / clearer interview code |
| `dict` | Unicode, mixed case, or "any printable char" |

**Interview default for LC:** `dict` is fine and readable. Mention array[26] if alphabet is fixed.

---

## 1B: Core Operations Framework

### Insert

```
node = root
for each char c in word:
    if c not in node.children: create child
    node = node.children[c]
node.is_end = True
```

**Time:** O(L) · **Space:** O(L) new nodes in worst case (no shared prefix)

### Search (exact word)

```
node = root
for each char c in word:
    if c not in node.children: return False
    node = node.children[c]
return node.is_end
```

### StartsWith (prefix)

Same as search, but return `True` if the path exists — **do not** require `is_end`.

### Python Skeleton

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str):
        node = self.root
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
```

**Interview talk:** "I'll build a trie of characters. Insert and search are O(length). Prefix queries walk to the prefix node in O(length), then I can explore the subtree if I need completions."

---

## 1C: Word Dictionary (Add Word / Search with `.` wildcards)

**Problem smell:** `addWord(word)` and `search(word)` where `.` matches any letter.

### Framework

- Insert is a normal trie insert
- Search becomes **DFS/backtracking on the trie**:
  - Normal char → follow that edge
  - `.` → try **every** child edge
  - At end of pattern → need `is_end`

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(i, node):
            if i == len(word):
                return node.is_end
            c = word[i]
            if c == '.':
                return any(dfs(i + 1, child) for child in node.children.values())
            if c not in node.children:
                return False
            return dfs(i + 1, node.children[c])
        return dfs(0, self.root)
```

### Complexity

- Insert: O(L)
- Search worst case: O(26^L) if pattern is all dots (branching factor × length). Average much better with sparse tries.
- **Interview honesty:** State the worst case. Mention pruning when alphabet is small and dictionary is sparse.

### Trap

Do **not** convert `.` to "skip one level blindly." You must branch over children. Also: empty children + `.` → False.

---

## 1D: Replace Words (Shortest Root)

**Problem:** Dictionary of roots. For each word in a sentence, replace with the **shortest root** that is a prefix. If none, keep the word.

### Framework

1. Insert all roots into a trie
2. For each word, walk the trie character by character
3. As soon as you hit `is_end`, that path is a root — return it (shortest because you stop at first end)
4. If walk fails before any `is_end`, keep original word

```python
def replaceWords(dictionary, sentence):
    root = TrieNode()
    for w in dictionary:
        node = root
        for c in w:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def shortest_root(word):
        node = root
        for i, c in enumerate(word):
            if c not in node.children:
                return word
            node = node.children[c]
            if node.is_end:
                return word[: i + 1]
        return word

    return " ".join(shortest_root(w) for w in sentence.split())
```

**Why trie beats hashing every prefix:** Hashing every prefix of every word works (`for i in range(1,len+1): if word[:i] in roots`), but trie walks once without slicing. Same asymptotics often; trie is the intended structure when they say "implement a prefix tree."

**Trap:** Prefer **shortest** root — stop at first `is_end`, don't continue to a longer root.

---

## 1E: Autocomplete Intuition (Design / Follow-ups)

Interviewers rarely ask full production autocomplete. They ask the **mental model**:

1. Insert corpus into trie (optionally store `freq` / `hot` on end nodes)
2. On query prefix `p`, walk to prefix node — O(|p|)
3. DFS/BFS the subtree to collect completions
4. Rank by frequency / lexicographic / recency

### What to say in a design interview

- **Hot path:** prefix walk must be fast → trie or sorted array + binary search
- **Ranking:** store top-k at each node (space↑, query↓) vs compute on the fly (space↓, query↑)
- **Updates:** trie handles online inserts; sorted array needs rebuild or fenwick/seg of ranks (overkill for most screens)

**Phase A depth:** Know insert/search/prefix/wildcard/replace-words cold. Autocomplete = explain the walk + subtree collect. Full ranking systems → System Design (Phase C).

---

## 1F: Trie vs Hash Set — Decision Table

| Situation | Prefer |
|---|---|
| Exact membership only | `set` |
| Prefix / shortest root / wildcard `.` | Trie |
| Many shared prefixes, memory matters | Trie (shares nodes) |
| One-off "does any word start with…" on tiny n | Scan / set of prefixes |
| Need sorted order of all words | Sorted list or trie inorder DFS |

---

## 1G: Worked Problem — Implement Trie (LC 208)

Already covered by the skeleton. Trace:

```
insert "apple"
search "apple" → True
search "app" → False   # path exists, is_end False
startsWith "app" → True
insert "app"
search "app" → True
```

**Edge cases:** empty string (define: usually allowed as `is_end` on root — confirm constraints), single char, duplicate inserts (idempotent).

---

## 1H: Worked Problem — Word Search II (Board + Trie) [Hard]

**Smell:** Find all dictionary words on a grid via adjacent cells (no reuse of cell in one word).

### Framework

1. Insert all words into a trie
2. DFS from every cell, walking **trie and board together**
3. When `is_end`, record word; optionally erase `is_end` / prune leaf to avoid duplicates and speed up
4. Backtrack board mark

```python
def findWords(board, words):
    root = TrieNode()
    for w in words:
        node = root
        for c in w:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
        node.word = w  # store full word at end

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        nxt = node.children[ch]
        if getattr(nxt, "word", None):
            found.append(nxt.word)
            nxt.word = None  # dedupe
        board[r][c] = "#"
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, nxt)
        board[r][c] = ch
        # optional prune: if not nxt.children: del node.children[ch]

    for i in range(rows):
        for j in range(cols):
            dfs(i, j, root)
    return found
```

**Why trie:** Prunes dead prefixes early — if board path isn't a prefix of any word, stop. Hash-set of words alone still explores many dead paths unless you also check prefixes (which reinvents a trie).

**Complexity talk:** O(R·C·4^L) worst case with pruning; trie reduces constants heavily. Space O(total dictionary characters).

---

# PART 2: MONOTONIC STACK / QUEUE — DEEP DIVE

## Recap From Module 4 (Do Not Skip Mentally)

| Pattern | Structure | Invariant |
|---|---|---|
| Next greater to right | Decreasing stack of indices | Tops are candidates waiting for a greater |
| Previous smaller | Increasing stack | Tops waiting for a smaller |
| Histogram largest rectangle | Increasing stack | Previous/next smaller → width |
| Sliding window maximum | Decreasing deque | Front = max of window |

**O(n) law:** Each index is pushed at most once and popped at most once → ≤ 2n stack ops.

This deep dive adds: **contribution technique**, **chunking**, **digit greedy**, **online span**, and **advanced window extrema**.

---

## 2A: Contribution Technique — Sum of Subarray Minimums

**Problem (LC 907):** Given `arr`, compute sum of `min(subarray)` over **all** contiguous subarrays. Mod 10⁹+7.

### Naive

O(n²) or O(n³) — enumerate subarrays, find min. Too slow for n ~ 3·10⁴+.

### Key Insight

For each index `i`, count how many subarrays have `arr[i]` as their **minimum**. Then contribute `arr[i] * count`.

For `arr[i]` to be the min of subarray `arr[L..R]`:
- `L` must be in `(prev_smaller[i], i]`
- `R` must be in `[i, next_smaller[i])`

If ties: use **strict** on one side and **non-strict** on the other so each subarray's min is attributed to exactly one index (avoid double-counting equal mins).

```
left[i]  = distance to previous strictly smaller (or -1 sentinel)
right[i] = distance to next smaller-or-equal (or n sentinel)
# common convention — verify against your strictness choice

count = left_span * right_span
contrib = arr[i] * count
```

### Framework

1. Monotonic **increasing** stack → previous smaller (strict)
2. Monotonic **increasing** stack → next smaller (non-strict) [or swap strictness]
3. Sum contributions

```python
def sumSubarrayMins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    left = [0] * n   # # of elements strictly greater to the left until smaller
    right = [0] * n
    stack = []

    # previous smaller (strict): distance
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:  # pop greater/equal → strict smaller remains
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack = []
    # next smaller (non-strict): distance
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
```

### Trace

```
arr = [3, 1, 2, 4]

Subarrays and mins:
[3]=3, [3,1]=1, [3,1,2]=1, [3,1,2,4]=1
[1]=1, [1,2]=1, [1,2,4]=1
[2]=2, [2,4]=2
[4]=4
Sum = 3+1+1+1 +1+1+1 +2+2 +4 = 17
```

For `i=1` (value 1): it is min of many subarrays — large contribution. Matches intuition.

**Interview talk:** "Instead of enumerating subarrays, I count how many subarrays have each element as the unique minimum using previous/next smaller from a monotonic stack, then sum value × count."

### Related Family

- Sum of subarray **maximums** — same idea, flip inequalities
- Sum of subarray ranges (max − min) — sum of maxes − sum of mins

---

## 2B: Max Chunks To Make Sorted

**Problem (LC 769 / 768):** Split array into max number of chunks so sorting each chunk individually sorts the whole array.

### Version 1 — Permutation of `0..n-1` (LC 769)

**Insight:** A chunk ending at `i` is valid iff `max(arr[0..i]) == i` (everything that belongs in `0..i` is already inside).

```python
def maxChunksToSorted(arr):
    chunks = cur_max = 0
    for i, x in enumerate(arr):
        cur_max = max(cur_max, x)
        if cur_max == i:
            chunks += 1
    return chunks
```

No explicit stack — but the **invariant** is monotonic in spirit: the running max must "catch up" to the index.

### Version 2 — General duplicates (LC 768)

Harder. One approach: monotonic stack of **chunk maxes**.

```python
def maxChunksToSorted(arr):
    stack = []  # increasing stack of max-values of chunks
    for x in arr:
        if not stack or x >= stack[-1]:
            stack.append(x)
        else:
            mx = stack.pop()
            while stack and stack[-1] > x:
                stack.pop()
            stack.append(mx)
    return len(stack)
```

**Intuition:** If a new value is smaller than previous chunk max, those chunks must merge until the maxes are consistent with sorted order.

**Interview talk:** "Chunks are valid when no future smaller value needs to move left past a larger left-side value. I maintain candidate chunk boundaries with a monotonic stack of maxima."

---

## 2C: Remove K Digits (Monotonic + Greedy)

**Problem (LC 402):** Given number string `num` and integer `k`, remove `k` digits to form the **smallest possible** number.

### Framework

Build an **increasing** digit stack (monotonic non-decreasing):

```
For each digit d:
  while k > 0 and stack and stack[-1] > d:
    pop stack; k -= 1
  push d
If k still > 0: pop k digits from the end
Strip leading zeros
```

**Why:** To minimize the number, you want **leftmost digits as small as possible**. A peak (larger digit before smaller) should be removed preferentially.

```python
def removeKdigits(num: str, k: int) -> str:
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[:-k]
    ans = "".join(stack).lstrip("0")
    return ans if ans else "0"
```

### Trace

```
num = "1432219", k = 3

1 → [1]
4 → [1,4]
3 → 4>3, pop 4, k=2 → [1,3]
2 → 3>2, pop 3, k=1 → [1,2]
2 → [1,2,2]
1 → 2>1, pop 2, k=0 → [1,2,1]
9 → [1,2,1,9]
Result "1219"
```

**Traps:**
- Leading zeros after strip → `"0"` if empty
- `k` remaining after scan → remove from the **end** (largest place values already optimal on the left)
- Do not confuse with "largest number after removal" (flip `>` to `<`)

**Complexity:** O(n) time, O(n) space.

---

## 2D: Online Stock Span

**Problem (LC 901):** Design a class. On each day, given price, return **span** = max consecutive days ending today with price ≤ today's price (including today).

### Naive

Walk backward until a greater price — O(n) per query → O(n²) total.

### Monotonic Stack

Keep decreasing stack of `(price, span)` or `(price, index)`:

```python
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

**Why O(1) amortized:** Each day's pair is pushed once and popped once across the whole stream.

**Interview talk:** "This is next-greater in reverse: I collapse previous days that can't beat today's price, accumulating their spans."

### Connection

Same family as "daily temperatures" / next greater — but **online** (you don't have the full array). Stack stores history of unanswered candidates.

---

## 2E: Sliding Window Extrema — Advanced

### Baseline (Module 4): Window Maximum

Decreasing deque of indices; front = max.

### Window Minimum

Increasing deque; front = min. Same expire-from-front rule.

### Both Max and Min (e.g., longest subarray with `max − min ≤ limit`)

**LC 1438:** Longest continuous subarray where abs difference between any two ≤ limit ⇔ `max − min ≤ limit`.

```python
from collections import deque

def longestSubarray(nums, limit):
    maxq, minq = deque(), deque()  # decreasing / increasing indices
    left = 0
    best = 0
    for right, x in enumerate(nums):
        while maxq and nums[maxq[-1]] < x:
            maxq.pop()
        maxq.append(right)
        while minq and nums[minq[-1]] > x:
            minq.pop()
        minq.append(right)
        while nums[maxq[0]] - nums[minq[0]] > limit:
            left += 1
            if maxq[0] < left:
                maxq.popleft()
            if minq[0] < left:
                minq.popleft()
        best = max(best, right - left + 1)
    return best
```

**Pattern fusion:** Variable sliding window **+** two monotonic deques for O(1) max/min.

### Constrained Subsequence Sum (Hard preview of DP + monoqueue)

**LC 1425:** `dp[i] = nums[i] + max(0, max(dp[j]) for j in [i-k, i-1])`.

Maintain a **decreasing deque of dp values** in the last k indices — classic DP + monotonic queue. Mention in interviews; full DP ownership is Modules 8–9.

---

## 2F: Max Chunk / Asteroid / Other Mono Hybrids (Quick Map)

| Problem | Structure | One-liner |
|---|---|---|
| Asteroid collision | Stack | While top > 0 and incoming < 0, resolve collision |
| Remove duplicate letters (smallest) | Mono stack + remaining counts + in-stack set | Greedy increasing + "can pop if char appears later" |
| Shortest unsorted continuous subarray | Mono or two-pass min/max | Find disorder bounds |
| Largest rectangle / maximal rectangle | Mono stack on heights | Histogram per row |

---

# PART 3: CHEAT SHEETS

## Trie Cheat Sheet

| Op | Time | Note |
|---|---|---|
| Insert word | O(L) | Share prefixes |
| Search word | O(L) | Check `is_end` |
| Prefix exists | O(L) | No `is_end` needed |
| Wildcard `.` | O(b^L) worst | DFS over children |
| Replace root | O(L) per word | Stop at first `is_end` |

**Node fields:** `children`, `is_end`, optional `word` / `count`.

**Smell words:** prefix, dictionary, autocomplete, root replacement, word search on board.

## Monotonic Cheat Sheet

| Goal | Stack/Deque order | Scan |
|---|---|---|
| Next greater right | Decreasing | L→R; pop < current |
| Next smaller right | Increasing | L→R; pop > current |
| Prev greater/smaller | Same, scan R→L or interpret pops as prev |
| Subarray min contribution | Prev + next smaller spans | Two mono passes |
| Remove k digits (smallest) | Non-decreasing digits | Pop larger left peaks |
| Stock span | Decreasing prices | Collapse ≤ today |
| Window max | Decreasing deque | Expire left; pop back dominated |
| Window min | Increasing deque | Same skeleton |
| Max−min window constraint | Both deques + two pointers | Shrink while max−min > limit |

**O(n) mantra:** push once, pop once.

## Interview Decision Tree

```
Prefix / dictionary of strings? → Trie (or set if exact only)
Next greater / span / histogram family? → Monotonic stack
Window max/min / max-min constraint? → Monotonic deque (+ window)
Minimize number by deleting digits? → Monotonic increasing digit stack
Online stream needing previous greater? → Stock-span style stack
Need segment/fenwick range structure? → See exposure lesson (usually overkill for screens)
```

---

# PART 4: WORKED PROBLEMS (MIXED)

## P1: Sum of Subarray Minimums — Edge Cases

- All equal: each element is min of carefully partitioned counts (strictness matters)
- Strictly increasing: each element is min only of subarrays starting at itself toward the right appropriately
- Single element: answer = that element

## P2: Remove K Digits — `"10200"`, k=1

```
1 → [1]
0 → pop 1 (1>0), k=0 → [0]
2 → [0,2]
0 → [0,2,0]
0 → [0,2,0,0]
lstrip → "200"
```

## P3: Stock Spanner Stream

```
prices: 100, 80, 60, 70, 60, 75, 85
spans:    1,  1,  1,  2,  1,  4,  6
```

At 75: collapses 60,70,60,80? Wait — stack holds after 60 (after 70): carefully accumulate — standard LC example spans are `1,1,1,2,1,4,6`.

## P4: Trie Replace Words

```
dictionary = ["cat","bat","rat"]
sentence = "the cattle was rattled by the battery"
→ "the cat was rat by the bat"
```

## P5: Longest Subarray max−min ≤ limit

```
nums = [8,2,4,7], limit = 4
Window grows; when 8 and 2 both in window, 8-2=6>4 → shrink left
Answer 2 (e.g. [2,4] or [4,7])
```

---

# PART 5: TRAPS & INTERVIEW PHRASES

## Traps

1. Trie search without `is_end` → false positives on prefixes
2. Replace words: continuing past first root → not shortest
3. Contribution double-count on equal elements → fix strictness asymmetry
4. Remove k digits: forgetting leading zeros / empty → `"0"`
5. Monotonic deque storing values not indices → can't expire by window left correctly
6. Using `list.pop(0)` for queue/deque needs → O(n)
7. Claiming O(n) mono stack but scanning stack for answers → broken

## Phrases That Score

- "Each index enters and leaves the stack at most once, so O(n)."
- "I'll attribute each subarray's minimum to exactly one index via previous/next smaller."
- "Prefix queries walk to a node in O(L); completions are a subtree DFS."
- "For online spans I keep a monotonic stack of unresolved prices."

---

# PART 6: SCOPE BOUNDARIES

| In scope (Module 10) | Deferred |
|---|---|
| Trie insert/search/prefix/wildcard/replace/board+trie | Full autocomplete product design (Phase C) |
| Mono deep: contribution, chunks, remove k digits, stock span, dual deque windows | Segment/Fenwick mastery (exposure lesson only) |
| Interview judgment trie vs hash | Suffix arrays / Aho-Corasick (CP / Phase B) |

**Status note:** This file = concept delivery. Raise to `complete` only after Module 10 retention + timed verify + ledger entries per Handoff Doc.

---

# PART 7: TRIE — FULL TRACES & FAILURE MODES

## 7A: Insert Trace — Shared Prefixes

```
Operations: insert("app"), insert("apple"), insert("apex")

After "app":
  root
   └─ a
       └─ p
           └─ p*

After "apple":
  root
   └─ a
       └─ p
           └─ p*          ← still is_end (word "app")
               └─ l
                   └─ e*

After "apex":
  root
   └─ a
       └─ p
          ├─ p*
          │   └─ l
          │       └─ e*
          └─ e
              └─ x*
```

**What to say:** "Shared prefix `ap` is one path. Branching happens at the first differing character. Ending a shorter word mid-path only flips `is_end` — it does not block longer words."

### Failure mode: forgetting `is_end` on the shorter word

If you insert `"apple"` then `"app"` but forget to set `is_end` on the second `p`, `search("app")` returns False forever. **Symptom in interviews:** startsWith works, search fails for prefixes that are also words.

### Failure mode: deleting a word incorrectly

Naive "delete path" can destroy `"apple"` when deleting `"app"`. Correct delete:
1. Walk path collecting nodes
2. Clear `is_end` on the end node
3. Only remove nodes with **no children and not is_end**, walking upward

```python
def delete(self, word: str) -> bool:
    def _delete(node, word, i):
        if i == len(word):
            if not node.is_end:
                return False  # word not present
            node.is_end = False
            return len(node.children) == 0  # tip parent: may prune
        c = word[i]
        if c not in node.children:
            return False
        should_prune = _delete(node.children[c], word, i + 1)
        if should_prune:
            del node.children[c]
        return (not node.is_end) and len(node.children) == 0
    return _delete(self.root, word, 0) is not None
```

**Interview depth:** Many screens never ask delete. Knowing the prune rule shows you understand shared structure.

---

## 7B: Search / StartsWith — Side-by-Side Trace

```
Trie contains: "app", "apple"

Query          Walk result              is_end?    Answer
search("app")  lands on 2nd p           True       True
search("appl") lands on l               False      False
search("ap")   lands on 1st p           False      False
startsWith("ap") lands on 1st p         n/a        True
startsWith("apple") lands on e          n/a        True
startsWith("apr") missing r edge        n/a        False
search("")     root                     root.is_end (usually False)
```

**Constraint check:** Confirm whether empty string is a valid word in the problem.

---

## 7C: Word Dictionary (Wildcards) — Full Trace

```
addWord("bad"), addWord("dad"), addWord("mad")
search("pad") → False
search("bad") → True
search(".ad") → True
search("b..") → True
```

### Trace `search(".ad")`

```
dfs(i=0, node=root), pattern[0]='.'
  try child 'b': dfs(1, b-node), pattern[1]='a'
    'a' in children → dfs(2, ba-node), pattern[2]='d'
      'd' in children → dfs(3, bad-node)
        i==len → return is_end True  ✓
  (short-circuit any() — done)
```

### Trace `search("b..")`

```
dfs(0): 'b' → b-node
dfs(1): '.' → try 'a' only child → ba-node
dfs(2): '.' → try 'd' → bad-node
dfs(3): i==3 → is_end True ✓
```

### Failure modes

| Bug | Symptom |
|---|---|
| Treat `.` as literal char | Never matches wildcards |
| On `.`, skip one level without iterating children | Wrong structure / crash |
| Return True when path exists but `is_end` False | `"ba."` matching prefix of longer word incorrectly if end missing |
| No base case `i == len(word)` | Infinite or wrong |

### Complexity honesty (say this)

"If the pattern is all dots, I branch over every child at every level — O(Σ branching^L) worst case. With a sparse dictionary it's much faster. If the interviewer cares about worst-case guarantees, I'd discuss limiting alphabet size or using Aho-Corasick for multi-pattern (Phase B)."

---

## 7D: Replace Words — Full Worked Solution

**Problem:** Replace each word in a sentence with the shortest dictionary root that is a prefix.

### Interview communication script

1. "I'll put all roots in a trie so each word walks once."
2. "While walking, the first `is_end` I hit is the shortest root."
3. "If the walk breaks before any end, I keep the original word."
4. "Time O(total characters in dictionary + sentence). Space O(total root characters)."

### Full code

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def replaceWords(dictionary, sentence):
    root = TrieNode()
    for w in dictionary:
        node = root
        for c in w:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def replace_one(word):
        node = root
        for i, c in enumerate(word):
            if c not in node.children:
                return word
            node = node.children[c]
            if node.is_end:
                return word[: i + 1]
        return word

    return " ".join(replace_one(w) for w in sentence.split())
```

### Trace

```
dictionary = ["a", "aa", "aaa"]  # shortest root "a" always wins if present
word = "aaaa"
Walk: a (is_end!) → return "a" immediately
Never continue to longer roots.
```

### Alternate without trie (acceptable if clear)

```python
roots = set(dictionary)
def replace_one(word):
    for i in range(1, len(word) + 1):
        if word[:i] in roots:
            return word[:i]
    return word
```

**Tradeoff talk:** "Set of roots with prefix checks is O(L²) string slicing cost per word in naive Python; trie is cleaner O(L) and shows prefix-structure thinking."

---

## 7E: Word Search II — FULL SOLUTION (Hard)

**Problem:** `m x n` board of letters + list of words. Return all words that can be formed by adjacent (4-dir) cells without reusing a cell in one word.

### Why this is the flagship trie problem

- Dictionary can be large → trie prunes impossible prefixes
- Board DFS alone with a set still explores dead prefixes unless you check "is this a prefix of something?" — which is what a trie encodes

### Full interview-grade code

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # store full word at terminal

def findWords(board, words):
    root = TrieNode()
    for w in words:
        node = root
        for c in w:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.word = w

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        nxt = node.children[ch]
        if nxt.word is not None:
            found.append(nxt.word)
            nxt.word = None  # dedupe; allow other words through same node

        board[r][c] = "#"  # visit mark
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, nxt)
        board[r][c] = ch  # backtrack

        # optional prune: empty leaf
        if not nxt.children:
            del node.children[ch]

    for i in range(rows):
        for j in range(cols):
            dfs(i, j, root)
    return found
```

### Full trace (small board)

```
board = [
  ["o","a","a","n"],
  ["e","t","a","e"],
  ["i","h","k","r"],
  ["i","f","l","v"]
]
words = ["oath","pea","eat","rain"]

Trie paths: o-a-t-h*, p-e-a*, e-a-t*, r-a-i-n*

Start (0,0)='o' → follow o → a (0,1) → t (1,1) → h (2,1) → word "oath" found
Start cells that begin 'e': (1,0) and (1,3)
  From (1,3)='e' → a (1,2) → t (1,1) → "eat"
"pea","rain" never form on this board → not returned
```

### Complexity communication

- Time: O(R·C·4^L) worst case with L = max word length; trie pruning + early delete of found words reduces constants dramatically
- Space: O(total dictionary characters) for trie + O(L) recursion

### Failure modes

| Bug | Fix |
|---|---|
| Forget to unmark board | Corrupts later searches |
| Don't null out `word` after find | Duplicates in output |
| Use set of words only, check `path in words` | Misses prefix pruning; TLE risk |
| 8-direction adjacency | Spec is usually 4-dir — confirm |
| Reuse cell | Must mark/unmark |

### Follow-ups interviewers ask

1. "What if the board is huge and dictionary tiny?" → Maybe reverse: DFS words against board (usually worse); or still trie
2. "What if we need counts of how many times each word appears?" → Don't null `word`; increment counter; still mark board per path
3. "Memory?" → array[26] children if lowercase only

---

## 7F: Autocomplete — Design Intuition (Interview Script)

**Prompt:** "Design autocomplete that returns top 3 hot searches for a prefix."

### Layered answer (Phase A depth)

1. **Index:** Trie of queries; each terminal stores `freq`
2. **Query:** Walk to prefix node O(|p|); DFS/BFS subtree collecting (word, freq); sort top 3
3. **Optimize:** Cache top-3 at each node; on insert/update, bubble hot lists up the path
4. **Tradeoff:** Cached top-k → fast query, more write cost + memory
5. **Out of scope for coding screen:** distributed sharding, typos (edit distance), personalization

**Phrase:** "For a coding interview I'd implement trie + subtree collect. For a design interview I'd discuss caching top-k per node and write amplification."

---

## 7G: Map Sum Pairs / Prefix Sum of Values (Trie + counts)

**Problem:** `insert(key, val)` (overwrite if key exists); `sum(prefix)` = sum of values of all keys with that prefix.

```python
class MapSum:
    def __init__(self):
        self.root = {}  # children dict; node also has 'val' and 'sum' optional
        self.vals = {}  # key -> last value for overwrite delta

    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)
        self.vals[key] = val
        node = self.root
        for c in key:
            node = node.setdefault(c, {"sum": 0, "children": {}})
            # simpler structure below in full form
        # ... see full implementation pattern: add delta along path to path_sum

class MapSumClear:
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
            node.path_sum = getattr(node, "path_sum", 0) + delta
        node.is_end = True

    def sum(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return 0
            node = node.children[c]
        return getattr(node, "path_sum", 0)
```

**Idea:** Each node stores sum of values of all words passing through it. Overwrite uses **delta**.

---

# PART 8: MONOTONIC — CONTRIBUTION FAMILY (DEEP)

## 8A: Sum of Subarray Minimums — Full Trace

```
arr = [3, 1, 2, 4]
MOD not needed for tiny example

Previous smaller (strict) distances left[i]:
  i=0 (3): no smaller → left=1
  i=1 (1): 3 is greater → left=2
  i=2 (2): 1 is smaller at i=1 → left=1
  i=3 (4): 2 is smaller at i=2 → left=1

Next smaller (non-strict / as per chosen convention) right[i]:
  Using lesson code (next with > pop):
  i=3 (4): right=1
  i=2 (2): right=2  (through 4)
  i=1 (1): right=3
  i=0 (3): right=1  (blocked by 1)

contrib:
  3*1*1 = 3
  1*2*3 = 6
  2*1*2 = 4
  4*1*1 = 4
Sum = 17 ✓
```

### Enumeration verification

| Subarray | min |
|---|---|
| [3] | 3 |
| [3,1] | 1 |
| [3,1,2] | 1 |
| [3,1,2,4] | 1 |
| [1] | 1 |
| [1,2] | 1 |
| [1,2,4] | 1 |
| [2] | 2 |
| [2,4] | 2 |
| [4] | 4 |
| **Total** | **17** |

### All-equal failure mode

```
arr = [2, 2, 2]
If both sides use non-strict smaller, double-count or zero-count.
Asymmetric strictness partitions subarrays among equal mins.
```

**Interview phrase:** "Ties are the bug farm. I make previous bound strict and next bound non-strict so each subarray's minimum is owned by exactly one index."

---

## 8B: Sum of Subarray Maximums

Same contribution idea; flip comparisons to previous/next **greater**.

```python
def sumSubarrayMaxs(arr):
    MOD = 10**9 + 7
    n = len(arr)
    left = [0] * n
    right = [0] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
```

---

## 8C: Sum of Subarray Ranges (LC 2104)

**Definition:** For every subarray, `max - min`. Sum those values.

**Insight:** `sum(max) - sum(min)` over all subarrays — reuse both contribution passes.

```python
def subArrayRanges(nums):
    def contrib(arr, is_max):
        n = len(arr)
        left = [0] * n
        right = [0] * n
        stack = []
        for i in range(n):
            if is_max:
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
            else:
                while stack and arr[stack[-1]] >= arr[i]:
                    stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            if is_max:
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
            else:
                while stack and arr[stack[-1]] > arr[i]:
                    stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)
        return sum(arr[i] * left[i] * right[i] for i in range(n))

    return contrib(nums, True) - contrib(nums, False)
```

**Complexity:** O(n) time, O(n) space. Beats O(n²) enumerate.

---

## 8D: Largest Rectangle in Histogram — Re-anchored Deep Dive

Module 4 introduced this; Module 10 owns the **contribution mindset** connection.

For bar `i` with height `h`:
- Left bound = previous strictly smaller index
- Right bound = next strictly smaller index  
- Width = `right - left - 1`
- Area = `h * width`

This is the same "how far does this value dominate" idea as subarray min contribution, but the aggregation is `max(area)` not `sum(h * count)`.

```python
def largestRectangleArea(heights):
    heights = [0] + heights + [0]  # sentinels
    stack = []  # increasing indices
    best = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            H = heights[stack.pop()]
            width = i - stack[-1] - 1
            best = max(best, H * width)
        stack.append(i)
    return best
```

### Trace `[2,1,5,6,2,3]`

Sentinels: `[0,2,1,5,6,2,3,0]`
When we pop 6 at the second 2: width between 5 and that 2 → area 6×1=6, then pop 5 → width larger, etc. Best includes 10 from height-5 width-2 and 8 from other configs — standard answer **10**.

---

## 8E: Maximal Rectangle in Binary Matrix (Hard)

**Reduce to histogram per row:**

```python
def maximalRectangle(matrix):
    if not matrix:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for row in matrix:
        for j, ch in enumerate(row):
            heights[j] = heights[j] + 1 if ch in ("1", 1) else 0
        best = max(best, largestRectangleArea(heights))
    return best
```

**Interview talk:** "Each row builds histogram heights of consecutive 1s upward; largest rectangle in histogram is the mono-stack subroutine."

---

## 8F: Remove Duplicate Letters / Smallest Subsequence (Mono + Greedy)

**Problem:** Return smallest in lexicographical order subsequence that contains each distinct letter once.

```python
def removeDuplicateLetters(s):
    last = {c: i for i, c in enumerate(s)}
    stack = []
    in_stack = set()
    for i, c in enumerate(s):
        if c in in_stack:
            continue
        while stack and c < stack[-1] and last[stack[-1]] > i:
            in_stack.remove(stack.pop())
        stack.append(c)
        in_stack.add(c)
    return "".join(stack)
```

**Invariant:** Stack is increasing; you may pop a letter only if it appears again later (`last[top] > i`).

**Connection:** Same "pop peaks when a better later option exists" as remove-k-digits, but with **must-keep-all-unique** constraint.

---

## 8G: Max Chunks — Full Traces

### Permutation version

```
arr = [1,0,2,3,4]
i=0: max=1 ≠ 0
i=1: max=1 == 1 → chunk++ (sort [1,0] → [0,1])
i=2: max=2 == 2 → chunk++
i=3: max=3 == 3 → chunk++
i=4: max=4 == 4 → chunk++
Answer 4
```

### General version (duplicates) — stack of maxima

```
arr = [2,1,3,4,4]
Process with mono stack of chunk maxes → number of chunks = len(stack)
```

---

## 8H: Online Stock Span — Full Stream Trace

```
next(100) stack=[] → span=1 → [(100,1)] → 1
next(80)  80<100 → span=1 → [(100,1),(80,1)] → 1
next(60)  → [(100,1),(80,1),(60,1)] → 1
next(70)  pop 60 span=1+1=2 → [(100,1),(80,1),(70,2)] → 2
next(60)  → [...,(70,2),(60,1)] → 1
next(75)  pop 60 (+1), pop 70 (+2) → span=4; 75<80 stop
          → [(100,1),(80,1),(75,4)] → 4
next(85)  pop 75(+4), pop 80(+1) → span=6; 85<100
          → [(100,1),(85,6)] → 6
```

**Failure mode:** Storing only prices without spans → must re-walk; loses O(1) amortized if you scan.

---

## 8I: Constrained Subsequence Sum (DP + Monoqueue) — Bridge

```
dp[i] = nums[i] + max(0, max(dp[j] for j in [i-k..i-1]))
```

Maintain decreasing deque of `dp` indices in window `k`.

```python
from collections import deque

def constrainedSubsetSum(nums, k):
    n = len(nums)
    dp = nums[:]
    q = deque()  # indices, decreasing dp
    best = nums[0]
    for i in range(n):
        if q:
            dp[i] = max(dp[i], nums[i] + dp[q[0]])
        best = max(best, dp[i])
        while q and dp[q[-1]] <= dp[i]:
            q.pop()
        q.append(i)
        if q[0] == i - k:
            q.popleft()
    return best
```

**Label:** Uses DP (Modules 8–9) + monoqueue. Include as **integration** once DP is earned; otherwise PREVIEW.

---

# PART 9: MORE WORKED PROBLEMS (FULL SOLUTIONS)

## P6: Implement Magic Dictionary (one char change)

```python
class MagicDictionary:
    def __init__(self):
        self.words = []

    def buildDict(self, dictionary):
        self.words = dictionary

    def search(self, searchWord):
        for w in self.words:
            if len(w) != len(searchWord):
                continue
            diff = sum(a != b for a, b in zip(w, searchWord))
            if diff == 1:
                return True
        return False
```

**Trie variant:** DFS with a `modified` boolean budget of 1. Better when dictionary is huge.

```python
def search_trie(self, word):
    def dfs(node, i, modified):
        if i == len(word):
            return node.is_end and modified
        c = word[i]
        # use exact edge
        if c in node.children and dfs(node.children[c], i + 1, modified):
            return True
        # spend modification
        if not modified:
            for ch, nxt in node.children.items():
                if ch != c and dfs(nxt, i + 1, True):
                    return True
        return False
    return dfs(self.root, 0, False)
```

---

## P7: Longest Word in Dictionary (trie build + DFS)

**Problem:** Longest word that can be built one character at a time from other dictionary words.

```python
def longestWord(words):
    root = TrieNode()
    for w in words:
        node = root
        for c in w:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
        node.word = w

    best = ""
    def dfs(node):
        nonlocal best
        if node is not root and not node.is_end:
            return
        if getattr(node, "word", None):
            w = node.word
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
        for ch in sorted(node.children.keys()):
            dfs(node.children[ch])
    dfs(root)
    return best
```

---

## P8: Shortest Unsorted Continuous Subarray (mono or two-pass)

```python
def findUnsortedSubarray(nums):
    n = len(nums)
    lo, hi = -1, -2
    mx, mn = float("-inf"), float("inf")
    for i in range(n):
        mx = max(mx, nums[i])
        if nums[i] < mx:
            hi = i
    for i in range(n - 1, -1, -1):
        mn = min(mn, nums[i])
        if nums[i] > mn:
            lo = i
    return hi - lo + 1
```

**Mono stack approach also works** — find leftmost/rightmost disorder bounds.

---

## P9: Asteroid Collision (stack)

```python
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
                continue
            elif stack[-1] == -a:
                stack.pop()
            alive = False
        if alive:
            stack.append(a)
    return stack
```

---

## P10: 132 Pattern (mono stack medium-hard)

```python
def find132pattern(nums):
    stack = []  # candidates for nums[k], decreasing
    third = float("-inf")  # nums[k]
    for j in range(len(nums) - 1, -1, -1):
        if nums[j] < third:
            return True  # nums[j] is '1', third is '2', stack had '3'
        while stack and stack[-1] < nums[j]:
            third = stack.pop()
        stack.append(nums[j])
    return False
```

---

# PART 10: EXPANDED CHEAT SHEETS

## Trie Decision & Complexity

| Task | Structure | Time |
|---|---|---|
| Exact word in dict | `set` or trie | O(L) |
| Prefix exists | trie / sorted+bisect | O(L) |
| Shortest root replace | trie walk | O(L) |
| `.` wildcards | trie DFS | O(b^L) worst |
| Board word search multi | trie + DFS | pruned 4^L |
| Prefix value sum | trie path aggregates | O(L) |
| Top-k autocomplete | trie + heap/cache | design tradeoff |

## Monotonic Pattern Matrix

| Problem smell | Structure | Strictness notes |
|---|---|---|
| Next greater/smaller | Mono stack indices | Decide < vs ≤ |
| Daily temps / span | Mono stack | Distances or merged spans |
| Histogram / maximal rectangle | Increasing stack | Sentinels help |
| Subarray min/max sum | Two mono passes + contrib | Asymmetric ties |
| Subarray ranges | sumMax − sumMin | |
| Remove k digits | Non-decreasing digit stack | Strip zeros |
| Remove duplicate letters | Increasing + last-index | Pop only if reappears |
| Window max/min | Deque | Store indices |
| max−min ≤ limit | Dual deques + two pointers | |
| 132 pattern | Mono from right | |
| Asteroids | Stack simulation | |

## Interview Opening Lines (Memorize)

**Trie:** "I'll build a character trie with `is_end` flags so prefix queries are a single walk."

**Contribution:** "I'll count how many subarrays have each element as the exclusive min using previous/next smaller spans."

**Remove k digits:** "To minimize the number I remove left-hand peaks with a monotonic increasing digit stack."

**Stock span:** "Online next-greater family — I collapse previous ≤ prices and accumulate spans."

**Word Search II:** "Dictionary goes into a trie; board DFS advances in the trie so dead prefixes die early."

## Edge Case Master List

| Area | Edges |
|---|---|
| Trie | empty string, duplicate inserts, delete shared prefix, unicode vs a-z |
| Wildcard | all dots, no children, longer than any word |
| Replace words | root equals word, multiple roots, empty dict |
| Board+trie | 1x1, no words, overlapping words, prune after find |
| Subarray mins | all equal, n=1, strictly sorted, negatives |
| Remove k digits | k=n, leading zeros, already increasing |
| Stock span | strictly decreasing, all equal, single day |
| Dual deque window | k=1, limit=0, all equal |

## Complexity Quick Card

| Algorithm | Time | Space |
|---|---|---|
| Trie insert/search | O(L) | O(L) new |
| WordDictionary search | O(b^L) worst | O(depth) |
| Word Search II | O(RC·4^L) worst | O(dict + L) |
| Mono stack family | O(n) | O(n) |
| Contribution sum mins | O(n) | O(n) |
| Remove k digits | O(n) | O(n) |
| Stock span amortized | O(1)/query | O(n) |
| Window max | O(n) | O(k) |

---

# PART 11: FAILURE MODES & DEBUG RITUALS

## When your mono stack is "O(n²)" in practice

You are scanning the stack for answers instead of assigning on pop. **Fix:** answers are written when an element is popped (or when a new element arrives that resolves previous tops).

## When trie TLE on Word Search II

1. Not pruning empty nodes after exploring  
2. Not marking board cells  
3. Dictionary contains duplicates — dedupe input  
4. Words much longer than board path possible — skip

## When remove-k-digits wrong

1. Forgot remaining `k` pops at end  
2. Forgot `lstrip("0")`  
3. Returned empty string instead of `"0"`  
4. Used `<` instead of `>` (built largest by mistake)

## Debug ritual (mono)

1. Draw array indices  
2. Write stack state after each i  
3. Verify each index pushed once  
4. Check strict vs non-strict against a ties example

## Debug ritual (trie)

1. Draw the trie after all inserts  
2. Mark `is_end` nodes with `*`  
3. Walk the failing query by hand  
4. Confirm search vs startsWith distinction

---

# PART 12: MODULE 4 → MODULE 10 UPGRADE MAP

| Module 4 (intro) | Module 10 (deep) |
|---|---|
| Next greater | + online stock span, 132 pattern |
| Daily temperatures | + span merging intuition |
| Histogram | + maximal rectangle, contribution link |
| Window max | + window min, dual deque constraints |
| — | Sum subarray mins/maxes/ranges |
| — | Remove k digits, remove duplicate letters |
| — | Max chunks |
| — | Tries entire half |

**Do not skip Module 4.** This lesson assumes you can already code next-greater and window-max cold.

---

# PART 13: SOLO DRILL LIST (NO ANSWERS HERE)

Do these blind after reading; answers live in Module 10 Retention.

1. LC 208 Implement Trie  
2. LC 211 Word Dictionary  
3. LC 648 Replace Words  
4. LC 212 Word Search II  
5. LC 907 Sum of Subarray Minimums  
6. LC 2104 Sum of Subarray Ranges  
7. LC 402 Remove K Digits  
8. LC 901 Online Stock Span  
9. LC 1438 Longest Continuous Subarray (max−min ≤ limit)  
10. LC 769/768 Max Chunks  
11. LC 316 Remove Duplicate Letters  
12. LC 84 + 85 Histogram / Maximal Rectangle  

---

*End of Tries & Monotonic — Complete Lesson (expanded).*
