<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 7 Retention.keys.md -->
> **Blind mode:** Section answer blocks moved to `keys/Module 7 Retention.keys.md`.

# MODULE 7 RETENTION — GRAPHS I

**Purpose:** Cumulative retention grill for Module 7 teach block.  
**Sources:** `Graphs/Graphs I.md`  
**Also pulls (light):** Queues/`deque`, recursion stack, hashing/`set`, tree BFS contrast, Big-O accounting.  
**Rules:** No notes. Identify pattern → approach → code → complexity → edges.  
**Governance:** Word Ladder + Alien Dictionary are **EARNED RE-CREDIT** (formerly Week 2 PREVIEW #7 / #12). Dijkstra / Union-Find items marked **PREVIEW** — recognition only, no Module 8 credit.

---

# SECTION A: RAPID FIRE — CONCEPTS & COMPLEXITY

Answer in 1–3 sentences unless code is requested.

---

## A1. Graph vs tree

In one sentence each: what extra freedom does a general graph have that a rooted binary tree does not? Why does that force a `visited` set?

---

## A2. Representation tradeoff

When do you prefer adjacency **list** vs adjacency **matrix**? Give space for each.

---

## A3. O(V + E) accounting

Why is BFS/DFS O(V + E), not O(V · E)? What goes wrong if you find neighbors by scanning the full edge list every time?

---

## A4. BFS shortest path

In an unweighted graph, why is the first time BFS reaches a node a shortest path (fewest edges)? What changes if edges have different positive weights?

---

## A5. Level freeze

Why does `for _ in range(len(q)):` work for processing one BFS level? What bug appears if you write `while q:` and try to use `len(q)` incorrectly inside?

---

## A6. DFS finishing time

Where in a recursive DFS do you record finishing time — on entry or on exit? Why does that matter for topological sort?

---

## A7. Undirected cycle trap

In undirected cycle detection DFS, why do you pass `parent`? What false positive happens without it?

---

## A8. Directed cycle colors

State what WHITE / GRAY / BLACK mean. Which color on a neighbor proves a directed cycle?

---

## A9. Kahn incomplete

After Kahn's algorithm, `len(order) < V`. What does that mean? Name one other algorithm that detects the same issue.

---

## A10. Bipartite

What graph property is equivalent to "not bipartite"? How does 2-coloring BFS detect it?

---

## A11. Topo existence

Topological order exists iff the digraph is a ____. If the problem is undirected, can you topo-sort it?

---

## A12. Implicit graph

Define an implicit graph in one sentence. Name two interview problems that use one.

---

## A13. Mark on enqueue

In BFS, why mark a node visited when you **enqueue** it (not when you dequeue)? What goes wrong if you mark on dequeue?

---

## A14. Arrow convention

Prerequisites: "b must be taken before a." Do you add edge `a→b` or `b→a` for Kahn where edge means "before → after"? State it clearly.

---

## A15. PREVIEW

In one sentence: what does Dijkstra store in its priority queue, and why is plain BFS wrong for positive weighted edges?

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION B: BFS / DFS / COMPONENTS DRILLS

---

## B1. BFS distances

Undirected graph `n=6`, edges `[[0,1],[0,2],[1,3],[2,3],[3,4]]`, start `0`. Node `5` isolated. List distance from 0 to each node (use `inf` if unreachable).

---

## B2. Code: level-order distances

Write `bfs_dist(graph, start)` returning a `dict` of distances using `deque`. Graph is `List[List[int]]`.

---

## B3. Connected components

`n=5`, edges `[[0,1],[1,2],[3,4]]`. How many components? Which nodes in each?

---

## B4. Number of islands

```
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
```
Return the count. Sketch DFS or BFS approach in ≤5 lines of prose, then complexity.

---

## B5. Bipartite?

Undirected edges on nodes 0..3: `[[0,1],[1,2],[2,3],[3,0]]`. Is it bipartite? Why?

Same nodes with extra edge `[0,2]` — bipartite?

---

## B6. Undirected cycle

`n=4`, edges `[[0,1],[1,2],[2,0],[2,3]]`. Does a cycle exist? Show the DFS parent reasoning when you first detect it.

---

## B7. Directed cycle

`n=3`, edges `0→1, 1→2, 2→0`. Walk 3-color DFS from 0 and show where GRAY is hit.

---

## B8. Clone graph sketch

Why do you need a hash map `old → new`? What goes wrong with a naive recursive clone without it on a cycle of 2 nodes?

---

## B9. Multi-source BFS

Rotting oranges: why put **all** initial rotten oranges in the queue at time 0 instead of running BFS from each separately and taking a min?

---

## B10. Identify the pattern

"Minimum number of moves to go from start state to target where each move changes the state in a small local way; every move costs 1."

Name the pattern.

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION C: TOPOLOGICAL SORT DRILLS

---

## C1. Kahn dry run

`n=4`, edges `0→1, 0→2, 1→3, 2→3`. Show indegrees, queue evolution, one valid order.

---

## C2. Code: Kahn

Write `topo_kahn(n, edges)` returning a list order or `None` if cycle. Edge `u→v` means u before v.

---

## C3. DFS topo vs Kahn

Same graph as C1. Explain in 2–3 sentences how DFS finishing times produce a valid order (no need for full stack trace).

---

## C4. Course Schedule

`numCourses=2`, `prerequisites=[[1,0],[0,1]]`. Can finish? Why?

`numCourses=3`, `[[1,0],[2,0]]`. Give one valid order for Course Schedule II.

---

## C5. Unique order?

Give a tiny DAG with **two** different valid topological orders. What structural feature allows non-uniqueness?

---

## C6. Identify

"Tasks with prerequisites; return order to run them, or detect impossibility."

Name the algorithm family.

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION D: EARNED RE-CREDIT — WORD LADDER + ALIEN DICTIONARY

> Formerly Week 2 PREVIEW #7 and #12. Now **earned** Module 7 credit. Treat as full interview solves.

---

## D1. Word Ladder Length — EARNED

Given `beginWord`, `endWord`, and `wordList`, return length of shortest transformation sequence (each step one letter; intermediates in list), or 0.

```
Input: beginWord = "hit", endWord = "cog"
       wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
```

**Required:** BFS on implicit graph; explain neighbor generation; full trace; complexity.

---

## D2. Word Ladder — variant check

If `endWord = "zog"` (not in list), what do you return and where do you short-circuit?

If someone uses DFS recursion to find *any* ladder and returns its length, what is wrong?

---

## D3. Alien Dictionary — EARNED

```
Input: ["wrt", "wrf", "er", "ett", "rftt"]
Output: "wertf"
```

Extract all edges, run Kahn (or DFS topo), full trace, complexity.

---

## D4. Alien Dictionary — invalid cases

(a) `["z","x","z"]` → ?  
(b) `["abc","ab"]` → ?  
Explain each.

---

## D5. Alien — why adjacent only?

Why is comparing only **adjacent** words in the sorted list enough to build the constraint graph?

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION E: IMPLICIT GRAPHS & GRID BFS

---

## E1. Shortest path binary matrix

`grid = [[0,1],[1,0]]`, 8-directional moves. Shortest clear path length from (0,0) to (1,1)? Approach + answer.

---

## E2. Open the Lock (sketch)

Start `"0000"`, target `"0201"`, deadends `["0202"]` (illustrative). What is a node? How many neighbors does each node have? Which algorithm?

---

## E3. Code: neighbors for lock

Write a function `lock_neighbors(s: str) -> list[str]` for a 4-digit string.

---

## E4. Jump on grid vs Word Ladder

Same pattern family — fill the analogy table:

| | Word Ladder | Binary matrix path |
|---|---|---|
| Node | | |
| Edge | | |
| Algorithm | | |

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION F: CUMULATIVE LIGHT PULL (PRIOR MODULES)

Keep answers short — confirm old tools still fire.

---

## F1. Deque vs list

Why use `collections.deque` for BFS, not a Python `list` with `pop(0)`?

---

## F2. Hash set role

In BFS, what is `visited` / `dist` keys doing that connects to the hashing module?

---

## F3. Recursion space

DFS recursive on a linked-list-shaped graph of V nodes: stack space? Risk in Python?

---

## F4. Tree level-order vs graph BFS

One difference that will break tree-only BFS code on a general undirected graph?

---

## F5. Amortized / Big O

Adj list: iterating all edges is Θ(E). Is building the list from an edge list O(E) or O(V+E)? Include isolated vertices initialization when labels are `0..n-1`.

---

## F6. Sorting callback (light)

Alien dictionary sometimes asks for the **lexicographically smallest** valid order. What do you swap in Kahn, and which module's tool is that?

---

## F7. Two pointers / windows (light)

True/False: sliding window is the right primary tool for Word Ladder. One sentence why.

---

## F8. Heap PREVIEW contrast

True/False: "shortest path in an unweighted graph" needs a min-heap. Correct the statement.

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION G: SYNTHESIS / TRAPS

---

## G1. Pick the tool

For each prompt, name the Graphs I tool (one phrase):

1. "Minimum knight moves to a square on infinite chessboard."  
2. "Order courses given prerequisites; detect impossible."  
3. "Is the network 2-colorable / no odd cycle?"  
4. "Count friend circles from adjacency matrix."  
5. "Derive alien alphabet from sorted words."  
6. "Shortest word transformation."  

---

## G2. Complexity call-out

Someone says: "My graph BFS is O(V²) because nested loops." When is that accurate, and when are they wrong?

---

## G3. Directed vs undirected checklist

List three bugs that appear when you accidentally treat a directed problem as undirected (or vice versa).

---

## G4. Interview script

Fill blanks for Word Ladder:

> "Nodes are __. Edges mean __. Because edges are __, shortest sequence is __. I'll generate neighbors by __. Time __."

---

## G5. PREVIEW boundary

Which of these are **not** earned in Module 7? (List them.)  
(a) Kahn topo  
(b) Dijkstra  
(c) Bipartite BFS  
(d) Union-Find components  
(e) Word Ladder BFS  

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION H: MORE CODE DRILLS

---

## H1. Keys and Rooms

`rooms = [[1],[2],[3],[]]`. Can visit all? Code reachability. Trace.

---

## H2. Parallel Courses (semesters)

`n=3`, `relations=[[1,3],[2,3]]`. Minimum semesters? Show Kahn-by-level.

---

## H3. Surrounded Regions (logic only)

Board with a ring of `'X'` enclosing an `'O'`, plus one `'O'` on the border. Which `'O'`s flip? Why start DFS from the border?

---

## H4. Pacific Atlantic (one insight)

Why run multi-source search **from the oceans inland** instead of from every cell downhill to the ocean?

---

## H5. Genetic Mutation vs Word Ladder

Name the only template differences (alphabet, length, return -1 vs 0).

---

## H6. Write bipartite check

Code `is_bipartite(graph: List[List[int]]) -> bool` from memory (BFS 2-color). Handle disconnected graphs.

---

## H7. Write undirected cycle detect

Code `has_cycle(n, edges)` with DFS + parent.

---

## H8. Reconstruct path

Given parent map from BFS, write `build_path(parent, start, target)` or explain why target missing ⇒ no path.

---


> **Answers for previous section →** `keys/Module 7 Retention.keys.md`

# SECTION I: TIMED-VERIFY RE-QUEUE (GATE PREP)

After this grill passes, schedule **blind timed** retries for gate credit:

| Problem | Pattern | Notes |
|---|---|---|
| Word Ladder Length | Implicit BFS | Earned re-credit #7 |
| Alien Dictionary | Graph + Kahn topo | Earned re-credit #12 |
| Course Schedule I/II | Cycle / topo | Core Module 7 |
| Number of Islands | Components on grid | Core |
| Is Graph Bipartite | 2-color | Core |
| Rotting Oranges | Multi-source BFS | Core |
| Open the Lock | Implicit BFS | Core |
| Clone Graph | DFS/BFS + map | Core |
| Keys and Rooms | Reachability DFS/BFS | Core |
| Parallel Courses | Level-Kahn | Core |
| Pacific Atlantic | Multi-source reverse DFS | Stretch |
| Surrounded Regions | Border DFS + capture | Core |
| Min Genetic Mutation | Word-Ladder twin | Core |

Tag each timed miss: knowledge-gap / misread / time-pressure / careless-slip. Update `Metrics/Scoreboard.md` and `Metrics/Retention Ledger.md`.

**Do not** mark Module 7 `complete` until retention-passed + timed-verified per Handoff Doc §2A.

---

# SECTION J: CHEAT SHEET — RETENTION FACE

| Signal | Reach for |
|---|---|
| Shortest / min steps, unit cost | BFS |
| Prerequisites / order / alien letters | Topo (Kahn) |
| Impossible order / circular deps | Cycle (Kahn incomplete / GRAY) |
| Friend groups / islands / provinces | Components |
| 2 teams / odd cycle | Bipartite color |
| Word/lock/grid states | Implicit BFS |
| Capture surrounded / flow to oceans | Border or ocean multi-source DFS |
| Semesters / parallel tasks | Level-Kahn |
| Weighted distances | PREVIEW Dijkstra |

**O(V+E)** — say it, mean it: one visit per vertex, one scan per edge endpoint.

**Earned re-credit checklist:** Word Ladder Length ✅ · Alien Dictionary ✅ · re-queue timed.

---

*End of Module 7 Retention. Grade via `keys/Module 7 Retention.keys.md`.*
