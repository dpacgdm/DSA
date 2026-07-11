# GRAPHS I — THE COMPLETE LESSON

**Module:** 7 (Graphs I)  
**Status:** `taught` content delivery — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Arrays, Hashing, Queues (`deque`), Recursion / call stack, Trees (BFS/DFS intuition).  
**Deferred to Module 8:** Dijkstra, Union-Find, MST, shortest paths on weighted graphs.

> **Re-credit unlocked here:** Week 2 PREVIEW #7 Word Ladder Length and #12 Alien Dictionary become **earned** after this module. Full worked solutions are in Parts 11–12. Re-queue both on timed verify for gate credit.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHY GRAPHS EXIST

## The Problem Graphs Solve

Arrays are linear. Trees are hierarchical with **one parent**. Real systems have **many-to-many** relationships:

| Domain | Nodes | Edges |
|---|---|---|
| Social network | People | Friendship / follow |
| Maps / routing | Intersections | Roads |
| Dependencies | Packages / courses / tasks | "A must finish before B" |
| Web | Pages | Hyperlinks |
| Grids / word games | Cells / words | Adjacency / one-letter edits |
| Compilers | Statements / symbols | Data-flow / call edges |

**The interview reason:** once you can model a problem as a graph, you unlock a small set of mechanical frameworks — BFS, DFS, topo sort — that solve an enormous family of problems. The hard part is rarely the loop; it is **seeing the graph**.

## Graph vs Tree (Precise)

A **tree** (rooted, as in Module 5) is a connected undirected acyclic graph with a chosen root — or equivalently, a directed structure where every node except the root has exactly one parent.

A **general graph** allows:
- Multiple parents / cycles
- Disconnected pieces
- Directed edges one way only
- Optional weights on edges

If you treat a cyclic dependency graph like a tree and recurse without a `visited` set, you infinite-loop. That is the #1 graph bug.

---

# PART 2: GRAPH VOCABULARY — PRECISE DEFINITIONS

Interviewers expect exact language. Use these.

### Vertex / Node
An element of the graph. Set of vertices: `V`. Size `|V|` or `n`.

### Edge
A connection between two vertices. Set of edges: `E`. Size `|E|` or `m`.

- **Undirected:** `{u, v}` — bidirectional.
- **Directed (arc):** `(u → v)` — one way.

### Adjacent / Neighbor
`v` is a neighbor of `u` if an edge connects them (for directed: an outgoing edge `u → v`).

### Degree
- Undirected: number of incident edges.
- Directed: **in-degree** (incoming) and **out-degree** (outgoing).

### Path
A sequence of vertices where consecutive pairs are edges. **Simple path:** no repeated vertices.

### Cycle
A path that returns to its start with length ≥ 1 (directed: follow arrow directions). **Simple cycle:** no repeated vertices except start/end.

### Connected (undirected)
Every vertex can reach every other via some path. **Connected component:** a maximal connected subgraph.

### Strongly connected (directed)
Every vertex can reach every other **following directions**. (SCC algorithms are Module 8+ exposure; Graphs I only needs the definition.)

### DAG
**Directed Acyclic Graph** — directed graph with no directed cycles. Topological order exists **iff** the digraph is a DAG.

### Weighted vs unweighted
Edges may carry costs. Graphs I BFS = **unweighted** shortest path (every edge cost 1). Weighted → Dijkstra (Module 8).

### Dense vs sparse
- **Sparse:** `|E|` is O(`|V|`) or O(`|V| log |V|`) — typical interview graphs.
- **Dense:** `|E|` approaches `|V|²`.

### Self-loop / Multiedge
Self-loop: `u → u`. Multiedge: multiple edges between same pair. Mention if input allows; most LC problems do not.

---

# PART 3: GRAPH TYPES — DECISION TABLE

| Type | Edges | Cycles? | Typical algorithms (Graphs I) |
|---|---|---|---|
| Undirected unweighted | `{u,v}` | Possible | BFS, DFS, components, bipartite, cycle detect |
| Directed unweighted | `u→v` | Possible | DFS, Kahn/topo, directed cycle |
| DAG | Directed | **No** | Topo sort (Kahn or DFS finish) |
| Implicit | Generated on the fly | Varies | BFS/DFS with neighbor function |
| Weighted | Costs on edges | Varies | **PREVIEW** — Dijkstra Module 8 |

**Bipartite graph:** vertices colorable with 2 colors so every edge joins different colors. Equivalent: no odd cycle. Check with BFS/DFS 2-coloring.

---

# PART 4: REPRESENTATION — ADJACENCY LIST VS MATRIX

## 4A: Adjacency List (Default Interview Choice)

Store, for each vertex, a list (or set) of neighbors.

```python
from collections import defaultdict

# Undirected: add both directions
def build_undirected(n, edges):
    """
    n = number of vertices labeled 0..n-1
    edges = list of [u, v]
    """
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# Directed: one direction
def build_directed(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    return graph


# When labels are strings / arbitrary hashables:
def build_generic(edges, undirected=False):
    graph = defaultdict(list)
    nodes = set()
    for u, v in edges:
        graph[u].append(v)
        nodes.add(u)
        nodes.add(v)
        if undirected:
            graph[v].append(u)
    return graph, nodes
```

### Space
`O(V + E)` — one slot per vertex plus one entry per directed endpoint (undirected edge stored twice → still `O(V + E)`).

