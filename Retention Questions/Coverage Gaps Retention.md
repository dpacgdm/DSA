<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Coverage Gaps Retention.keys.md -->
> **Blind mode:** Section answer blocks moved to `keys/Coverage Gaps Retention.keys.md`.

# COVERAGE GAPS RETENTION

**Purpose:** Cumulative retention grill for the six coverage-gap lessons.  
**Sources:**
- `Intervals/Intervals & Sweep Line.md`
- `Bitwise/Bit Manipulation.md`
- `Strings/String Algorithms.md`
- `Math/Math for Interviews.md`
- `Matrix/Matrix & Grid Patterns.md`
- `Design/Design Data Structures.md`

**Rules:** No notes. Identify pattern → approach → code sketch → complexity → edges.  
**Governance:** All items are **earned** from the six lessons above (no PREVIEW credit games). Escalating within each section and across the grill.

---

# SECTION A: RAPID FIRE — CONCEPTS

Answer in 1–3 sentences unless code is requested.

---

## A1. Overlap predicate
State the closed-interval overlap test in one inequality using max/min.

## A2. Merge sort key
Why sort by **start** for merge, but by **end** for maximum non-overlapping subset?

## A3. Meeting Rooms II tie-break
In a +1/−1 sweep, why process ends before starts at the same timestamp when touching is allowed?

## A4. Difference array vs sweep
When do you prefer a dense difference array over an event sweep?

## A5. XOR cancel
Why does XORing every element find the number that appears once when all others appear twice?

## A6. n & (n−1)
What does `n & (n-1)` do? How do you test power-of-two?

## A7. LPS meaning
Define `lps[i]` for KMP in one sentence.

## A8. Z vs KMP
One sentence each: what Z[i] stores; how you use Z for pattern search.

## A9. Hash vs KMP
When is rolling hash preferred over KMP? Name the main risk.

## A10. Modular subtraction
Write the safe formula for `(a - b) % m` with possibly negative intermediates.

## A11. Fast pow complexity
Binary exponentiation does how many multiplications in terms of n?

## A12. Orientation
What does the sign of the 2D cross product `(B-A)×(C-A)` tell you?

## A13. Spiral guard
Why does spiral traversal need `if top <= bottom` before the bottom row pass?

## A14. Multi-source BFS
How do you initialize BFS for "distance to nearest zero" on a grid?

## A15. MinStack invariant
What does the auxiliary min stack store, and when do you pop it?

## A16. RandomizedSet delete
How do you delete an arbitrary element from the array in O(1)?

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION B: INTERVALS & SWEEP — PROBLEMS

---

## B1. Merge
Merge `[[1,4],[0,2],[3,5]]`. Show sorted order and final answer.

## B2. Insert
`intervals=[[1,2],[3,5],[6,7],[8,10],[12,16]]`, insert `[4,8]`. Give the three-phase result.

## B3. Meeting Rooms I
Can you attend `[[0,30],[5,10],[15,20]]`? Why?

## B4. Meeting Rooms II
Min rooms for `[[1,5],[2,6],[3,7],[8,9]]`. Show peak active from sweep.

## B5. Car Pooling
`trips=[[2,1,5],[3,3,7]]`, `capacity=4` and `5`. Answers + one-line reason.

## B6. Employee Free Time
`schedule=[[[1,2],[5,6]],[[1,3]],[[4,10]]]`. Free intervals?

## B7. Erase Overlap
Min removals for `[[1,2],[2,3],[3,4],[1,3]]`.

## B8. Code — sweep rooms
Write `min_meeting_rooms_sweep(intervals)` with ends-before-starts tie-break. Complexity?

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION C: BITWISE — PROBLEMS

---

## C1. Popcount
Hamming weight of `n=11` via Brian Kernighan — show steps.

## C2. Single Number
`[4,1,2,1,2]` → answer + why XOR works.

## C3. Missing Number
`nums=[3,0,1]` (n=3). XOR method result.

## C4. Power of Two
Classify: `0`, `1`, `16`, `18`.

## C5. Subsets masks
List subsets of `[1,2]` by masks `0..3`.

## C6. Counting Bits DP
Fill `countBits(5)` using `ans[i]=ans[i&(i-1)]+1`.

## C7. Single Number III
`[1,2,1,3,2,5]` — explain partition mask and result.

## C8. Code — reverse bits (8-bit toy)
Reverse `0b00010110` to 8 bits. Show result binary.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION D: STRINGS — PROBLEMS

---

## D1. LPS
Compute LPS for `"AAACAAAA"`.

## D2. KMP mismatch
In matching, on mismatch with `j>0`, what do you set `j` to?

