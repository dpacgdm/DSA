# MATRIX & GRID PATTERNS — THE COMPLETE LESSON

**Module:** Coverage gap — Matrix / Grid (first-class hub)  
**Status:** `content-delivered` — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Arrays, BFS/DFS (`Graphs I`), DP basics (`DP I`).  
**Cross-refs:** Islands / flood fill ↔ Graphs I; path counting ↔ DP I; multi-source BFS ↔ Graphs I Part 6C.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHY MATRICES ARE A HUB

A grid is an **implicit graph**: each cell is a node; edges go to 4 (or 8) neighbors. Almost every "matrix" interview problem is one of:

| Family | Examples |
|---|---|
| Traversal / reshape | Spiral, diagonal traverse |
| In-place transform | Rotate, set zeros |
| Search | Sorted matrix search |
| Graph on grid | Islands, flood fill, walls & gates |
| DP on grid | Unique paths, min path sum |
| Multi-source BFS | Rotting oranges, 01 matrix |

**Interview sentence:**  
> "I'll treat the grid as a graph — neighbors `(r±1,c),(r,c±1)` inside bounds — and apply BFS/DFS/DP."

---

# PART 2: GRID VOCABULARY & BOILERPLATE

```python
DIRS4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRS8 = DIRS4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C
```

**TRAP:** `len(grid)` = rows; `len(grid[0])` = cols. Empty grid → early return.

**Visited:** mutate cell (e.g. `'1'→'0'`) or use `visited` set of `(r,c)`.

---

# PART 3: SPIRAL TRAVERSAL

## 3A: Layer / Boundary Shrink

```python
def spiral_order(matrix):
    if not matrix:
        return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res
```

### Trace — `[[1,2,3],[4,5,6],[7,8,9]]`
```
top row 1 2 3 → top=1
right 6 9 → right=1
bottom 8 7 → bottom=0
left 4 → left=1
center 5
→ [1,2,3,6,9,8,7,4,5]
```

**TRAP:** the `if top<=bottom` / `if left<=right` guards prevent double-counting a single row/col.

---

# PART 4: SET MATRIX ZEROES

## 4A: O(1) Extra Space — First Row/Col as Markers

```python
def set_zeroes(matrix):
    R, C = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(C))
    first_col_zero = any(matrix[r][0] == 0 for r in range(R))

    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if first_row_zero:
        for c in range(C):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(R):
            matrix[r][0] = 0
```

**Why markers:** using the matrix itself avoids O(R+C) arrays. Process first row/col **last**.

---

# PART 5: ROTATE IMAGE (90° CLOCKWISE IN-PLACE)

```python
def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()
```

**Trace 2×2:** `[[1,2],[3,4]]` → transpose `[[1,3],[2,4]]` → reverse rows `[[3,1],[4,2]]`.

**CCW:** transpose then reverse columns (or reverse rows then transpose).

---

# PART 6: SEARCH A 2D MATRIX

## 6A: Fully Sorted (treat as 1D)

Each row sorted; first of next > last of prev.

```python
def search_matrix(matrix, target):
    if not matrix:
        return False
    R, C = len(matrix), len(matrix[0])
    lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // C][mid % C]
        if val == target:
            return True
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

## 6B: Row-wise + Col-wise Sorted (Young tableau start corner)

Start top-right: left = smaller, down = larger.

```python
def search_matrix_ii(matrix, target):
    if not matrix:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        if matrix[r][c] > target:
            c -= 1
        else:
            r += 1
    return False
```

---

# PART 7: ISLANDS — DFS/BFS BRIDGE TO GRAPHS

```python
def num_islands(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])

    def dfs(r, c):
        if not in_bounds(r, c, R, C) or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        for dr, dc in DIRS4:
            dfs(r + dr, c + dc)

    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
```

**This is connected components on an implicit graph** (`Graphs I`). Same as flood fill with a counter.

### Max Area of Island
Same DFS; return size; track max.

---

# PART 8: FLOOD FILL

```python
def flood_fill(image, sr, sc, color):
    orig = image[sr][sc]
    if orig == color:
        return image
    R, C = len(image), len(image[0])

    def dfs(r, c):
        if not in_bounds(r, c, R, C) or image[r][c] != orig:
            return
        image[r][c] = color
        for dr, dc in DIRS4:
            dfs(r + dr, c + dc)

    dfs(sr, sc)
    return image
```

**TRAP:** if `orig == color`, infinite recursion without early return.

---

# PART 9: MULTI-SOURCE BFS ON GRIDS

## 9A: Pattern

Enqueue **all** sources with dist 0. First visit wins = shortest to nearest source.

```python
from collections import deque

