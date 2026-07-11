# Answer Key — Module 8 Retention.md

**Source questions:** `Retention Questions/Module 8 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
### Answer
`4 > dist[1]` → **continue** (skip). No neighbor relaxation from the stale pop.

---


<!-- answer block 2 -->
### Answer
After one BF pass (that order): dist[1] becomes 10 then 2→1 updates to 6; dist=[0,6,5]. Dijkstra final same `[0,6,5]`.

---


<!-- answer block 3 -->
### Answer

```python
def union(parent, size, a, b):
    ra, rb = find(parent, a), find(parent, b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True
```

---


<!-- answer block 4 -->
### Answer
`gabe0@, gabe2@, gabe3@, gabe4@` (all linked via gabe0/gabe2).

---


<!-- answer block 5 -->
### Answer
`(1,2)` reject (same component). `(2,3)` add (merges).

---


<!-- answer block 6 -->
### Answer
`dp[0]=1`
`dp[1]=1`
`dp[2]=2` (1+1, 2)
`dp[3]=4` (1+1+1, 1+2, 2+1, 3)
`dp[4]=7`
Answer **7**.

---


<!-- answer block 7 -->
### Answer
`dp = [1, 1, 2, 1, 1]` → answer **1**.

---


<!-- answer block 8 -->
### Answer
**4** (see DP I combinations trace).

---


<!-- answer block 9 -->
### Answer
**9**.

---


<!-- answer block 10 -->
### Answer
**6**.

---


<!-- answer block 11 -->
### Answer
Maintain current jump's end window. Scan window for farthest reach. When index hits window end, jumps += 1 and set new end to farthest. Like BFS levels on the array.

---


<!-- answer block 12 -->
### Answer
**Dijkstra**; `new_effort = max(old_effort, |Δheight|)`; minimize effort.

---


<!-- answer block 13 -->
### Answer
Add virtual node connected to each village by well cost; MST on that graph = optimal dig/pipe mix.

---


<!-- answer block 14 -->
### Answer
STATE: `dp[i]` = min squares summing to i.  
TRANSITION: `dp[i]=min(dp[i-sq]+1)` for sq=1,4,9,…≤i.  
BASE: `dp[0]=0`.  
ORDER: i=1..n.  
ANSWER: `dp[n]`.

---


<!-- answer block 15 -->
### Answer
No optimal substructure with simple-path constraint (cycles/reuse); problem is NP-hard. Heap trick doesn't apply.

---


<!-- answer block 16 -->
### Answer
Kruskal: sort edges, DSU add if no cycle. Prim: grow tree from a node with a heap of outgoing edges.

---


<!-- answer block 17 -->
### Answer
Inverse Ackermann — grows so slowly it's ≤ 4 for all practical n; say "effectively constant amortized."

---


<!-- answer block 18 -->
### Answer
Must insert both `(u,v,w)` and `(v,u,w)` into the adjacency list.

---


<!-- answer block 19 -->
### Answer
**1** if `dp[i]` = ways to climb `i` stairs (one empty way). If you only define `dp[1], dp[2]`, set those explicitly instead.

---


<!-- answer block 20 -->
### Answer
O(n²) worst; with L cap on inner span often O(n·L) checks.

---


<!-- answer block 21 -->
### Answer
**Yes** — non-negative includes 0. Still correct.

---


<!-- answer block 22 -->
### Answer
Not always. Different MSTs can share the same total weight if equal-weight edges exist.

---


<!-- answer block 23 -->
### Answer
`[]→0`, `[x]→x`.

---


<!-- answer block 24 -->
### Answer
If a full pass does zero updates, stop early — distances already stable.

---


<!-- answer block 25 -->
### Answer
Allowed. Only **shared email** merges accounts; names are labels for output.

---


<!-- answer block 26 -->
### Answer
Without `nxt = dist[:]`, multiple edges might chain in one "round," exceeding the stop budget. Layer copy enforces at most one new edge per iteration.

---


<!-- answer block 27 -->
### Answer
Both O(n² log n) dominated by O(n²) edges. Prim with binary heap on dense graph similar; Kruskal fine. n=1000 → ~5e5 edges OK.

---


<!-- answer block 28 -->
### Answer
A→B 1, B→C −100, A→C 2. True dist C = −99. If C finalized at 2 first, wrong.

---


<!-- answer block 29 -->
### Answer
Identical problem — `nums` are house values.

---


<!-- answer block 30 -->
### Answer
**2**: `AB` (1|2) and `L` (12).

---


