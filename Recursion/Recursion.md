# RECURSION — THE COMPLETE LESSON

---

> **Lesson contract:** Read framework + patterns first. Cap in-lesson traces at a few exemplars; drill from Retention + Spine. Answers for retention live under `Retention Questions/keys/`.


# PART 1: WHAT RECURSION ACTUALLY IS

## The Core Idea

A recursive function is a function that **calls itself** to solve smaller versions of the same problem.

That's the one-sentence definition. But it tells you nothing about **why** it works, **how** to think about it, or **when** to use it. Let me fix that.

## The Three Components of Every Recursive Function

Every recursive function has exactly three things:

```
1. BASE CASE     — When to STOP. The simplest version of the problem
                   that can be answered directly without recursion.

2. RECURSIVE CASE — How to SHRINK. Break the current problem into a
                    smaller version of itself.

3. COMBINATION   — How to USE the result of the smaller problem to
                    solve the current problem.
```

If any of these is missing, your recursion is broken:
- No base case → infinite recursion → stack overflow → crash
- No shrinking → never reaches base case → infinite recursion → crash
- No combination → you solve subproblems but never use them → wrong answer

## The Simplest Possible Example

```python
def countdown(n):
    if n == 0:           # BASE CASE: stop at 0
        print("Done!")
        return
    print(n)             # Do something with current problem
    countdown(n - 1)     # RECURSIVE CASE: smaller version (n-1)
```

```
countdown(3):
  prints 3
  calls countdown(2):
    prints 2
    calls countdown(1):
      prints 1
      calls countdown(0):
        prints "Done!"
        returns
      returns
    returns
  returns
```

Each call handles its own piece (printing its number) and delegates the rest to a smaller call.

## A More Meaningful Example

```python
def factorial(n):
    if n == 0:                    # BASE CASE
        return 1
    return n * factorial(n - 1)   # RECURSIVE CASE + COMBINATION
```

The **combination** here is multiplication: `n * (result of smaller problem)`.

```
factorial(4):
  4 * factorial(3)
  4 * (3 * factorial(2))
  4 * (3 * (2 * factorial(1)))
  4 * (3 * (2 * (1 * factorial(0))))
  4 * (3 * (2 * (1 * 1)))          ← base case returns 1
  4 * (3 * (2 * 1))
  4 * (3 * 2)
  4 * 6
  24
```

---

# PART 2: THE CALL STACK — HOW RECURSION WORKS IN MEMORY

## Why You Must Understand This

If you don't understand the call stack, you will:
- Not know why recursion uses O(n) space
- Not know why deep recursion crashes with "RecursionError: maximum recursion depth exceeded"
- Not be able to analyze space complexity of recursive solutions
- Not understand how to convert recursion to iteration

## What Happens When You Call a Function

Every time a function is called, Python creates a **stack frame** — a block of memory that holds:
- The function's local variables
- The parameters passed to it
- The return address (where to go back when this call finishes)

These frames are stored on the **call stack** — a last-in, first-out (LIFO) data structure.

## Visualizing the Stack

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

factorial(4)
```

**Step 1:** `factorial(4)` is called. Frame pushed onto stack.

```
STACK:
| factorial(4)  n=4 |  ← top
|____________________|
```

**Step 2:** Needs `factorial(3)`. New frame pushed.

```
STACK:
| factorial(3)  n=3 |  ← top
| factorial(4)  n=4 |
|____________________|
```

**Step 3:** Needs `factorial(2)`. New frame pushed.

```
STACK:
| factorial(2)  n=2 |  ← top
| factorial(3)  n=3 |
| factorial(4)  n=4 |
|____________________|
```

**Step 4:** Needs `factorial(1)`. New frame pushed.

```
STACK:
| factorial(1)  n=1 |  ← top
| factorial(2)  n=2 |
| factorial(3)  n=3 |
| factorial(4)  n=4 |
|____________________|
```

**Step 5:** Needs `factorial(0)`. Base case! Returns 1. Frame popped.

```
STACK:
| factorial(0)  n=0  → returns 1 |  ← popped
| factorial(1)  n=1 |  ← now top
| factorial(2)  n=2 |
| factorial(3)  n=3 |
| factorial(4)  n=4 |
|____________________|
```

**Step 6:** `factorial(1)` receives 1, computes `1 * 1 = 1`, returns 1. Popped.

```
| factorial(1)  → returns 1 |  ← popped
| factorial(2)  n=2 |  ← now top
| factorial(3)  n=3 |
| factorial(4)  n=4 |
```

**Steps 7-9:** Each frame receives result, computes, returns, pops.

```
factorial(2) → 2 * 1 = 2 → returns 2
factorial(3) → 3 * 2 = 6 → returns 6
factorial(4) → 4 * 6 = 24 → returns 24
```

**Final stack:** empty. Result: 24.

## The Space Cost

At the deepest point, we had **5 frames** on the stack (for `factorial(4)`, that's n+1 frames). Each frame is O(1) space (just stores n and the return address).

**Space complexity of factorial: O(n)** — not because we create arrays, but because of the **call stack depth.**

**This is the hidden space cost of recursion that most beginners miss.**

## Stack Overflow

Python has a default recursion limit of ~1000 frames.

```python
factorial(10000)  # RecursionError: maximum recursion depth exceeded
```

You can increase it:
```python
import sys
sys.setrecursionlimit(10000)
```

But this is a band-aid. Deep recursion is a real problem. Solutions:
1. Convert to iteration (eliminates stack frames)
2. Use tail recursion (Python doesn't optimize this, but other languages do)
3. Use memoization to avoid redundant branches (doesn't reduce depth, but reduces total calls)

---

# PART 3: HOW TO THINK RECURSIVELY

## The "Leap of Faith" Method

This is the **most important mental model** for writing recursive code. Most beginners fail because they try to trace every recursive call in their head. That's impossible for complex problems. Instead:

**Step 1:** Define what your function does in plain English. Be precise.

> `sum_array(arr, i)` returns the sum of all elements from index i to the end.

**Step 2:** Identify the base case. What's the simplest input where you know the answer immediately?

> If `i == len(arr)`, there are no elements left. Sum is 0.

**Step 3:** Assume the recursive call works correctly (the LEAP OF FAITH). If you call the function on a smaller input, it gives you the right answer. You don't need to know how.

> `sum_array(arr, i + 1)` correctly returns the sum from index i+1 to end. I trust this.

**Step 4:** Use that trusted result to solve the current problem.

> The sum from index i to end = `arr[i]` + sum from i+1 to end = `arr[i] + sum_array(arr, i + 1)`

```python
def sum_array(arr, i=0):
    if i == len(arr):              # Base case
        return 0
    return arr[i] + sum_array(arr, i + 1)  # Current + trusted result