### Time
| Query | Cost |
|---|---|
| Iterate all neighbors of `u` | `O(deg(u))` |
| Check if edge `u–v` exists | `O(deg(u))` with list; `O(1)` avg with `set` |
| Iterate all edges | `O(V + E)` |

**Python tip:** use `list` when you only iterate neighbors. Use `set` when you need fast membership or must avoid duplicate edges.

```python
graph = defaultdict(set)
graph[u].add(v)
```

---

## 4B: Adjacency Matrix

`matrix[u][v] = 1` (or weight) if edge exists, else `0`.

```python
def build_matrix(n, edges, directed=False):
    mat = [[0] * n for _ in range(n)]
    for u, v in edges:
        mat[u][v] = 1
        if not directed:
            mat[v][u] = 1
    return mat
```

### Space
`O(V²)` always — even if the graph is sparse.

### Time
| Query | Cost |
|---|---|
| Check edge `u–v` | **O(1)** |
| Iterate neighbors of `u` | **O(V)** (scan whole row) |
| Iterate all edges | `O(V²)` |

---

## 4C: Tradeoff Cheat Sheet (Memorize)

| Need | Prefer | Why |
|---|---|---|
| Sparse graph (interview default) | **Adj list** | Space `O(V+E)`; neighbor scan `O(deg)` |
| Dense graph / many edge queries | Matrix | O(1) edge check; space already ~`V²` |
| BFS / DFS / topo | **Adj list** | Algorithms walk neighbors |
| Floyd-Warshall all-pairs | Matrix | Natural `dp[i][j]` (Module 8+) |
| Edge existence hot path | Matrix or `set` neighbors | Avoid O(deg) scans |

**Interview default sentence:**  
> "I'll use an adjacency list — space O(V+E), and BFS/DFS run in O(V+E)."

---

## 4D: Edge List Alone

Sometimes input is only `edges = [[u,v], ...]`. That is fine for building a graph, but **do not BFS on an edge list** — each step would scan all edges → O(E) per hop → catastrophic. Always convert to adj list first.

---

# PART 5: COMPLEXITY O(V + E) — DEEP DIVE

## Why Almost Every Graph Traversal Is O(V + E)

Canonical BFS/DFS with a `visited` set:

1. Each vertex is **enqueued / recursed into at most once** (marked visited when first discovered).
2. When you process vertex `u`, you scan its neighbor list once → total neighbor scans = `Σ deg(u) = Θ(E)` (directed) or `2|E|` (undirected).
3. Overhead to touch all vertices (even isolates) is `O(V)`.

**Total: O(V + E).**

This is not a slogan — it is an accounting identity:

```
time = (work per vertex) × V  +  (work per edge endpoint) × E
```

If your "BFS" re-visits nodes without a visited set, or regenerates neighbors from scratch poorly, you leave O(V+E).

## Common Ways People Blow O(V + E)

| Mistake | Actual complexity |
|---|---|
| No `visited` → reprocess nodes | Exponential / infinite |
| For each node, scan **all edges** to find neighbors | O(V·E) |
| Adj matrix neighbor scan without care | O(V²) even if sparse |
| Word Ladder: compare all pairs every step | Extra × n factor (see Part 11) |
| Copying huge neighbor lists carelessly | Extra time/space constants |

## Space

| Structure | Space |
|---|---|
| Adj list | O(V + E) |
| `visited` set / array | O(V) |
| BFS queue (worst) | O(V) |
| DFS recursion stack (worst path) | O(V) |
| Parent / dist arrays | O(V) |

**Interview line:** Time O(V+E), space O(V+E) dominated by the graph itself; auxiliary O(V).

## Isolated Vertices

If the problem gives `n` nodes `0..n-1` and an edge list, **isolates still count**. Loop `for start in range(n)` when you need all components. If nodes are only those appearing in edges, build the node set explicitly.

---

# PART 6: BFS FRAMEWORK

## 6A: Mental Model

BFS explores in **layers** (distance rings) from a source:

```
Level 0:  start
Level 1:  all neighbors of start
Level 2:  new neighbors of level-1 nodes
...
```

Uses a **queue** (FIFO). First time you reach a node in an **unweighted** graph, that path is a **shortest path** (fewest edges).

**Analogy (from queues):** BFS is the same shape as level-order on trees — but you must mark `visited` because graphs can have cross edges and cycles.

## 6B: The Mechanical Template

```python
from collections import deque

def bfs(graph, start):
    """
    graph: list[list[int]] or dict[node, list[node]]
    Returns: dist map (fewest edges from start); unreachable absent or inf
    """
    q = deque([start])
    dist = {start: 0}          # also serves as visited

    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

### Level-by-level variant (when you need "layers")

```python
def bfs_levels(graph, start):
    q = deque([start])
    visited = {start}
    level = 0
    while q:
        for _ in range(len(q)):          # process exactly this layer
            u = q.popleft()
            # work on u at `level`
            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        level += 1
    return level  # meaning depends on problem
