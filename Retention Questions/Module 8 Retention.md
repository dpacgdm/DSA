<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 8 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 8 Retention.keys.md`. Attempt first, then grade.

# MODULE 8 RETENTION — GRAPHS II + DP I

**Purpose:** Cumulative retention grill for Module 8 teach blocks.  
**Sources:** `Graphs/Graphs II.md`, `Dynamic Programming/DP I.md`  
**Also pulls:** Graphs I (BFS vs weighted), Heaps (Dijkstra PQ), Recursion (memo ↔ DP).  
**Rules:** No notes. Identify pattern → approach → code → complexity → edges.  
**Governance:** 2D knapsack / LCS / edit distance tagged **PREVIEW — DP II** if they appear. Floyd-Warshall PREVIEW only.

**Escalation map:**

| Section | Focus | Difficulty |
|---|---|---|
| A | Rapid fire concepts | Warm |
| B | Dijkstra + Bellman-Ford | Medium |
| C | Union-Find / MST | Medium |
| D | DP framework + 1D classics | Medium |
| E | Harder / combined | Medium → Hard |
| F | Cumulative integration | Mixed |
| G | Blind-style mixed set | Interview |

---

# SECTION A: RAPID FIRE — CONCEPTS & COMPLEXITY

Answer in 1–3 sentences unless code is requested.

---

## A1. Weighted vs BFS

When is BFS the correct shortest-path algorithm, and when must you switch to Dijkstra?

---

## A2. Dijkstra invariant

State the key invariant that lets Dijkstra finalize a node's distance when it is popped (non-stale). What weight assumption does it need?

---

## A3. Stale heap entry

In lazy binary-heap Dijkstra, why might you pop `(d, u)` with `d > dist[u]`, and what do you do?

---

## A4. Dijkstra complexity

Give the common interview time bound for binary-heap Dijkstra on a graph with `V` vertices and `E` edges.

---

## A5. Negative edge

In one sentence: why does a negative edge break Dijkstra? What algorithm do you use instead?

---

## A6. Bellman-Ford

How many full relaxation passes over all edges does classic Bellman-Ford run before the negative-cycle check? What does the extra pass detect?

---

## A7. DSU find

Write path-compressing `find` in ≤4 lines of Python (array `parent`).

---

## A8. Union by rank

What goes wrong if you always do `parent[find(a)] = find(b)` with no rank/size heuristic? What does union by rank do?

---

## A9. Redundant connection

How does DSU detect the redundant edge in an undirected near-tree?

---

## A10. Kruskal

State Kruskal's algorithm in three steps. Time complexity dominated by what?

---

## A11. DP two conditions

Name the two conditions required for DP. Give one sentence each.

---

## A12. Five-line framework

List the five labels of the DP framework (STATE, …).

---

## A13. Memo vs tabulation

One pro of memoization; one pro of tabulation.

---

## A14. House robber transition

Write the recurrence for `dp[i]` = max money from houses `0..i`.

---

## A15. Coin change

What does `dp[a]` mean in min-coin-change? Base case? When return −1?

---

## A16. LIS

Give O(n²) recurrence for LIS ending at `i`. What is the O(n log n) method called informally?

---

## A17. Space opt

If `dp[i]` depends only on `dp[i-1]` and `dp[i-2]`, how do you get O(1) extra space?

---

## A18. Recursion bridge

How does the Recursion module's fibonacci memoization relate to DP I?

---

# SECTION A — ANSWERS

### A1
BFS when all edges have equal weight (or unweighted) — hop distance equals cost distance. Unequal **non-negative** weights → Dijkstra. Negatives → Bellman-Ford.

### A2
When you first pop `u` with the best known distance (non-stale), `dist[u]` is optimal. Requires **all edge weights ≥ 0** so no later path can undercut a finalized node.

### A3
An older worse distance was pushed before `dist[u]` improved; the old heap entry remains. **Skip** it (`continue`) — lazy deletion.

### A4
**O((V + E) log V)** (or O(E log V) with duplicate heap entries). Interview-acceptable.

### A5
A later negative edge can improve a path through a node that looked farther, violating finalize-on-pop. Use **Bellman-Ford**.

### A6
**|V| − 1** relaxation rounds. An **Nth** pass that still improves some `dist[v]` detects a **negative cycle** reachable from the source (affecting that node).

### A7
```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, x)
    return parent[x]
