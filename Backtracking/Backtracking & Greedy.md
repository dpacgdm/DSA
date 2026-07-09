# BACKTRACKING & GREEDY — THE COMPLETE LESSON

**Module:** 9 (DP II + Backtracking + Greedy)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Prerequisite:** Recursion (call stack, include/exclude, complexity of branching); DP I/II for the "greedy vs DP" contrast  
**Language:** Python

---

# PART 0: TWO TOOLS, ONE MODULE

| Tool | Question it answers | Output shape |
|---|---|---|
| **Backtracking** | What are *all* valid configurations? / Does *any* exist? | Enumerate or search with undo |
| **Greedy** | What is *one* optimal choice sequence, locally justified? | Single pass / sort + pick |

They sit next to DP in interviews because all three solve "decision" problems — but with different guarantees and costs.

```
Need every solution / construct board?     → Backtracking
Need optimal value with overlapping subs? → DP
Need optimal with provable local choice?  → Greedy
```

---

# PART 1: BACKTRACKING — CORE FRAMEWORK

## 1A: What Backtracking Actually Is

Backtracking = **DFS on an implicit decision tree**, with **undo** after each recursive call so the shared state is restored.

You are not "generating all arrays in memory at once." You are walking one path, recording when complete, then retreating and trying the next branch.

## 1B: The Choose / Explore / Unchoose Template

```python
def backtrack(state):
    if is_goal(state):
        record_solution(state)
        return                     # or return True if only searching for one

    for choice in choices(state):
        if not is_valid(state, choice):   # prune
            continue
        make(choice)                      # CHOOSE
        backtrack(state)                  # EXPLORE
        undo(choice)                      # UNCHOOSE
```

| Step | Meaning |
|---|---|
| **Choose** | Mutate shared state (append, place queen, mark visited) |
| **Explore** | Recurse with the choice committed |
| **Unchoose** | Reverse the mutation (`pop`, unplace, unmark) |

**Why undo matters:** Without unchoose, later branches see polluted state. The classic bug is appending to `path` and forgetting `path.pop()`.

## 1C: Search vs Enumerate

| Mode | On goal | Typical return |
|---|---|---|
| Enumerate all | Record copy of `path`, continue | `List[List[...]]` |
| Find any | `return True` and unwind | `bool` |
| Count | `ans += 1`, continue | `int` |
| Optimize | Update global best, continue (often with prune) | best score |

For enumerate: **always** store `path[:]` (a copy), never `path` itself — otherwise every recorded answer mutates together.

## 1D: Complexity Reality Check

If each position has up to `b` choices and depth `d`:

```
Time  ≤ O(b^d)     (often less with pruning)
Space = O(d)       call stack + current path
```

Pruning does **not** change worst-case big-O for many problems, but it makes the difference between TLE and AC.

## 1E: The Recursion Recipe Adapted

1. **What is a partial solution?** (path, board, index `start`)
2. **When is it complete?** (path length n, board filled, index past end)
3. **What are the choices at this step?**
4. **What makes a choice illegal?** (prune)
5. **How do I undo?**

Write those five answers in comments before coding.

---

# PART 2: CLASSIC BACKTRACKING PATTERNS

## 2A: Subsets (Include / Exclude Power Set)

**Problem:** All subsets of `nums` (unique elements).

**Decision at index `i`:** include `nums[i]` or skip it. Or equivalently: build by choosing next element with increasing index.

```python
def subsets(nums):
    ans = []
    path = []

    def bt(start):
        ans.append(path[:])          # every node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])     # choose
            bt(i + 1)                # explore (no reuse of earlier indices)
            path.pop()               # unchoose

    bt(0)
    return ans
```

### Trace — `nums = [1,2,3]`

```
bt(0) record []
  pick 1 → bt(1) record [1]
    pick 2 → bt(2) record [1,2]
      pick 3 → bt(3) record [1,2,3]
    pick 3 → bt(3) record [1,3]
  pick 2 → bt(2) record [2]
    pick 3 → bt(3) record [2,3]
  pick 3 → bt(3) record [3]
```

