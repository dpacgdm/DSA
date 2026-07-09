# MODULE 9 RETENTION — DP II + BACKTRACKING + GREEDY (+ CUMULATIVE)

---

**Purpose:** Cumulative retention grill for Module 9 teach artifacts:
- `Dynamic Programming/DP II.md`
- `Backtracking/Backtracking & Greedy.md`

Plus spaced pull from prior Phase A material (especially DP I concepts, recursion/backtracking seeds, heaps for Huffman/meeting-rooms contrast). Problems that need **untaught** Module 10+ machinery (tries deep, segment trees) are tagged **`PREVIEW — no mastery credit`**.

**Rules:**
1. No pattern labels on the problem statement side — identify the tool yourself, then check the answer key.
2. For each problem: approach → code → trace → edge cases → complexity.
3. Tag misses: `knowledge-gap` / `misread` / `time-pressure` / `careless-slip`.
4. Passing this grill alone ≠ `complete`. Still need timed verification + ledger updates per `Handoff Doc.md`.

**Escalation map:**

| Section | Focus | Difficulty |
|---|---|---|
| A | Vocabulary + complexity rapid fire | Warm |
| B | Grid DP + knapsack | Warm → Medium |
| C | Subsequence + interval DP | Medium |
| D | Backtracking classics | Medium |
| E | Greedy + decision (greedy vs DP vs BT) | Medium |
| F | Debug the bug | Medium |
| G | Cumulative integration | Mixed |
| H | Blind-style mixed set | Interview |

---

# SECTION A: RAPID FIRE — VOCABULARY & COMPLEXITY

Answer in 1–3 sentences unless code is requested.

---

## A1. Five DP questions

List the five questions you must answer before coding any DP solution.

---

## A2. Grid unique paths

State `dp[r][c]`, transition, base cases, and answer cell for Unique Paths on an `m×n` grid (right/down only).

---

## A3. Dungeon direction

Why is Dungeon Game typically filled **bottom-right → top-left** instead of top-left → bottom-right?

---

## A4. 0/1 vs unbounded loop

In 1D knapsack, which capacity loop direction is 0/1? Which is unbounded? Why?

---

## A5. Coin combinations vs permutations

For "number of coin combinations," should coins be the outer loop or inner? What goes wrong if you swap?

---

## A6. LCS transition

Write the LCS recurrence for `dp[i][j]` when comparing `s[i-1]` and `t[j-1]`.

---

## A7. Edit distance ops

Name the three operations in the mismatch case of edit distance and which prior cell each uses.

---

## A8. LPS shortcut

How can you compute Longest Palindromic Subsequence using LCS?

---

## A9. Interval DP complexity

Why is classic interval DP (matrix chain / burst balloons) O(n³)?

---

## A10. Bitmask when

When is state-compression / bitmask DP a reasonable interview tool? When is it not?

---

## A11. Choose / explore / unchoose

State the backtracking template in three steps. Why must you copy `path[:]` when recording?

---

## A12. Combination sum reuse

In combination sum (unlimited reuse), do you recurse with `i` or `i+1`? What about combination sum II?

---

## A13. N-Queens diagonals

Which two expressions identify the two diagonal families for cell `(r, c)`?

---

## A14. Activity selection key

To maximize the number of non-overlapping intervals, what do you sort by, and what is the greedy pick rule?

---

## A15. Jump Game II idea

In one sentence, how does the O(n) greedy for Jump Game II work?

---

## A16. Gas station reset

If running tank goes negative at index `i`, what do you set `start` to, and why can you discard earlier starts?

---

## A17. Greedy vs 0/1 knapsack

Why does value/weight greedy fail for 0/1 knapsack but work for fractional knapsack?

---

## A18. Tool choice

"Return all palindrome partitions of a string" vs "minimum cuts to palindrome-partition" — which tools?

---

# SECTION A — ANSWERS

### A1
State meaning; transition; base cases; fill order; answer cell (or aggregation).