```

**TRAP:** `for _ in range(len(q))` must capture length **before** the loop body grows the queue. That freezes the current layer size.

## 6C: Multi-Source BFS

When many starts are equivalent (rotting oranges, gates-and-walls):

```python
q = deque(sources)
dist = {s: 0 for s in sources}
# same loop — first touch wins → shortest to nearest source
```

## 6D: Reconstruct Path

Keep `parent[v] = u` when you first discover `v` from `u`. Then walk backward from target to start and reverse.

```python
def bfs_path(graph, start, target):
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        if u == target:
            break
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                q.append(v)
    if target not in parent:
        return None
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path
```

## 6E: When BFS Is the Right Tool

| Signal in the problem | Why BFS |
|---|---|
| "Shortest" / "minimum steps" / "least moves" | Unweighted shortest path |
| "Level order" / "by distance rings" | Natural layers |
| Spread / infection / multi-source | Multi-source BFS |
| Implicit graph, unit cost edges | Same |

**Not BFS:** weighted edges with different costs → Dijkstra (Module 8). "Any path exists" can be DFS or BFS; shortest → BFS.

---

# PART 7: DFS FRAMEWORK

## 7A: Mental Model

DFS goes **deep** along one branch before backtracking. Uses the **call stack** (recursive) or an explicit **stack** (iterative).

Trees: DFS felt natural because no cycles. Graphs: **always track visited** (or a 3-color state for directed cycle / topo).

## 7B: Recursive DFS Template

```python
def dfs_recursive(graph, start):
    visited = set()

    def dfs(u):
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v)

    dfs(start)
    return visited
```

### Preorder vs postorder hooks

```python
def dfs(u):
    visited.add(u)
    # PRE: enter node
    for v in graph[u]:
        if v not in visited:
            dfs(v)
    # POST: all descendants done — finishing time lives here
```

**Finishing time** (postorder leave) is the key for DFS topological sort.

## 7C: Iterative DFS (Explicit Stack)

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                stack.append(v)
    return visited
```

**TRAP:** Iterative DFS with a single "visit on pop" does **not** easily give correct finishing times for topo sort. For topo / directed cycle, prefer **recursive DFS with colors** or Kahn's algorithm.

**Neighbor order:** stack reverses neighbor processing order vs recursion depending on push order. For "visit all reachable," order usually does not matter. For deterministic output, sort neighbors or use Kahn with a heap.

## 7D: Recursion Depth

Worst-case path length = O(V). Python default recursion limit ~1000. For large V in interviews, mention iterative DFS or Kahn if needed. LC constraints often fit; still know the issue.

## 7E: BFS vs DFS — Decision

| Goal | Prefer |
|---|---|
| Shortest path (unweighted) | **BFS** |
| Connected components | Either |
| Cycle detect undirected | Either (DFS parent trick common) |
| Cycle detect directed | DFS 3-color **or** Kahn leftover |
| Topo sort | Kahn **or** DFS finish |
| Path existence / flood fill | Either |
| Explicit "levels" | BFS |

---

# PART 8: CONNECTED COMPONENTS (UNDIRECTED)

## 8A: Framework

```
components = 0
visited = empty
for each vertex u:
    if u not visited:
        components += 1
        BFS or DFS from u  # marks the whole component
```

```python
def count_components(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)

    count = 0
    for u in range(n):
        if not visited[u]:
            count += 1
            dfs(u)
    return count
```

**Complexity:** O(V + E) — each vertex/edge touched once across all searches.

## 8B: Number of Islands (Grid = Implicit Graph)

Treat each land cell as a node; edges to 4-directional land neighbors.

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # mark visited in-place
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count
```

**TRAP:** Forgetting bounds checks; visiting water; not marking visited → infinite recursion on cycles of land.

---

# PART 9: BIPARTITE CHECK (2-COLORING)

## 9A: Idea

Try to color the graph with colors `0` and `1` so every edge joins different colors. BFS or DFS. Conflict → not bipartite.

Odd cycle ⇔ not bipartite.

```python
from collections import deque

def is_bipartite(graph):
    """
    graph: list[list[int]] for nodes 0..n-1 (undirected)
    """
    n = len(graph)
    color = [-1] * n  # -1 = uncolored

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

**Must loop all starts** — disconnected graphs can have one bipartite component and one that is not; also an uncolored component needs its own seed color.

**Complexity:** O(V + E).

---

# PART 10: CYCLE DETECTION

## 10A: Undirected — DFS With Parent

An edge to an already-visited neighbor that is **not** your parent means a cycle (back edge).

```python
def has_cycle_undirected(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    def dfs(u, parent):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for u in range(n):
        if not visited[u]:
            if dfs(u, -1):
                return True
    return False
```

**TRAP:** Treating the parent edge as a cycle. Always pass `parent`.

## 10B: Directed — Three-Color DFS

| Color | Meaning |
|---|---|
| WHITE (0) | Unvisited |
| GRAY (1) | On the current recursion stack (being explored) |
| BLACK (2) | Fully finished |

**Back edge:** edge to a **GRAY** node → cycle.

```python
def has_cycle_directed(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in range(n):
        if color[u] == WHITE:
            if dfs(u):
                return True
    return False
```

**TRAP:** Using undirected logic on directed graphs. Edge to BLACK is fine (cross/forward to finished node), not a cycle.

## 10C: Directed Cycle via Kahn

Run topological BFS. If you cannot order all vertices (`len(result) < V`), a cycle exists. Same machinery as Part 11 Kahn — cycle detection is free.

---

# PART 11: TOPOLOGICAL SORT

## 11A: What It Is

A **topological order** of a digraph is a linear order of vertices such that for every edge `u → v`, `u` appears before `v`.

**Exists iff the graph is a DAG.**

**Use cases:** course schedule, build order, alien alphabet, task scheduling with prerequisites.

**Convention in this lesson:** edge `u → v` means **u must come before v** (u is a prerequisite of v). Some problems draw the arrow the other way — **read the problem** and stay consistent when you build edges.

## 11B: Kahn's Algorithm (BFS / Indegree)

