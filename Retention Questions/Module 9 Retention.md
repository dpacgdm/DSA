<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 9 Retention.keys.md -->
> **Blind mode:** Section answer blocks moved to `keys/Module 9 Retention.keys.md`.

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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


> **Answers for previous section →** `keys/Module 9 Retention.keys.md`

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