### A2
`dp[r][c]` = ways to reach `(r,c)`. `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. First row/col = 1. Answer `dp[m-1][n-1]`.

### A3
You need the minimum HP **required to finish from here**; that depends on future damage. Backward DP computes "need on entry" from already-solved later cells. Forward needs unknown future slack.

### A4
**0/1 → backward** (so `dp[w - wt]` is still the previous item). **Unbounded → forward** (reuse of the same item in one pass is intended).

### A5
**Outer = coins, inner = amount forward** → combinations. Swap → counts ordered sequences (permutations), usually overcounting.

### A6
If equal: `1 + dp[i-1][j-1]`; else `max(dp[i-1][j], dp[i][j-1])`.

### A7
Delete → `dp[i-1][j]`; insert → `dp[i][j-1]`; replace → `dp[i-1][j-1]`; take `1 + min` of those.

### A8
`LPS(s) = LCS(s, reverse(s))`.

### A9
Θ(n²) intervals × Θ(n) choices of split/last index `k` → O(n³).

### A10
Reasonable when `n ≤ ~20` and state is a subset. Not when `n` is large (2ⁿ explodes) or a standard 2D DP already fits.

### A11
Choose (mutate) → explore (recurse) → unchoose (undo). Record `path[:]` so later mutations don't alter stored answers.

### A12
Unlimited: `bt(i, ...)`. Comb II (each once): `bt(i+1, ...)` after sorting + duplicate skip.

### A13
`r - c` and `r + c` (or equivalent diag indices).

### A14
Sort by **end time ascending**. Take next interval if `start >= last_end`.

### A15
Scan left→right tracking farthest reach in the current jump window; when `i` hits window end, take one jump and extend window to `farthest`.

### A16
`start = i + 1`, reset tank to 0. Any start in the failed prefix would also go negative by `i` (cumulative deficit argument).

### A17
Fractional: you can take part of an item → ratio order is optimal. 0/1: taking a high-ratio item can block a better combination of others → need DP.

### A18
All partitions → **backtracking**. Min cuts → **DP** (often with palindrome precompute).

---

# SECTION B: GRID DP + KNAPSACK

---

## B1. Unique Paths II

Obstacle grid:

```
[[0,0,0],
 [0,1,0],
 [0,0,0]]
```

How many paths? Show the DP table.

---

## B2. Minimum Path Sum

```
[[1,3,1],
 [1,5,1],
 [4,2,1]]
```

Min path sum and one optimal path.

---

## B3. Dungeon (tiny)

```
[[-2,-3,3],
 [-5,-10,1],
 [10,30,-5]]
