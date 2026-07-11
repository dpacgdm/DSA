# DYNAMIC PROGRAMMING II — ADVANCED PATTERNS

**Module:** 9 (DP II + Backtracking + Greedy)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Prerequisite:** Module 8 DP I — memoization vs tabulation, 1D DP (fib, climb stairs, house robber, coin change intro, LIS intro)  
**Language:** Python

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 0: HOW THIS DIFFERS FROM DP I

Module 8 taught the **machinery**:

| DP I (basics) | DP II (this file) |
|---|---|
| Identify overlapping subproblems | Design **2D / multi-index** states |
| Memo vs table; bottom-up fill order | Grid DP, knapsack families, subsequence DP |
| 1D recurrence (`dp[i]` from `dp[i-1]`, `dp[i-2]`) | Transitions over **two sequences**, **capacity**, **intervals** |
| "Try include/exclude" on linear arrays | Pattern recognition: which DP family? |
| Space-optimize 1D when safe | Know when 2D collapses to 1D / rolling arrays |

**Escalation rule:** Same three questions — *What is the state? What is the transition? What is the base case?* — but states get richer and fill order matters more.

If you cannot write climb stairs / house robber / 0-1 knapsack skeleton cold from DP I, stop and redrill those first.

---

# PART 1: THE ADVANCED DP RECIPE

## 1A: The Five Questions (Always)

Before writing code, answer in order:

```
1. STATE     — What does dp[...] mean in one English sentence?
2. TRANSITION — How do you compute one cell from smaller cells?
3. BASE      — Which cells are known without looking at others?
4. ORDER     — In what order must you fill so dependencies exist?
5. ANSWER    — Which cell (or aggregation) is the final answer?
```

Wrong state → wrong problem. Wrong order → reading garbage. Wrong answer cell → off-by-one forever.

## 1B: State Design Heuristics

| Signal in the problem | Likely state shape |
|---|---|
| Path on an `m×n` grid | `dp[r][c]` = best/count ending at `(r,c)` |
| Capacity / budget / weight | `dp[i][w]` = best using first `i` items with capacity `w` |
| Two strings / sequences | `dp[i][j]` = answer for prefixes `s[:i]`, `t[:j]` |
| Contiguous segment / burst / matrix chain | `dp[i][j]` = answer for subarray / substring `i..j` |
| Subset of small `n ≤ 20` choices | `dp[mask]` or `dp[mask][i]` (state compression) |

## 1C: Transition Design Heuristics

Ask: **"What was the last decision?"**

- Last cell entered from left or above → grid
- Last item taken or not → knapsack
- Last characters matched / substituted / deleted → edit / LCS
- Last cut / last balloon burst → interval DP

## 1D: Complexity Template

For table size `S` and work per cell `W`:

```
Time  ≈ S × W
Space ≈ S  (or less with rolling arrays / in-place)
```

Examples:
- Grid `m×n`, `W=O(1)` → O(mn)
- LCS `n×m`, `W=O(1)` → O(nm)
- Interval DP length `n`, `W=O(n)` per cell → O(n³)
- Knapsack `n` items, capacity `W` → O(nW)

---

# PART 2: 2D GRID DP

## 2A: Mental Model

A grid is a DAG: you only move right/down (or similar restricted moves). Every cell's answer depends only on cells that can reach it.

```
(0,0) → → →
  ↓   ↓   ↓
  → → → →
  ↓   ↓   ↓
        (m-1,n-1)
```

**State:** `dp[r][c]` = number of ways / min cost / max score to reach `(r,c)` from start (or from `(r,c)` to end — pick one direction and stick to it).

## 2B: Unique Paths (count ways)

**Problem:** `m×n` grid. Move only right or down. How many paths from top-left to bottom-right?

**State:** `dp[r][c]` = number of ways to reach `(r,c)` from `(0,0)`.

**Transition:**
```
dp[r][c] = dp[r-1][c] + dp[r][c-1]   # from above + from left
```

**Base:** First row and first column are all `1` (only one way: always right, or always down).

**Answer:** `dp[m-1][n-1]`

```python
def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]
```

**Space optimize:** Only need previous row → O(n) array.

```python
def uniquePaths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]
```

### Worked Trace — Unique Paths 3×3

```
Initial (bases filled):
1 1 1
1 ? ?
1 ? ?

Fill (1,1): from above=1 + left=1 → 2
1 1 1
1 2 ?
1 ? ?

Fill (1,2): 1 + 2 → 3
1 1 1
1 2 3
1 ? ?

Fill (2,1): 2 + 1 → 3
1 1 1
1 2 3
1 3 ?

Fill (2,2): 3 + 3 → 6
Answer: 6
```

## 2C: Unique Paths II (obstacles)

Same as Unique Paths, but some cells are blocked (`1` = obstacle).

