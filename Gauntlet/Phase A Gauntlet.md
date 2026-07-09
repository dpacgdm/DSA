# PHASE A GAUNTLET — MODULE 11

**Purpose:** Close Phase A (Interview DSA) with full mock protocols, mixed timed sets, weak-spot drilling tied to the Retention Ledger, and an honest declaration checklist against gates **G1–G7** from `Handoff Doc.md`.

**Governance:**
- Chat-guided solves ≠ timed-verified. Mocks here count toward **G5** when run as real talk-aloud sessions.
- Only **earned** patterns for credit. If a problem needs an untaught tool, label **PREVIEW** (should not appear in Phase A declaration sets).
- Update `Metrics/Scoreboard.md` and `Metrics/Retention Ledger.md` after every mock and timed set.
- **No percentile claims. No "you're ready" without gates.**

**Prerequisites:** Majority of Phase A modules at `complete` (or explicitly waived with documented risk). Module 2 blocking retention must already be cleared.

---

# PART 1: FULL MOCK INTERVIEW PROTOCOL

## 1A: Session Setup

| Item | Standard |
|---|---|
| Duration | 45–60 min total (or 2× 25–35 mini-mocks) |
| Format | Talk while coding; interviewer (human or self-proctor) silent except clarifying Qs |
| Environment | Blind: no notes, no pattern labels, no lesson open |
| Language | Python (Phase A) |
| Problems | 1 hard **or** 2 mediums (see sets below) |
| After | Score rubric immediately; tag misses; ledger updates |

### Self-proctor script (if solo)

1. Start timer. Reveal problem text only.
2. Speak: restatement → examples → approach → complexity → code → trace → edges.
3. No pausing timer to "think silently for 10 minutes without talking" — interviews need narration. Brief silent coding bursts OK after approach is stated.
4. When stuck > 3 min with no progress: note it; try a smaller example; do **not** open solutions until the block ends.
5. After timer: compare to reference; score rubric honestly.

---

## 1B: Rubric (5 dimensions × 1–5)

Score each dimension 1–5. **G5 threshold:** average ≥ **4.0** over last **4** mocks.

| Score | Clarity | Correctness | Complexity talk | Code quality | Recovery |
|---|---|---|---|---|---|
| 5 | Crystal restatement, examples, structured plan | Fully correct + edges | Precise T/S with justification | Clean, idiomatic, few bugs | Stuck → self-corrects fast |
| 4 | Clear with minor vagueness | Correct core; tiny edge miss | Right big-O; small gap in why | Readable; minor slips | Recovers with light nudge |
| 3 | Understandable but rambling | Partial / buggy logic | States O(·) without derivation | Messy but workable | Needs substantial hint |
| 2 | Confused problem statement | Wrong approach mostly | Wrong or missing | Hard to follow | Spins; little progress |
| 1 | Cannot explain | No viable path | None | Unusable | Frozen |

### Dimension definitions

1. **Clarity** — Restate problem; ask constraints; walk examples; outline before code.
2. **Correctness** — Algorithm right; handles edges; matches spec.
3. **Complexity communication** — States time/space and *why* (e.g., "each index pushed once").
4. **Code quality** — Names, structure, Python pitfalls avoided (`deque` vs `pop(0)`, immutability, etc.).
5. **Recovery** — Debugs own bugs; simplifies; switches approach without panic.

### Scoring sheet (copy per mock)

```
Mock ID: ________  Date: ________  Set: ________
Problem(s): ________
Clarity: _/5  Correctness: _/5  Complexity: _/5  Code: _/5  Recovery: _/5
Average: _/5
Hints used: Y/N  First-pass correct: Y/N
Error tags: knowledge-gap / misread / time-pressure / careless-slip
Ledger rows touched: ________
Would-pass-screen: Y/N
```

---

## 1C: Interview Phases (Mechanical Checklist)

```
[ ] 0:00–2:00  Restate + constraints + examples (including edge)
[ ] 2:00–8:00  Brute force OK → optimize; state invariant/pattern
[ ] 8:00–12:00 Complexity + confirm with interviewer
[ ] 12:00–35:00 Code (narrate); use helper functions if clean
[ ] 35:00–42:00 Trace happy path + one edge on the code
[ ] 42:00–45:00 Complexity restatement + tradeoffs / follow-ups
```

Adjust times for 2-medium format (≈20–25 min each).

---

# PART 2: THREE FULL MOCK PROBLEM SETS

Each set: mixed medium/hard. **Reference solutions + scoring notes** included. Run blind first.

---

## MOCK SET 1 — Arrays / Hash / Window / Mono

