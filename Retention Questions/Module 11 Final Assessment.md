# MODULE 11 FINAL ASSESSMENT — PHASE A CUMULATIVE

**With answers.** This is the end-of–Phase A written/oral assessment. It does **not** replace gates G1–G7; it feeds evidence for G1 (teach-back) and retention. Pair with `Gauntlet/Phase A Gauntlet.md` for timed mocks (G3–G5).

**Rules:**
1. Blind first. Cover answers.
2. Tag misses: `knowledge-gap` / `misread` / `time-pressure` / `careless-slip`.
3. Update ledger + scoreboard after scoring.
4. Fenwick/segment = **exposure** only.
5. Master Theorem: only if Module 3 Sorting was completed; otherwise recurrence-tree reasoning is enough.

**Suggested pass bar:**  
Section A ≥ 85% · B teach-backs solid · C ≥ 70% first-pass reasoning · D judgment ≥ 80% · E synthesis coherent.  
Any `weak` family → gauntlet weak-spot loop before Phase A declaration.

---

# SECTION A: RAPID FIRE — ALL PHASE A

One breath each.

---

## A1. Three Big-O simplification rules?

**Answer:** Drop constants; drop non-dominant terms; different inputs → different variables.

---

## A2. `for i in range(n): for j in range(i):` complexity?

**Answer:** O(n²) — triangle number of iterations.

---

## A3. Why is `s = s + c` in a loop O(n²) in Python?

**Answer:** Immutable strings; each concat copies. Use list + `join`.

---

## A4. Variable sliding window fails for subarray sum = k when?

**Answer:** When negatives (or non-monotone sums) exist — use prefix + hash.

---

## A5. Two Sum unsorted — best expected approach?

**Answer:** One-pass hash map value→index. O(n)/O(n).

---

## A6. Prefix sum formula for `sum(l..r)` with `prefix[0]=0`, `prefix[i]=sum(a[0..i-1])`?

**Answer:** `prefix[r+1] - prefix[l]`.

---

## A7. Recursion space for depth-d call chain?

**Answer:** O(d) stack (Python: no TCO; ~1000 limit).

---

## A8. Memoization helps when?

**Answer:** Overlapping subproblems + polynomial state space.

---

## A9. Binary search: what must you define precisely?

**Answer:** The boolean predicate / invariant (what is true on the left vs right of `lo`/`hi`).

---

## A10. Merge sort time/space? Quicksort average/worst?

**Answer:** Merge: O(n log n) time, O(n) space. Quick: avg O(n log n), worst O(n²); expected O(n log n) with random pivot.

---

## A11. Dummy head in linked lists — why?

**Answer:** Uniform handling when head may change (delete, merge, remove nth from end).

---

## A12. Floyd cycle: how find entrance after meeting?

**Answer:** One pointer to head; both step +1; meet at entrance.

---

## A13. Stack vs queue Python implementations?

**Answer:** Stack = `list` append/pop. Queue = `deque` append/popleft. Never `list.pop(0)` hot path.

---

## A14. Monotonic stack O(n) reason?

**Answer:** Each index pushed and popped at most once.

---

## A15. Sliding window maximum structure?

**Answer:** Decreasing deque of indices; front = max; expire left.

---

## A16. Tree preorder / inorder / postorder visit order?

**Answer:** Root-L-R; L-Root-R; L-R-Root.

---

## A17. BST invariant — local child check enough?

**Answer:** No — entire left subtree < node < entire right. Use bounds or inorder increasing.

---

## A18. Heap peek / insert / extract-min complexities (binary heap)?

**Answer:** O(1) peek; O(log n) insert/extract.

---

## A19. BFS vs DFS primary data structures?

**Answer:** BFS queue; DFS stack/recursion.

---

## A20. Topological sort — when impossible?

**Answer:** Cycle in directed graph.

---

## A21. Union-Find use case one-liner?

**Answer:** Dynamic connectivity / components with near-O(1) union and find (with path compression + union by rank).

---

## A22. Dijkstra finds?

**Answer:** Shortest paths from source on graphs with **non-negative** weights.

---

## A23. 0/1 knapsack vs unbounded — DP difference (one line)?

**Answer:** 0/1: each item once (loop capacity downward or 2D). Unbounded: item reusable (coin change style loops).

---

