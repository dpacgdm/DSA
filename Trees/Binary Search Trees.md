# BINARY SEARCH TREES — THE COMPLETE LESSON

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHAT A BST ACTUALLY IS

## The Core Idea

A **Binary Search Tree (BST)** is a binary tree with an **ordering invariant** on values:

```
For every node u:
  every value in u.left  subtree  <  u.val
  every value in u.right subtree  >  u.val
```

(Some definitions allow `≤` on one side for duplicates. Interview problems usually use **strict** `<` / `>` and unique values unless stated otherwise. **State your duplicate policy** if asked.)

That single invariant is why BSTs exist: it turns "search in a tree" into the same binary-decision process as binary search on a sorted array — but with structural flexibility for inserts and deletes.

---

## 1A: Why the Invariant Matters

```
Valid BST:                NOT a BST:
      4                         4
     / \                       / \
    2   6                     2   6
   / \ / \                   / \ /
  1  3 5  7                 1  5 3
                              ↑
                    5 is in LEFT of 4 but 5 > 4  → broken
                    (also 3 is in RIGHT of 2? wait — 3 under 6's left with 3<6
                     but 3 is not > 4 — still broken relative to ancestors)
```

**Critical subtlety:** It is not enough that `left.val < node.val < right.val` for immediate children. The invariant applies to **entire subtrees**. A common wrong validator only checks local parent-child and accepts invalid trees.

```
Invalid, but local checks pass:
      5
     / \
    1   6
       / \
      4   7
```

`6 > 5` and `4 < 6` look fine locally, but `4` is in the **right** subtree of `5` while `4 < 5` — **invalid BST**.

This is why validate-BST uses **bounds**, not only local comparisons.

---

## 1B: Inorder of a BST

**Theorem:** Inorder traversal of a BST visits values in **sorted non-decreasing order**.

```
      4
     / \
    2   6
   / \ / \
  1  3 5  7

Inorder: 1, 2, 3, 4, 5, 6, 7
```

Consequences used constantly:
- Kth smallest = kth node in inorder
- Validate BST = check inorder is strictly increasing
- Convert sorted array → balanced BST = recursive mid-as-root (inorder identity)

---

## 1C: Shape Depends on Insertion Order

Same values, different trees:

```
Insert 1,2,3,4,5:           Insert 3,1,4,2,5:
    1                           3
     \                         / \
      2                       1   4
       \                       \   \
        3                       2   5
         \
          4
           \
            5
```

Left tree is a **linked list** — search is O(n). Right tree is bushier — search is O(log n).

**BST time complexities are in terms of height h, not n.** Balanced ⇒ h = Θ(log n). Skewed ⇒ h = Θ(n).

Balancing (AVL / Red-Black) exists to keep h = O(log n) under updates. Covered in Part 8 as intuition.

---

# PART 2: SEARCH, INSERT, DELETE

## 2A: Search

### Framework

From root: if target equals node, found. If target < node, go left. Else go right. Hit null → not found.

```python
def searchBST(root, val):
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root  # node or None
```

Recursive:

```python
def searchBST(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return searchBST(root.left, val)
    return searchBST(root.right, val)
```

### Trace

```
Tree: 4 / 2 6 / 1 3 5 7    search 5
4 → 5>4 → right 6 → 5<6 → left 5 → found
```

### Complexity

Time O(h), Space O(1) iterative / O(h) recursive.

---

## 2B: Insert

### Framework

Search until you fall off the tree; attach new node there. Usually insert as a **leaf**.

```python
def insertIntoBST(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insertIntoBST(root.left, val)
    else:
        root.right = insertIntoBST(root.right, val)
    return root
```

Iterative:

```python
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

### Duplicate policy

If `val == curr.val`, problem statements vary: ignore, count frequency in node, or always go right. Default interview: values unique.

### Complexity

O(h) time.

---

## 2C: Delete — The Three Cases

Deleting is the operation people under-prepare. Memorize the cases.

### Case 1: Node is a leaf
Remove it (parent link → None).

### Case 2: Node has one child
Bypass node: parent points to that child.

### Case 3: Node has two children
Replace node's value with **inorder successor** (minimum of right subtree) or **inorder predecessor** (maximum of left subtree), then delete that successor/predecessor from the subtree (it has at most one child).

```
Delete 4 from:
      4
     / \
    2   6
   / \ / \
  1  3 5  7

Inorder successor of 4 = min(right)=5
Replace 4 with 5, delete original 5:
      5
     / \
    2   6
   / \   \
  1   3   7