```

**You never traced through the full recursion.** You just defined what the function does, handled the base case, and trusted that the recursive call handles the rest. That's the leap of faith.

## The Recipe For Writing Any Recursive Function

```
STEP 1: DEFINE — What does this function return/do? 
        Write it as a precise English sentence.

STEP 2: BASE CASE — What input is so simple you can answer 
        without recursion? Return that answer directly.

STEP 3: RECURSIVE CASE — How do you make the problem smaller?
        What parameter changes?
        Call yourself with the smaller version.

STEP 4: COMBINE — How do you use the result of the smaller 
        call to answer the current call?

STEP 5: VERIFY — Does the base case stop the recursion?
        Does the recursive case always move toward the base case?
        If both yes, it terminates.
```

## Common Mistakes

**Mistake 1: Wrong base case**
```python
# ❌ Off-by-one: misses the last element
def sum_array(arr, i=0):
    if i == len(arr) - 1:    # Wrong! Skips case where i == len(arr)
        return arr[i]
    return arr[i] + sum_array(arr, i + 1)

sum_array([])  # IndexError! arr[-1] doesn't exist for empty array
```

**Mistake 2: Not shrinking toward base case**
```python
# ❌ Infinite recursion
def broken(n):
    if n == 0:
        return 0
    return broken(n + 1)  # n grows instead of shrinks!
```

**Mistake 3: Forgetting to return the recursive result**
```python
# ❌ Returns None
def sum_array(arr, i=0):
    if i == len(arr):
        return 0
    sum_array(arr, i + 1)  # Forgot 'return'! Result is lost.
```

---

# PART 4: THE FIVE RECURSIVE PATTERNS

## Pattern 1: Linear Recursion

One recursive call per function invocation. The call stack grows linearly with input size.

### Framework
```python
def linear_recursion(problem):
    if is_base_case(problem):
        return base_answer
    
    smaller = make_smaller(problem)
    sub_result = linear_recursion(smaller)
    return combine(current, sub_result)
```

### Examples

**Sum of array:**
```python
def array_sum(arr, i=0):
    if i == len(arr):
        return 0
    return arr[i] + array_sum(arr, i + 1)
```

Time: O(n). Space: O(n) stack frames.

**Reverse a string:**
```python
def reverse_string(s):
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]
```

Time: O(n²) — because `s[1:]` creates a new string of length n-1 each time. 
Space: O(n²) — n stack frames, each holding a slice.

**Better version (reverse in-place with indices):**
```python
def reverse_string(chars, left=0, right=None):
    if right is None:
        right = len(chars) - 1
    if left >= right:
        return
    chars[left], chars[right] = chars[right], chars[left]
    reverse_string(chars, left + 1, right - 1)
```

Time: O(n). Space: O(n) stack frames. Each frame is O(1) since we only pass indices.

**Check if array is sorted:**
```python
def is_sorted(arr, i=0):
    if i >= len(arr) - 1:
        return True
    if arr[i] > arr[i + 1]:
        return False
    return is_sorted(arr, i + 1)
```

Time: O(n). Space: O(n).

### Complexity Pattern

Linear recursion with O(1) work per call:
- Time: O(n) — n calls, O(1) each
- Space: O(n) — n stack frames

Linear recursion with O(n) work per call (like slicing):
- Time: O(n²) — n calls, O(n) each
- Space: O(n²) — n frames, each holding O(n) data

---

## Pattern 2: Binary Recursion (Divide and Conquer)

Two recursive calls per function invocation. The problem is split into two halves.

### Framework
```python
def binary_recursion(problem):
    if is_base_case(problem):
        return base_answer
    
    left_half, right_half = split(problem)
    left_result = binary_recursion(left_half)
    right_result = binary_recursion(right_half)
    return combine(left_result, right_result)