**2ⁿ subsets.** Recording at every node (not only leaves) is the cleanest form.

### Subsets II (duplicates)

Sort first. Skip a duplicate at the same depth:

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

This prevents `[1a,2]` and `[1b,2]` from both appearing when two `1`s exist.

## 2B: Permutations

**Problem:** All orderings of `nums`.

**State:** `path` + `used[]` boolean (or swap-in-place).

```python
def permute(nums):
    ans = []
    path = []
    used = [False] * len(nums)

    def bt():
        if len(path) == len(nums):
            ans.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            bt()
            path.pop()
            used[i] = False

    bt()
    return ans
```

### Trace — `[1,2,3]` (first levels)

```
pick 1 → pick 2 → pick 3 → [1,2,3]
       → pick 3 → pick 2 → [1,3,2]
pick 2 → ...
pick 3 → ...
```

**n! leaves.** Space O(n) for path + used.

### Permutations II (duplicates)

Sort. Skip: if `nums[i] == nums[i-1]` and `not used[i-1]`, continue — only the first identical value at this depth may start a branch.

## 2C: Combination Sum

**Problem:** Combinations from `candidates` (reusable) that sum to `target`. Order doesn't matter.

```python
def combinationSum(candidates, target):
    ans = []
    path = []

    def bt(start, remain):
        if remain == 0:
            ans.append(path[:])
            return
        if remain < 0:
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            bt(i, remain - candidates[i])   # i, not i+1 → reuse allowed
            path.pop()

    bt(0, target)
    return ans
```

| Variant | Next index | Notes |
|---|---|---|
| Combination Sum | `bt(i, ...)` | unlimited reuse |
| Combination Sum II | sort + `bt(i+1)` + skip dupes | each number once |
| Combinations (n choose k) | `bt(i+1)`, stop at `len==k` | fixed length |

### Prune early

If `candidates` sorted: `if candidates[i] > remain: break`.

## 2D: N-Queens

**Problem:** Place `n` queens so no two share row, column, or diagonal.

**State:** one queen per row `r`; track attacked columns and diagonals.

Diagonals:
- `r - c` constant (one diagonal family)
- `r + c` constant (other family)

```python
def solveNQueens(n):
    ans = []
    board = [['.'] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c

    def bt(r):
        if r == n:
            ans.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            board[r][c] = 'Q'
            cols.add(c); diag1.add(r - c); diag2.add(r + c)
            bt(r + 1)
            board[r][c] = '.'
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)

    bt(0)
    return ans
```

### Why this prunes hard

Placing row by row + set checks rejects illegal columns **before** descending. Naive "place then validate whole board" explores far more dead boards.

## 2E: Sudoku Solver

**Problem:** Fill empty cells `'.'` with digits 1–9 respecting row/col/box constraints.

**Search:** Find next empty cell; try digits; recurse; undo on failure. Return `True` when solved (search mode).

```python
def solveSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                v = board[r][c]
                rows[r].add(v); cols[c].add(v)
                boxes[(r // 3) * 3 + c // 3].add(v)

    def bt():
        for r in range(9):
            for c in range(9):
                if board[r][c] != '.':
                    continue
                b = (r // 3) * 3 + c // 3
                for ch in '123456789':
                    if ch in rows[r] or ch in cols[c] or ch in boxes[b]:
                        continue
                    board[r][c] = ch
                    rows[r].add(ch); cols[c].add(ch); boxes[b].add(ch)
                    if bt():
                        return True
                    board[r][c] = '.'
                    rows[r].remove(ch); cols[c].remove(ch); boxes[b].remove(ch)
                return False          # no digit worked
        return True                  # no empty cell left

    bt()
```

**Optimization (interview mention):** Pick the empty cell with **fewest legal candidates** (MRV heuristic) — same template, smarter choice order.

## 2F: Word Search

**Problem:** Does `word` exist as a path in a grid (4-directional, no cell reuse)?

