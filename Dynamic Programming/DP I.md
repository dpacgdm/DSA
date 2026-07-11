# DYNAMIC PROGRAMMING I — INTRO TO 1D DP

**Module:** 8 (Graphs II + DP I)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Recursion (call stack, memoization preview), Arrays, basic complexity.  
**Companion:** `Graphs/Graphs II.md`  
**Deferred to DP II:** 2D grids, knapsack family depth, LCS/edit distance, interval DP, digit DP.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHY DP EXISTS

## The Two Conditions

Dynamic Programming is not a data structure. It is a **method** for solving problems that have:

### 1. Overlapping Subproblems

The naive recursion recomputes the **same** smaller problem many times.

```
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   └── fib(1)
│   └── fib(2)
└── fib(3)          ← fib(3) and fib(2) computed again
    ├── fib(2)
    └── fib(1)
```

Without caching: exponential blow-up.  
With caching (or building bottom-up): each distinct subproblem once.

### 2. Optimal Substructure

An optimal solution to the full problem can be built from optimal solutions to subproblems.

Example: shortest path to `t` through `u` uses a shortest path to `u` (non-negative / appropriately defined).  
Counterexample (no optimal substructure for "longest simple path"): longest path to `u` plus an edge may create cycles / invalidate — that's why longest simple path is hard, not classic DP.

**Both required.** Overlap alone → memoize for speed. Optimal substructure → compose answers correctly. Together → DP.

---

## The Recursion Module Connection

You already saw this in Recursion:

| Recursion lesson | DP name |
|---|---|
| Fibonacci tree blow-up | Overlapping subproblems |
| `memo={}` dict cache | **Memoization** (top-down DP) |
| "Compute smaller first" | **Tabulation** (bottom-up DP) |
| Base case | DP base cases |
| Combination step | Transition |

**DP is recursion with a guarantee you never recompute, plus a habit of naming state explicitly.**

Mental model upgrade:

```
Recursion:  "trust the smaller call"
DP:         "name every smaller call as a state; store its answer; define how states depend"
```

---

## Real-World Intuition

Climbing stairs: ways to reach step `n` = ways to reach `n-1` (then +1) + ways to reach `n-2` (then +2).  
You don't recount ways to reach step 10 every time you think about step 12 — you **reuse** the number.

Same idea as filling a spreadsheet where each cell's formula references earlier cells — that's tabulation.

---

# PART 2: THE DP FRAMEWORK (MEMORIZE COLD)

Every DP solution is five decisions. Write them **before** code.

```
1. STATE      — What does dp[...] mean? What parameters uniquely identify a subproblem?
2. TRANSITION — How do you compute dp[state] from smaller states?
3. BASE       — What are the answers for the smallest states? (no dependency)
4. ORDER      — In what order must you fill so dependencies exist? (tabulation)
                Or: recursion order naturally goes to base (memoization)
5. ANSWER     — Which state(s) hold the final answer?
```

### Worked micro-example: Climbing Stairs

```
STATE:      dp[i] = number of distinct ways to climb i stairs (1 or 2 at a time)
TRANSITION: dp[i] = dp[i-1] + dp[i-2]
BASE:       dp[0]=1 (one way to stay at ground — empty climb), dp[1]=1
            (or dp[1]=1, dp[2]=2 and start loop at 3)
ORDER:      i = 2,3,...,n  (increasing)
ANSWER:     dp[n]
```

If you cannot fill these five lines, you do not yet understand the problem in DP terms — keep refining state.

---

## State Design Rules

1. **State must be sufficient** — from `dp[state]` alone + transition, you can finish.
2. **State must be minimal** — extra dimensions explode time/space.
3. **Ask:** "If I knew the answer for all strictly smaller instances, how do I get this one?"

Common 1D state shapes:

| Shape | Meaning |
|---|---|
| `dp[i]` | best / ways using prefix `nums[0..i]` or ending at `i` |
| `dp[i]` | best / ways to make amount `i` |
| `dp[i]` | answer for length `i` or index `i` |

**Ending at i vs using first i:** say it out loud. Off-by-one lives here.

---

# PART 3: MEMOIZATION VS TABULATION

## Memoization (Top-Down)

Write the natural recursive function. Cache results.

```python
def climb(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return 1
    memo[n] = climb(n - 1, memo) + climb(n - 2, memo)
    return memo[n]
```

Better — avoid mutable default:

```python
def climb_stairs(n):
    memo = {}
    def dp(i):
        if i <= 1:
            return 1
        if i in memo:
            return memo[i]
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]
    return dp(n)
```

**Pros:** Only visits needed states; easy when transition is recursive-shaped.  
**Cons:** Recursion depth (Python default ~1000); overhead of call stack; harder to see order.

## Tabulation (Bottom-Up)

Create array/table. Fill from base upward.