**Extra rules:**
- If cell is obstacle → `dp[r][c] = 0`
- First row/col: once you hit an obstacle, everything beyond on that row/col is `0`

```python
def uniquePathsWithObstacles(grid):
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1:
        return 0
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                dp[r][c] = 0
                continue
            if r == 0 and c == 0:
                continue
            from_up = dp[r - 1][c] if r > 0 else 0
            from_left = dp[r][c - 1] if c > 0 else 0
            dp[r][c] = from_up + from_left
    return dp[m - 1][n - 1]
```

## 2D: Minimum Path Sum

**Problem:** Each cell has a cost. Find min sum path from top-left to bottom-right (right/down only).

**State:** `dp[r][c]` = min path sum to reach `(r,c)`.

**Transition:**
```
dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
```

**Base:** `dp[0][0] = grid[0][0]`; first row = running sum rightward; first col = running sum downward.

```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for c in range(1, n):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, m):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])
    return dp[m - 1][n - 1]
```

### Worked Trace — Min Path Sum

```
grid:
1 3 1
1 5 1
4 2 1

dp after bases:
1 4 5
2 ? ?
6 ? ?

(1,1): 5 + min(4,2) = 7
(1,2): 1 + min(5,7) = 6
(2,1): 2 + min(7,6) = 8
(2,2): 1 + min(6,8) = 7

Answer: 7  (path 1→3→1→1→1)
```

## 2E: Dungeon Game (harder grid)

**Problem:** Grid of health deltas (negative = damage). Knight starts top-left, ends bottom-right. Health must stay ≥ 1 at every cell. Find **minimum initial health**.

**Key insight:** Working forward is awkward (you don't know how much health you'll need later). Work **backward** from the princess.

**State:** `dp[r][c]` = minimum HP you must have **entering** `(r,c)` to reach the end safely.

**Transition (right/down moves):**
```
need = min(dp[r+1][c], dp[r][c+1]) - dungeon[r][c]
dp[r][c] = max(1, need)
```

**Base (bottom-right):**
```
dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
```

```python
def calculateMinimumHP(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    dp[m - 1][n - 1] = max(1, 1 - dungeon[m - 1][n - 1])

    for c in range(n - 2, -1, -1):
        dp[m - 1][c] = max(1, dp[m - 1][c + 1] - dungeon[m - 1][c])
    for r in range(m - 2, -1, -1):
        dp[r][n - 1] = max(1, dp[r + 1][n - 1] - dungeon[r][n - 1])

    for r in range(m - 2, -1, -1):
        for c in range(n - 2, -1, -1):
            need = min(dp[r + 1][c], dp[r][c + 1]) - dungeon[r][c]
            dp[r][c] = max(1, need)
    return dp[0][0]
```

### Why Backward?

Forward: "I have H health here" — but optimal path depends on future damage spikes.  
Backward: "To survive from here, I need at least X" — future is already solved. Classic **optimal substructure from the end**.

### Worked Trace — Dungeon (tiny)

```
dungeon:
-2  -3   3
-5  -10  1
10   30 -5

Start at bottom-right: max(1, 1-(-5)) = 6

Last row (right→left):
(2,1): max(1, 6-30)=1
(2,0): max(1, 1-10)=1

Last col (bottom→up):
(1,2): max(1, 6-1)=5
(0,2): max(1, 5-3)=2

(1,1): min(5,1) - (-10) = 11 → max(1,11)=11
(1,0): min(11,1) - (-5) = 6
(0,1): min(11,2) - (-3) = 5
(0,0): min(6,5) - (-2) = 7

Answer: 7
```

## 2F: Grid DP Cheat Sheet

| Problem | State | Transition | Order |
|---|---|---|---|
| Unique Paths | ways to `(r,c)` | up + left | TL → BR |
| Unique Paths II | same + obstacles → 0 | same | TL → BR |
| Min Path Sum | min cost to `(r,c)` | cell + min(up,left) | TL → BR |
| Max Path Sum (similar) | max to `(r,c)` | cell + max(up,left) | TL → BR |
| Dungeon | min HP entering `(r,c)` | max(1, min(down,right)−cell) | BR → TL |
| Cherry pickup / dual path | often 3D or dual-agent | advanced | — |

**Interview tell:** "paths on grid with only right/down" → almost always grid DP (or combinatorics if no obstacles/weights).

---

# PART 3: KNAPSACK FAMILY — DEEP

## 3A: The Family Tree

```
                    KNAPSACK
                   /        \
            0/1 (each item      Unbounded (item
             at most once)       reusable)
                |                    |
         dp[i][w] from          dp[w] from
         dp[i-1][...]           same row / 1D forward
```