```

### Example: Merge Sort (Preview)

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

We'll analyze merge sort fully in Week 3 (Sorting). For now, know the pattern.

### Example: Maximum Element (Divide and Conquer)

```python
def find_max(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    
    if left == right:               # Base case: one element
        return arr[left]
    
    mid = (left + right) // 2
    left_max = find_max(arr, left, mid)
    right_max = find_max(arr, mid + 1, right)
    return max(left_max, right_max)  # Combine
```

Time: O(n) — every element is visited once.
Space: O(log n) — the recursion depth is log₂(n) because we halve each time.

### Complexity Pattern

Binary recursion that halves the problem and does O(n) work to combine:
- Time: O(n log n) — merge sort pattern
- Space: O(n) or O(log n) depending on whether merge is in-place

Binary recursion that halves the problem and does O(1) work to combine:
- Time: O(n) — still visits all elements
- Space: O(log n) — depth of recursion tree

---

## Pattern 3: Multiple Branching (Exponential)

More than two recursive calls per invocation. These produce exponential time.

### The Classic: Fibonacci

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

The recursion tree:

```
                    fib(5)
                   /      \
              fib(4)      fib(3)
             /    \       /    \
         fib(3)  fib(2) fib(2) fib(1)
         /   \    / \    / \
     fib(2) fib(1) ... ...
      / \
  fib(1) fib(0)
```

Each node branches into two children. The tree has approximately 2ⁿ nodes.

Time: **O(2ⁿ)** — each call does O(1) work, roughly 2ⁿ calls.
Space: **O(n)** — the maximum **depth** of the tree, not the width. Only one branch is "active" at a time on the stack.

**This is terrible.** `fib(50)` makes over a trillion calls. The fix is **memoization** (Pattern 7 from hashing):

```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

With memoization:
- Time: **O(n)** — each value computed once
- Space: **O(n)** — memo dict + stack depth

### Complexity Pattern

Branching factor b, depth d:
- Total nodes in tree: **O(bᵈ)**
- Space (stack depth): **O(d)**

For Fibonacci: b ≈ 2, d = n → O(2ⁿ) time, O(n) space.

---

## Pattern 4: Accumulator Pattern (Tail Recursion Style)

Instead of combining results on the way **back up** the stack, carry the result **forward** as a parameter.

### Standard (Combines on the way back)

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)  # Must wait for sub-call to return before multiplying
```

### Accumulator (Carries result forward)

```python
def factorial(n, acc=1):
    if n == 0:
        return acc          # Result is already computed!
    return factorial(n - 1, acc * n)  # Pass updated result forward
```

Trace:
```
factorial(4, 1)
factorial(3, 4)      # acc = 1 * 4 = 4
factorial(2, 12)     # acc = 4 * 3 = 12
factorial(1, 24)     # acc = 12 * 2 = 24
factorial(0, 24)     # base case, return 24
```

**Why this matters:** The last thing the function does is call itself (no work after the recursive call). This is called **tail recursion.** Some languages (Scheme, Scala, many functional languages) optimize tail recursion into a loop — O(1) space instead of O(n).

**Python does NOT optimize tail recursion.** The stack still grows to O(n). But the pattern is still useful because:
1. It makes converting to iteration trivial
2. Some interviewers ask about it
3. Understanding it deepens your grasp of how recursion flows

### Converting Accumulator Recursion to Iteration

The accumulator pattern converts to iteration **mechanically:**

```python
# Recursive with accumulator
def factorial(n, acc=1):
    if n == 0:
        return acc
    return factorial(n - 1, acc * n)

# Iterative equivalent — exact same logic
def factorial_iter(n):
    acc = 1
    while n > 0:
        acc = acc * n
        n = n - 1
    return acc
```

The parameters become loop variables. The base case becomes the loop condition. The recursive call becomes the next iteration.

---

## Pattern 5: Tree Recursion (Recursive Data Structures)

Trees and linked lists are **inherently recursive** data structures. A tree node contains references to other tree nodes. Processing a tree naturally follows the recursive structure.

This is a preview — we'll go deep in Week 5 (Trees). But the pattern is:

```python
def process_tree(node):
    if node is None:              # Base case: empty tree
        return base_value
    
    left_result = process_tree(node.left)
    right_result = process_tree(node.right)
    return combine(node.value, left_result, right_result)
```

### Example: Height of Binary Tree

```python
def tree_height(node):
    if node is None:
        return 0
    left_height = tree_height(node.left)
    right_height = tree_height(node.right)
    return 1 + max(left_height, right_height)
```

Time: O(n) — visits every node once.
Space: O(h) where h = height of tree. Balanced: O(log n). Worst case (skewed): O(n).

---

# PART 5: RECURSIVE COMPLEXITY ANALYSIS

This is the deferred section from Big O. Now you have the context to understand it fully.

## Method 1: Recursion Trees

Draw the tree of calls. Count total work.

### How To Build a Recursion Tree

1. Root = the original call with its work
2. Children = the recursive calls made
3. Each node shows the **work done at that node** (excluding recursive calls)
4. Total work = sum of work across all nodes

### Example: Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # T(n/2)
    right = merge_sort(arr[mid:])    # T(n/2)
    return merge(left, right)         # O(n) work
```

