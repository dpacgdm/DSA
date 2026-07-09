# COVERAGE GAPS RETENTION — FULL ANSWER KEY

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

# SECTION A — ANSWERS

### A1
Overlap iff `max(s1,s2) < min(e1,e2)` (equivalently `s1 < e2 and s2 < e1`).

### A2
Merge only needs the next interval relative to the current open union → sort by start. Max non-overlapping greedy needs earliest finish to leave room → sort by end.

### A3
So a room freed at time `t` can be reused by a meeting starting at `t` (no false concurrency spike). Sort key `(time, delta)` with `delta=-1` before `+1`.

### A4
When the timeline coordinate range `T` is small/dense (e.g. stations 0..1000). Sweep when coordinates are large/sparse.

### A5
`x^x=0` and `x^0=x`; pairs cancel; associative/commutative order doesn't matter; leftover is the unique.

### A6
Clears the lowest set bit. Power of two: `n > 0 and (n & (n-1)) == 0`.

### A7
`lps[i]` = length of the longest proper prefix of `p[0..i]` that is also a suffix of `p[0..i]`.

### A8
`Z[i]` = longest substring starting at `i` that matches a prefix of `s`. Build `pattern + sep + text`; hits where `Z[i] == len(pattern)`.

### A9
Many substring equality checks / Rabin–Karp multi-pattern. Risk: hash collisions (mitigate with double hash or fall back to verify).

### A10
`(a % m - b % m + m) % m`.

### A11
`O(log n)` multiplications (one square per bit; one multiply into result per set bit).

### A12
Positive → C left of directed line AB (CCW); negative → right (CW); zero → collinear.

### A13
Without it, a single remaining row (or column) can be traversed twice when top/bottom (or left/right) meet.

### A14
Enqueue every cell with `0` at distance 0; BFS outward; first touch on a `1` cell is nearest-zero distance.

### A15
Non-increasing sequence of minima of the stack so far. Pop from min stack only when the popped value equals the current min (use `<=` on push for duplicates).

### A16
Swap it with the last element, update the hash index of the moved element, then `pop()` the array and delete the key from the map.

---

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

# SECTION B — ANSWERS

### B1
Sort `[[0,2],[1,4],[3,5]]` → merge to `[[0,5]]`.

### B2
`[[1,2],[3,10],[12,16]]` (merge `[3,5],[6,7],[8,10]` into `[3,10]`).

### B3
No — after sort, `5 < 30` → conflict.

### B4
Events peak at active=3 (meetings 1–3 overlap) → **3 rooms**.

### B5
Capacity 4: False (at time 3, load 5). Capacity 5: True.

### B6
Merged busy `[1,3],[4,10]` → free `[[3,4]]`.

### B7
Sort by end; keep 3 → remove **1**.

### B8
```python
def min_meeting_rooms_sweep(intervals):
    events = []
    for s, e in intervals:
        events.append((s, +1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], x[1]))
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best
# O(n log n) time, O(n) space
```

---

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

# SECTION C — ANSWERS

### C1
`11=1011` → `1010` → `1000` → `0` → count **3**.

### C2
**4**. Pairs cancel; leftover unique.

### C3
**2** (`0^1^2^3 ^ 3^0^1 = 2`).

### C4
False, True, True, False.

### C5
`[]`, `[1]`, `[2]`, `[1,2]`.

### C6
`[0,1,1,2,1,2]`.

### C7
XOR all = `3^5=6`; `mask=6&-6=2`; partition by bit1 → `{3}` and `{5}`.

### C8
`0b00010110` → `0b01101000` (bits reversed within 8).

---

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

# SECTION D — ANSWERS

### D1
`[0,1,2,0,1,2,3,3]`.

### D2
`j = lps[j-1]`.

### D3
`P + sep + T` with `sep` not in alphabet. Hits at indices `i` with `Z[i]==len(P)`; text start = `i-(len(P)+1)`.

### D4
Subtract outgoing char · BASE^(m−1), multiply by BASE, add incoming char; all mod MOD.