```
1. Compute indegree[v] for all v
2. Queue all nodes with indegree 0
3. While queue not empty:
     pop u, append u to order
     for each neighbor v of u:
         indegree[v] -= 1
         if indegree[v] == 0: enqueue v
4. If order length < V: cycle → impossible
```

```python
from collections import deque

def topo_kahn(n, edges):
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:          # u before v
        graph[u].append(v)
        indeg[v] += 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != n:
        return None  # cycle
    return order
```

### Trace

```
n=4, edges: 0→1, 0→2, 1→3, 2→3

indeg: [0,1,1,2]
queue: [0]
pop 0 → order [0]; indeg[1]=0, indeg[2]=0 → queue [1,2]
pop 1 → order [0,1]; indeg[3]=1
pop 2 → order [0,1,2]; indeg[3]=0 → queue [3]
pop 3 → order [0,1,2,3]
len=4 ✅
```

Valid orders include `[0,1,2,3]` and `[0,2,1,3]` — topo is not always unique.

**Complexity:** O(V + E).

**Interview preference:** Kahn is easy to code, naturally detects cycles, and matches "peel sources layer by layer."

## 11C: DFS Finishing Times

Run DFS. When a node **finishes** (postorder), push it on a stack. Pop stack → topological order.

**Why:** for edge `u → v`, v finishes before u (in a DAG), so u is pushed after v; reversing finishing order puts u before v.

```python
def topo_dfs(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    stack = []
    cycle = False

    def dfs(u):
        nonlocal cycle
        if cycle:
            return
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                cycle = True
                return
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
        stack.append(u)  # finished

    for u in range(n):
        if color[u] == WHITE:
            dfs(u)
            if cycle:
                return None

    stack.reverse()
    return stack
```

**TRAP:** Preorder push is wrong. Must push on **finish**.

## 11D: Kahn vs DFS Topo

| | Kahn | DFS finish |
|---|---|---|
| Data structure | Queue + indegrees | Recursion + colors |
| Cycle detect | `len(order) < V` | GRAY back edge |
| Intuition | Peel sources | Finish dependencies first |
| Unique order? | Neither guarantees uniqueness | Same |

Know **both**. Interviews often accept either; Alien Dictionary classically uses Kahn.

---

# PART 12: IMPLICIT GRAPHS

## 12A: The Idea

You never build an explicit adj list. A **state** is a node. A **neighbor function** generates next states.

| Problem | Node | Edge |
|---|---|---|
| Word Ladder | word | one-letter change to a word in dict |
| Grid shortest path | cell `(r,c)` | step to adjacent open cell |
| Lock / dial | digit string | rotate one wheel ±1 |
| Knight moves | board square | knight leap |
| Jump Game II style | index | jump edges (sometimes BFS) |

**Template:**

```python
from collections import deque

def bfs_implicit(start, is_target, neighbors_fn):
    q = deque([start])
    dist = {start: 0}
    while q:
        u = q.popleft()
        if is_target(u):
            return dist[u]
        for v in neighbors_fn(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return -1
```

**Key skill:** define state carefully. Too coarse → wrong; too fine (extra unused dimensions) → TLE.

## 12B: Neighbor Generation Cost

Word Ladder: naive "compare to every word" is O(n) per node. Pattern trick / 26×L generation is usually better (Part 13). Always account for neighbor-gen in complexity:  
`O( (V_touched) × cost(neighbors) )`, with V_touched ≤ state space.

---

# PART 13: WORD LADDER LENGTH — EARNED RE-CREDIT

> **Re-credit:** Week 2 Problem 7 was **PREVIEW**. After Graphs I, it is an **earned** BFS-on-implicit-graph problem. Re-queue on timed verify for gate credit.

## 13A: Problem

Given `beginWord`, `endWord`, and a word list, find the length of the **shortest** transformation sequence from begin to end such that:

- You may change **one letter** at a time
- Every intermediate word (and typically the end) must be in the word list

Return `0` if impossible.

```
Input: beginWord = "hit", endWord = "cog"
       wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: hit → hot → dot → dog → cog
```

## 13B: Graph Model

- **Nodes:** `beginWord` + all words in the list (that you can reach).
- **Edge:** between words of equal length that differ by exactly one character.
- **Ask:** shortest path length in an **unweighted** graph → **BFS**.
- Length in LC 127 counts **words in the sequence** (nodes), not edges. `hit→…→cog` has 5 words = 4 edges; return 5.

**Why not DFS?** DFS finds *a* path, not the shortest. BFS level order guarantees minimum steps.

## 13C: Neighbor Generation

**Bad:** for each word, compare to all others → O(n² L) preprocess or O(n L) per expansion.

**Good:** for current word length L, try all 26 letters at each of L positions → 26L candidates; O(1) avg set lookup:

```text
cost per dequeued word: O(26 · L · L) if string hashing is O(L)
words dequeued ≤ n
→ O(n · 26 · L²) often written O(n · L · 26) with care about hash cost
```

## 13D: Full Correct Implementation

```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    q = deque([(begin_word, 1)])  # (word, sequence_length)
    visited = {begin_word}

    while q:
        word, length = q.popleft()
        if word == end_word:
            return length

        for i in range(len(word)):
            orig = word[i]
            for ord_c in range(26):
                c = chr(ord("a") + ord_c)
                if c == orig:
                    continue
                nxt = word[:i] + c + word[i + 1 :]
                if nxt in word_set and nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, length + 1))
    return 0
```

**Variant:** check `nxt == end_word` on generation and `return length + 1` early — same idea.