```

### A8
Trees can degenerate to linked lists → find becomes O(n). Union by rank attaches the lower-rank root under the higher-rank root (and increments rank on ties), keeping trees shallow.

### A9
Process edges in order; `union(u,v)` returns **False** when `u` and `v` are already in the same component → that edge is redundant (creates a cycle).

### A10
(1) Sort edges by weight ascending. (2) Add edge if DSU union succeeds (no cycle). (3) Stop at V−1 edges. Time **O(E log E)** dominated by **sorting**.

### A11
**Overlapping subproblems** — same subproblem recomputed many times. **Optimal substructure** — optimal solution built from optimal sub-solutions.

### A12
STATE, TRANSITION, BASE, ORDER, ANSWER.

### A13
Memo: only computes needed states / natural recursion. Tabulation: no recursion-depth risk / easy space rolling / clear loops.

### A14
`dp[i] = max(dp[i-1], dp[i-2] + nums[i])` with bases `dp[0]=nums[0]`, `dp[1]=max(nums[0], nums[1])`.

### A15
`dp[a]` = fewest coins to make amount `a`. `dp[0]=0`; others init ∞. Return −1 if `dp[amount]` still ∞.

### A16
`dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])` (or 1 if none). **Patience sorting** / tails + binary search.

### A17
Keep two variables `prev2, prev1` and roll forward.

### A18
Fibonacci memo is top-down DP: overlapping subproblems cached. Tabulation/O(1) roll is the bottom-up form of the same recurrence.

---

# SECTION B: DIJKSTRA & BELLMAN-FORD DRILLS

---

## B1. Implement Dijkstra

Implement `dijkstra(n, edges, source)` returning a distance list (`inf` if unreachable). Edges are directed `(u, v, w)`, nodes `0..n-1`, weights ≥ 0. Use binary heap + stale skip.

```
n=5, source=0
edges=[(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3),(2,4,10)]
Expected dist: [0, 3, 1, 4, 7]
```

---

## B2. Network Delay Time

`times` = `[u,v,w]` directed; `n` nodes labeled 1..n; signal from `k`. Return time for all nodes to receive, or −1.

```
times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
```

---

## B3. Explain the bug

Someone runs Dijkstra on:

```
A→B weight 5, B→C weight -10, A→C weight 1; source A
```

They get `dist[C]=1`. Is that correct? What should they use?

---

## B4. Bellman-Ford detect

Write the negative-cycle check loop after `|V|-1` rounds. When is `has_neg_cycle = True`?

---

## B5. K stops flights

Cheapest price from `src` to `dst` with at most `k` stops. Why is plain Dijkstra (ignoring k) wrong for the constraint? Give the BF-style layered approach sketch.

```
n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1
Output: 200
```

---

## B6. Multi-source

You have hospitals on a grid graph with positive travel times. Want min time from **any** hospital to each cell. How do you initialize Dijkstra?

---

## B7. Early exit

You only need `dist[t]` with non-negative weights. When can you stop Dijkstra early?

---

# SECTION B — ANSWERS

### B1

```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, source):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float('inf')] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

Trace matches lesson: `[0,3,1,4,7]`.

### B2

Dijkstra from `k`; answer `max(dist.values())` if all finite else −1. Trace: dist 1←1, 3←1, 4←2; max=2.

### B3

Correct shortest is A→B→C = −5, not 1. Dijkstra may finalize C via A→C. Use **Bellman-Ford**.

### B4

```python
has_neg_cycle = False
for u, v, w in edges:
    if dist[u] != float('inf') and dist[u] + w < dist[v]:
        has_neg_cycle = True
        break
```

True if any edge can still relax → reachable negative cycle (from nodes with finite dist).

### B5