```python
def climb_stairs(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**Pros:** No stack overflow; clear complexity; easy space optimization.  
**Cons:** Must get iteration order right; may compute unused states.

## Equivalence

Same recurrence. Same asymptotics usually. Interview: either is fine if correct; mention both.

| | Memoization | Tabulation |
|---|---|---|
| Direction | Top-down | Bottom-up |
| Storage | Hash map / array on demand | Array / table full |
| Order | Implicit via recursion | Explicit loop |
| Space opt | Harder | Natural rolling vars |

---

# PART 4: 1D CLASSICS

---

## Classic 1: Climbing Stairs

**Problem:** `n` stairs; 1 or 2 steps. Ways to reach top?

### Framework

```
STATE:      dp[i] = ways to reach i
TRANSITION: dp[i] = dp[i-1] + dp[i-2]
BASE:       dp[0]=1, dp[1]=1
ANSWER:     dp[n]
```

### Code (space-optimized)

```python
def climb_stairs(n):
    if n <= 1:
        return 1
    a, b = 1, 1  # dp[0], dp[1]
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Trace n=5

```
i=2: a,b = 1, 2
i=3: a,b = 2, 3
i=4: a,b = 3, 5
i=5: a,b = 5, 8
→ 8 ways
```

### Complexity

Time O(n), Space O(1).

---

## Classic 2: House Robber

**Problem:** nums[i] = money in house i. Cannot rob adjacent houses. Max money.

### Framework

```
STATE:      dp[i] = max money robbing from houses 0..i
TRANSITION: dp[i] = max(dp[i-1],          # skip house i
                        dp[i-2] + nums[i]) # rob house i
BASE:       dp[0] = nums[0]
            dp[1] = max(nums[0], nums[1])
ANSWER:     dp[n-1]
```

**Alternative state:** `dp[i]` = max money with the robber **ending** at i (must rob i). Then answer = max over all i. Same family.

### Code

```python
def rob(nums):
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, n):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1
```

### Trace

```
nums = [2, 7, 9, 3, 1]

i=0: prev2=2
i=1: prev1=max(2,7)=7
i=2: max(7, 2+9)=11  → prev2,prev1 = 7, 11
i=3: max(11, 7+3)=11 → 11, 11
i=4: max(11, 11+1)=12 → 11, 12

Answer 12 (2+9+1 or 7+3+1? 7+3+1=11; 2+9+1=12 ✓)
```

### Edge Cases

Empty; single house; all zeros; decreasing values (always skip wisely).

### Complexity

O(n) time, O(1) space.

---

## Classic 3: Decode Ways

**Problem:** Digits string; map `1→A` … `26→Z`. Number of ways to decode. Leading zeros invalid.

### Framework

```
STATE:      dp[i] = ways to decode s[:i]  (prefix of length i)
TRANSITION: dp[i] = 0
            if s[i-1] != '0':                 # single digit
                dp[i] += dp[i-1]
            if i >= 2 and 10 <= int(s[i-2:i]) <= 26:  # two digit
                dp[i] += dp[i-2]
BASE:       dp[0] = 1  # empty string one way
ANSWER:     dp[n]
```

### Code

```python
def num_decodings(s):
    n = len(s)
    if not s:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        two = int(s[i - 2:i])
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
    return dp[n]
```

### Trace

```
s = "226"
dp[0]=1
dp[1]=1  ("2")
i=2 "22": single ok → +dp[1]; two=22 ok → +dp[0] → dp[2]=2
i=3 "226": single ok → +dp[2]; two=26 ok → +dp[1] → dp[3]=3

Ways: 2|2|6, 22|6, 2|26
```

### Trap

`"06"` → 0 ways. `"10"` → 1 way (`J`, not `1`+`0`). `"27"` two-digit invalid; singles may still work.

### Complexity

O(n) time, O(n) or O(1) space with rolling vars.

---

## Classic 4: Coin Change (Min Coins)

**Problem:** coins of given denominations; amount. Fewest coins to make amount (unlimited each). −1 if impossible.

### Framework

```
STATE:      dp[a] = fewest coins to make amount a
TRANSITION: dp[a] = min(dp[a - coin] + 1) over coins where coin <= a
BASE:       dp[0] = 0; else init ∞
ANSWER:     dp[amount] or -1 if ∞
```

### Code

```python
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

### Trace

```
coins = [1, 2, 5], amount = 11

dp[0]=0
dp[1]=1 (1)
dp[2]=1 (2)
dp[3]=2 (2+1)
dp[4]=2 (2+2)
dp[5]=1 (5)
...
dp[10]=2 (5+5)
dp[11]=3 (5+5+1)