```

Minimum initial HP? (You may cite the standard answer if you can justify the BR→TL recurrence.)

---

## B4. 0/1 Knapsack

Weights `[1,3,4,5]`, values `[1,4,5,7]`, `W=7`. Max value? Show final 1D `dp` after each item (backward).

---

## B5. Partition Equal Subset Sum

`nums = [1,5,11,5]`. Can you partition? Reduce to which target?

---

## B6. Target Sum

`nums = [1,1,1,1,1]`, `target = 3`. How many ways? Show the reduction to subset-sum count.

---

## B7. Coin Change (fewest)

`coins = [1,2,5]`, `amount = 11`. Fewest coins? Sketch `dp[0..11]`.

---

## B8. Coin Change II (combinations)

`amount = 5`, `coins = [1,2,5]`. Number of combinations? Final `dp[5]`?

---

## B9. Space optimize Unique Paths

Write O(n) space Unique Paths for `m` rows, `n` cols.

---

## B10. Identify

"You have `m` zeros and `n` ones. Each string in `strs` costs some zeros and ones. Max number of strings you can form." Which DP family?

---

# SECTION B — ANSWERS

### B1
Table:
```
1 1 1
1 0 1
1 1 2
```
Answer **2**.

### B2
Answer **7**. Path e.g. `1→3→1→1→1` (right, right, down, down) or `1→1→2→1` wait — valid min path: `1→3→1→1→1` sum 7. DP end cell 7.

### B3
Answer **7**. Recurrence: `dp[r][c] = max(1, min(down,right) - dungeon[r][c])` with end `max(1, 1 - dungeon[m-1][n-1])`, fill BR→TL.

### B4
After items (as in DP II lesson): final `dp[7] = 9` (e.g. items weight 3+4). Trace matches Part 3B worked example → **9**.

### B5
Sum 22 even → target **11**. Yes (e.g. `{11}` and `{1,5,5}`).

### B6
`P = (total + target) / 2 = (5+3)/2 = 4`. Count subsets summing to 4 from five 1's → C(5,4) = **5**.

### B7
`dp[11] = 3` (5+5+1).  
`dp ≈ [0,1,1,2,2,1,2,2,3,3,2,3]`.

### B8
**4** combinations. Final `dp[5]=4`.

### B9
```python
def uniquePaths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]
```

### B10
**2D 0/1 knapsack** (two capacities: zeros and ones). `dp[z][o]` max strings.

---

# SECTION C: SUBSEQUENCE + INTERVAL DP

---

## C1. LCS

`s = "abcde"`, `t = "ace"`. LCS length? Fill the bottom-right of the table.

---

## C2. Edit Distance

`word1 = "horse"`, `word2 = "ros"`. Distance? Name one optimal op sequence.

---

## C3. LPS

`s = "bbbab"`. LPS length?

---

## C4. Distinct Subsequences (concept)

`s = "rabbbit"`, `t = "rabbit"`. What does `dp[i][j]` mean? Why can match case add two terms?

---

## C5. LCS vs LCSubstring

On mismatch, what does each do?

---

## C6. Matrix chain (light)

Dims `[1,2,3,4]` (3 matrices 1×2, 2×3, 3×4). Min multiply cost? Show the `k` choices for multiplying all three.

---

## C7. Burst balloons idea

For `nums = [3,1,5]`, what is the padded array? What does "last burst in `(l,r)`" buy you?

---

## C8. SCS length

If LCS(s,t) = 3, `|s|=5`, `|t|=4`, shortest common supersequence length?

---

## C9. Min insertions to palindrome

`s` length `n`, LPS length `L`. Formula for min insertions?

---

## C10. Identify

"Min cost to cut a stick at given cut positions" — which DP pattern?

---

# SECTION C — ANSWERS

### C1
**3** (`"ace"`). `dp[5][3] = 3`.

### C2
**3**. e.g. replace `h→r`, delete `r`, delete `e` (or equivalent sequences).

### C3
**4** (`"bbbb"`).

### C4
`dp[i][j]` = ways to form `t[:j]` from `s[:i]`. On match: use this `s` char (`diag`) **or** skip it (`up`) → sum.

### C5
LCS: `max(up, left)`. LCSubstring: reset to **0** (and track global max on matches).

### C6
Cost `(A1A2)A3`: `1*2*3 + 1*3*4 = 6+12=18`.  
Cost `A1(A2A3)`: `2*3*4 + 1*2*4 = 24+8=32`.  
Min **18**.

### C7
`[1,3,1,5,1]`. Last burst `k` has neighbors exactly `arr[l]` and `arr[r]`; subproblems `(l,k)` and `(k,r)` independent. Answer for this instance **35**.

### C8
`5+4-3 = 6`.

### C9
`n - L`.

### C10
**Interval / partition DP** (cost of cutting a segment depends on current stick length = interval endpoints).

---

# SECTION D: BACKTRACKING

---

## D1. Subsets

Generate all subsets of `[1,2,3]` using the `start`-index template. How many?

---

## D2. Subsets II rule

`nums = [1,2,2]`. State the duplicate-skip condition.

---

## D3. Permutations

How many permutations of `[1,2,3]`? What does `used[]` prevent?

---

## D4. Combination Sum

`candidates = [2,3,6,7]`, `target = 7`. List all combinations.

---

## D5. N-Queens n=4

How many distinct solutions? What sets do you maintain?

---

## D6. Word Search

Board letter matches `word[k]` but you still return false later — what must you undo, and why?

---

## D7. Palindrome partition

List all partitions of `"aab"`.

---

## D8. Sudoku mode

Is sudoku solver enumerate-all or search-any? What does the function return on success vs dead end?

---

## D9. Complexity

Worst-case time class for generating all permutations of `n` distinct nums (output included).

---

## D10. Pruning

In combination sum with sorted candidates, when can you `break` instead of `continue`?

---

# SECTION D — ANSWERS

### D1
8 subsets: `[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]`.

### D2
After sorting: `if i > start and nums[i] == nums[i-1]: continue`.

### D3
**6**. `used[i]` prevents reusing the same index in one permutation.

### D4
`[[2,2,3],[7]]`.

### D5
**2** solutions. Sets: columns, `r-c` diags, `r+c` diags.

### D6
Restore the cell from `'#'` (or visited mark) on the way back — otherwise other paths think the cell is gone forever.

### D7
`[["a","a","b"],["aa","b"]]`.

### D8
**Search-any**. Success: `return True` up the stack. Dead end for a cell: try next digit; if none work `return False`.

### D9
**Θ(n · n!)** time to build/output all (n! perms × O(n) copy), space O(n) for recursion aside from output.

### D10
When `candidates[i] > remain` (later candidates only larger) → `break`.

---

# SECTION E: GREEDY + DECISION

---

## E1. Activity selection

Intervals `(1,4),(2,3),(3,5),(0,6),(5,7),(8,9),(5,9)`. Max non-overlapping count and one set.

---

## E2. Jump Game II

`nums = [2,3,1,1,4]`. Min jumps? Trace windows.

---

## E3. Jump Game I

`nums = [3,2,1,0,4]`. Reachable? Why?

---

## E4. Gas station

```
gas  = [1,2,3,4,5]
cost = [3,4,5,1,2]
```
Start index?

---

## E5. Huffman intuition

Why merge the two smallest frequencies first?

---

## E6. Decision

Min coins for amount with arbitrary coin set — greedy or DP? Why?

---

## E7. Decision

Max non-overlapping intervals — greedy or DP?

---

## E8. Decision

Longest increasing subsequence — greedy or DP? (Name the O(n log n) structure if you know it.)

---

## E9. Exchange sketch

In 3–4 sentences, sketch why earliest-finish activity selection is optimal.

---

## E10. Fractional vs 0/1

One sentence each: correct algorithm family.

---

# SECTION E — ANSWERS

### E1
Count **4**. e.g. `(2,3),(3,5),(5,7),(8,9)`.

### E2
**2**. At i=0 jump→cur_end=2; at i=2 jump→cur_end=4.

### E3
**False**. Farthest reach dies at index 3 (`0`); cannot pass the zero.

### E4
**3**.

### E5
Rarest symbols should sit deeper; an optimal tree can always make the two rarest siblings (exchange). Heap repeatedly merges least frequent.

### E6
**DP** (unbounded knapsack). Greedy fails on arbitrary denominations (counterexamples exist). US canonical coins happen to be canonical — don't assume.

### E7
**Greedy** (earliest end). DP possible but worse.

### E8
**DP** O(n²) classic; patience sorting / tails binary search **O(n log n)** is a greedy-ish structure for length only (not full DP table).

### E9
Take OPT. At first difference, OPT's activity finishes no earlier than greedy's earliest-finish pick. Swap OPT's activity for greedy's; remaining schedule stays feasible; count unchanged. So some OPT matches greedy step-by-step.

### E10
Fractional → greedy by ratio. 0/1 → DP.

---

# SECTION F: DEBUG THE BUG

---

## F1

```python
def knapsack_01(wt, val, W):
    dp = [0] * (W + 1)
    for i in range(len(wt)):
        for w in range(wt[i], W + 1):  # bug?
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