Recurrence: `T(n) = 2T(n/2) + O(n)`

Recursion tree:

```
Level 0:            [n]                    work = n
                   /    \
Level 1:       [n/2]    [n/2]              work = n/2 + n/2 = n
                / \      / \
Level 2:    [n/4][n/4] [n/4][n/4]          work = 4 × n/4 = n
                ...
Level k:    [1][1][1]...[1]                work = n × 1 = n
```

- Each level does **O(n)** total work
- Number of levels = **log₂(n)** (halving each time until size 1)
- Total: **O(n) × O(log n) = O(n log n)**

### Example: Fibonacci

```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

Recurrence: `T(n) = T(n-1) + T(n-2) + O(1)`

Recursion tree:

```
Level 0:              fib(5)                    1 node
                     /      \
Level 1:        fib(4)      fib(3)              2 nodes
               /    \       /    \
Level 2:   fib(3) fib(2) fib(2) fib(1)         ~4 nodes
            ...
Level n:   fib(0), fib(1), ...                  ~2ⁿ nodes
```

- Each node does O(1) work
- Roughly 2ⁿ nodes (not exactly — left subtree is bigger than right)
- Total: **O(2ⁿ)**

More precisely, the exact count is related to the golden ratio: O(φⁿ) ≈ O(1.618ⁿ). But O(2ⁿ) is the standard approximation.

### Example: Binary Search

```python
def binary_search(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)
```

Recurrence: `T(n) = T(n/2) + O(1)` — only ONE recursive call.

```
Level 0:    [n]        work = O(1)
Level 1:    [n/2]      work = O(1)
Level 2:    [n/4]      work = O(1)
...
Level k:    [1]        work = O(1)
```

- O(1) work per level
- log₂(n) levels
- Total: **O(log n)**

---

## Method 2: Recurrence Relations

Express the time as a mathematical equation and solve it.

### Common Recurrences and Their Solutions

```
RECURRENCE                   SOLUTION            EXAMPLE
─────────────────────────────────────────────────────────────
T(n) = T(n-1) + O(1)        O(n)                Linear recursion (factorial)
T(n) = T(n-1) + O(n)        O(n²)               Selection sort recursive
T(n) = 2T(n/2) + O(1)       O(n)                Binary tree traversal
T(n) = 2T(n/2) + O(n)       O(n log n)          Merge sort
T(n) = 2T(n/2) + O(n²)      O(n²)               Bad divide and conquer
T(n) = T(n/2) + O(1)        O(log n)            Binary search
T(n) = T(n/2) + O(n)        O(n)                Quickselect average
T(n) = 2T(n-1) + O(1)       O(2ⁿ)              Fibonacci, Tower of Hanoi
T(n) = T(n-1) + T(n-2) + O(1) O(2ⁿ)            Fibonacci (more precise: O(φⁿ))
```

**Memorize this table.** When you see a recursive function, extract its recurrence, match it to this table, and read off the answer.

### How To Extract a Recurrence

1. **Identify the recursive calls.** How many? On what size input?
2. **Identify the non-recursive work.** What does the function do besides calling itself?
3. **Write the equation:** `T(n) = [number of calls] × T([sub-size]) + [non-recursive work]`

Example:

```python
def mystery(arr, left, right):
    if left >= right:
        return 0
    mid = (left + right) // 2
    count = 0
    for i in range(left, right + 1):   # O(n) work
        count += arr[i]
    left_result = mystery(arr, left, mid)      # T(n/2)
    right_result = mystery(arr, mid + 1, right) # T(n/2)
    return count + left_result + right_result
```

Recurrence: `T(n) = 2T(n/2) + O(n)` → from the table → **O(n log n)**

---

## Method 3: The Master Theorem

> **Governance (2026-07-09):** This section is **exposure / reference**, not Module 2 mastery credit. **Master Theorem is deferred to Module 3 (Searching & Sorting)** for `taught` → `complete` status. Module 2 owns recursion trees and recurrence *setup*; Module 3 owns full MT application on merge sort / quick sort. Do not mark MT `complete` from Recursion alone. See `Handoff Doc.md` §2G.

For recurrences of the form: **T(n) = aT(n/b) + O(nᶜ)**

Where:
- `a` = number of recursive calls
- `b` = factor by which input shrinks
- `c` = exponent of the non-recursive work

Compare `log_b(a)` with `c`:

```
CASE 1: If log_b(a) > c    →  T(n) = O(n^(log_b(a)))
        Recursion dominates. Many subproblems doing little work each.

CASE 2: If log_b(a) == c   →  T(n) = O(nᶜ × log n)
        Balanced. Equal work at each level.

CASE 3: If log_b(a) < c    →  T(n) = O(nᶜ)
        Root dominates. Non-recursive work overwhelms recursion.