Answer 3
```

### Order Note

Outer amount, inner coins → **unbounded** knapsack style (reuse coin).  
(Coin change **combinations count** needs careful loop order — see variants; min-coins as above is standard.)

### Complexity

O(amount * |coins|) time, O(amount) space.

---

## Classic 5: Word Break

**Problem:** string `s`, wordDict. Can `s` be segmented into dict words (reuse allowed)?

### Framework

```
STATE:      dp[i] = True iff s[:i] can be segmented
TRANSITION: dp[i] = True if exists j < i with dp[j] and s[j:i] in wordSet
BASE:       dp[0] = True
ANSWER:     dp[n]
```

### Code

```python
def word_break(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

Optimize: only try `j` where `i-j` ≤ max word length.

### Trace

```
s = "leetcode", wordDict = ["leet","code"]

dp[0]=T
i=4: s[0:4]="leet" in set, dp[0] → dp[4]=T
i=8: s[4:8]="code" in set, dp[4] → dp[8]=T
→ True
```

### Complexity

O(n² * L) naive string slices; with set lookups average better. Space O(n).

---

## Classic 6: Longest Increasing Subsequence (LIS)

**Problem:** length of longest strictly increasing subsequence (not necessarily contiguous).

### Approach A — Classic DP O(n²)

```
STATE:      dp[i] = LIS length ending at index i
TRANSITION: dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i], default 0)
BASE:       dp[i] = 1 for all i
ANSWER:     max(dp)
```

```python
def length_of_lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0
```

### Trace O(n²)

```
nums = [10, 9, 2, 5, 3, 7, 101, 18]

i=0: 10 → 1
i=1: 9 → 1
i=2: 2 → 1
i=3: 5 → 2 (2,5)
i=4: 3 → 2 (2,3)
i=5: 7 → 3 (2,5,7) or (2,3,7)
i=6: 101 → 4
i=7: 18 → 4 (2,5,7,18)

Answer 4
```

### Approach B — Patience Sorting / Tails O(n log n)

Maintain `tails[k]` = smallest tail of all increasing subsequences of length `k+1`.

For each `x`: binary search first tail ≥ `x`; replace (or append).

```python
import bisect

def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

### Trace patience

```
10 → [10]
9  → [9]
2  → [2]
5  → [2,5]
3  → [2,3]
7  → [2,3,7]
101→ [2,3,7,101]
18 → [2,3,7,18]

len=4
```

**Interview:** Know O(n²) cold; mention O(n log n) patience as optimization. Reconstructing the actual subsequence needs parent pointers (extra work).

---

## Classic 7: Jumping Game

### Jump Game I — Can reach last index?

Greedy is optimal (max reach). DP formulation still teaches state:

```
STATE:      dp[i] = True iff index i reachable from 0
TRANSITION: dp[i] = any(dp[j] and j + nums[j] >= i for j < i)
BASE:       dp[0] = True
ANSWER:     dp[n-1]
```

O(n²) DP; **prefer greedy O(n)**:

```python
def can_jump(nums):
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + jump)
    return True
```

### Jump Game II — Min jumps to last index

```
STATE:      dp[i] = min jumps to reach i
TRANSITION: dp[i] = min(dp[j]+1 for j < i if j+nums[j] >= i)
BASE:       dp[0]=0; else ∞
```

O(n²) DP; interview often wants O(n) BFS/greedy levels.

```python
def jump(nums):
    n = len(nums)
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i):
            if j + nums[j] >= i:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[-1]
```

### Trace Jump II DP

```
nums = [2,3,1,1,4]
dp[0]=0
dp[1]=1 (from 0)
dp[2]=1 (from 0)
dp[3]=2 (from 1)
dp[4]=2 (from 1: 1+3>=4)

Answer 2
```

**Teaching point:** DP gives correctness baseline; greedy/BFS may be the intended optimal solution — say both in interview.

---

# PART 5: SPACE OPTIMIZATION PATTERNS

## Pattern S1: Rolling Variables

If `dp[i]` depends only on `dp[i-1]` and `dp[i-2]`:

```python
# instead of array
prev2, prev1 = base0, base1
for i in range(2, n+1):
    prev2, prev1 = prev1, f(prev1, prev2)
```

Used in: climb stairs, house robber, fibonacci, decode ways (careful with two prev).

## Pattern S2: Rolling Array (1D overwrite)

For unbounded coin / knapsack-like:

```python
# dp[a] uses smaller amounts — iterate a ascending for unbounded
for c in coins:
    for a in range(c, amount + 1):
        dp[a] = min(dp[a], dp[a - c] + 1)
```

**0/1 knapsack** (each item once) → iterate capacity **descending** so you don't reuse. Deferred deep dive to DP II; know the slogan now.

## Pattern S3: When NOT to optimize

If you need the full table for reconstruction (print path / which coins), keep the array. Optimize only after correctness.

---

# PART 6: HOW TO RECOGNIZE DP IN INTERVIEWS

## Cue Phrases

| Cue | Likely |
|---|---|
| "number of ways" | DP counting |
| "minimum / maximum cost" with overlapping choices | DP optimization |
| "can you reach / segment / decode" | Boolean DP |
| "longest / shortest subsequence" (not substring) | DP (or patience for LIS) |
| Exhaustive recursion with reuse of subanswers | Memoize → DP |

## Decision Tree

```
Can I define subproblems with optimal substructure + overlap?
├── NO → greedy / graph / other
└── YES
     ├── Natural recursion clear → memoization
     └── Clear order on array → tabulation
          └── Depends on O(1) prior cells → space optimize
```

## Common Mistakes

1. Wrong state (missing a parameter — e.g. last house robbed or not)  
2. Wrong base cases (especially decode ways zeros)  
3. Off-by-one on prefix length vs index  
4. Iterating in an order that uses uncomputed states  
5. Confusing subsequence vs subarray  
6. Using DP when greedy is enough (jump game I) — still OK if you explain

---

# PART 7: FULL TRACES — SIDE-BY-SIDE MEMO VS TABLE

## Example: House Robber Top-Down

```python
def rob(nums):
    memo = {}
    def dp(i):
        """max from houses i..n-1"""
        if i >= len(nums):
            return 0
        if i in memo:
            return memo[i]
        memo[i] = max(dp(i + 1), nums[i] + dp(i + 2))
        return memo[i]
    return dp(0)
