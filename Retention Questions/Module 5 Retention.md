<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 5 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 5 Retention.keys.md`. Attempt first, then grade.

# MODULE 5 RETENTION — BINARY TREES + BST (+ CUMULATIVE)

---

**Purpose:** Cumulative retention grill for Module 5 teach artifacts:
- `Trees/Binary Trees.md`
- `Trees/Binary Search Trees.md`

Plus spaced pull from prior Phase A material (Big O, Arrays/Strings, Hashing, Recursion). Problems that need **untought** Module 3–4 / Graphs / DP machinery are tagged **`PREVIEW — no mastery credit`**.

**Rules:**
1. No pattern labels on the problem statement side — identify the tool yourself, then check the answer key.
2. For each problem: approach → code → trace → edge cases → complexity.
3. Tag misses: `knowledge-gap` / `misread` / `time-pressure` / `careless-slip`.
4. Passing this grill alone ≠ `complete`. Still need timed verification + ledger updates per `Handoff Doc.md`.

**Escalation map:**

| Section | Focus | Difficulty |
|---|---|---|
| A | Vocabulary + complexity rapid fire | Warm |
| B | Traversals + recursive framework | Warm → Medium |
| C | Classic binary tree | Medium |
| D | BST | Medium |
| E | Harder tree / BST | Medium → Hard |
| F | Cumulative integration | Mixed |
| G | Blind-style mixed set | Interview |

---

# SECTION A: RAPID FIRE — VOCABULARY & COMPLEXITY

---

## A1.

Define **depth** of a node vs **height** of a node (edges convention from the Binary Trees lesson). What is height of an empty tree? What does LeetCode 104 `maxDepth` return for a single node?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 1)

## A2.

```
        1
       / \
      2   3
     / \
    4   5
```

Give: preorder, inorder, postorder, level-order (as list of levels). Diameter in **edges**.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 2)

## A3.

True or false: If every node satisfies `left.val < node.val < right.val` (when children exist), the tree is a valid BST.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 3)

## A4.

Time and space of recursive DFS on a binary tree with `n` nodes and height `h`. Same for BFS level-order.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 4)

## A5.

BST search / insert / delete: average vs worst-case time. What causes the worst case?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 5)

## A6.

```python
def f(node):
    if node is None:
        return 0
    return 1 + max(f(node.left), f(node.right))
```

What does `f` compute? Recurrence for time on a perfect binary tree of height h (nodes n = 2^{h+1}-1)?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 6)

## A7.

When does a **BST** beat a **hash set/map**? When does hash win?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 7)

## A8.

Null identity: what should an empty subtree return for (a) sum, (b) height in edges, (c) max value, (d) "is balanced" flag?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 8)

# SECTION B: TRAVERSALS & FRAMEWORK

---

## B1.

Implement iterative **inorder** traversal. Trace on:

```
    2
   / \
  1   3
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 9)

## B2.

Implement iterative **preorder**. Why push **right before left**?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 10)

## B3.

Write the **recursive tree framework** in three lines of English, then implement `count_nodes` and `tree_max`.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 11)

## B4.

Level-order that returns **list of levels**. What does `level_size = len(q)` buy you?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 12)

## B5.

Convert recursive postorder thinking into: "I need both children's answers before I can decide at this node." Name three problems that require this.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 13)

# SECTION C: CLASSIC BINARY TREE

---

## C1. Maximum Depth

Compute max depth (nodes). Empty → 0.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 14)

## C2. Diameter of Binary Tree

Return diameter in **edges** (LC 543).


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 15)

## C3. Path Sum I

Return whether any root-to-leaf path sums to `targetSum`.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 16)

## C4. Path Sum II

Return all root-to-leaf paths that sum to target.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 17)

## C5. Symmetric Tree


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 18)

## C6. Invert Binary Tree


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 19)

## C7. Flatten Binary Tree to Linked List