### M1-P1 (Medium): Longest Substring with At Most K Distinct Characters

**Prompt:** Given string `s` and int `k`, return length of longest substring with at most `k` distinct characters.

#### Reference solution

```python
from collections import defaultdict

def longest_k_distinct(s, k):
    if k == 0:
        return 0
    count = defaultdict(int)
    left = best = 0
    for right, c in enumerate(s):
        count[c] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Complexity:** O(n) time, O(k) space.

#### Scoring notes

| Dimension | What earns 4–5 |
|---|---|
| Clarity | States window invariant: shrink while distinct > k |
| Correctness | Deletes key at 0 (not just decrement); k=0 edge |
| Complexity | O(n) amortized shrink |
| Code | `defaultdict` / Counter; no O(n²) rescans |
| Recovery | If broken on `"eceba", k=2` → expected 3 (`ece`) |

**Common miss:** `knowledge-gap` on variable window; `careless-slip` forgetting `del` when count hits 0.

---

### M1-P2 (Hard): Sliding Window Median (or discuss) / Alternative Hard: First Missing Positive

**Prompt (use this hard):** Given unsorted `nums`, find the smallest missing positive integer in O(n) time and O(1) extra space.

#### Reference solution

```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
```

**Complexity:** O(n) time, O(1) extra.

#### Scoring notes

- Clarity: "place value `v` at index `v-1`."
- Correctness: cycle-safe swap condition; ignore out-of-range.
- Recovery: if O(n) space hash set first, upgrade to in-place — partial credit on Correctness (3) if hash-only unless constraints force O(1).

---

### Mock Set 1 — Suggested run order

1. M1-P1 (25–30 min)  
2. M1-P2 (25–30 min)  
Or single hard M1-P2 with follow-up: "What if O(n) space allowed?"

**Rubric average target:** ≥ 4.0

---

## MOCK SET 2 — Trees / Graphs / Stack

### M2-P1 (Medium): Binary Tree Right Side View

**Prompt:** Given root, return list of node values from right side (top to bottom).

#### Reference solution

```python
from collections import deque

def right_side_view(root):
    if not root:
        return []
    ans = []
    q = deque([root])
    while q:
        rightmost = None
        for _ in range(len(q)):
            node = q.popleft()
            rightmost = node.val
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        ans.append(rightmost)
    return ans
```

**Alt:** DFS recurse right-first, record first visit per depth.

#### Scoring notes

- Must get **level** rightmost, not only root-to-leaf right spine (`[1,2,3]` with `2` having left `4` → `[1,3,4]`).
- Complexity O(n)/O(w).

---

### M2-P2 (Medium-Hard): Course Schedule II (topo) OR Daily Temperatures + follow-up Histogram

**Prompt:** `numCourses`, `prerequisites` as `[a,b]` meaning b before a. Return a valid order or empty if cycle.

#### Reference solution

```python
from collections import defaultdict, deque

