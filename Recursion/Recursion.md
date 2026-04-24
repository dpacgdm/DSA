# RECURSION — THE COMPLETE LESSON

---

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

# PART 11: TEST PROBLEMS

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

### Problem 4: Generate All Subsets

Given an array of **unique** integers, return all possible subsets.

```
Input: [1, 2, 3]
Output: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
```

---

### Problem 5: Generate All Permutations

Given an array of **unique** integers, return all possible permutations.

```
Input: [1, 2, 3]
Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

---

### Problem 6: Flatten Nested List

Given a nested list of integers, flatten it to a single-level list.

```
Input: [1, [2, [3, 4], 5], [6, 7]]
Output: [1, 2, 3, 4, 5, 6, 7]
```

---

### Problem 7: Tower of Hanoi

Move n disks from source peg to target peg using an auxiliary peg. Only one disk can be moved at a time. A larger disk cannot be placed on a smaller disk.

Print each move. Return the total number of moves.

```
Input: n = 3
Output: 7 moves
  Move disk 1 from A to C
  Move disk 2 from A to B
  Move disk 1 from C to B
  Move disk 3 from A to C
  Move disk 1 from B to A
  Move disk 2 from B to C
  Move disk 1 from A to C
```

Show the recurrence and prove the number of moves is 2ⁿ - 1.

---

### Problem 8: Merge Sort

Implement merge sort. Show the full complexity analysis using the recurrence and recursion tree.

```
Input: [38, 27, 43, 3, 9, 82, 10]
Output: [3, 9, 10, 27, 38, 43, 82]
```

---

### Problem 9: Complexity Analysis Challenge

What is the time and space complexity of this function? Show your work using recursion tree or recurrence.

```python
def mystery(n):
    if n <= 1:
        return 1
    return mystery(n // 3) + mystery(n // 3) + mystery(n // 3)
```

---

### Problem 10: The Boss — Letter Combinations of a Phone Number

Given a string containing digits 2-9, return all possible letter combinations that the number could represent (like on a phone keypad).

```
Mapping:
2 → "abc", 3 → "def", 4 → "ghi", 5 → "jkl"
6 → "mno", 7 → "pqrs", 8 → "tuv", 9 → "wxyz"

Input: "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

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

# Problem 4: Generate All Subsets

## Pattern Identification

**Pattern: Include/Exclude Recursion (Decision Tree)**

Why? For each element, we have exactly **two choices**: include it in the current subset, or don't. n elements × 2 choices each = 2ⁿ total subsets. The recursion tree is a binary tree where the left branch includes the element and the right branch excludes it.

## Solution

```python
def subsets(nums):
    result = []

    def backtrack(index, current):
        if index == len(nums):
            result.append(current[:])    # append a COPY
            return

        # Choice 1: Include nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()                    # undo (backtrack)

        # Choice 2: Exclude nums[index]
        backtrack(index + 1, current)

    backtrack(0, [])
    return result
```

## Why `current[:]` and Not `current`

Lists are **mutable** and passed **by reference**. If we do `result.append(current)`, every entry in result points to the **same list object**. As we modify `current` later, all previously appended entries change too. `current[:]` creates a **copy** frozen at this moment.

## Why `current.pop()` (Backtracking)

After exploring the "include" branch, we need to undo the inclusion before exploring the "exclude" branch. Without the pop, `current` would accumulate elements incorrectly.

## Decision Tree

```
                        []
                       /   \
                   [1]       []
                  /   \     /   \
             [1,2]   [1]  [2]    []
             /  \    / \   / \   / \
         [1,2,3][1,2][1,3][1][2,3][2][3][]
```

Leaves (bottom row) are the 2³ = 8 subsets.

## Trace Through Main Example

```
nums = [1, 2, 3]

backtrack(0, [])
├─ include 1: backtrack(1, [1])
│  ├─ include 2: backtrack(2, [1,2])
│  │  ├─ include 3: backtrack(3, [1,2,3]) → APPEND [1,2,3]
│  │  └─ exclude 3: backtrack(3, [1,2])   → APPEND [1,2]
│  └─ exclude 2: backtrack(2, [1])
│     ├─ include 3: backtrack(3, [1,3])   → APPEND [1,3]
│     └─ exclude 3: backtrack(3, [1])     → APPEND [1]
└─ exclude 1: backtrack(0, [])
   ├─ include 2: backtrack(2, [2])
   │  ├─ include 3: backtrack(3, [2,3])   → APPEND [2,3]
   │  └─ exclude 3: backtrack(3, [2])     → APPEND [2]
   └─ exclude 2: backtrack(2, [])
      ├─ include 3: backtrack(3, [3])     → APPEND [3]
      └─ exclude 3: backtrack(3, [])      → APPEND []

result = [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]] ✅
```

## Edge Cases

**Edge case 1: Empty array**
```
nums = []
backtrack(0, []) → index==0==len([]) → append [] → result = [[]]
return [[]] ✅ (the empty set is the only subset)
```

**Edge case 2: Single element**
```
nums = [5]
backtrack(0, [])
├─ include 5: backtrack(1, [5]) → append [5]
└─ exclude 5: backtrack(1, []) → append []
result = [[5], []] ✅
```

## Complexity Analysis

**Time:**

How many recursive calls? The decision tree is a complete binary tree of depth n. Total nodes = 2⁰ + 2¹ + ... + 2ⁿ = 2ⁿ⁺¹ - 1 = **O(2ⁿ)** calls.

But we also copy `current` at each leaf. There are 2ⁿ leaves. Each copy is at most O(n) (subset can have up to n elements).

Total: O(2ⁿ) calls × O(1) non-leaf work + O(2ⁿ) leaves × O(n) copy work = **O(n × 2ⁿ)**

**Space:**

- Call stack depth: n levels → O(n)
- `current`: at most n elements → O(n)
- `result`: 2ⁿ subsets, average size n/2 → O(n × 2ⁿ) total
- Auxiliary space (excluding output): **O(n)** (stack + current)

> **Time: O(n × 2ⁿ), Space: O(n × 2ⁿ)** total
> **Auxiliary space (excluding output): O(n)**

---

# Problem 5: Generate All Permutations

## Pattern Identification

**Pattern: Swap-Based Backtracking**

Why? A permutation is a rearrangement using ALL elements. At position 0, we can place any of the n elements. At position 1, any of the remaining n-1. And so on. This gives n! total permutations.

The approach: for each position `start`, try swapping it with every position from `start` to `n-1`. Recurse to fill the next position. Then swap back (backtrack).

## Solution

```python
def permutations(nums):
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]   # choose
            backtrack(start + 1)                            # explore
            nums[start], nums[i] = nums[i], nums[start]    # unchoose

    backtrack(0)
    return result
```

## Why Swap Instead of "Used" Array?

An alternative approach uses a `used[]` boolean array and builds a separate `current` list. The swap approach is more elegant — it rearranges `nums` in-place, avoiding extra data structures. Both produce the same result.

## Decision Tree

```
                    [1, 2, 3]
                  /     |      \
            [1,2,3]  [2,1,3]  [3,2,1]     (swap pos 0 with 0,1,2)
            /   \     /   \     /   \
       [1,2,3][1,3,2][2,1,3][2,3,1][3,2,1][3,1,2]  (swap pos 1 with 1,2)
```

Branching factor: position 0 has n choices, position 1 has n-1, ... → n! leaves.

## Trace Through Main Example

```
nums = [1, 2, 3]

backtrack(0):
  i=0: swap(0,0) → [1,2,3]
    backtrack(1):
      i=1: swap(1,1) → [1,2,3]
        backtrack(2):
          i=2: swap(2,2) → [1,2,3]
            backtrack(3) → APPEND [1,2,3]
          swap back → [1,2,3]
        swap back → [1,2,3]
      i=2: swap(1,2) → [1,3,2]
        backtrack(2):
          i=2: swap(2,2) → [1,3,2]
            backtrack(3) → APPEND [1,3,2]
          swap back → [1,3,2]
        swap back → [1,2,3]
    swap back → [1,2,3]

  i=1: swap(0,1) → [2,1,3]
    backtrack(1):
      i=1: [2,1,3] → APPEND [2,1,3]
      i=2: swap(1,2) → [2,3,1] → APPEND [2,3,1]
    swap back → [1,2,3]

  i=2: swap(0,2) → [3,2,1]
    backtrack(1):
      i=1: [3,2,1] → APPEND [3,2,1]
      i=2: swap(1,2) → [3,1,2] → APPEND [3,1,2]
    swap back → [1,2,3]

result = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,2,1],[3,1,2]] ✅
```

## Edge Cases

**Edge case 1: Single element**
```
nums = [1]
backtrack(0): i=0 swap(0,0) → backtrack(1) → append [1]
result = [[1]] ✅
```

**Edge case 2: Two elements**
```
nums = [1, 2]
backtrack(0):
  i=0: [1,2] → backtrack(1): i=1: append [1,2]
  i=1: swap → [2,1] → backtrack(1): i=1: append [2,1]
result = [[1,2], [2,1]] ✅ (2! = 2 permutations)
```

## Complexity Analysis

**Time:**

Total permutations = n!. For each permutation, we copy the array → O(n).

But we also need to count the total work in the recursion tree:
- Level 0: 1 node, each does n iterations of the for loop
- Level 1: n nodes, each does n-1 iterations
- Level 2: n×(n-1) nodes, each does n-2 iterations
- ...
- Level n-1: n! nodes, each does 1 iteration

Total work (excluding copies): n + n(n-1) + n(n-1)(n-2) + ... + n! 

This is dominated by the last term: **O(n × n!)**

Including the copy at each leaf: n! leaves × O(n) per copy → O(n × n!)

**Total time: O(n × n!)**

**Space:**

- Call stack depth: n levels → O(n)
- `result`: n! permutations, each of size n → O(n × n!)
- Auxiliary (excluding output): **O(n)**

> **Time: O(n × n!), Space: O(n × n!)** total
> **Auxiliary space: O(n)**

---

# Problem 6: Flatten Nested List

## Pattern Identification

**Pattern: Structural Recursion (Recurse on Structure)**

Why? The input has a recursive structure — lists can contain integers OR other lists, nested arbitrarily deep. We process each element: if it's an integer, add it to the result. If it's a list, recursively flatten it.

## Solution

```python
def flatten(nested):
    result = []

    def helper(item):
        if isinstance(item, list):
            for element in item:
                helper(element)
        else:
            result.append(item)

    helper(nested)
    return result
```

## How the Recursion Unfolds

```
flatten([1, [2, [3, 4], 5], [6, 7]])

helper([1, [2, [3, 4], 5], [6, 7]])    ← is a list, iterate elements
  helper(1)                              ← not a list, append 1
  helper([2, [3, 4], 5])                 ← is a list, iterate
    helper(2)                            ← append 2
    helper([3, 4])                       ← is a list, iterate
      helper(3)                          ← append 3
      helper(4)                          ← append 4
    helper(5)                            ← append 5
  helper([6, 7])                         ← is a list, iterate
    helper(6)                            ← append 6
    helper(7)                            ← append 7

result = [1, 2, 3, 4, 5, 6, 7] ✅
```

## Call Stack at Deepest Point

```
helper([1, [2, [3, 4], 5], [6, 7]])     ← frame 1
  helper([2, [3, 4], 5])                 ← frame 2
    helper([3, 4])                        ← frame 3
      helper(3)                           ← frame 4 (max depth)
```

Four frames deep — equal to the maximum nesting depth + 1.

## Edge Cases

**Edge case 1: Already flat**
```
flatten([1, 2, 3])
helper([1,2,3]) → helper(1), helper(2), helper(3) → all append
result = [1, 2, 3] ✅
```

**Edge case 2: Deeply nested single element**
```
flatten([[[[[5]]]]])
helper([[[[[5]]]]]) → helper([[[[5]]]]) → helper([[[5]]]) → helper([[5]]) → helper([5]) → helper(5) → append 5
result = [5] ✅
```

**Edge case 3: Empty nested lists**
```
flatten([1, [], [2, []], 3])
helper(1) → append 1
helper([]) → iterate 0 elements → nothing
helper([2, []]) → helper(2) → append 2, helper([]) → nothing
helper(3) → append 3
result = [1, 2, 3] ✅
```

## Complexity Analysis

Let n = total number of integers in the structure, d = maximum nesting depth.

**Time:** Every element (integer or list) is visited exactly once. Total visits = total nodes in the nested structure. If there are n integers and some number of list wrappers, total visits ≤ n + (number of sublists). In the worst case: **O(n + number of sublists)** = **O(total elements)**.

Simplifying: **O(n)** where n = total number of items in the structure at all levels.

**Space:**
- Call stack: proportional to maximum nesting depth → **O(d)**
- `result`: n integers → **O(n)**
- Auxiliary (excluding output): **O(d)**

> **Time: O(n), Space: O(n + d)**
> Where n = total number of integers, d = max nesting depth

---

# Problem 7: Tower of Hanoi

## Pattern Identification

**Pattern: Recursive Decomposition into Subproblems**

Why? Moving n disks seems complex, but it decomposes beautifully:
1. Move the top n-1 disks from source to auxiliary (using target as temporary)
2. Move the bottom disk from source to target (one move)
3. Move the n-1 disks from auxiliary to target (using source as temporary)

The base case: n=1, just move the single disk directly.

## Solution

```python
def hanoi(n, source='A', target='C', auxiliary='B'):
    if n == 0:
        return 0

    # Step 1: Move top n-1 disks from source to auxiliary
    moves = hanoi(n - 1, source, auxiliary, target)

    # Step 2: Move the bottom disk from source to target
    print(f"Move disk {n} from {source} to {target}")
    moves += 1

    # Step 3: Move n-1 disks from auxiliary to target
    moves += hanoi(n - 1, auxiliary, target, source)

    return moves
```

## Trace Through n=3

```
hanoi(3, A, C, B)
├─ hanoi(2, A, B, C)                    ← move top 2 from A to B
│  ├─ hanoi(1, A, C, B)                 ← move top 1 from A to C
│  │  ├─ hanoi(0, A, B, C) → 0
│  │  ├─ Print: "Move disk 1 from A to C"
│  │  └─ hanoi(0, B, C, A) → 0
│  │  return 1
│  ├─ Print: "Move disk 2 from A to B"
│  └─ hanoi(1, C, B, A)                 ← move top 1 from C to B
│     ├─ hanoi(0, ...) → 0
│     ├─ Print: "Move disk 1 from C to B"
│     └─ hanoi(0, ...) → 0
│     return 1
│  return 3
├─ Print: "Move disk 3 from A to C"
└─ hanoi(2, B, C, A)                    ← move top 2 from B to C
   ├─ hanoi(1, B, A, C)
   │  Print: "Move disk 1 from B to A"
   │  return 1
   ├─ Print: "Move disk 2 from B to C"
   └─ hanoi(1, A, C, B)
      Print: "Move disk 1 from A to C"
      return 1
   return 3
return 7

Output:
  Move disk 1 from A to C
  Move disk 2 from A to B
  Move disk 1 from C to B
  Move disk 3 from A to C
  Move disk 1 from B to A
  Move disk 2 from B to C
  Move disk 1 from A to C
Total: 7 moves ✅
```

## The Recurrence and Proof That Moves = 2ⁿ - 1

**Recurrence:**
```
T(0) = 0
T(n) = T(n-1) + 1 + T(n-1) = 2T(n-1) + 1
```

**Solving by expansion:**
```
T(n) = 2T(n-1) + 1
     = 2(2T(n-2) + 1) + 1 = 4T(n-2) + 2 + 1
     = 4(2T(n-3) + 1) + 2 + 1 = 8T(n-3) + 4 + 2 + 1
     ...
     = 2^k × T(n-k) + (2^(k-1) + 2^(k-2) + ... + 1)
```

When k = n: T(n-k) = T(0) = 0:
```
T(n) = 2^n × 0 + (2^(n-1) + 2^(n-2) + ... + 1)
     = 2^(n-1) + 2^(n-2) + ... + 1
     = 2^n - 1
```

**Verification:** T(3) = 2³ - 1 = 7 ✅

## Edge Cases

**Edge case 1: n = 0**
```
No disks to move. return 0 ✅
```

**Edge case 2: n = 1**
```
hanoi(1, A, C, B)
  hanoi(0) → 0
  Print: "Move disk 1 from A to C"
  hanoi(0) → 0
return 1 = 2¹ - 1 ✅
```

## Complexity Analysis

**Time:** T(n) = 2T(n-1) + O(1). As proved above: **T(n) = 2ⁿ - 1 = O(2ⁿ)**

Total calls in the recursion tree: each call spawns 2 children, depth is n → 2⁰ + 2¹ + ... + 2ⁿ = 2ⁿ⁺¹ - 1 ≈ O(2ⁿ) calls. Each does O(1) work. Confirmed: **O(2ⁿ)**.

**Space:** Maximum call stack depth = n (one call per level, each reducing n by 1) → **O(n)**

> **Time: O(2ⁿ), Space: O(n)**

---

# Problem 8: Merge Sort

## Pattern Identification

**Pattern: Divide and Conquer (Split, Recurse, Merge)**

Why? Merge sort splits the array in half, recursively sorts each half, then merges the two sorted halves. The merge step is where the real work happens — combining two sorted arrays into one sorted array in O(n) time.

## Solution

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

    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result
```

## Why `<=` Instead of `<` in the Merge

Using `<=` makes the sort **stable** — equal elements maintain their original relative order. The left half's elements came first in the original array, so we keep them first when equal.

## Trace Through Main Example

```
merge_sort([38, 27, 43, 3, 9, 82, 10])

Split: [38, 27, 43]  and  [3, 9, 82, 10]

Left half: merge_sort([38, 27, 43])
  Split: [38] and [27, 43]
  [38] → base case, return [38]
  merge_sort([27, 43])
    Split: [27] and [43]
    [27] → return [27]
    [43] → return [43]
    merge([27], [43]) → [27, 43]
  merge([38], [27, 43]) → [27, 38, 43]

Right half: merge_sort([3, 9, 82, 10])
  Split: [3, 9] and [82, 10]
  merge_sort([3, 9])
    Split: [3] and [9]
    merge([3], [9]) → [3, 9]
  merge_sort([82, 10])
    Split: [82] and [10]
    merge([82], [10]) → [10, 82]
  merge([3, 9], [10, 82]) → [3, 9, 10, 82]

Final merge: merge([27, 38, 43], [3, 9, 10, 82])
  i=0,j=0: 27 vs 3 → 3.   result=[3]
  i=0,j=1: 27 vs 9 → 9.   result=[3,9]
  i=0,j=2: 27 vs 10 → 10.  result=[3,9,10]
  i=0,j=3: 27 vs 82 → 27.  result=[3,9,10,27]
  i=1,j=3: 38 vs 82 → 38.  result=[3,9,10,27,38]
  i=2,j=3: 43 vs 82 → 43.  result=[3,9,10,27,38,43]
  remaining: [82].          result=[3,9,10,27,38,43,82]

return [3, 9, 10, 27, 38, 43, 82] ✅
```

## The Recurrence and Recursion Tree Proof

**Recurrence:**
```
T(n) = 2T(n/2) + O(n)
```

Two recursive calls, each on half the input. The merge step scans all n elements → O(n) work.

**Recursion Tree:**

```
Level 0:        [n]                    → n work (one merge of size n)
Level 1:      [n/2] [n/2]             → n work (two merges of size n/2)
Level 2:    [n/4][n/4][n/4][n/4]      → n work (four merges of size n/4)
...
Level log n: [1][1][1]...[1]          → n work (n "merges" of size 1)
```

**Each level does O(n) total work. There are log₂(n) levels.**

Total: **O(n) × O(log n) = O(n log n)**

**By Master Theorem:** a=2, b=2, f(n)=O(n). log_b(a) = log₂(2) = 1. f(n) = O(n¹). Case 2: **T(n) = O(n log n).**

## Edge Cases

**Edge case 1: Already sorted**
```
[1, 2, 3] → still O(n log n), merge sort doesn't benefit from pre-sorting
```

**Edge case 2: Single element**
```
[5] → len ≤ 1 → return [5] ✅
```

**Edge case 3: Two elements, reversed**
```
[2, 1] → split [2] and [1], merge → [1, 2] ✅
```

## Complexity Analysis

**Time:** As proved: **O(n log n)** — this is true for ALL inputs (best, worst, average case). Merge sort has no bad inputs.

**Space:**
- Each level creates new arrays for left, right, and result
- At any one time, the total memory for one merge path through the tree:
  - The current level's slices and merge result
  - All parent frames waiting on the stack
- The slices `arr[:mid]` and `arr[mid:]` create O(n) new elements per level
- Stack depth: O(log n)
- Total extra space: **O(n)** (dominated by the merge arrays; at each level the arrays sum to n, and garbage collection frees completed levels)

> **Time: O(n log n), Space: O(n)**

---

# Problem 9: Mystery Function — Complexity Analysis

```python
def mystery(n):
    if n <= 1:
        return 1
    return mystery(n // 3) + mystery(n // 3) + mystery(n // 3)
```

## Step 1: Understand What It Does

Each call makes **3 recursive calls**, each with input **n/3**. Base case when n ≤ 1. Each call does O(1) work besides the recursive calls (just addition and return).

## Step 2: Write the Recurrence

```
T(n) = 3T(n/3) + O(1)
```

## Step 3: Solve Using Recursion Tree

```
Level 0:           T(n)                     → 1 node, O(1) work each = O(1)
Level 1:      T(n/3) T(n/3) T(n/3)         → 3 nodes, O(1) each = O(3)
Level 2:  T(n/9) × 9                        → 9 nodes, O(1) each = O(9)
Level 3:  T(n/27) × 27                      → 27 nodes, O(1) each = O(27)
...
Level k:  3^k nodes, each with input n/3^k  → O(3^k) work
```

**How many levels?** We stop when n/3^k ≤ 1, i.e., 3^k ≥ n, i.e., k = log₃(n).

**Total work:**
```
= 3⁰ + 3¹ + 3² + ... + 3^(log₃ n)
= (3^(log₃(n) + 1) - 1) / (3 - 1)
= (3 × n - 1) / 2
= O(n)
```

Because 3^(log₃ n) = n.

**So the total work is O(n).**

## Step 4: Verify Using Master Theorem

```
T(n) = 3T(n/3) + O(1)
a = 3, b = 3, f(n) = O(1)
```

log_b(a) = log₃(3) = **1**

f(n) = O(1) = O(n⁰)

Compare: n^(log_b(a)) = n¹ = n. f(n) = O(1) = O(n^(1-ε)) for ε=1.

**Case 1 of Master Theorem:** f(n) = O(n^(log_b(a) - ε))

Therefore: **T(n) = O(n^(log_b(a))) = O(n¹) = O(n)**

## Step 5: Space Complexity

**Call stack depth:** Each level divides by 3. Depth = log₃(n) = **O(log n)**.

At any point, only ONE path from root to leaf is on the stack (the other branches haven't been called yet or have already returned). So maximum simultaneous frames = depth = O(log n).

Each frame stores O(1) local data.

**Space: O(log n)**

## Important Observation

This function computes `3 × mystery(n // 3)` in O(n) time. If we simply wrote:

```python
def mystery_optimized(n):
    if n <= 1:
        return 1
    return 3 * mystery_optimized(n // 3)
```

This would be T(n) = T(n/3) + O(1) = **O(log n)** time instead of O(n). The original version does redundant work by computing `mystery(n//3)` three times instead of once — the same trap as the naive Fibonacci recursion.

> **Time: O(n), Space: O(log n)**

---

# Problem 10: Letter Combinations of a Phone Number

## Pattern Identification

**Pattern: Multi-Way Branching Recursion (Cartesian Product)**

Why? For each digit, we have 3 or 4 letter choices. We need ALL combinations — every possible way to pick one letter per digit. This is a Cartesian product built via recursion: at each position (digit), we branch into every possible letter for that digit, then recurse to the next position.

This is similar to subsets/permutations, but the branching factor varies per level (3 or 4 depending on the digit).

## Solution

```python
def letter_combinations(digits):
    if not digits:
        return []

    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = []

    def backtrack(index, current):
        if index == len(digits):
            result.append("".join(current))
            return

        for letter in phone[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

## Why `"".join(current)` Instead of String Concatenation

We build `current` as a list of characters (append/pop is O(1)). At the leaf, we join once. If we used string concatenation throughout, each level would create a new string copy — much less efficient.

## Decision Tree for "23"

```
                        ""
                  /     |     \
                "a"    "b"    "c"         ← digit '2' → "abc"
              / | \   / | \   / | \
            ad ae af bd be bf cd ce cf    ← digit '3' → "def"
```

3 × 3 = 9 leaves = 9 combinations.

## Trace Through Main Example

```
digits = "23"
phone['2'] = "abc", phone['3'] = "def"

backtrack(0, [])
├─ letter='a': current=['a']
│  backtrack(1, ['a'])
│  ├─ letter='d': current=['a','d'] → backtrack(2) → append "ad"
│  ├─ letter='e': current=['a','e'] → backtrack(2) → append "ae"
│  └─ letter='f': current=['a','f'] → backtrack(2) → append "af"
│
├─ letter='b': current=['b']
│  backtrack(1, ['b'])
│  ├─ letter='d' → append "bd"
│  ├─ letter='e' → append "be"
│  └─ letter='f' → append "bf"
│
└─ letter='c': current=['c']
   backtrack(1, ['c'])
   ├─ letter='d' → append "cd"
   ├─ letter='e' → append "ce"
   └─ letter='f' → append "cf"

result = ["ad","ae","af","bd","be","bf","cd","ce","cf"] ✅
```

## Edge Cases

**Edge case 1: Empty string**
```
digits = ""
Guard clause returns [] ✅
```

**Edge case 2: Single digit**
```
digits = "2"
backtrack(0, [])
├─ 'a' → backtrack(1) → append "a"
├─ 'b' → backtrack(1) → append "b"
└─ 'c' → backtrack(1) → append "c"
result = ["a", "b", "c"] ✅
```

**Edge case 3: Digit with 4 letters**
```
digits = "7"
phone['7'] = "pqrs" → 4 branches
result = ["p", "q", "r", "s"] ✅
```

**Edge case 4: All 4-letter digits**
```
digits = "79"
phone['7'] = "pqrs" (4), phone['9'] = "wxyz" (4)
Total = 4 × 4 = 16 combinations ✅
```

## Complexity Analysis

**STEP 1:** `digits` → n = len(digits). Let m = maximum letters per digit (m=4 for digits 7 and 9, m=3 for others).

**Time:**

The recursion tree:
- Level 0: 1 node, branches into 3 or 4 children
- Level 1: 3-4 nodes, each branches into 3-4 children
- ...
- Level n: total leaves

In the **worst case** (all digits are 7 or 9, each having 4 letters):
- Total leaves = 4ⁿ
- At each leaf, we do `"".join(current)` which is O(n)
- Total leaf work: O(n × 4ⁿ)

Internal node work: each non-leaf node does O(1) work (loop overhead, append, pop). Total internal nodes < total leaves. Dominated by leaf work.

**Total time: O(n × 4ⁿ)**

More precisely: O(n × m^n) where m is the max branching factor.

**Space:**

- Call stack depth: n levels → O(n)
- `current`: at most n characters → O(n)
- `result`: up to 4ⁿ strings, each of length n → **O(n × 4ⁿ)**
- Auxiliary (excluding output): **O(n)**

> **Time: O(n × 4ⁿ), Space: O(n × 4ⁿ)** total
> **Auxiliary space: O(n)**

### Why This Complexity Is Acceptable

For phone numbers, n is at most ~10-15 digits. 4¹⁰ = ~1 million, 4¹⁵ = ~1 billion. For typical interview constraints (n ≤ 10), this is fast enough. There's no way to avoid generating all combinations since the problem asks for ALL of them — the output size itself is O(n × 4ⁿ), so the algorithm is **output-optimal.**
