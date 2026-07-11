# GRAPHS II — WEIGHTED PATHS, UNION-FIND, MST

**Module:** 8 (Graphs II + DP I)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Graphs I (adj list, BFS/DFS, components, topo). Heaps Module 6 (`heapq`).  
**Companion:** `Dynamic Programming/DP I.md`

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHY WEIGHTED GRAPHS EXIST

## The Gap After Graphs I

Graphs I gave you **unweighted** reachability and distance-in-hops:

| Tool | Answers | Cost model |
|---|---|---|
| BFS | shortest path in **# of edges** | every edge costs 1 |
| DFS | connectivity, cycles, topo | no distances |
| Components | "same island?" | unweighted |

Real systems rarely treat every edge as equal:

- Road networks → travel **time** or **distance**
- Flights → ticket **price**
- Networks → **latency** or **bandwidth cost**
- Dependency install → download **size**

**Weighted graph:** each edge `(u → v)` carries a number `w(u,v)` — the cost of that hop.

### Representation (interview default)

Adjacency list of `(neighbor, weight)` pairs:

```python
# Undirected weighted: add both directions
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8)],
    'D': [('B', 5), ('C', 8)],
}
```

Directed: only add the one direction the problem states.

### What "shortest path" means now

**Shortest path** = path from `s` to `t` whose **sum of edge weights** is minimized (not hop count).

BFS is **wrong** for positive unequal weights. Counterexample:

```
s --1--> a --100--> t
s -------2--------> t
```

BFS (hop-minimizing) prefers `s→t` (1 hop) over `s→a→t` (2 hops).  
Weight-minimizing prefers `s→a→t` cost 101? No — prefers `s→t` cost 2. Bad example for BFS failure.

Better counterexample:

```
s --100--> t
s --1--> a --1--> t
```

BFS: `s→t` is 1 hop, "shortest" in hops.  
True weight-shortest: `s→a→t` cost 2 ≪ 100.

**Rule:** unequal positive weights → Dijkstra (or Bellman-Ford). Equal weights / unweighted → BFS.

---

# PART 2: THE SHORTEST-PATH LANDSCAPE (INTERVIEW MAP)

| Situation | Algorithm | Why |
|---|---|---|
| Unweighted / all weights equal | **BFS** | Hop distance = weight distance |
| Weights ∈ {0,1} only | **0-1 BFS** (deque) | O(V+E); see Part 2B |
| Non-negative weights (general) | **Dijkstra** | Greedy finalize works |
| Negative weights, no neg cycle needed for answer | **Bellman-Ford** | Relaxes all edges V−1 times |
| Detect negative cycle | **Bellman-Ford** (+1 pass) | Extra relaxation improves → cycle |
| All-pairs, dense, no neg | Floyd-Warshall (rare in interviews) | O(V³) DP |
| DAG | DP / topo order relax | One pass in topo order |

**This module's focus:** Dijkstra (binary heap) + **0-1 BFS** + Bellman-Ford (when/why, awareness) + Union-Find + MST intuition.

| Situation | Algorithm | Why |
|---|---|---|
| **Weights only 0 or 1** | **0-1 BFS** (deque) | Faster than heap Dijkstra; same idea as BFS with front/back pushes |

Update the decision tree: unweighted → BFS · **0/1 weights → 0-1 BFS** · general non-neg → Dijkstra · negatives → Bellman-Ford.

---

# PART 2B: 0-1 BFS — MUST-KNOW (FAANG)

When every edge weight is **0 or 1**, you do **not** need a binary heap. Use a **deque**:

- Weight **0** edge → `appendleft` (process ASAP — distance unchanged)
- Weight **1** edge → `append` (distance +1)

Invariant: deque stays sorted by distance (0/1 increments). Each node settled once via `dist[]`.

```python
from collections import deque

def zero_one_bfs(n, graph, src):
    """graph[u] = list of (v, w) with w in {0, 1}. Returns dist[]."""
    INF = 10**18
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist
```

**Complexity:** O(V+E) — each edge relaxes like BFS, no `log V`.

**Interview triggers:** grid with two move costs; "teleport" edges cost 0; binary graph shortest path; sometimes disguised as "special roads free."

**Vs Dijkstra:** Same relaxation idea; deque replaces heap because 0/1 keeps distances nearly sorted. If weights are `{0,1,2,...,K}` small, Dial's algorithm generalizes — rare on screens; mention only if asked.

**Vs plain BFS:** Plain BFS assumes all weights equal (usually 1). A 0-weight edge breaks hop-count = cost.

### Mini worked example

Nodes `0-3`. Edges: `0→1` w=1, `0→2` w=0, `2→1` w=0, `1→3` w=1.

From 0: push 0. Pop 0; via w=0 to 2 → dist[2]=0 appendleft; via w=1 to 1 → dist[1]=1 append. Pop 2; via w=0 to 1 → dist[1]=0 (improve!) appendleft. Pop 1; to 3 → dist[3]=1. Answer dist = [0,0,0,1].

Heap Dijkstra also works but is slower to code and asymptotics worse by `log V`.

### Teach-back

1. When must you refuse plain BFS even on an unweighted-looking graph?
2. Why `appendleft` for weight 0?
3. State the full shortest-path picker in one sentence.

---

# PART 3: DIJKSTRA'S ALGORITHM — FULL TREATMENT

## 3A: The Core Idea (Greedy Finalize)

Maintain `dist[u]` = best known distance from source `s` to `u` (initially `∞`, `dist[s]=0`).

**Invariant Dijkstra relies on:** once you **extract** a node `u` from the priority queue as the current closest unsettled node, `dist[u]` is **final** — no future path can improve it.

