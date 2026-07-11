# BINARY TREES — THE COMPLETE LESSON

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHAT A BINARY TREE ACTUALLY IS

## Why You Need This

Arrays give you contiguous slots. Hash maps give you key → value. Linked lists give you a chain. A **binary tree** gives you a hierarchy: every node can branch into at most two children.

If you only memorize "left and right pointers," you will fail interviews the moment the problem asks for diameter, LCA, serialize, or construct-from-traversals. Those problems are not about pointers — they are about **what information flows up from subtrees** and **what information flows down from ancestors**.

This lesson builds that mental model first, then the frameworks, then the classics.

---

## 1A: The Node

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Three fields. That is the entire structure:

| Field | Meaning |
|---|---|
| `val` | The payload (int, string, whatever the problem stores) |
| `left` | Reference to left child, or `None` |
| `right` | Reference to right child, or `None` |

A tree is just a root `TreeNode` whose children point to more `TreeNode`s. There is no separate "Tree" class required for interviews — the root *is* the tree.

---

## 1B: Tree Vocabulary — Precise Definitions

These words get abused. Interviewers expect the precise meanings below.

### Root
The unique top node. No parent. Every path into the tree starts here. If the tree is empty, root is `None`.

### Leaf
A node with **no children** (`left is None` and `right is None`). Leaves are where recursion bottoms out for many problems.

### Parent / Child / Sibling
- Parent of `u`: the node that points to `u` as left or right.
- Child of `u`: `u.left` or `u.right` if non-null.
- Siblings: two nodes that share the same parent.

### Ancestor / Descendant
- Ancestor of `u`: any node on the path from root to `u` (excluding `u` itself, usually).
- Descendant of `u`: any node in `u`'s subtree (excluding `u` itself, usually).
- Subtree rooted at `u`: `u` plus all its descendants.

### Depth of a node
Number of **edges** on the path from the **root** to that node.

```
        1          ← depth 0
       / \
      2   3        ← depth 1
     / \
    4   5          ← depth 2
```

- `depth(1) = 0`
- `depth(2) = 1`
- `depth(4) = 2`

Some texts count nodes instead of edges (root depth = 1). In interviews, **state your convention**. This lesson uses **edges from root** (root depth = 0).

### Height of a node
Number of **edges** on the longest path from that node **down to a leaf**.

```
        1
       / \
      2   3
     / \
    4   5
```

- `height(4) = 0` (leaf)
- `height(5) = 0`
- `height(2) = 1`
- `height(3) = 0`
- `height(1) = 2`

### Height of a tree
Height of the root. Empty tree height is conventionally `-1` (so a single-node tree has height `0`). Many LeetCode problems ask for **depth as number of nodes** (single node → 1). Always read the problem statement.

| Convention | Empty | Single node | Tree above |
|---|---|---|---|
| Height (edges) | -1 | 0 | 2 |
| Max depth (nodes, LC 104) | 0 | 1 | 3 |

### Level
All nodes at the same depth. Level 0 = root. Level-order traversal visits level by level.

### Diameter
The **number of edges** (or sometimes nodes — check the problem) on the **longest path between any two nodes** in the tree. The path does **not** have to pass through the root.

```
        1
       / \
      2   3
     / \
    4   5
```

Longest path: `4 → 2 → 5` (2 edges) or `4 → 2 → 1 → 3` (3 edges). Diameter = 3 edges.

### Binary tree vs binary search tree
A **binary tree** only constrains structure: ≤ 2 children. Values can be anything, in any order.

A **BST** adds an ordering invariant (covered in `Trees/Binary Search Trees.md`). Do not assume sorted order on a plain binary tree.

### Full / Complete / Perfect / Balanced (recognition only)

| Term | Meaning |
|---|---|
| **Full** | Every node has 0 or 2 children (no single-child nodes) |
| **Perfect** | All leaves at same depth; every internal node has 2 children |
| **Complete** | Filled level-by-level left-to-right (heap shape) |
| **Height-balanced** | For every node, \|height(left) − height(right)\| ≤ 1 |

You do not need to implement classifiers unless asked. You need to recognize when a problem *assumes* one of these (e.g., heap indexing assumes complete).

---

## 1C: Why Trees Exist — Real Use Cases

| Domain | Why a tree |
|---|---|
| File systems | Directories nest; path = root → … → file |
| DOM / UI | HTML elements nest; layout walks the tree |
| Compilers | AST — expression trees, statement trees |
| Databases | Indexes (B-trees are generalizations) |
| Decision systems | Decision trees, game trees |
| Interviews | Hierarchical data; recursive structure problems |

**The interview reason:** trees force you to prove you can think recursively with a clear base case, combine left/right results, and sometimes switch to BFS when "by level" matters.

---

# PART 2: REPRESENTATIONS

## 2A: Pointer / Object Form (Default for Interviews)

```python
# Build:
#       1
#      / \
#     2   3
#    /
#   4

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
```