Plain Dijkstra finds unconstrained cheapest path (might use more than k stops). Relax edges for **k+1** rounds using a copy `nxt` each round so each round adds at most one edge. Trace: after enough rounds `dist[2]=200`.

### B6

Set `dist[h]=0` for every hospital `h` and push all `(0, h)` into the heap (multi-source Dijkstra).

### B7

When you pop `t` with a non-stale distance, that distance is final — return it.

---

# SECTION C: UNION-FIND & MST DRILLS

---

## C1. DSU template

Implement class `DSU` with `find`, `union` (by rank, return bool), `components` count.

---

## C2. Redundant Connection

```
edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
```

Code + one-line why.

---

## C3. Accounts Merge

```
accounts = [
  ["John","johnsmith@mail.com","john_newyork@mail.com"],
  ["John","johnsmith@mail.com","john00@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnnybravo@mail.com"]
]
```

Describe unions and final groups (emails sorted). No need for full code if logic is precise.

---

## C4. Number of Provinces

```
isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
```

DSU solution sketch.

---

## C5. Kruskal MST

```
n=4
edges (u,v,w): (0,1,1),(0,2,4),(1,2,2),(1,3,6),(2,3,3)
```

Which edges enter the MST and what is total weight? Show reject reason for skipped edges you consider.

---

## C6. Graph Valid Tree

```
n=5, edges=[[0,1],[0,2],[0,3],[1,4]] → True
n=5, edges=[[0,1],[1,2],[2,3],[1,3],[1,4]] → False
```

State the two conditions checked via DSU / edge count.

---

## C7. Islands II intuition

Start with all water. Add land cells one by one. How do `islands` count updates with DSU when a new land has 2 land neighbors already in **different** components? Same component?

---

# SECTION C — ANSWERS

### C1

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        self.components -= 1
        return True
```

### C2

```python
def find_redundant_connection(edges):
    dsu = DSU(len(edges) + 1)
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    return []
```

`[2,3]` already connected via 1.

### C3

Union all emails in account0; account1 shares `johnsmith@mail.com` → merges `john00`. Mary alone. `johnnybravo` alone.  
Groups: John with `{john00, john_newyork, johnsmith}` sorted; Mary `{mary}`; John `{johnnybravo}`.

### C4

`DSU(n)`; for `i<j` if `isConnected[i][j]`: union. Answer `dsu.components` → 2.

### C5

Add (0,1,1), (1,2,2), (2,3,3). Total **6**. Skip (0,2,4) — cycle in {0,1,2}. Skip (1,3,6) — already connected via 2–3.

### C6

Need **exactly n−1 edges** and **no cycle** (every union succeeds) ⇒ one component. First True. Second has n edges / cycle on (1,3) → False.

### C7

New land: `islands += 1`. For each neighbor land: if `union` merges two components, `islands -= 1`. Two different neighbors in different components → two successful unions → net `islands += 1 - 1 - 1 = -1` relative to before add... wait: start +1, then −1 per successful merge → if 2 merges, islands decreases by 1 overall vs previous. Same component neighbors: second union fails → only one −1.

---

# SECTION D: DP I DRILLS

---

## D1. Framework drill

For **Decode Ways**, write STATE / TRANSITION / BASE / ORDER / ANSWER (no code).

---

## D2. Climbing Stairs

`n=5` → ? Show rolling variable states.

---

## D3. House Robber

```
nums = [2,7,9,3,1]
Output: 12
```

Bottom-up with O(1) space; show `prev1` after each index.

---

## D4. Decode Ways

```
s = "226" → 3
s = "06" → 0
s = "10" → 1
```

Explain each briefly.

---

## D5. Coin Change

```
coins = [1,2,5], amount = 11 → 3
coins = [2], amount = 3 → -1
```

Fill `dp[0..11]` key cells for the first.

---

## D6. Word Break

```
s = "leetcode", wordDict = ["leet","code"] → True
```

Show when `dp[4]` and `dp[8]` become True.

---

## D7. LIS

```
nums = [10,9,2,5,3,7,101,18]
```

Give O(n²) `dp` array final values and answer. Optionally patience `tails` evolution.

---

## D8. Jump Game I

```
nums = [2,3,1,1,4] → True
nums = [3,2,1,0,4] → False
```

Greedy `reach` trace for both.

---

## D9. Jump Game II (DP)

```
nums = [2,3,1,1,4]
```

Give `dp[i]` min jumps array.

---

## D10. House Robber II

```
nums = [1,2,3,1] → 4
```

Why can't you use linear robber directly? What two ranges do you run?

---

## D11. Space optimization

Rewrite climb stairs with only two ints. Why is this valid?

---

## D12. Memo vs table

For word break, would you prefer memo or tabulation? Defend in one sentence each way.

---

# SECTION D — ANSWERS

### D1
STATE: `dp[i]` = ways to decode prefix `s[:i]`.  
TRANSITION: add `dp[i-1]` if `s[i-1]!='0'`; add `dp[i-2]` if two-digit in 10..26.  
BASE: `dp[0]=1`; `dp[1]=1` if first≠0 else 0.  
ORDER: i=2..n.  
ANSWER: `dp[n]`.

### D2
8 ways. Roll: (1,1)→(1,2)→(2,3)→(3,5)→(5,8).

### D3
prev: 2; 7; 11; 11; 12. Answer 12.

### D4
226: three segmentations. 06: leading zero → 0. 10: only "J" (`1`+`0` invalid as split).

### D5
`dp[0]=0`, `1=1`, `2=1`, `5=1`, `10=2`, `11=3`. Second: `dp[3]=∞` → −1.

### D6
`dp[0]=T`; at i=4 `"leet"` with j=0; at i=8 `"code"` with j=4.

### D7
`dp ≈ [1,1,1,2,2,3,4,4]`; max **4**. Patience ends length 4 (`[2,3,7,18]` typical).

### D8
`[2,3,1,1,4]`: reach grows to ≥ last. `[3,2,1,0,4]`: at index 4, `i > reach` when stuck at reach=3 (0 blocks).

### D9
`dp = [0,1,1,2,2]`.

### D10
First and last are adjacent. `max(rob(nums[:-1]), rob(nums[1:]))` → max(3,4)=4.

### D11
```python
a, b = 1, 1
for _ in range(2, n+1):
    a, b = b, a+b