**Optimization (optional interview flex):** bidirectional BFS from begin and end; still same pattern family.

## 13E: Full Trace

```
begin = "hit", end = "cog"
word_set = {hot, dot, dog, lot, log, cog}

Queue: [(hit, 1)]
visited: {hit}

Process hit (len 1):
  neighbors in set: hot
  enqueue (hot, 2)

Process hot (len 2):
  neighbors: dot, lot  (hit already visited)
  enqueue (dot, 3), (lot, 3)

Process dot (len 3):
  neighbors: dog
  enqueue (dog, 4)

Process lot (len 3):
  neighbors: log
  enqueue (log, 4)

Process dog (len 4):
  neighbors: cog → enqueue (cog, 5)  [or early return 5]

Process cog (len 5): return 5 ✅
```

## 13F: Edge Cases

| Case | Result |
|---|---|
| `endWord` not in list | 0 |
| `beginWord == endWord` | Problem-dependent; LC usually begin ≠ end; if equal, often 1 |
| No path | BFS exhausts → 0 |
| begin not in list | Still OK — begin is a virtual node |
| Duplicate words in list | `set` handles |

## 13G: Complexity

Let `n = |wordList|`, `L = word length`.

> **Time: O(n · L · 26 · L)** with string build/hash, commonly stated **O(n · L · 26)**  
> **Space: O(n · L)** for the set + visited + queue

## 13H: Interview Communication

1. "Shortest transformation → unweighted shortest path → BFS."  
2. "Implicit graph: words as nodes; one-letter edits as edges."  
3. "Generate neighbors with 26×L, not all-pairs."  
4. "Return node-count length; mark visited when enqueue to keep O(V+E)-style."  

---

# PART 14: ALIEN DICTIONARY — EARNED RE-CREDIT

> **Re-credit:** Week 2 Problem 12 was **PREVIEW**. After Graphs I, it is an **earned** graph + topological sort problem. Re-queue on timed verify for gate credit.

## 14A: Problem

You are given a list of words **sorted** in an alien language's dictionary order. Derive **a** valid alphabet order of characters. If multiple orders exist, any valid one is OK (or the problem specifies lexicographically smallest — then use a min-heap instead of a deque). If the input is **invalid**, return `""`.

```
Input: ["wrt", "wrf", "er", "ett", "rftt"]
Output: "wertf"

Input: ["z", "x"]
Output: "zx"

Input: ["z", "x", "z"]
Output: ""   # contradiction / cycle
```

## 14B: Pipeline (Four Pieces)

1. **Compare adjacent words** → extract precedence constraints.  
2. Build a **directed graph** on characters.  
3. **Topological sort** (Kahn).  
4. **Cycle / invalid prefix** → return `""`.

Only **adjacent** pairs in the sorted list are needed: non-adjacent order is implied by transitivity if the list is globally sorted.

## 14C: Extracting an Edge

For adjacent `w1`, `w2` (w1 before w2 in alien order):

- Find first index `j` where `w1[j] != w2[j]`.
- Then `w1[j]` comes **before** `w2[j]` → edge `w1[j] → w2[j]` (prerequisite style: from earlier char to later char).
- **Break** after first difference — later characters do not give a direct constraint from this pair.

**Invalid prefix rule:** If `w1` is longer than `w2` and `w2` is a prefix of `w1` (e.g. `"apple"` before `"app"`), the ordering is illegal → `""`.

## 14D: Full Correct Implementation (Kahn)

```python
from collections import deque, defaultdict

def alien_order(words):
    # 1. Nodes = all unique characters
    graph = defaultdict(set)
    indeg = {}
    for w in words:
        for ch in w:
            if ch not in indeg:
                indeg[ch] = 0
                graph[ch] = set()

    # 2. Edges from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""

        for j in range(min_len):
            if w1[j] != w2[j]:
                a, b = w1[j], w2[j]  # a before b
                if b not in graph[a]:
                    graph[a].add(b)
                    indeg[b] += 1
                break

    # 3. Kahn
    q = deque([c for c in indeg if indeg[c] == 0])
    order = []
    while q:
        c = q.popleft()
        order.append(c)
        for nxt in graph[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    # 4. Cycle?
    if len(order) != len(indeg):
        return ""
    return "".join(order)
```

## 14E: Full Trace — Valid

```
words = ["wrt", "wrf", "er", "ett", "rftt"]

Chars: {w,r,t,f,e}

Pairs:
  wrt vs wrf → t before f     t→f
  wrf vs er  → w before e     w→e
  er  vs ett → r before t     r→t
  ett vs rftt → e before r    e→r

graph: w:{e}, e:{r}, r:{t}, t:{f}, f:{}
indeg: w:0, e:1, r:1, t:1, f:1

Kahn:
  queue [w]
  w → order w; e indeg 0 → [e]
  e → we; r indeg 0 → [r]
  r → wer; t indeg 0 → [t]
  t → wert; f indeg 0 → [f]
  f → wertf

len 5 == 5 → "wertf" ✅
```

## 14F: Full Trace — Cycle

```
words = ["z", "x", "z"]
z→x and x→z
indeg both 1 → queue empty → order [] → "" ✅
```

## 14G: Edge Cases

| Case | Handling |
|---|---|
| Single word | No edges; any order of its distinct chars |
| Duplicate adjacent words | No new edge |
| Prefix violation | Immediate `""` |
| Disconnected letters | All appear in indeg; multiple indeg-0 OK |
| Need lex-smallest order | Use `heapq` instead of `deque` for sources |