Pros: natural recursion, matches LeetCode `TreeNode`.
Cons: no random access by index; parent pointer usually absent (unless you add one).

---

## 2B: Array / Heap-Index Form

For a **complete** binary tree stored in an array `a` (1-indexed for clarity):

```
Index:  1  2  3  4  5  6  7
Value: [1, 2, 3, 4, 5, 6, 7]

            1
           / \
          2   3
         / \ / \
        4  5 6  7
```

| Relation | Formula (1-indexed) |
|---|---|
| Left child of `i` | `2i` |
| Right child of `i` | `2i + 1` |
| Parent of `i` | `i // 2` |

0-indexed variant: left = `2i+1`, right = `2i+2`, parent = `(i-1)//2`.

**When this appears:** heaps (Module 6), segment trees (Module 10 exposure). For general binary trees with missing children, array form wastes space or needs explicit null markers — prefer pointers.

---

## 2C: Nested List / Level-Order Serialization

LeetCode input format is level-order with `null` placeholders:

```
[1, 2, 3, 4, null, null, 5]
```

```
        1
       / \
      2   3
     /     \
    4       5
```

Rules:
1. List nodes left-to-right, level by level.
2. Include `null` when a non-leaf position is missing a child **if** a later sibling on that level exists (standard LC serialization includes nulls needed to place later nodes).
3. Trailing nulls after the last real node are usually omitted.

You will implement serialize/deserialize properly in Part 8.

---

## 2D: Edge List / Parent Array (Rare in BT interviews)

Sometimes: `parent[i] = j` means node `j` is parent of `i`. Convert to `TreeNode` by building adjacency then assigning left/right (need a rule for which child is left). Mention only so you are not surprised.

---

# PART 3: TRAVERSALS — THE COMPLETE SET

Traversals are how you **visit every node in a defined order**. Almost every tree problem is a traversal with extra bookkeeping.

## 3A: The Three DFS Orders (Recursive)

For a node, the three classic orders differ only in **when you process the node relative to its children**:

```
PREORDER:  Node → Left → Right     (process BEFORE children)
INORDER:   Left → Node → Right     (process BETWEEN children)
POSTORDER: Left → Right → Node     (process AFTER children)
```

### Running example

```
        1
       / \
      2   3
     / \
    4   5
```

| Order | Sequence | Mnemonic |
|---|---|---|
| Preorder | 1, 2, 4, 5, 3 | Root first — copy structure top-down |
| Inorder | 4, 2, 5, 1, 3 | Left subtree, root, right — **sorted order on BST** |
| Postorder | 4, 5, 2, 3, 1 | Children first — safe for delete / compute-then-combine |

### Recursive implementations

```python
def preorder(node, out):
    if node is None:
        return
    out.append(node.val)          # NODE
    preorder(node.left, out)      # LEFT
    preorder(node.right, out)     # RIGHT

def inorder(node, out):
    if node is None:
        return
    inorder(node.left, out)       # LEFT
    out.append(node.val)          # NODE
    inorder(node.right, out)      # RIGHT

def postorder(node, out):
    if node is None:
        return
    postorder(node.left, out)     # LEFT
    postorder(node.right, out)    # RIGHT
    out.append(node.val)          # NODE
```

### Trace — preorder on the example

```
preorder(1)
  visit 1
  preorder(2)
    visit 2
    preorder(4)
      visit 4
      preorder(None) → return
      preorder(None) → return
    preorder(5)
      visit 5
      ...
  preorder(3)
    visit 3
    ...
→ [1, 2, 4, 5, 3]
```

### When to use which (decision table)

| Need | Prefer |
|---|---|
| Clone / serialize structure top-down | Preorder |
| BST sorted values | Inorder |
| Compute child results before parent (height, delete tree) | Postorder |
| "Visit every node, order doesn't matter" | Any DFS or BFS |
| Process by distance from root / by level | Level-order BFS |

---

## 3B: Iterative DFS — Explicit Stack

Interviews often ask: "Do it without recursion." You simulate the call stack with an explicit stack.

### Iterative preorder

```python
def preorder_iterative(root):
    if not root:
        return []
    stack = [root]
    out = []
    while stack:
        node = stack.pop()
        out.append(node.val)
        # Push RIGHT first so LEFT is processed first (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

**Why right before left:** stack is LIFO. You want left next → push it last.

### Iterative inorder

```python
def inorder_iterative(root):
    stack = []
    out = []
    curr = root
    while curr or stack:
        # Go as left as possible
        while curr:
            stack.append(curr)
            curr = curr.left
        # No more left — process node
        curr = stack.pop()
        out.append(curr.val)
        # Now go right
        curr = curr.right
    return out
```

**Mental model:** the stack holds the path of ancestors waiting for their turn after the left subtree finishes.

### Trace — inorder iterative

```
Tree:     1
         / \
        2   3
       / \
      4   5