```

### Implementation

```python
def deleteNode(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        # Found node to delete
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # Two children: successor
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = deleteNode(root.right, succ.val)
    return root
```

### Helper: min / max in BST

```python
def find_min(node):
    while node.left:
        node = node.left
    return node

def find_max(node):
    while node.right:
        node = node.right
    return node
```

### Complexity

O(h) time.

---

## 2D: Operation Complexity Summary

| Operation | Average (balanced) | Worst (skewed) |
|---|---|---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Inorder walk | O(n) | O(n) |
| Min / Max | O(log n) | O(n) |

---

# PART 3: VALIDATE BST

## 3A: Wrong Approach (Local Only)

```python
# ❌ REJECT THIS
def isValidBST_wrong(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return isValidBST_wrong(root.left) and isValidBST_wrong(root.right)
```

Fails on the `5 → 1,6 → 4,7` counterexample.

---

## 3B: Correct Approach — Bounds Method

### Framework

Each node must lie in an open interval `(low, high)` inherited from ancestors:
- Going left: `high` becomes `node.val`
- Going right: `low` becomes `node.val`

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

### Trace — invalid tree

```
      5
     / \
    1   6
       / \
      4   7

valid(5, -∞, ∞) OK
  valid(1, -∞, 5) OK
  valid(6, 5, ∞) OK
    valid(4, 5, 6) → 4 < 5? FAIL
```

### Trace — valid tree

```
      5
     / \
    1   7
       / \
      6   8

valid(6, 5, 7) → 5 < 6 < 7 OK
```

---

## 3C: Alternative — Inorder Strictly Increasing

```python
def isValidBST(root):
    prev = float('-inf')
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        if curr.val <= prev:
            return False
        prev = curr.val
        curr = curr.right
    return True
```

Same O(n) time. Bounds method generalizes better to "validate with custom comparator" explanations.

---

## 3D: Edge Cases

| Case | Result |
|---|---|
| Empty | True |
| Single node | True |
| Duplicates (`<=` fails strict) | False under strict invariant |
| INT_MIN / INT_MAX values | Use None sentinels instead of ±inf if language overflows; Python fine with ±inf |

```python
# Sentinel-null variant (safe in all languages)
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        return valid(node.left, low, node.val) and \
               valid(node.right, node.val, high)
    return valid(root, None, None)
```

> **Time: O(n), Space: O(h)**

---

# PART 4: KTH SMALLEST

## Pattern Identification

Inorder yields sorted order; stop at kth visit.

## Solution — Iterative Inorder (optimal for early exit)

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

## Recursive with counter

```python
def kthSmallest(root, k):
    ans = None
    def inorder(node):
        nonlocal k, ans
        if not node or ans is not None:
            return
        inorder(node.left)
        k -= 1
        if k == 0:
            ans = node.val
            return
        inorder(node.right)
    inorder(root)
    return ans
```

## Follow-up (interview): frequent kth queries

Augment each node with `subtree_size`. Then walk like order-statistic tree: if `left.size + 1 == k` return node; if `k <= left.size` go left; else go right with `k - left.size - 1`. Updates on insert/delete maintain sizes — O(h) per query.

## Trace

```
      5
     / \
    3   6
   / \
  2   4
 /
1
k=3 → inorder 1,2,3 → answer 3
```

> **Time: O(h + k), Space: O(h)**

---

# PART 5: RANGE SUM OF BST

## Pattern Identification

Prune branches that cannot intersect `[low, high]`.

```python
def rangeSumBST(root, low, high):
    if not root:
        return 0
    if root.val < low:
        return rangeSumBST(root.right, low, high)
    if root.val > high:
        return rangeSumBST(root.left, low, high)
    # root in range
    return (root.val
            + rangeSumBST(root.left, low, high)
            + rangeSumBST(root.right, low, high))
```

### Why pruning works

If `root.val < low`, entire left subtree is even smaller — skip it. Symmetric for high.

### Complexity

O(n) worst case (all nodes in range / skewed). Better when many branches prune. Space O(h).

---

# PART 6: LCA IN A BST

## Pattern Identification

Use value ordering — walk down until you find the split point.

```
While root:
  if p and q both < root → go left
  if p and q both > root → go right
  else → root is LCA (split or one equals root)
```

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

Recursive equivalent:

```python
def lowestCommonAncestor(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor(root.right, p, q)
    return root
```

### Trace

```
      6
     / \
    2   8
   / \ / \
  0  4 7  9
    / \
   3   5

LCA(2,8)=6  (split at root)
LCA(2,4)=2  (2 is ancestor)
LCA(3,5)=4
```

### vs Binary Tree LCA

| | BT LCA | BST LCA |
|---|---|---|
| Uses values? | No | Yes |
| Time | O(n) | O(h) |
| Must visit both subtrees? | Often | No — single walk down |

> **Time: O(h), Space: O(1) iterative**

---

# PART 7: CONVERTED ARRAY → BALANCED BST

## Pattern Identification

Sorted array **is** the inorder of the BST you want. Pick mid as root → balanced height; recurse on left/right halves.

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

### Trace

```
nums = [-10, -3, 0, 5, 9]
mid=0 → root
  left [-10,-3] → -3 as root with left -10
  right [5,9] → 5 or 9 depending on mid convention
Height-balanced by construction.
```

### Why mid?

Guarantees left and right subtrees differ in size by at most 1 → height O(log n).

### Related: sorted list → BST (LC 109)

Same idea, but list has no random access — either convert to array, or use inorder construction with slow/fast mid finding (more subtle). Prefer array conversion in interviews unless constrained.

> **Time: O(n), Space: O(log n) stack**

---

# PART 8: BALANCING — AVL & RED-BLACK INTUITION

You are **not** implementing full AVL/RBT unless a rare interview asks. You **are** expected to know why balancing exists and what guarantees you get.

## 8A: The Problem

Naive BST + sorted inserts → linked list → O(n) ops. Databases and language libraries need **O(log n)** guarantees.

## 8B: AVL Trees (Height-Balanced)

**Invariant:** For every node, `|height(left) - height(right)| ≤ 1`.

On insert/delete, if a node becomes unbalanced, apply **rotations**:

```
Right rotation (fix left-left heavy):

      y                x
     / \              / \
    x   C    →       A   y
   / \                  / \
  A   B                B   C
```

```
Left rotation (fix right-right heavy): mirror of above
```

Left-right / right-left heaviness: double rotation (rotate child first, then node).

**Guarantee:** height ≤ ~1.44 log₂(n). Lookups slightly faster than RBT; inserts/deletes may rotate more.

## 8C: Red-Black Trees

**Idea:** Color nodes red/black with rules that imply height ≤ 2 log₂(n+1).

Rough rules (recognition only):
1. Each node red or black
2. Root black
3. No two reds in a row (red node's children black)
4. Every path from node to null has the same number of black nodes

**Guarantee:** O(log n) ops. Fewer rotations on update than AVL on average → common choice for libraries (`std::map`, Java `TreeMap`, Linux CFS historically, etc.).

## 8D: What Python Gives You

| Structure | Ordered? | Complexity |
|---|---|---|
| `dict` / `set` | No (hash) | Amortized O(1) |
| `sortedcontainers.SortedList` (3rd party) | Yes | O(log n) |
| Manual BST | Yes | O(h) — you balance yourself |
| `heapq` | Partial (heap order) | Not a BST |

Python's standard library does **not** expose a BST. In interviews, implement tree nodes explicitly or use sorted list / bisect on arrays when mutation is rare.

## 8E: Interview Speech

> "A plain BST is O(log n) only if balanced. Sorted inserts degrade to O(n). Self-balancing trees (AVL/Red-Black) restore O(log n) via rotations. In production I'd use the language's TreeMap equivalent; in an interview I'll implement a plain BST unless asked to balance."

---

# PART 9: BST ITERATOR

## Pattern Identification

Controlled inorder — stack holds the path to the next smallest. Lazy: don't flatten entire tree unless required.

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

### Complexity

- `hasNext`: O(1)
- `next`: **Amortized O(1)** — each node pushed/popped once across n calls
- Space: O(h)

### Trace

```
      7
     / \
    3  15
      /  \
     9   20

Init: push_left 7→3 → stack [7,3]
next → 3; 3 has no right → stack [7]
next → 7; push_left 15→9 → stack [15,9]
next → 9 → stack [15]
next → 15; push_left 20 → stack [20]
next → 20
```

### Why not store full inorder array?

Array is O(n) space upfront. Iterator is O(h) and supports early stop — better for "merge two BSTs" style problems.

---

# PART 10: WHEN BST BEATS HASH — AND WHEN IT DOESN'T

## Decision Table

| Need | Prefer | Why |
|---|---|---|
| Exact lookup / insert / delete only | **Hash set/map** | Average O(1) vs O(log n) |
| Ordered iteration (sorted keys) | **BST / TreeMap** | Hash has no order |
| Range queries `[L, R]` | **BST** | Prune by order; hash must scan all |
| Kth smallest / order statistics | **BST** (augmented) | Hash cannot rank efficiently |
| Closest element / successor / predecessor | **BST** | Floor/ceil via walk |
| Min / max repeatedly with inserts | **BST** or **Heap** | Heap if only min/max; BST if full order |
| Memory-tight + adversarial keys | Balanced BST | Hash worst-case / attack concerns (rare in interviews) |
| Simplicity in Python interview | **Hash**, or **sorted list + bisect** | No built-in BST |

## The One-Sentence Rule

> **Hash** optimizes equality. **BST** optimizes order.

If the problem never needs order, ranges, or rank — hash wins. If it needs "next larger", "all between", "median", "kth" — think BST (or sorted array / policy-based data if static).

## Hybrid Patterns

- **Hash + BST:** e.g., values in a TreeMap for order, hash for O(1) existence of a secondary key.
- **Sorted array:** static data, many range/kth queries, few updates — binary search may beat building a tree.
- **Heap:** only care about extreme, not full sorted order.

---

# PART 11: MORE CLASSIC BST PROBLEMS

## 11A: Convert BST to Greater Tree (LC 538 / 1038)

Reverse inorder (right → node → left), accumulate running sum.

```python
def convertBST(root):
    acc = 0
    def dfs(node):
        nonlocal acc
        if not node:
            return
        dfs(node.right)
        acc += node.val
        node.val = acc
        dfs(node.left)
    dfs(root)
    return root
```

## 11B: Recover BST — Two Nodes Swapped (LC 99)

Inorder should increase. Find two violations; swap their values. O(n) time, O(h) space (or Morris O(1)).

## 11C: Trim BST to Range (LC 669)

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

## 11D: Mode in BST (LC 501)

Inorder; track current streak vs best (duplicates allowed in this problem's BST definition).

## 11E: Two Sum IV — Input is BST (LC 653)

Hash set during DFS (any binary tree method works), **or** BST iterator from left + reverse iterator from right (two pointers on sorted order).

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

# PART 12: BST vs BINARY TREE — PROBLEM ROUTING

```
╔════════════════════════════════════════════════════════════════╗
║  Is the tree promised to be a BST?                             ║
║                                                                ║
║  NO  → use Binary Trees.md frameworks (LCA postorder, etc.)    ║
║  YES → can you exploit ordering?                               ║
║         • search / insert / delete / LCA walk                  ║
║         • bounds validation                                    ║
║         • inorder = sorted                                     ║
║         • prune ranges                                         ║
║                                                                ║
║  Trap: problem shows a tree that LOOKS sorted locally but      ║
║  does not say BST — do not assume.                             ║
╚════════════════════════════════════════════════════════════════╝
```

---

# PART 13: MASTER CHEAT SHEETS

## 13A: Invariant

```
∀ node u:
  ∀ x in left(u):  x < u.val
  ∀ y in right(u): y > u.val
```

## 13B: Operations

| Op | Action |
|---|---|
| Search | Compare, branch left/right |
| Insert | Search to null, attach leaf |
| Delete | 0 kids: remove; 1 kid: bypass; 2 kids: successor swap + delete |
| Min | Hard left |
| Max | Hard right |
| Successor | Min of right, else walk ancestors (needs parent / stack) |

## 13C: Validate

```
valid(node, low, high):
  node is None → True
  not (low < node.val < high) → False
  valid(left, low, node.val) and valid(right, node.val, high)
```

## 13D: High-Frequency Map

| Problem | Trick |
|---|---|
| Validate BST | Bounds (not local) |
| Kth smallest | Inorder count |
| Range sum | Prune outside [L,R] |
| LCA BST | Walk until split |
| Sorted array → BST | Mid root recurse |
| BST iterator | Stack left spine |
| Greater tree | Reverse inorder accum |
| Trim range | Redirect root to valid side |

## 13E: BST vs Hash

```
Equality only          → Hash
Order / range / rank   → BST
Static + binary search → Sorted array
Extremes only          → Heap
```

## 13F: Balancing One-Liners

| Structure | Height bound | Use |
|---|---|---|
| AVL | ~1.44 log n | Lookup-heavy |
| Red-Black | ≤ 2 log(n+1) | General libraries |
| Treap / Splay | Expected / amortized log n | Specialized |

---

# PART 14: FULL WORKED TRACES

## Trace A — Insert sequence

```
Insert 5, 3, 7, 2, 4, 6, 8

5
 → 3 left of 5
 → 7 right of 5
 → 2 left of 3
 → 4 right of 3
 → 6 left of 7
 → 8 right of 7

Final:
      5
     / \
    3   7
   / \ / \
  2  4 6  8
```

## Trace B — Delete 3 (two children)

```
Successor of 3 = 4
Replace 3 with 4; delete leaf 4 from right of old 3:
      5
     / \
    4   7
   /   / \
  2   6   8
```

## Trace C — Validate bounds on valid tree

```
valid(5,-∞,∞)
  valid(3,-∞,5)
    valid(2,-∞,3) OK
    valid(4,3,5) OK
  valid(7,5,∞)
    valid(6,5,7) OK
    valid(8,7,∞) OK
→ True
```

## Trace D — Range sum [4, 7]

```
Visit 5 (in) + left pruned partially + right
4 in, 6 in, 7 in, 8 pruned, 2 pruned, 3 pruned?
3 < 4 → skip 3's left; 3 not in range; still need check 3.right=4
Sum = 5+4+6+7 = 22
```

---

# PART 15: TEST PROBLEMS (WITH FULL SOLUTIONS)

# Problem 1: Search in a BST (warmup)

## Solution

```python
def searchBST(root, val):
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root
```

## Complexity

O(h) time, O(1) space.

---

# Problem 2: Insert into a BST

## Solution

See Part 2B. Return the (possibly new) root.

## Edge Cases

Empty tree → new node is root. `val` already exists → define policy.

---

# Problem 3: Inorder Successor in BST

Given a node (or value), find next larger value in BST.

## Solution (no parent pointers; search from root)

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

## Trace

```
Tree 2,1,3 — successor of 1 is 2; of 2 is 3; of 3 is None
```

If `p` has right child: successor = min(p.right). The walk-from-root method handles both.

> **Time: O(h)**

---

# Problem 4: Unique BSTs Count (LC 96) — Catalan DP Preview

Number of structurally unique BSTs with values 1..n.

```python
def numTrees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            dp[nodes] += dp[root - 1] * dp[nodes - root]
    return dp[n]
```

Catalan numbers. Full DP treatment in later modules; recognize the recurrence here.

---

# Problem 5: Construct BST from Preorder (LC 1008)

## Pattern Identification

Preorder: first is root. Bound method: consume preorder with upper bounds (efficient O(n)).

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

## Trace

```
preorder [8,5,1,7,10,12]
build 8; left upper 8 → 5; left upper 5 → 1; ... right of 5 → 7; right of 8 → 10 → 12
```

> **Time: O(n), Space: O(h)**

---

# Problem 6: Balance a BST (LC 1382)

## Pattern Identification

Extract inorder (sorted values) → `sortedArrayToBST`.

```python
def balanceBST(root):
    vals = []
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        vals.append(node.val)
        inorder(node.right)
    inorder(root)

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(vals[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(vals) - 1)
```

---

# Problem 7: Closest Binary Search Tree Value (LC 270)

## Pattern Identification

Walk like search; track closest. At each node, decide left/right by comparison with target — but always update best.

```python
def closestValue(root, target):
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target) or (
            abs(root.val - target) == abs(closest - target) and root.val < closest
        ):
            closest = root.val
        root = root.left if target < root.val else root.right
    return closest
```

(Tie-break policy depends on problem statement.)

> **Time: O(h)**

---

# PART 16: WHAT THIS MODULE DOES NOT COVER

| Topic | Where |
|---|---|
| General binary tree traversals / diameter / serialize | `Trees/Binary Trees.md` |
| Full AVL/RBT implementation | Optional deep dive — not required for Phase A gates |
| B-trees / B+ trees | System design / databases later |
| Treaps, splay trees | CP / advanced — deferred |
| Segment trees / Fenwick | Module 10 exposure |
| Heaps | Module 6 |

---

# PART 17: STATUS NOTES (PROGRAM GOVERNANCE)

- Teach artifact for Module 5 — BSTs (+ balancing concepts).
- Balancing is **intuition + interview speech**, not full implement, unless a future scope addendum expands it.
- `complete` still requires retention + timed verification per `Handoff Doc.md`.

---

# END OF BINARY SEARCH TREES LESSON