## D3. Z-search setup
Exact string you build to search pattern `P` in text `T`. Where do hits appear?

## D4. Rolling hash update
From hash of `s[i..i+m)`, formula idea for `s[i+1..i+m]` (words OK).

## D5. Anagrams window
`s="cbaebabacd"`, `p="abc"` → start indices.

## D6. Repeated substring
Why does `lps[-1]` decide if `"abab"` is repeated unit?

## D7. Happy prefix
Longest happy prefix of `"leetcodeleet"`.

## D8. Code — build_lps
Write `build_lps(p)`. State O(m).

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION E: MATH — PROBLEMS

---

## E1. GCD/LCM
`gcd(48,18)` and `lcm(48,18)`.

## E2. Mod inverse
How do you compute `a^(-1) mod MOD` for prime MOD in Python one-liner?

## E3. Fast pow trace
Compute `3^10` via binary exponentiation steps (values of res/a/n).

## E4. nCr
`C(5,2)` via factorials.

## E5. Unique paths combo
Paths in `3×7` grid (only right/down) as a binomial.

## E6. Sieve
List primes ≤ 20.

## E7. Orientation
A(0,0), B(2,0), C(1,1) — left, right, or collinear?

## E8. Midpoint / ceil
Safe mid formula; `ceil_div(10,3)`.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION F: MATRIX & GRID — PROBLEMS

---

## F1. Spiral
Spiral order of `[[1,2,3],[4,5,6],[7,8,9]]`.

## F2. Set zeroes idea
In O(1) extra space, where do you store row/col zero markers, and what do you process last?

## F3. Rotate
After 90° CW, where does `(i,j)` go in an `n×n` matrix?

## F4. Search II
Start cell for Young-tableau search; move rules.

## F5. Islands
Why mutating `'1'→'0'` is valid visited marking.

## F6. Flood fill trap
What infinite-loop bug if `newColor == original`?

## F7. Rotting oranges
Why multi-source BFS by levels gives minutes?

## F8. Code — unique paths with obstacles
Sketch DP transition; handle start blocked.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION G: DESIGN DS — PROBLEMS

---

## G1. MinStack
After push 3,5,2,2; pop; what is getMin?

## G2. RandomizedSet
Why is `getRandom` O(1) with array+hash?

## G3. TimeMap get
`set(k,v1,1)`, `set(k,v2,4)`; `get(k,3)` returns?

## G4. Snapshot Array
Why not copy the whole array on every `snap`?

## G5. FreqStack
After push 5,7,5,7,4,5 — first three pops?

## G6. BST Iterator
What does the stack hold? Amortized cost of `next`?

## G7. Twitter feed
How do you get top 10 among self+followees efficiently (name the merge idea)?

## G8. Design principles
List three principles you state before coding a DS design problem.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION H: INTEGRATION / ESCALATION

---

## H1. Car fleet cousin
You have intervals of "busy CPU"; also a capacity of concurrent jobs = 2. Given jobs `[s,e]`, return whether feasible. Which lesson patterns combine?

## H2. Grid + bits
`m×n` grid of 0/1 with `m≤20`, `n≤10^5` — count distinct rows. Approach?

## H3. String + math
Rolling hash uses fast pow for `BASE^k`. Why `pow(BASE, k, MOD)` beats a loop of k multiplies when k is large and you need many random powers?

## H4. Design + intervals
Implement a calendar that books if no overlap (My Calendar I). Structures + complexity.

## H5. Matrix + graphs
Shortest path in binary matrix (8-dir) from top-left to bottom-right. Algorithm + complexity.

## H6. Full code — RandomizedSet
Write the class. Then state what breaks if you `del self.pos[val]` before updating `pos[last]` when `last==val`.

## H7. Full code — KMP search returning first index
Write `strStr(haystack, needle)` via KMP; empty needle → 0.

## H8. Trace monster — Rooms II + Car Pool analogy
Explain in 4 sentences how Meeting Rooms II and Car Pooling are the same sweep skeleton with different payloads.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

# SECTION I: CHEAT-SHEET RECALL (WRITE FROM MEMORY)

Reproduce from memory (answers below for self-check):

1. Interval decision table (merge / rooms / car / free / greedy-by-end).  
2. Bit idioms: check/set/clear/toggle/lowbit/power2.  
3. KMP build + match skeleton in ≤8 lines each.  
4. `gcd`, `modinv`, `ceil_div`, orientation cross.  
5. DIRS4 + rotate 90 CW two steps.  
6. Design combo table: MinStack, RandomizedSet, TimeMap, FreqStack.

---


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`


> **Answers for previous section →** `keys/Coverage Gaps Retention.keys.md`