### D5
`[0, 6]`.

### D6
`lps=[0,0,1,2]`, `n-lps[-1]=2`, `n % 2 == 0` and border > 0 → period 2 (`"ab"`).

### D7
`"leet"`.

### D8
```python
def build_lps(p):
    m = len(p)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if p[i] == p[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps
# O(m)
```

---

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

# SECTION E — ANSWERS

### E1
gcd **6**; lcm **144**.

### E2
`pow(a, MOD-2, MOD)`.

### E3
`n=10=1010₂`: square path `a:3→9→81→6561→...`; res picks `9` then `9*6561=59049` (=3^10). Exact bit walk: start res=1,a=3; n even→a=9,n=5; odd→res=9,a=81,n=2; even→a=6561,n=1; odd→res=9*6561=59049.

### E4
`5!/(2!3!)=10`.

### E5
`C(3+7-2, 3-1)=C(8,2)=28`.

### E6
`2,3,5,7,11,13,17,19`.

### E7
cross=`2*1-0*1=2>0` → **left / CCW**.

### E8
`lo+(hi-lo)//2`; ceil_div=`(10+3-1)//3=4`.

---

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

# SECTION F — ANSWERS

### F1
`[1,2,3,6,9,8,7,4,5]`.

### F2
Markers in first row & first column; remember whether first row/col originally had zeros; zero the first row/col **last**.

### F3
`(i,j) → (j, n-1-i)`. Equivalent: transpose + reverse each row.

### F4
Start top-right (or bottom-left). If too big, move left; if too small, move down.

### F5
Land cells only need to be visited once for component flooding; changing to water prevents re-entry without a separate set.

### F6
Every DFS neighbor still "matches" original and keeps painting forever. Early-return if colors equal.

### F7
Each BFS layer = one simultaneous minute of rotting; queue starts with all initially rotten oranges.

### F8
```python
if grid[0][0]==1: return 0
dp[0][0]=1
# if cell blocked: dp=0 else dp = from_up + from_left
```

---

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

# SECTION G — ANSWERS

### G1
**2** (one duplicate 2 remains; min stack still has 2).

### G2
Uniform index into dense array `random.randrange(len(arr))`; hash gives O(1) index for insert/remove via swap-with-last.

### G3
**v1** (latest timestamp ≤ 3).

### G4
Store sparse history per index `{snap_id: value}`; most indices unchanged across snaps → save time/space.

### G5
**5, 7, 5** (freq 3 then freq 2 most recent).

### G6
Left spine / path to next inorder node. Amortized **O(1)** (each node pushed/popped once); space O(h).

### G7
Max-heap merge of recent tweet lists (k-way merge by timestamp), or heap of all candidates pruned to last 10 per user.

### G8
Any three of: API+complexities first; name invariant; compose structures; discuss lazy deletion; call out amortized vs worst; don't overbuild.

---

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

# SECTION H — ANSWERS

### H1
Interval concurrency (Meeting Rooms II / sweep). Feasible iff max active ≤ 2.

### H2
Pack each row into a bitmask (m bits) or tuple/hash; insert into a set; answer = set size. Bits shine when m≤20.

### H3
Binary exponentiation is O(log k) per power; precompute prefix powers in O(n) for rolling. A naive O(k) loop per query is too slow when many queries / large k.

### H4
Sorted list of bookings + binary search for neighbors; check overlap with prev/next. Book O(n) insert (or TreeMap O(log n) in other langs).

### H5
BFS on cells with value 0; 8 neighbors; mark visited on enqueue. O(RC) time/space.