def update_matrix(mat):  # 01 Matrix — dist to nearest 0
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, R, C) and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```

## 9B: Rotting Oranges

Multi-source all rotten; BFS minutes by levels; check fresh remain.

## 9C: Walls and Gates

Multi-source all gates (0); fill INF rooms with dist.

---

# PART 10: DP ON GRIDS BRIDGE

## 10A: Unique Paths

```python
def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]
```

Or `C(m+n-2, m-1)` (`Math`).

## 10B: Min Path Sum

```python
def min_path_sum(grid):
    R, C = len(grid), len(grid[0])
    dp = [float('inf')] * C
    dp[0] = 0
    for r in range(R):
        for c in range(C):
            if c == 0:
                dp[c] = dp[c] + grid[r][c]
            else:
                dp[c] = min(dp[c], dp[c - 1]) + grid[r][c]
    return dp[-1]
```

## 10C: When DP vs BFS

| Signal | Tool |
|---|---|
| Count paths / min sum with only right/down | **DP** |
| Shortest steps, 4-dir, obstacles | **BFS** |
| Weighted cells arbitrary | Dijkstra (Graphs II) |

---

# PART 11: PATH COUNTING WITH OBSTACLES

```python
def unique_paths_with_obstacles(obstacleGrid):
    R, C = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1:
        return 0
    dp = [[0] * C for _ in range(R)]
    dp[0][0] = 1
    for r in range(R):
        for c in range(C):
            if obstacleGrid[r][c] == 1:
                dp[r][c] = 0
                continue
            if r:
                dp[r][c] += dp[r - 1][c]
            if c:
                dp[r][c] += dp[r][c - 1]
    return dp[-1][-1]
```

---

# PART 12: CHEAT SHEETS

```
DIRS4 = (1,0),(-1,0),(0,1),(0,-1)
spiral: shrink top/bottom/left/right + guards
zeros: mark on first row/col; clear last
rotate 90 CW: transpose + reverse rows
search sorted: 1D binary mid//C, mid%C
search II: start top-right
islands: DFS/BFS components
flood: early exit if same color
multi-source: enqueue all sources dist0
paths: DP or nCr
```

---

# PART 13: TRAPS

| Trap | Fix |
|---|---|
| Spiral double-count | Guards after top/right |
| Set zero using marked cells early | Clear first row/col last |
| Flood fill same color | Early return |
| BFS mark on dequeue | Mark on enqueue |
| `grid[0]` on empty | Guard |
| 8-dir when problem says 4 | Read adjacency |

---

# PART 14: WORKED PROBLEMS

## WP1 — Spiral
`[[1,2],[3,4]]` → `[1,2,4,3]`

## WP2 — Set zeroes
`[[1,1,1],[1,0,1],[1,1,1]]` → middle row/col zeroed.

## WP3 — Rotate
`[[1,2,3],[4,5,6],[7,8,9]]` → `[[7,4,1],[8,5,2],[9,6,3]]`

## WP4 — Search matrix
`[[1,3,5],[7,9,11]]`, target 9 → True via 1D index 4.

## WP5 — Num islands
Standard 4-island grid → count components.

## WP6 — Flood fill
Center paint; verify early exit when color matches.

## WP7 — 01 Matrix
Multi-source from zeros; cell of 1s get dist.

## WP8 — Rotting oranges
Level BFS; return minutes or -1.

## WP9 — Unique paths 3×2 → 3

## WP10 — Min path sum small grid — DP table trace

---

# PART 15: INTERVIEW SCRIPT

1. Classify: transform / search / graph / DP.
2. State DIRS4 + bounds.
3. Complexity O(RC) typical.
4. For BFS: multi-source? mark on enqueue?
5. Dry-run a 3×3.

---

**Status note (interim):** Core above; deep expansions in Parts 16+.

---

# PART 16: SPIRAL GENERATE / DIAGONAL TRAVERSE

## 16A: Generate matrix 1..n² in spiral

```python
def generate_matrix(n):
    mat = [[0]*n for _ in range(n)]
    top, bottom, left, right = 0, n-1, 0, n-1
    val = 1
    while top <= bottom and left <= right:
        for c in range(left, right+1):
            mat[top][c] = val; val += 1
        top += 1
        for r in range(top, bottom+1):
            mat[r][right] = val; val += 1
        right -= 1
        if top <= bottom:
            for c in range(right, left-1, -1):
                mat[bottom][c] = val; val += 1
            bottom -= 1
        if left <= right:
            for r in range(bottom, top-1, -1):
                mat[r][left] = val; val += 1
            left += 1
    return mat