## 14H: Complexity

Let `C` = total characters across words, `V` ≤ 26 unique letters, `E` ≤ V² (tiny).

> **Time: O(C + V + E) = O(C)** for English letters  
> **Space: O(V + E)**

## 14I: Interview Communication

1. "Sorted alien words → compare adjacent pairs for inequalities."  
2. "Characters = nodes; precedence = directed edges."  
3. "Topo sort; cycle or bad prefix → invalid."  
4. "Only first differing character per adjacent pair."  

---

# PART 15: WORKED PROBLEMS (WITH TRACES)

## Problem 1: Clone Graph

Each node has `val` and `neighbors` list. Clone the entire connected component.

**Pattern:** DFS or BFS + hash map `old → new`.

```python
def clone_graph(node):
    if not node:
        return None
    clones = {}

    def dfs(u):
        if u in clones:
            return clones[u]
        copy = Node(u.val)
        clones[u] = copy
        for v in u.neighbors:
            copy.neighbors.append(dfs(v))
        return copy

    return dfs(node)
```

**Trace (triangle 1—2—3—1):**  
Visit 1 → create copy1; neighbor 2 → create copy2; neighbor 3 → create copy3; 3's neighbor 1 already in map → link. Undirected links filled as recursion returns.

> **Time/Space: O(V + E)**

---

## Problem 2: Course Schedule (Can Finish?)

`numCourses`, prerequisites ` [a,b] ` meaning b before a (b → a). Return whether you can finish all.

**Pattern:** Cycle detection in digraph = Kahn or 3-color DFS.

```python
from collections import deque

def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:  # b before a
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num_courses) if indeg[i] == 0])
    taken = 0
    while q:
        u = q.popleft()
        taken += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == num_courses
```

**Trace:** `2, [[1,0]]` → edge 0→1; order [0,1]; True.  
`2, [[1,0],[0,1]]` → cycle; taken < 2; False.

> **Time: O(V + E)**

---

## Problem 3: Course Schedule II (Return Order)

Same as above but return a topo order (or empty list if cycle).

```python
def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num_courses) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []
```

---

## Problem 4: Number of Provinces

`isConnected[i][j] == 1` means city i–j linked (undirected). Count connected components.

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    visited = [False] * n

    def dfs(i):
        for j in range(n):
            if is_connected[i][j] and not visited[j]:
                visited[j] = True
                dfs(j)

    count = 0
    for i in range(n):
        if not visited[i]:
            visited[i] = True
            dfs(i)
            count += 1
    return count
```

**Note:** Input is an adj **matrix** — neighbor scan is O(V) per vertex → O(V²) time, which matches dense input size.

---

## Problem 5: Is Graph Bipartite?

LC 785 — `graph` is adj list for undirected graph.

```python
from collections import deque

def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

**Trace (odd cycle):** edges 0-1, 1-2, 2-0.  
Color 0←0, 1←1, 2←0; edge 2-0 same color → **False**.

**Trace (even cycle):** 0-1, 1-2, 2-3, 3-0 → colors 0,1,0,1 → **True**.

> **Time: O(V+E)**

---

## Problem 6: Shortest Path in Binary Matrix

Grid of 0/1; move 8 directions; shortest clear path from (0,0) to (n-1,n-1).

**Pattern:** BFS on grid implicit graph; each step cost 1.

```python
from collections import deque

def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1
    q = deque([(0, 0, 1)])
    grid[0][0] = 1  # visited
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    while q:
        r, c, d = q.popleft()
        if r == n-1 and c == n-1:
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                q.append((nr, nc, d + 1))
    return -1
```

> **Time: O(n²)**

---

## Problem 7: Rotting Oranges (Multi-Source BFS)

0 empty, 1 fresh, 2 rotten. Each minute, rotten infects adjacent fresh. Minutes until all fresh rotten, or -1.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    mins = 0
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while q:
        r, c, t = q.popleft()
        mins = t
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return mins if fresh == 0 else -1
```

**Trace:** all initial 2s in queue at t=0 → infection expands in rings = multi-source BFS.

---

## Problem 8: Open the Lock

4-wheel lock, deadends, target. Each move rotate one wheel ±1. Shortest moves.

**Pattern:** Implicit BFS; state = 4-char string; 8 neighbors.

```python
from collections import deque

def open_lock(deadends, target):
    dead = set(deadends)
    start = "0000"
    if start in dead:
        return -1
    q = deque([(start, 0)])
    seen = {start}

    def neighbors(s):
        res = []
        for i in range(4):
            x = int(s[i])
            for d in (-1, 1):
                y = (x + d) % 10
                res.append(s[:i] + str(y) + s[i+1:])
        return res

    while q:
        cur, dist = q.popleft()
        if cur == target:
            return dist
        for nxt in neighbors(cur):
            if nxt not in seen and nxt not in dead:
                seen.add(nxt)
                q.append((nxt, dist + 1))
    return -1
```

---

## Problem 9: Detect Cycle in Directed Graph (Explicit)

Use Part 10B. Interview follow-up: return any cycle path via recursion stack tracking — optional stretch.

---

## Problem 10: All Paths From Source to Target (DAG)

LC 797 — graph is a DAG given as adj list. DFS backtracking enumerate paths.

```python
def all_paths_source_target(graph):
    n = len(graph)
    paths = []
    path = [0]

    def dfs(u):
        if u == n - 1:
            paths.append(path[:])
            return
        for v in graph[u]:
            path.append(v)
            dfs(v)
            path.pop()

    dfs(0)
    return paths