```

```
nums = [2,7,9,3,1]
dp(0) = max(dp(1), 2+dp(2))
dp(1) = max(dp(2), 7+dp(3))
dp(2) = max(dp(3), 9+dp(4))
dp(3) = max(dp(4), 3+dp(5))
dp(4) = max(dp(5), 1+dp(6)) = max(0,1)=1
dp(5)=0
dp(3)=max(1, 3+0)=3
dp(2)=max(3, 9+1)=10
dp(1)=max(10, 7+3)=10
dp(0)=max(10, 2+10)=12
```

Same answer as bottom-up. State here is "suffix starting at i" — equally valid.

---

# PART 8: CONSOLIDATED CHEAT SHEETS

## Five-Line Template

```
STATE:
TRANSITION:
BASE:
ORDER:
ANSWER:
```

## Classic Recurrences

| Problem | Recurrence (sketch) |
|---|---|
| Climb stairs | `f(i)=f(i-1)+f(i-2)` |
| House robber | `f(i)=max(f(i-1), f(i-2)+a[i])` |
| Decode ways | singles + valid doubles |
| Coin change min | `f(a)=min(f(a-c)+1)` |
| Word break | `f(i)=∃j: f(j)∧s[j:i]∈dict` |
| LIS | `f(i)=1+max{f(j): j<i, a[j]<a[i]}` |
| Jump I | reachable OR greedy reach |
| Jump II | `f(i)=min f(j)+1` over j that reach i |

## Complexity Snapshot

| Problem | Time | Space (opt) |
|---|---|---|
| Climb / Robber / Decode | O(n) | O(1) |
| Coin change | O(amount · k) | O(amount) |
| Word break | O(n²) | O(n) |
| LIS DP | O(n²) | O(n) |
| LIS patience | O(n log n) | O(n) |
| Jump I greedy | O(n) | O(1) |
| Jump II DP | O(n²) | O(n) |

## Memo vs Tabulation

| Prefer memo when | Prefer tabulation when |
|---|---|
| Sparse state space | Dense 1D/2D natural |
| Recursion is obvious | Need tight loops / space roll |
| Hard to find order | Order is obvious left→right |

## Space Opt Rules

```
Depends on last 2 → two variables
Unbounded knapsack 1D → forward iterate
0/1 knapsack 1D → backward iterate (DP II)
```

---

# PART 9: WORKED PROBLEMS WITH TRACES

---

# Problem 1: Climbing Stairs

Covered in Classic 1. Variants: 1..k steps → `dp[i]=sum(dp[i-j] for j=1..k if i-j>=0)`.

---

# Problem 2: House Robber II (Circular)

**Twist:** First and last adjacent.

```python
def rob_circular(nums):
    if len(nums) == 1:
        return nums[0]
    def rob_linear(arr):
        prev2 = prev1 = 0
        for x in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Trace

```
[2,3,2]
rob[2,3]=3; rob[3,2]=3 → 3
[1,2,3,1]
rob[1,2,3]=3; rob[2,3,1]=4 → 4
```

---

# Problem 3: Decode Ways Full Trace

```
s = "2101"
dp[0]=1
dp[1]: '2' ok → 1
i=2 "21": '1' ok +dp1; two=21 ok +dp0 → 2
i=3 "210": '0' not single; two=10 ok +dp1 → 1
i=4 "2101": '1' ok +dp3; two=01 invalid → 1

Answer 1  (2 | 10 | 1)
```

---

# Problem 4: Coin Change Trace (Impossible)

```
coins=[2], amount=3
dp=[0,∞,∞,∞]
dp[2]=1
dp[3] stays ∞ → -1
```

---

# Problem 5: Word Break False Case

```
s="catsandog", dict=["cats","dog","sand","and","cat"]
...
dp ends False — leftover "og" / failed joins
```

---

# Problem 6: LIS Both Methods

Same array as Classic 6 — verify O(n²) max and patience length both 4.

---

# Problem 7: Min Cost Climbing Stairs

```
STATE: dp[i] = min cost to reach i
TRANSITION: dp[i] = cost[i] + min(dp[i-1], dp[i-2])
ANSWER: min(dp[n-1], dp[n-2])  # can step beyond from either
```

Or: pay cost when you leave a step — read problem statement carefully (LC 746).

```python
def min_cost_climbing_stairs(cost):
    n = len(cost)
    a, b = cost[0], cost[1]
    for i in range(2, n):
        a, b = b, cost[i] + min(a, b)
    return min(a, b)
```

---

# Problem 8: Perfect Squares (Coin Change Disguise)

Min number of perfect squares summing to n → coin change with `coins=[1,4,9,...,⌊√n⌋²]`.

---

# PART 10: BRIDGE FROM RECURSION — FIBONACCI REVISITED