return b
```
Only last two states needed for transition.

### D12
Tabulation: simple left-to-right boolean array. Memo on `(i)` start index: only explores needed splits — also natural. Either fine.

---

# SECTION E: HARDER / COMBINED

---

## E1. Min Cost to Connect All Points

Points on plane; cost = Manhattan distance. Algorithm name + complexity sketch for n points.

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
```

---

## E2. Equations Possible

```
equations = ["a==b","b!=c","c==a"] → False
equations = ["a==b","b==c","a==c"] → True
```

DSU plan: which equations first?

---

## E3. Perfect Squares

Min number of perfect squares summing to `n=12` → 3 (`4+4+4`). Which classic DP is this?

---

## E4. Dijkstra + reconstruct

Extend Dijkstra with `parent` array; reconstruct path 0→4 for B1 graph.

---

## E5. Word Break + Decode kinship

Both are "segment string with valid pieces." Contrast what `dp[i]` means in each.

---

## E6. Why not greedy coins?

US coins greedy works for min coins; for `coins=[1,3,4], amount=6`, greedy 4+1+1=3 vs optimal 3+3=2. What does that say about reaching for DP?

---

## E7. PREVIEW only

Name the all-pairs O(V³) DP shortest path algorithm. Do **not** implement — recognition only.

---

# SECTION E — ANSWERS

### E1
**Kruskal** (or Prim): build all pairs edges O(n²), sort, DSU. Time O(n² log n). MST weight 20.

### E2
Union all `==` first; then for each `!=`, if `find(a)==find(b)` → False. First: a=b=c contradiction with b!=c. Second: consistent.

### E3
**Coin change** with denominations `{1,4,9,...,⌊√n⌋²}`.

### E4
Path e.g. `0→2→1→3→4` (parent chain). Cost 7.