```python
def exist(board, word):
    m, n = len(board), len(board[0])

    def bt(r, c, k):
        if k == len(word):
            return True
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return False
        tmp = board[r][c]
        board[r][c] = '#'              # mark visited
        found = (bt(r+1, c, k+1) or bt(r-1, c, k+1) or
                 bt(r, c+1, k+1) or bt(r, c-1, k+1))
        board[r][c] = tmp              # unmark
        return found

    for i in range(m):
        for j in range(n):
            if bt(i, j, 0):
                return True
    return False
```

**Pruning ideas:** Early exit if letter frequencies in board can't cover `word`; reverse `word` if last letter is rarer (optional flex).

## 2G: Palindrome Partitioning

**Problem:** Partition `s` into substrings that are all palindromes. Return all partitions.

```python
def partition(s):
    ans = []
    path = []

    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1; j -= 1
        return True

    def bt(start):
        if start == len(s):
            ans.append(path[:])
            return
        for end in range(start, len(s)):
            if is_pal(start, end):
                path.append(s[start:end+1])
                bt(end + 1)
                path.pop()

    bt(0)
    return ans
```

### Trace — `"aab"`

```
"a"|"a"|"b"
"aa"|"b"
```

**Upgrade:** Precompute `pal[i][j]` boolean DP to make `is_pal` O(1) — backtracking + DP hybrid (Module 9 synergy).

---

# PART 3: PRUNING — MAKING BACKTRACKING FAST ENOUGH

## 3A: Types of Prunes

| Prune type | Idea | Example |
|---|---|---|
| **Validity** | Choice breaks a hard constraint | Queen attacks; sudoku clash |
| **Bound** | Even best-case finish can't beat current best | Knapsack branch-and-bound |
| **Ordering** | Sort candidates so failures happen early / `break` | Combination sum sorted |
| **Symmetry** | Skip duplicate states | Subsets II / Perm II skip |
| **Feasibility** | Remaining resource insufficient | `remain < 0`; letters left |

## 3B: Pruning Template Additions

```python
for choice in ordered_choices:
    if clearly_impossible(state, choice):
        continue          # or break if monotonic
    make(choice)
    if still_promising(state):
        backtrack(state)
    undo(choice)
```

## 3C: When Backtracking Is the Wrong Tool

- You only need an **optimal count/value** and subproblems overlap heavily → **DP**
- Constraint system is 2-SAT / maxflow specialty → not classic BT
- `n` large and output size is exponential → problem may ask count via DP/math instead of listing

---

# PART 4: BACKTRACKING CHEAT SHEET

## 4A: Problem → Skeleton

| Problem | Choices | Undo | Complete when |
|---|---|---|---|
| Subsets | next index ≥ start | pop | every node (or leaf of include/exclude) |
| Permutations | unused indices | unmark + pop | `len(path)==n` |
| Comb sum | candidates from `start` | pop | `remain==0` |
| N-Queens | columns in row r | unplace + sets | `r==n` |
| Sudoku | digits in empty cell | clear cell | no empties |
| Word search | 4 neighbors | unmark `#` | `k==len(word)` |
| Pal partition | end index of next piece | pop | `start==len(s)` |

## 4B: Duplicate-Handling Rules

```
Sort the array first.
At the same depth, skip nums[i] if nums[i]==nums[i-1] and the previous
identical value was not "consumed" in the way the pattern requires:
  - Subsets II / Comb II: i > start and equal to previous
  - Perm II: equal to previous AND previous not used
```

## 4C: Interview Script

```
1. "I'll DFS with a partial path and undo."
2. State: ___  Choices: ___  Goal: ___
3. Prune: ___
4. Complexity: branching ___ depth ___ ; output size ___
5. Code template; mention copy-on-record.
6. Trace a tiny input on the whiteboard.
```

---

# PART 5: GREEDY — WHEN LOCAL = GLOBAL

## 5A: What Greedy Means

A greedy algorithm builds a solution by always taking the choice that looks best **right now**, never reconsidering.

It is correct **only** when you can justify that some optimal solution includes that local choice (or an exchange argument transforms any optimal solution into one that does).

## 5B: Exchange Argument Intuition (How to "Prove" Greedy)

Sketch used in interviews:

```
1. Take any optimal solution OPT.
2. Look at the first place OPT differs from greedy choice G.
3. Show you can swap/adjust OPT to take G's choice without worsening.
4. Therefore an optimal solution exists that matches greedy at that step.
5. Repeat → greedy is optimal.
```

You rarely write a formal proof in an interview — but you should **name** the invariant ("earliest finish time", "farthest reachable", "lowest cost merge").

## 5C: When Greedy Fails (Reach for DP)

Classic trap: **0/1 knapsack by value/weight ratio** — counterexamples exist → DP.

If you can find a small counterexample to a greedy idea, abandon it.

---

# PART 6: CLASSIC GREEDY PATTERNS

## 6A: Activity Selection / Interval Scheduling

**Problem:** Max number of non-overlapping intervals.

**Greedy choice:** Always take the interval that **finishes earliest** among remaining compatible ones.

```python
def eraseOverlapIntervals(intervals):
    # LeetCode variant: min removals = n - max non-overlapping
    intervals.sort(key=lambda x: x[1])
    end = float('-inf')
    keep = 0
    for s, e in intervals:
        if s >= end:
            keep += 1
            end = e
    return len(intervals) - keep
```

### Why earliest finish?

Frees the timeline ASAP → maximizes room for future activities. Exchange: if OPT picks a later-finishing first activity, swap for the earliest-finish one; still feasible, not worse.

### Related scheduling

| Goal | Sort key |
|---|---|
| Max count non-overlapping | End time ascending |
| Min rooms (Meeting Rooms II) | Sweep line / heap on ends — see Heaps module |
| Min arrows to burst balloons | End time, same as non-overlap count |

## 6B: Jump Game II (Min Jumps)

**Problem:** `nums[i]` = max jump length from `i`. Min jumps to last index. (Guaranteed reachable.)

**Greedy:** BFS layers without a queue — track current window's farthest reach.

```python
def jump(nums):
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

### Trace — `[2,3,1,1,4]`

```
i=0: farthest=2, i==cur_end → jump=1, cur_end=2
i=1: farthest=max(2,4)=4
i=2: farthest=4, i==cur_end → jump=2, cur_end=4
done → 2 jumps
```

**Jump Game I** (reachable?): only track `farthest`; return `farthest >= n-1`. Pure greedy, no jump count.

## 6C: Gas Station

**Problem:** Circular route. `gas[i]` fuel, `cost[i]` to go to next. Start index if unique completable circuit, else -1.

**Key facts:**
1. If `sum(gas) < sum(cost)` → impossible.
2. Otherwise unique start exists (for the classic problem).
3. Greedy: if tank goes negative at `i`, start cannot be anything in `(prev_start..i]` — reset start to `i+1`.

```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start
```

### Intuition

The prefix with the worst cumulative deficit determines the unique viable start just after it. You don't need a full simulation from every index.

## 6D: Huffman Coding (Light Intuition)

**Problem:** Build an optimal prefix-free binary code for symbol frequencies.

**Greedy:** Repeatedly merge two **least frequent** nodes; new node weight = sum. (Min-heap.)

```
Why optimal (intuition): rarest symbols end up deepest; exchange argument
says an optimal tree can always put the two rarest as siblings.
```

Interview: explain the idea + heap implementation sketch; rarely implement full codec.

```python
import heapq

def huffman_cost(freqs):
    # total weighted external path related cost demo
    h = list(freqs)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        s = a + b
        cost += s          # depends on cost definition
        heapq.heappush(h, s)
    return cost