```

### Applying To Known Algorithms

**Merge Sort:** `T(n) = 2T(n/2) + O(n)` → a=2, b=2, c=1
- log₂(2) = 1, c = 1 → Case 2 → **O(n log n)** ✅

**Binary Search:** `T(n) = T(n/2) + O(1)` → a=1, b=2, c=0
- log₂(1) = 0, c = 0 → Case 2 → **O(n⁰ × log n) = O(log n)** ✅

**Strassen Matrix Multiplication:** `T(n) = 7T(n/2) + O(n²)` → a=7, b=2, c=2
- log₂(7) ≈ 2.807, c = 2 → Case 1 → **O(n^2.807)** (better than O(n³) naive)

**Binary Tree Traversal:** `T(n) = 2T(n/2) + O(1)` → a=2, b=2, c=0
- log₂(2) = 1, c = 0 → Case 1 → **O(n)** ✅

### When The Master Theorem Doesn't Apply

- **Non-equal subproblems:** `T(n) = T(n/3) + T(2n/3) + O(n)` — subproblems aren't the same size
- **Non-polynomial work:** `T(n) = 2T(n/2) + O(n log n)` — work isn't O(nᶜ) form
- **Subtract instead of divide:** `T(n) = T(n-1) + O(n)` — this subtracts, doesn't divide by constant

For these, use recursion trees or substitution.

---

## Recursive Space Complexity — The Complete Picture

Recursive space = **max call stack depth × space per frame** + **any extra data structures**

### Rule: Space = Max Depth, Not Total Calls

```
           fib(5)
          /      \
      fib(4)    fib(3)
      /    \
  fib(3)  fib(2)
```

Total calls: ~2ⁿ. But the stack at any one moment holds only the frames along **one path** from root to leaf. Maximum depth = n.

**Space: O(n), not O(2ⁿ).**

The left subtree is fully explored (all frames pushed and popped) before the right subtree begins. So the maximum simultaneous frames = depth.

### Space Per Frame

Each frame holds the function's local variables:

```python
def func(arr, left, right):    # 3 parameters → O(1) per frame
    mid = (left + right) // 2  # 1 local variable → O(1)
    ...
```

If a frame creates O(n) data:

```python
def func(arr):
    copy = arr[:]              # O(n) data created in this frame!
    ...
```

Then space per frame is O(n), and total space = O(n) × depth.

### Complete Space Formula

```
Space = (max depth) × (space per frame) + (auxiliary structures)
```

Examples:

| Function | Max Depth | Space Per Frame | Auxiliary | Total Space |
|---|---|---|---|---|
| `factorial(n)` | O(n) | O(1) | None | **O(n)** |
| `fib(n)` (naive) | O(n) | O(1) | None | **O(n)** |
| `fib(n)` (memo) | O(n) | O(1) | O(n) memo dict | **O(n)** |
| `merge_sort(arr)` | O(log n) | O(n) slicing | O(n) merge result | **O(n log n)** or **O(n)** depending on implementation |
| `binary_search(arr)` | O(log n) | O(1) | None | **O(log n)** |

---

# PART 6: RECURSION VS ITERATION

## When To Use Recursion

| Use Recursion When | Why |
|---|---|
| Problem has **recursive structure** (trees, graphs, nested structures) | The code mirrors the data structure naturally |
| Problem involves **branching choices** (backtracking, subsets, permutations) | Recursion handles branching elegantly; iteration requires explicit stack |
| Divide and conquer (merge sort, quick sort) | Splitting and combining maps naturally to recursion |
| Problem definition is recursive ("solve for n using solution for n-1") | Direct translation of the mathematical definition |

## When To Use Iteration

| Use Iteration When | Why |
|---|---|
| Simple linear processing | A loop is simpler and clearer |
| Stack depth would be too large | Iteration avoids stack overflow |
| Performance-critical code | Function call overhead is eliminated |
| The recursive version is tail-recursive | Mechanically converts to a loop |

## Converting Recursion to Iteration

### Method 1: Tail Recursion → Loop (Already Shown)

Works when the recursive call is the last operation. Parameters become loop variables.

### Method 2: Explicit Stack

Any recursion can be converted to iteration using an **explicit stack.** The stack simulates the call stack.

```python
# Recursive DFS on tree
def inorder(node):
    if node is None:
        return
    inorder(node.left)
    print(node.val)
    inorder(node.right)

# Iterative with explicit stack
def inorder_iterative(root):
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        print(current.val)
        current = current.right
```

The explicit stack uses O(h) heap memory instead of O(h) stack memory. The advantage: heap memory is much larger than stack memory, so you can handle deeper structures.

We'll practice this extensively in Week 5 (Trees).

---

# PART 7: CLASSIC RECURSIVE PROBLEMS

These problems illustrate the patterns and build your recursive thinking muscle.

## Problem Type 1: Simple Linear Recursion

### Power Function

```python
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)
```

Time: O(n) where n = exp. Space: O(n).

**Optimized: Fast Exponentiation**

```python
def power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    else:
        return base * power(base, exp - 1)
```

Time: **O(log n)** — halves the exponent each time.
Space: O(log n).

Recurrence: `T(n) = T(n/2) + O(1)` → O(log n). Master theorem: a=1, b=2, c=0 → Case 2.

### String Reversal

```python
def reverse(s, left, right):
    if left >= right:
        return
    s[left], s[right] = s[right], s[left]
    reverse(s, left + 1, right - 1)
```

### Check Palindrome

```python
def is_palindrome(s, left=0, right=None):
    if right is None:
        right = len(s) - 1
    if left >= right:
        return True
    if s[left] != s[right]:
        return False
    return is_palindrome(s, left + 1, right - 1)