### E5
Decode: `dp[i]` = **count of ways** to decode prefix. Word break: `dp[i]` = **boolean** whether prefix can be segmented. Same skeleton, different monoid (sum vs OR).

### E6
Greedy choice property fails for arbitrary coin systems → use DP min-coins.

### E7
**Floyd-Warshall** (PREVIEW — DP II / advanced graphs).

---

# SECTION F: CUMULATIVE INTEGRATION

Mix Module 8 with prior tools. Tag PREVIEW if beyond earned scope.

---

## F1. BFS or Dijkstra?

Undirected graph, every edge weight 7. Shortest path from s to t?

---

## F2. Heap connection

What Module 6 structure implements Dijkstra's frontier, and what tuple do you push?

---

## F3. Recursion → DP

Convert this exponential recursion to O(n) DP (either style):

```python
def ways(i):
    if i == 0: return 1
    if i < 0: return 0
    return ways(i-1) + ways(i-2)
```

---

## F4. Components

`n` nodes, undirected unweighted edges. Count connected components — give **both** DFS/BFS and DSU one-liners of approach.

---

## F5. Sliding window vs DP

"Longest substring without repeating characters" — is this DP? What tool from earlier modules?

---

## F6. Topo + DP PREVIEW

On a DAG with edge weights, longest path — why Dijkstra is wrong and what order works? (Brief; full DAG DP may be PREVIEW depth.)

---

## F7. Hashing + DSU

In accounts merge, why map emails to ids / use emails as DSU nodes instead of account indices only?

---

# SECTION F — ANSWERS

### F1
**BFS** (or Dijkstra — same answer). Equal weights ⇒ BFS is enough and simpler O(V+E).

### F2
**Binary min-heap** (`heapq`); push `(distance, node)` (and tie-breaker if needed).

### F3
Climb stairs / fib-like: `dp[i]=dp[i-1]+dp[i-2]`, `dp[0]=1`, or rolling vars. `ways(n)`.

### F4
DFS/BFS flood count starts. DSU: union endpoints; answer `components` (or count unique roots).

### F5
Not classic DP. **Sliding window + hash set/map** (Module 1/6 advanced window).

### F6
Longest path needs maximizing; Dijkstra is for shortest with non-neg. On DAG: process in **topo order**, relax max. (PREVIEW if not drilled.)

### F7
Merges are defined by **shared emails**, not shared names. Account indices alone miss transitive email links across list entries.

---

# SECTION G: BLIND-STYLE MIXED SET

No pattern labels. Solve as in interview. Answers at end of section.

---

## G1.

You are given `n` cities and flights `[from, to, price]`. Find the cheapest price from `src` to `dst` with at most `k` stops. Return −1 if impossible.

---

## G2.

`nums` houses in a line; max money without adjacent. Then: same but houses in a **circle**.

---

## G3.

Undirected edges on nodes 1..n that form a tree plus one extra edge. Return that extra edge.

---

## G4.

String `s` of digits; count decode ways `A..Z` ↔ `1..26`.

---

## G5.

Weighted directed graph, all weights positive. Return distances from node `0` to all, or state unreachable.

---

## G6.

Can string be split into dictionary words? Return boolean.

---

## G7.

Connect all points with min total Manhattan wiring cost.

---

## G8.

Length of longest strictly increasing subsequence.

---

## G9.

`isConnected` matrix; return number of provinces.

---

## G10.

Explain to an interviewer: "When do you pick Dijkstra vs Bellman-Ford vs BFS vs DSU?" ≤60 seconds worth of text.

---

# SECTION G — ANSWERS

### G1
Bellman-Ford for `k+1` iterations (or BFS DP by stops). Not unconstrained Dijkstra.

### G2
Linear house robber DP O(n)/O(1). Circular: `max(rob(nums[:-1]), rob(nums[1:]))` (n=1 edge).

### G3
DSU; first edge whose union fails.

### G4
Decode ways 1D DP; careful zeros.

### G5
Dijkstra from 0.

### G6
Word break DP boolean.

### G7
MST Kruskal on complete Manhattan graph (or Prim).