```

## 6E: More Interval / Assignment Greedies

| Problem | Greedy idea |
|---|---|
| Assign cookies | Sort kids & cookies; smallest sufficient cookie |
| Non-overlapping / arrows | Sort by end |
| Minimum platforms / rooms | Sort starts & ends; two pointers or heap |
| Candies (ratings) | Two-pass greedy slopes |
| Boats to save people | Two pointers lightest+heaviest |
| Task scheduler cool-down | Math on max frequency (or heap sim) |

## 6F: Fractional Knapsack (Contrast with 0/1)

**Fractional** allowed → greedy by value/weight ratio is optimal.  
**0/1** → greedy ratio fails → DP.

Say this contrast out loud in interviews when knapsack appears.

---

# PART 7: GREEDY CHEAT SHEET

## 7A: Pattern Table

| Pattern | Sort / structure | Choice |
|---|---|---|
| Activity selection | End time | Take if start ≥ last end |
| Jump II | — | Extend window; jump at window end |
| Gas station | — | Reset start when tank < 0 |
| Huffman | Min-heap | Merge two smallest |
| Cookies / assign | Both arrays | Greedy smallest fit |
| Sweep intervals | Events | Track active count |

## 7B: Proof Checklist (30-second version)

1. State the greedy rule in one sentence.
2. Name the invariant ("always maximize remaining time").
3. Sketch exchange: differing OPT can adopt greedy's pick.
4. Mention a failed alternative you considered (shows judgment).

## 7C: Complexity

Usually **O(n log n)** from sorting, or **O(n)** after a linear scan, or **O(n log n)** with heap (Huffman, meeting rooms).

---

# PART 8: GREEDY VS DP — DECISION GUIDE

## 8A: Side-by-Side

| Question | Greedy | DP |
|---|---|---|
| Local choice enough? | Yes, with proof/invariant | No — need to try alternatives |
| Subproblems overlap? | Often irrelevant | Essential |
| Typical time | n log n / n | nW, n², n³, … |
| Output | One optimal structure | Optimal value (sometimes reconstruct) |
| Risk | Silent wrong answer | Slower but systematic |

## 8B: Decision Flow

```
Can I find a counterexample to my greedy idea?
  YES → DP / backtracking / other
  NO, and I have an exchange/invariant story → Greedy

Does the problem ask for ALL solutions?
  → Backtracking (not greedy/DP alone)

Is it optimal value on a grid / two strings / knapsack 0/1?
  → DP (Module 9 DP II)

Is it "reachable with jumps" / "earliest finish intervals"?
  → Greedy classics
```

## 8C: Famous Pairs (Same Story, Different Tools)

| Problem | Greedy? | DP? |
|---|---|---|
| Jump Game I | Yes (farthest) | Possible but overkill |
| Jump Game II | Yes (windows) | Also possible |
| Coin change fewest (canonical coins) | Sometimes (US coins) | Always safe DP |
| 0/1 knapsack | No | Yes |
| LCS | No | Yes |
| Activity selection | Yes | DP works but slower |
| House robber | No (adjacent constraint) | Yes 1D DP |

**Rule of thumb:** If greedy correctness isn't obvious in 60 seconds, code DP (or prove first).

---

# PART 9: BACKTRACKING VS GREEDY VS DP

```
ENUMERATE / CONSTRUCT ALL VALID
  └─ Backtracking (+ prune)

OPTIMIZE WITH OVERLAPPING SUBPROBLEMS
  └─ DP

OPTIMIZE WITH SAFE LOCAL CHOICE
  └─ Greedy

SEARCH FOR ANY VALID (constraint board)
  └─ Backtracking (return on first success)
```

Hybrid appearances:
- Palindrome partition **list all** → BT; **min cuts** → DP
- Combination sum **list** → BT; **number of combos** with coins → DP
- Meeting rooms II → greedy sweep / heap (not BT)

---

# PART 10: WORKED PROBLEMS

## Problem 1: Subsets with Duplicates

`nums = [1,2,2]` (sorted).

```
[] 
[1] [1,2] [1,2,2]
[2] [2,2]
```

Skip second `2` at the depth where first `2` wasn't chosen → avoids duplicate `[2]` from the other 2.

## Problem 2: Combination Sum

`candidates=[2,3,6,7], target=7` → `[[2,2,3],[7]]`

Reuse via `bt(i)`, not `bt(i+1)`.

## Problem 3: N-Queens n=4

Two solutions (standard). Emphasize diagonal sets in explanation.

## Problem 4: Jump Game II

`[2,3,1,1,4]` → 2 (trace in Part 6B).

## Problem 5: Gas Station

```
gas  = [1,2,3,4,5]
cost = [3,4,5,1,2]
```

Total equal. Tank fails early; start resets to index 3. Answer **3**.

## Problem 6: Activity Selection

Intervals `(1,4),(2,3),(3,5),(0,6),(5,7),(8,9),(5,9)`  
Sort by end → pick `(2,3),(3,5),(5,7),(8,9)` → count **4**.

---

# PART 11: IMPLEMENTATION PITFALLS

### Backtracking
1. Forgetting `path.pop()` / unmark visited
2. Recording `path` without copy → all answers identical
3. Wrong reuse index (`i` vs `i+1`)
4. Duplicate handling without sorting
5. Sudoku: mutating board but forgetting to restore on failure
6. Word search: forgetting to restore the `#` mark
7. Returning `False` too early in sudoku inner loops