What does this actually compute? How do you fix for 0/1?

---

## F2

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]
```

What is wrong relative to LeetCode Coin Change II?

---

## F3

```python
def subsets(nums):
    ans = []
    path = []
    def bt(start):
        ans.append(path)  # bug?
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1)
            path.pop()
    bt(0)
    return ans
```

Symptom? Fix?

---

## F4

```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums)):  # bug?
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

What goes wrong? Fix?

---

## F5

```python
def longestCommonSubsequence(s, t):
    n, m = len(s), len(t)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m):
            if s[i] == t[j]:
                dp[i][j] = 1 + dp[i-1][j-1]  # bug?
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n-1][m-1]
```

List the indexing bugs.

---

# SECTION F — ANSWERS

### F1
Computes **unbounded** knapsack. Fix: `for w in range(W, wt[i]-1, -1)`.

### F2
Counts **permutations** (order matters). Fix: outer `for c in coins`, inner `for a in range(c, amount+1)`.

### F3
All entries in `ans` alias the same list → end up identical/`[]`. Fix: `ans.append(path[:])`.

### F4
Loop includes last index → often **extra jump** when `i` hits `n-1` as `cur_end`. Fix: `for i in range(len(nums)-1)`.

### F5
Should use `(n+1)×(m+1)` table with loops `i=1..n`, `j=1..m`, compare `s[i-1], t[j-1]`, write `dp[i][j]`, return `dp[n][m]`. As written: wrong indices, `i-1` when `i=0` wraps, answer cell wrong.