```

---

## Problem Type 2: Decision-Based Recursion (Subsets / Permutations)

### Generate All Subsets

At each element, make a **binary choice**: include it or exclude it.

```python
def subsets(arr):
    result = []
    
    def backtrack(index, current):
        if index == len(arr):
            result.append(current[:])    # Base case: made all decisions
            return
        
        # Choice 1: Include arr[index]
        current.append(arr[index])
        backtrack(index + 1, current)
        current.pop()                    # Undo choice (backtrack)
        
        # Choice 2: Exclude arr[index]
        backtrack(index + 1, current)
    
    backtrack(0, [])
    return result
```

For `arr = [1, 2, 3]`:

```
                         []
                  /               \
             [1]                    []
           /     \              /       \
       [1,2]    [1]          [2]        []
       /  \     /  \        /  \       /  \
  [1,2,3][1,2] [1,3][1]  [2,3][2]   [3]  []
```

Time: **O(n × 2ⁿ)** — 2ⁿ subsets, O(n) to copy each.
Space: **O(n)** for the recursion stack + O(n × 2ⁿ) for the output.

### Generate All Permutations

At each position, choose from the **remaining** unused elements.

```python
def permutations(arr):
    result = []
    
    def backtrack(start):
        if start == len(arr):
            result.append(arr[:])
            return
        
        for i in range(start, len(arr)):
            arr[start], arr[i] = arr[i], arr[start]   # Choose
            backtrack(start + 1)                        # Explore
            arr[start], arr[i] = arr[i], arr[start]   # Undo (backtrack)
    
    backtrack(0)
    return result
```

Time: **O(n × n!)** — n! permutations, O(n) to copy each.
Space: **O(n)** stack depth + O(n × n!) output.

### The Backtracking Template

Both subsets and permutations follow the same **backtracking** template:

```python
def backtrack(state):
    if is_complete(state):
        record(state)
        return
    
    for choice in available_choices(state):
        make_choice(choice)        # Modify state
        backtrack(state)           # Recurse
        undo_choice(choice)        # Restore state (BACKTRACK)
```

The key: **undo the choice** after exploring that branch. This restores the state for the next choice to explore a different branch. This is why it's called "backtracking" — you back up and try a different path.

We'll dive much deeper into backtracking in Week 9. For now, understand the recursive structure.

---

## Problem Type 3: Divide and Conquer

### Maximum Subarray (Divide and Conquer Version)

```python
def max_crossing_sum(arr, left, mid, right):
    # Maximum sum subarray that INCLUDES mid and mid+1
    left_sum = float('-inf')
    total = 0
    for i in range(mid, left - 1, -1):
        total += arr[i]
        left_sum = max(left_sum, total)
    
    right_sum = float('-inf')
    total = 0
    for i in range(mid + 1, right + 1):
        total += arr[i]
        right_sum = max(right_sum, total)
    
    return left_sum + right_sum

def max_subarray_dc(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    
    if left == right:
        return arr[left]
    
    mid = (left + right) // 2
    left_max = max_subarray_dc(arr, left, mid)
    right_max = max_subarray_dc(arr, mid + 1, right)
    cross_max = max_crossing_sum(arr, left, mid, right)
    
    return max(left_max, right_max, cross_max)
```

The max subarray is either entirely in the left half, entirely in the right half, or **crosses the midpoint.** We solve all three and take the maximum.

Recurrence: `T(n) = 2T(n/2) + O(n)` → **O(n log n)**

Note: Kadane's algorithm solves this in O(n). The D&C version is pedagogically important but not the optimal solution for this specific problem.

---

# PART 8: RECURSION ON DATA STRUCTURES (PREVIEW)

## Linked Lists (Week 4 Preview)

```python
def linked_list_sum(node):
    if node is None:
        return 0
    return node.val + linked_list_sum(node.next)

def reverse_linked_list(node):
    if node is None or node.next is None:
        return node
    new_head = reverse_linked_list(node.next)
    node.next.next = node
    node.next = None
    return new_head
```

## Trees (Week 5 Preview)

```python
def tree_sum(node):
    if node is None:
        return 0
    return node.val + tree_sum(node.left) + tree_sum(node.right)

def tree_height(node):
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))
```

## Graphs (Week 7 Preview)

```python
def dfs(graph, node, visited):
    if node in visited:
        return
    visited.add(node)
    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)
```

Every one of these follows the same recursive structure: base case → recursive call on smaller structure → combine results.

---

# PART 9: THE COMPLETE RECURSION RECIPE

```
╔════════════════════════════════════════════════════════════════╗
║                    THE RECURSION RECIPE                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  WRITING A RECURSIVE FUNCTION:                                 ║
║                                                                ║
║  1. DEFINE: What does this function do? (precise sentence)     ║
║  2. BASE CASE: Simplest input with direct answer               ║
║  3. RECURSIVE CASE: How to make the problem smaller            ║
║  4. COMBINE: How to use sub-result to solve current            ║
║  5. VERIFY: Does it always reach the base case?                ║
║                                                                ║
║  ANALYZING A RECURSIVE FUNCTION:                               ║
║                                                                ║
║  TIME:                                                         ║
║  1. Extract recurrence: T(n) = aT(n/b) + O(nᶜ)                 ║
║  2. Try Master Theorem: compare log_b(a) with c                ║
║  3. If Master doesn't apply: draw recursion tree               ║
║     - Count work per level                                     ║
║     - Count number of levels                                   ║
║     - Total = sum across levels                                ║
║  4. Or match to known recurrence table                         ║
║                                                                ║
║  SPACE:                                                        ║
║  1. Max recursion depth × space per frame                      ║
║  2. + any auxiliary data structures                            ║
║  3. Remember: depth ≠ total calls                              ║
║     (only one branch active at a time)                         ║
║                                                                ║
║  PATTERN MATCHING:                                             ║
║                                                                ║
║  Linear processing → Linear recursion (or just use a loop)     ║
║  Split in half + combine → Binary recursion / D&C              ║
║  Make choices at each step → Backtracking                      ║
║  Overlapping subproblems → Memoize (DP preview)                ║
║  Process tree/graph → Tree/graph recursion                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

