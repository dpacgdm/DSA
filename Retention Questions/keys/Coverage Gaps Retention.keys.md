# Answer Key — Coverage Gaps Retention.md

**Source questions:** `Retention Questions/Coverage Gaps Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

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