Why (non-negative weights only):

- Any path that reaches `u` later must go through some other unsettled node `v` first.
- When we popped `u`, `dist[u] ≤ dist[v]` for every unsettled `v`.
- Extending through `v` adds `w(v,…) ≥ 0`, so you cannot undercut `dist[u]`.

**Negative edge breaks this.** A cheap (negative) edge later can undercut a "finalized" distance. That is why Dijkstra fails on negatives — see Part 4.

### Real-world analogy

GPS exploring roads from your location: always expand the **closest unexplored intersection** next. Because driving farther never makes an already-reached intersection "closer" (distances aren't negative), the first time you settle an intersection, that travel time is optimal.

---

## 3B: Binary-Heap Dijkstra — The Interview Implementation

**Lazy Dijkstra** (standard with `heapq`): allow duplicate entries; skip outdated pops.

```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, source):
    """
    n: number of nodes 0..n-1
    edges: list of (u, v, w) directed; for undirected, pass both ways or add both
    returns: dist list; unreachable stay float('inf')
    """
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[source] = 0
    heap = [(0, source)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # outdated lazy entry — skip
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
```

### Why the `if d > dist[u]: continue` line

When we improve `dist[v]`, we **push** a new `(nd, v)` without removing the old heap entry. Old worse entries may pop later. They are stale — ignore them.

This is the same lazy-deletion pattern as Module 6 heaps.

### Path reconstruction (optional)

Keep `parent[v] = u` whenever you improve `dist[v]`. Walk parents from `t` back to `s`.

```python
# inside the improve block:
parent[v] = u

def reconstruct(parent, s, t):
    if dist[t] == float('inf'):
        return []
    path = []
    cur = t
    while cur != s:
        path.append(cur)
        cur = parent[cur]
    path.append(s)
    path.reverse()
    return path
```

---

## 3C: Full Trace — Worked Example

```
Nodes: 0,1,2,3,4
Edges (directed):
  0→1 (4), 0→2 (1),
  2→1 (2), 1→3 (1),
  2→3 (5), 3→4 (3),
  2→4 (10)

Source: 0
```

```
Init: dist = [0, ∞, ∞, ∞, ∞]
heap = [(0, 0)]

Pop (0,0): finalize-ish process 0
  relax 0→1: dist[1]=4, push (4,1)
  relax 0→2: dist[2]=1, push (1,2)
  heap ≈ [(1,2), (4,1)]

Pop (1,2): d=1 == dist[2]
  relax 2→1: 1+2=3 < 4 → dist[1]=3, push (3,1)
  relax 2→3: 1+5=6 → dist[3]=6, push (6,3)
  relax 2→4: 1+10=11 → dist[4]=11, push (11,4)
  heap has (3,1), (4,1 outdated), (6,3), (11,4)...

Pop (3,1): d=3 == dist[1]
  relax 1→3: 3+1=4 < 6 → dist[3]=4, push (4,3)

Pop (4,1): d=4 > dist[1]=3 → SKIP outdated

Pop (4,3): d=4 == dist[3]
  relax 3→4: 4+3=7 < 11 → dist[4]=7, push (7,4)

Pop (6,3): d=6 > dist[3]=4 → SKIP

Pop (7,4): d=7 == dist[4] → done neighbors
Pop (11,4): outdated → SKIP

Final dist: [0, 3, 1, 4, 7]
Paths: 0→2→1→3→4 cost 7
```

**Verify:** `0→2→4` = 11 worse; `0→2→3→4` = 1+5+3=9 worse than 7.

---

## 3D: Complexity

Let `V` = nodes, `E` = edges.

| Implementation | Time | Notes |
|---|---|---|
| Binary heap (lazy) | **O((V + E) log V)** typical interview bound; more precisely O(E log V) with duplicates | Python `heapq` |
| Fibonacci heap (theory) | O(E + V log V) | almost never coded in interviews |
| Dense / array Dijkstra | O(V²) | pick min by scan; good if E ~ V² |

Space: O(V + E) for graph + dist + heap.

**Interview line:** "Binary-heap Dijkstra is O((V+E) log V); I skip stale heap entries."

---

## 3E: Interview Decision Checklist

Use Dijkstra when:

1. Graph is weighted
2. All weights **≥ 0**
3. Single-source (or few sources — run multiple times / multi-source init)
4. Need actual distances or path

Do **not** use Dijkstra when:

1. Negative weights exist → Bellman-Ford
2. Unweighted → BFS (simpler, O(V+E))
3. Need detect negative cycle → Bellman-Ford

### Multi-source Dijkstra

Same algorithm: push all sources with `dist[s]=0` initially (like multi-source BFS). Example: "minimum effort from any hospital."

### Early exit

If you only need `dist[target]`, you can return when you first pop `target` with a non-stale distance (because that pop finalizes it under non-negative weights).

---

# PART 4: WHEN DIJKSTRA FAILS — NEGATIVES & BELLMAN-FORD

## 4A: The Failure Mode (Must Be Able to Explain)

```
s --1--> a --(-2)--> b
s -------3---------> b
```

Dijkstra may finalize `b` via `s→b` cost 3 before discovering `s→a→b` cost −1.

Or more classic:

```
A --5--> B --(-10)--> C
A -----------1------> C
```

Depending on pop order, greedy finalize can lock in a wrong distance because a **negative** edge later improves a path through a node that looked "farther."

**One-sentence interview answer:**  
"Dijkstra assumes adding an edge never decreases a path cost relative to already-finalized nodes; a negative edge violates that, so finalized distances can be wrong."

---

## 4B: Bellman-Ford — Interview Awareness (Demoted Drill Depth)

> **Craft note:** FAANG screens rarely require coding full BF. Know: (1) negatives break Dijkstra, (2) BF = V−1 relax rounds, (3) Nth pass detects neg cycle, (4) "cheapest within K stops" is bounded BF/DP. Prefer **0-1 BFS** and Dijkstra for timed reps.


**Idea:** Relax **every** edge `|V|−1` times. After `k` rounds, `dist[u]` is correct for all paths using ≤ `k` edges (if no neg cycle reachable).

```python
def bellman_ford(n, edges, source):
    """
    edges: list of (u, v, w)
    returns (dist, has_negative_cycle_reachable_from_source)
    """
    dist = [float('inf')] * n
    dist[source] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break  # early stop optimization

    # Nth pass: if any relaxation possible, neg cycle affects that node
    has_neg_cycle = False
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg_cycle = True
            break

    return dist, has_neg_cycle
```

### When you need Bellman-Ford

| Need | Use BF? |
|---|---|
| Negative edge weights, still want shortest paths | **Yes** |
| Detect arbitrage / negative cycle | **Yes** (Nth pass) |
| All weights ≥ 0 | Prefer Dijkstra (faster) |
| Unweighted | Prefer BFS |

### Complexity

Time **O(V·E)**. Space O(V).

Slower than Dijkstra — only reach for it when negatives (or cycle detection) force you.

### Tiny trace

```
edges: (0,1,4), (0,2,5), (1,2,-3), (2,3,1); source 0; n=4

After round 1: dist ≈ [0, 4, 5, ∞] then 4+(-3)=1 updates dist[2]→1; dist[3]→6
After enough rounds: [0, 4, 1, 2]
Path 0→1→2→3 cost 4-3+1=2
```

Dijkstra with a bad finalize order could mishandle the −3; BF doesn't care about order of edges within a round — it just repeats.

---

# PART 5: UNION-FIND / DISJOINT SET UNION (DSU)

## 5A: The Problem DSU Solves

You have elements in **disjoint groups**. You need:

1. **Find** which group an element belongs to (canonical representative)
2. **Union** merge two groups
3. Optionally: count components, detect if adding an edge creates a cycle

Naive: each union rebuilds labels O(n).  
DSU: nearly **O(1)** amortized per op with path compression + union by rank/size.

### Real-world intuition

Social network "friend circles," electrical components connected by wires, pixels in the same island, accounts that share an email — anything that is "same component under merge operations."

---

## 5B: Find with Path Compression

Each node points to a parent. Root points to itself. **Find(x)** = walk to root.

**Path compression:** after find, point `x` (and nodes on the path) directly at the root so future finds are O(1)-ish.

```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, x)  # path compression
    return parent[x]
```

Iterative version (same idea):

```python
def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    # compress
    while parent[x] != root:
        nxt = parent[x]
        parent[x] = root
        x = nxt
    return root
```

---

## 5C: Union by Rank (or Size)

Without care, trees can become linked lists → find is O(n).

**Union by rank:** attach shorter tree under taller tree's root. Rank ≈ upper bound on height.

```python
def union(parent, rank, a, b):
    ra, rb = find(parent, a), find(parent, b)
    if ra == rb:
        return False  # already same set — often means "redundant edge" / cycle
    if rank[ra] < rank[rb]:
        parent[ra] = rb
    elif rank[ra] > rank[rb]:
        parent[rb] = ra
    else:
        parent[rb] = ra
        rank[ra] += 1
    return True  # merged
```

**Union by size:** attach smaller component under larger; store `size[root]`.

### Full template (interview paste-ready)

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

    def connected(self, a, b):
        return self.find(a) == self.find(b)
```

### Complexity

With path compression + union by rank: amortized **≈ O(α(n))** per op — inverse Ackermann, effectively constant. Interview speak: "nearly O(1) amortized."

---

## 5D: Trace — Path Compression + Union by Rank

```
Init n=5: parent=[0,1,2,3,4], rank=[0,0,0,0,0]

union(0,1): ranks equal → parent[1]=0, rank[0]=1
  parent=[0,0,2,3,4]

union(2,3): parent[3]=2, rank[2]=1
  parent=[0,0,2,2,4]

union(0,2): find0=0 rank1, find2=2 rank1 → parent[2]=0, rank[0]=2
  parent=[0,0,0,2,4]  (3 still points to 2)

find(3): parent[3]=2, parent[2]=0 → root 0
  compress: parent[3]=0, parent[2]=0
  parent=[0,0,0,0,4]
```

---

# PART 6: UNION-FIND APPLICATIONS (INTERVIEW PATTERNS)

## Pattern A: Number of Islands Variants

**Grid DFS/BFS** is the classic for "number of islands."  
**DSU** shines when:

- You add land cells **dynamically** (Number of Islands II)
- You think in "cells as nodes, adjacent land = union"

### Static islands via DSU (teaching bridge)

```python
def num_islands_dsu(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    def idx(r, c): return r * C + c
    dsu = DSU(R * C)
    water = 0
    dirs = [(1,0), (0,1)]  # union right/down to avoid double

    for r in range(R):
        for c in range(C):
            if grid[r][c] == '0':
                water += 1
                continue
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == '1':
                    dsu.union(idx(r, c), idx(nr, nc))

    # components among land cells only
    land = R * C - water
    # count unique roots among land
    roots = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1':
                roots.add(dsu.find(idx(r, c)))
    return len(roots)
```

**Interview preference:** DFS/BFS for static grid; DSU for online / union-heavy variants.

### Number of Islands II (add positions over time)

Start all water. For each new land cell: `islands += 1`, then for each adjacent land neighbor, if `union` succeeds, `islands -= 1`.

---

## Pattern B: Redundant Connection

**Problem:** Undirected graph that started as a tree; one extra edge. Return the edge that forms the cycle (last one in input that connects two already-connected nodes).

```python
def find_redundant_connection(edges):
    n = len(edges)  # n edges on n nodes → one cycle
    dsu = DSU(n + 1)  # nodes 1..n
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    return []
```

**Trace:**

```
edges = [[1,2],[1,3],[2,3]]
union(1,2) OK
union(1,3) OK
union(2,3) → same component → return [2,3]
```

**Why DSU:** cycle detection in undirected graph while scanning edges = "union returns False."

---

## Pattern C: Accounts Merge

**Problem:** List of accounts `[name, email1, email2, ...]`. Merge accounts that share any email. Output merged emails sorted per account.

**Model:**

- Each email is a DSU node (map email → id)
- Union emails that appear in the same account
- Group by root; attach name from any account in the group

```python
from collections import defaultdict

def accounts_merge(accounts):
    email_to_id = {}
    email_to_name = {}
    dsu = DSU(10001)  # or len of unique emails after counting
    # safer: assign ids dynamically
    # --- cleaner version below ---

def accounts_merge(accounts):
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        parent.setdefault(a, a)
        parent.setdefault(b, b)
        parent[find(a)] = find(b)

    email_to_name = {}
    for acc in accounts:
        name = acc[0]
        first = acc[1]
        for email in acc[1:]:
            email_to_name[email] = name
            union(first, email)

    groups = defaultdict(list)
    for email in email_to_name:
        groups[find(email)].append(email)

    return [[email_to_name[root]] + sorted(emails)
            for root, emails in groups.items()]
```

**Key insight:** shared email ⇒ same person ⇒ union. Transitive merges fall out of DSU automatically.

---

## Pattern D: Other Classic DSU Cues

| Cue | Approach |
|---|---|
| "Connecting wires / cities with cost" | Kruskal MST (Part 7) |
| "Earliest time all friends connected" | Sort events, union until 1 component |
| "Equations == and !=" | Union equals; check unequals not same root |
| "Number of provinces" | Union adjacent 1s in matrix; count components |
| "Graph valid tree?" | n−1 edges + union all without cycle + 1 component |

---

# PART 7: MST INTUITION — KRUSKAL WITH UNION-FIND

## 7A: What Is an MST?

**Minimum Spanning Tree** of a connected undirected weighted graph:

- Connects all vertices
- No cycles (a tree)
- Minimum total edge weight among all such trees

**Interview level:** know the definition, Kruskal's algorithm with DSU, complexity, and when MST appears (network wiring, clustering intuition). Prim's is the heap-based alternative (similar to Dijkstra shape) — mention, don't over-drill unless asked.

### Kruskal intuition

Sort edges by weight ascending. Add next edge if it **doesn't form a cycle** (DSU `union` succeeds). Stop at `V−1` edges.

Greedy correctness (sketch): lightest edge that connects two components is safe for some MST (cut property).

---

## 7B: Kruskal Implementation

```python
def kruskal_mst(n, edges):
    """
    n nodes 0..n-1
    edges: (w, u, v) or (u, v, w) — we'll sort by w
    returns (total_weight, mst_edges) or None if not connected
    """
    edges = sorted(edges, key=lambda e: e[2])  # (u,v,w)
    dsu = DSU(n)
    total = 0
    mst = []
    for u, v, w in edges:
        if dsu.union(u, v):
            total += w
            mst.append((u, v, w))
            if len(mst) == n - 1:
                break
    if len(mst) != n - 1:
        return None  # disconnected
    return total, mst
```

### Trace

```
n=4
edges: (0,1,1), (0,2,4), (1,2,2), (1,3,6), (2,3,3)

Sort: (0,1,1), (1,2,2), (2,3,3), (0,2,4), (1,3,6)

Add 0-1 (1): OK
Add 1-2 (2): OK
Add 2-3 (3): OK → 3 edges, done
Skip rest

MST weight = 1+2+3 = 6
Edges: 0-1, 1-2, 2-3
(0-2 would cycle; 1-3 heavier)
```

### Complexity

Sort O(E log E) + DSU almost O(E) → **O(E log E)** dominated by sort.

### Kruskal vs Prim (one glance)

| | Kruskal | Prim |
|---|---|---|
| Core | Sort edges + DSU | Grow tree from a node + heap |
| Feels like | Greedy edges | Dijkstra-shaped |
| Best when | Sparse, edge list natural | Dense / adjacency natural |
| Interview | **Most common MST ask** | Know it exists |

### When MST shows up in disguise

- "Minimum cost to connect all points" (Manhattan/Euclidean) → build complete graph edges, Kruskal/Prim
- "Optimize water distribution" — sometimes virtual node + MST
- Clustering: remove k−1 heaviest MST edges → k clusters (concept only)

---

# PART 8: EDGE CASES & INTERVIEW WORKFLOW

## Edge Cases

| Topic | Watch for |
|---|---|
| Dijkstra | Disconnected nodes → `inf`; 0-weight edges OK; self-loops ignore or non-negative |
| Dijkstra | Undirected: add both directions |
| Dijkstra | Overflow: use large sentinel carefully; Python int fine |
| Bellman-Ford | Unreachable neg cycle shouldn't always poison answer — define problem |
| DSU | 0-index vs 1-index nodes; `n` vs `n+1` sizing |
| Kruskal | Disconnected graph → no MST; duplicate edges |
| Accounts merge | Same name ≠ same person; only emails merge |

## Interview Workflow — Shortest Path

```
1. Weighted? Negative? Directed?
2. Unweighted → BFS
3. Non-neg weights → Dijkstra
4. Negatives / cycle detect → Bellman-Ford
5. State complexity; mention stale heap entries
6. Trace 4–5 node example
```

## Interview Workflow — DSU / MST

```
1. "Components under merges / cycle on undirected edges?" → DSU
2. Need min cost connect all? → MST / Kruskal
3. Write DSU template first (find + union)
4. Sort if Kruskal; process edges
```

---

# PART 9: CONSOLIDATED CHEAT SHEETS

## Algorithm Choice

| Problem shape | Tool |
|---|---|
| Shortest path, equal/unweighted | BFS |
| Shortest path, weights ≥ 0 | Dijkstra + heap |
| Shortest path, negative weights | Bellman-Ford |
| Negative cycle / arbitrage | Bellman-Ford + extra pass |
| Dynamic connectivity / merge sets | DSU |
| Undirected cycle while adding edges | DSU union False |
| Min cost to connect all nodes | Kruskal (DSU) or Prim |
| Accounts / emails merge | DSU on emails |
| Redundant edge in near-tree | DSU |

## Complexities

| Algo | Time | Space |
|---|---|---|
| Dijkstra (binary heap) | O((V+E) log V) | O(V+E) |
| Bellman-Ford | O(VE) | O(V) |
| DSU op | ≈ O(α(n)) | O(n) |
| Kruskal | O(E log E) | O(V) |

## Dijkstra Snippet (memorize)

```python
dist = [inf]*n; dist[s]=0
heap=[(0,s)]
while heap:
    d,u = heappop(heap)
    if d > dist[u]: continue
    for v,w in graph[u]:
        if d+w < dist[v]:
            dist[v]=d+w
            heappush(heap,(dist[v],v))
```

## DSU Snippet (memorize)

```python
parent=list(range(n)); rank=[0]*n
def find(x):
    if parent[x]!=x: parent[x]=find(parent[x])
    return parent[x]
def union(a,b):
    ra,rb=find(a),find(b)
    if ra==rb: return False
    if rank[ra]<rank[rb]: parent[ra]=rb
    elif rank[ra]>rank[rb]: parent[rb]=ra
    else: parent[rb]=ra; rank[ra]+=1
    return True
```

## Decision Tree

```
Need distances on graph?
├── unweighted → BFS
├── weights ∈ {0,1} → 0-1 BFS
├── weights ≥ 0 (general) → Dijkstra
└── negatives → Bellman-Ford

Need merges / same-component queries?
└── DSU (path compression + union by rank)

Need min total wire to connect all?
└── Kruskal: sort edges, DSU add if not cycle
```

---

# PART 10: WORKED PROBLEMS WITH TRACES

---

# Problem 1: Network Delay Time (Dijkstra)

## Pattern Identification

**Single-source shortest path, non-negative times** → Dijkstra. Answer = max dist among reachable; if any unreachable → −1.

## Solution

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))

    ans = max(dist.values())
    return ans if ans < float('inf') else -1
```

## Trace

```
n=4, k=2, times=[[2,1,1],[2,3,1],[3,4,1]]

dist init: {1:∞,2:0,3:∞,4:∞}
pop (0,2): update 1→1, 3→1
pop (1,1): no outs
pop (1,3): update 4→2
pop (2,4): done

max=2 → answer 2
```

## Complexity

O((n+E) log n)

---

# Problem 2: Cheapest Flights Within K Stops (Bellman-Ford style)

## Pattern Identification

At most `K` stops ⇒ at most `K+1` edges. **Bounded relaxations** — Bellman-Ford for `K+1` rounds (or BFS-like DP). Dijkstra alone without stop constraint is wrong for this problem's constraint.

## Solution

```python
def find_cheapest_price(n, flights, src, dst, k):
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(k + 1):
        nxt = dist[:]  # use previous layer only
        for u, v, w in flights:
            if dist[u] != float('inf') and dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt

    return dist[dst] if dist[dst] != float('inf') else -1
```

## Trace

```
n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1

Round 1 (≤1 edge): dist[1]=100, dist[2]=500
Round 2 (≤2 edges): dist[2]=min(500, 100+100)=200

Answer 200
```

## Note

This is BF with early stop count — bridges Module 8 Dijkstra/BF thinking to DP-on-graphs.

---

# Problem 3: Redundant Connection

## Pattern Identification

**DSU cycle detection** on undirected edges.

## Solution

See Pattern B above.

## Trace

```
[[1,2],[2,3],[3,4],[1,4],[1,5]]
unions OK until (1,4): 1 and 4 already connected via 1-2-3-4
return [1,4]
```

---

# Problem 4: Accounts Merge

## Pattern Identification

**DSU on emails**; group by root; sort.

## Trace (small)

```
accounts = [
  ["John","a@x","b@x"],
  ["John","b@x","c@x"],
  ["Mary","d@x"],
]

union a-b, union b-c → {a,b,c} one component
d alone

Output:
[["John","a@x","b@x","c@x"], ["Mary","d@x"]]
```

---

# Problem 5: Min Cost to Connect All Points (Kruskal)

## Pattern Identification

**MST** on complete graph with Manhattan distance `|x1-x2|+|y1-y2|`.

## Solution

```python
def min_cost_connect_points(points):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((i, j, w))
    edges.sort(key=lambda e: e[2])
    dsu = DSU(n)
    cost = 0
    used = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            cost += w
            used += 1
            if used == n - 1:
                break
    return cost
```

## Trace

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Light edges connect nearby points first; DSU rejects cycles;
total MST cost = 20 (classic LC 1584 example)
```

---

# Problem 6: Number of Provinces

## Pattern Identification

**DSU** (or DFS components) on adjacency matrix.

## Solution

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.components
```

## Trace

```
[[1,1,0],[1,1,0],[0,0,1]]
union(0,1) → components 2
no union with 2
answer 2
```

---

# Problem 7: Why Not Dijkstra? (Explain)

```
Edges: A→B weight 1, B→C weight -100, A→C weight 2
Source A. Claimed Dijkstra finalize order risk.
```

## Answer

Non-negative assumption fails. Path A→B→C = −99 beats A→C = 2. If C were finalized via A→C before processing the negative edge through B, Dijkstra can return wrong dist[C]. Use Bellman-Ford.

---

# Problem 8: Graph Valid Tree

## Pattern Identification

Undirected graph is a tree iff **exactly n−1 edges** and **fully connected** (no cycle). DSU: every union succeeds and final components == 1.

```python
def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):
            return False
    return dsu.components == 1
```

---

# PART 11: PRIM'S ALGORITHM — INTERVIEW AWARENESS

Kruskal grows by **lightest global edge**. Prim grows a tree from a **seed vertex**, always adding the lightest edge that leaves the tree — Dijkstra-shaped with a min-heap of `(edge_weight, node)`.

```python
import heapq
from collections import defaultdict

def prim_mst(n, edges, start=0):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    visited = [False] * n
    heap = [(0, start)]  # (weight_to_add, node)
    total = 0
    taken = 0
    while heap and taken < n:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        total += w
        taken += 1
        for v, wt in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (wt, v))
    return total if taken == n else None
```

**Interview line:** "Prim is to MST what Dijkstra is to shortest paths; Kruskal + DSU is usually faster to code for sparse edge lists."

| | Kruskal | Prim |
|---|---|---|
| Data structure | Sort + DSU | Heap + adj list |
| Feels like | Greedy edges | Dijkstra |
| Dense graphs | OK | Often preferred in theory |
| Coding interviews | **More common** | Know the shape |

---

# PART 12: MORE WORKED PROBLEMS WITH FULL TRACES

---

# Problem 9: Path With Minimum Effort (Binary Search + BFS PREVIEW / Dijkstra)

## Pattern Identification

Grid; effort of a path = **max absolute height diff** on any step. Minimize effort.

This is shortest path with a **custom cost**: edge weight = `|h[u]-h[v]|`, path cost = **max** edge on path (not sum). Dijkstra still works if you redefine relaxation: `nd = max(d, edge_effort)` and minimize `nd`.

## Solution (Dijkstra variant)

```python
import heapq

def minimum_effort_path(heights):
    R, C = len(heights), len(heights[0])
    dist = [[float('inf')] * C for _ in range(R)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]  # effort, r, c
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while heap:
        e, r, c = heapq.heappop(heap)
        if e > dist[r][c]:
            continue
        if (r, c) == (R - 1, C - 1):
            return e
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                if ne < dist[nr][nc]:
                    dist[nr][nc] = ne
                    heapq.heappush(heap, (ne, nr, nc))
    return 0
```

## Trace (tiny)

```
heights = [[1,2,2],[3,8,2],[5,3,5]]
Path 1→2→2→2→5 has max step effort max(1,0,0,3)=3
Other paths worse or equal. Answer 2 on the classic LC case with better path —
run algorithm; effort expands like Dijkstra with max-combine.
```

**Takeaway:** Dijkstra is not only for sum-of-weights — any "path score" that is **non-decreasing along extensions** and wants a minimum can often use the same heap pattern. Confirm monotonicity before claiming it.

---

# Problem 10: Connecting Cities With Minimum Cost (Kruskal)

## Pattern Identification

`n` cities, connections `[u,v,cost]`. Min cost to connect all, or −1. **MST**; if not fully connected after Kruskal → −1.

```python
def minimum_cost(n, connections):
    connections.sort(key=lambda x: x[2])
    dsu = DSU(n + 1)  # 1-indexed cities
    cost = 0
    edges_used = 0
    for u, v, w in connections:
        if dsu.union(u, v):
            cost += w
            edges_used += 1
            if edges_used == n - 1:
                return cost
    return -1
```

## Trace

```
n=3, connections=[[1,2,5],[1,3,6],[2,3,1]]
Sort: (2,3,1), (1,2,5), (1,3,6)
Add 2-3 cost 1; add 1-2 cost 5; done (2 edges). Total 6.
(1,3) skipped — would cycle.
```

---

# Problem 11: Smallest String With Swaps (DSU + Sort)

## Pattern Identification

You may swap `s[i]` and `s[j]` if `[i,j]` in pairs (transitively). Minimize lexicographic string.

**Model:** indices in same DSU component can be freely rearranged. For each component: sort indices, sort characters, assign smallest chars to earliest indices.

```python
from collections import defaultdict

def smallest_string_with_swaps(s, pairs):
    n = len(s)
    dsu = DSU(n)
    for a, b in pairs:
        dsu.union(a, b)
    groups = defaultdict(list)
    for i in range(n):
        groups[dsu.find(i)].append(i)
    res = list(s)
    for idxs in groups.values():
        chars = sorted(res[i] for i in idxs)
        for i, ch in zip(sorted(idxs), chars):
            res[i] = ch
    return ''.join(res)
```

## Trace

```
s = "dcab", pairs = [[0,3],[1,2]]
Components: {0,3}, {1,2}
{0,3}: chars d,b → b,d at positions 0,3
{1,2}: c,a → a,c at 1,2
Result: "bacd"
```

---

# Problem 12: Optimize Water Distribution (Virtual Node + MST)

## Pattern Identification

Wells cost `wells[i]` to dig in village i; pipes `[u,v,cost]`. Min cost so every village has water.

**Trick:** create virtual node 0; edge `0—i` weight `wells[i-1]`. Then MST on villages+virtual = dig some wells + lay some pipes.

```python
def min_cost_to_supply_water(n, wells, pipes):
    edges = []
    for i, w in enumerate(wells, 1):
        edges.append((0, i, w))
    for u, v, c in pipes:
        edges.append((u, v, c))
    edges.sort(key=lambda e: e[2])
    dsu = DSU(n + 1)
    total = 0
    used = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            total += w
            used += 1
            if used == n:  # n edges connect n+1 nodes (0..n)
                break
    return total
```

**Interview gold:** "virtual node turns 'build facility OR connect' into a single MST."

---

# Problem 13: Swim in Rising Water (Dijkstra on Grid)

## Pattern Identification

Grid of heights; time `t` you can enter cells ≤ t. Min `t` to reach end = minimize the **max height** on the path (you wait until water reaches that).

Dijkstra with cost = `max(current_time, grid[nr][nc])`.

```python
import heapq

def swim_in_water(grid):
    n = len(grid)
    dist = [[float('inf')] * n for _ in range(n)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if (r, c) == (n - 1, n - 1):
            return t
        if t > dist[r][c]:
            continue
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                nt = max(t, grid[nr][nc])
                if nt < dist[nr][nc]:
                    dist[nr][nc] = nt
                    heapq.heappush(heap, (nt, nr, nc))
    return -1
```

---

# Problem 14: Earliest Moment When Everyone Becomes Friends

## Pattern Identification

Logs `[timestamp, a, b]` friendships form. Earliest time all `n` people connected → sort by time, DSU until `components == 1`.

```python
def earliest_acq(logs, n):
    logs.sort()
    dsu = DSU(n)
    for t, a, b in logs:
        dsu.union(a, b)
        if dsu.components == 1:
            return t
    return -1
```

## Trace

```
n=4, logs sorted by time
unions gradually merge; when components hits 1, return that timestamp
```

---

# Problem 15: Critical / Pseudo-Critical Edges in MST (Interview Depth)

**Critical:** removing it increases MST weight (or disconnects).  
**Pseudo-critical:** can appear in some MST but not all.

Approach (interview sketch, not full code):

1. Compute MST weight `base` with Kruskal.  
2. For each edge e: force-exclude e, recompute MST → if worse/impossible, e is critical.  
3. Else force-include e, complete MST → if weight == `base`, e is pseudo-critical (or critical already handled).

This is a **stretch** problem — know the definitions; implement only if time allows.

---

# PART 13: COMMON INTERVIEW TRAPS (GRAPHS II)

| Trap | Fix |
|---|---|
| Using BFS on unequal weights | Counterexample with 1-hop expensive vs 2-hop cheap |
| Forgetting undirected = two directed edges | Always add both in adj list |
| Comparing custom objects in heap without tie-break | `(dist, counter, node)` |
| Dijkstra with negatives "just this once" | Never — use BF |
| DSU 0-index vs 1-index off-by-one | Size `n+1` when nodes are 1..n |
| Kruskal on disconnected graph returning a "tree" | Check `len(mst)==n-1` |
| Accounts merge by name | Names collide; emails define identity |
| Mutating `dist` while iterating BF in one array for K-stops | Use layer copy `nxt` |

### Spoken 30-second Dijkstra pitch

> "I'll run Dijkstra with a min-heap of (distance, node). dist[source]=0. Pop the closest unsettled distance; skip if stale. Relax neighbors. Because weights are non-negative, the first time I settle a node it's optimal. Complexity O((V+E) log V) with a binary heap."

### Spoken 20-second DSU pitch

> "Disjoint set with path compression and union by rank. find returns the root; union merges by rank and returns false if already connected — that's my cycle check. Amortized nearly constant per operation."

---

# PART 14: PRACTICE SET (SOLO — THEN CHECK)

Do these blind after teaching. Solutions are patterns above.

1. Network Delay Time  
2. Cheapest Flights Within K Stops  
3. Path With Minimum Effort  
4. Redundant Connection  
5. Accounts Merge  
6. Number of Provinces  
7. Graph Valid Tree  
8. Min Cost to Connect All Points  
9. Connecting Cities With Minimum Cost  
10. Smallest String With Swaps  
11. Optimize Water Distribution (virtual node)  
12. Earliest Friends Acquaintance  

For each: name tool in 5 seconds → code → complexity → one edge case.

---

# PART 15: CONNECTION TO PRIOR MODULES

| Prior module | Connection |
|---|---|
| Graphs I BFS | Unweighted special case of shortest path |
| Heaps | Dijkstra's priority queue; stale entries; Prim |
| Recursion/DFS | Island DFS alternative to DSU |
| Hashing | email→id maps in accounts merge |
| Sorting | Kruskal edge sort; logs by timestamp |

| Next | Connection |
|---|---|
| DP I | Flight K-stops is DP/BF hybrid; path counts later |
| DP II | Floyd-Warshall as all-pairs DP |

---

# PART 16: WHAT "DONE" LOOKS LIKE FOR THIS TEACH BLOCK

You can, without notes:

1. Implement lazy binary-heap Dijkstra and explain the stale-pop skip  
2. Explain **why** negatives break Dijkstra; when to switch to Bellman-Ford  
3. Write DSU with path compression + union by rank  
4. Solve redundant connection + accounts merge + provinces  
5. Run Kruskal mentally on a 5-edge graph and get the MST weight  
6. Pick BFS vs Dijkstra vs BF vs DSU from a problem statement in ≤30 seconds  
7. Recognize Prim as Dijkstra-shaped MST; virtual-node MST tricks  
8. Adapt Dijkstra to min-max path costs (effort / swim)  

**Status after reading:** `taught`. Next: Module 8 retention grill + timed set before `complete`.

---

# PART 17: DIJKSTRA — SECOND FULL TRACE (STEP TABLE)

```
Undirected (add both ways):
0—1:2, 0—2:5, 1—2:1, 1—3:4, 2—3:2
Source 0. Goal: all dist + parent for path to 3.
```

| Step | Pop | Stale? | dist after relaxes | heap (approx) |
|---|---|---|---|---|
| init | — | — | [0,∞,∞,∞] | (0,0) |
| 1 | (0,0) | no | [0,2,5,∞] | (2,1),(5,2) |
| 2 | (2,1) | no | [0,2,3,6] via 1→2 (2+1), 1→3 (2+4) | (3,2),(5,2),(6,3) |
| 3 | (3,2) | no | [0,2,3,5] via 2→3 (3+2) | (5,2 stale),(5,3),(6,3) |
| 4 | (5,2) | yes skip | unchanged | … |
| 5 | (5,3) | no | final | … |
| 6 | (6,3) | yes skip | — | empty-ish |

**Final dist:** `[0, 2, 3, 5]`. Path 0→1→2→3 (parents: 1←0, 2←1, 3←2).

Verify: 0→2→3 = 5+2=7 worse; 0→1→3 = 2+4=6 worse than 5.

---

# PART 18: BELLMAN-FORD — ARBITRAGE INTUITION

Currency exchange: edge A→B weight `−log(rate)`. Negative cycle ⇒ arbitrage (multiply rates > 1 around a loop).

**Interview:** You do not need to code logs in most screens — say: "model as graph; negative cycle detection via Bellman-Ford Nth pass."

```
If after V-1 rounds any edge still relaxes on a reachable node,
a negative cycle exists → report arbitrage / impossible shortest paths.
```

### BF vs SPFA (mention only)

SPFA = queue-based BF variant; average fast, worst exponential. Rarely required; stick to classic BF + Dijkstra.

---

# PART 19: DSU — RANK VS SIZE DEEP DIVE + COMPONENT SIZE QUERIES

Often you need **size of component** containing `x`:

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def component_size(self, x):
        return self.size[self.find(x)]
```

### Application: Longest consecutive sequence (hash + optional DSU)

Hash set O(n) is the usual solution. DSU variant: union `x` with `x+1` if both present; track max `component_size`. Same asymptotic idea.

### Application: Satisfiability of Equality Equations (full code)

```python
def equations_possible(equations):
    parent = list(range(26))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a, b):
        parent[find(a)] = find(b)

    for eq in equations:
        if eq[1:3] == '==':
            union(ord(eq[0]) - 97, ord(eq[3]) - 97)
    for eq in equations:
        if eq[1:3] == '!=':
            if find(ord(eq[0]) - 97) == find(ord(eq[3]) - 97):
                return False
    return True
```

---

# PART 20: MST CUT PROPERTY (WHY KRUSKAL WORKS — INTERVIEW SKETCH)

**Cut property:** For any cut (partition of vertices into two sets), the lightest edge crossing the cut is in *some* MST.

Kruskal always adds a lightest edge connecting two components = lightest edge across that cut → safe.

**Cycle property:** Heaviest edge on any cycle is not needed in some MST — explains why we skip edges that would close a cycle (they'd be redundant and not lighter than alternatives already considered in sorted order).

You need the **name** and one-sentence cut property for strong interviews — not a formal proof.

---

# PART 21: COMPARISON MATRIX (PRINT & MEMORIZE)

| Need | BFS | Dijkstra | Bellman-Ford | DSU | Kruskal |
|---|---|---|---|---|---|
| Unweighted SP | ✅ | OK | OK | — | — |
| Non-neg weighted SP | ❌ | ✅ | OK slow | — | — |
| Neg weights SP | ❌ | ❌ | ✅ | — | — |
| Neg cycle detect | ❌ | ❌ | ✅ | — | — |
| Dynamic connectivity | — | — | — | ✅ | — |
| Undirected cycle on add | — | — | — | ✅ | — |
| Min cost connect all | — | Prim~ | — | used by | ✅ |
| Merge accounts/emails | — | — | — | ✅ | — |

---

# PART 22: CODE TEMPLATES — COPY BLOCK

### Template A — Dijkstra (dict graph)

```python
import heapq
from collections import defaultdict

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
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

### Template B — Bellman-Ford

```python
def bellman_ford(n, edges, source):
    dist = [float('inf')] * n
    dist[source] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] < float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] < float('inf') and dist[u] + w < dist[v]:
            return dist, True
    return dist, False
```

### Template C — Kruskal

```python
def mst_kruskal(n, edges):
    edges = sorted(edges, key=lambda e: e[2])
    dsu = DSU(n)
    wsum, used = 0, []
    for u, v, w in edges:
        if dsu.union(u, v):
            wsum += w
            used.append((u, v, w))
            if len(used) == n - 1:
                break
    return (wsum, used) if len(used) == n - 1 else (None, None)
```

---

# PART 23: ORAL DRILL (SAY ALOUD)

1. "BFS finds shortest paths when …"  
2. "I skip a Dijkstra heap entry when …"  
3. "Dijkstra fails when … because …"  
4. "Bellman-Ford runs … rounds then …"  
5. "Path compression means …"  
6. "Union by rank means …"  
7. "Kruskal sorts … and uses DSU to …"  
8. "Accounts merge unions on … not on …"  

If you hesitate >3 seconds on any, re-read that part.

---