# PART 10: COMMON RECURRENCES CHEAT SHEET

```
RECURRENCE                    SOLUTION        ALGORITHM
──────────────────────────────────────────────────────────────
T(n) = T(n-1) + O(1)         O(n)            Factorial, linear scan
T(n) = T(n-1) + O(n)         O(n²)           Selection sort, insertion sort
T(n) = 2T(n-1) + O(1)        O(2ⁿ)           Fibonacci naive, Tower of Hanoi
T(n) = T(n/2) + O(1)         O(log n)        Binary search
T(n) = T(n/2) + O(n)         O(n)            Quickselect average
T(n) = 2T(n/2) + O(1)        O(n)            Tree traversal
T(n) = 2T(n/2) + O(n)        O(n log n)      Merge sort, quicksort average
T(n) = 2T(n/2) + O(n²)       O(n²)           Bad divide and conquer
T(n) = 3T(n/2) + O(n)        O(n^1.585)      Karatsuba multiplication
T(n) = 7T(n/2) + O(n²)       O(n^2.807)      Strassen multiplication

MASTER THEOREM: T(n) = aT(n/b) + O(nᶜ)
  log_b(a) > c  →  O(n^(log_b(a)))    Recursion dominates
  log_b(a) = c  →  O(nᶜ log n)        Balanced
  log_b(a) < c  →  O(nᶜ)              Work dominates
```

---

# PART 11: TRACED EXEMPLARS (CAP = 3)

**Craft rule:** In-lesson solutions stop at **3** full traces. Rest → Retention + Spine + problem-bank.

Attempt blind. Answers for exemplars follow the prompts.

---

### Problem 1: Warm-Up — Sum of Digits

Write a recursive function that returns the sum of digits of a positive integer.

```
Input: 1234
Output: 10 (1 + 2 + 3 + 4)
```

---

### Problem 2: Power Function

Implement `power(base, exp)` that runs in **O(log n)** time using fast exponentiation.

```
Input: power(2, 10)
Output: 1024
```

Show the recurrence and prove it's O(log n).

---

### Problem 3: Recursive Binary Search

Implement binary search recursively. Return the index of the target, or -1.

```
Input: arr = [1, 3, 5, 7, 9, 11], target = 7
Output: 3
```

---


---

# ANSWER KEY — EXEMPLARS ONLY

# Problem 1: Sum of Digits

## Pattern Identification

**Pattern: Linear Recursion (Reduce by One Digit)**

Why? A number's digit sum = its last digit + the digit sum of the remaining number. We extract the last digit with `n % 10` and remove it with `n // 10`. Each recursive call shrinks the number by one digit until we reach the base case (single digit or 0).

## Solution

```python
def sum_of_digits(n):
    if n < 10:
        return n
    return (n % 10) + sum_of_digits(n // 10)
```

## How the Recursion Unfolds

```
sum_of_digits(1234)
= 4 + sum_of_digits(123)
= 4 + (3 + sum_of_digits(12))
= 4 + (3 + (2 + sum_of_digits(1)))
= 4 + (3 + (2 + 1))              ← base case: 1 < 10, return 1
= 4 + (3 + 3)
= 4 + 6
= 10 ✅
```

## Call Stack Visualization

```
sum_of_digits(1234)  — waiting for result
  sum_of_digits(123) — waiting for result
    sum_of_digits(12) — waiting for result
      sum_of_digits(1) — BASE CASE, returns 1
    returns 2 + 1 = 3
  returns 3 + 3 = 6
returns 4 + 6 = 10
```

Four frames on the stack simultaneously at maximum depth.

## Edge Cases

**Edge case 1: Single digit**
```
sum_of_digits(7)
7 < 10 → return 7 ✅ (base case immediately)
```

**Edge case 2: Zero**
```
sum_of_digits(0)
0 < 10 → return 0 ✅
```

**Edge case 3: Number with zeros in it**
```
sum_of_digits(1001)
= 1 + sum_of_digits(100)
= 1 + (0 + sum_of_digits(10))
= 1 + (0 + (0 + sum_of_digits(1)))
= 1 + (0 + (0 + 1))
= 2 ✅
```

## Complexity Analysis

**How many recursive calls?** Each call removes one digit. A number n has `⌊log₁₀(n)⌋ + 1` digits. Let d = number of digits.

**Time:** d calls, O(1) work each → **O(d) = O(log n)**

**Space:** Maximum call stack depth = d frames → **O(d) = O(log n)**