### G8
LIS O(n²) or patience O(n log n).

### G9
DSU unions on `1`s; return components (or DFS).

### G10
Unweighted/equal → BFS. Non-neg weighted distances → Dijkstra. Negatives/cycle detect → Bellman-Ford. Merges, undirected cycle-on-add, components-under-union, Kruskal → DSU.

---

# SECTION H: SELF-SCORE & LEDGER HOOKS

After the grill, tag each miss:

| Tag | Meaning |
|---|---|
| knowledge-gap | Didn't know the tool/recurrence |
| misread | Knew it, answered a different question |
| time-pressure | Right idea, incomplete under time |
| careless-slip | Off-by-one, stale-heap forget, zero-case |

**Subskills to log in `Metrics/Retention Ledger.md`:**

- Dijkstra lazy heap + stale skip  
- Dijkstra failure on negatives  
- Bellman-Ford use cases + K-stops variant  
- DSU find/union by rank  
- Redundant connection / accounts merge / provinces  
- Kruskal MST intuition  
- DP five-line framework  
- Climb / robber / decode / coin / word break / LIS / jump  
- Memo vs tabulation + space roll  
- Recursion↔DP connection  

**Passing this grill alone ≠ `complete`.** Still need timed verification + ledger updates per `Handoff Doc.md`.

---

# SECTION I: QUICK ANSWER KEY — NUMERIC / SHORT

| ID | Short answer |
|---|---|
| B1 | `[0,3,1,4,7]` |
| B2 | `2` |
| B5 | `200` |
| C2 | `[2,3]` |
| C4 | `2` |
| C5 | weight `6` |
| D2 | `8` |
| D3 | `12` |
| D7 | `4` |
| D9 | `[0,1,1,2,2]` |
| D10 | `4` |
| E1 | `20` |
| E3 | coin change / `3` |

---

# SECTION J: EXTRA DRILLS WITH FULL ANSWERS

---

## J1. Dijkstra stale-entry trace

Heap after improvements contains both `(4,1)` and `(3,1)`. Dist[1]=3. What happens when `(4,1)` is popped?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 1)

## J2. Bellman-Ford one round vs Dijkstra

Graph: `0→1 (10)`, `0→2 (5)`, `2→1 (1)`. Source 0. After **one** BF relaxation pass over edges in order `(0,1),(0,2),(2,1)`, what is `dist`? After Dijkstra completes?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 2)

## J3. Union by size vs rank

Implement `union` by **size** instead of rank (attach smaller to larger; update size). Same API return bool.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 3)

## J4. Accounts merge code output

```
[["Gabe","gabe0@","gabe3@"],["Gabe","gabe2@","gabe0@"],["Gabe","gabe2@","gabe4@"]]
```
Final merged emails for the single Gabe group (sorted)?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 4)

## J5. Kruskal reject

MST building; components currently `{0,1,2}` and `{3}`. Edge `(1,2,9)` — add or reject? Edge `(2,3,4)`?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 5)

## J6. Climb stairs k=3

Ways to climb `n=4` with steps 1, 2, or 3.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 6)

## J7. Decode `"2101"` full dp array


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 7)

## J8. Coin change II

`amount=5, coins=[1,2,5]` combination count?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 8)

## J9. Delete and earn

`nums=[2,2,3,3,3,4]` → ?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 9)

## J10. Max product

`nums=[2,3,-2,4]` → ?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 10)

## J11. Jump II greedy layers (optional)

`[2,3,1,1,4]` — explain O(n) BFS-layer idea in 3 sentences.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 11)

## J12. Min effort path tool

Heights grid; minimize the max step absolute difference. Which Module 8 tool, and how is relaxation defined?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 12)

## J13. Virtual node MST

Water wells + pipes problem in one sentence.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 13)

## J14. Write five lines for Perfect Squares


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 14)

## J15. False friend: Dijkstra for longest path

Why doesn't swapping min-heap for max-heap solve longest simple path?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 15)

# SECTION K: TIMED-STYLE MINI SET (ANSWERS BELOW)

Work 25–30 minutes blind, then check.