```

**Why no visited?** DAG → no cycles. On general graphs you must mark/unmark along the path carefully.

> **Time:** O(V + E) to explore structure, but **output size** can be exponential in paths — state that in interviews.

---

## Problem 11: Keys and Rooms

`rooms[i]` = list of keys in room i. Start in room 0. Can you visit all rooms?

**Pattern:** DFS/BFS reachability from 0 on directed graph room→key→room.

```python
def can_visit_all_rooms(rooms):
    n = len(rooms)
    seen = set()
    stack = [0]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        for k in rooms[u]:
            if k not in seen:
                stack.append(k)
    return len(seen) == n
```

**Trace:** `[[1],[2],[3],[]]` → 0→1→2→3 → True.  
`[[1,3],[3,0,1],[2],[0]]` → never reach 2 → False.

> **Time: O(V+E)** keys as edges

---

## Problem 12: Pacific Atlantic Water Flow (Grid Multi-Source)

Heights grid. Ocean touches top/left (Pacific) and bottom/right (Atlantic). Return cells that can flow to **both** oceans (water flows to neighbor with height ≤ current).

**Pattern:** Reverse the edges — multi-source DFS/BFS **inland from each ocean**, intersect reachable sets.

```python
def pacific_atlantic(heights):
    if not heights:
        return []
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    def dfs(r, c, seen):
        seen.add((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in seen
                    and heights[nr][nc] >= heights[r][c]):
                dfs(nr, nc, seen)

    for c in range(cols):
        dfs(0, c, pac)
        dfs(rows - 1, c, atl)
    for r in range(rows):
        dfs(r, 0, pac)
        dfs(r, cols - 1, atl)

    return list(pac & atl)
```

**Insight:** "Can flow to ocean" ≡ "ocean can climb uphill in reverse." Classic Graphs I transfer problem.

> **Time: O(R·C)**

---

## Problem 13: Surrounded Regions

Board `'X'`/`'O'`. Capture all `'O'` regions **fully surrounded** by `'X'` (flip to `'X'`). Border-connected `'O'`s are safe.

**Pattern:** DFS/BFS from all border `'O'`s mark safe; then flip unmarked `'O'` → `'X'`.

```python
def solve(board):
    if not board:
        return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != "O":
            return
        board[r][c] = "S"  # safe
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        dfs(r, 0); dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c); dfs(rows - 1, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "S":
                board[r][c] = "O"
```

> **Time: O(R·C)**

---

## Problem 14: Minimum Genetic Mutation

Same family as Word Ladder: gene string length 8, alphabet `ACGT`, bank of valid genes. Return min mutations begin→end, or -1.

**Pattern:** Implicit BFS; neighbors = 8 positions × 3 other letters, must be in bank.

```python
from collections import deque

def min_mutation(start, end, bank):
    bank_set = set(bank)
    if end not in bank_set:
        return -1
    q = deque([(start, 0)])
    seen = {start}
    while q:
        gene, dist = q.popleft()
        if gene == end:
            return dist
        for i in range(len(gene)):
            for ch in "ACGT":
                if ch == gene[i]:
                    continue
                nxt = gene[:i] + ch + gene[i+1:]
                if nxt in bank_set and nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, dist + 1))
    return -1
```

**Interview note:** If you solved Word Ladder, this is the same template with a smaller alphabet — say that out loud.

---

## Problem 15: Parallel Courses (Topo + Levels)

`n` courses, relations `[prev, next]`. Return **minimum semesters** to finish all (any number of courses with indegree 0 in parallel), or -1 if cycle.

**Pattern:** Kahn **by levels** — each BFS layer = one semester.

```python
from collections import deque

def minimum_semesters(n, relations):
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        graph[a].append(b)
        indeg[b] += 1
    q = deque([i for i in range(1, n + 1) if indeg[i] == 0])
    semesters = 0
    taken = 0
    while q:
        for _ in range(len(q)):
            u = q.popleft()
            taken += 1
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        semesters += 1
    return semesters if taken == n else -1
```

**Trace:** `n=3`, relations `[[1,3],[2,3]]` → semester1: {1,2}; semester2: {3} → **2**.

This combines **topo + BFS levels** — high-yield interview hybrid.

---

# PART 15B: FULL TRACE GALLERY (MECHANICAL)

## Trace G1: BFS parent reconstruction

```
Undirected: 0-1, 0-2, 1-3, 2-3, 3-4
start=0, target=4

Discover:
  0 parent None
  1 parent 0, 2 parent 0
  3 parent 1   (first touch; ignore later from 2)
  4 parent 3

Path walk: 4←3←1←0 → [0,1,3,4]
dist[4]=3
```

## Trace G2: Kahn with a cycle leftover

```
edges: 0→1, 1→2, 2→1
indeg: 0:0, 1:2, 2:1
queue: [0]
pop 0 → order [0]; indeg[1]=1
queue empty while 1,2 still positive indeg
len(order)=1 < 3 → cycle involving {1,2}
```

## Trace G3: DFS finish order (DAG)

```
edges: 0→1, 0→2, 1→3, 2→3

One DFS from 0:
  enter 0 → enter 1 → enter 3 → finish 3 → finish 1
         → enter 2 → (3 black) → finish 2
  finish 0