## A24. Backtracking three steps?

**Answer:** Choose → explore → unchoose (push/recurse/pop).

---

## A25. Trie: search vs startsWith?

**Answer:** Search requires `is_end`; startsWith only requires path exists.

---

## A26. Remove k digits — stack monotonicity?

**Answer:** Non-decreasing digits; pop larger left peaks while k > 0.

---

## A27. Fenwick exposure: update + range sum?

**Answer:** O(log n) each. Static → prefer prefix sums.

---

## A28. Greedy interval scheduling classic rule?

**Answer:** Sort by end time; take next compatible (earliest finishing).

---

# SECTION B: CONCEPTUAL TEACH-BACKS

---

## B1. Teach the sliding-window framework (variable size) in under 1 minute.

**Answer:** Expand `right` to include new element; update state (sum/counts/set); while invariant violated, shrink `left` and undo state; track best. Amortized O(n) if each pointer moves ≤ n times. State must support O(1) add/remove.

---

## B2. Explain hash map for "count subarrays with sum k."

**Answer:** Running prefix `p`; need prior prefixes equal to `p-k`; store frequencies of prefixes seen; `freq[0]=1` for subarrays from start. O(n). Works with negatives.

---

## B3. Recursion tree for T(n)=2T(n/2)+O(n) → O(n log n) without naming MT.

**Answer:** log n levels; each level total work O(n); product O(n log n).

---

## B4. Binary search on answer — when?

**Answer:** When feasibility is monotone in a numeric answer (e.g., "can we finish in mid days?"). Binary search `mid`, check predicate O(f), total O(f log range).

---

## B5. Histogram largest rectangle — mono stack story.

**Answer:** For each bar, width = distance between previous smaller and next smaller. Increasing stack finds those bounds; area = h×width. O(n).

---

## B6. Validate BST with bounds — walk an example that fools local checks.

**Answer:** Tree `5 → right 6 → left 4`. Local OK; bounds on 4 require >5 → fail.

---

## B7. Why Dijkstra fails with negative edges; what instead (name only)?

**Answer:** Relaxation assumption breaks; negative cycles possible. Bellman-Ford / other (PREVIEW depth OK). Don't use Dijkstra.

---

## B8. DP definition: optimal substructure + overlapping — example.

**Answer:** Fib/climb stairs/coin change: optimal solution built from smaller amounts; same sub-amount recomputed → memo/tabulate.

---

## B9. Trie vs hash set decision.

**Answer:** Exact membership → set. Prefix/autocomplete/wildcard/shortest root → trie.

---

## B10. Interview: "point updates + range sums?" — 30-second answer.

