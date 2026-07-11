# Answer Key — Module 5 Retention.md

**Source questions:** `Retention Questions/Module 5 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
### Answer

- **Depth(node):** number of edges on the path from the **root** to that node. Root has depth 0.
- **Height(node):** number of edges on the longest path from that node **down to a leaf**. Leaf has height 0.
- **Height(empty tree):** **-1** (so a single-node tree has height 0).
- **LC 104 maxDepth:** counts **nodes** on the longest root→leaf path. Single node → **1**. Empty → **0**.

---


<!-- answer block 2 -->
### Answer

| Order | Result |
|---|---|
| Preorder | 1, 2, 4, 5, 3 |
| Inorder | 4, 2, 5, 1, 3 |
| Postorder | 4, 5, 2, 3, 1 |
| Level-order | [[1], [2, 3], [4, 5]] |
| Diameter (edges) | **3** (path 4-2-1-3 or 5-2-1-3) |

---


<!-- answer block 3 -->
### Answer

**False.** The BST invariant applies to **entire subtrees**, not only immediate children.

Counterexample:

```
      5
     / \
    1   6
       / \
      4   7
```

Local checks pass; `4` is in the right subtree of `5` but `4 < 5` → invalid.

Correct approach: **bounds method** `(low, high)` or verify inorder is strictly increasing.

---


<!-- answer block 4 -->
### Answer

| | Time | Space |
|---|---|---|
| Recursive DFS | Θ(n) | O(h) stack; O(n) if skewed |
| BFS level-order | Θ(n) | O(w) queue; O(n) worst (perfect tree bottom level ~ n/2) |

---


<!-- answer block 5 -->
### Answer

- Average (random / balanced): **O(log n)**
- Worst: **O(n)** when the tree is skewed (e.g., sorted insertion order into an unbalanced BST)
- Self-balancing trees (AVL / Red-Black) restore **O(log n)** height guarantees

---


<!-- answer block 6 -->
### Answer

Computes **max depth in nodes** (LC 104 style).

Time: each node visited once → **T(n) = Θ(n)** regardless of shape.  
(If writing a recurrence on perfect trees: `T(n) = 2T(n/2) + O(1) = Θ(n)`.)

Space: O(h) = O(log n) on perfect tree; O(n) if skewed.

---


<!-- answer block 7 -->
### Answer

| Prefer BST | Prefer Hash |
|---|---|
| Sorted iteration | Exact lookup only |
| Range queries `[L,R]` | No order needed |
| Kth / rank / predecessor / successor | Average O(1) ops |
| Closest value | Simpler in Python interviews |

**One-liner:** Hash optimizes **equality**. BST optimizes **order**.

---


<!-- answer block 8 -->
### Answer

| Quantity | Empty returns |
|---|---|
| Sum / count | 0 |
| Height (edges) | -1 |
| Max value | -∞ |
| Is balanced | True |

---


<!-- answer block 9 -->
### Answer

**Approach:** Explicit stack; drive to left spine; pop/visit; go right.

```python
def inorder_iterative(root):
    stack, out = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        out.append(curr.val)
        curr = curr.right
    return out
```

**Trace:**

```
curr=2 → stack=[2], curr=1
curr=1 → stack=[2,1], curr=None
pop 1, visit 1, curr=None
pop 2, visit 2, curr=3
curr=3 → stack=[3], curr=None
pop 3, visit 3
→ [1, 2, 3]
```

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 10 -->
### Answer

```python
def preorder_iterative(root):
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

**Why right then left:** Stack is LIFO. Pushing left last means left is popped next — preserving Node → Left → Right order.

---


<!-- answer block 11 -->
### Answer

1. **Null base** → return identity  
2. **Solve left and right** (leap of faith)  
3. **Combine** with current node  

```python
def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

def tree_max(node):
    if node is None:
        return float('-inf')
    return max(node.val, tree_max(node.left), tree_max(node.right))
```

---