curr=1, go left → stack=[1], curr=2
curr=2, go left → stack=[1,2], curr=4
curr=4, go left → stack=[1,2,4], curr=None
pop 4, visit 4, curr=4.right=None
pop 2, visit 2, curr=2.right=5
curr=5, go left → stack=[1,5], curr=None
pop 5, visit 5, curr=None
pop 1, visit 1, curr=1.right=3
curr=3, go left → stack=[3], curr=None
pop 3, visit 3, curr=None
→ [4, 2, 5, 1, 3]
```

### Iterative postorder (two-stack or one-stack)

**Two-stack method** (clearest):

```python
def postorder_iterative(root):
    if not root:
        return []
    s1, s2 = [root], []
    while s1:
        node = s1.pop()
        s2.append(node)
        if node.left:
            s1.append(node.left)
        if node.right:
            s1.append(node.right)
    return [n.val for n in reversed(s2)]
    # Equivalent: while s2: out.append(s2.pop().val)
```

Idea: modified preorder (Node → Right → Left), then reverse → Left → Right → Node.

**One-stack method** exists but is error-prone under time pressure. Prefer two-stack or recursion unless asked for O(1) extra structures beyond the stack.

---

## 3C: Level-Order Traversal (BFS)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    result = []
    while q:
        level_size = len(q)
        level = []
        for _ in range(level_size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result
```

### Trace

```
        1
       / \
      2   3
     / \
    4   5

q=[1]
level_size=1 → visit 1, enqueue 2,3 → result=[[1]]
q=[2,3]
level_size=2 → visit 2 (enqueue 4,5), visit 3 → result=[[1],[2,3]]
q=[4,5]
level_size=2 → visit 4, visit 5 → result=[[1],[2,3],[4,5]]
```

### Why `level_size = len(q)` matters

Without it, you get a flat list of all nodes in BFS order. With it, you know exactly which nodes belong to the current level — required for zigzag, level averages, right-side view, etc.

### Flat BFS (no levels)

```python
def bfs_flat(root):
    if not root:
        return []
    q = deque([root])
    out = []
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return out
```

---

## 3D: Traversal Complexity Cheat Sheet

| Traversal | Time | Extra space (worst) | Extra space (balanced) |
|---|---|---|---|
| Recursive DFS | O(n) | O(n) stack (skewed) | O(log n) |
| Iterative DFS | O(n) | O(n) explicit stack | O(log n) |
| BFS level-order | O(n) | O(n) queue (wide level) | O(w) width |

Every node visited once → **Θ(n) time** always. Space is about the **frontier** (stack depth or queue width).

---

# PART 4: THE RECURSIVE TREE FRAMEWORK

This is the single most important section in the lesson. Almost every classic problem is an instance of this template.

## 4A: The Template

```
def solve(node):
    # 1. NULL BASE CASE
    if node is None:
        return <identity / sentinel for empty tree>

    # 2. SOLVE LEFT AND RIGHT (leap of faith)
    left_ans  = solve(node.left)
    right_ans = solve(node.right)

    # 3. COMBINE with current node
    return combine(node, left_ans, right_ans)
```

Three questions you answer for every problem:

1. **What does `solve(node)` return?** One precise English sentence.
2. **What does empty (`None`) return?** The identity for your combine operation.
3. **How do you combine** `node.val`, `left_ans`, `right_ans`?

If you cannot answer (1), you are not ready to code.

---

## 4B: Worked Micro-Examples

### Tree sum

> `solve(node)` = sum of all values in the subtree rooted at `node`.
> Empty → 0.
> Combine → `node.val + left + right`.

```python
def tree_sum(node):
    if node is None:
        return 0
    return node.val + tree_sum(node.left) + tree_sum(node.right)
```

### Node count

```python
def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)
```

### Max value

```python
def tree_max(node):
    if node is None:
        return float('-inf')   # identity for max
    return max(node.val, tree_max(node.left), tree_max(node.right))
```

### Height (edges)

```python
def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))
```

### Max depth (nodes) — LeetCode 104 style

```python
def max_depth(node):
    if node is None:
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))
```

---

## 4C: Information Flow — Up vs Down

Two directions of information:

### Bottom-up (return values)
Children compute answers; parent combines. Height, sum, diameter helper, balanced check.

### Top-down (parameters)
Parent passes context into children: current depth, path-so-far, running sum, bounds.

```python
def print_depths(node, depth=0):
    if node is None:
        return
    print(node.val, depth)
    print_depths(node.left, depth + 1)
    print_depths(node.right, depth + 1)
```

Many hard problems need **both**: pass something down, return something up (path sum variants, LCA with status flags, max path sum).

---

## 4D: The "What to Return" Decision Guide

| Problem asks for… | Often return… |
|---|---|
| A single number about whole tree | int / float from root call |
| Yes/No property | bool |
| A node | TreeNode or None |
| Multiple facts per subtree | tuple (e.g., `(height, is_balanced)`) |
| Side effect (mutate / collect) | void + external list / nonlocal |