```python
# Recursion module: exponential
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# DP I: memo
def fib_memo(n, memo=None):
    if memo is None: memo = {}
    if n <= 1: return n
    if n in memo: return memo[n]
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# DP I: tabulation O(1) space
def fib_tab(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

**This is the entire DP idea in one page:** identify recurrence → store answers → (optional) compress space.

---

# PART 11: EDGE CASES & INTERVIEW WORKFLOW

## Edge Checklist

| Problem | Edges |
|---|---|
| Climb | n=0,1 |
| Robber | n=0,1,2; negatives usually not present |
| Decode | leading zero, `"0"`, `"10"`, `"30"` |
| Coins | amount 0 → 0; empty coins; unreachable |
| Word break | empty s; dict empty; overlapping words (`cat`,`cats`) |
| LIS | empty; strictly decreasing → 1; duplicates (strict <) |
| Jump | zero in middle blocking; last index 0 |

## Interview Workflow

```
1. Restate; ask constraints (n size → O(n²) OK?)
2. Write STATE / TRANSITION / BASE / ORDER / ANSWER
3. Code tabulation or memo
4. Trace small example aloud
5. Complexity + space optimization if easy
6. Mention greedy alternative if one exists (jump)
```

---

# PART 12: WHAT'S NEXT (DP II PREVIEW — NO CREDIT YET)

| Topic | Why later |
|---|---|
| Unique Paths / min path grid | 2D state |
| 0/1 Knapsack, Partition Equal Subset | choice include/exclude |
| LCS, Edit Distance | 2-string DP |
| Longest Palindromic Subsequence | interval / 2D |
| House Robber on trees | tree DP |

You have the **framework**. DP II adds dimensions and patterns; the five-line ritual stays identical.

---

# PART 13: MORE 1D PATTERNS & FULL TRACES

---

## Pattern: Delete and Earn (House Robber Disguise)

**Problem:** Points = value of number; if you take `x` you cannot take `x-1` or `x+1`. Max points.

**Reduce:** Count frequency; `gain[v] = v * count[v]`. Then house-robber on the sorted unique values where adjacent values that differ by 1 are "adjacent houses."

```python
from collections import Counter

def delete_and_earn(nums):
    if not nums:
        return 0
    count = Counter(nums)
    vals = sorted(count)
    # rob along values; if vals[i]-vals[i-1] > 1, not adjacent constraint
    prev2 = prev1 = 0
    prev_val = None
    for v in vals:
        take = v * count[v]
        if prev_val is not None and v == prev_val + 1:
            cur = max(prev1, prev2 + take)
        else:
            cur = prev1 + take  # can always take after non-adjacent value
        prev2, prev1 = prev1, cur
        prev_val = v
    return prev1
```

### Trace

```
nums = [2,2,3,3,3,4]
gain: 2→4, 3→9, 4→4
vals 2,3,4 consecutive
rob: take 2: 4
     at 3: max(4, 0+9)=9
     at 4: max(9, 4+4)=9