<!-- answer block 12 -->
### Answer

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    result = []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result
```

`len(q)` at the start of the iteration freezes how many nodes belong to the **current** level so later enqueues don't get processed in the same round — required for zigzag, averages, right-side view, etc.

---


<!-- answer block 13 -->
### Answer

Examples: **height / max depth**, **diameter** (helper returns height), **is balanced** (return height + flag), **max path sum**, **House Robber III**, **LCA binary tree** (combine left/right hits).

Preorder alone is wrong when the combine depends on finished sub-results.

---


<!-- answer block 14 -->
### Answer

```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

**Trace:**

```
  1
 / \
2   3
   /
  4
→ 3
```

**Edges:** None → 0; single → 1.  
**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 15 -->
### Answer

**Approach:** Postorder height helper; at each node `best = max(best, left_h + right_h)`.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        L, R = height(node.left), height(node.right)
        best = max(best, L + R)
        return 1 + max(L, R)
    height(root)
    return best
```

**Key insight:** Diameter need not pass through the root — must consider every node as bend point.

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 16 -->
### Answer

```python
def hasPathSum(root, targetSum):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == targetSum
    remain = targetSum - root.val
    return hasPathSum(root.left, remain) or hasPathSum(root.right, remain)
```

**Trap:** Empty tree → False (even if targetSum == 0), unless problem says otherwise.

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 17 -->
### Answer

```python
def pathSum(root, targetSum):
    result = []
    def dfs(node, remain, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remain == node.val:
            result.append(path[:])
        else:
            dfs(node.left, remain - node.val, path)
            dfs(node.right, remain - node.val, path)
        path.pop()
    dfs(root, targetSum, [])
    return result
```

**Must copy** `path[:]` and **backtrack** with `pop`.

---


<!-- answer block 18 -->
### Answer

```python
def isSymmetric(root):
    def mirrors(a, b):
        if not a and not b:
            return True
        if not a or not b:
            return False
        return (a.val == b.val
                and mirrors(a.left, b.right)
                and mirrors(a.right, b.left))
    return True if not root else mirrors(root.left, root.right)
```

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 19 -->
### Answer

```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

---


<!-- answer block 20 -->
### Answer

```python
def flatten(root):
    prev = None
    def dfs(node):
        nonlocal prev
        if not node:
            return
        dfs(node.right)
        dfs(node.left)
        node.right = prev
        node.left = None
        prev = node
    dfs(root)
```

**Order:** reverse postorder (right, left, visit) rebuilds the preorder chain from the tail.

---


<!-- answer block 21 -->
### Answer

```python
class Codec:
    def serialize(self, root):
        vals = []
        def dfs(node):
            if not node:
                vals.append('#')
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(vals)

    def deserialize(self, data):
        tokens = iter(data.split(','))
        def dfs():
            val = next(tokens)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()
```

**Why `#`:** Structure is not recoverable from values alone.

**Trace:** Tree `1,left 2,right 3` → `1,2,#,#,3,#,#`

---


<!-- answer block 22 -->
### Answer

```python
def lowestCommonAncestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

**Trace logic:** Both sides non-null → current is split point → LCA. One side only → propagate. Current is p or q → return current (covers ancestor cases).

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 23 -->
### Answer

```python
def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    pre_i = 0
    def build(lo, hi):
        nonlocal pre_i
        if lo > hi:
            return None
        root_val = preorder[pre_i]
        pre_i += 1
        mid = idx[root_val]
        root = TreeNode(root_val)
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(inorder) - 1)
```

**Facts:** Preorder gives root first; inorder splits left/right sizes. Hash map → O(n) total.

**Why not preorder + postorder alone?** Ambiguous for general binary trees (single-child left vs right).

---


<!-- answer block 24 -->
### Answer

```python
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return valid(node.left, low, node.val) and \
               valid(node.right, node.val, high)
    return valid(root, float('-inf'), float('inf'))
```

**Common miss:** local-only parent/child checks.

---


<!-- answer block 25 -->
### Answer

```python
def searchBST(root, val):
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root

def insertIntoBST(root, val):
    node = TreeNode(val)
    if not root:
        return node
    curr = root
    while True:
        if val < curr.val:
            if not curr.left:
                curr.left = node
                return root
            curr = curr.left
        else:
            if not curr.right:
                curr.right = node
                return root
            curr = curr.right