**Returning a tuple** is the pro move when one recursive pass must compute two coupled facts (balanced + height, diameter + height).

```python
def is_balanced(root):
    def helper(node):
        if not node:
            return 0, True  # height, balanced
        lh, lb = helper(node.left)
        rh, rb = helper(node.right)
        height = 1 + max(lh, rh)
        balanced = lb and rb and abs(lh - rh) <= 1
        return height, balanced
    return helper(root)[1]
```

---

## 4E: Common Framework Mistakes

**Mistake 1: Forgetting the null check**
```python
# ❌ AttributeError on empty tree or missing child
def max_depth(node):
    return 1 + max(max_depth(node.left), max_depth(node.right))
```

**Mistake 2: Wrong identity for empty**
```python
# ❌ height as edges but empty returns 0 → single node height becomes 1
def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))
```

**Mistake 3: Combining before recursing when you need child answers**
You need postorder-style combine for height/diameter. Preorder is for "act then go."

**Mistake 4: Mutating shared lists without copying**
Path-sum "find all paths" needs `path.append` + recurse + `path.pop` (backtracking), or pass `path + [node.val]` (copies).

---

# PART 5: CLASSIC PROBLEM — MAX DEPTH

## Pattern Identification

**Pattern: Bottom-up recursive combine (binary recursion on tree)**

`maxDepth(node)` = 1 + max(maxDepth(left), maxDepth(right)); empty → 0.

## Solution

```python
def maxDepth(root):
    if root is None:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

## BFS Alternative

```python
from collections import deque

def maxDepth_bfs(root):
    if not root:
        return 0
    q = deque([root])
    depth = 0
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        depth += 1
    return depth
```

## Trace

```
        3
       / \
      9  20
        /  \
       15   7

maxDepth(3)
  maxDepth(9)=1
  maxDepth(20)=1+max(maxDepth(15), maxDepth(7))=1+max(1,1)=2
→ 1+max(1,2)=3
```

## Edge Cases

| Input | Output |
|---|---|
| `None` | 0 |
| Single node | 1 |
| Skewed left chain of n | n |

## Complexity

Time O(n). Space O(h) recursion or O(w) BFS.

> **Time: O(n), Space: O(h)**

---

# PART 6: CLASSIC PROBLEM — DIAMETER

## Pattern Identification

**Pattern: Postorder helper returning height; track global max path**

At every node, the longest path **through that node** uses `height(left) + height(right)` edges (LC 543). Diameter is the max of that quantity over all nodes.

Critical insight: diameter may **not** pass through the root. You must consider every node as a potential "highest point" of the path.

## Solution

```python
def diameterOfBinaryTree(root):
    best = 0

    def height(node):
        nonlocal best
        if not node:
            return 0  # LC uses node-count height; edges = left+right
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)  # edges through node
        return 1 + max(left, right)

    height(root)
    return best
```

## Trace

```
        1
       / \
      2   3
     / \
    4   5

height(4)=1, height(5)=1
at 2: best = max(0, 1+1)=2; height(2)=2
height(3)=1
at 1: best = max(2, 2+1)=3; height(1)=3
return 3
```

## Edge Cases

| Case | Diameter (edges) |
|---|---|
| Empty / single node | 0 |
| Two nodes | 1 |
| Straight line of n nodes | n-1 |

## Complexity

Time O(n) — one pass. Space O(h).

> **Time: O(n), Space: O(h)**

## Related: Binary Tree Maximum Path Sum (LC 124)

Same skeleton, but values can be negative — you may skip a child:

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

`gain` = max path sum **starting at node and going down** (contribution to parent). `best` considers paths that bend at node.

---

# PART 7: CLASSIC PROBLEM — PATH SUM

## 7A: Path Sum I — Root-to-Leaf Exists (LC 112)

### Pattern

Top-down remaining target. At leaf, check equality.

```python
def hasPathSum(root, targetSum):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == targetSum
    remain = targetSum - root.val
    return hasPathSum(root.left, remain) or hasPathSum(root.right, remain)
```

### Trace

```
      5
     / \
    4   8
   /   / \
  11  13  4
 /  \      \
7    2      1
target = 22

