# Answer Key — Module 11 Final Assessment.md

**Source questions:** `Retention Questions/Module 11 Final Assessment.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
**Answer:** Drop constants; drop non-dominant terms; different inputs → different variables.

---


<!-- answer block 2 -->
**Answer:** O(n²) — triangle number of iterations.

---


<!-- answer block 3 -->
**Answer:** Immutable strings; each concat copies. Use list + `join`.

---


<!-- answer block 4 -->
**Answer:** When negatives (or non-monotone sums) exist — use prefix + hash.

---


<!-- answer block 5 -->
**Answer:** One-pass hash map value→index. O(n)/O(n).

---


<!-- answer block 6 -->
**Answer:** `prefix[r+1] - prefix[l]`.

---


<!-- answer block 7 -->
**Answer:** O(d) stack (Python: no TCO; ~1000 limit).

---


<!-- answer block 8 -->
**Answer:** Overlapping subproblems + polynomial state space.

---


<!-- answer block 9 -->
**Answer:** The boolean predicate / invariant (what is true on the left vs right of `lo`/`hi`).

---


<!-- answer block 10 -->
**Answer:** Merge: O(n log n) time, O(n) space. Quick: avg O(n log n), worst O(n²); expected O(n log n) with random pivot.

---


<!-- answer block 11 -->
**Answer:** Uniform handling when head may change (delete, merge, remove nth from end).

---


<!-- answer block 12 -->
**Answer:** One pointer to head; both step +1; meet at entrance.

---


<!-- answer block 13 -->
**Answer:** Stack = `list` append/pop. Queue = `deque` append/popleft. Never `list.pop(0)` hot path.

---


<!-- answer block 14 -->
**Answer:** Each index pushed and popped at most once.

---


<!-- answer block 15 -->
**Answer:** Decreasing deque of indices; front = max; expire left.

---


<!-- answer block 16 -->
**Answer:** Root-L-R; L-Root-R; L-R-Root.

---


<!-- answer block 17 -->
**Answer:** No — entire left subtree < node < entire right. Use bounds or inorder increasing.

---


<!-- answer block 18 -->
**Answer:** O(1) peek; O(log n) insert/extract.

---


<!-- answer block 19 -->
**Answer:** BFS queue; DFS stack/recursion.

---


<!-- answer block 20 -->
**Answer:** Cycle in directed graph.

---


<!-- answer block 21 -->
**Answer:** Dynamic connectivity / components with near-O(1) union and find (with path compression + union by rank).

---


<!-- answer block 22 -->
**Answer:** Shortest paths from source on graphs with **non-negative** weights.

---


<!-- answer block 23 -->
**Answer:** 0/1: each item once (loop capacity downward or 2D). Unbounded: item reusable (coin change style loops).

---


<!-- answer block 24 -->
**Answer:** Choose → explore → unchoose (push/recurse/pop).

---


<!-- answer block 25 -->
**Answer:** Search requires `is_end`; startsWith only requires path exists.

---


<!-- answer block 26 -->
**Answer:** Non-decreasing digits; pop larger left peaks while k > 0.

---


<!-- answer block 27 -->
**Answer:** O(log n) each. Static → prefer prefix sums.

---


<!-- answer block 28 -->
**Answer:** Sort by end time; take next compatible (earliest finishing).

---


<!-- answer block 29 -->
**Answer:** Expand `right` to include new element; update state (sum/counts/set); while invariant violated, shrink `left` and undo state; track best. Amortized O(n) if each pointer moves ≤ n times. State must support O(1) add/remove.

---


<!-- answer block 30 -->
**Answer:** Running prefix `p`; need prior prefixes equal to `p-k`; store frequencies of prefixes seen; `freq[0]=1` for subarrays from start. O(n). Works with negatives.

---


<!-- answer block 31 -->
**Answer:** log n levels; each level total work O(n); product O(n log n).

---


<!-- answer block 32 -->
**Answer:** When feasibility is monotone in a numeric answer (e.g., "can we finish in mid days?"). Binary search `mid`, check predicate O(f), total O(f log range).

---


<!-- answer block 33 -->
**Answer:** For each bar, width = distance between previous smaller and next smaller. Increasing stack finds those bounds; area = h×width. O(n).

---


<!-- answer block 34 -->
**Answer:** Tree `5 → right 6 → left 4`. Local OK; bounds on 4 require >5 → fail.

---


<!-- answer block 35 -->
**Answer:** Relaxation assumption breaks; negative cycles possible. Bellman-Ford / other (PREVIEW depth OK). Don't use Dijkstra.

---


<!-- answer block 36 -->
**Answer:** Fib/climb stairs/coin change: optimal solution built from smaller amounts; same sub-amount recomputed → memo/tabulate.

---


<!-- answer block 37 -->
**Answer:** Exact membership → set. Prefix/autocomplete/wildcard/shortest root → trie.

---


<!-- answer block 38 -->
**Answer:** "Prefix sums if static. If updates interleave, Fenwick or segment tree, O(log n) update and query. I can sketch Fenwick for sums." (Exposure — don't force 100-line segtree.)

---


<!-- answer block 39 -->
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


<!-- answer block 40 -->
**Answer:** Set; only start runs where `x-1 not in set`. O(n).

---


<!-- answer block 41 -->
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


<!-- answer block 42 -->
**Answer:** Reverse: save/rewire/advance three pointers. Cycle: Floyd slow/fast.

---


<!-- answer block 43 -->
**Answer:** Decreasing mono stack of indices; `ans[j]=i-j` on pop. O(n).

---


<!-- answer block 44 -->
**Answer:** BFS with deque; zigzag alternates append direction or reverse odd levels.

---


<!-- answer block 45 -->
**Answer:** Min-heap of size k. O(n log k).

---


<!-- answer block 46 -->
**Answer:** Hash map old→new; BFS/DFS copy neighbors. O(V+E).

---


<!-- answer block 47 -->
**Answer:** Topo / cycle detect DFS colors or Kahn indegree. Cycle ⇒ false.

---


<!-- answer block 48 -->
**Answer:** O(n²): `dp[i]=1+max(dp[j])` for j<i with a[j]<a[i]. O(n log n): tails binary search patience method.

---


<!-- answer block 49 -->
**Answer:** DFS with start index; reuse allowed → recurse `i` not `i+1`; prune when remain < 0.

---


<!-- answer block 50 -->
**Answer:** Trie skeleton standard. Remove k: pop first `1`? Actually `"112"` k=1 → pop last possible peak: stack [1,1,2], no pop during (non-decreasing), k left → pop end → `"11"`.

---


<!-- answer block 51 -->
**Answer:** **False.** Two pointers O(1) extra space; hash O(n) space. Sorted enables two pointers.

---


<!-- answer block 52 -->
**Answer:** **False** (for general positive weights). BFS = unweighted (or equal weight). Weighted → Dijkstra/0-1 BFS variants.

---


<!-- answer block 53 -->
**Answer:** Stack overflow / recursion limit; use loop. Also unnecessary.

---


<!-- answer block 54 -->
**Answer:** Usually no — monotonic deque is expected. Segtree = overkill unless interviewer asks.

---


<!-- answer block 55 -->
**Answer:** Tree DP OK along DAG of subtrees. General graph cycles need care (not naive tree recursion).

---


<!-- answer block 56 -->
**Answer:** No — `RuntimeError` if size changes during iterate. Copy keys or collect then mutate.

---


<!-- answer block 57 -->
**Answer:** O(n²) on adversarial pivots. Say so; mention random pivot.

---


<!-- answer block 58 -->
**Answer:** **Not allowed.** Threshold 70% on last 20 timed mediums. Keep drilling.

---


<!-- answer block 59 -->
**Answer (model):**
1. Input type: array/string/LL/tree/graph/stream?
2. Ask: contiguous? → window/prefix/mono deque. Pairs/complements? → hash/two ptr. Ordering/next greater? → mono stack. Hierarchy? → tree. Dependencies? → graph. Optimize count/min/max with subproblems? → DP. Enumerate? → BT. Prefix words? → trie.
3. Constraints → rule out O(n²) if n=10^5.
4. Brute → optimize; state complexity; code; trace edges.

---


<!-- answer block 60 -->
**Answer:** Personal — must fill from `Metrics/Retention Ledger.md`. Assessment incomplete without this honesty (G2/G7 spirit).

---


<!-- answer block 61 -->
**Answer:** Per Handoff enum — chat help = drilled only; complete needs retention + blind timed + ledger. No status inflation.

---


<!-- answer block 62 -->
**Answer:** Insert words in trie; DFS from each cell with trie node; mark visited; collect at end; prune. See Module 10.

**Rubric focus:** Clarity of trie pruning; backtracking correctness; complexity honesty.

---


<!-- answer block 63 -->
**Answer:** Contribution via prev/next smaller mono stacks; mod 10⁹+7. Strictness asymmetry for ties.

**Rubric focus:** Complexity talk; edge all-equal.

---


<!-- answer block 64 -->
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


<!-- answer block 65 -->
**Answer:** Occasional O(n) resize; average O(1) per append.

---


<!-- answer block 66 -->
**Answer:** Sorted order (or monotonic structure).

---


<!-- answer block 67 -->
**Answer:** Fixed: size k always. Variable: shrink/grow to maintain invariant.

---


<!-- answer block 68 -->
**Answer:** Initialize best/cur to first element (or track max element) — empty subarray disallowed variants differ.

---


<!-- answer block 69 -->
**Answer:** Count array[26] or Counter equality.

---


<!-- answer block 70 -->
**Answer:** Verify substring on hash hit; or double hash. (Advanced Hashing lesson.)

---


<!-- answer block 71 -->
**Answer:** Tree visualizes work per level; recurrence is algebraic form of same.

---


<!-- answer block 72 -->
**Answer:** Parentheses: never add `)` if closes ≥ opens.

---


<!-- answer block 73 -->
**Answer:** `lo,hi` answer space; if `ok(mid): hi=mid` else `lo=mid+1`.

---


<!-- answer block 74 -->
**Answer:** O(log n) stack expected; O(n) worst.

---


<!-- answer block 75 -->
**Answer:** Equal keys keep relative order. Timsort yes.

---


<!-- answer block 76 -->
**Answer:** prev, cur, nxt — save / rewire / advance.

---


<!-- answer block 77 -->
**Answer:** Walk both; switch heads when None — meet at intersection or None.

---


<!-- answer block 78 -->
**Answer:** Store (val, min_so_far) pairs.

---


<!-- answer block 79 -->
**Answer:** Stack; operands push; operator pops 2.

---


<!-- answer block 80 -->
**Answer:** At each node, candidate = left_h+right_h; track global max; return height upward.

---


<!-- answer block 81 -->
**Answer:** Controlled inorder stack; each node push/pop once.

---


<!-- answer block 82 -->
**Answer:** DFS return found nodes; if both sides nonempty current is LCA.

---


<!-- answer block 83 -->
**Answer:** Most nodes near leaves; Σ costs geometric O(n).

---


<!-- answer block 84 -->
**Answer:** max-heap left half, min-heap right; sizes differ ≤1; tops bound median.

---


<!-- answer block 85 -->
**Answer:** Min-heap of size K (root = Kth largest threshold).

---


<!-- answer block 86 -->
**Answer:** Unweighted (or equal weight) edges.

---


<!-- answer block 87 -->
**Answer:** Visiting gray neighbor ⇒ cycle.

---


<!-- answer block 88 -->
**Answer:** Amortized α(n) ≈ constant.

---


<!-- answer block 89 -->
**Answer:** Min-heap of (dist, node); relax neighbors; skip outdated pops.

---


<!-- answer block 90 -->
**Answer:** Classic `dp[i][w]` or 1D backward capacity loop.

---


<!-- answer block 91 -->
**Answer:** If equal: 1+LCS(i-1,j-1) else max(LCS(i-1,j), LCS(i,j-1)).

---


<!-- answer block 92 -->
**Answer:** Earliest end leaves max room; exchange argument.

---


<!-- answer block 93 -->
**Answer:** Don't remove nodes still needed by longer words — clear is_end + prune empty.

---


<!-- answer block 94 -->
**Answer:** Asymmetric strictness on left/right spans.

---


<!-- answer block 95 -->
**Answer:** lstrip `0`; empty → `"0"`.

---


<!-- answer block 96 -->
**Answer:** Dynamic vs static range sums.

---


<!-- answer block 97 -->
**Answer:** Associative combination from children (sum/min/max/gcd…).

---


<!-- answer block 98 -->
**Answer:** Yes overkill — use mono deque.

---


<!-- answer block 99 -->
**Answer:** O(n) auxiliary typically.

---


<!-- answer block 100 -->
**Answer:** Sorted order.

---


<!-- answer block 101 -->
**Answer:** O(V+E).

---


<!-- answer block 102 -->
**Answer:** Greedy local choice proves global; DP considers many substates when greedy fails.

---


<!-- answer block 103 -->
**Answer:** `(r,c)` or 2D table.

---


<!-- answer block 104 -->
**Answer:** Lowest set bit — Fenwick jumps / some bit DPs.

---


<!-- answer block 105 -->
**Answer:** ~1000 default.

---


<!-- answer block 106 -->
**Answer:** Large n (1e5); constants matter but asymptotics dominate.

---


<!-- answer block 107 -->
**Answer:** Indices in decreasing value order.

---


<!-- answer block 108 -->
**Answer:** b prerequisite of a → b→a.

---


<!-- answer block 109 -->
**Answer:** Both MST; Prim grows tree; Kruskal sorts edges + UF.

---


<!-- answer block 110 -->
**Answer:** O(n·2ⁿ).

---


<!-- answer block 111 -->
**Answer:** Chaining; open addressing.

---


<!-- answer block 112 -->
**Answer:** Concat in loop copies → O(n²); use list join.

---


<!-- answer block 113 -->
**Answer:** O(n) for wide level / queue.

---


<!-- answer block 114 -->
**Answer:** `dp[0]=0`, rest INF; relax `dp[x]=min(dp[x], dp[x-c]+1)`.

---


<!-- answer block 115 -->
**Answer:** ≥70% first-pass on last 20 timed mediums.

---


<!-- answer block 116 -->
**Answer:** **No** — drilled only.

---


<!-- answer block 117 -->
**Answer:** O(n log n).

---


<!-- answer block 118 -->
**Answer:** Read/write pointer — write non-zeros forward; fill zeros. O(n)/O(1).

---


<!-- answer block 119 -->
**Answer:** Counter then scan; or OrderedDict frequency.

---


<!-- answer block 120 -->
**Answer:** Exponentiation by squaring O(log n).

```python
def myPow(x, n):
    if n < 0: return 1/myPow(x, -n)
    if n == 0: return 1
    half = myPow(x, n//2)
    return half*half if n%2==0 else half*half*x
```

---


<!-- answer block 121 -->
**Answer:** Lower bound bisect template. O(log n).

---


<!-- answer block 122 -->
**Answer:** Two pointers into output. O(n+m).

---


<!-- answer block 123 -->
**Answer:** Slow/fast mid; reverse second half; compare. O(n)/O(1).

---


<!-- answer block 124 -->
**Answer:** Mono decreasing indices. O(n).

---


<!-- answer block 125 -->
**Answer:** `1+max(left,right)`; empty 0. O(n).

---


<!-- answer block 126 -->
**Answer:** 0 children; 1 child; 2 children → successor/predecessor swap.

---


<!-- answer block 127 -->
**Answer:** Min-heap of (val, list_id, node). O(N log K).

---


<!-- answer block 128 -->
**Answer:** Map + BFS/DFS. O(V+E).

---


<!-- answer block 129 -->
**Answer:** Union edges; first failing union is redundant.

---


<!-- answer block 130 -->
**Answer:** `dp[0][0]` set; zeros on obstacle; sum from top/left.

---


<!-- answer block 131 -->
**Answer:** Sort; skip `i>start and nums[i]==nums[i-1]`.

---


<!-- answer block 132 -->
**Answer:** Track farthest reachable. O(n).

---


<!-- answer block 133 -->
**Answer:** Walk; no is_end needed.

---


<!-- answer block 134 -->
**Answer:** Stack (price, span). Amortized O(1).

---


<!-- answer block 135 -->
**Answer:** Static queries; window max; tiny n.

---


<!-- answer block 136 -->
**Answer:** knowledge-gap / misread / time-pressure / careless-slip — 100% of timed misses.

---


<!-- answer block 137 -->
**Answer:** `OrderedDict` move_to_end / popitem(last=False), or DLL+dict. O(1) ops.

---


<!-- answer block 138 -->
**Answer:** Full code in `Advanced/Tries & Monotonic.md` Part 7E.

---


<!-- answer block 139 -->
**Answer:** Prefix sums.

---


<!-- answer block 140 -->
**Answer:** Fenwick/segment.

---


<!-- answer block 141 -->
**Answer:** Monotonic deque.

---


<!-- answer block 142 -->
**Answer:** Trie (or sorted+bisect).

---


<!-- answer block 143 -->
**Answer:** BFS.

---


<!-- answer block 144 -->
**Answer:** Dijkstra.

---


<!-- answer block 145 -->
**Answer:** Only special coin systems; general → DP.

---


<!-- answer block 146 -->
**Answer:** Explain shape+complexity; offer Fenwick code for sums; don't derail into lazy unless asked.

---


<!-- answer block 147 -->
**Answer:** No first-pass credit; add redo queue G6.

---


<!-- answer block 148 -->
**Answer:** No — need ≥4.0 on last 4 mocks.

---