---

# SECTION G: CUMULATIVE INTEGRATION

Pulls Module 9 + earlier tools. Tag PREVIEW if beyond earned scope.

---

## G1

You need the k most frequent words. Heap or sorting? Contrast with generating all subsets of words.

---

## G2

House robber on a **line** vs **circle** vs **tree**. Which is Module 8/9 DP, which needs tree DP?

---

## G3

`minPathSum` on a grid vs Dijkstra on a grid with 4-direction moves and varying costs. When is grid DP enough?

---

## G4

Palindrome partitioning **min cuts** uses a boolean palindrome table. Is that table DP or backtracking?

---

## G5. PREVIEW — no mastery credit

Digit DP / "count numbers ≤ R with property" — name the technique only; do not solve.

---

## G6

Meeting Rooms II (min rooms) — greedy sweep/heap from Module 6, or N-Queens-style backtracking? Why?

---

## G7

Recover the actual LCS string from a filled `dp` table. Pseudocode the walk.

---

## G8

Word break: return **True/False** vs return **all sentences**. Tools?

---

# SECTION G — ANSWERS

### G1
Top-K → **heap** O(n log k) or sort. All subsets → **backtracking** exponential; different question.

### G2
Line: 1D DP (DP I). Circle: two-range DP or similar. Tree: **tree DP** (rob/not-rob per node) — Module 5 trees + DP idea.

### G3
Grid DP when moves are **DAG-like** (e.g. only right/down). General 4-dir with weights can have cycles / need Dijkstra (Module 8).

### G4
Palindrome `is_pal[i][j]` is **DP**. Min cuts is DP over prefixes. Listing partitions is **backtracking**.

### G5
**Digit DP** (PREVIEW). State often `pos, tight, ...` with memo.

### G6
**Sweep / heap** — need min resources for all intervals, not enumerate assignments. BT would be the wrong complexity class.

### G7
From `(n,m)`, while i,j > 0: if equal chars, append and `i--,j--`; else move to larger of `dp[i-1][j]` vs `dp[i][j-1]`. Reverse at end.

### G8
True/False → DP / BFS / memo DFS. All sentences → **backtracking** (with word-dict prune), optionally memoized.

---

# SECTION H: BLIND-STYLE MIXED SET

No labels. For each: name the tool in one line, then solve (approach + complexity). Answers below.

---

## H1

Given a `m×n` grid filled with non-negative costs, move only right or down. Return min cost from top-left to bottom-right.

---

## H2

Given distinct integers, return all possible permutations.

---

## H3

Given `gas` and `cost` arrays on a circular route, return the unique starting gas station index to complete the circuit, or -1.

---

## H4

Given two strings, return the length of their longest common subsequence.

---

## H5

Given an array of intervals, return the minimum number of intervals to remove to make the rest non-overlapping.

---

## H6

Given coins and amount, return the number of **combinations** that make up the amount.

---

## H7

Fill a partially completed 9×9 sudoku board in-place.

---

## H8

Given `word1` and `word2`, return the minimum number of insert/delete/replace operations to convert `word1` to `word2`.

---

## H9

Given balloons with coins, bursting `i` scores `left*nums[i]*right` with neighbors. Maximize coins.

---

## H10

Given a board and a word, return whether the word exists in the grid via adjacent cells without reuse.

---

## H11

`nums` of positive integers; assign each `+` or `-` so the expression equals `target`. Return number of ways.

---

## H12

You can jump at most `nums[i]` steps from index `i`. Return the minimum number of jumps to reach the last index (guaranteed possible).

---

# SECTION H — ANSWERS