### Greedy
1. Sorting by the wrong key (start instead of end)
2. Jump II: looping to `n` instead of `n-1` (extra jump bug)
3. Gas: forgetting total sum check
4. Assuming coin greedy works for arbitrary denominations
5. Interval inclusive/exclusive endpoint confusion (`s >= end` vs `s > end`)

---

# PART 12: PRACTICE SET

| # | Problem | Family |
|---|---|---|
| 1 | Subsets | BT |
| 2 | Subsets II | BT + dupes |
| 3 | Permutations | BT |
| 4 | Permutations II | BT + dupes |
| 5 | Combination Sum | BT |
| 6 | Combination Sum II | BT |
| 7 | N-Queens | BT |
| 8 | Sudoku Solver | BT |
| 9 | Word Search | BT |
| 10 | Palindrome Partition | BT |
| 11 | Letter Combinations of Phone | BT |
| 12 | Restore IP Addresses | BT |
| 13 | Jump Game II | Greedy |
| 14 | Gas Station | Greedy |
| 15 | Non-overlapping Intervals | Greedy |
| 16 | Minimum Number of Arrows | Greedy |
| 17 | Assign Cookies | Greedy |
| 18 | Jump Game I | Greedy |
| 19 | Task Scheduler | Greedy / math |
| 20 | Identify: greedy or DP? (mixed prompts) | Decision |

---

# PART 13: MORE BACKTRACKING PATTERNS (INTERVIEW FREQUENCY)

## 13A: Letter Combinations of a Phone Number

**Problem:** Digits `2–9` map to letters. Return all strings from digit sequence.

```python
MAP = {
    '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
    '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
}

def letterCombinations(digits):
    if not digits:
        return []
    ans = []
    path = []

    def bt(i):
        if i == len(digits):
            ans.append(''.join(path))
            return
        for ch in MAP[digits[i]]:
            path.append(ch)
            bt(i + 1)
            path.pop()

    bt(0)
    return ans
```

**Complexity:** O(4^n · n) if every digit has ≤4 letters. Same template as permutations over heterogeneous alphabets.

### Trace — `"23"`

```
a→d ae af
b→d be bf
c→d ce cf
→ ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

## 13B: Restore IP Addresses

**Problem:** Insert dots into digit string to form valid IPs (4 parts, each 0–255, no leading zero unless `0`).

```python
def restoreIpAddresses(s):
    ans = []
    path = []

    def bt(start):
        if len(path) == 4:
            if start == len(s):
                ans.append('.'.join(path))
            return
        for length in range(1, 4):
            if start + length > len(s):
                break
            piece = s[start:start + length]
            if (piece[0] == '0' and length > 1) or int(piece) > 255:
                continue
            path.append(piece)
            bt(start + length)
            path.pop()

    bt(0)
    return ans
