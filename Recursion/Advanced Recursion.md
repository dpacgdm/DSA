# RECURSION DEEP DRILLING — THE COMPLETE LESSON

---

# PART 1: WHY THIS SESSION EXISTS

Week 1 gave you the **mechanics** of recursion — the five patterns, the recipe, the complexity tools. You proved mastery on clean, textbook problems.

This session breaks you out of textbook. The goals:

1. **Recursive problems where the decomposition isn't obvious** — you must find the subproblem structure yourself
2. **Recursion + pruning** — backtracking where naive recursion is too slow without cutting branches
3. **Recursion + memoization** — the bridge to dynamic programming (Week 8-9 preview)
4. **Recursion + hashing** — integrating Week 2's hash map knowledge
5. **Complex recurrence analysis** — functions where extracting the recurrence requires real thought
6. **Knowing when NOT to use recursion** — recognizing when iteration is cleaner

---

# PART 2: BACKTRACKING WITH PRUNING

## The Problem With Naive Backtracking

Week 1's backtracking template explores ALL branches:

```python
def backtrack(state):
    if is_complete(state):
        record(state)
        return
    for choice in available_choices(state):
        make_choice(choice)
        backtrack(state)
        undo_choice(choice)
```

This works but can be astronomically slow. For many problems, **most branches lead nowhere.** Pruning cuts branches early when we can **prove** they won't lead to a valid solution.

```
WITHOUT PRUNING:           WITH PRUNING:
       *                        *
      /|\                      /|\
     * * *                    * * ✗ (cut)
    /|\ ...                  /|\ 
   * * *                    * ✗ * (cut)
  ... (explore everything)  ... (much less work)
```

## The Pruning Principle

Before recursing into a branch, ask: **"Can this branch possibly lead to a valid solution?"** If the answer is provably no, skip it.

```python
def backtrack(state):
    if is_complete(state):
        record(state)
        return
    for choice in available_choices(state):
        if not is_promising(state, choice):    # ← PRUNE
            continue
        make_choice(choice)
        backtrack(state)
        undo_choice(choice)
```

## Example: Combination Sum

Find all unique combinations of candidates that sum to target. Each number can be used **unlimited times.**

```python
def combination_sum(candidates, target):
    candidates.sort()  # Enables pruning
    result = []
    
    def backtrack(start, remaining, current):
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            # PRUNE: if this candidate exceeds remaining, all subsequent will too
            if candidates[i] > remaining:
                break
            
            current.append(candidates[i])
            backtrack(i, remaining - candidates[i], current)  # i, not i+1: reuse allowed
            current.pop()
    
    backtrack(0, target, [])
    return result
```

**The pruning:** `if candidates[i] > remaining: break`. Since candidates are sorted, once one candidate exceeds the remaining target, all larger candidates will too. We cut the entire rest of the loop — not just skip one, but **break out entirely.**

**Without pruning:** We'd recurse into branches like `[2, 2, 2, 2, 2, ...]` for target=7 with candidate 2, far past the point where the sum exceeds 7.

**With pruning:** We stop the moment the running sum would exceed the target. Massive reduction in branches.

## Example: N-Queens

Place N queens on an N×N board so no two queens attack each other (same row, column, or diagonal).

```python
def solve_n_queens(n):
    result = []
    cols = set()          # Columns under attack
    diag1 = set()         # Main diagonals (row - col)
    diag2 = set()         # Anti-diagonals (row + col)
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            # PRUNE: skip if this position is under attack
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1)
            
            # Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diag1.discard(row - col)
            diag2.discard(row + col)
    
    backtrack(0)
    return result
```

**The pruning insight:** Instead of placing all N queens and then checking validity (which would explore N^N states), we check **as we place each queen.** If column `col` or either diagonal is already attacked, we don't recurse — we skip immediately.

**Why sets for tracking attacks:** O(1) membership test. The diagonal trick: all cells on the same main diagonal have the same `row - col` value. All cells on the same anti-diagonal have the same `row + col` value.

**Complexity:** Without pruning, N^N states. With pruning, roughly N! (much better). Exact analysis is complex, but the pruning reduces the search space by orders of magnitude.

## The Pruning Decision Framework

```
╔═══════════════════════════════════════════════════════════════╗
║              COMMON PRUNING STRATEGIES                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  SORT + BREAK                                                 ║
║    Sort candidates. Break when a candidate exceeds limit.     ║
║    Works for: combination sum, subset sum, partition problems  ║
║                                                               ║
║  CONSTRAINT TRACKING                                          ║
║    Track constraints in sets/arrays. Skip invalid choices.    ║
║    Works for: N-queens, Sudoku, graph coloring                ║
║                                                               ║
║  DUPLICATE SKIPPING                                           ║
║    Sort + skip adjacent duplicates at same decision level.    ║
║    Works for: permutations/combinations with duplicates       ║
║                                                               ║
║  BOUND ESTIMATION                                             ║
║    Estimate best possible outcome of a branch.                ║
║    If best possible < current best, prune.                    ║
║    Works for: optimization problems (branch and bound)        ║
║                                                               ║
║  REMAINING CAPACITY                                           ║
║    If remaining elements can't possibly fill the requirement, ║
║    prune early.                                               ║
║    Works for: combinations of size k, partition into groups    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

# PART 3: RECURSION WITH MEMOIZATION (DP PREVIEW)

## The Overlapping Subproblems Problem

Some recursive functions solve the **same subproblem** multiple times:

```python
# Fibonacci: fib(5) calls fib(4) and fib(3)
# But fib(4) also calls fib(3)
# fib(3) is computed TWICE

fib(5)
├── fib(4)
│   ├── fib(3)     ← computed here
│   │   ├── fib(2)
│   │   └── fib(1)
│   └── fib(2)
└── fib(3)         ← and AGAIN here
    ├── fib(2)
    └── fib(1)
```

## Memoization: Cache Results

Store the result of each unique subproblem. Before computing, check the cache. If already solved, return the cached result.

```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

**Without memo:** O(2ⁿ) time, O(n) space.
**With memo:** O(n) time, O(n) space. Each value computed exactly once.

## The `@lru_cache` Decorator — Python's Built-In Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

`@lru_cache` automatically caches results based on the function arguments. `maxsize=None` means unlimited cache.