def find_order(numCourses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == numCourses else []
```

#### Scoring notes

- Clarity: Kahn vs DFS topo; cycle ⇒ incomplete order.
- Code: direction of edge `b → a` correct.
- Tag `misread` if edge direction flipped.

---

### M2-P3 (Hard alternate): Largest Rectangle in Histogram

Use if graphs not yet `complete` — stay in earned mono stack.

#### Reference (sketch)

Increasing mono stack of indices; area = `h * (right - left - 1)` with sentinels.

#### Scoring notes

G5 credit only if Module 4+ mono is earned. Perfect place to test Complexity talk ("each bar once").

---

## MOCK SET 3 — DP / Backtracking / Trie-Mono

### M3-P1 (Medium): Coin Change (min coins) or House Robber II

**Prompt:** `coins`, `amount` — fewest coins to make amount, else -1.

#### Reference solution

```python
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

#### Scoring notes

- States `dp[x]` clearly.
- Unbounded knapsack loop order.
- Complexity O(amount · |coins|).

---

### M3-P2 (Medium): Word Break (dictionary) — trie or DP set

**Prompt:** `s`, `wordDict` — can `s` be segmented into dict words?

#### Reference solution

```python
def word_break(s, wordDict):
    words = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
```

**Trie variant:** OK if Module 10 earned — walk trie from each True `dp` index.

#### Scoring notes

- Prefer set for clarity unless asked for trie.
- Recovery: TLE on nested loops with long s → mention trie / max word length prune.

---

### M3-P3 (Hard): Remove K Digits OR Sum of Subarray Minimums

Pick one for mono deep dive credit.

#### Remove K Digits — reference

Monotonic non-decreasing digit stack; strip zeros; `"0"` if empty. (See Module 10 lesson.)

#### Scoring notes

- Clarity of greedy "remove left peaks."
- Edges: all removals, leading zeros, `k=0`.

---

# PART 3: TIMED MIXED SETS (BLIND)

**Protocol:** 45–60 min per set. No pattern labels. Score first-pass correct Y/N per problem. Tag misses (G7). Feed G3/G4 rolling windows on scoreboard.

Answers below — cover until done.

---

## TIMED SET A (4 problems, ~50 min) — Target: ≥ 3/4 first-pass

### A1. Merge Intervals

**Answer:** Sort by start; merge if `start <= last_end`. O(n log n).

```python
def merge(intervals):
    intervals.sort()
    out = []
    for s, e in intervals:
        if not out or s > out[-1][1]:
            out.append([s, e])
        else:
            out[-1][1] = max(out[-1][1], e)
    return out
```

---

### A2. Top K Frequent Elements

**Answer:** Counter + heap of size k, or bucket sort by frequency. O(n log k) heap / O(n) bucket.

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

### A3. Validate BST

**Answer:** Bounds recursion `(low, high)` or inorder strictly increasing.

```python
def is_valid_bst(root):
    def ok(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))
```

---

### A4. Next Greater Element II (circular)

**Answer:** Monotonic decreasing stack; scan twice `for i in range(2*n)`. O(n).

```python
def next_greater_elements(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []
    for i in range(2 * n):
        x = nums[i % n]
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        if i < n:
            stack.append(i)
    return ans
```

---

## TIMED SET B (4 problems, ~50 min)

### B1. 3Sum

**Answer:** Sort + fix i + two pointers; skip duplicates. O(n²).

---

### B2. Number of Islands

**Answer:** DFS/BFS flood fill or Union-Find. O(RC).

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(r + dr, c + dc)
    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "1":
                count += 1
                dfs(i, j)
    return count
```

---

### B3. House Robber (linear)

**Answer:** DP `rob/skip` or two variables. O(n)/O(1).

```python
def rob(nums):
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

---

### B4. Implement Trie (LC 208) — or Replace Words if trie already drilled

**Answer:** See Module 10 skeleton. Must use `is_end`.

---

## TIMED SET C (4 problems, ~55 min) — Slightly harder mix

### C1. Subarray Sum Equals K (count)

**Answer:** Prefix frequency hash. O(n).

---

### C2. Lowest Common Ancestor of BST

**Answer:** Walk down: both < → left; both > → right; else current. O(h).

---

### C3. Jump Game II (min jumps) or Jump Game I

**Answer (II):** Greedy end/farthest. O(n).

```python
def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
```

---

### C4. Stock Spanner design **or** Sum of Subarray Minimums

**Answer:** Mono stack per Module 10. Prefer Spanner for speed under timer; SOASM if aiming G4 hard transfer.

---

# PART 4: WEAK-SPOT IDENTIFICATION ↔ RETENTION LEDGER

## 4A: After every mock / timed set

1. Open `Metrics/Retention Ledger.md`.
2. For each miss, map to a **subskill row** (create row if missing).
3. Apply heat rules:

| Event | Heat action | Next due |
|---|---|---|
| Pass under timer | Upgrade toward `strong` | Longer interval |
| Fail / hint | Downgrade (`strong`→`shaky`→`weak`) | Shorten; `weak` twice → re-teach |
| Misread | Keep heat; add "restatement ritual" note | Due next session |
| Time-pressure | Speed drill that pattern; don't only re-teach theory | Due soon |

4. Update `Metrics/Scoreboard.md`: G3/G4 rolling, G5 mock averages, G6 redo queue, G7 tag completeness.

## 4B: Weak-spot checklist (Phase A families)

Mark `strong` / `shaky` / `weak` from ledger + latest evidence:

| Family | Subskills to scan | Heat |
|---|---|---|
| Complexity | Hidden costs, dependent nesting, communication | |
| Arrays/Strings | Two pointers, window, prefix, in-place | |
| Hashing | Prefix+hash, frequency, anagram keys | |
| Recursion/BT | Stack space, backtracking skeleton | |
| Binary search | Boundary predicates, bisect | |
| Sorting | Merge/quick, when to sort | |
| Linked lists | Reverse, two pointers, dummy | |
| Stack/Queue/Mono | Next greater, histogram, deque window | |
| Trees/BST | Traversals, LCA, validate BST | |
| Heaps | top-k, two heaps median | |
| Graphs | BFS/DFS, topo, UF, Dijkstra | |
| DP | 1D/2D, knapsack, LIS/LCS family | |
| Greedy | Interval, jump, remove k digits | |
| Trie | insert/search/prefix/wildcard | |
| Fenwick | exposure only — optional | |

## 4C: Targeted drill prescription

| Heat | Action before declaring Phase A |
|---|---|
| Any `weak` overdue > 2 cycles | **Block declaration** (G2). Re-teach + drill + re-grill |
| `shaky` due | Include in next retention warm-up |
| Failed timed medium | Add to **redo queue**; re-solve blind after ≥ 7 days (G6) |
| Mock dimension ≤ 2 | Mini-mock focusing that dimension only (e.g., clarity drills) |

---

# PART 5: PHASE A DECLARATION CHECKLIST (G1–G7)

Declare **Phase A ready for mocks-at-scale / applications** only when **ALL** pass. Cite evidence in scoreboard.

### G1 — Concept (teach-back)

| Module / topic | Teach-back without notes | Pass? |
|---|---|---|
| Big O framework | | |
| Arrays & strings patterns | | |
| Hashing | | |
| Recursion (MT only if M3 taught) | | |
| Binary search + sorting | | |
| LL + stacks/queues/mono intro | | |
| Trees + BST | | |
| Heaps + advanced windows | | |
| Graphs I/II | | |
| DP I/II + BT + greedy | | |
| Tries + mono deep | | |
| Fenwick/segment **exposure** explain-only | | |

**G1 Pass:** All completed modules teachable. □

### G2 — Retention ledger

| Check | Pass? |
|---|---|
| No `weak` subskill overdue > 2 review cycles | |
| All due items cleared or re-taught | |

**G2 Pass:** □

### G3 — Blind timed mediums

| Metric | Threshold | Actual |
|---|---|---|
| Last 20 timed mediums first-pass correct, no hints | ≥ 70% | ____% |

**G3 Pass:** □

### G4 — Hard transfer

| Metric | Threshold | Actual |
|---|---|---|
| Last 10 timed hards first-pass **or** same-session recovery to correct | ≥ 40% | ____% |

**G4 Pass:** □

### G5 — Interview skill

| Metric | Threshold | Actual |
|---|---|---|
| Last 4 full/mini mocks rubric average | ≥ 4.0 / 5.0 | ____ |

**G5 Pass:** □

### G6 — Redo integrity

| Metric | Threshold | Actual |
|---|---|---|
| Failed/hinted problems re-solved blind after ≥ 7 days | ≥ 90% | ____% |

**G6 Pass:** □

### G7 — Error honesty

| Metric | Threshold | Actual |
|---|---|---|
| Every timed miss tagged (knowledge-gap / misread / time-pressure / careless-slip) | 100% | ____% |

**G7 Pass:** □

---

## Declaration statement (fill only when all boxes checked)

```
PHASE A DECLARATION
Date: __________
Student: __________
All gates G1–G7: PASS
Scoreboard snapshot: (link/date) __________
Notes / residual risks: __________
Next: optional Phase B (CP) or Phase C (System Design); continued spaced ledger maintenance.
```

**Forbidden declarations:** "top X%", guaranteed offers, "complete" without timed-verify on claimed modules.

---

# PART 6: GAUNTLET WEEK PLAN (PACE-FLEXIBLE)

Not a deadline — a suggested order:

| Block | Activity |
|---|---|
| 1 | Timed Set A → ledger/scoreboard |
| 2 | Mock Set 1 → rubric G5 |
| 3 | Weak-spot drills from ledger |
| 4 | Timed Set B |
| 5 | Mock Set 2 |
| 6 | Timed Set C + hard focus (G4) |
| 7 | Mock Set 3 |
| 8 | Module 11 Final Assessment (`Retention Questions/Module 11 Final Assessment.md`) |
| 9 | Gate review → declare or loop weak spots |

---

# PART 7: QUICK REFERENCE — PATTERN → MODULE

| Smell | Reach for |
|---|---|
| Contiguous + constraint | Window / prefix / mono deque |
| Pairs / complements | Hash / two pointers |
| Next greater / spans / digits greedy | Monotonic stack |
| Prefix dictionary | Trie |
| Hierarchy / ancestors | Tree DFS / BST bounds |
| Dependencies / levels | Graph BFS / topo |
| Optimal substructure overlapping | DP |
| Explore all configs | Backtracking |
| Repeated max/min extract | Heap |
| Mutable range sum | Fenwick exposure / prefix if static |

---

*End of Phase A Gauntlet. Advance only on evidence.*

---

# PART 8: FULL MOCK SCRIPTS (INTERVIEWER SIDE)

## 8A: Mock Set 1 — Interlocutor Script (M1-P1 K Distinct)

```
[0:00] "Here's the problem. Take a minute to read."
[0:01] If silent >45s: "Can you restate the problem in your own words?"
[0:03] Expect: examples including k=0, empty s, all unique, all same.
[0:05] If jump to code: "What's the invariant of your window?"
[0:08] Hint ladder (only if stuck):
  H1: "What do you need to track inside the window?"
  H2: "When do you move left?"
  H3: "How do you delete a key from the count map cleanly?"
[0:25] "What's the time complexity and why is shrinking amortized?"
[0:28] "What if k is larger than the number of unique chars in s?"
```

### Rubric example — Strong candidate (avg 4.6)

| Dim | Score | Evidence |
|---|---|---|
| Clarity | 5 | Restated; examples k=0 and `"eceba",2` |
| Correctness | 5 | Deletes zero-count keys; correct best update |
| Complexity | 4 | Said O(n); needed nudge for amortized shrink |
| Code | 5 | Clean defaultdict; no off-by-one |
| Recovery | 4 | Caught missing `del` on self-trace |

### Rubric example — Weak candidate (avg 2.4)

| Dim | Score | Evidence |
|---|---|---|
| Clarity | 3 | Vague "use sliding window" |
| Correctness | 2 | Fixed window of size k (wrong problem) |
| Complexity | 2 | Claimed O(n²) without structure |
| Code | 2 | Nested loops scanning unique each time |
| Recovery | 3 | Fixed approach after H2 but buggy |

---

## 8B: Mock Set 1 — M1-P2 First Missing Positive Script

```
[0:00] Read problem; emphasize O(n) time O(1) space.
[0:04] Accept hash-set O(n) space as intermediate — then push constraints.
[0:10] "Where should value v live if it's in 1..n?"
[0:15] Watch infinite swap loops — need `nums[nums[i]-1] != nums[i]`.
[0:25] Trace [3,4,-1,1] on their code.
[0:35] Follow-up: "What if O(n) space allowed?" (set / bool array)
```

### Scoring notes detail

- Hash-only under O(1) constraint → Correctness ≤ 3 unless they upgrade
- Infinite loop on duplicates → Recovery opportunity
- Return `n+1` when `[1..n]` all present — often missed (Correctness)

---

## 8C: Mock Set 2 — Right Side View Script

```
Expect BFS level or DFS right-first.
Trap tree: 
      1
     / \
    2   3
     \
      4
Answer [1,3,4] not [1,3].
If they only walk right children: Correctness 2.
```

---

## 8D: Mock Set 2 — Course Schedule II Script

```
Clarify edge direction: [a,b] means b before a → edge b→a.
Ask: "What does an empty return mean?" → cycle.
Follow-up: "Return any valid order" vs "all orders" (backtrack — harder).
```

### Rubric example — Edge direction flip

Clarity 4, Correctness 1–2 until fixed, Recovery 5 if they catch on sample.

---

## 8E: Mock Set 3 — Coin Change Script

```
Distinguish: fewest coins (this) vs number of combinations vs permutations.
Trap: greedy fails on [1,3,4] amount 6 → greedy 4+1+1=3 but optimal 3+3=2.
Demand DP state definition before code.
```

---

## 8F: Mock Set 3 — Remove K Digits Script

```
Ask them to dry-run "1432219", k=3 before coding.
If they delete smallest digits: wrong — want remove peaks on the left.
Leading zeros follow-up mandatory.
```

---

# PART 9: ADDITIONAL TIMED SETS D–F

## TIMED SET D (~50 min) — Answers

### D1. Valid Palindrome II (at most one delete)

**Answer:** Two pointers; on mismatch try skip left or skip right.

```python
def validPalindrome(s):
    def ok(l, r):
        while l < r:
            if s[l] != s[r]: return False
            l += 1; r -= 1
        return True
    l, r = 0, len(s)-1
    while l < r:
        if s[l] != s[r]:
            return ok(l+1, r) or ok(l, r-1)
        l += 1; r -= 1
    return True
```

### D2. Insert Interval

**Answer:** Append non-overlapping before; merge overlaps; append rest. O(n).

### D3. Binary Tree Level Order

**Answer:** BFS deque; collect each level list.

### D4. Kth Smallest in BST

**Answer:** Inorder iterative stack until k pops; O(h+k).

---

## TIMED SET E (~50 min) — Answers

### E1. Longest Repeating Character Replacement

**Answer:** Window + max freq in window; shrink while `len - maxf > k`.

### E2. Number of Provinces (UF or DFS)

**Answer:** Connected components on adjacency matrix.

### E3. House Robber II (circular)

**Answer:** max(rob linear[0..n-2], rob linear[1..n-1]).

### E4. Implement Queue using Stacks

**Answer:** Two stacks; amortized O(1).

---

## TIMED SET F (~55 min, harder) — Answers

### F1. Trapping Rain Water

**Answer:** Two pointers or pref max L/R. O(n).

```python
def trap(height):
    lo, hi = 0, len(height)-1
    lmax = rmax = ans = 0
    while lo < hi:
        if height[lo] < height[hi]:
            lmax = max(lmax, height[lo])
            ans += lmax - height[lo]
            lo += 1
        else:
            rmax = max(rmax, height[hi])
            ans += rmax - height[hi]
            hi -= 1
    return ans
```

### F2. Word Ladder length (Graphs — only if M7 complete; else PREVIEW)

**Answer:** BFS from beginWord; neighbors by alphabet changes. O(words·L·26).

### F3. LIS O(n log n) patience

**Answer:** `tails` binary search replace.

### F4. Serialize/Deserialize BT

**Answer:** Preorder with `#` sentinels — see Module 11 Final F3.

---

# PART 10: DETAILED RUBRIC DIMENSION DRILLS

## 10A: Clarity drill (15 min)

Problem: any easy. Score **only** Clarity.
Checklist: restate, constraints asked, 2 examples, edge example, plan bullets before code.

## 10B: Complexity talk drill

After solving, record 60s complexity speech. Must include:
- Dominant operation count
- Why not worse (e.g., amortized pops)
- Space including output / recursion

## 10C: Recovery drill

Give a buggy solution (off-by-one window). Candidate must find bug by tracing — no new approach.

## 10D: Code quality checklist

```
[ ] No list.pop(0) for queue
[ ] No string += in hot loop
[ ] Clear names (left/right not i1/i2 without meaning)
[ ] Helpers extracted when nested >2 levels
[ ] Edges handled without copy-paste blocks
```

---

# PART 11: WEAK-SPOT DRILL PACKS (LEDGER-TIED)

## Pack α — Arrays/Hash shaky

1. Timed: 3Sum, Subarray Sum K, Longest substring no repeat (45 min)  
2. If miss → re-teach window vs prefix+hash decision tree  
3. Redo blind ≥7 days later (G6)

## Pack β — Mono/Trie shaky

1. Daily temps, Remove K digits, Implement Trie, Stock span  
2. Contribution problem only after spans solid  
3. Word Search II last

## Pack γ — Graphs shaky

1. Number of islands, Course schedule, Clone graph  
2. Dijkstra only if M8 taught  
3. Tag PREVIEW if attempted early

## Pack δ — DP shaky

1. Climb stairs, Coin change, House robber, LIS O(n²)  
2. Force state definition aloud before code  
3. Error-tag knowledge-gap vs careless transition bugs

## Pack ε — Interview skill (G5)

1. Two mini-mocks focusing lowest rubric dimension  
2. Record Clarity score trend across 4 sessions  
3. Do not declare Phase A if last-4 avg < 4.0

### Ledger update template after pack

```
Subskill: __________
Prior heat: __________
Result: pass / fail
New heat: __________
Next due: __________
Fail count: __________
Error tags: __________
```

---

# PART 12: MORE MOCK PROBLEM BANK (BRIEF PROMPTS + KEYS)

| ID | Prompt | Key | Diff |
|---|---|---|---|
| X1 | Min Window Substring | Need Counter + shrink | H |
| X2 | LRU Cache | DLL + hashmap | H |
| X3 | Alien Dictionary | Topo — M7 | H |
| X4 | Median of Two Sorted | Binsearch partition | H |
| X5 | Task Scheduler | Math/greedy counts | M |
| X6 | Decode String | Stack | M |
| X7 | Path Sum III | Prefix+hash on tree | M/H |
| X8 | Network Delay Time | Dijkstra — M8 | M |
| X9 | Edit Distance | 2D DP | H |
| X10 | Max Path Sum BT | DFS gains | H |

Use X-items for extra mocks after Sets 1–3. Score with same rubric.

---

# PART 13: TIMED SET SCORING SHEET

```
Set: A/B/C/D/E/F   Date: ____
P1: first-pass Y/N  time ____  tag ____
P2: first-pass Y/N  time ____  tag ____
P3: first-pass Y/N  time ____  tag ____
P4: first-pass Y/N  time ____  tag ____
Set accuracy: _/4
Feed into G3 (mediums) / G4 (hards) rolling windows
Hints used? (disqualifies first-pass) Y/N
```

---

# PART 14: PHASE A DECLARATION DRY-RUN

Before real declaration, run this dry-run:

1. Print scoreboard G3/G4/G5/G6/G7 numbers  
2. List any `weak` ledger rows — must be empty overdue  
3. Re-teach-back 3 random modules (G1 sample)  
4. If any fail → schedule packs α–ε; do **not** declare  

### Sample failing dry-run

```
G3: 65% → FAIL
G5: 4.2 → PASS
G2: 1 weak overdue (prefix+hash) → FAIL
Action: Pack α + 2 timed medium sets; re-check in later session
```

### Sample passing dry-run

```
G1–G7 all thresholds met with dates on scoreboard
Residual risk: Fenwick exposure only (acceptable)
Declare Phase A; maintain ledger weekly
```

---

# PART 15: COMMUNICATION CHEAT SHEET (MOCK USE)

| Moment | Line |
|---|---|
| Open | "Constraints on n? Mutate input OK? Duplicate values?" |
| Plan | "Brute is X; I can do Y because invariant Z." |
| Mid-code | "I'm maintaining … so that …" |
| Stuck | "I'll try a smaller example / restate the goal." |
| Close | "Time … because … Space … Edges I handled …" |

---

*End of Phase A Gauntlet (expanded). Advance only on evidence.*

---

# PART 16: FULL MOCK SET 4 & 5 (EXTRA)

## MOCK SET 4 — Mixed Medium

### M4-P1: Minimum Window Substring (Hard)

**Reference:** See Module 11 Final L1.  
**Scoring:** Clarity on need/missing counters; Correctness on shrink; Complexity O(|s|+|t|).

### M4-P2: LRU Cache (Hard)

**Reference:** OrderedDict or DLL+map.  
**Scoring:** O(1) claim must match structure; get updates recency.

### Interlocutor notes

```
Push: "What is O(1) about your DLL approach?"
Trap: using list.index (O(n)) — Code quality 2.
```

---

## MOCK SET 5 — Pressure Round (2 mediums, 40 min)

### M5-P1: 3Sum  
### M5-P2: Number of Islands  

**Scoring sheet:** average rubric; if either fails first-pass, G3 no credit for that problem.

### Sample strong narrative (3Sum)

"Sort O(n log n). Fix i, two pointers. Skip duplicates on i, lo, hi. Time O(n²)."

---

# PART 17: TIMED SET G & H

## SET G Answers

1. **Rotate Image** — transpose + reverse rows. O(n²).  
2. **Search 2D Matrix** — treat as virtual array BS or row then col.  
3. **Lowest Common Ancestor BST** — walk down.  
4. **Top K Frequent** — bucket or heap.

## SET H Answers

1. **Trapping Rain Water** — two pointers (Set F).  
2. **Binary Tree Zigzag** — BFS + reverse alternate.  
3. **Decode String** — stack of (str, count).  
4. **Jump Game II** — greedy end/far.

---

# PART 18: WEAK-SPOT MICRO-DRILLS (30 MIN EACH)

| Micro | Problems | Pass bar |
|---|---|---|
| Window | Longest no repeat; Min size sum; K distinct | 3/3 reasoning |
| Hash | Two sum; Subarray sum k; Group anagrams | 3/3 |
| Mono | Daily temps; Remove k digits; Window max | 3/3 |
| Tree | Invert; Level order; Validate BST | 3/3 |
| Graph | Islands; Course schedule; Clone | 3/3 |
| DP | Climb; Robber; Coin change | 3/3 |
| Trie | Implement; Replace words; startsWith cases | 3/3 |

After micro: update ledger heats same day.

---

# PART 19: RUBRIC CALIBRATION VIGNETTES

### Vignette 1 — Clarity 2
Candidate codes immediately; when asked to explain, cannot restate constraints.  
**Coach:** Stop coding; force 2-minute restatement ritual.

### Vignette 2 — Correctness 5, Complexity 2
Works on samples; says "I think O(n)" with nested loops actually O(n²).  
**Coach:** Count iterations aloud on n=4.

### Vignette 3 — Recovery 5
Bug on first trace; finds off-by-one; fixes without hint.  
**Keep:** This is G5 gold — note on scoreboard.

### Vignette 4 — Code 2
Uses `list.pop(0)` for BFS; string += in loop.  
**Coach:** Python ops cheat sheet redo from Module 1.

---

# PART 20: G3/G4 ROLLING WINDOW LOG TEMPLATE

```
Date | Problem | Diff | First-pass | Time | Hint | Tag | Notes
-----|---------|------|------------|------|------|-----|------
     |         | M/H  | Y/N        |      | Y/N  |     |
```

Compute: last 20 M → G3%; last 10 H → G4%.

---

*End of Phase A Gauntlet (expanded).*

---

# PART 21: COMPLETE MOCK DAY SCHEDULE (EVIDENCE PACK)

## Morning — Timed Set (50 min)

1. Pick Set A/B/C/D/E/F/G/H rotating unused sets.
2. Blind; no tags on problems.
3. Fill rolling log for G3/G4.
4. Tag every miss (G7).

## Midday — Weak-spot micro (30 min)

1. Choose pack from Part 11 / Part 18 based on morning tags.
2. Three problems only; quality over quantity.
3. Update Retention Ledger heats same day.

## Afternoon — Mini-mock (35 min)

1. One medium from Mock Sets 1–5.
2. Full talk-aloud; score all 5 rubric dimensions.
3. Write one Improvement Note: "Next mock I will …"

## Evening — Redo queue (optional 25 min)

1. Pull G6 items due (≥7 days since fail/hint).
2. Blind re-solve; mark success/fail on scoreboard.

---

# PART 22: PROBLEM-BY-PROBLEM SCORING ANCHORS

## Anchor: Sliding Window Medium

| Score | Clarity | Correctness |
|---|---|---|
| 5 | Names invariant; examples before code | Handles empty, k=0, all unique |
| 3 | Says "window" vaguely | Works on happy path only |
| 1 | No plan | Brute nested without recognition |

## Anchor: Graph BFS Medium

| Score | Complexity | Recovery |
|---|---|---|
| 5 | O(V+E) with visited justification | Fixes off-by-one queue level |
| 3 | Says O(n) unclear n | Needs hint to mark visited |
| 1 | No complexity | Infinite loop / no visited |

## Anchor: DP Medium

| Score | Clarity | Code |
|---|---|---|
| 5 | State + transition + base before code | Clean 1D/2D; INF init correct |
| 3 | Codes then reverse-explains | Off-by-one on amount loop |
| 1 | Greedy without checking | Wrong recurrence |

## Anchor: Hard Mono / Trie

| Score | Complexity talk | Correctness |
|---|---|---|
| 5 | Push/pop once law or trie O(L) | Full edges + trace |
| 3 | Right big-O weak why | Core OK missing ties/zeros |
| 1 | Claims O(n²) mono | Wrong structure |

---

# PART 23: PRE-DECLARATION AUDIT SCRIPT

Read aloud and check boxes:

```
[ ] Scoreboard updated within last 7 days
[ ] G3 ≥ 70% on last 20 timed mediums (number: ____)
[ ] G4 ≥ 40% on last 10 timed hards (number: ____)
[ ] G5 ≥ 4.0 on last 4 mocks (average: ____)
[ ] G6 redo ≥ 90% (number: ____)
[ ] G7 100% misses tagged
[ ] G2 no weak overdue > 2 cycles
[ ] G1 teach-back sample 3 modules passed this week
[ ] Module 2 no longer blocking
[ ] Fenwick labeled exposure only (OK)
[ ] No percentile claims in notes
```

If any unchecked → do not declare; schedule Part 21 day.

---

# PART 24: EXTRA TIMED SET I (ANSWERS)

1. **Product Except Self** — prefix/suffix products.  
2. **Validate Parentheses** — stack.  
3. **Max Depth BT** — recurse.  
4. **Implement Trie** — Module 10.  

## EXTRA TIMED SET J (ANSWERS)

1. **Merge k Sorted Lists** — heap.  
2. **Pacific Atlantic** — multi-source DFS/BFS (graphs).  
3. **Partition Equal Subset Sum** — DP knapsack.  
4. **Online Stock Span** — mono stack.  

---

# PART 25: CANDIDATE SELF-REVIEW FORM (POST-MOCK)

```
What I explained well: __________
Where I went silent: __________
First wrong turn: __________
Hint that would have been fair: __________
Pattern I should drill tomorrow: __________
Rubric dimension to raise: Clarity / Correctness / Complexity / Code / Recovery
Emotional state (optional): calm / rushed / foggy
```

Use this to pick tomorrow's micro-drill — not vibes alone.

---

# PART 26: LINKED ARTIFACTS

| Artifact | Role |
|---|---|
| `Metrics/Scoreboard.md` | G3–G7 numbers |
| `Metrics/Retention Ledger.md` | Heats / due |
| `Retention Questions/Module 11 Final Assessment.md` | Written cumulative |
| This Gauntlet | Mocks + timed + declaration |

---

*End of Phase A Gauntlet (expanded).*