```

### Trace — `"25525511135"`

Valid: `255.255.11.135`, `255.255.111.35`.

**Prune:** Remaining digits must fit in remaining slots (roughly `rem_slots ≤ rem_digits ≤ 3*rem_slots`).

## 13C: Generate Parentheses

**Problem:** All valid strings of `n` pairs.

**Prune:** Never place `)` if `close == open`; never place `(` if `open == n`.

```python
def generateParenthesis(n):
    ans = []
    def bt(s, open_n, close_n):
        if len(s) == 2 * n:
            ans.append(s)
            return
        if open_n < n:
            bt(s + '(', open_n + 1, close_n)
        if close_n < open_n:
            bt(s + ')', open_n, close_n + 1)
    bt('', 0, 0)
    return ans
```

Catalan-number many results — know the count is C_n, don't memorize the formula under pressure unless asked.

## 13D: Word Break II (list all sentences)

Dictionary word break that **lists** sentences = backtracking with memo of remaining suffix → list of tails (or pure BT if n small).

```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    memo = {}

    def bt(start):
        if start in memo:
            return memo[start]
        if start == len(s):
            return ['']
        res = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for tail in bt(end):
                    res.append(word + ((' ' + tail) if tail else ''))
        memo[start] = res
        return res

    return bt(0)
```

**Contrast:** Word Break I (bool) → DP/BFS. Word Break II (all) → BT + memo.

## 13E: Include/Exclude Form of Subsets (alternate)

Same power set, different tree shape:

```python
def subsets(nums):
    ans = []
    def bt(i, path):
        if i == len(nums):
            ans.append(path[:])
            return
        path.append(nums[i])   # include
        bt(i + 1, path)
        path.pop()
        bt(i + 1, path)        # exclude
    bt(0, [])
    return ans
```

Both forms are valid. The `start`-index form often extends more cleanly to combination-sum style problems.

---

# PART 14: MORE GREEDY PATTERNS (INTERVIEW FREQUENCY)

## 14A: Candies (Two-Pass)

**Problem:** Kids in a line with ratings. Give candies so higher-rated neighbor gets more than lower. Minimize total.

**Greedy:** 
1. Left→right: if `r[i] > r[i-1]`, `candies[i] = candies[i-1] + 1`
2. Right→left: if `r[i] > r[i+1]`, `candies[i] = max(candies[i], candies[i+1] + 1)`

```python
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)
```

Two local constraints → two directional passes. Classic "greedy that isn't a single sort."

## 14B: Boats to Save People

Sort weights. Pair lightest+heaviest if they fit; else heaviest alone.

```python
def numRescueBoats(people, limit):
    people.sort()
    i, j = 0, len(people) - 1
    boats = 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return boats
```

## 14C: Task Scheduler (Math / Greedy)

**Problem:** Tasks with cooldown `n` between same letters. Min time units.

**Formula intuition:** Let `f_max` be max frequency, `count_max` how many tasks share that frequency.

```
frame = (f_max - 1) * (n + 1) + count_max
answer = max(frame, len(tasks))
```

Why `max` with `len(tasks)`? If many distinct tasks fill idle slots naturally, you never idle.

Heap simulation (schedule most remaining frequently) is the constructive greedy view — see Heaps module.

## 14D: Minimum Arrows to Burst Balloons

Same as max non-overlapping **points**: sort by end; shoot at end; skip all balloons covering that point.

```python
def findMinArrowShots(points):
    points.sort(key=lambda x: x[1])
    arrows = 0
    end = float('-inf')
    for s, e in points:
        if s > end:          # note: > not >= if touching counts as overlap
            arrows += 1
            end = e
    return arrows
```

**Endpoint care:** Problem statement decides whether touching intervals overlap. Read carefully.

## 14E: Assign Cookies

Sort `g` (greed factors) and `s` (cookie sizes). Give smallest cookie that satisfies next child.

```python
def findContentChildren(g, s):
    g.sort(); s.sort()
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            i += 1
        j += 1
    return i
```

---

# PART 15: FULL WORKED TRACES (BOARD-STYLE)

## Trace A — Combination Sum II

`candidates = [10,1,2,7,6,1,5]`, `target = 8` (sorted first: `[1,1,2,5,6,7,10]`).

```
path building (skip duplicate 1 at same depth):
[1,1,6]
[1,2,5]
[1,7]
[2,6]
[1(second),7] skipped as dup of [1,7] via skip rule
...
```

Valid unique: `[[1,1,6],[1,2,5],[1,7],[2,6]]`.

## Trace B — N-Queens n=4 (first solution path)

```
Row0: try c=0 → diag/col mark → Row1 blocked many
Row0: c=1 place Q
  Row1: c=3 place Q  (c=0,2 attacked)
    Row2: c=0 place Q
      Row3: c=2 place Q → SOLUTION
        .Q..
        ...Q
        Q...
        ..Q.