| Variant | Item reuse | Classic problems |
|---|---|---|
| **0/1** | No | 0/1 knapsack, subset sum, partition equal subset, target sum |
| **Unbounded** | Yes | Coin change (ways / fewest), complete knapsack, rod cutting |
| **Bounded** | Up to `k` copies | Rare in interviews; reduce to 0/1 via binary splitting |

## 3B: 0/1 Knapsack — Full Derivation

**Problem:** `n` items, weights `wt[]`, values `val[]`, capacity `W`. Maximize value without exceeding `W`. Each item at most once.

**State:** `dp[i][w]` = max value using items `0..i-1` with capacity exactly-at-most `w`.

**Decision for item `i-1`:**
```
skip:  dp[i][w] = dp[i-1][w]
take:  dp[i][w] = val[i-1] + dp[i-1][w - wt[i-1]]   if wt[i-1] ≤ w
dp[i][w] = max(skip, take)
```

**Base:** `dp[0][w] = 0` for all `w` (no items → value 0).

```python
def knapsack_01(wt, val, W):
    n = len(wt)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]  # skip
            if wt[i - 1] <= w:
                dp[i][w] = max(dp[i][w], val[i - 1] + dp[i - 1][w - wt[i - 1]])
    return dp[n][W]
```

### Space Optimization (critical interview move)

Only previous row needed → 1D array. **Iterate capacity backward** so `dp[w - wt]` still refers to the previous item's row.

```python
def knapsack_01(wt, val, W):
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        for w in range(W, wt[i] - 1, -1):   # BACKWARD
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

**Why backward?** Forward would reuse the same item in one pass (accidentally unbounded).

### Worked Trace — 0/1 Knapsack

```
items: (wt,val) = (1,1), (3,4), (4,5), (5,7)   W = 7

After item0 (1,1): dp = [0,1,1,1,1,1,1,1]
After item1 (3,4): dp = [0,1,1,4,5,5,5,5]
After item2 (4,5): dp = [0,1,1,4,5,6,6,9]
After item3 (5,7): dp = [0,1,1,4,5,7,8,9]

Answer: 9  (items 1+2: weights 3+4, values 4+5)
```

## 3C: Subset Sum / Partition Equal Subset

**Subset sum:** Can you pick a subset of `nums` that sums to `target`?

This is 0/1 knapsack with `val = wt = nums`, asking reachability.

```python
def canPartition(nums):
    s = sum(nums)
    if s % 2:
        return False
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for t in range(target, x - 1, -1):
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
```

## 3D: Target Sum (assign +/-)

Assign `+` or `-` to each number so expression equals `target`.

**Trick:** Let `P` = sum of positive group, `N` = sum of negative.  
`P + N = total`, `P - N = target` → `P = (total + target) / 2`.  
Reduce to **count subsets with sum P** (0/1 knapsack counting).

```python
def findTargetSumWays(nums, target):
    total = sum(nums)
    if (total + target) % 2 or abs(target) > total:
        return 0
    P = (total + target) // 2
    dp = [0] * (P + 1)
    dp[0] = 1
    for x in nums:
        for t in range(P, x - 1, -1):
            dp[t] += dp[t - x]
    return dp[P]
```

## 3E: Unbounded Knapsack

**Difference from 0/1:** Item can be used many times.

**1D transition — iterate capacity FORWARD:**

```python
def unbounded_knapsack(wt, val, W):
    dp = [0] * (W + 1)
    for w in range(1, W + 1):
        for i in range(len(wt)):
            if wt[i] <= w:
                dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

Or outer loop items, inner capacity **forward**:

```python
def unbounded_knapsack(wt, val, W):
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        for w in range(wt[i], W + 1):      # FORWARD
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

## 3F: Coin Change — Two Flavors

### Fewest coins (unbounded min)

```python
def coinChange(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != INF else -1
```

### Number of combinations (order-independent)

**Outer coins, inner amount forward** — each combination counted once:

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:                    # outer = coins
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```

**If you swap loops** (outer amount, inner coins), you count **permutations** (order matters) — usually wrong for "number of combinations."

### Worked Trace — Coin Change Ways

```
amount=5, coins=[1,2,5]

After coin 1: dp = [1,1,1,1,1,1]
After coin 2: dp = [1,1,2,2,3,3]
After coin 5: dp = [1,1,2,2,3,4]

Answer: 4
  (5), (2+2+1), (2+1+1+1), (1+1+1+1+1)
```

## 3G: Knapsack Decision Cheat Sheet

| You need… | Loop direction (1D) | Pattern |
|---|---|---|
| Each item ≤ 1 | Capacity **backward** | 0/1 |
| Items reusable | Capacity **forward** | Unbounded |
| Can we hit sum T? | bool DP, backward | Subset sum |
| Count subsets sum T | int DP, backward | 0/1 count |
| Fewest coins | min DP, forward | Unbounded min |
| # coin combinations | outer coin, forward | Unbounded count |
| # coin permutations | outer amount | (usually not wanted) |

**Memory hook:**  
0/1 = "don't reuse updated cell" → go **back**.  
Unbounded = "reuse is OK" → go **forward**.

---

# PART 4: SUBSEQUENCE DP

## 4A: Two-String Grid Mental Model

For strings `s` (len n) and `t` (len m):

```
dp[i][j] = answer for s[:i] and t[:j]
         = prefixes of length i and j
```

Fill by increasing `i`, then `j`. Compare `s[i-1]` and `t[j-1]`.

## 4B: Longest Common Subsequence (LCS)

**State:** `dp[i][j]` = LCS length of `s[:i]` and `t[:j]`.

**Transition:**
```
if s[i-1] == t[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Base:** `dp[0][*] = dp[*][0] = 0`

```python
def longestCommonSubsequence(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]
```

### Worked Trace — LCS

```
s = "abcde", t = "ace"

      ""  a  c  e
""     0  0  0  0
a      0  1  1  1
b      0  1  1  1
c      0  1  2  2
d      0  1  2  2
e      0  1  2  3

Answer: 3 ("ace")
```

**Related:**
- Longest Common **Substring** → reset to 0 on mismatch; track global max (contiguous)
- Shortest Common Supersequence length = `n + m - LCS`
- Min deletions to make equal = `n + m - 2*LCS`

## 4C: Edit Distance (Levenshtein)

**Problem:** Min operations (insert, delete, replace) to turn `word1` into `word2`.

**State:** `dp[i][j]` = edit distance of `word1[:i]` → `word2[:j]`.

**Transition:**
```
if word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]          # free match
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],     # delete word1[i-1]
        dp[i][j-1],     # insert word2[j-1]
        dp[i-1][j-1],   # replace
    )
