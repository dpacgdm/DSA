# Answer Key — Module 9 Retention.md

**Source questions:** `Retention Questions/Module 9 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

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