Flatten in-place to preorder list via `right` pointers; all `left` null.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 20)

## C8. Serialize / Deserialize


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 21)

## C9. LCA of Binary Tree (not BST)

Nodes `p` and `q` are guaranteed to exist.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 22)

## C10. Construct from Preorder + Inorder

Assume unique values.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 23)

# SECTION D: BINARY SEARCH TREES

---

## D1. Validate BST


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 24)

## D2. Insert + Search

Implement both iteratively.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 25)

## D3. Delete Node in BST

Delete `key`. Cover all three cases in code.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 26)

## D4. Kth Smallest


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 27)

## D5. Range Sum BST


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 28)

## D6. LCA in BST


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 29)

## D7. Sorted Array → Balanced BST


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 30)

## D8. BST Iterator

Implement `BSTIterator` with `next` / `hasNext`, amortized O(1) `next`, O(h) space.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 31)

## D9. Balancing intuition (short answer)

What problem do AVL / Red-Black solve? State one height guarantee. Do you implement them in a standard FAANG coding round?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 32)

# SECTION E: HARDER TREE / BST

---

## E1. Binary Tree Maximum Path Sum

Any node-to-node path; node values may be negative. Return max path sum.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 33)

## E2. Right Side View


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 34)

## E3. Zigzag Level Order


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 35)

## E4. Width of Binary Tree

Max width using heap-style indices.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 36)

## E5. Construct BST from Preorder Only


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 37)

## E6. Inorder Successor in BST

No parent pointers. Given root and node `p`, return successor node (or None).


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 38)

## E7. Trim BST

Keep only nodes with values in `[low, high]`.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 39)

## E8. House Robber III

Cannot rob two adjacent nodes (parent-child).


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 40)

## E9. Recover BST (two nodes swapped)

Describe the approach; optional code.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 41)

## E10. Path Sum III (any downward path) — two solutions

(a) Brute O(n²)  
(b) Prefix + hash O(n) — **earned if hashing complete**


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 42)

# SECTION F: CUMULATIVE INTEGRATION

Uses Module 5 + prior earned tools (Big O, Arrays, Hashing, Recursion). Tag PREVIEW if you reach for untaught heavy machinery.

---

## F1. Complexity

```python
def walk(node):
    if not node:
        return 0
    return node.val + walk(node.left) + walk(node.right)
```

Time / space on (a) perfect tree n nodes (b) right-skewed chain n nodes.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 43)

## F2. Array + Tree

Given a binary tree, return `True` if there exist two nodes (not necessarily distinct positions — problem: two **different** nodes) whose values sum to `k`. Tree is a **BST**.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 44)

## F3. Recursion + Tree

Explain why naive

```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

is exponential, but tree `maxDepth` is linear — both are "binary recursion."


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 45)

## F4. Hashing + Traversal

Return vertical order traversal labels: map `hd → list of values` where root hd=0, left hd-1, right hd+1. Any order within a column acceptable for this retention item.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 46)

## F5. Arrays — Build tree then query

You are given sorted `nums` unique. Build height-balanced BST, then return kth smallest. Complexity of full pipeline?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 47)

## F6. Decision

Problem: "Design a structure supporting insert, delete, and getRandom in O(1) average." Is BST the right tool?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 48)

## F7. PREVIEW — Word Ladder style BFS on implicit graph

`PREVIEW — no mastery credit` (Graphs module).

Short note only: level-order BFS skill from trees transfers to graph BFS; the new piece is building adjacency / neighbor generation.

---

## F8. Subarray sum equals K vs Path Sum III

State the shared pattern in one sentence.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 49)

# SECTION G: BLIND-STYLE MIXED SET

Solve without scrolling to answers first. Answer key below each problem.

---

## G1.

Implement `isBalanced(root)` — height-balanced per AVL definition — in one pass.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 50)

## G2.

Given preorder and inorder of a binary tree (unique vals), return postorder **without** necessarily building the tree (or build then postorder — either OK).


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 51)

## G3.

BST: find the closest value to a float `target`.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 52)

## G4.

```python
def mystery(node, L, R):
    if not node:
        return None
    node.left = mystery(node.left, L, R)
    node.right = mystery(node.right, L, R)
    if node.val < L:
        return node.right
    if node.val > R:
        return node.left
    return node