**Answer:** "Prefix sums if static. If updates interleave, Fenwick or segment tree, O(log n) update and query. I can sketch Fenwick for sums." (Exposure — don't force 100-line segtree.)

---

# SECTION C: PROBLEM SOLVING (MIXED MEDIUM/HARD)

Full solutions. Aim ≥ 8/12 solid.

---

## C1. Container With Most Water

**Answer:** Two pointers at ends; move the shorter side inward. O(n).

```python
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best
```

---

## C2. Longest Consecutive Sequence

**Answer:** Set; only start runs where `x-1 not in set`. O(n).

---

## C3. Search in Rotated Sorted Array

**Answer:** Binary search; identify which half is sorted; decide where target lies. O(log n).

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

---

## C4. Reverse Linked List + detect cycle (state both)

**Answer:** Reverse: save/rewire/advance three pointers. Cycle: Floyd slow/fast.

---

## C5. Daily Temperatures

**Answer:** Decreasing mono stack of indices; `ans[j]=i-j` on pop. O(n).

---

## C6. Level Order + Zigzag (describe)

**Answer:** BFS with deque; zigzag alternates append direction or reverse odd levels.

---

## C7. Kth Largest in Stream / Array

**Answer:** Min-heap of size k. O(n log k).

---

## C8. Clone Graph

**Answer:** Hash map old→new; BFS/DFS copy neighbors. O(V+E).

---

## C9. Course Schedule (can finish?)

**Answer:** Topo / cycle detect DFS colors or Kahn indegree. Cycle ⇒ false.

---

## C10. LIS length O(n log n) sketch OR O(n²) DP

**Answer:** O(n²): `dp[i]=1+max(dp[j])` for j<i with a[j]<a[i]. O(n log n): tails binary search patience method.

---

## C11. Combination Sum (backtracking)

**Answer:** DFS with start index; reuse allowed → recurse `i` not `i+1`; prune when remain < 0.

---

## C12. Implement Trie + one Remove K Digits trace `"112", k=1`

**Answer:** Trie skeleton standard. Remove k: pop first `1`? Actually `"112"` k=1 → pop last possible peak: stack [1,1,2], no pop during (non-decreasing), k left → pop end → `"11"`.

---

# SECTION D: TRICK / JUDGMENT

---

## D1. True/False: Sorted array + hash set is always better than two pointers for pair sum.

**Answer:** **False.** Two pointers O(1) extra space; hash O(n) space. Sorted enables two pointers.

---

## D2. True/False: BFS shortest path works on weighted graphs.

**Answer:** **False** (for general positive weights). BFS = unweighted (or equal weight). Weighted → Dijkstra/0-1 BFS variants.

---

## D3. You used recursion for factorial of n=10^6. Issue?

**Answer:** Stack overflow / recursion limit; use loop. Also unnecessary.

---

## D4. Window max via segment tree in a 45-min screen — good idea?

**Answer:** Usually no — monotonic deque is expected. Segtree = overkill unless interviewer asks.

---

## D5. DP on tree vs graph with cycles.

**Answer:** Tree DP OK along DAG of subtrees. General graph cycles need care (not naive tree recursion).

---

## D6. `dict` iteration while inserting — safe?

**Answer:** No — `RuntimeError` if size changes during iterate. Copy keys or collect then mutate.

---

## D7. Quickselect worst case without randomization?

**Answer:** O(n²) on adversarial pivots. Say so; mention random pivot.

---

## D8. Phase A declaration with G3 at 60%?

**Answer:** **Not allowed.** Threshold 70% on last 20 timed mediums. Keep drilling.

---

# SECTION E: SYNTHESIS / SYSTEMS OF THOUGHT

---

## E1. Given a new problem, outline your 60-second classification checklist.

**Answer (model):**
1. Input type: array/string/LL/tree/graph/stream?
2. Ask: contiguous? → window/prefix/mono deque. Pairs/complements? → hash/two ptr. Ordering/next greater? → mono stack. Hierarchy? → tree. Dependencies? → graph. Optimize count/min/max with subproblems? → DP. Enumerate? → BT. Prefix words? → trie.
3. Constraints → rule out O(n²) if n=10^5.
4. Brute → optimize; state complexity; code; trace edges.

---

## E2. Pick three patterns you are weakest on (from ledger). For each: one drill problem + error type you usually make.

**Answer:** Personal — must fill from `Metrics/Retention Ledger.md`. Assessment incomplete without this honesty (G2/G7 spirit).

---

## E3. Explain to a junior: difference between `taught`, `drilled`, `retention-passed`, `timed-verified`, `complete`.

**Answer:** Per Handoff enum — chat help = drilled only; complete needs retention + blind timed + ledger. No status inflation.

---

# SECTION F: FULL WORKED HARD (CHOOSE ONE TO WRITE OUT)

Proctor picks one; reference below.

---

## F1. Word Search II (board + trie)

**Answer:** Insert words in trie; DFS from each cell with trie node; mark visited; collect at end; prune. See Module 10.

**Rubric focus:** Clarity of trie pruning; backtracking correctness; complexity honesty.

---

## F2. Sum of Subarray Minimums

**Answer:** Contribution via prev/next smaller mono stacks; mod 10⁹+7. Strictness asymmetry for ties.

**Rubric focus:** Complexity talk; edge all-equal.

---

## F3. Serialize / Deserialize Binary Tree

**Answer:** Preorder with null markers, or level-order BFS. Parse recursively or with queue.

```python
class Codec:
    def serialize(self, root):
        def dfs(node):
            if not node:
                return ["#"]
            return [str(node.val)] + dfs(node.left) + dfs(node.right)
        return ",".join(dfs(root))

    def deserialize(self, data):
        vals = iter(data.split(","))
        def dfs():
            v = next(vals)
            if v == "#":
                return None
            node = TreeNode(int(v))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()
```

---

# SECTION G: TIMED MINI-SET (30–40 MIN) — ANSWERS

Do under timer; then check.

### G1. Valid Parentheses — stack map open→close. O(n).

### G2. Maximum Subarray (Kadane) — running best ending here. O(n).

```python
def max_sub_array(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

### G3. Invert Binary Tree — swap children recurse/BFS. O(n).

### G4. Meeting Rooms II (min rooms) — sort starts/ends or heap of end times. O(n log n).

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort()
    heap = []  # end times
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

---

# SECTION H: SCORECARD

| Section | Score | Notes / tags |
|---|---|---|
| A Rapid fire (/28) | | |
| B Teach-back (/10) | | |
| C Problems (/12) | | |
| D Tricks (/8) | | |
| E Synthesis (/3) | | |
| F Hard | | |
| G Timed mini (/4) | | |

**Families to re-queue on ledger:** _______________

**Ready to attempt Phase A declaration checklist?** Y/N (only if G1–G7 evidence exists — this assessment alone is insufficient)

---

# SECTION I: ANSWER KEY INDEX

| ID | Kernel |
|---|---|
| A1–A28 | See Section A |
| C1 | Two pointers water |
| C2 | Set consecutive |
| C3 | Rotated binary search |
| C5 | Mono stack temps |
| C10 | LIS DP / patience |
| C12 | Remove k → `"11"` |
| D2 | BFS ≠ weighted shortest |
| D4 | Deque not segtree |
| D8 | G3 70% gate |
| F1–F3 | Hard references |
| G1–G4 | Mini timed answers |

---

**After this assessment:** Run or continue `Gauntlet/Phase A Gauntlet.md` until G1–G7 pass. Then optional Phase B (CP) or Phase C (System Design).

*End of Module 11 Final Assessment.*

---

# SECTION J: EXPANDED RAPID FIRE — FULL PHASE A (A29–A80)

---

## A29. Amortized array append — one sentence?

**Answer:** Occasional O(n) resize; average O(1) per append.

---

## A30. Opposite-ends two pointers need what precondition for pair sum?

**Answer:** Sorted order (or monotonic structure).

---

## A31. Fixed vs variable sliding window — difference?

**Answer:** Fixed: size k always. Variable: shrink/grow to maintain invariant.

---

## A32. Kadane handles all-negative how?

**Answer:** Initialize best/cur to first element (or track max element) — empty subarray disallowed variants differ.

---

## A33. Anagram check O(L) tool?

**Answer:** Count array[26] or Counter equality.

---

## A34. Rolling hash exposure — collision handling?

**Answer:** Verify substring on hash hit; or double hash. (Advanced Hashing lesson.)

---

## A35. Recursion tree vs recurrence — relationship?

**Answer:** Tree visualizes work per level; recurrence is algebraic form of same.

---

## A36. Backtracking prune example?

**Answer:** Parentheses: never add `)` if closes ≥ opens.

---

## A37. Binary search first True in monotone predicate — template idea?

**Answer:** `lo,hi` answer space; if `ok(mid): hi=mid` else `lo=mid+1`.

---

## A38. Quicksort space average?

**Answer:** O(log n) stack expected; O(n) worst.

---

## A39. Stable sort meaning? Python sort stable?

**Answer:** Equal keys keep relative order. Timsort yes.

---

## A40. LL reverse three pointers?

**Answer:** prev, cur, nxt — save / rewire / advance.

---

## A41. Intersection of two LL — length align method?

**Answer:** Walk both; switch heads when None — meet at intersection or None.

---

## A42. Min stack O(1) — how?

**Answer:** Store (val, min_so_far) pairs.

---

## A43. Evaluate RPN — structure?

**Answer:** Stack; operands push; operator pops 2.

---

## A44. Tree diameter via heights?

**Answer:** At each node, candidate = left_h+right_h; track global max; return height upward.

---

## A45. BST iterator — next amortized O(1)?

**Answer:** Controlled inorder stack; each node push/pop once.

---

## A46. Lowest Common Ancestor BT (not BST)?

**Answer:** DFS return found nodes; if both sides nonempty current is LCA.

---

## A47. Heapify Floyd why O(n)?

**Answer:** Most nodes near leaves; Σ costs geometric O(n).

---

## A48. Two-heap median invariant?

**Answer:** max-heap left half, min-heap right; sizes differ ≤1; tops bound median.

---

## A49. Top-K largest — heap type size K?

**Answer:** Min-heap of size K (root = Kth largest threshold).

---

## A50. BFS shortest path condition?

**Answer:** Unweighted (or equal weight) edges.

---

## A51. Detect cycle directed DFS colors?

**Answer:** Visiting gray neighbor ⇒ cycle.

---

## A52. Union by rank + path compression Ackermann?

**Answer:** Amortized α(n) ≈ constant.

---

## A53. Dijkstra structure?

**Answer:** Min-heap of (dist, node); relax neighbors; skip outdated pops.

---

## A54. 0/1 knapsack DP dim?

**Answer:** Classic `dp[i][w]` or 1D backward capacity loop.

---

## A55. LCS recurrence?

**Answer:** If equal: 1+LCS(i-1,j-1) else max(LCS(i-1,j), LCS(i,j-1)).

---

## A56. Greedy activity selection proof sketch?

**Answer:** Earliest end leaves max room; exchange argument.

---

## A57. Trie delete danger?

**Answer:** Don't remove nodes still needed by longer words — clear is_end + prune empty.

---

## A58. Sum subarray mins ties?

**Answer:** Asymmetric strictness on left/right spans.

---

## A59. Remove k digits zeros?

**Answer:** lstrip `0`; empty → `"0"`.

---

## A60. Fenwick vs prefix one line?

**Answer:** Dynamic vs static range sums.

---

## A61. Segment tree merge must be?

**Answer:** Associative combination from children (sum/min/max/gcd…).

---

## A62. Interview overkill: window max with segtree?

**Answer:** Yes overkill — use mono deque.

---

## A63. Space of mergesort?

**Answer:** O(n) auxiliary typically.

---

## A64. Inorder of BST yields?

**Answer:** Sorted order.

---

## A65. Graph adj list space?

**Answer:** O(V+E).

---

## A66. DP vs greedy distinction?

**Answer:** Greedy local choice proves global; DP considers many substates when greedy fails.

---

## A67. Memo key for grid unique paths with obstacles?

**Answer:** `(r,c)` or 2D table.

---

## A68. Bit trick: x & -x?

**Answer:** Lowest set bit — Fenwick jumps / some bit DPs.

---

## A69. Python recursion limit approx?

**Answer:** ~1000 default.

---

## A70. When is O(n log n) better than O(n²) practically?

**Answer:** Large n (1e5); constants matter but asymptotics dominate.

---

## A71. Sliding window max deque stores?

**Answer:** Indices in decreasing value order.

---

## A72. Course schedule edge [a,b]?

**Answer:** b prerequisite of a → b→a.

---

## A73. Prim vs Kruskal one line?

**Answer:** Both MST; Prim grows tree; Kruskal sorts edges + UF.

---

## A74. Backtracking time for subsets?

**Answer:** O(n·2ⁿ).

---

## A75. Hash collision resolution names?

**Answer:** Chaining; open addressing.

---

## A76. String immutability interview line?

**Answer:** Concat in loop copies → O(n²); use list join.

---

## A77. Tree BFS space worst?

**Answer:** O(n) for wide level / queue.

---

## A78. DP coin change fewest — init?

**Answer:** `dp[0]=0`, rest INF; relax `dp[x]=min(dp[x], dp[x-c]+1)`.

---

## A79. Phase A G3 threshold?

**Answer:** ≥70% first-pass on last 20 timed mediums.

---

## A80. Chat-guided solve counts as timed-verified?

**Answer:** **No** — drilled only.

---

# SECTION K: TOPIC-BY-TOPIC MINI PROBLEMS (WITH ANSWERS)

---

## K1. Big O: analyze

```python
for i in range(n):
    j = 1
    while j < n:
        j *= 2