```

---


<!-- answer block 26 -->
### Answer

```python
def deleteNode(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = deleteNode(root.right, succ.val)
    return root
```

**Cases:** 0 children → null; 1 child → bypass; 2 children → inorder successor replace + delete successor.

---


<!-- answer block 27 -->
### Answer

```python
def kthSmallest(root, k):
    stack = []
    curr = root
    while True:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
```

**Follow-up speech:** Augment with subtree sizes for O(h) repeated queries.

---


<!-- answer block 28 -->
### Answer

```python
def rangeSumBST(root, low, high):
    if not root:
        return 0
    if root.val < low:
        return rangeSumBST(root.right, low, high)
    if root.val > high:
        return rangeSumBST(root.left, low, high)
    return (root.val
            + rangeSumBST(root.left, low, high)
            + rangeSumBST(root.right, low, high))
```

**Pruning:** Outside range ⇒ skip the impossible side.

---


<!-- answer block 29 -->
### Answer

```python
def lowestCommonAncestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

**Contrast:** BT LCA is O(n) postorder; BST LCA is O(h) single walk.

---


<!-- answer block 30 -->
### Answer

```python
def sortedArrayToBST(nums):
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        root = TreeNode(nums[mid])
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(nums) - 1)
```

**Why mid:** Keeps height O(log n).

---


<!-- answer block 31 -->
### Answer

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)
```

---


<!-- answer block 32 -->
### Answer

They keep BST height **O(log n)** under inserts/deletes via rotations (and recoloring for RBT).

- AVL: height ≲ 1.44 log₂ n  
- Red-Black: height ≤ 2 log₂(n+1)

**Standard coding round:** explain why balancing matters; use plain BST or language TreeMap. Full AVL/RBT implement is rare unless explicitly requested.

---


<!-- answer block 33 -->
### Answer

```python
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best
```

**Ideas:** `gain` = best downward contribution to parent; `max(..., 0)` drops negative children; `best` allows bend at node.

**Complexity:** O(n) time, O(h) space.

---


<!-- answer block 34 -->
### Answer

```python
from collections import deque

def rightSideView(root):
    if not root:
        return []
    q = deque([root])
    view = []
    while q:
        n = len(q)
        for i in range(n):
            node = q.popleft()
            if i == n - 1:
                view.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return view
```

---


<!-- answer block 35 -->
### Answer

```python
from collections import deque

def zigzagLevelOrder(root):
    if not root:
        return []
    q = deque([root])
    result = []
    ltr = True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        if not ltr:
            level.reverse()
        result.append(level)
        ltr = not ltr
    return result
```

---


<!-- answer block 36 -->
### Answer

```python
from collections import deque

def widthOfBinaryTree(root):
    if not root:
        return 0
    q = deque([(root, 0)])
    best = 0
    while q:
        _, first = q[0]
        _, last = q[-1]
        best = max(best, last - first + 1)
        for _ in range(len(q)):
            node, i = q.popleft()
            i -= first  # normalize to avoid overflow in deep trees
            if node.left:
                q.append((node.left, 2 * i))
            if node.right:
                q.append((node.right, 2 * i + 1))
    return best
```

---


<!-- answer block 37 -->
### Answer

```python
def bstFromPreorder(preorder):
    i = 0
    def build(upper):
        nonlocal i
        if i == len(preorder) or preorder[i] > upper:
            return None
        root = TreeNode(preorder[i])
        i += 1
        root.left = build(root.val)
        root.right = build(upper)
        return root
    return build(float('inf'))
```

**Complexity:** O(n) — each value consumed once.

---


<!-- answer block 38 -->
### Answer

```python
def inorderSuccessor(root, p):
    succ = None
    while root:
        if p.val < root.val:
            succ = root
            root = root.left
        else:
            root = root.right
    return succ