> **Time: O(log n), Space: O(log n)** where n is the number itself (not array length)

---

# Problem 2: Power Function (Fast Exponentiation)

## Pattern Identification

**Pattern: Divide and Conquer (Halving the Problem)**

Why? Naive recursion: `power(b, e) = b * power(b, e-1)` makes e recursive calls → O(n). But we can halve the exponent each time using the identity:

```
b^e = (b^(e/2))² if e is even
b^e = b × (b^(e/2))² if e is odd
```

We compute `b^(e/2)` **once**, then square it. This halves the problem each step → O(log n).

## Solution

```python
def power(base, exp):
    if exp == 0:
        return 1
    if exp == 1:
        return base

    half = power(base, exp // 2)

    if exp % 2 == 0:
        return half * half
    else:
        return base * half * half
```

## Why Compute `half` Once, Not Twice

```python
# WRONG — O(n) because two recursive calls per level
return power(base, exp // 2) * power(base, exp // 2)

# RIGHT — O(log n) because one recursive call per level
half = power(base, exp // 2)
return half * half
```

The wrong version creates a full binary tree of calls (2^(log n) = n total calls). The right version creates a single chain (log n calls).

## Trace Through Main Example

```
power(2, 10)
  exp=10 (even): half = power(2, 5)
    exp=5 (odd): half = power(2, 2)
      exp=2 (even): half = power(2, 1)
        exp=1: return 2              ← base case
      half=2, return 2*2 = 4
    half=4, return 2 * 4*4 = 32
  half=32, return 32*32 = 1024

return 1024 ✅
```

Only 4 recursive calls for exp=10.

## The Recurrence

```
T(n) = T(n/2) + O(1)
```

One recursive call of size n/2, plus O(1) work (multiplication).

**Solving by expansion:**
```
T(n) = T(n/2) + 1
     = T(n/4) + 1 + 1
     = T(n/8) + 1 + 1 + 1
     ...
     = T(1) + log₂(n)
     = O(log n)
```

**By Master Theorem:** a=1, b=2, f(n)=O(1). log_b(a) = log₂(1) = 0. f(n) = O(n⁰) = O(1). Case 2: **T(n) = O(log n).**

## Edge Cases

**Edge case 1: Exponent is 0**
```
power(5, 0) → return 1 ✅ (anything to the 0 is 1)
```

**Edge case 2: Exponent is 1**
```
power(5, 1) → return 5 ✅
```

**Edge case 3: Base is 0**
```
power(0, 5)
  half = power(0, 2)
    half = power(0, 1) → return 0
  return 0*0 = 0
return 0 * 0*0 = 0 ✅
```

## Complexity Analysis

**Time:** Recurrence T(n) = T(n/2) + O(1) → **O(log n)** where n = exp

**Space:** Call stack depth = log n levels → **O(log n)**

> **Time: O(log n), Space: O(log n)**

---

# Problem 3: Recursive Binary Search

## Pattern Identification

**Pattern: Divide and Conquer (Search Space Halving)**

Why? Binary search naturally maps to recursion: check the middle, then recurse on the left or right half. Each call halves the search space. The base case is when the search space is empty (left > right) or we find the target.

## Solution

```python
def binary_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)
```

## Trace Through Main Example

```
arr = [1, 3, 5, 7, 9, 11], target = 7

Call 1: left=0, right=5, mid=2
        arr[2]=5 < 7 → search right half

Call 2: left=3, right=5, mid=4
        arr[4]=9 > 7 → search left half

Call 3: left=3, right=3, mid=3
        arr[3]=7 == 7 → return 3 ✅
```

## Call Stack

```
binary_search(arr, 7, 0, 5)  — waiting
  binary_search(arr, 7, 3, 5) — waiting
    binary_search(arr, 7, 3, 3) — returns 3
  returns 3
returns 3
```

Three frames deep. Each return value bubbles straight up.

## Edge Cases

**Edge case 1: Target not found**
```
arr = [1, 3, 5], target = 4
Call 1: left=0, right=2, mid=1, arr[1]=3 < 4 → right half
Call 2: left=2, right=2, mid=2, arr[2]=5 > 4 → left half
Call 3: left=2, right=1, left > right → return -1 ✅
```

**Edge case 2: Single element, found**
```
arr = [5], target = 5
Call 1: left=0, right=0, mid=0, arr[0]=5 == 5 → return 0 ✅
```

**Edge case 3: Target at first position**
```
arr = [1, 3, 5, 7, 9], target = 1
mid=2: 5>1 → left half
mid=0: 1==1 → return 0 ✅
```

## Complexity Analysis

**Recurrence:** T(n) = T(n/2) + O(1)

Same as fast exponentiation. Each call does O(1) work and recurses on half the input.

**Time: O(log n)**

**Space:** Call stack depth. Each call halves the problem → log n levels deep → **O(log n)**

This is why iterative binary search is sometimes preferred — it's O(1) space vs O(log n) for recursive.

> **Time: O(log n), Space: O(log n)**

---


---

## Rest of the old in-lesson bank

Drill via Retention Questions + `Practice Spines/Phase A MVP Spines.md` + `problem-bank/`. Do not paste full solutions back into this lesson.

## Teach-back

Explain the core frameworks from earlier parts without notes, then open Retention (questions-only).