finish stack push order: 3,1,2,0
reverse → [0,2,1,3] or depending on neighbor order [0,1,2,3]
Both valid topo orders.
```

## Trace G4: Bipartite conflict mid-component

```
graph: 0:[1,3], 1:[0,2], 2:[1,3], 3:[0,2]  # C4 even — OK
Add 1-3: now odd cycle 1-2-3-1
BFS: color[0]=0,1=1,3=1 → edge 1-3 both color 1 → False
```

---

# PART 16: EDGE CASES & TRAPS

| Trap | Fix |
|---|---|
| Forgetting `visited` | Infinite loops on cycles |
| Undirected parent edge counted as cycle | Pass `parent` into DFS |
| Directed: edge to BLACK treated as cycle | Only GRAY = back edge |
| Topo on undirected graph | Meaningless — need directed constraints |
| Arrow direction flipped vs problem statement | Write one example edge before coding |
| Kahn without isolates | Loop `0..n-1`, not only nodes in edges |
| BFS "shortest" on weighted graph | Wrong — need Dijkstra |
| Mark visited too late in BFS | Multiple queue copies of same node → blowup; mark on enqueue |
| Alien: constraints from non-adjacent only | Adjacent pairs suffice if list sorted |
| Alien: ignore prefix rule | `"abc"` before `"ab"` must return invalid |
| Word Ladder DFS | Not shortest |
| Building matrix for sparse LC graph | Wastes space; use list |
| Recursion on V=10^5 chain | Prefer iterative / Kahn |
| Modifying graph while iterating neighbors | Iterate over a copy or collect first |

---

# PART 17: CONSOLIDATED CHEAT SHEETS

## 17A: Representation

| | Adj List | Adj Matrix |
|---|---|---|
| Space | O(V+E) | O(V²) |
| Edge check | O(deg) / O(1) with set | O(1) |
| BFS/DFS | Natural | Neighbor scan O(V) |
| Default | **Yes** | Dense / Floyd |

## 17B: Algorithm Picker

```
Shortest path, unit edges?     → BFS
Reachability / flood / islands → DFS or BFS
Components (undirected)?       → multi-source DFS/BFS count
Bipartite?                     → 2-color BFS/DFS
Cycle undirected?              → DFS + parent
Cycle directed?                → 3-color DFS or Kahn incomplete
Ordering with prerequisites?   → Topo (Kahn or DFS finish)
Word mutations / locks / grid? → Implicit BFS
Weighted shortest?             → PREVIEW Module 8 Dijkstra
```

## 17C: Templates (Memorize Structure)

**BFS:** queue + dist/visited; mark on enqueue; O(V+E).

**DFS recursive:** visited; pre/post hooks; post = finish.

**Kahn:** indegree → queue zeros → peel → if `len < V` cycle.

**2-color:** `color[v] = 1 - color[u]`; conflict if same.

## 17D: Complexity One-Liners

- Traversal: **O(V + E)** time, **O(V)** aux (+ graph storage).  
- Matrix input dense: **O(V²)**.  
- Word Ladder: **O(n · 26 · L²)** style.  
- Alien: **O(C)** for fixed alphabet.

## 17E: Interview Opening Script

> "I'll model this as a graph where nodes are __ and edges mean __. The graph is [directed/undirected], [weighted/unweighted]. Because we need __, I'll use __. Time O(V+E), space O(V+E)."

Fill the blanks out loud before coding.

---

# PART 18: WHAT IS NOT IN GRAPHS I (NAMED DEFERRALS)

| Topic | Where |
|---|---|
| Dijkstra / 0-1 BFS | Module 8 |
| Union-Find (DSU) | Module 8 |
| MST (Kruskal/Prim) | Module 8 / later |
| Strongly connected components (Kosaraju/Tarjan) | Later exposure |
| Bellman-Ford / SPFA / Floyd | Later |
| Max flow | Not Phase A core |

Do not claim those as earned from this file.

---

# PART 19: MODULE 7 MASTERY CHECKLIST

Before marking Graphs I `drilled` → retention → timed:

- [ ] Build adj list (directed + undirected) from edge list in Python cold  
- [ ] Explain O(V+E) accounting in one minute  
- [ ] Code BFS shortest path + level variant without notes  
- [ ] Code recursive DFS + iterative DFS  
- [ ] Count components; bipartite check  
- [ ] Cycle detect undirected (parent) and directed (colors)  
- [ ] Kahn topo + explain DFS finishing-time topo  
- [ ] Word Ladder earned solution with neighbor gen + complexity  
- [ ] Alien Dictionary earned solution with prefix rule + cycle  
- [ ] Identify implicit-graph problems from English prompts  

**Next:** `Retention Questions/Module 7 Retention.md` grill, then timed re-queue for Word Ladder + Alien Dictionary gate credit. Module 8 adds Dijkstra + Union-Find.

---

## 19A: Subskill Ledger Seeds (for Retention Ledger)

| Subskill | Heat start after teach |
|---|---|
| Adj list build (dir / undir) | shaky until coded cold |
| O(V+E) accounting | must be strong before timed |
| BFS shortest + levels + multi-source | core |
| DFS recursive + iterative | core |
| Components / islands | core |
| Bipartite 2-color | core |
| Cycle undirected (parent) | core |
| Cycle directed (3-color) | core |
| Kahn topo | core |
| DFS finish topo | core |
| Implicit BFS (ladder/lock/grid) | core |
| Word Ladder (earned) | re-credit → timed |
| Alien Dictionary (earned) | re-credit → timed |
| Pacific / surrounded transfer | stretch |

---

*End of Graphs I teach block. Status after reading ≠ `complete`. Evidence gates still apply.*