1. Implement DSU + redundant connection.  
2. Dijkstra network delay.  
3. House robber I + II.  
4. Coin change min.  
5. Word break.  
6. LIS length O(n²).  
7. Kruskal min cost connect points (Manhattan) — sketch edges + DSU.  
8. Explain Dijkstra vs BF vs BFS in 4 sentences.

### K — Answer checklist

1. Union false → return edge.  
2. Max dist or −1.  
3. Linear roll; circular two ranges.  
4. `dp[a]=min(dp[a-c]+1)`.  
5. `dp[i]` boolean prefix.  
6. `dp[i]=1+max compatible j`.  
7. All pairs Manhattan; sort; union until n−1.  
8. Equal→BFS; ≥0 weighted→Dijkstra; negative→BF; connectivity merges→DSU (bonus).

---

# SECTION L: CUMULATIVE ERROR CLINIC

For each wrong student answer, diagnose type.

| Symptom | Likely error type | Fix |
|---|---|---|
| Used BFS on weighted roads | knowledge-gap | Re-teach weighted map |
| Forgot stale skip; wrong dist | careless-slip | Always `if d>dist[u]: continue` |
| Decode `"06"` returned 1 | knowledge-gap / slip | Zero rules drill |
| Circular robber robbed first+last | knowledge-gap | Two-range pattern |
| Kruskal didn't sort | misread / gap | Sort first |
| LIS used subarray thinking | knowledge-gap | Subsequence ≠ subarray |
| Ran Dijkstra with k-stops needed | misread | Constraint → BF layers |

---

**End of Module 8 Retention.** Next session: timed verification set mixing Dijkstra, DSU, and 1D DP without labels; update Scoreboard + Retention Ledger.

---

# SECTION M: MORE RAPID FIRE (WITH ANSWERS)

---

## M1. Prim vs Kruskal one-liner each.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 16)

## M2. What does `α(n)` mean in DSU complexity talk?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 17)

## M3. Dijkstra on undirected graph — implementation pitfall?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 18)

## M4. `dp` for climb stairs: is `dp[0]=1` or `0`?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 19)

## M5. Word break time with max word length L?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 20)

## M6. Can Dijkstra handle 0-weight edges?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 21)

## M7. MST unique?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 22)

## M8. House robber empty / single?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 23)

## M9. BF early exit?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 24)

## M10. Accounts merge: same name different people?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 25)

# SECTION N: FULL SOLUTION WRITEUPS

---

## N1. Network Delay — full code + complexity

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    g = defaultdict(list)
    for u, v, w in times:
        g[u].append((v, w))
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    h = [(0, k)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (dist[v], v))
    ans = max(dist.values())
    return -1 if ans == float('inf') else ans
```
Time O((n+E) log n), Space O(n+E).

---

## N2. Redundant Connection — full

```python
def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    return []
```

---

## N3. Decode Ways — full O(1) space

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1  # dp[0], dp[1]
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != '0':
            cur += prev1
        two = int(s[i - 2:i])
        if 10 <= two <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
```

---

## N4. Word Break — full

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

---

## N5. LIS O(n log n) — full

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

---

# SECTION O: MIXED HARD PROMPTS (ANSWERS)

---

## O1. Cheapest flights with k stops — why layer copy?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 26)

## O2. Min cost connect points — Prim vs Kruskal when n=1000?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 27)

## O3. Give a graph where Dijkstra returns wrong with a negative edge (numbers).


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 28)

## O4. Transform "max sum non-adjacent" on array to house robber.


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 29)

## O5. Is `"12"` decode ways 1 or 2?


> **Answer key:** `Retention Questions/keys/Module 8 Retention.keys.md` (block 30)

# SECTION P: PASS BAR FOR MODULE 8 RETENTION

Aim before timed verification:

- Section A: ≥ 16/18  
- Sections B–D: ≥ 80% correct approaches  
- Section G: ≥ 8/10 tool IDs correct  
- Zero confusion on Dijkstra-vs-BF and robber circular  

Misses → ledger `weak` / `shaky` and re-teach before Module 9.

---