### H1
**Grid DP (min path sum).** `dp[r][c] = grid + min(up,left)`. O(mn).

### H2
**Backtracking permutations** with `used[]`. O(n·n!).

### H3
**Greedy gas station.** Total check + reset start on negative tank. O(n).

### H4
**LCS DP.** O(nm).

### H5
**Greedy interval scheduling** — sort by end, count keep, answer `n - keep`. O(n log n).

### H6
**Unbounded knapsack count**, outer coins. O(amount · |coins|).

### H7
**Backtracking search** with row/col/box sets. Exponential with heavy prune.

### H8
**Edit distance DP.** O(nm).

### H9
**Interval DP (burst balloons)**, last-burst transition. O(n³).

### H10
**Backtracking DFS** on grid with mark/unmark. O(m·n·4^L) rough.

### H11
**0/1 subset-sum count** after `P=(total+target)/2`. O(n·P).

### H12
**Greedy Jump Game II** windows. O(n).

---

# SECTION I: TEACH-BACK (GATES G1)

Answer in plain language as if teaching a peer. No code required unless clearer.

---

## I1

Explain choose/explore/unchoose and why undo is mandatory.

---

## I2

Explain why 0/1 knapsack iterates capacity backward in 1D.

---

## I3

Give the Module 9 decision rule: backtracking vs greedy vs DP.

---

## I4

Walk through LCS on `"abc"` vs `"ac"` verbally (table highlights only).

---

## I5

Why does Jump Game I not need DP?

---

# SECTION I — ANSWERS

### I1
You mutate shared state to try a choice, recurse, then reverse the mutation so sibling branches see a clean state. Without undo, the search tree corrupts itself.

### I2
Backward ensures `dp[w - wt]` still reflects results **before** taking the current item. Forward would reuse the item (unbounded).

### I3
All/construct configurations → BT. Optimal with overlapping subproblems → DP. Optimal with provable local choice (and no counterexample) → greedy.

### I4
Match `a` → 1; `b` vs `c` mismatch → stay 1; match `c` → 2. Answer 2 (`"ac"`).

### I5
Tracking the farthest reachable index is a safe greedy invariant: if you can reach a cell, you can reach anything before it; no need to store multiple subproblem optima.

---

# SECTION J: TIMED SET BLUEPRINT (FOR G3)

Use after `drilled`. Blind, no pattern labels, 45–60 min. Pick 4–5:

| Slot | Pool |
|---|---|
| 1 | Unique Paths II / Min Path Sum |
| 2 | Coin Change or Partition Equal Subset |
| 3 | LCS or Edit Distance |
| 4 | Combination Sum or Subsets II or Word Search |
| 5 | Jump Game II or Gas Station or Non-overlapping Intervals |
| Stretch | Burst Balloons or N-Queens or Dungeon |

Log on `Metrics/Scoreboard.md`: time, first-pass Y/N, hint Y/N, error tag.

---

# PASS CRITERIA (RETENTION)

| Bar | Requirement |
|---|---|
| Section A | ≥ 16/18 correct without notes |
| Sections B–E | ≥ 80% with sound approach (minor code bugs OK if diagnosed) |
| Section F | ≥ 4/5 bugs correctly identified |
| Section H | ≥ 10/12 correct tool + approach |
| Section I | All 5 teach-backs clear (G1 signal) |

Failures → tag subskill in `Metrics/Retention Ledger.md`, re-teach weak rows of the cheat sheets, re-quiz with different instances.

---

# ONE-PAGE MODULE 9 RECALL

```
GRID:     dp from up/left (dungeon: from down/right, BR→TL)
0/1:      1D capacity BACKWARD
UNBOUNDED:1D capacity FORWARD; combos = outer coins
LCS:      match diag+1 else max(up,left)
EDIT:     match diag else 1+min(del,ins,rep)
LPS:      LCS(s,rev) or interval
INTERVAL: dp[i][j] best k; O(n³)
BT:       choose/explore/unchoose; copy path; prune
GREEDY:   earliest end / jump window / gas reset
PICK:     all→BT | overlap opt→DP | safe local→greedy
```

**Next:** Module 10 (Tries + Monotonic Stack deep) after this module reaches `complete` per Handoff gates — not after teaching alone.