```

Second solution is the mirror. Sets make illegal columns O(1) to reject.

## Trace C — Word Search `"ABCCED"`

```
Board:
A B C E
S F C S
A D E E

Start (0,0) A → (0,1) B → (0,2) C → (1,2) C → (2,2) E → (2,1) D  YES
Mark/unmark each step; failed neighbor restores `#` → letter.
```

## Trace D — Gas Station detailed

```
i:     0   1   2   3   4
gas:   1   2   3   4   5
cost:  3   4   5   1   2
diff: -2  -2  -2   3   3

tank cumulative with resets:
i=0: tank=-2 → start=1, tank=0
i=1: tank=-2 → start=2, tank=0
i=2: tank=-2 → start=3, tank=0
i=3: tank=3
i=4: tank=6
sum(diff)=0 ≥ 0 → return 3
```

## Trace E — Activity Selection

```
sorted by end:
(2,3) take end=3
(1,4) skip
(3,5) take end=5
(0,6) skip
(5,7) take end=7
(5,9) skip
(8,9) take end=9
→ 4 activities
```

---

# PART 16: DECISION DRILLS (FORCE THE CHOICE)

For each prompt, answer only: **BT / Greedy / DP / Other** and one reason.

| # | Prompt | Answer |
|---|---|---|
| 1 | All subsets of a set | BT — enumerate |
| 2 | Max value 0/1 knapsack | DP — overlap + no safe greedy |
| 3 | Max non-overlapping meetings | Greedy — earliest end |
| 4 | Min edit distance | DP — two-string table |
| 5 | Does a word exist on a grid path? | BT — search with undo |
| 6 | Min jumps (Jump Game II) | Greedy — window expand |
| 7 | Fewest coins arbitrary denominations | DP — unbounded |
| 8 | Valid N-Queens boards | BT — construct |
| 9 | LCS length | DP |
| 10 | Unique start gas station | Greedy — reset on deficit |
| 11 | Min cuts palindrome partition | DP |
| 12 | All palindrome partitions | BT |
| 13 | Fractional knapsack max value | Greedy — ratio |
| 14 | House robber line | DP — 1D |
| 15 | Schedule tasks with cooldown (min time) | Greedy/math (or heap sim) |

If you miss more than two, re-read Part 8–9 of this file and Part 7 of DP II.

---

# PART 17: COMPLEXITY CHEAT CARD

| Problem | Time (typical) | Space |
|---|---|---|
| Subsets | O(n·2ⁿ) | O(n) |
| Permutations | O(n·n!) | O(n) |
| Comb sum | exponential in target/min | O(target/min) depth |
| N-Queens | ~n! with prune | O(n) |
| Sudoku | high branching, strong prune | O(1) extra sets |
| Word search | O(mn·4^L) | O(L) |
| Activity / arrows | O(n log n) | O(1) |
| Jump II / Gas | O(n) | O(1) |
| Candies | O(n) | O(n) |
| Huffman build | O(n log n) | O(n) |

---

# PART 18: ONE-PAGE SUMMARY

```
BACKTRACKING
  choose → explore → unchoose
  copy path on record; prune hard; sort+skip for duplicates
  subsets / perms / combos / N-Queens / sudoku / word search / pal-partition
  phone letters / restore IP / parentheses / word break II

GREEDY
  local choice + exchange/invariant story
  activity by earliest end / jump windows / gas reset / Huffman merge
  candies two-pass / boats two-pointer / arrows / cookies
  fractional knapsack YES; 0/1 knapsack NO

DECISION
  all solutions → BT
  optimal + overlap → DP
  optimal + safe local → Greedy
  counterexample to greedy → abandon
```

**Mastery bar:** Write the choose/explore/unchoose template from memory; solve combination sum + N-Queens + jump game II cold; explain why 0/1 knapsack is DP not greedy; give an exchange-argument sketch for activity selection; clear the Part 16 decision table at ≥13/15.