```

If `p.right` exists, successor is also `min(p.right)` — the walk-from-root method covers both.

---


<!-- answer block 39 -->
### Answer

```python
def trimBST(root, low, high):
    if not root:
        return None
    if root.val < low:
        return trimBST(root.right, low, high)
    if root.val > high:
        return trimBST(root.left, low, high)
    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)
    return root
```

---


<!-- answer block 40 -->
### Answer

```python
def rob(root):
    def dfs(node):
        if not node:
            return 0, 0  # rob, skip
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob_this = node.val + ls + rs
        skip_this = max(lr, ls) + max(rr, rs)
        return rob_this, skip_this
    return max(dfs(root))
```

**Note:** Tree DP pattern — preview of later DP modules; still fair game once trees are taught.

---


<!-- answer block 41 -->
### Answer

**Approach:** Inorder traversal should be sorted. Find the two positions where `prev.val > curr.val` (first violation: mark `prev` as `x`; second: mark `curr` as `y`). Swap `x.val` and `y.val`.

One swap of non-adjacent nodes → two breaks; adjacent swap → one break (then `y = curr` on that single break).

```python
def recoverTree(root):
    x = y = prev = None
    stack = []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        if prev and prev.val > curr.val:
            y = curr
            if not x:
                x = prev
            else:
                break
        prev = curr
        curr = curr.right
    x.val, y.val = y.val, x.val
```

---


<!-- answer block 42 -->
### Answer

**(a) Brute:**

```python
def pathSum(root, targetSum):
    def count_from(node, remain):
        if not node:
            return 0
        here = 1 if node.val == remain else 0
        return here + count_from(node.left, remain - node.val) \
                    + count_from(node.right, remain - node.val)
    if not root:
        return 0
    return (count_from(root, targetSum)
            + pathSum(root.left, targetSum)
            + pathSum(root.right, targetSum))
```

**(b) Prefix hash:**

```python
from collections import defaultdict

def pathSum(root, targetSum):
    count = 0
    freq = defaultdict(int)
    freq[0] = 1
    def dfs(node, prefix):
        nonlocal count
        if not node:
            return
        prefix += node.val
        count += freq[prefix - targetSum]
        freq[prefix] += 1
        dfs(node.left, prefix)
        dfs(node.right, prefix)
        freq[prefix] -= 1  # backtrack
    dfs(root, 0)
    return count
```

Same idea as subarray sum equals k, on root→node prefixes.

---


<!-- answer block 43 -->
### Answer

Both shapes: **Time Θ(n)** (each node once).  
Space: (a) O(log n) stack (b) O(n) stack.

---


<!-- answer block 44 -->
### Answer

**Best BST-specific:** two iterators (forward inorder + reverse inorder) like two-sum on sorted array — O(n) time, O(h) space.

**Also valid:** hash set DFS — O(n) time/space; works even if not BST.

```python
def findTarget(root, k):
    seen = set()
    def dfs(node):
        if not node:
            return False
        if k - node.val in seen:
            return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)
    return dfs(root)
```

---


<!-- answer block 45 -->
### Answer

Fibonacci branches on **overlapping** subproblems with **recomputed** DAGs of calls → Θ(φⁿ) calls.  
`maxDepth` branches on **disjoint** subtrees; each node appears in exactly one call → Θ(n).

Overlapping vs partitioning the input is the difference.

---


<!-- answer block 46 -->
### Answer

```python
from collections import defaultdict, deque

def vertical_lists(root):
    if not root:
        return []
    cols = defaultdict(list)
    q = deque([(root, 0)])
    min_hd = max_hd = 0
    while q:
        node, hd = q.popleft()
        cols[hd].append(node.val)
        min_hd = min(min_hd, hd)
        max_hd = max(max_hd, hd)
        if node.left:
            q.append((node.left, hd - 1))
        if node.right:
            q.append((node.right, hd + 1))
    return [cols[h] for h in range(min_hd, max_hd + 1)]