```

**Base:**
```
dp[i][0] = i   # delete all
dp[0][j] = j   # insert all
```

```python
def minDistance(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[n][m]
```

### Worked Trace — Edit Distance

```
word1="horse", word2="ros"

      "" r o s
""     0 1 2 3
h      1 1 2 3
o      2 2 1 2
r      3 2 2 2
s      4 3 3 2
e      5 4 4 3

Answer: 3
  horse → rorse (replace h→r)
       → rose  (delete r)
       → ros   (delete e)
```

## 4D: Longest Palindromic Subsequence (LPS)

**Insight:** LPS(s) = LCS(s, reverse(s)).

Or direct interval-style 2D on one string:

**State:** `dp[i][j]` = LPS length in `s[i..j]` inclusive.

**Transition:**
```
if s[i] == s[j]:
    dp[i][j] = 2 + dp[i+1][j-1]    # (careful when j=i+1 → 2)
else:
    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
```

**Base:** `dp[i][i] = 1`

**Order:** Increasing length of substring.

```python
def longestPalindromeSubseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 if length == 2 else 2 + dp[i + 1][j - 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

### Worked Trace — LPS

```
s = "bbbab"

length 1: all 1s on diagonal
length 2: "bb"→2, "bb"→2, "ba"→1, "ab"→1
...
dp[0][4] = 4  ("bbbb")

Answer: 4
```

**Related:** Min insertions to make palindrome = `n - LPS(s)`.

## 4E: Distinct Subsequences

**Problem:** Number of times `t` appears as a subsequence of `s`.

```
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]  # use or skip this s char
else:
    dp[i][j] = dp[i-1][j]
```

Base: `dp[i][0] = 1` (one way to form empty `t`).

## 4F: Subsequence DP Cheat Sheet

| Problem | Match case | Mismatch case |
|---|---|---|
| LCS | `1 + diag` | `max(up, left)` |
| Edit distance | `diag` | `1 + min(up, left, diag)` |
| LPS (interval) | `2 + inside` | `max(shrink L, shrink R)` |
| Distinct subsequences | `diag + up` | `up` |
| LCS substring | `1 + diag` else `0` | reset; track max |

---

# PART 5: INTERVAL / PARTITION DP (INTRO)

## 5A: When You See This Pattern

Signals:
- "Burst balloons / matrix chain / burst balloons / palindrome partitioning min cuts"
- Optimal cost of processing a **contiguous segment**
- You choose a **last** (or first) operation that splits `i..j` into parts

**State:** `dp[i][j]` = best answer for range `i..j`.

**Transition shape:**
```
for k in i..j:   # last cut / last burst / last multiply
    dp[i][j] = best( dp[i][k] ⊕ dp[k+1][j] ⊕ cost(i,k,j) )
```

**Order:** By increasing interval length. Length-1 first, then 2, …

**Complexity:** Usually **O(n³)** — n² intervals × n choices of `k`.

## 5B: Matrix Chain Multiplication (light)

**Problem:** Matrices `A1..An` with dimensions `dims[0..n]`. Min scalar multiplications to compute product.

**State:** `dp[i][j]` = min cost to multiply matrices `i..j` inclusive.

```
dp[i][j] = min over k=i..j-1 of:
    dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1]
```

```python
def matrix_chain(dims):
    n = len(dims) - 1  # number of matrices
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n - 1]
```

## 5C: Burst Balloons (canonical hard interval DP)

**Problem:** Balloons with coins `nums[i]`. Bursting `i` gives `nums[L]*nums[i]*nums[R]` where `L,R` are nearest remaining neighbors. Maximize coins.

**Trick:** Think of **last** balloon burst in open interval `(left, right)`.

Pad: `arr = [1] + nums + [1]`

**State:** `dp[l][r]` = max coins bursting balloons **strictly between** `l` and `r`.

```
dp[l][r] = max over k in (l+1 .. r-1):
    arr[l]*arr[k]*arr[r] + dp[l][k] + dp[k][r]
```

```python
def maxCoins(nums):
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):          # r - l
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r],
                    arr[l] * arr[k] * arr[r] + dp[l][k] + dp[k][r])
    return dp[0][n - 1]
```

### Why "Last Burst"?

If `k` is last in `(l,r)`, then when it bursts, neighbors are exactly `arr[l]` and `arr[r]` (everything between already gone). Subproblems `(l,k)` and `(k,r)` are independent. Beautiful optimal substructure.

### Tiny Trace

```
nums = [3,1,5] → arr = [1,3,1,5,1]

Small intervals first, build up to dp[0][4].
Answer: 35
  One optimal order: burst 1 → 3*1*5=15; burst 3 → 1*3*5=15; burst 5 → 1*5*1=5; total 35
```

## 5D: Palindrome Partitioning II (min cuts) — bridge

`dp[i]` = min cuts for prefix `s[:i]`.  
`dp[j+1] = min(dp[j+1], dp[i] + 1)` when `s[i..j]` is palindrome.

Uses interval **palindrome precompute** + 1D DP. Interview-common hybrid.

## 5E: Interval DP Cheat Sheet

| Problem | What `k` means | Cost combine |
|---|---|---|
| Matrix chain | Split after matrix k | left + right + multiply cost |
| Burst balloons | Last balloon in open interval | left + right + l*k*r |
| Min score triangulation | Diagonal / triangle tip | similar O(n³) |
| Rod cutting (unbounded) | often NOT interval — unbounded knapsack | — |

**When NOT interval:** If order of items doesn't care about contiguity, use knapsack / subsequence instead.

---

# PART 6: STATE COMPRESSION DP (MENTION)

## 6A: When It Appears

- `n ≤ 20` (sometimes 15–24)
- "Assign each person a task", "TSP-style visit cities", "subset of skills"
- State naturally is a **bitmask** of used/visited elements

**State:** `dp[mask]` = best answer for the subset represented by bits.  
Or `dp[mask][i]` = best ending at `i` having visited `mask`.

## 6B: Traveling Salesman sketch (Held–Karp)

```
dp[mask][i] = min cost to visit exactly the nodes in mask, ending at i

dp[mask | (1<<j)][j] = min(dp[mask][i] + dist[i][j])
```

Time O(n² · 2ⁿ). Know it exists; rarely coded from scratch in interviews unless n is tiny and problem screams TSP.

## 6C: Interview Guidance

- If n≤20 and subsets matter → mention bitmask DP as candidate
- If n=100 → bitmask is impossible; need different structure
- Don't force compression when standard 2D DP works

---

# PART 7: DECISION GUIDE — WHICH DP PATTERN?

## 7A: Flowchart (Interview Speed)

```
1. Grid + restricted moves (right/down)?
      → GRID DP

2. Capacity / weight / sum-to-target / coins?
      → KNAPSACK family
         each item once? → 0/1 (backward)
         reusable? → unbounded (forward)

3. Two strings / sequences, subsequence or edit?
      → SUBSEQUENCE 2D DP (LCS / edit / distinct)

4. One string, palindrome subsequence / min inserts?
      → LPS (LCS with reverse OR interval on one string)

5. Contiguous range, choose split/last operation, O(n³) OK?
      → INTERVAL / PARTITION DP

6. n ≤ 20, subsets of choices?
      → STATE COMPRESSION

7. Still stuck?
      → Write recursive solution + memoize (top-down).
         The memo keys ARE your state.
```

## 7B: Top-Down Escape Hatch

When bottom-up fill order is confusing, write the recursive definition first:

```python
from functools import lru_cache

@lru_cache(None)
def dfs(i, j):
    # base cases
    # return transition using dfs(smaller states)
```

Then convert to table if needed for speed/space clarity.

## 7C: Common Misidentification Traps

| Looks like… | Actually… |
|---|---|
| "Longest increasing **subsequence**" | 1D DP O(n²) or patience O(n log n) — not LCS unless two arrays |
| "Longest palindromic **substring**" | Expand around center / DP boolean — not LPS |
| Coin change "number of ways" | Loop order matters (combos vs perms) |
| House robber on **tree** | Tree DP (Module 5 skill + DP) |
| Shortest path in weighted graph | Dijkstra — **not** DP unless DAG |

---

# PART 8: MASTER CHEAT SHEETS

## 8A: Pattern → State → Complexity

| Pattern | Typical state | Time | Space |
|---|---|---|---|
| Grid paths/cost | `dp[r][c]` | O(mn) | O(mn)→O(n) |
| 0/1 knapsack | `dp[i][w]` / 1D | O(nW) | O(W) |
| Unbounded | `dp[w]` | O(nW) | O(W) |
| LCS / Edit | `dp[i][j]` | O(nm) | O(nm)→O(min) |
| LPS | `dp[i][j]` | O(n²) | O(n²) |
| Interval | `dp[i][j]` + k | O(n³) | O(n²) |
| Bitmask | `dp[mask]` | O(S·2ⁿ) | O(2ⁿ) |

## 8B: Base Case Catalog

| Pattern | Bases |
|---|---|
| Grid count | first row/col = 1 (or 0 past obstacle) |
| Grid min sum | running sums on borders |
| Dungeon | end cell `max(1, 1-cell)`; fill BR→TL |
| Knapsack | `dp[0]=0` or `dp[0]=True` / `1` for counts |
| LCS | row0/col0 = 0 |
| Edit | row0 = j, col0 = i |
| LPS | diagonal = 1 |
| Interval | length 1 = 0 or trivial; build by length |

## 8C: Space Optimization Moves

1. Grid / LCS: keep only previous row
2. 0/1 knapsack: 1D backward
3. Unbounded: 1D forward
4. Edit distance: 1D with careful prev-diag save
5. Interval: usually cannot drop below O(n²)

## 8D: Reconstruction (optional interview flex)

To recover the actual path / subset / LCS string:
- Store predecessor choices, or
- Walk backward from answer cell using the same transition logic in reverse

```python
# Reconstruct LCS
i, j = n, m
out = []
while i > 0 and j > 0:
    if s[i-1] == t[j-1]:
        out.append(s[i-1]); i -= 1; j -= 1
    elif dp[i-1][j] >= dp[i][j-1]:
        i -= 1
    else:
        j -= 1
return ''.join(reversed(out))
```

---

# PART 9: WORKED PROBLEMS (FULL TRACES)

## Problem 1: Unique Paths II

**Grid:**
```
0 0 0
0 1 0
0 0 0
```

**Fill:**
```
1 1 1
1 0 1
1 1 2
```

Obstacle zeros out center. Answer **2**.

---

## Problem 2: Partition Equal Subset Sum

`nums = [1,5,11,5]`, total 22, target 11.

```
dp bool for target 11, process items backward:
start: [T,F,F,...,F]
+1: can hit 1
+5: can hit 5,6
+11: can hit 11,12,16,17
+5: can hit 11 via 6+5 etc.

dp[11] = True
```

---

## Problem 3: Edit Distance "kitten" → "sitting"

Classic answer **3**:  
kitten → sitten (replace k) → sittin (replace e) → sitting (insert g).

Verify with DP table mentally: final cell 3.

---

## Problem 4: Burst Balloons [3,1,5,8]

Padded `[1,3,1,5,8,1]`. Full O(n³) fill yields **167** (LeetCode 312 canonical).

Key check in interview: explain last-burst transition, not memorize number.

---

## Problem 5: Coin Change Combinations vs Permutations

`amount=3`, `coins=[1,2]`

| Method | Result | Meaning |
|---|---|---|
| Outer coins | 2 | `{1+1+1}, {1+2}` |
| Outer amount | 3 | also counts `{2+1}` as different |

Know which the problem asks for.

---

# PART 10: IMPLEMENTATION PITFALLS

1. **Off-by-one on string DP** — `dp` is `(n+1)×(m+1)`; compare `s[i-1]`.
2. **Wrong knapsack loop direction** — 0/1 forward = bug.
3. **Forgetting bases on grid borders.**
4. **Dungeon forward** — usually wrong; go backward.
5. **Interval DP wrong order** — must increase length, not row-major blindly.
6. **LCS vs substring** — mismatch handling differs completely.
7. **Modulo** on "number of ways" problems — apply on every add.
8. **Python recursion depth** on top-down for large n — prefer bottom-up or raise limit carefully.
9. **INF sentinel** in min-coin — use `amount+1`, not `float('inf')` if you add `1+dp[...]` carelessly without checks.
10. **Mutating 1D incorrectly** when you still need the previous diagonal (edit distance space opt).

---

# PART 11: INTERVIEW SCRIPT

When you see a DP problem:

```
1. "I'll define a state: dp[...] means ___."
2. "Transition: to compute this, I consider last decision ___."
3. "Base cases: ___."
4. "Fill order: ___ so dependencies are ready."
5. "Answer is in cell ___."
6. "Time ___, space ___; I can optimize space by ___ if needed."
7. Code. Trace a 3×3 or tiny example out loud.
8. Edge cases: empty, single cell, zeros, impossible → -1/0.
```

---

# PART 12: PRACTICE SET (MODULE 9 DP II)

Solve blind after teaching. Tag pattern before coding.

| # | Problem | Pattern |
|---|---|---|
| 1 | Unique Paths | Grid count |
| 2 | Unique Paths II | Grid + obstacles |
| 3 | Minimum Path Sum | Grid min |
| 4 | Dungeon Game | Grid backward |
| 5 | 0/1 Knapsack (classic) | 0/1 |
| 6 | Partition Equal Subset Sum | 0/1 bool |
| 7 | Target Sum | 0/1 count |
| 8 | Coin Change | Unbounded min |
| 9 | Coin Change II | Unbounded ways |
| 10 | LCS | Subsequence |
| 11 | Edit Distance | Subsequence |
| 12 | Longest Palindromic Subsequence | LPS |
| 13 | Distinct Subsequences | Subsequence count |
| 14 | Burst Balloons | Interval |
| 15 | Matrix Chain (practice) | Interval |
| 16 | Min Cost to Cut a Stick | Interval |
| 17 | Ones and Zeroes (strs with 0/1 budget) | 2D knapsack |
| 18 | Longest Common Substring | Variant |
| 19 | Shortest Common Supersequence | LCS-derived |
| 20 | PREVIEW: TSP n≤12 | Bitmask |

---

# PART 13: BRIDGE TO BACKTRACKING / GREEDY

| If the problem… | Prefer |
|---|---|
| Needs **count/optimize** with overlapping subproblems | DP |
| Needs **all configurations** / construct every valid board | Backtracking |
| Local choice is provably safe (exchange argument) | Greedy |
| Feels like DP but greedy works (jump game I) | Greedy — prove it |
| Feels like greedy but counterexample exists | DP |

Module 9's other file (`Backtracking/Backtracking & Greedy.md`) covers the non-DP half of this decision.

---

# PART 14: ADDITIONAL WORKED PROBLEMS

## 14A: Ones and Zeroes (2D 0/1 Knapsack)

**Problem:** `strs` of binary strings; budgets `m` zeros and `n` ones. Max strings you can form.

**State:** `dp[z][o]` = max strings using ≤ `z` zeros and ≤ `o` ones.

```python
def findMaxForm(strs, m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count('0')
        ones = s.count('1')
        for z in range(m, zeros - 1, -1):
            for o in range(n, ones - 1, -1):
                dp[z][o] = max(dp[z][o], 1 + dp[z - zeros][o - ones])
    return dp[m][n]
```

**Why backward in both dimensions?** Same 0/1 reason — each string at most once.

## 14B: Shortest Common Supersequence (length + reconstruct)

Length = `n + m - LCS`. To reconstruct: walk the LCS DP table; on mismatch append the char from the side you move from; on match append once.

```python
def shortestCommonSupersequence(str1, str2):
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j = n, m
    out = []
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            out.append(str1[i - 1]); i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            out.append(str1[i - 1]); i -= 1
        else:
            out.append(str2[j - 1]); j -= 1
    while i > 0:
        out.append(str1[i - 1]); i -= 1
    while j > 0:
        out.append(str2[j - 1]); j -= 1
    return ''.join(reversed(out))
```

## 14C: Longest Common Substring (contrast drill)

```python
def longestCommonSubstring(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                best = max(best, dp[i][j])
            # else leave 0
    return best
```

Say out loud: **subsequence** allows gaps; **substring** does not → mismatch resets.

## 14D: Min Cost to Cut a Stick (interval)

Cuts `cuts` on stick length `n`. Cost of a cut = current segment length.

Pad cuts with `0` and `n`, sort. `dp[i][j]` = min cost to cut everything between padded cuts `i` and `j`.

```python
def minCost(n, cuts):
    arr = sorted([0] + cuts + [n])
    m = len(arr)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = float('inf')
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
            dp[i][j] += arr[j] - arr[i]
    return dp[0][m - 1]
```

Same family as burst balloons / matrix chain.

## 14E: Top-Down LCS (escape hatch demo)

```python
from functools import lru_cache

def longestCommonSubsequence(s, t):
    @lru_cache(None)
    def dfs(i, j):
        if i == len(s) or j == len(t):
            return 0
        if s[i] == t[j]:
            return 1 + dfs(i + 1, j + 1)
        return max(dfs(i + 1, j), dfs(i, j + 1))
    return dfs(0, 0)
```

Memo keys `(i,j)` = the DP state. Convert to bottom-up when you need guaranteed O(nm) without recursion limits.

---

# PART 15: FILL-ORDER DRILLS

Say the fill order for each (no code):

| Problem | Order |
|---|---|
| Unique Paths | increasing r, then c |
| Dungeon | decreasing r, then c |
| 0/1 knapsack 2D | increasing i, any w (inner) |
| 0/1 knapsack 1D | per item, w from W down to wt |
| Unbounded coin ways | per coin, a from coin to amount |
| LCS / Edit | increasing i, then j |
| LPS interval | increasing substring length |
| Burst balloons | increasing open-interval length |
| Bitmask TSP | increasing popcount(mask), or any order that adds bits |

Wrong order → reading uninitialized / stale cells → silent WA.

---

# PART 16: ONE-PAGE SUMMARY

```
GRID:        dp[r][c] from up/left (or down/right for dungeon)
0/1 KNAP:    backward 1D; each item once
UNBOUNDED:   forward 1D; coins/rod
LCS:         match → diag+1; else max(up,left)
EDIT:        match → diag; else 1+min(3)
LPS:         LCS(s, rev) OR interval dp[i][j]
INTERVAL:    dp[i][j] = best split/last k; O(n³)
BITMASK:     n≤20 subset DP
ESCAPE:      recurse + memo; keys = state
SCS:         n+m-LCS; reconstruct by walking table
```

**Mastery bar for this file:** Explain any row of the decision guide, write LCS + 0/1 knapsack + min path sum from scratch, trace edit distance on a 4×4 table without notes, and state fill order for dungeon vs unique paths cold.


---

# PART — DIGIT DP (MUST-KNOW TEMPLATE)

**When:** Count / aggregate over numbers in `[0, N]` (then range via `f(R)-f(L-1)`) with digit constraints.

## Five lines

```
STATE:  dfs(pos, tight, lead_zero, extra...)
BASE:   pos == len(digits) → valid complete number
TRANS:  try digit 0..up; update tight/lead; recurse
MEMO:   (pos, tight, lead_zero, extra)
ANSWER: dfs(0, True, True) on digits of N
```

## Worked: count integers `≤ N` whose digits contain **no** `4`

```python
def count_no_four(n: int) -> int:
    if n < 0:
        return 0
    digits = list(map(int, str(n)))
    memo = {}

    def dfs(pos: int, tight: bool, lead: bool) -> int:
        if pos == len(digits):
            return 1
        key = (pos, tight, lead)
        if key in memo:
            return memo[key]
        up = digits[pos] if tight else 9
        total = 0
        for d in range(up + 1):
            if not lead and d == 4:
                continue  # started number cannot use 4
            # leading zeros: still "lead", digit 4 as leading zero doesn't start the number
            nlead = lead and d == 0
            if not nlead and d == 4:
                continue
            ntight = tight and (d == up)
            total += dfs(pos + 1, ntight, nlead)
        memo[key] = total
        return total

    return dfs(0, True, True)
```

Range `[L, R]` → `count_no_four(R) - count_no_four(L - 1)`.

**Interview line:** "Digit DP on the decimal representation with `tight` and `lead_zero`; memoize."

## Teach-back

1. What does `tight` prevent?  
2. Why keep `lead_zero` instead of treating leading zeros as digit 0 forever?  
3. How do you reduce `[L,R]` to one function?

---

# PART — BITMASK DP (ONE WORKED PATTERN)

**When:** `n ≤ 20`; state is a subset; transitions add one element.

```
dp[mask] = best / ways for subset mask
for i not in mask: consider mask | (1<<i)
```

## Worked: assign `n` jobs to `n` workers (min cost)

`cost[i][j]` = cost of worker `i` doing job `j`. Stage = `mask.bit_count()` = next worker.

```python
def min_cost(cost: list[list[int]]) -> int:
    n = len(cost)
    N = 1 << n
    INF = 10**18
    dp = [INF] * N
    dp[0] = 0
    for mask in range(N):
        i = mask.bit_count()
        if i >= n:
            continue
        for j in range(n):
            if mask & (1 << j):
                continue
            nxt = mask | (1 << j)
            dp[nxt] = min(dp[nxt], dp[mask] + cost[i][j])
    return dp[N - 1]
```

**TSP-shaped** needs `dp[mask][i]` (last city). **Assignment** above does not.

**Refuse** raw `2^n` if n>20 unless meet-in-middle.

## Teach-back

When is stage=`popcount` valid? When must you store the last index too?