### H6
```python
import random
class RandomizedSet:
    def __init__(self):
        self.arr, self.pos = [], {}
    def insert(self, val):
        if val in self.pos: return False
        self.pos[val] = len(self.arr)
        self.arr.append(val)
        return True
    def remove(self, val):
        if val not in self.pos: return False
        i, last = self.pos[val], self.arr[-1]
        self.arr[i] = last
        self.pos[last] = i
        self.arr.pop()
        del self.pos[val]
        return True
    def getRandom(self):
        return random.choice(self.arr)
```
If `last==val` (removing final element) and you delete `pos[val]` first, then `pos[last]=i` recreates a stale entry after pop — or you write to a deleted key incorrectly depending on order. Safe order: assign `pos[last]=i`, pop array, **then** `del pos[val]` (when last≠val, del is required; when last==val, del after pop still correct if you del val once).

### H7
```python
def strStr(haystack, needle):
    if needle == "":
        return 0
    lps = build_lps(needle)
    i = j = 0
    n, m = len(haystack), len(needle)
    while i < n:
        if haystack[i] == needle[j]:
            i += 1; j += 1
            if j == m:
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return -1
```

### H8
Both create timeline events and walk sorted order while maintaining a running total. Rooms: +1 at start, −1 at end; track max total (= rooms). Car pooling: +passengers at pickup, −passengers at drop; check total never exceeds capacity. Tie-break (drop/end before pick/start) is the same idea. Payload is unit concurrency vs weighted capacity — skeleton identical.

---

# SECTION I: CHEAT-SHEET RECALL (WRITE FROM MEMORY)

Reproduce from memory (answers below for self-check):

1. Interval decision table (merge / rooms / car / free / greedy-by-end).  
2. Bit idioms: check/set/clear/toggle/lowbit/power2.  
3. KMP build + match skeleton in ≤8 lines each.  
4. `gcd`, `modinv`, `ceil_div`, orientation cross.  
5. DIRS4 + rotate 90 CW two steps.  
6. Design combo table: MinStack, RandomizedSet, TimeMap, FreqStack.

---

# SECTION I — ANSWER KEY (BRIEF)

1. Merge@start; RoomsI@start; RoomsII sweep/heap; Car +/− capacity; Free=merge busy→gaps; Erase@**end**.  
2. `n&(1<<i)`; `n|(1<<i)`; `n&~(1<<i)`; `n^(1<<i)`; `n&-n`; `n>0 and n&(n-1)==0`.  
3. See lesson templates / D8 / H7.  
4. Euclid; `pow(a,m-2,m)`; `(a+b-1)//b`; `(bx-ax)*(cy-ay)-(by-ay)*(cx-ax)`.  
5. Four dirs; transpose + reverse rows.  
6. Dual stack; arr+hash; hash+bisect; freq+group stacks.

---

# SCORING GUIDE (SELF)

| Band | Meaning |
|---|---|
| A+B+C solid | Foundations OK — drill weak codes |
| Miss H items | Integration shaky — revisit decision sheets |
| Miss idioms I | Flashcard week on cheat sheets |
| All clean timed | Ready for `timed-verified` attempts on these patterns |

---

**Status:** Retention grill `content-delivered` with full answers. Learner credit still requires blind attempt then check.


---

# SECTION J: TIMED SET SIMULATION (ANSWERS BELOW)

Do in 45 minutes closed-book, then score.

1. Merge `[[2,3],[4,5],[6,7],[8,9],[1,10]]`  
2. Rooms II for `[[1,3],[2,4],[3,5],[4,6]]`  
3. XOR single number `[7,3,7,8,3]`  
4. LPS of `"ABABAA"`  
5. `gcd(84,30)`, `lcm`  
6. Spiral `[[1,2,3,4],[5,6,7,8],[9,10,11,12]]`  
7. MinStack ops: push 2, push 0, push 3, push 0, getMin, pop, getMin, pop, getMin, pop, getMin  
8. Car pooling `[[2,1,5],[3,5,7]]` cap 3  

## SECTION J — ANSWERS

1. `[[1,10]]`  
2. Peak 2  
3. `8`  
4. `[0,0,1,2,3,2]`  
5. gcd 6, lcm 420  
6. `[1,2,3,4,8,12,11,10,9,5,6,7]`  
7. mins: 0,0,0,2  
8. True (drop at 5 before pick 3)

---

**Retention file status:** `content-delivered` with full keys.
