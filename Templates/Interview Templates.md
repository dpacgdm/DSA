# Interview Templates (Prose Guide)

Copy-paste skeletons live in `Templates/python_templates.py`. This file explains **when** to reach for each template and the invariants you must keep true.

---

## Clean coding conventions (interview)

1. **Names that state role:** `lo/hi`, `left/right`, `indeg`, `dist`, `path`, `best` — not `a/b/x1`.
2. **Early returns** for empty / impossible / trivial (`if not root: return 0`).
3. **One invariant comment** above the hot loop (one line is enough).
4. **Don’t mutate inputs** unless the problem allows it (or say so out loud).
5. **Extract helpers** only when they clarify (e.g. `neighbors`, `valid`); avoid framework soup.
6. **Complexity out loud** before coding: time, space, what `n` is.
7. **Types in your head:** index vs value; node vs value; 0-based vs problem’s labels.

---

## Binary search

**Use when:** monotonic predicate on a sorted range or answer space (“first True”, min feasible capacity).

**Two shapes:**

| Shape | Loop | Update | Returns |
|---|---|---|---|
| Exact find | `lo <= hi` | `lo=mid+1` / `hi=mid-1` | index or `-1` |
| Lower bound (first ≥ target) | `lo < hi` half-open `[lo,hi)` | `lo=mid+1` if `a[mid] < t` else `hi=mid` | `lo` |

**Invariant:** every iteration shrinks the range; never `lo = mid` on a closed interval.

---

## Sliding window

**Use when:** contiguous subarray/substring; optimize count/length/sum with a moveable left edge.

**Skeleton idea:** expand `right`; while window invalid, advance `left`; update answer.

**Invariant:** after the `while`, `[left, right]` satisfies the constraint (or is empty).

**Traps:** stale index maps (`last[ch] >= left`); confusing length `right-left+1` with sum.

---

## BFS / DFS graphs

**BFS:** shortest path in **unweighted** graphs; level order; queues.

**DFS:** connectivity, components, backtracking on graphs, topo via recursion stack (or prefer Kahn).

**Invariant (BFS):** first time you visit a node, distance is minimal (if unit weights).

**Always:** mark seen when **enqueue** (BFS) to avoid duplicates; define whether distance is nodes or edges.

---

## Union-Find (DSU)

**Use when:** dynamic connectivity, redundant edges, number of provinces, Kruskal flavor.

**Invariant:** `find` is idempotent with path compression; `union` by rank/size keeps forests shallow.

---

## Dijkstra

**Use when:** non-negative weighted shortest path.

**Invariant:** when a node is popped with best `dist`, that distance is final (non-negative weights).

**Trap:** negative weights → Bellman-Ford / SPFA discussion, not Dijkstra.

---

## DP memo / tab

**Memo:** top-down; state = arguments of recursion; store results in dict/array.

**Tab:** bottom-up; define `dp[i]` meaning in one sentence before filling.

**Invariant:** transitions only use **already computed** subproblems.

**Climb / coin / knapsack:** know whether order of loops counts combinations vs permutations.

---

## Backtracking

**Use when:** generate subsets/permutations/combinations; search with undo.

**Skeleton:** `path` + choose/explore/unchoose; prune early.

**Invariant:** `path` always represents a valid partial solution; undo restores prior state exactly.

---

## Trie

**Use when:** prefix queries, word search dictionaries, autocomplete.

**Invariant:** `end` flag marks complete words; prefix walk ≠ search unless `end`.

---

## Linked list helpers

Know cold: reverse, merge two sorted, cycle detect (Floyd), middle (slow/fast), dummy head for edge-empty.

**Invariant for reverse:** `prev` is head of reversed prefix; `cur` is head of remaining.

---

## Heap patterns

- **Top-K:** size-`k` heap (min-heap of size k for k largest).
- **Merge K lists / streaming medians:** multi-pointer heaps.
- Python: `heapq` is min-heap; negate for max-heap.

---

## Monotonic stack

**Use when:** next greater/smaller, histogram, stock span.

**Invariant:** stack stores indices with values mono-increasing or decreasing; pop means “answer found for that index.”

---

## How to practice with the bank

1. Open the matching template section in `python_templates.py`.
2. Solve the bank problem **without** looking at `solution.py`.
3. Diff your code against the template invariants, not against golfed syntax.
4. On failure, use `Debugging/Debugging Diagnosis.md`.