```

What does this do? Is the child recursion order important?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 53)

## G5.

Prove or disprove: Inorder of any binary tree is sorted iff the tree is a BST (unique values, strict invariant).


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 54)

## G6.

You must serialize a binary tree to a string and deserialize. Constraints: values fit in 32-bit ints. Give two valid strategies and one invalid.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 55)

## G7.

Delete the minimum node in a BST; return new root. Do not assume min is a leaf.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 56)

## G8.

Complexity of building a BST by inserting `n` sorted values one-by-one into an initially empty unbalanced BST?


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 57)

## G9.

```
preorder = [3,9,20,15,7]
inorder  = [9,3,15,20,7]
```

Draw the tree; give postorder.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 58)

## G10.

Interview speech (write 4–6 sentences): Compare hash map, unbalanced BST, and Red-Black tree for a system that needs frequent range reports over live keys.


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 59)

# SECTION H: ERROR DIAGNOSIS DRILL

For each buggy snippet, name the bug and fix.

---

## H1.

```python
def isValidBST(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return isValidBST(root.left) and isValidBST(root.right)
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 60)

## H2.

```python
def diameter(root):
    if not root:
        return 0
    return max_depth(root.left) + max_depth(root.right)
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 61)

## H3.

```python
def pathSum(root, target):
    result = []
    def dfs(node, remain, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remain == node.val:
            result.append(path)  # !!!
        dfs(node.left, remain - node.val, path)
        dfs(node.right, remain - node.val, path)
        path.pop()
    dfs(root, target, [])
    return result
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 62)

## H4.

```python
def lca_bst(root, p, q):
    if p.val < root.val:
        return lca_bst(root.left, p, q)
    if q.val > root.val:
        return lca_bst(root.right, p, q)
    return root
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 63)

## H5.

```python
def maxDepth(root):
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```


> **Answer key:** `Retention Questions/keys/Module 5 Retention.keys.md` (block 64)

# SECTION I: CHEAT SHEET — RETENTION FACE

```
BINARY TREE
  DFS: pre N-L-R | in L-N-R | post L-R-N
  BFS: queue + level_size loop
  Framework: null → left/right → combine
  Diameter / max path: global + downward gain
  LCA(BT): both sides hit → root
  Build: pre/post + in + index map
  Serialize: markers for null

BST
  Invariant: all left < node < all right
  Validate: BOUNDS not local
  Inorder = sorted
  LCA: walk to split
  Range: prune
  Kth: inorder / sizes
  Delete: successor if 2 kids
  vs Hash: order vs equality
  Balance: AVL/RBT keep h = O(log n)
```

---

# SECTION J: SCORING & LEDGER HOOKS

| Band | Suggestion |
|---|---|
| Miss vocab / bounds / diameter-through-root | Re-teach Binary Trees Parts 1, 4, 6 + BST Part 3 |
| Miss iterator / delete / LCA BST | Re-drill BST Parts 2, 6, 9 |
| Miss cumulative hash+path | Integration: Path Sum III + subarray sum |
| Clean Section G under time | Ready to schedule Module 5 **timed verify** |

Update `Metrics/Retention Ledger.md` subskills:

- BT traversals (rec+iter+BFS)
- Recursive tree framework
- Diameter / path sum family
- Serialize / construct
- LCA BT vs BST
- BST CRUD + validate bounds
- Range / kth / iterator
- BST vs hash decision

Mark heat `strong` / `shaky` / `weak` from this grill. Fail twice on same subskill → re-teach before timed gate.

---

# END OF MODULE 5 RETENTION