```

## 16B: Diagonal traverse
Alternate up-right / down-left; careful bounds bounce.

---

# PART 17: ISLAND VARIANTS DEEP

## 17A: Number of Closed Islands
DFS from border land first (mark ocean-connected); then count remaining islands.

## 17B: Max Area of Island
DFS returns size; track global max.

## 17C: Surrounded Regions
Border `'O'` DFS mark safe; flip remaining `'O'` to `'X'`.

## 17D: Pacific Atlantic Water Flow
Multi-source DFS/BFS from Pacific shores and Atlantic shores; intersect reachable sets.

---

# PART 18: BFS GRID CLASSICS — FULL TEMPLATES

## 18A: Shortest Path Binary Matrix (8-dir)

```python
def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1
    q = deque([(0, 0, 1)])
    grid[0][0] = 1  # visited
    while q:
        r, c, d = q.popleft()
        if (r, c) == (n-1, n-1):
            return d
        for dr, dc in DIRS8:
            nr, nc = r+dr, c+dc
            if 0<=nr<n and 0<=nc<n and grid[nr][nc]==0:
                grid[nr][nc] = 1
                q.append((nr, nc, d+1))
    return -1
```

## 18B: Walls and Gates
Multi-source from all gates; fill INF.

## 18C: 01 Matrix — already Part 9; add obstacle walls variant: skip cells with wall flag.

---

# PART 19: DP GRID CLASSICS EXPANDED

## 19A: Maximal Square
`dp[r][c] = min(up,left,diag)+1` if `'1'`.

## 19B: Cherry Pickup / path DP
Harder dual-agent DP — mention as advanced grid DP.

## 19C: Dungeon Game
DP from end: min HP needed — reverse transition.

## 19D: Triangle min path
Bottom-up in-place on rows.

---

# PART 20: MORE WORKED TRACES

## WP11 — Set zero full
Matrix with zeros at (1,1) and (2,0) — mark walk then clear.

## WP12 — Search II
Matrix sorted rows+cols; walk from top-right to find 20.

## WP13 — Rotting oranges
```
2 1 1
1 1 0
0 1 1
```
Minutes = 4; if a fresh unreachable → -1.

## WP14 — Unique paths obstacles
Obstacle in middle blocks some paths — DP zeros that cell.

## WP15 — Flood fill 3×3 center
Trace recursion stack depth.

## WP16 — Spiral empty / 1×n / n×1
Guards prevent double count.

## WP17 — Rotate 4×4 one layer
Map four-cycle `(i,j)→(j,n-1-i)→...` alternatively to transpose method.

## WP18 — Number of islands with DFS mutation
Count increments only when finding `'1'`.

---

# PART 21: COMPLEXITY CHEAT

| Problem | Time | Space |
|---|---|---|
| Spiral / rotate / set zero | O(RC) | O(1) extra (set zero markers) |
| Search sorted I | O(log(RC)) | O(1) |
| Search II | O(R+C) | O(1) |
| Islands / flood | O(RC) | O(RC) stack worst |
| Multi-source BFS | O(RC) | O(RC) |
| Unique paths DP | O(RC) or O(C) | O(C) |

---

# PART 22: 30-MINUTE DRILL

1. Spiral + rotate from memory.  
2. Set zeroes O(1) space narrative.  
3. Islands + max area.  
4. 01 matrix multi-source.  
5. Unique paths + obstacles.  
6. Classify 5 prompts as transform/search/graph/DP.

---

**End of Matrix lesson.** Status: `content-delivered`.

---

# PART 23: GRID AS GRAPH — EXPLICIT BUILD (RARELY NEEDED)

```python
def grid_to_adj(grid, walls=None):
    R, C = len(grid), len(grid[0])
    adj = {}
    for r in range(R):
        for c in range(C):
            if walls and grid[r][c] in walls:
                continue
            adj[(r,c)] = []
            for dr,dc in DIRS4:
                nr,nc=r+dr,c+dc
                if 0<=nr<R and 0<=nc<C and not (walls and grid[nr][nc] in walls):
                    adj[(r,c)].append((nr,nc))
    return adj
```

Usually **don't** build this — generate neighbors on the fly.

---

# PART 24: ROTTING ORANGES FULL TRACE

```
minute0:
2 1 1
1 1 0
0 1 1

minute1:
2 2 1
2 1 0
0 1 1

minute2:
2 2 2
2 2 0
0 1 1

minute3:
2 2 2
2 2 0
0 2 1