```

**Answer:** O(n log n).

---

## K2. Arrays: move zeros in-place

**Answer:** Read/write pointer — write non-zeros forward; fill zeros. O(n)/O(1).

---

## K3. Hash: first unique char in stream / string

**Answer:** Counter then scan; or OrderedDict frequency.

---

## K4. Recursion: pow(x,n) fast

**Answer:** Exponentiation by squaring O(log n).

```python
def myPow(x, n):
    if n < 0: return 1/myPow(x, -n)
    if n == 0: return 1
    half = myPow(x, n//2)
    return half*half if n%2==0 else half*half*x
```

---

## K5. Binary search: search insert position

**Answer:** Lower bound bisect template. O(log n).

---

## K6. Sorting: merge two sorted lists/arrays

**Answer:** Two pointers into output. O(n+m).

---

## K7. LL: palindrome list

**Answer:** Slow/fast mid; reverse second half; compare. O(n)/O(1).

---

## K8. Stack: daily temperatures

**Answer:** Mono decreasing indices. O(n).

---

## K9. Tree: max depth

**Answer:** `1+max(left,right)`; empty 0. O(n).

---

## K10. BST: delete node cases

**Answer:** 0 children; 1 child; 2 children → successor/predecessor swap.

---

## K11. Heap: merge K sorted lists

**Answer:** Min-heap of (val, list_id, node). O(N log K).

---

## K12. Graph: clone graph

**Answer:** Map + BFS/DFS. O(V+E).

---

## K13. UF: redundant connection

**Answer:** Union edges; first failing union is redundant.

---

## K14. DP: unique paths with obstacles

**Answer:** `dp[0][0]` set; zeros on obstacle; sum from top/left.

---

## K15. BT: subsets with duplicates

**Answer:** Sort; skip `i>start and nums[i]==nums[i-1]`.

---

## K16. Greedy: jump game I

**Answer:** Track farthest reachable. O(n).

---

## K17. Trie: startsWith

**Answer:** Walk; no is_end needed.

---

## K18. Mono: stock span

**Answer:** Stack (price, span). Amortized O(1).

---

## K19. Fenwick exposure: when not to use

**Answer:** Static queries; window max; tiny n.

---

## K20. Interview meta: G7 tags

**Answer:** knowledge-gap / misread / time-pressure / careless-slip — 100% of timed misses.

---

# SECTION L: FULL SOLUTIONS — EXTRA CUMULATIVE HARDS

---

## L1. Min Window Substring

```python
from collections import Counter

def minWindow(s, t):
    need = Counter(t)
    missing = len(t)
    best = (0, float("inf"))
    left = 0
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best[1] == float("inf") else s[best[0]:best[1]+1]
```

---

## L2. LRU Cache (sketch)

**Answer:** `OrderedDict` move_to_end / popitem(last=False), or DLL+dict. O(1) ops.

---

## L3. Edit Distance

```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = list(range(n+1))
    for i in range(1, m+1):
        prev, dp[0] = dp[0], i
        for j in range(1, n+1):
            cur = dp[j]
            if word1[i-1] == word2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = cur
    return dp[n]
```

---

## L4. Binary Tree Max Path Sum

```python
def maxPathSum(root):
    best = float("-inf")
    def gain(node):
        nonlocal best
        if not node: return 0
        l = max(0, gain(node.left))
        r = max(0, gain(node.right))
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    gain(root)
    return best
```

---

## L5. Word Search II — reference pointer

**Answer:** Full code in `Advanced/Tries & Monotonic.md` Part 7E.

---

# SECTION M: JUDGMENT SCENARIOS

---

## M1. n=1e5, need range sum, no updates — tool?

**Answer:** Prefix sums.

---

## M2. n=1e5, updates + range sum — tool?

**Answer:** Fenwick/segment.

---

## M3. Find max in every window k — tool?

**Answer:** Monotonic deque.

---

## M4. Dictionary prefix queries — tool?

**Answer:** Trie (or sorted+bisect).

---

## M5. Shortest path unweighted — tool?

**Answer:** BFS.

---

## M6. Shortest path weighted nonnegative — tool?

**Answer:** Dijkstra.

---

## M7. Greedy coin change OK?

**Answer:** Only special coin systems; general → DP.

---

## M8. Interview 45 min, mentions segment tree follow-up — what do?

**Answer:** Explain shape+complexity; offer Fenwick code for sums; don't derail into lazy unless asked.

---

## M9. Failed timed medium with hint — G3 credit?

**Answer:** No first-pass credit; add redo queue G6.

---

## M10. Ready to declare Phase A with G5=3.8?

**Answer:** No — need ≥4.0 on last 4 mocks.

---

# SECTION N: SYNTHESIS ESSAY PROMPTS (MODEL ANSWERS SHORT)

---

## N1. "How do you choose between two pointers, sliding window, and prefix+hash?"

**Model:** Contiguous + monotone add/remove state → window. Contiguous + negatives / arbitrary sum k → prefix+hash. Sorted pairs / opposite ends → two pointers. State the invariant aloud.

---

## N2. "Map Phase A modules to interview smells."

**Model:** See Gauntlet Part 7 pattern table — recite 8+ smells with tools.

---

## N3. "What does complete mean in this program?"

**Model:** Status enum: taught→drilled→retention-passed→timed-verified→complete with ledger. No inflation.

---

# SECTION O: FINAL TIMED BATTERY (60 MIN) — ANSWERS

1. **Two Sum** — hash.  
2. **Invert Tree** — recurse swap.  
3. **Course Schedule** — topo/cycle.  
4. **Coin Change** — DP.  
5. **Remove K Digits** — mono stack.  

Score /5 first-pass; tag misses; update scoreboard.

---

# SECTION P: FINAL SCORECARD (EXPANDED)

| Block | Items | Score |
|---|---|---|
| A Rapid (1–28) | /28 | |
| A Rapid (29–80) | /52 | |
| B Teach-back | /10 | |
| C Problems | /12 | |
| D Tricks | /8 | |
| E Synthesis | /3 | |
| F Hard | /1 | |
| G Mini timed | /4 | |
| K Topic minis | /20 | |
| L Hards | /5 | |
| M Judgment | /10 | |
| O Battery | /5 | |

**Weak families for ledger:** ________________

**Attempt Phase A declaration?** Only with Gauntlet G1–G7 evidence — this file alone is insufficient.

---

*End of Module 11 Final Assessment (expanded).*

---

# SECTION Q: MODULE SWEEP — ONE PROBLEM EACH (ANSWERS)

| Module | Problem | Answer kernel |
|---|---|---|
| M1 Big O | Nested i, j=i..n | O(n²) |
| M1 Arrays | Max area water | Two pointers shorter move |
| M1 Window | Longest no repeat | Window + last index |
| M2 Hash | Subarray sum k count | Prefix freq |
| M2 Recursion | Subsets | BT start index |
| M3 BS | First bad version | lo/hi predicate |
| M3 Sort | Merge intervals | Sort + merge |
| M4 LL | Reverse list | 3 pointers |
| M4 Stack | Valid parentheses | Stack match |
| M4 Mono | Daily temps | Dec stack |
| M5 Tree | Level order | BFS |
| M5 BST | Validate | Bounds |
| M6 Heap | Kth largest | Min-heap size k |
| M6 Adv arr | Trap water | Two pointers / prefmax |
| M7 Graph | Islands | DFS flood |
| M7 Topo | Course schedule | Kahn/DFS |
| M8 UF | Provinces | Union-Find |
| M8 Dijkstra | Network delay | Heap relax |
| M8 DP | Coin change | dp amount |
| M9 DP2 | LIS | dp O(n²) or patience |
| M9 BT | Combos | DFS prune |
| M9 Greedy | Jump I | Farthest |
| M10 Trie | Implement | children+is_end |
| M10 Mono | Remove k digits | Inc digit stack |
| M10 Exp | Fenwick use | Dynamic range sum |

---

# SECTION R: FULL ANSWER — VALIDATE BST + TRACE

```python
def isValidBST(root):
    def ok(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))
```

Counterexample tree `5,1,4,null,null,3,6` fails at 3 (not >5).

---

# SECTION S: FULL ANSWER — COURSE SCHEDULE II TRACE

```
n=4, prereqs=[[1,0],[2,0],[3,1],[3,2]]
indeg=[0,1,1,2]
queue starts [0]
order: 0 → unlock 1,2 → then 3
order [0,1,2,3] or [0,2,1,3]
```

---

# SECTION T: FINAL ORAL EXAM (10 PROMPTS)

1. Teach Big O simplification rules.  
2. Window vs prefix+hash decision.  
3. Recursion stack space.  
4. Binary search invariant.  
5. LL dummy head why.  
6. Mono stack O(n) law.  
7. BST vs heap.  
8. BFS vs Dijkstra.  
9. DP state for coin change.  
10. Trie vs set; Fenwick when.

**Pass:** 8/10 solid without notes (G1 sample).

---

*End of Module 11 Final Assessment (expanded).*