**Requirement:** All arguments must be **hashable** (since they're used as dict keys internally). Lists aren't hashable — convert to tuples.

```python
# ❌ Won't work: list is not hashable
@lru_cache(maxsize=None)
def func(arr):  # arr is a list → TypeError
    ...

# ✅ Use tuple instead
@lru_cache(maxsize=None)
def func(arr):  # arr is a tuple → works
    ...

# Call with: func(tuple(my_list))
```

## When Memoization Applies

Memoization works when:
1. **Overlapping subproblems** — the same subproblem is solved multiple times
2. **Optimal substructure** — the optimal solution contains optimal solutions to subproblems
3. **The state can be captured in hashable parameters** — you need a cache key

**How to identify overlapping subproblems:** If your recursion tree has **repeated nodes** (same function called with same arguments from different paths), memoization helps.

## Example: Climbing Stairs

How many distinct ways to climb n stairs, taking 1 or 2 steps at a time?

```python
# Without memo: O(2ⁿ)
def climb(n):
    if n <= 1:
        return 1
    return climb(n - 1) + climb(n - 2)

# With memo: O(n)
@lru_cache(maxsize=None)
def climb(n):
    if n <= 1:
        return 1
    return climb(n - 1) + climb(n - 2)
```

This is literally Fibonacci. The recursion tree is identical.

## Example: Minimum Cost Path in Grid

Given a grid of costs, find the minimum cost to travel from top-left to bottom-right, moving only right or down.

```python
@lru_cache(maxsize=None)
def min_cost(grid_tuple, row, col):
    m, n = len(grid_tuple), len(grid_tuple[0])
    
    if row == m - 1 and col == n - 1:
        return grid_tuple[row][col]
    
    if row >= m or col >= n:
        return float('inf')
    
    right = min_cost(grid_tuple, row, col + 1)
    down = min_cost(grid_tuple, row + 1, col)
    
    return grid_tuple[row][col] + min(right, down)

# Usage: convert grid to tuple of tuples for hashability
grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
grid_tuple = tuple(tuple(row) for row in grid)
result = min_cost(grid_tuple, 0, 0)
```

**Without memo:** O(2^(m+n)) — each cell branches right and down.
**With memo:** O(m × n) — each cell computed once.

**Alternative: pass grid separately, cache only on (row, col):**

```python
def min_cost_path(grid):
    m, n = len(grid), len(grid[0])
    
    @lru_cache(maxsize=None)
    def helper(row, col):
        if row == m - 1 and col == n - 1:
            return grid[row][col]
        if row >= m or col >= n:
            return float('inf')
        return grid[row][col] + min(helper(row, col + 1), helper(row + 1, col))
    
    return helper(0, 0)
```

This is cleaner — `grid` is captured in the closure, only `(row, col)` is the cache key.

## Memoization vs Tabulation (Preview)

```
MEMOIZATION (Top-Down):
  Start from the big problem, recurse to smaller ones
  Cache results as you go
  Only solves subproblems that are actually needed
  Uses recursion (call stack)

TABULATION (Bottom-Up):
  Start from smallest subproblems, build up
  Fill a table iteratively
  Solves all subproblems in order
  Uses iteration (no call stack)
```

Both are DP. We'll cover tabulation fully in Weeks 8-9. For now, memoization is the tool: take your recursive solution, add `@lru_cache`, done.

---

# PART 4: RECURSIVE STRING DECOMPOSITION

## Why This Is Hard

String problems often don't have an obvious recursive structure. The key insight: at each position, you make a **choice** about how to "consume" the string — which prefix to take, which split to make, which character to match.

## Example: Word Break

Given a string `s` and a dictionary of words, determine if `s` can be segmented into dictionary words.

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    
    @lru_cache(maxsize=None)
    def can_break(start):
        if start == len(s):
            return True
        
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if prefix in word_set and can_break(end):
                return True
        
        return False
    
    return can_break(0)
```

**The recursive structure:** At position `start`, try every possible prefix `s[start:end]`. If it's a word AND the remainder can be broken, return True.

**Without memoization:** O(2ⁿ) — at each position, binary choice to end a word or extend.
**With memoization:** O(n²) — n possible start positions, each tries up to n end positions. But slicing is O(n), so total is O(n³).

**Optimization: limit prefix length to max word length:**
```python
max_len = max(len(w) for w in word_dict)

@lru_cache(maxsize=None)
def can_break(start):
    if start == len(s):
        return True
    for end in range(start + 1, min(start + max_len + 1, len(s) + 1)):
        if s[start:end] in word_set and can_break(end):
            return True
    return False
```

## Example: Generate Parentheses

Generate all combinations of `n` pairs of well-formed parentheses.

```python
def generate_parentheses(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        
        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()
        
        if close_count < open_count:
            current.append(')')
            backtrack(current, open_count + 1, close_count + 1)
            current.pop()
    
    backtrack([], 0, 0)
    return result
```

Wait — there's a bug. Let me fix:

```python
def generate_parentheses(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        
        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()
        
        if close_count < open_count:
            current.append(')')
            backtrack(current, close_count + 1, close_count + 1)
            current.pop()
    
    backtrack([], 0, 0)
    return result
```

Hmm, that's still wrong. Let me be precise:

```python
def generate_parentheses(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        
        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()
        
        if close_count < open_count:
            current.append(')')
            backtrack(current, open_count, close_count + 1)
            current.pop()
    
    backtrack([], 0, 0)
    return result
```

**The pruning rules:**
1. Can add `(` only if `open_count < n` (haven't used all opening parens)
2. Can add `)` only if `close_count < open_count` (more opens than closes so far)

These two rules guarantee every generated string is valid. No invalid strings are ever explored.

**Complexity:** The number of valid strings is the **Catalan number** C(n) = (2n)! / ((n+1)! × n!), which is approximately 4ⁿ / (n√n). Each string has length 2n. So total work is O(n × 4ⁿ/n√n) ≈ O(4ⁿ/√n).

---

# PART 5: DIVIDE AND CONQUER ON NON-OBVIOUS PROBLEMS

## Beyond "Split in Half"

Week 1's D&C was clean: split array in half, recurse, combine. Real problems don't always split neatly.

## Example: Count Inversions

An inversion is a pair (i, j) where i < j but arr[i] > arr[j]. Count all inversions in O(n log n).

**Naive approach:** Check all pairs → O(n²).

**D&C approach:** Modified merge sort. During the merge step, when we pick an element from the right half over the left, it means that element is smaller than all remaining elements in the left half — each of those is an inversion.

```python
def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    
    merged = []
    inversions = left_inv + right_inv
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i  # All remaining left elements > right[j]
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, inversions
```

**Why `len(left) - i` inversions:** When `right[j] < left[i]`, since both halves are sorted, `right[j]` is also less than `left[i+1], left[i+2], ..., left[-1]`. That's `len(left) - i` inversions.

**Recurrence:** T(n) = 2T(n/2) + O(n) → **O(n log n).**

## Example: Closest Pair of Points

Given n points in 2D, find the pair with minimum distance.

**Naive:** Check all pairs → O(n²).

**D&C approach:**
1. Sort points by x-coordinate
2. Split into left half and right half
3. Recursively find closest pair in each half
4. Check pairs that cross the dividing line (the "strip")
5. The strip check is O(n) with a clever observation about geometry

```python
def closest_pair(points):
    points_sorted_x = sorted(points, key=lambda p: p[0])
    
    def helper(pts):
        n = len(pts)
        if n <= 3:
            return brute_force(pts)
        
        mid = n // 2
        mid_x = pts[mid][0]
        
        dl = helper(pts[:mid])
        dr = helper(pts[mid:])
        d = min(dl, dr)
        
        # Build strip: points within distance d of the dividing line
        strip = [p for p in pts if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])  # Sort strip by y
        
        # Check strip pairs (at most 6 comparisons per point)
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < d:
                d = min(d, dist(strip[i], strip[j]))
                j += 1
        
        return d
    
    return helper(points_sorted_x)

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5

def brute_force(pts):
    min_d = float('inf')
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            min_d = min(min_d, dist(pts[i], pts[j]))
    return min_d
```

**The geometric insight:** In the strip, each point needs to be compared with at most 6-7 other points (those within a d×2d rectangle). So the strip check is O(n), not O(n²).

**Recurrence:** T(n) = 2T(n/2) + O(n log n) due to strip sorting. This gives O(n log²n). Can be optimized to O(n log n) by maintaining a y-sorted list across recursive calls.

This is a classic D&C problem that shows the pattern extends beyond simple array splitting.

---

# PART 6: RECURSION + HASHING INTEGRATION

## Memoization IS Hashing

Every `@lru_cache` and every `memo = {}` is a hash map. The cache key must be hashable. The cache lookup is O(1). This is recursion + hashing working together.

## Example: Target Sum

Given an array of non-negative integers and a target, assign `+` or `-` to each number. Count ways to reach the target.

```python
def find_target_sum_ways(nums, target):
    @lru_cache(maxsize=None)
    def helper(index, current_sum):
        if index == len(nums):
            return 1 if current_sum == target else 0
        
        add = helper(index + 1, current_sum + nums[index])
        subtract = helper(index + 1, current_sum - nums[index])
        return add + subtract
    
    return helper(0, 0)
```

**Without memo:** O(2ⁿ) — binary tree of +/- choices.
**With memo:** O(n × S) where S = range of possible sums. Each (index, sum) pair computed once.

The state space is `index × current_sum`. Hashing maps each unique (index, sum) to its result.

## Example: Palindrome Partitioning

Given a string, partition it such that every substring is a palindrome. Return all such partitions.

```python
def partition(s):
    result = []
    
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if is_palindrome(substring):
                current.append(substring)
                backtrack(end, current)
                current.pop()
    
    backtrack(0, [])
    return result
```

**Optimization with memoized palindrome check:**

```python
def partition(s):
    n = len(s)
    # Precompute palindrome table using DP
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]
    
    result = []
    
    def backtrack(start, current):
        if start == n:
            result.append(current[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                current.append(s[start:end + 1])
                backtrack(end + 1, current)
                current.pop()
    
    backtrack(0, [])
    return result
```

The palindrome precomputation is O(n²) and uses the DP insight: `s[i..j]` is a palindrome iff `s[i] == s[j]` AND `s[i+1..j-1]` is a palindrome. This avoids O(n) palindrome checks during backtracking.

---

# PART 7: COMPLEX RECURRENCE ANALYSIS

## Beyond the Standard Table

Some functions don't have clean recurrences. You need to think harder.

### Type 1: Variable Branching

```python
def func(s):
    if len(s) == 0:
        return 0
    total = 0
    for i in range(1, len(s) + 1):
        total += func(s[i:])
    return total + 1
```

What's the recurrence? Let n = len(s).
- The loop calls func on strings of length n-1, n-2, ..., 0.
- Each call also does O(i) work for slicing `s[i:]`.

```
T(n) = T(n-1) + T(n-2) + ... + T(0) + O(n²)
```

The O(n²) comes from total slicing cost: (n-1) + (n-2) + ... + 0 = n(n-1)/2.

This recurrence has the property that T(n) = 2T(n-1) + O(n) (by telescoping: T(n) - T(n-1) = T(n-1) + O(n)).

Solving: T(n) = O(n × 2ⁿ).

### Type 2: Input-Dependent Branching

```python
def func(arr, target):
    if target == 0:
        return 1
    if target < 0:
        return 0
    total = 0
    for num in arr:
        total += func(arr, target - num)
    return total
```

Let k = len(arr), T = target, m = min(arr).

At each call, we branch into k children. Maximum depth = T/m (each branch reduces target by at least m).

Total nodes: up to k^(T/m).

**Time: O(k^(T/m))** without memoization.

With memoization on `target`: O(k × T) — there are T possible target values, each does k work.

### Type 3: Multi-Dimensional Recursion

```python
def func(m, n):
    if m == 0 or n == 0:
        return 1
    return func(m - 1, n) + func(m, n - 1)
```

This counts paths in a grid. Without memo: the recursion tree has depth m+n, branching factor 2.

With memo: O(m × n) — each (m, n) pair computed once.

**Recognizing the state space is crucial for complexity analysis.** The number of unique subproblems = the number of unique argument combinations.

---

# PART 8: WHEN NOT TO USE RECURSION

## Recursion Is NOT Always Better

| Situation | Better Approach | Why |
|---|---|---|
| Simple linear processing | Iteration | Cleaner, no stack overhead |
| Tail recursion in Python | Convert to loop | Python doesn't optimize tail calls |
| Deep recursion (n > 1000) | Iteration or increase limit | Stack overflow risk |
| Accumulating a simple result | Loop with accumulator | More readable |
| BFS | Iterative with queue | Recursion naturally does DFS, not BFS |

## The Conversion Decision

```
╔═══════════════════════════════════════════════════════════════╗
║              RECURSION vs ITERATION DECISION                  ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  USE RECURSION when:                                          ║
║  • Problem has tree/graph structure                           ║
║  • Multiple branching choices (backtracking)                  ║
║  • Divide and conquer                                         ║
║  • The recursive code is dramatically simpler                 ║
║                                                               ║
║  USE ITERATION when:                                          ║
║  • Linear processing (one direction)                          ║
║  • Depth could exceed ~1000                                   ║
║  • Tail recursion pattern                                     ║
║  • BFS needed (use queue)                                     ║
║  • Performance-critical inner loop                            ║
║                                                               ║
║  USE MEMOIZED RECURSION when:                                 ║
║  • Overlapping subproblems exist                              ║
║  • State space is manageable (< ~10⁷)                        ║
║  • Cleaner than tabulation for the specific problem           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

# PART 9: RECURSION COMPLEXITY ANALYSIS — THE HARD CASES

## Method: State Space Analysis

For memoized recursion, the complexity is:

```
Time = (number of unique states) × (work per state)
Space = (number of unique states) + (max recursion depth)
```

**Counting unique states:**
- One integer parameter in range [0, n]: **n+1** states
- Two integer parameters (i, j) where 0 ≤ i ≤ n, 0 ≤ j ≤ m: **(n+1)(m+1)** states
- Integer parameter + sum in range [-S, S]: **n × (2S+1)** states

**Work per state:**
- Constant work (comparison, addition): O(1)
- Loop over array of size k: O(k)
- String slicing of length up to n: O(n)

### Example Analysis

```python
@lru_cache(maxsize=None)
def func(i, j):
    if i == 0 or j == 0:
        return 0
    if grid[i][j] == 1:
        return 1 + min(func(i-1, j), func(i, j-1), func(i-1, j-1))
    return 0
```

- Unique states: i ranges [0, m], j ranges [0, n] → O(m × n) states
- Work per state: O(1) (min of three values, addition)
- **Time: O(m × n)**
- **Space: O(m × n)** for cache + O(m + n) for stack depth

---

# PART 10: TEST PROBLEMS

---

### Problem 1: Combination Sum With Unique Combinations

Given an array of **distinct** integers and a target, find all unique combinations that sum to target. Each number may be used **unlimited** times.

```
Input: candidates = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]
```

Include pruning. Explain what branches are cut and why.

---

### Problem 2: Permutations With Duplicates

Given an array that **may contain duplicates**, return all unique permutations.

```
Input: [1, 1, 2]
Output: [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
```

Explain your duplicate-skipping strategy precisely.

---

### Problem 3: Word Search

Given an m×n board of characters and a word, determine if the word exists in the grid. The word can be constructed from sequentially adjacent cells (horizontal or vertical). Each cell may be used at most once.

```
Input: 
board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]
word = "ABCCED"
Output: True
```

---

### Problem 4: Word Break (Memoized)

Given a string and a dictionary, determine if the string can be segmented into dictionary words.

```
Input: s = "leetcode", wordDict = ["leet", "code"]
Output: True

Input: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
Output: False
```

Analyze time complexity both with and without memoization.

---

### Problem 5: Generate Parentheses

Generate all combinations of `n` pairs of well-formed parentheses.

```
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

---

### Problem 6: Count Inversions (Merge Sort D&C)

Count the number of inversions in an array: pairs (i, j) where i < j but arr[i] > arr[j].

```
Input: [2, 4, 1, 3, 5]
Output: 3 (inversions: (2,1), (4,1), (4,3))
```

Show the full merge sort trace with inversion counting.

---

### Problem 7: Sudoku Solver

Write a program to solve a Sudoku puzzle. Empty cells are represented by `0`.

```
Input: 9×9 grid with some cells filled
Output: Completed valid grid
```

Use backtracking with constraint tracking (sets for rows, columns, boxes). Explain your pruning strategy.

---

### Problem 8: Recurrence Analysis Challenge

Analyze the time and space complexity of each function. Show your work.

**8a:**
```python
def func(n):
    if n <= 1:
        return 1
    return func(n - 1) + func(n - 2) + func(n - 3)
```

**8b:**
```python
def func(n, k):
    if k == 0 or k == n:
        return 1
    return func(n - 1, k - 1) + func(n - 1, k)
```
Analyze both without and with memoization.

**8c:**
```python
def func(arr, left, right):
    if left >= right:
        return 0
    mid = (left + right) // 2
    count = 0
    for i in range(left, right + 1):
        for j in range(left, right + 1):
            count += 1
    return count + func(arr, left, mid) + func(arr, mid + 1, right)
```

---

### Problem 9: Target Sum (Memoized Recursion)

Given an array of non-negative integers and a target, assign `+` or `-` to each number. Return the **number of ways** to reach the target.

```
Input: nums = [1, 1, 1, 1, 1], target = 3
Output: 5
```

Solve with memoization. State the cache key. Analyze time and space.

---

### Problem 10: The Boss — Regular Expression Matching

Implement regular expression matching with support for `.` and `*`:
- `.` matches any single character
- `*` matches zero or more of the **preceding** element

```
Input: s = "aab", p = "c*a*b"
Output: True (c* matches empty, a* matches "aa", b matches "b")

Input: s = "mississippi", p = "mis*is*p*."
Output: False
```

Use memoized recursion. Explain all cases in your recursive logic.

---

**Solve all 10. Full reasoning, traces, edge cases, complexity analysis.**

# Problem 1: Combination Sum With Unique Combinations

## Pattern Identification

**Pattern: Backtracking with Reuse (Unbounded Choice)**

Each number can be used unlimited times. At each step, we choose to either include the current candidate (and stay at the same index, allowing reuse) or skip it (move to next candidate). To avoid duplicate combinations like [2,3,2] and [2,2,3], we enforce an ordering: only consider candidates from the current index onward.

## Solution

```python
def combination_sum(candidates, target):
    candidates.sort()  # enables pruning
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            # PRUNING: if this candidate exceeds remaining, all future
            # candidates will too (array is sorted) — cut entire branch
            if candidates[i] > remaining:
                break
            
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])  # i, not i+1 (reuse)
            current.pop()

    backtrack(0, [], target)
    return result
```

## What Branches Are Cut and Why

**Pruning 1: `if candidates[i] > remaining: break`**
Since candidates are sorted, if `candidates[i]` exceeds the remaining sum, then `candidates[i+1]`, `candidates[i+2]`, etc., all exceed it too. We can break out of the entire loop, cutting all remaining branches at this level.

Without this pruning, we'd recurse into branches that can never reach sum=0, wasting work.

**Pruning 2: `start` parameter**
By passing `i` (not 0) as the start of the next recursion, we only consider candidates at index ≥ i. This prevents generating [3,2,2] when we've already generated [2,2,3]. The combinations are always built in non-decreasing order.

## Trace

```
candidates = [2, 3, 6, 7], target = 7

backtrack(0, [], 7)
├─ i=0, pick 2: backtrack(0, [2], 5)
│  ├─ i=0, pick 2: backtrack(0, [2,2], 3)
│  │  ├─ i=0, pick 2: backtrack(0, [2,2,2], 1)
│  │  │  ├─ i=0: candidates[0]=2 > 1 → BREAK (prune all)
│  │  ├─ i=1, pick 3: backtrack(1, [2,2,3], 0) → FOUND [2,2,3] ✅
│  │  ├─ i=2: candidates[2]=6 > 3 → BREAK
│  ├─ i=1, pick 3: backtrack(1, [2,3], 2)
│  │  ├─ i=1: candidates[1]=3 > 2 → BREAK
│  ├─ i=2: candidates[2]=6 > 5 → BREAK
├─ i=1, pick 3: backtrack(1, [3], 4)
│  ├─ i=1, pick 3: backtrack(1, [3,3], 1)
│  │  ├─ i=1: 3 > 1 → BREAK
│  ├─ i=2: 6 > 4 → BREAK
├─ i=2, pick 6: backtrack(2, [6], 1)
│  ├─ i=2: 6 > 1 → BREAK
├─ i=3, pick 7: backtrack(3, [7], 0) → FOUND [7] ✅

result = [[2,2,3], [7]] ✅
```

## Edge Cases

**No valid combinations:** `candidates=[2], target=3` → 2+2=4>3 with no way to hit 3 → [] ✅

**Single candidate equals target:** `candidates=[5], target=5` → [[5]] ✅

## Complexity Analysis

**Time:** In the worst case (candidates=[1], target=t), the recursion tree has depth t and explores all compositions of t. Upper bound: **O(n^(t/min_candidate))** where n = len(candidates). More precisely, the number of valid combinations can be exponential in t.

**Space:** Recursion depth = target/min_candidate (at most). Current list: same depth. Result: depends on number of combinations.
Auxiliary: **O(target/min_candidate)**

> **Time: O(n^(t/m))** where m = min candidate, **Space: O(t/m)** auxiliary

---

# Problem 2: Permutations With Duplicates

## Pattern Identification

**Pattern: Backtracking with Sort + Adjacent Duplicate Skip**

Sort the array so duplicates are adjacent. At each position, try each available element, but skip an element if it's the same as the previous one AND the previous one wasn't used in the current recursive path. This prevents generating the same permutation from different "copies" of the same value.

## Solution

```python
def permute_unique(nums):
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # DUPLICATE SKIP: if nums[i] == nums[i-1] and nums[i-1] 
            # was NOT used, skip. This means we only use duplicates
            # in left-to-right order.
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False

    backtrack([])
    return result
```

## Duplicate-Skipping Strategy Explained

Consider `nums = [1, 1, 2]` (sorted). The two 1s are at indices 0 and 1.

**The rule:** Among identical elements, we always pick them in **left-to-right index order.** If we're about to pick `nums[i]` and `nums[i-1]` is identical but NOT used, that means we're trying to pick the second copy before the first. Skip.

**Why `not used[i-1]`?**

- If `used[i-1] = True`: the previous duplicate IS in our current permutation. Using `nums[i]` too is fine — we're building a permutation that legitimately uses both copies. Like building [1₀, 1₁, 2].

- If `used[i-1] = False`: the previous duplicate is NOT in our current permutation. If we pick `nums[i]` now, we'd be choosing the second copy while skipping the first. This would produce the same permutation as choosing the first copy. Skip to avoid duplication.

## Trace

```
nums = [1, 1, 2], used = [F, F, F]

backtrack([]):
  i=0: nums[0]=1, used[0]=F → use it. used=[T,F,F]
    backtrack([1]):
      i=0: used[0]=T → skip
      i=1: nums[1]=1, nums[1]==nums[0] and not used[0]? 
           used[0]=T → condition fails → proceed! used=[T,T,F]
        backtrack([1,1]):
          i=0: used → skip
          i=1: used → skip
          i=2: use 2. → APPEND [1,1,2] ✅
      i=2: nums[2]=2, use it. used=[T,F,T]
        backtrack([1,2]):
          i=0: used → skip
          i=1: nums[1]==nums[0] and not used[0]?
               used[0]=T → condition fails → use it.
            → APPEND [1,2,1] ✅

  i=1: nums[1]=1, nums[1]==nums[0] and not used[0]?
       used[0]=F → YES → SKIP! (would duplicate i=0's branch)

  i=2: nums[2]=2, use it. used=[F,F,T]
    backtrack([2]):
      i=0: use 1. used=[T,F,T]
        backtrack([2,1]):
          i=1: nums[1]==nums[0] and not used[0]? used[0]=T → no → use it.
            → APPEND [2,1,1] ✅
      i=1: nums[1]==nums[0] and not used[0]? used[0]=F → YES → SKIP

result = [[1,1,2], [1,2,1], [2,1,1]] ✅
```

## Edge Cases

**All duplicates:** `nums=[1,1,1]` → only one permutation: [[1,1,1]] ✅

**No duplicates:** `nums=[1,2,3]` → standard 3! = 6 permutations, no skips triggered ✅

## Complexity

**Time:** At most n! permutations (fewer with duplicates). Each takes O(n) to copy. For the loop at each level, we scan n elements. Total: **O(n × n!)** worst case (all unique).

**Space:** `used` array O(n), recursion depth O(n), result O(n × n!).
Auxiliary: **O(n)**

> **Time: O(n × n!), Space: O(n)** auxiliary

---

# Problem 3: Word Search

## Pattern Identification

**Pattern: Grid Backtracking with In-Place Visited Marking**

Start DFS from every cell matching the first character. Explore all four directions. Mark visited cells to prevent reuse. Backtrack (unmark) when returning.

## Solution

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, index):
        if index == len(word):
            return True

        if (r < 0 or r >= rows or c < 0 or c >= cols 
                or board[r][c] != word[index]):
            return False

        # Mark as visited by temporarily replacing
        temp = board[r][c]
        board[r][c] = '#'

        # Explore all 4 directions
        found = (backtrack(r + 1, c, index + 1) or
                 backtrack(r - 1, c, index + 1) or
                 backtrack(r, c + 1, index + 1) or
                 backtrack(r, c - 1, index + 1))

        # Backtrack — restore the cell
        board[r][c] = temp

        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True

    return False
```

## Why In-Place Marking Instead of a Visited Set

A visited set would use O(L) space where L = word length. In-place marking (`board[r][c] = '#'`) uses O(1) extra space — we temporarily modify the board and restore it on backtrack. This is both space-efficient and faster (no hash overhead).

## Trace

```
board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]
word = "ABCCED"

Start at (0,0) = 'A' = word[0] ✓

backtrack(0,0,0): 'A'=='A' ✓, mark #
  backtrack(1,0,1): 'S'≠'B' → False
  backtrack(-1,0,1): out of bounds → False
  backtrack(0,1,1): 'B'=='B' ✓, mark #
    backtrack(1,1,2): 'F'≠'C' → False
    backtrack(-1,1,2): out of bounds → False
    backtrack(0,2,2): 'C'=='C' ✓, mark #
      backtrack(1,2,3): 'C'=='C' ✓, mark #
        backtrack(2,2,4): 'E'=='E' ✓, mark #
          backtrack(2,1,5): 'D'=='D' ✓, mark #
            backtrack(2,0,6): index 6 == len("ABCCED") → True! ✅

Path: (0,0)A → (0,1)B → (0,2)C → (1,2)C → (2,2)E → (2,1)D
```

## Edge Cases

**Single cell board, single char word:** `board=[["A"]], word="A"` → match at (0,0), index 1 == length → True ✅

**Word longer than total cells:** `board=[["A"]], word="AB"` → can't find second char → False ✅

## Complexity

**Time:** For each cell (m×n starting points), the backtracking explores up to 4 directions at each step, for up to L steps (word length). But at each step we have at most 3 new directions (can't go back where we came from). So per starting cell: O(3^L). Total: **O(m × n × 3^L)**

**Space:** Recursion depth = L (word length). In-place marking uses no extra structures. **O(L)**

> **Time: O(m × n × 3^L), Space: O(L)**

---

# Problem 4: Word Break (Memoized)

## Pattern Identification

**Pattern: Recursion with Memoization (Top-Down DP)**

At each position, try every word in the dictionary. If a word matches the current prefix, recurse on the remaining suffix. Memoize by start index to avoid recomputing.

## Solution

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    memo = {}

    def can_break(start):
        if start == len(s):
            return True

        if start in memo:
            return memo[start]

        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set and can_break(end):
                memo[start] = True
                return True

        memo[start] = False
        return False

    return can_break(0)
```

## Trace — Example 1

```
s = "leetcode", word_set = {"leet", "code"}

can_break(0):
  end=1: "l" not in dict
  end=2: "le" not in dict
  end=3: "lee" not in dict
  end=4: "leet" in dict! → can_break(4)
    end=5: "c" not in dict
    end=6: "co" not in dict
    end=7: "cod" not in dict
    end=8: "code" in dict! → can_break(8)
      start==len(s) → return True
    memo[4] = True, return True
  memo[0] = True, return True ✅
```

## Trace — Example 2

```
s = "catsandog", word_set = {"cats","dog","sand","and","cat"}

can_break(0):
  "cat" → can_break(3):
    "sand" → can_break(7):
      "og" — no match for any end → memo[7]=False
    "san" not in dict, "s" not, "sa" not, "sandog" not → memo[3]=False
  "cats" → can_break(4):
    "and" → can_break(7): memo hit → False
    "andog" not, "a" not, "an" not → memo[4]=False
  No other prefix matches → memo[0]=False, return False ✅
```

## Without vs With Memoization

**Without memoization:**

At each position, we try up to n suffixes. Each suffix can trigger another n tries. The recursion tree branches with factor up to n at each of n levels.

Recurrence: T(n) = T(n-1) + T(n-2) + ... + T(1) + T(0) + O(n)

This solves to **T(n) = O(2ⁿ).**

Worst case example: `s = "aaaaab"`, `dict = ["a", "aa", "aaa", ...]` — almost every split point looks promising, creating exponential branches that all eventually fail at the 'b'.

**With memoization:**

There are at most n unique start positions (0 to n-1). Each is computed at most once. For each start position, we iterate through at most n end positions. Each inner iteration does a substring extraction O(n) and a set lookup.

Total: n start positions × n end positions × O(n) substring = **O(n³)**

With optimization (using the max word length to limit inner loop): can improve in practice.

## Edge Cases

**Empty string:** `s=""` → start=0=len(s) → True ✅ (empty string is trivially segmented)

**Single character:** `s="a", dict=["a"]` → "a" matches, can_break(1)=True ✅

## Complexity

> **Without memo: O(2ⁿ) time**
> **With memo: O(n³) time** (n states × n transitions × O(n) substring)
> **Space: O(n)** for memo + O(n) call stack = **O(n)**

---

# Problem 5: Generate Parentheses

## Pattern Identification

**Pattern: Constrained Backtracking (Counting Resources)**

Two resources: open parens remaining and close parens remaining. At each step:
- Add `(` if open count < n
- Add `)` if close count < open count (more opens have been placed than closes)

The second rule ensures validity — we never close more than we've opened.

## Solution

```python
def generate_parentheses(n):
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append("".join(current))
            return

        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()

        if close_count < open_count:
            current.append(')')
            backtrack(current, open_count, close_count + 1)
            current.pop()

    backtrack([], 0, 0)
    return result
```

## Why `close_count < open_count` Guarantees Validity

At any point in the string being built:
- `open_count` = number of `(` placed so far
- `close_count` = number of `)` placed so far
- Difference = `open_count - close_count` = number of currently "unmatched" opens

If we allow `)` only when `close_count < open_count`, we guarantee there's always an unmatched `(` to pair with. We never have more closes than opens at any prefix → the string is always valid.

## Trace for n=3

```
backtrack([], 0, 0)
├─ open<3: add '('
│  backtrack(['('], 1, 0)
│  ├─ open<3: add '('
│  │  backtrack(['(','('], 2, 0)
│  │  ├─ open<3: add '('
│  │  │  backtrack(['(','(','('], 3, 0)
│  │  │  ├─ open=3, can't add (
│  │  │  └─ close<3: add ')'... recurse until "((()))" ✅
│  │  └─ close<2: add ')'
│  │     backtrack(['(','(',')'], 2, 1)
│  │     ├─ add '(' → ... → "(()())" ✅
│  │     └─ add ')' → ... → "(())()" ✅
│  └─ close<1: add ')'
│     backtrack(['(',')'], 1, 1)
│     ├─ add '(' → ... → "()(())" ✅
│     └─ can't add ) (close not < open)
│        ... eventually → "()()()" ✅

result = ["((()))","(()())","(())()","()(())","()()()"] ✅
```

## Edge Cases

**n=0:** `len(current)==0==2*0` immediately → [""] ✅

**n=1:** Only one possibility → ["()"] ✅

## Complexity

**Time:** The number of valid parenthesizations is the n-th **Catalan number**: C(n) = (2n)! / ((n+1)! × n!), which is approximately **O(4ⁿ / √n)**. Each result takes O(n) to construct.

Total: **O(n × 4ⁿ / √n)**

**Space:** Recursion depth = 2n. Current list = 2n. Result = O(C(n) × 2n).
Auxiliary: **O(n)**

> **Time: O(4ⁿ / √n), Space: O(n)** auxiliary

---

# Problem 6: Count Inversions (Merge Sort D&C)

## Pattern Identification

**Pattern: Divide and Conquer (Modified Merge Sort)**

An inversion (i,j) where i<j but arr[i]>arr[j] can occur in three ways relative to the midpoint:
1. Both elements in left half → counted by left recursion
2. Both in right half → counted by right recursion
3. One in left, one in right → counted during merge

The merge step counts cross-inversions: when merging two sorted halves, if we pick from the right half before exhausting the left, every remaining left element forms an inversion with the picked right element.

## Solution

```python
def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    merged, split_inv = merge_count(left, right)

    return merged, left_inv + right_inv + split_inv

def merge_count(left, right):
    result = []
    inversions = 0
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            # left[i] > right[j]: ALL remaining left elements
            # are greater than right[j] (left is sorted)
            result.append(right[j])
            inversions += len(left) - i
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result, inversions
```

## Why `inversions += len(left) - i`

When we pick `right[j]` because `left[i] > right[j]`, the left half is sorted. So `left[i], left[i+1], ..., left[end]` are ALL greater than `right[j]`. That's `len(left) - i` inversions involving `right[j]` and elements in the left half.

## Full Trace

```
arr = [2, 4, 1, 3, 5]

Split: [2, 4] and [1, 3, 5]

LEFT: count_inversions([2, 4])
  Split: [2] and [4]
  merge_count([2], [4]):
    2 ≤ 4 → pick 2. i=1.
    extend [4].
    inversions = 0
  return [2, 4], 0

RIGHT: count_inversions([1, 3, 5])
  Split: [1] and [3, 5]
  
  count_inversions([3, 5]):
    Split: [3] and [5]
    merge: 3 ≤ 5 → pick 3, pick 5. inversions=0
    return [3, 5], 0
  
  merge_count([1], [3, 5]):
    1 ≤ 3 → pick 1. i=1. extend [3,5].
    inversions = 0
  return [1, 3, 5], 0

FINAL MERGE: merge_count([2, 4], [1, 3, 5])
  i=0,j=0: left[0]=2 > right[0]=1 → pick 1
           inversions += len(left)-0 = 2. (Both 2 and 4 > 1)
           inversions = 2. j=1.
  
  i=0,j=1: left[0]=2 ≤ right[1]=3 → pick 2. i=1.
  
  i=1,j=1: left[1]=4 > right[1]=3 → pick 3
           inversions += len(left)-1 = 1. (4 > 3)
           inversions = 3. j=2.
  
  i=1,j=2: left[1]=4 ≤ right[2]=5 → pick 4. i=2.
  
  extend [5].
  
  return [1, 2, 3, 4, 5], inversions = 3

Total: 0 + 0 + 3 = 3

Inversions: (2,1), (4,1), (4,3) ✅
```

## Edge Cases

**Already sorted:** `[1,2,3]` → all merges pick from left first → 0 inversions ✅

**Reverse sorted:** `[3,2,1]` → maximum inversions = n(n-1)/2 = 3 ✅

## Complexity

Same as merge sort — the inversion counting adds O(1) per comparison.

> **Time: O(n log n), Space: O(n)**

---

# Problem 7: Sudoku Solver

## Pattern Identification

**Pattern: Constraint-Propagation Backtracking**

Try numbers 1-9 in each empty cell. Before placing, check if the number violates row, column, or 3×3 box constraints. Maintain sets for each row, column, and box for O(1) constraint checking. Backtrack when no valid number exists.

## Solution

```python
def solve_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []

    # Initialize constraint sets from given numbers
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                num = board[r][c]
                rows[r].add(num)
                cols[c].add(num)
                boxes[(r // 3) * 3 + c // 3].add(num)
            else:
                empty.append((r, c))

    def backtrack(idx):
        if idx == len(empty):
            return True  # all cells filled

        r, c = empty[idx]
        box_id = (r // 3) * 3 + c // 3

        for num in range(1, 10):
            if num in rows[r] or num in cols[c] or num in boxes[box_id]:
                continue  # constraint violation — prune

            # Place the number
            board[r][c] = num
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_id].add(num)

            if backtrack(idx + 1):
                return True

            # Backtrack — remove the number
            board[r][c] = 0
            rows[r].remove(num)
            cols[c].remove(num)
            boxes[box_id].remove(num)

        return False  # no valid number for this cell

    backtrack(0)
```

## Pruning Strategy

**Constraint sets** are the primary pruning mechanism. For each empty cell, instead of blindly trying all 9 numbers and checking the entire board for validity (O(n) per check), we check three sets in O(1). Any number already present in the cell's row, column, or box is immediately skipped.

**Pre-collecting empty cells** avoids scanning the entire board at each recursive step to find the next empty cell.

**Further optimization (not implemented but worth mentioning in interview):** Choose the empty cell with the **fewest valid candidates** first (MRV — Minimum Remaining Values heuristic). This fails faster on dead ends, pruning more branches.

## Trace (Partial — Full Trace Would Be Enormous)

```
board with some cells empty...

backtrack(0): empty[0] = (0, 2)
  row 0 has {5, 3, 7}, col 2 has {1, 9, 8, 6}, box 0 has {5, 3, 6, 9, 8}
  Valid candidates: {2, 4} (everything else is in some constraint set)
  
  Try 2: place, add to sets
    backtrack(1): empty[1] = (0, 3)
      ... recurse deeper
      ... if dead end, backtrack to here
  
  Try 4: place, add to sets
    backtrack(1): ...
```

## Edge Cases

**Already solved:** `empty = []` → backtrack(0) returns True immediately ✅

**Unsolvable:** All paths return False → backtrack(0) returns False ✅

## Complexity

**Time:** In the absolute worst case, we try 9 values in each of the 81 cells: O(9^81). But constraint pruning dramatically reduces this. In practice, the constraint sets cut branches so aggressively that most Sudoku puzzles solve in milliseconds.

Tighter bound for a puzzle with k empty cells: **O(9^k)** worst case, but practically much less due to pruning.

**Space:** 
- Constraint sets: 9 rows + 9 cols + 9 boxes, each with at most 9 elements → O(81) = **O(1)**
- Empty list: at most 81 entries → O(1)
- Recursion depth: at most 81 → O(1)

Everything is bounded by the fixed 9×9 board size.

> **Time: O(9^k)** worst case where k = empty cells, **Space: O(1)** (fixed board size)

---

# Problem 8: Recurrence Analysis Challenge

## 8a

```python
def func(n):
    if n <= 1:
        return 1
    return func(n - 1) + func(n - 2) + func(n - 3)
```

**Recurrence:** T(n) = T(n-1) + T(n-2) + T(n-3) + O(1)

This is "Tribonacci" — similar structure to Fibonacci but with three branches.

**Recursion tree:** Each node has 3 children. The tree is unbalanced (depths n-1, n-2, n-3), but the total nodes grow exponentially.

The characteristic equation is x³ = x² + x + 1. The dominant root is approximately 1.839. So:

**Time: O(1.839ⁿ) ≈ O(2ⁿ)** (exponential, slightly less than pure 2ⁿ)

More loosely: each call makes 3 calls with n reduced by at most 3, giving an upper bound of 3ⁿ. The tighter bound from the characteristic equation gives ~1.839ⁿ.

**Space:** Maximum call stack depth. The longest path is the `func(n-1)` chain: n-1, n-2, n-3, ..., 1. Depth = **O(n)**.

> **Time: O(1.839ⁿ), Space: O(n)**

---

## 8b

```python
def func(n, k):
    if k == 0 or k == n:
        return 1
    return func(n - 1, k - 1) + func(n - 1, k)
```

This computes C(n, k) — the binomial coefficient (Pascal's triangle).

**Without memoization:**

The recursion tree: each node branches into 2. The depth is n (n decreases by 1 each level). This looks like O(2ⁿ), but not all paths go to full depth — the k parameter constrains it.

The total number of distinct subproblems computed is the number of nodes in Pascal's triangle above row n, which includes many repeated computations. The total calls are actually **O(C(n, k) × some overhead)**, but more precisely, the total nodes in the recursion tree equals **O(2ⁿ)** in the worst case when k ≈ n/2.

**Time without memo: O(2ⁿ)**, **Space: O(n)** (depth)

**With memoization:**

Unique subproblems: each (n, k) pair is computed once. n ranges from 0 to n, k ranges from 0 to k. Total unique states: **O(n × k)**.

Each state does O(1) work (two lookups + addition).

**Time with memo: O(n × k)**, **Space: O(n × k)** for the memo table + O(n) stack = **O(n × k)**

> **Without memo: Time O(2ⁿ), Space O(n)**
> **With memo: Time O(n × k), Space O(n × k)**

---

## 8c

```python
def func(arr, left, right):
    if left >= right:
        return 0
    mid = (left + right) // 2
    count = 0
    for i in range(left, right + 1):
        for j in range(left, right + 1):
            count += 1
    return count + func(arr, left, mid) + func(arr, mid + 1, right)
```

**Recurrence:** The nested loops iterate over the range [left, right], which has size m = right - left + 1. The loops do m × m = m² work.

$$T(m) = T(m/2) + T(m/2) + O(m^2) = 2T(m/2) + O(m^2)$$

**Master Theorem:** a=2, b=2, f(m)=O(m²). log_b(a) = log₂(2) = 1. f(m) = O(m²) = O(m^(1+1)).

Case 3: f(m) = Ω(m^(log_b(a) + ε)) for ε=1. Check regularity: 2 × f(m/2) = 2 × (m/2)² = m²/2 ≤ c × m² for c=1/2. ✓

**T(m) = O(f(m)) = O(m²).**

Wait, let me verify with recursion tree:

```
Level 0: 1 problem of size m → m² work
Level 1: 2 problems of size m/2 → 2(m/2)² = m²/2
Level 2: 4 problems of size m/4 → 4(m/4)² = m²/4
...
Level k: 2^k problems → m²/2^k
```

Total: m²(1 + 1/2 + 1/4 + ...) = m² × 2 = **O(m²)** where m = n (initial range).

The geometric series converges — the root dominates.

**Space:** Recursion depth = log m. Each frame O(1). **O(log m).**

> **Time: O(n²), Space: O(log n)** where n = array length

---

# Problem 9: Target Sum (Memoized)

## Pattern Identification

**Pattern: Memoized Recursion (Subset Decision)**

At each element, choose + or -. Recurse with updated running sum. Memoize by (index, current_sum) to avoid recomputation.

## Solution

```python
def find_target_sum_ways(nums, target):
    memo = {}

    def backtrack(index, current_sum):
        if index == len(nums):
            return 1 if current_sum == target else 0

        if (index, current_sum) in memo:
            return memo[(index, current_sum)]

        # Two choices: add or subtract
        add = backtrack(index + 1, current_sum + nums[index])
        sub = backtrack(index + 1, current_sum - nums[index])

        memo[(index, current_sum)] = add + sub
        return add + sub

    return backtrack(0, 0)
```

## Cache Key

**(index, current_sum)** — the index tells us which elements remain to be decided, and current_sum tells us what we need to reach. Two calls with the same (index, current_sum) will always return the same count, regardless of how they got there.

## Trace

```
nums = [1, 1, 1, 1, 1], target = 3

backtrack(0, 0)
├─ +1: backtrack(1, 1)
│  ├─ +1: backtrack(2, 2)
│  │  ├─ +1: backtrack(3, 3)
│  │  │  ├─ +1: backtrack(4, 4)
│  │  │  │  ├─ +1: bt(5, 5) → 5≠3 → 0
│  │  │  │  └─ -1: bt(5, 3) → 3==3 → 1 ✓
│  │  │  │  return 1
│  │  │  └─ -1: backtrack(4, 2)
│  │  │     ├─ +1: bt(5, 3) → 1 ✓
│  │  │     └─ -1: bt(5, 1) → 0
│  │  │     return 1
│  │  │  return 2
│  │  └─ -1: backtrack(3, 1)
│  │     ├─ +1: bt(4, 2) → memo hit → 1
│  │     └─ -1: bt(4, 0) → ... → 0
│  │     return 1
│  │  return 3
│  └─ -1: backtrack(2, 0)
│     ... (builds symmetrically)
│     return 2
│  return 5
└─ -1: backtrack(1, -1)
   ... return 0 (can't reach 3 from sum=-1 with four 1s)

Total: 5 ✅

The 5 ways: +1+1+1+1-1, +1+1+1-1+1, +1+1-1+1+1, +1-1+1+1+1, -1+1+1+1+1
```

## Edge Cases

**All zeros:** `nums=[0,0,0], target=0` → every combination sums to 0 → 2³ = 8 ways ✅

**Impossible target:** `nums=[1,1], target=5` → max sum is 2 → 0 ways ✅

## Complexity

**Without memo:** Binary tree of depth n → **O(2ⁿ)**

**With memo:**
- Index ranges: 0 to n → n+1 values
- current_sum ranges: -S to +S where S = sum(nums)
- Total unique states: O(n × S) where S = sum of all elements
- Each state does O(1) work

**Time: O(n × S)**, **Space: O(n × S)** for memo + O(n) stack

> **Time: O(n × S), Space: O(n × S)** where S = sum(nums)

---

# Problem 10: Regular Expression Matching

## Pattern Identification

**Pattern: Memoized Recursion with Case Analysis**

Compare character by character. The tricky part is `*`, which refers to the preceding element and can match zero or more. We need to handle all cases recursively and memoize by position pair (i, j).

## Solution

```python
def is_match(s, p):
    memo = {}

    def dp(i, j):
        """Does s[i:] match p[j:]?"""
        if (i, j) in memo:
            return memo[(i, j)]

        # Base case: pattern exhausted
        if j == len(p):
            result = (i == len(s))  # match only if string also exhausted
            memo[(i, j)] = result
            return result

        # Check if current characters match
        first_match = (i < len(s) and (p[j] == s[i] or p[j] == '.'))

        # Case: next character is '*'
        if j + 1 < len(p) and p[j + 1] == '*':
            # Option 1: '*' matches ZERO occurrences — skip pattern pair
            # Option 2: '*' matches ONE occurrence — consume s[i], keep pattern
            result = (dp(i, j + 2) or                          # zero matches
                     (first_match and dp(i + 1, j)))           # one+ matches
        else:
            # No '*': current chars must match, advance both
            result = first_match and dp(i + 1, j + 1)

        memo[(i, j)] = result
        return result

    return dp(0, 0)
```

## All Cases in Recursive Logic

**Case 1: Pattern exhausted (`j == len(p)`)**
Return True only if string is also exhausted. If there's remaining string with no pattern to match → False.

**Case 2: Next pattern char is `*` (`p[j+1] == '*'`)**
The `*` means "zero or more of `p[j]`." Two sub-options:
- **Zero occurrences:** Skip `p[j]` and `*` entirely → `dp(i, j+2)`. The pattern character matched nothing.
- **One or more occurrences:** Current characters must match (`first_match`), then consume `s[i]` but keep the pattern at `j` (the `*` can match more) → `dp(i+1, j)`.

The "one or more" path handles multiple matches naturally through recursion: dp(i+1, j) will again check if s[i+1] matches p[j], and if so, can consume another character, etc.

**Case 3: Next pattern char is NOT `*`**
Simple: current characters must match, then advance both pointers → `dp(i+1, j+1)`.

**`first_match` logic:** `p[j]` matches `s[i]` if they're equal OR if `p[j]` is `.` (wildcard). Also must check `i < len(s)` to avoid index out of bounds.

## Trace — Example 1

```
s = "aab", p = "c*a*b"

dp(0, 0): p[0]='c', p[1]='*' → star case
  first_match: s[0]='a' vs p[0]='c' → False
  Zero: dp(0, 2)  |  One+: first_match=False → False
  
  dp(0, 2): p[2]='a', p[3]='*' → star case
    first_match: s[0]='a' vs p[2]='a' → True
    Zero: dp(0, 4)  |  One+: dp(1, 2)
    
    dp(0, 4): p[4]='b', no star
      first_match: s[0]='a' vs p[4]='b' → False → return False
    
    dp(1, 2): p[2]='a', p[3]='*' → star case
      first_match: s[1]='a' vs p[2]='a' → True
      Zero: dp(1, 4)  |  One+: dp(2, 2)
      
      dp(1, 4): p[4]='b', no star
        first_match: s[1]='a' vs 'b' → False → return False
      
      dp(2, 2): p[2]='a', p[3]='*' → star case
        first_match: s[2]='b' vs p[2]='a' → False
        Zero: dp(2, 4)  |  One+: False
        
        dp(2, 4): p[4]='b', no star
          first_match: s[2]='b' vs 'b' → True
          dp(3, 5): j=5==len(p), i=3==len(s) → True! ✅
        
        return True
      return True
    return True
  return True

return True ✅
```

## Trace — Example 2

```
s = "mississippi", p = "mis*is*p*."

dp(0, 0): p[0]='m', no star after
  first_match: 'm'=='m' → True → dp(1, 1)

dp(1, 1): p[1]='i', no star → dp(2, 2)

dp(2, 2): p[2]='s', p[3]='*' → star case
  first_match: s[2]='s'=='s' → True
  Zero: dp(2, 4) | One+: dp(3, 2)
  
  This branches extensively...
  Eventually all paths fail because the pattern can't match 
  the final "ippi" — the p[7]='p', p[8]='*' can match some p's
  but p[9]='.' matches only one char, leaving unmatched characters.

return False ✅
```

## Edge Cases

**Empty string, empty pattern:** `s="", p=""` → dp(0,0): j==0==len(p), i==0==len(s) → True ✅

**Empty string, star pattern:** `s="", p="a*"` → dp(0,0): star case, zero matches → dp(0,2): j=2==len(p), i=0==len(s) → True ✅

**Dot matches any:** `s="ab", p=".."` → dp(0,0): .==a → dp(1,1): .==b → dp(2,2): both exhausted → True ✅

## Complexity

**States:** i ranges 0 to len(s), j ranges 0 to len(p). Total: **(len(s)+1) × (len(p)+1)** unique states.

Each state does O(1) work (just comparisons and recursive calls that hit memo).

**Time: O(s × p)** where s=len(s), p=len(p)

**Space:** Memo table: O(s × p). Call stack: O(s + p) maximum depth.

> **Time: O(s × p), Space: O(s × p)**