```

BFS keeps top-to-bottom order within a column.

---


<!-- answer block 47 -->
### Answer

Build O(n); kth O(h+k) = O(log n + k). Total **O(n)**.  
(If only kth needed from sorted array: just `nums[k-1]` in O(1) — building a tree is pointless. Interview awareness check.)

---


<!-- answer block 48 -->
### Answer

**No.** Classic answer: hash map + array (swap-with-last delete). BST gives ordered ops, not O(1) getRandom without augmentation tricks. Hash wins for equality + random index.

---


<!-- answer block 49 -->
### Answer

Both count ranges with target sum using **prefix sums + hash frequency** of prefixes seen; Path Sum III applies it on root-to-node paths with backtracking to remove prefixes when leaving a subtree.

---


<!-- answer block 50 -->
### Answer

```python
def isBalanced(root):
    def helper(node):
        if not node:
            return 0, True
        lh, lb = helper(node.left)
        rh, rb = helper(node.right)
        return 1 + max(lh, rh), lb and rb and abs(lh - rh) <= 1
    return helper(root)[1]
```

---


<!-- answer block 51 -->
### Answer (build then walk — clear)

Use `buildTree` from C10, then:

```python
def postorder(node, out):
    if not node:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)
```

Direct index-arithmetic construction of postorder also exists; building is acceptable.

---


<!-- answer block 52 -->
### Answer

```python
def closestValue(root, target):
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        root = root.left if target < root.val else root.right
    return closest
```

(Add tie-break if required by statement.)

---


<!-- answer block 53 -->
### Answer

**Trim BST** to `[L, R]` (same as D/E trim).  

Yes, order matters for correctness of rewiring: by trimming children first (postorder-style), when you bypass `node` you return an already-trimmed subtree. (Equivalent formulations trim before recursing on the kept side only — also fine.)

---


<!-- answer block 54 -->
### Answer

**True** (⇒ and ⇐) under unique values and the standard strict BST invariant.

- If BST ⇒ inorder sorted (standard theorem).  
- If inorder strictly increasing ⇒ for every node, left subtree values appear before it and right after; combined with binary tree structure this implies the BST property (can be shown by induction on size / using the bounds view).

---


<!-- answer block 55 -->
### Answer

**Valid:** (1) Preorder + null markers (2) Level-order + null markers  

**Invalid:** Inorder alone; or preorder of values without nulls / structure markers — not unique.

---


<!-- answer block 56 -->
### Answer

```python
def deleteMin(root):
    if not root:
        return None
    if not root.left:
        return root.right  # min node; may have right child
    root.left = deleteMin(root.left)
    return root
```

---


<!-- answer block 57 -->
### Answer

Inserts cost 1 + 2 + … + n = **Θ(n²)** time. Final tree is a chain of height n.

Fix: build from mid recursively O(n), or shuffle, or use self-balancing tree.

---


<!-- answer block 58 -->
### Answer

```
    3
   / \
  9  20
    /  \
   15   7
```

Postorder: **9, 15, 7, 20, 3**

---


<!-- answer block 59 -->
### Answer (rubric)

Must hit: hash cannot range efficiently; unbalanced BST degrades with sorted inserts; RBT/AVL (or TreeMap) give O(log n) update and O(log n + k) range; mention rotations/rebalancing at high level; Python lacks stdlib BST so note language reality. Deduct if claiming hash does ranges in O(k) without scanning all keys.

---


<!-- answer block 60 -->
### Answer

**Bug:** local-only checks. **Fix:** bounds method or inorder increasing.

---


<!-- answer block 61 -->
### Answer

**Bug:** only measures path through root; diameter may lie entirely in one subtree. **Fix:** global best updated at every node with `left_h + right_h`, helper returns height.

---


<!-- answer block 62 -->
### Answer

**Bug:** `result.append(path)` aliases the mutable list — all entries end empty or identical. **Fix:** `result.append(path[:])`.

---


<!-- answer block 63 -->
### Answer

**Bug:** does not require **both** on the same side before descending; also ignores cases where one is on left and one on right incorrectly mixed with single comparisons. **Fix:**

```python
if p.val < root.val and q.val < root.val: go left
elif p.val > root.val and q.val > root.val: go right
else: return root
```

---


<!-- answer block 64 -->
### Answer

**Bug:** no null base case → AttributeError. **Fix:** `if not root: return 0`.

---