5→4→11→2: 5+4+11+2=22 → True
```

---

## 7B: Path Sum II — All Root-to-Leaf Paths (LC 113)

```python
def pathSum(root, targetSum):
    result = []

    def dfs(node, remain, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remain == node.val:
            result.append(path[:])  # copy
        else:
            dfs(node.left, remain - node.val, path)
            dfs(node.right, remain - node.val, path)
        path.pop()  # backtrack

    dfs(root, targetSum, [])
    return result
```

**Why `path[:]`:** without a copy, every entry in `result` aliases the same list object that gets mutated.

**Why `pop`:** restore path for the sibling branch.

---

## 7C: Path Sum III — Any Downward Path (LC 437) — PREVIEW note

Any node to descendant (not necessarily root/leaf). Prefix-sum + hash map is the optimal approach (hashing module). Brute: from every node, DFS downward — O(n²) worst case. Full optimal treatment belongs with hashing + trees integration; brute is acceptable early drill.

```python
def pathSum_brute(root, targetSum):
    def count_from(node, remain):
        if not node:
            return 0
        here = 1 if node.val == remain else 0
        return here + count_from(node.left, remain - node.val) \
                    + count_from(node.right, remain - node.val)

    if not root:
        return 0
    return count_from(root, targetSum) \
         + pathSum_brute(root.left, targetSum) \
         + pathSum_brute(root.right, targetSum)
```

---

# PART 8: SYMMETRIC, INVERT, FLATTEN

## 8A: Symmetric Tree (LC 101)

### Pattern

Two trees (or two subtrees) are mirrors: values equal, and left↔right crossed recursion.

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
    return mirrors(root, root) if root else True
    # cleaner: return True if not root else mirrors(root.left, root.right)
```

### Trace

```
      1
     / \
    2   2
   / \ / \
  3  4 4  3

mirrors(2,2): vals equal
  mirrors(3,3) True
  mirrors(4,4) True
→ True
```

### Edge Cases

Empty → True. Single node → True. One side missing child → False if other has it.

> **Time: O(n), Space: O(h)**

---

## 8B: Invert Binary Tree (LC 226)

### Pattern

Swap left/right at every node. Preorder or postorder both work; postorder swaps after children inverted.

```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

Or BFS:

```python
from collections import deque

def invertTree_bfs(root):
    if not root:
        return None
    q = deque([root])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return root
```

> **Time: O(n), Space: O(h) or O(w)**

---

## 8C: Flatten to Linked List (LC 114)

Flatten into a "linked list" using `right` pointers, preorder order, in-place.

### Approach — reverse postorder (right, left, visit) with running `prev`

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

### Why this order

You rebuild from the end of the preorder sequence backward. After processing, `prev` is the head of the already-flattened suffix. Attach current node's right to that suffix.

### Trace

```
    1
   / \
  2   5
 / \   \
3   4   6

Process order (right-left-root): 6, 5, 4, 3, 2, 1
After: 1 → 2 → 3 → 4 → 5 → 6 (via right), all left None
```

### Alternative — find rightmost of left subtree

Classic O(n) pointer rewiring without reverse thinking — also fine.

> **Time: O(n), Space: O(h)**

---

# PART 9: SERIALIZE / DESERIALIZE

## Pattern Identification

**Pattern: Preorder with null markers** (or level-order with nulls)

You must encode structure, not just values — hence explicit nulls.

## Preorder DFS Solution

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

## Trace

```
    1
   / \
  2   3
     / \
    4   5

serialize: 1,2,#,#,3,4,#,#,5,#,#
deserialize consumes tokens in same preorder, building left then right.
```

## Level-Order Variant (LC-style BFS protocol)

```python
from collections import deque

class CodecBFS:
    def serialize(self, root):
        if not root:
            return ""
        out, q = [], deque([root])
        while q:
            node = q.popleft()
            if not node:
                out.append('#')
                continue
            out.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        # optional: trim trailing #s
        while out and out[-1] == '#':
            out.pop()
        return ','.join(out)

    def deserialize(self, data):
        if not data:
            return None
        vals = data.split(',')
        root = TreeNode(int(vals[0]))
        q = deque([root])
        i = 1
        while q and i < len(vals):
            node = q.popleft()
            if vals[i] != '#':
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != '#':
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1
        return root
```

**Interview tip:** State the protocol first ("preorder with `#` nulls" or "BFS with `#`"), then code. Mismatched serialize/deserialize is the #1 fail.

## Edge Cases

Empty tree → `"#"` or `""` (pick one and stay consistent). Negative values — `str(node.val)` handles them. Multi-digit — delimiter `,` required. Single node → `"5,#,#"` (preorder) or `"5"`.

> **Time: O(n), Space: O(n)**

**Spine:** LC 297 is an M5/M11 hard — blind-code both protocols once.

---

# PART 9B: TREE DP FAMILY (MUST-KNOW)

Tree DP = postorder returning a **tuple of states** for the subtree (not a single scalar).

### Pattern template

```
dfs(node) -> tuple:
  base: empty → zeros / -inf as needed
  combine children tuples
  return states for *this* subtree
answer = best over root states (or global)
```

### Classic 1 — House Robber III (LC 337)

State: `(rob_this, skip_this)`.

```python
def rob(root):
    def dfs(node):
        if not node:
            return 0, 0
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob_this = node.val + ls + rs
        skip_this = max(lr, ls) + max(rr, rs)
        return rob_this, skip_this
    return max(dfs(root))
```

### Classic 2 — Binary Tree Max Path Sum (LC 124)

Path can bend at a node. Helper returns **gain downward** (one arm); global tracks bend.

```python
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        L = max(0, gain(node.left))
        R = max(0, gain(node.right))
        best = max(best, node.val + L + R)  # bend
        return node.val + max(L, R)         # one arm to parent
    gain(root)
    return best
```

### Classic 3 — Binary Tree Cameras (LC 968) — stretch

State per subtree: `0` = needs camera, `1` = has camera, `2` = covered by child. Place greedily in postorder. Know the state machine; code once under timer as stretch.

### Decision cues

| Cue | Tool |
|---|---|
| Choose parent XOR child | Rob/skip tuple |
| Path may bend | Down-gain + global |
| Cover / infect / camera | Multi-state postorder |

**Not the same as** graph DP on general graphs (cycles). Trees: no visited-set drama if you only go to children.

---

# PART 10: LOWEST COMMON ANCESTOR (BINARY TREE)

Not a BST — you cannot use value comparisons. Structure only.

## Pattern Identification

**Pattern: Postorder search — return node if found in subtree; combine left/right hits**

Definition: LCA of `p` and `q` is the deepest node that has both `p` and `q` as descendants (a node is a descendant of itself).

## Solution (LC 236 — nodes guaranteed present)

```python
def lowestCommonAncestor(root, p, q):
    if root is None or root is p or root is q:
        return root

    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:
        return root          # p and q in different subtrees
    return left or right     # both in one side (or neither)
```

## Why this works

- If current is `p` or `q`, return it (could be the LCA if the other lies below).
- If both sides return non-null, current splits the two nodes → current is LCA.
- If only one side non-null, propagate that upward.

## Trace

```
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4

LCA(5, 1): left finds 5, right finds 1 → return 3
LCA(5, 4): left of 3 finds 5 (and 4 is under 5, so when at 5:
           root is p → return 5) → propagate 5
LCA(6, 4): under 5, left finds 6, right finds 4 → return 5
```

## Edge Cases

`p` is ancestor of `q` → answer is `p`. Root is one of them → root. Problem variants where nodes may be missing need an extra "found count" — LC 236 assumes both exist.

> **Time: O(n), Space: O(h)**

---

# PART 11: CONSTRUCT TREE FROM TRAVERSALS

## 11A: Preorder + Inorder (LC 105)

### Key facts

- Preorder: **root is first** element.
- Inorder: root splits into **left subtree inorder** | root | **right subtree inorder**.
- Recurse on the matching preorder slices.

```python
def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}  # value → inorder index
    pre_i = 0

    def build(lo, hi):
        nonlocal pre_i
        if lo > hi:
            return None
        root_val = preorder[pre_i]
        pre_i += 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder) - 1)
```

### Trace

```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]

root=3, mid splits inorder: left=[9], right=[15,20,7]
left subtree: pre next=9 → leaf
right subtree: pre next=20, inorder mid at 20: left=[15], right=[7]
→ standard LC example tree
```

### Why the hash map

Finding root in inorder each time is O(n) → total O(n²). Map makes split O(1) → total O(n).

**Assumption:** values are unique. If duplicates exist, this map breaks — problems usually guarantee uniqueness.

---

## 11B: Postorder + Inorder (LC 106)

Postorder: **root is last**. Build right subtree before left if you scan postorder from the end (symmetric to preorder technique).

```python
def buildTree(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    post_i = len(postorder) - 1

    def build(lo, hi):
        nonlocal post_i
        if lo > hi:
            return None
        root_val = postorder[post_i]
        post_i -= 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.right = build(mid + 1, hi)  # right FIRST
        root.left = build(lo, mid - 1)
        return root

    return build(0, len(inorder) - 1)
```

---

## 11C: Why Preorder + Postorder Is Not Enough (Usually)

Preorder + postorder does **not** uniquely determine a general binary tree (ambiguous left/right for single-child nodes). It works for **full** binary trees under extra constraints. Interview default: pre+in or post+in.

---

# PART 12: MORE HIGH-FREQUENCY PATTERNS (COMPRESSED)

## 12A: Right Side View (LC 199)

BFS: last node in each level. Or DFS prioritizing right, record first visit per depth.

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

## 12B: Count Complete Tree Nodes (LC 222)

Naive O(n). Exploit complete shape: height of left spine vs right spine — if equal, perfect subtree `2^h - 1`; else recurse. O(log² n).

## 12C: Validate same tree (LC 100)

```python
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

## 12D: Subtree of another tree (LC 572)

For each node in `root`, check `isSameTree(node, subRoot)`. O(n·m) naive; fine for interviews unless constrained harder.

---

# PART 13: COMPLEXITY ANALYSIS FOR TREES

## Time

Visiting each node a constant number of times → **O(n)**.

Exceptions:
- Naive Path Sum III: O(n²)
- Naive subtree check: O(n·m)
- Construct without hash map: O(n²)

## Space

| Source | Cost |
|---|---|
| Recursion depth | O(h); worst O(n) skewed; best O(log n) balanced |
| BFS queue | O(w); worst ~n/2 at bottom of perfect tree → O(n) |
| Output list of all paths | Can be O(n·h) or worse |

**Always state h vs n** in interviews: "O(h) stack, O(n) worst case if skewed."

---

# PART 14: DECISION FRAMEWORK — WHICH TOOL?

```
╔════════════════════════════════════════════════════════════════╗
║              BINARY TREE PROBLEM DECISION GUIDE                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  1. Does "level" / "distance from root" / "left→right by row"  ║
║     matter? → BFS level-order                                  ║
║                                                                ║
║  2. Need child answers before deciding at parent?              ║
║     → Postorder / bottom-up recursion                          ║
║                                                                ║
║  3. Need ancestor context (depth, path, bounds)?               ║
║     → Top-down parameters (+ maybe return upward)              ║
║                                                                ║
║  4. Looking for a path property root→leaf?                     ║
║     → DFS with remaining sum / backtracking path list          ║
║                                                                ║
║  5. Longest / best path that can BEND at a node?               ║
║     → Global accumulator + helper returning "gain downward"    ║
║                                                                ║
║  6. Find deepest common ancestor of two nodes?                 ║
║     → LCA postorder combine (BT) or BST value walk (BST file)  ║
║                                                                ║
║  7. Rebuild structure from sequences?                          ║
║     → Pre/Post + Inorder split with index map                  ║
║                                                                ║
║  8. Persist tree as string?                                    ║
║     → Serialize with explicit null markers                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

# PART 15: MASTER CHEAT SHEETS

## 15A: Vocabulary

| Term | Definition (this lesson) |
|---|---|
| Depth(node) | Edges from root to node |
| Height(node) | Edges from node to deepest leaf |
| Height(tree) | Height(root); empty = -1 |
| Max depth (LC) | Nodes on longest root→leaf; empty = 0 |
| Diameter | Max edges on any path; check every bend node |
| Leaf | Both children None |
| Level | All nodes at equal depth |

## 15B: Traversal Orders

```
PRE:  N L R     ITER: stack, push R then L
IN:   L N R     ITER: left spine, pop, go right
POST: L R N     ITER: two-stack or reverse modified pre
BFS:  level     QUEUE: size-loop per level
```

## 15C: Recursive Framework

```
NULL → identity
LEFT = f(node.left)
RIGHT = f(node.right)
return COMBINE(node, LEFT, RIGHT)
```

## 15D: Classic Problem Map

| Problem | Core trick |
|---|---|
| Max depth | 1 + max(left, right) |
| Diameter | track left_h + right_h globally |
| Path sum I | remaining target; check at leaf |
| Path sum II | backtrack path list |
| Symmetric | mirror recursion crossed |
| Invert | swap children |
| Flatten | reverse postorder rewire / rightmost link |
| Serialize | preorder + `#` markers |
| LCA (BT) | if both sides hit → root |
| Build pre+in | root from pre; split in with map |

## 15E: Null Identity Table

| Quantity | Empty returns |
|---|---|
| Sum / count | 0 |
| Max value | -∞ |
| Min value | +∞ |
| Height (edges) | -1 |
| Depth/height (nodes, LC) | 0 |
| Balanced flag | True |
| Node reference search | None |

---

# PART 16: FULL WORKED TRACES (STUDY SET)

## Trace A — Inorder / Preorder / Postorder / BFS

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7
```

| Order | Result |
|---|---|
| Pre | 4, 2, 1, 3, 6, 5, 7 |
| In | 1, 2, 3, 4, 5, 6, 7 |
| Post | 1, 3, 2, 5, 7, 6, 4 |
| BFS | [[4], [2, 6], [1, 3, 5, 7]] |

## Trace B — Diameter helper values

```
Node: height_return, best_after_node

1: h=1
3: h=1
2: left+right=2 → best≥2; h=2
5: h=1
6: h=1
4: left+right via 2 and 6 = 2+1=3 → best=3; h=3
Diameter edges = 3  (path 1-2-4-6-5 or 3-2-4-6-5)
```

## Trace C — LCA

```
LCA(1,3) under tree above = 2
LCA(1,7) = 4
LCA(5,7) = 6
LCA(4,1) = 4
```

## Trace D — Build from traversals

```
pre = [4,2,1,3,6,5,7]
in  = [1,2,3,4,5,6,7]
→ uniquely rebuilds the tree in Trace A
```

---

# PART 17: TEST PROBLEMS (WITH FULL SOLUTIONS)

# Problem 1: Sum of Left Leaves

## Pattern Identification

DFS; a left leaf is `node.left` that is a leaf. Or pass a flag `is_left`.

## Solution

```python
def sumOfLeftLeaves(root):
    def dfs(node, is_left):
        if not node:
            return 0
        if not node.left and not node.right:
            return node.val if is_left else 0
        return dfs(node.left, True) + dfs(node.right, False)
    return dfs(root, False)
```

## Trace

```
    3
   / \
  9  20
    /  \
   15   7
Left leaves: 9 and 15 → 24
```

## Complexity

O(n) time, O(h) space.

---

# Problem 2: Binary Tree Zigzag Level Order

## Pattern Identification

BFS levels; reverse odd levels (0-index even = left→right).

## Solution

```python
from collections import deque

def zigzagLevelOrder(root):
    if not root:
        return []
    q = deque([root])
    result = []
    left_to_right = True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        if not left_to_right:
            level.reverse()
        result.append(level)
        left_to_right = not left_to_right
    return result
```

## Trace

```
    3
   / \
  9  20
    /  \
   15   7
→ [[3], [20, 9], [15, 7]]
```

## Complexity

O(n) time, O(w) space.

---

# Problem 3: Lowest Common Ancestor — Parent Pointers Variant

## Pattern Identification

If nodes have `parent` pointers: walk from `p` to root marking ancestors; walk from `q` until hit a marked node. Or equalize depths then climb together.

## Solution (depth equalize)

```python
def lca_with_parent(p, q):
    def depth(node):
        d = 0
        while node:
            d += 1
            node = node.parent
        return d

    dp, dq = depth(p), depth(q)
    # Make p the deeper one
    if dq > dp:
        p, q = q, p
        dp, dq = dq, dp
    for _ in range(dp - dq):
        p = p.parent
    while p is not q:
        p = p.parent
        q = q.parent
    return p
```

## Complexity

O(h) time, O(1) space.

---

# Problem 4: Maximum Width of Binary Tree (LC 662)

## Pattern Identification

BFS with **indexed positions** like heap indices. Width of level = last_index - first_index + 1.

## Solution

```python
from collections import deque

def widthOfBinaryTree(root):
    if not root:
        return 0
    q = deque([(root, 0)])  # node, index
    best = 0
    while q:
        _, first = q[0]
        _, last = q[-1]
        best = max(best, last - first + 1)
        for _ in range(len(q)):
            node, i = q.popleft()
            if node.left:
                q.append((node.left, 2 * i))
            if node.right:
                q.append((node.right, 2 * i + 1))
    return best
```

Normalize indices by subtracting `first` each level to avoid unbounded integers in deep skewed trees (interview polish).

## Complexity

O(n) time, O(w) space.

---

# Problem 5: House Robber III (LC 337) — Tree DP (see Part 9B)

## Pattern Identification

At each node: (gain_if_rob_this, gain_if_skip_this). Cannot rob parent and child.

## Solution

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

## Complexity

O(n) time, O(h) space.

---

# Problem 6: Validate Binary Tree — No Cycles / Single Root (Structural)

Given `n` nodes labeled `0..n-1` and `leftChild[i]`, `rightChild[i]` (-1 = none), check whether they form a valid binary tree (LC 1361).

## Pattern Identification

Each child has ≤ 1 parent; exactly one root (indegree 0); from root, reachable count = n (no cycles / disconnected).

## Solution Sketch

```python
def validateBinaryTreeNodes(n, leftChild, rightChild):
    indeg = [0] * n
    for i in range(n):
        for c in (leftChild[i], rightChild[i]):
            if c != -1:
                indeg[c] += 1
                if indeg[c] > 1:
                    return False
    roots = [i for i in range(n) if indeg[i] == 0]
    if len(roots) != 1:
        return False
    # BFS/DFS count reachable
    seen = set()
    stack = [roots[0]]
    while stack:
        u = stack.pop()
        if u in seen:
            return False
        seen.add(u)
        for c in (leftChild[u], rightChild[u]):
            if c != -1:
                stack.append(c)
    return len(seen) == n
```

---

# PART 18: WHAT THIS MODULE DOES NOT COVER

| Topic | Where |
|---|---|
| BST invariant, insert/delete, validate BST | `Trees/Binary Search Trees.md` |
| AVL / Red-Black mechanics | BST lesson (intuition) + later if needed |
| Tries | Module 10 |
| Heaps as trees | Module 6 |
| Graphs (general) | Module 7 — trees are special DAGs/undirected acyclic graphs |
| Segment / Fenwick | Module 10 exposure |
| Re-rooting DP / binary lifting LCA | Optional stretch / Phase B |

---

# PART 19: STATUS NOTES (PROGRAM GOVERNANCE)

- This file is the **teach** artifact for Module 5 — Binary Trees.
- Status remains `taught` only after concept delivery; `complete` requires retention + timed gates per `Handoff Doc.md`.
- Path Sum III optimal hash solution is **integration** with hashing — brute version is in-scope here; optimal may be drilled as earned-tools integration.

---

# END OF BINARY TREES LESSON
