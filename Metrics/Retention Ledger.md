# RETENTION LEDGER — SPACED REVIEW

**Last updated:** 2026-07-09  
**Machine SoT:** `Metrics/ledger.json` (use with `py -3 tools/spaced_drill.py --write`)  
**Rule:** Every retention grill must pull **due** rows from this ledger plus new module material.  
**Heat:** `strong` · `shaky` · `weak`  
**Content:** All Phase A retention files exist (see `Phase A Curriculum Index.md`). Rows below track **learner** passes, not content delivery.

### Suggested intervals after a learner pass

| Heat | Next due after pass |
|---|---|
| strong | ~21 days (or 3 modules later) |
| shaky | ~7 days (or next retention) |
| weak | ~2–3 days + re-teach before credit |

---

## Module 1 — Big O & Complexity

| Subskill | Heat | Last pass | Next due | Fail count | Notes |
|---|---|---|---|---|---|
| Simplification rules (3) | strong | Week 1 grill | due-now (M2 grill) | 0 | |
| Loop pattern recognition | strong | Week 1 grill | due-now | 0 | |
| Dependent nesting (sum / harmonic) | shaky | Week 1 grill | due-now | 0 | |
| Hidden costs (Python ops) | shaky | Week 1 grill | due-now | 0 | |
| Space + call stack (non-recursive) | strong | Week 1 grill | due-now | 0 | |
| Interview complexity communication | shaky | Week 1 grill | due-now | 0 | |

## Module 1 — Arrays & Strings

| Subskill | Heat | Last pass | Next due | Fail count | Notes |
|---|---|---|---|---|---|
| Contiguous memory / op costs | strong | Week 1 grill | due-now | 0 | |
| Two pointers | strong | Week 1 grill | due-now | 0 | |
| Sliding window | shaky | Week 1 grill | due-now | 0 | |
| Prefix sums | strong | Week 1 grill | due-now | 0 | |
| In-place techniques | shaky | Week 1 grill | due-now | 0 | |
| String immutability traps | strong | Week 1 grill | due-now | 0 | |

## Module 2 — Hashing

| Subskill | Heat | Last pass | Next due | Fail count | Notes |
|---|---|---|---|---|---|
| Hash + collision model | shaky | drilled only | M2 retention | 0 | File ready |
| Dict/set Python semantics | shaky | drilled only | M2 retention | 0 | |
| Frequency / grouping | shaky | drilled only | M2 retention | 0 | |
| Prefix sum + hash map | shaky | drilled only | M2 retention | 0 | |
| Rolling hash exposure | weak | drilled only | M2 retention | 0 | |

## Module 2 — Recursion

| Subskill | Heat | Last pass | Next due | Fail count | Notes |
|---|---|---|---|---|---|
| Base / recursive / combine | shaky | drilled only | M2 retention | 0 | |
| Call stack space | shaky | drilled only | M2 retention | 0 | |
| Recursion tree → recurrence setup | shaky | drilled only | M2 retention | 0 | |
| Memo vs tabulation intro | shaky | drilled only | M2 retention | 0 | |
| Backtracking skeleton | weak | drilled only | M2 retention | 0 | |
| Master Theorem | — | **not M2** | Module 3 | — | Home = Sorting |

## Modules 3–11 — seed rows (activate when learner starts module)

| Module | Core subskills (seed) | Learner last pass | Next due |
|---|---|---|---|
| 3 | BS templates, bounds, BS-on-answer, bisect, merge/quick, **Master Theorem**, Count of Range Sum | none | on start |
| 4 | LL reverse/Floyd/dummy, monotonic stack/queue, deque vs list | none | on start |
| 5 | Traversals, recursive tree framework, BST CRUD/validate, LCA | none | on start |
| 6 | heapq patterns, top-K, advanced window/two-pointer | none | on start |
| 7 | BFS/DFS, components, bipartite, cycle, topo, Word Ladder, Alien Dict | none | on start |
| 8 | Dijkstra, DSU, MST intuition, DP 1D framework | none | on start |
| 9 | 2D/knapsack/LCS/edit, backtracking template, greedy vs DP | none | on start |
| 10 | Trie ops, monotonic contribution, Fenwick exposure | none | on start |
| 11 | Mock rubric dims, timed mixed sets, weak-spot loop | none | on start |

## PREVIEW re-credit (content now earned in home modules)

| Item | Home module | Learner re-queue |
|---|---|---|
| Word Ladder | Module 7 | after Graphs I learner `complete` → timed credit |
| Count of Range Sum | Module 3 | after Sorting learner `complete` → timed credit |
| Alien Dictionary | Module 7 | after Graphs I learner `complete` → timed credit |

---

## Grill checklist

1. Pull all `due-now` / overdue rows  
2. Add new-module questions from that module's retention file  
3. Grade vs answer key; tag fails; update heat  
4. Update `Metrics/Scoreboard.md` G2  
5. Raise learner status only via Handoff enum  


## Seed note (2026-07-11)

`ledger.json` now includes M3–M11 + coverage subskills at `weak` / due today until first pass. Run `python tools/spaced_drill.py --write`.