Answer 9 (three 3's)
```

**Lesson:** Many "can't pick neighbors" problems **are** house robber after a transform.

---

## Pattern: Counting Bits / Linear DP Build

```
dp[i] = dp[i >> 1] + (i & 1)
```

Not interview-central for Module 8, but shows DP as "answer for i from answer for smaller i."

---

## Pattern: Maximum Product Subarray (1D with two states)

**Problem:** Max product of a contiguous subarray (negatives flip signs).

```
STATE: max_ending_here, min_ending_here (min needed because negative * negative)
TRANSITION: candidates = (x, max_end*x, min_end*x); update max/min
ANSWER: global max of max_ending
```

```python
def max_product(nums):
    res = max_e = min_e = nums[0]
    for x in nums[1:]:
        candidates = (x, max_e * x, min_e * x)
        max_e = max(candidates)
        min_e = min(candidates)
        res = max(res, max_e)
    return res
```

### Trace

```
[2,3,-2,4]
x=2: max=2,min=2,res=2
x=3: max=6,min=3,res=6
x=-2: max=-2,min=-12,res=6
x=4: max=4,min=-48,res=6
Answer 6
```

**Two-state 1D:** still "1D DP" — state is a pair at each index.

---

## Pattern: Partition Equal Subset Sum (PREVIEW bridge)

Boolean knapsack: can subset sum to `total/2`?

```python
def can_partition(nums):
    s = sum(nums)
    if s % 2: return False
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for a in range(target, x - 1, -1):  # backward = 0/1
            dp[a] = dp[a] or dp[a - x]
    return dp[target]
```

**PREVIEW — DP II** for full knapsack family. Shown so you see **backward 1D** once.

---

## Full Trace Gallery

### Decode Ways — `"11106"`

```
dp[0]=1
dp[1]=1 ("1")
i=2 "11": +dp1 +dp0 (11) → 2
i=3 "111": +dp2 +dp1 (11) → 3
i=4 "1110": no single 0; two=10 → +dp2 → 2
i=5 "11106": single 6 → +dp4; two=06 invalid → 2
Ways: 1|1|10|6 and 11|10|6
```

### Coin Change — count combinations (order-insensitive)

Different from min coins. Loop **coins outer**, amount inner:

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```

```
amount=5, coins=[1,2,5]
After 1s: dp=[1,1,1,1,1,1]
After 2s: dp=[1,1,2,2,3,3]
After 5s: dp=[1,1,2,2,3,4]
Answer 4
```

**Interview:** know min-coins vs count-combinations; loop order changes meaning.

### Word Break — overlapping dict

```
s="catsandog", dict=["cats","dog","sand","and","cat"]
dp[0]=T
"cat" → dp[3]=T; "cats" → dp[4]=T
"sand" from 3 → dp[7]=T; "and" from 4 → dp[7]=T
"dog" from 7 would need s[7:]= "og" fail; from 4 "andog" fail
dp[n]=F
```

### LIS reconstruct (parent pointers)

```python
def lis_sequence(nums):
    n = len(nums)
    dp = [1] * n
    parent = [-1] * n
    best_i = 0
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
        if dp[i] > dp[best_i]:
            best_i = i
    seq = []
    i = best_i
    while i != -1:
        seq.append(nums[i])
        i = parent[i]
    return seq[::-1]
```

```
[10,9,2,5,3,7,101,18] → one LIS [2,5,7,101] or [2,3,7,18]
```

---

# PART 14: DEBUGGING DP — SYSTEMATIC CHECKLIST

When your DP is wrong:

```
1. Print the dp table for a tiny input — does BASE look right?
2. Check STATE English: "dp[i] means ___ using ___ ending/prefix?"
3. Manually compute transition for one i — did you miss a candidate?
4. Off-by-one: length n array vs n+1 prefix array?
5. Impossible sentinel: did you use 0 for "impossible" when 0 is valid?
6. Order: are you reading a cell before it's written?
7. Mutating while iterating (coin combinations vs 0/1)?
```

### Classic bug zoo

| Bug | Symptom |
|---|---|
| `dp[0]=0` for climb ways | Off-by-one ways |
| Decode: treat `0` as valid single | Nonzero garbage |
| Coin INF = 0 | Thinks free |
| Word break: only check last word | Misses mid splits |
| LIS: `<=` instead of `<` | Wrong on duplicates if strict required |
| Robber circular: rob all then subtract | Incorrect; use two ranges |

---

# PART 15: COMPLEXITY TALK TRACKS (INTERVIEW)

**Climb / Robber:** "Linear DP, O(n) time, O(1) space after rolling."

**Coin change:** "O(amount * k). If amount is huge, discuss BFS on residual or math."

**Word break:** "O(n²) substring checks; optimize with max word length and a set."

**LIS:** "O(n²) DP is the clear solution; O(n log n) patience if they ask to optimize."

**Jump II:** "DP O(n²) is correct; optimal interview solution is O(n) greedy BFS layers."

---

# PART 16: SOLO PRACTICE SET (1D DP)

1. Climbing Stairs (+ k steps variant)  
2. Min Cost Climbing Stairs  
3. House Robber I / II  
4. Delete and Earn  
5. Decode Ways  
6. Coin Change (min)  
7. Coin Change II (combinations count)  
8. Word Break  
9. LIS length (+ reconstruct once)  
10. Jump Game I / II  
11. Maximum Product Subarray  
12. Perfect Squares  

For each: write the five lines first, then code, then one trace.

---

# PART 17: SPOKEN PITCHES

### 20-second "What is DP?"

> "DP solves problems with overlapping subproblems and optimal substructure. I define a state, a transition from smaller states, base cases, fill order, and which state is the answer. I either memoize recursion or tabulate bottom-up."

### 20-second House Robber

> "dp[i] is the best using the prefix through i. At each house I skip and take dp[i-1], or rob and take dp[i-2]+nums[i]. Roll two variables for O(1) space."

### 20-second Coin Change

> "dp[a] is fewest coins for amount a. Try every coin, dp[a]=min(dp[a], dp[a-coin]+1). Init dp[0]=0 others inf. Unbounded so nested loops over amounts and coins."

---

# PART 18: WHAT "DONE" LOOKS LIKE FOR THIS TEACH BLOCK

You can, without notes:

1. State the two DP conditions and connect them to the recursion module  
2. Fill STATE / TRANSITION / BASE / ORDER / ANSWER for a new 1D problem  
3. Implement climb stairs, house robber, decode ways, coin change, word break  
4. Implement LIS O(n²) and explain patience O(n log n) at high level  
5. Explain Jump I greedy vs DP; Jump II DP recurrence  
6. Space-optimize a 2-prev recurrence to O(1)  
7. Choose memo vs tabulation and defend the choice  
8. Recognize house-robber transforms (delete and earn) and two-state 1D (max product)  
9. Debug a wrong DP table with the checklist  

**Status after reading:** `taught`. Next: Module 8 retention grill + timed set before `complete`.

---

# PART 19: COUNTING VS OPTIMIZATION VS DECISION DP

Three flavors share the same framework; only the **combine** operator changes.

| Flavor | Combine | Examples |
|---|---|---|
| **Decision** (boolean) | OR | Word break, jump can-reach, partition subset |
| **Optimization** (min/max) | min / max | Coin change min, house robber, LIS length, jump II |
| **Counting** | sum / + | Climb stairs, decode ways, coin combinations |

```
Boolean:  dp[i] = any(compatible predecessors)
Optimize: dp[i] = best(compatible predecessors)
Count:    dp[i] = sum(compatible predecessors)
```

**Interview move:** After stating STATE, say which flavor — it locks the transition algebra.

---

# PART 20: TOP-DOWN vs BOTTOM-UP — SAME PROBLEM THREE WAYS

## Coin Change Min — Memo

```python
def coin_change(coins, amount):
    memo = {}
    def dp(a):
        if a == 0:
            return 0
        if a < 0:
            return float('inf')
        if a in memo:
            return memo[a]
        best = float('inf')
        for c in coins:
            best = min(best, 1 + dp(a - c))
        memo[a] = best
        return best
    ans = dp(amount)
    return ans if ans != float('inf') else -1
```

## Coin Change Min — Tabulation (already in Classic 4)

## Coin Change Min — BFS (0-1 edges in coin graph)

Each coin is an edge of weight 1 in "amount space." Unweighted shortest path from 0 to amount → **BFS**. Same answer as DP; good cross-check with Graphs I.

```python
from collections import deque

def coin_change_bfs(coins, amount):
    if amount == 0:
        return 0
    q = deque([0])
    dist = {0: 0}
    while q:
        a = q.popleft()
        for c in coins:
            na = a + c
            if na == amount:
                return dist[a] + 1
            if na < amount and na not in dist:
                dist[na] = dist[a] + 1
                q.append(na)
    return -1
```

**Bridge:** DP on amounts ↔ BFS on implicit graph. Module 8 Graphs + DP meet here.

---

# PART 21: WORD BREAK — MEMO FORM + OPTIMIZATIONS

```python
def word_break(s, wordDict):
    word_set = set(wordDict)
    max_len = max((len(w) for w in word_set), default=0)
    memo = {}
    def dp(i):
        if i == len(s):
            return True
        if i in memo:
            return memo[i]
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if s[i:j] in word_set and dp(j):
                memo[i] = True
                return True
        memo[i] = False
        return False
    return dp(0)
```

### Trace memo calls on `"leetcode"`

```
dp(0): try "l","le","lee","leet" → "leet" in set → dp(4)
dp(4): try "c","co","cod","code" → "code" → dp(8)=True
→ True; memo={8:True,4:True,0:True} conceptually
```

---

# PART 22: HOUSE ROBBER — INCLUDE/EXCLUDE STATE MACHINE

Explicit two-state formulation (useful when circular / tree later):

```
inc[i] = nums[i] + exc[i-1]   # robbed i ⇒ must skip i-1
exc[i] = max(inc[i-1], exc[i-1])
answer = max(inc[n-1], exc[n-1])
```

```python
def rob(nums):
    inc = exc = 0
    for x in nums:
        inc, exc = exc + x, max(inc, exc)
    return max(inc, exc)
```

### Trace `[2,7,9,3,1]`

```
x=2: inc=2, exc=0
x=7: inc=0+7=7, exc=max(2,0)=2
x=9: inc=2+9=11, exc=max(7,2)=7
x=3: inc=7+3=10, exc=max(11,7)=11
x=1: inc=11+1=12, exc=max(10,11)=11
max=12
```

Same answer; clearer for "rob / skip" talk track.

---

# PART 23: LIS PATIENCE — WHY REPLACING TAILS WORKS (INTUITION)

`tails[len-1]` = smallest possible tail of any IS of that length.

When `x` arrives:
- If `x` larger than all tails → extend longest.
- Else replace the first tail ≥ `x` → future extensions stay as easy as possible (smaller tail is always better or equal for extending).

You do **not** store the actual subsequence in `tails` — only lengths. Hence reconstruct needs parent pointers or a second structure.

### Binary search detail

`bisect_left` finds insertion point for strict increase. For non-decreasing LIS, use `bisect_right` carefully — interview default is **strict**.

---

# PART 24: JUMP GAME II — O(n) GREEDY FULL TRACE

```
nums = [2,3,1,1,4]
jumps=0, end=0, farthest=0

i=0: farthest=max(0,0+2)=2; i==end → jumps=1, end=2
i=1: farthest=max(2,1+3)=4
i=2: farthest=max(4,2+1)=4; i==end → jumps=2, end=4
i=3: …
done when end >= n-1

Answer 2
```

```python
def jump(nums):
    jumps = end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == end:
            jumps += 1
            end = farthest
    return jumps
```

Know **both** DP O(n²) and greedy O(n). Prefer greedy in timed interviews; DP proves understanding.

---

# PART 25: FROM RECURSION MODULE — EXPLICIT MIGRATION CHECKLIST

Take any recursive solution from the Recursion lesson:

```
1. Identify arguments that change → candidate STATE
2. If same args called twice → OVERLAP → memo dict
3. If answer(args) = combine(answer(smaller)) → OPTIMAL SUBSTRUCTURE
4. Rewrite as dp[state] = combine(...)
5. Find topological order of states → tabulation
6. Drop unused dimensions / roll arrays → space opt
```

**Worked migration: triangular path sum (1D rolling preview of 2D)**

Bottom-up from last row:

```python
def minimum_total(triangle):
    dp = triangle[-1][:]
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(len(triangle[r])):
            dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])
    return dp[0]
```

PREVIEW of 2D/grid DP — still uses Module 8 framework.

---

# PART 26: CHEAT SHEET — ONE PAGE RECURRENCES

```
Climb:     f(i) = f(i-1)+f(i-2)
Rob:       f(i) = max(f(i-1), f(i-2)+a[i])
Rob circ:  max(rob[0..n-2], rob[1..n-1])
Decode:    f(i) += f(i-1) if s[i-1]!='0'
           f(i) += f(i-2) if 10..26
Coin min:  f(a) = min_c f(a-c)+1
Coin cnt:  outer coins, f(a) += f(a-c)
Word:      f(i) = OR_j f(j) && s[j:i] in dict
LIS:       f(i) = 1+max f(j), j<i, a[j]<a[i]
Jump I:    reach = max(reach, i+a[i])
Jump II:   f(i)=min f(j)+1 over j reaching i  OR greedy layers
Prod max:  track max_end & min_end
Del&Earn:  robber on gain[v]
Squares:   coin change on squares
```

---

# PART 27: ORAL DRILL

1. Two conditions for DP?  
2. Five framework labels?  
3. Decode ways base for `"0"`?  
4. Why coin combinations loop coins outer?  
5. LIS O(n log n) structure name?  
6. Circular robber method?  
7. When is Jump I greedy enough?  
8. How does recursion memo become tabulation?  

---

---

# PART 28: WORKED INTERVIEW SCRIPT — "COIN CHANGE"

**Interviewer:** Fewest coins to make `amount`.

**You (out loud):**

1. "This is unbounded knapsack / min-coin DP.  
2. State: `dp[a]` = fewest coins to make `a`.  
3. Transition: for each coin `c ≤ a`, `dp[a] = min(dp[a], dp[a-c]+1)`.  
4. Base: `dp[0]=0`, rest `amount+1` as INF.  
5. Answer: `dp[amount]` or −1.  
6. Time O(amount * k), space O(amount).  
7. Edge: amount 0 → 0; no coins → −1 if amount>0."

Then code the tabulation. Trace `[1,2,5], 11` → 3.

If they ask combinations count: "Different problem — outer loop coins so order doesn't double-count."

---

# PART 29: WORKED INTERVIEW SCRIPT — "ACCOUNTS MERGE"

1. "Emails are nodes; shared email ⇒ same person ⇒ union.  
2. DSU on emails (or email→id).  
3. Group by find(email); sort emails; prepend name.  
4. Names alone don't merge — only emails.  
5. Nearly O(E α(E) + E log E) for sorts."

Trace the John/Mary example from Graphs II.

---

# PART 30: EDGE-CASE GAUNTLET (DP)

| Input | Expected | Why |
|---|---|---|
| climb n=1 | 1 | only one single step |
| rob [] | 0 | empty |
| rob [5] | 5 | single |
| decode "" | 0 | empty string |
| decode "0" | 0 | cannot start |
| decode "10" | 1 | only "J" |
| decode "101" | 1 | 10\|1 not 1\|0\|1 |
| coins=[], amount=0 | 0 | zero amount |
| coins=[], amount=7 | -1 | impossible |
| wordBreak "", ["a"] | True | empty segmented vacuously / problem-dependent — LC True |
| LIS [5,4,3] | 1 | decreasing |
| LIS [1,1,1] | 1 | strict increase |
| jump [0] | True | already there |
| jump [1,0,1] | False | stuck at 0 |

---

# PART 31: CONNECTION TABLE — RECURSION → DP I → DP II

| Recursion idea | DP I | DP II |
|---|---|---|
| fib memo | 1D roll | — |
| backtrack subsets | boolean knapsack preview | 0/1 knapsack |
| grid DFS paths | — | unique paths DP |
| string recursion | decode / word break | LCS / edit |
| tree recursion | — | tree DP / house robber III |

**Rule:** If you catch yourself writing exponential recursion with repeated args, stop and name the DP state.

---

# PART 32: FINAL SELF-CHECK (YES/NO) — DP I ONLY

*(Prior draft wrongly listed Dijkstra/DSU/Kruskal here — those belong to `Graphs/Graphs II.md`.)*

- [ ] I can fill the five DP lines (STATE / TRANSITION / BASE / ORDER / ANSWER) before coding  
- [ ] I can do climb / robber / decode / coin / word break / LIS blind  
- [ ] I know memo vs tabulation tradeoffs  
- [ ] I can roll O(1) space for 2-prev DP  
- [ ] I can explain overlapping subproblems + optimal substructure in plain English  
- [ ] I can debug a wrong DP by checking base cases then transition on a failing index  

All yes → ready for Module 8 retention grill + timed set (with Graphs II).

---

---

# PART 33: QUICK REFERENCE — STATE ENGLISH SENTENCES

Write these until automatic:

| Problem | State English |
|---|---|
| Climb | "ways to reach step i" |
| Rob | "best money using houses 0..i" |
| Decode | "ways to decode the first i characters" |
| Coin min | "fewest coins to total exactly a" |
| Word break | "whether the first i characters can be segmented" |
| LIS | "LIS length among subsequences ending at index i" |
| Jump II | "minimum jumps needed to reach index i" |
| Max product | "best and worst product ending at i" |

If you cannot say the English sentence, the code will be fuzzy.

---

# PART 34: CLOSING

DP I is the **framework module**. Patterns multiply in DP II, but every new pattern still answers the same five questions. Master the ritual; the catalog will stick.

**Status after reading:** `taught`. Pair with `Graphs/Graphs II.md`, then `Retention Questions/Module 8 Retention.md`, then timed verification.

---

---

# APPENDIX: FIBONACCI AS THE CANONICAL DP STORY (RECAP)

```
Naive recursion:  T(n) = T(n-1)+T(n-2)+O(1) → Θ(φⁿ)
Memoization:      each n once → Θ(n) time, Θ(n) stack+memo
Tabulation:       loop 2..n → Θ(n) time, Θ(n) array
Rolling:          two ints → Θ(n) time, Θ(1) space
```

Every 1D DP in this lesson is "fibonacci with a different combine and a different meaning of n."

When stuck on a new problem, ask: **"What is my fibonacci index, and what does f(i) mean?"**

---