minute4:
2 2 2
2 2 0
0 2 2
→ 4
```

---

# PART 25: UNIQUE PATHS DP TABLE

`m=3,n=4`:
```
1 1 1 1
1 2 3 4
1 3 6 10
→ 10
```

Obstacles: zero a cell; dependents may become 0.

---

# PART 26: SEARCH MATRIX II TRACE

```
1  4  7 11 15
2  5  8 12 19
3  6  9 16 22
10 13 14 17 24
18 21 23 26 30
target 5: start 15 → left ... → down/left → find 5
target 20: walk off → False
```

---

# PART 27: BLIND CODE CHECKLIST

- [ ] Rows/cols dims correct  
- [ ] Empty grid  
- [ ] DIRS4 vs DIRS8  
- [ ] Mark visited on enqueue  
- [ ] Spiral guards  
- [ ] Flood early exit same color  

---

**Final status:** Matrix & Grid Patterns — `content-delivered`.

---

# PART 28: FULL WORKED SOLUTION BANK (MATRIX)

## S1–S6
Spiral, set zero, rotate, search I/II, islands, flood — Parts 3–8.

## S7 — Max Area of Island
DFS returns size; track max; mutate visited.

## S8 — 01 Matrix / Walls&Gates
Multi-source BFS from zeros/gates.

## S9 — Rotting Oranges
Multi-source level BFS; return minutes or -1 if fresh remain.

## S10 — Unique Paths / Obstacles / Min Path Sum
DP Parts 10–11; or combinatorics without obstacles.

## S11 — Surrounded Regions
DFS mark border-safe `'O'`→`'S'`; flip remaining `'O'`→`'X'`; restore `'S'`.

## S12 — Pacific Atlantic
Two reachable boolean matrices from each ocean; intersect.

## S13 — Shortest Path Binary Matrix
8-dir BFS; mark on enqueue; return dist or -1.

## S14 — Maximal Square
`dp = min(up,left,diag)+1` on `'1'` cells; track max side².

---

# PART 29: DECISION TREE

```
transform in-place → spiral/rotate/set0
sorted query → binsearch or corner walk
components/flood → DFS/BFS
shortest steps → BFS (± multi-source)
path counts/sums right-down → DP/nCr
```

---

# PART 30: ORAL EXAM

1. Spiral double-count failure mode.  
2. Why clear first row/col last in set-zero.  
3. Multi-source correctness (first touch).  
4. DP vs BFS.  
5. Flood same-color infinite loop.

---

# PART 31: FINAL MATRIX MASTERY CHECK

DIRS4 · spiral · zeros · rotate · search · islands · multi-source · grid DP.

**Final status:** Matrix & Grid Patterns — `content-delivered`.

---

# PART — LONGEST INCREASING PATH IN MATRIX (LC 329)

Grid DFS + memo. From each cell, longest strictly increasing path (4-dir).

## Framework

```
dfs(r,c) = 1 + max(dfs(nr,nc) for neighbors with grid[nr][nc] > grid[r][c], else 0)
memo[(r,c)] = that value
answer = max dfs over all cells
```

This is **graph DP on DAG** of cell→larger-neighbor edges (acyclic because values strictly increase).

```python
def longest_increasing_path(matrix):
    if not matrix or not matrix[0]:
        return 0
    R, C = len(matrix), len(matrix[0])
    memo = {}

    def dfs(r, c):
        if (r, c) in memo:
            return memo[(r, c)]
        best = 1
        for nr, nc in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[(r, c)] = best
        return best

    return max(dfs(r, c) for r in range(R) for c in range(C))
```

### Worked trace

```
matrix = [
  [9, 9, 4],
  [6, 6, 8],
  [2, 1, 1],
]
```

Compute bottom-up by dependency (or memo as you go). Strictly increasing neighbors only.

Example cell `(2,1)=1`:
- right `(2,2)=1` not greater
- up `(1,1)=6` greater → path continues from 6
- left `(2,0)=2` greater → path continues from 2

From `(2,0)=2` → up `(1,0)=6` → up `(0,0)=9` → stop. Length from 2: `1+1+1=3` (2→6→9).  
From `(1,1)=6` → right `(1,2)=8` → stop, or up 9. Best arm length 2 (6→8 or 6→9).  
So `dfs(2,1) = 1 + max(dfs(2,0), dfs(1,1), ...) = 1 + max(3, 2, ...) = 4`  
One longest path in the grid: `1 → 2 → 6 → 9` (length **4**).

**Memo:** each cell’s answer stored once → total O(R·C) edges examined.

**Complexity:** O(R·C) time/space — each cell computed once.

**Trap:** Without memo → exponential. Without strict `>` → cycles / infinite recursion.

## Teach-back

Why is the graph a DAG? Where does memo key live?
