# BIG O & COMPLEXITY ANALYSIS — THE COMPLETE LESSON

---

# PART 1: WHY BIG O EXISTS

When you write code, your computer performs **operations.** An operation is any single unit of work:

- Assigning a value: `x = 5` → 1 operation
- Comparing two things: `x > 3` → 1 operation
- Adding numbers: `x + y` → 1 operation
- Accessing an index: `arr[0]` → 1 operation
- Returning something: `return x` → 1 operation

Now imagine two solutions to the same problem. Both are correct. But one does 100 operations and the other does 10 billion. On a small input, you won't notice. On a large input, one finishes instantly and the other takes hours.

Computer scientists needed a **universal language** to describe how algorithms behave as input grows. Not exact time in seconds because that depends on your machine, your language, your operating system. They needed something **machine-independent.**

That language is **Big O Notation.**

**Big O answers one question:**

> "As my input grows toward infinity, how does the number of operations grow?"

It doesn't care about small inputs. It doesn't care about your specific machine. It cares about the **shape of growth.**

---

## What "Shape of Growth" Means

O(2n) and O(n) are both **straight lines** on a graph. One is steeper but they're both lines. Big O treats them as the same because the **shape** is identical: linear.

O(n²) is a **curve.** It's a fundamentally different shape from a line. No matter how steep your line is, eventually the curve overtakes it.

**Big O captures shape, not steepness.** That's why we drop constants. Constants change steepness. They don't change shape. O(5n) is still a line. O(100n) is still a line. O(n²) is always a curve.

---

## The Three Simplification Rules

**Rule 1: Drop Constants**

O(3n) → **O(n)**
O(500) → **O(1)**
O(n/2) → **O(n)**

Same shape regardless of the multiplier.

**Rule 2: Drop Non-Dominant Terms**

O(n² + n) → **O(n²)**
O(n + log n) → **O(n)**
O(2ⁿ + n³) → **O(2ⁿ)**

At massive scale, the biggest term **devours** the smaller ones. When n = 1,000,000: n² = 1,000,000,000,000. The extra n = 1,000,000 is a rounding error.

**Rule 3: Different Inputs = Different Variables**

```python
def work(arr1, arr2):
```

`arr1` and `arr2` are **independent.** You cannot call both "n." What if arr1 has 5 elements and arr2 has 5 million? Use separate variables: a = len(arr1), b = len(arr2).

---

## The Complexity Family — Ranked Slowest to Fastest

```
O(1)         — Constant        🟢  Fixed work regardless of input
O(log n)     — Logarithmic     🟢  Grows incredibly slowly
O(√n)        — Square Root     🟢  Between log and linear
O(n)         — Linear          🟡  Proportional to input
O(n log n)   — Linearithmic    🟡  Slightly worse than linear
O(n√n)       — n Square Root   🟠  Between n log n and n²
O(n²)        — Quadratic       🟠  Nested work over input
O(n³)        — Cubic           🔴  Triple nested work
O(2ⁿ)        — Exponential     🔴  Doubles with each new element
O(n!)        — Factorial       💀  Multiplies with each new element
```

**The full chain to memorize:**

```
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n√n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

Quick comparison to make this concrete. When n = 1,000,000:

```
O(1)         = 1
O(log n)     = ~20
O(√n)        = 1,000
O(n)         = 1,000,000
O(n log n)   = ~20,000,000
O(n²)        = 1,000,000,000,000
O(2ⁿ)        = a number with 300,000 digits
```

---

## Why Log Base Doesn't Matter

When we write O(log n), we don't specify a base. Base 2? Base 10? It doesn't matter.

```
log₂(n) = log₁₀(n) / log₁₀(2)
```

`log₁₀(2)` is a constant (~0.301). Changing log bases just multiplies by a constant. We drop constants.

So O(log₂ n) = O(log₁₀ n) = O(ln n) = **O(log n).**

In CS, people **mentally** think log₂ because we deal with halving and doubling. But the Big O is the same regardless.

---

## Best Case, Worst Case, Average Case

Big O technically describes an **upper bound.** But algorithms can behave differently depending on the input.

```python
def find_element(arr, target):
    for num in arr:
        if num == target:
            return True
    return False
```

- **Best case (Ω — Omega):** Target is the first element. O(1).
- **Worst case (O — Big O):** Target is last or not present. O(n).
- **Average case (Θ — Theta):** On average, check half. O(n/2) = O(n).

**The default in interviews and this course: we analyze WORST CASE unless stated otherwise.**

Why this matters practically:

| Algorithm | Average Case | Worst Case |
|---|---|---|
| Hash table lookup | O(1) | O(n) due to collisions |
| Quicksort | O(n log n) | O(n²) with bad pivot |
| Binary search | O(log n) | O(log n) |

If an interviewer asks *"What's the worst case of your hash map approach?"* and you only know "hash map is O(1)," you'll be exposed. The correct answer: **"O(1) average, O(n) worst case due to hash collisions, but in practice with a good hash function, collisions are rare."**

---

## Amortized Complexity

You'll learn that Python's `list.append()` is O(1). That's actually a **simplification.** Here's the full truth.

Python lists use **dynamic arrays.** When the internal array is full and you append:

1. Python allocates a **new, bigger array** (roughly 2x the size)
2. **Copies all existing elements** to the new array → O(n) work
3. Adds your new element

So occasionally, append is O(n). But these expensive operations happen so **rarely** that averaged over many appends, the cost per operation is O(1).

This is called **amortized O(1).** "Amortized" means "averaged over a sequence of operations."

Analogy: You pay $1,200 rent monthly. Once a year you pay a $2,400 repair bill. Any single month might spike, but your amortized monthly cost is ~$1,400. Predictable on average.

**In interviews:** Saying "append is O(1)" is acceptable. Saying "append is amortized O(1) due to dynamic array resizing" is impressive.

---

## Practical Constraints Table

In competitive programming and interviews, problems give input size constraints. These tell you **what complexity your solution must be:**

```
n ≤ 10          → O(n!) is fine
n ≤ 20          → O(2ⁿ) is fine
n ≤ 500         → O(n³) is fine
n ≤ 5,000       → O(n²) is fine
n ≤ 100,000     → O(n log n) is needed
n ≤ 1,000,000   → O(n) is needed
n ≤ 10⁸         → O(n) barely works
```

**Memorize this.** When you see "1 ≤ n ≤ 10⁵" in a problem, your brain should instantly say: "I need O(n log n) or better."

---

## Real World Use Cases

**Amazon:** Searching 350 million products. O(n) scans 350 million items in seconds. O(log n) binary search checks ~28 items in microseconds. O(n²) does 10¹⁴ operations and crashes the server.

**Google Maps:** Finding shortest route across millions of road segments. Dijkstra's algorithm is O((V+E) log V). A brute force O(V!) approach checking every possible path would take longer than the age of the universe.

**System Design:** Designing a feed for 1 billion users. O(n) vs O(n log n) at that scale is the difference between 100 servers and 3,000 servers. That's millions of dollars in infrastructure costs.

---

# PART 2: THE PYTHON OPERATIONS CHEAT SHEET

Before we learn to analyze code, you must know the **cost of individual Python operations.** Without this, you will miscalculate every time.

```
OPERATION                          TIME          WHY
──────────────────────────────────────────────────────────────
VARIABLES & MATH
  x = 5                          O(1)          Simple assignment
  x + y, x * y, x // y           O(1)          Arithmetic
  x > y, x == y                  O(1)          Comparison
  return x                       O(1)          Return value

LISTS
  arr[i]                         O(1)          Direct index access
  arr[i] = x                     O(1)          Direct index assignment
  arr.append(x)                  O(1)*         Amortized — see above
  arr.pop()                      O(1)          Removes from END
  arr.pop(0)                    ⚠️ O(n)        Removes from FRONT, shifts everything
  arr.insert(0, x)              ⚠️ O(n)        Inserts at FRONT, shifts everything
  arr.insert(i, x)              ⚠️ O(n)        Shifts elements after position i
  x in arr                      ⚠️ O(n)        Scans ENTIRE list
  arr.remove(x)                 ⚠️ O(n)        Finds + shifts
  arr.copy()                    ⚠️ O(n)        Copies every element
  arr[a:b]                      ⚠️ O(b-a)      Creates new list of that slice
  len(arr)                       O(1)           Stored internally
  arr.sort()                    ⚠️ O(n log n)  Timsort algorithm
  sorted(arr)                   ⚠️ O(n log n)  Creates sorted copy
  min(arr), max(arr)            ⚠️ O(n)        Must scan entire list

SETS
  x in my_set                    O(1)*         Hash lookup (average)
  my_set.add(x)                  O(1)*         Hash insertion (average)
  my_set.remove(x)               O(1)*         Hash deletion (average)

DICTIONARIES
  d[key]                         O(1)*         Hash lookup (average)
  d[key] = val                   O(1)*         Hash insertion (average)
  key in d                       O(1)*         Hash lookup (average)

STRINGS
  s + t                          ⚠️ O(n)        Creates ENTIRELY new string
  s[i]                           O(1)          Index access
  len(s)                         O(1)          Stored internally
  "".join(list_of_strings)       O(total)      Total length of all strings
  s[a:b]                        ⚠️ O(b-a)      Creates new string

* = amortized average case, O(n) worst case
```

### The Critical Python Trap: String Concatenation

```python
def build_string(arr):
    result = ""
    for word in arr:          # n iterations
        result = result + word    # O(len(result)) EACH TIME
```

Each `+` creates a **brand new string** and copies everything. As result grows, each concatenation costs more. The total work is 1 + 2 + 3 + ... + n = **O(n²).**

**The fix:**

```python
def build_string(arr):
    return "".join(arr)       # O(total length) = O(n)
```

This appears in interviews **constantly.** Python strings are **immutable.** Every concatenation creates a new object.

---

# PART 3: THE COMPLETE FRAMEWORK FOR TIME COMPLEXITY

## The Six Sub-Skills

```
Skill 1: Identifying your inputs and labeling sizes
Skill 2: Analyzing single operations
Skill 3: Analyzing ALL types of loops
Skill 4: Analyzing sequential blocks (ADD)
Skill 5: Analyzing nested loops (MULTIPLY) including dependent bounds
Skill 6: Analyzing what's INSIDE a loop (hidden costs, branches, function calls)
```

---

## Skill 1: Identifying Inputs

Before analyzing anything, answer: **What are the inputs and what letters represent their sizes?**

| Code Signature | Labels |
|---|---|
| `def f(arr):` | n = len(arr) |
| `def f(arr1, arr2):` | a = len(arr1), b = len(arr2) |
| `def f(n):` | n is already a number |
| `def f(s):` (string) | n = len(s) |
| `def f(grid):` (2D) | r = rows, c = columns |

**Always do this first. Write it down. No exceptions.**

---

## Skill 2: Single Operations

Any fixed number of O(1) operations is O(1). It doesn't matter if there are 3 lines or 50 lines, as long as none depend on the input size.

```python
x = arr[0]          # O(1)
y = arr[1]          # O(1)
z = x + y           # O(1)
w = z * 2           # O(1)
flag = w > 100      # O(1)
return flag          # O(1)
```

Six operations. O(6) = **O(1).**

**But check each operation against the cheat sheet.** If any single line is secretly expensive, it's not O(1):

```python
x = arr[0]              # O(1) ✅
y = sorted(arr)         # O(n log n) ⚠️ NOT O(1)
z = arr.copy()          # O(n) ⚠️ NOT O(1)
```

---

## Skill 3: Analyzing ALL Types of Loops

For any loop, the question is: **How many times does it iterate relative to the input?**

### Pattern A: Standard Linear Loop

```python
for i in range(n):      # Runs n times
    print(i)
```

n iterations. **O(n).**

### Pattern B: Fixed Iteration Loop

```python
for i in range(100):    # Runs 100 times, always
    print(i)
```

100 is a constant. Input doesn't matter. **O(1).**

### Pattern C: Linear Step Loop

```python
i = 0
while i < n:
    print(i)
    i += 3              # Steps by 3
```

Runs n/3 times. O(n/3) = **O(n).** Any constant step size is still linear. The step just changes the constant, which we drop.

### Pattern D: Halving Loop

```python
i = n
while i > 0:
    print(i)
    i = i // 2
```

Trace with n = 32: i goes 32 → 16 → 8 → 4 → 2 → 1 → 0. That's 6 iterations.

How many times can you halve n before hitting 0? **log₂(n).** Total: **O(log n).**

### Pattern E: Doubling Loop

```python
i = 1
while i < n:
    print(i)
    i = i * 2
```

i goes 1 → 2 → 4 → 8 → 16... until reaching n. How many doublings to reach n? **log₂(n).** Total: **O(log n).**

### Pattern F: Multiplying by Any Constant

```python
i = 1
while i < n:
    print(i)
    i = i * 3          # Triples each time
```

i goes 1 → 3 → 9 → 27 → 81... Reaches n in log₃(n) steps. But O(log₃ n) = **O(log n)** because log bases don't matter.

**General rule: If the loop variable is MULTIPLIED or DIVIDED by a constant each iteration → O(log n).**

### Pattern G: Squaring Loop

```python
i = 2
while i < n:
    print(i)
    i = i * i           # Squares each time
```

Trace with n = 10000: i goes 2 → 4 → 16 → 256 → 65536 (> 10000, stop).

That's only 4 iterations for n = 10000. This grows as **O(log log n).** Why? After k iterations, i = 2^(2^k). We stop when 2^(2^k) ≥ n, so 2^k ≥ log n, so k ≥ log(log n).

This is rare but appears in advanced problems.

### The General Method When Confused

**When you can't identify the pattern, TRACE IT:**

1. Pick a specific n (like 16 or 100)
2. Write out every value of the loop variable
3. Count iterations
4. Try a bigger n (like 1000)
5. See how the count scales
6. Match to a known pattern

---

## Skill 4: Sequential Blocks — ADD

When blocks of code appear one after another, **add** their complexities.

```python
def func(arr):
    # Block 1: O(1)
    x = arr[0]
    y = arr[1]

    # Block 2: O(n)
    for num in arr:
        print(num)

    # Block 3: O(n log n)
    arr.sort()

    # Block 4: O(n)
    for num in arr:
        print(num)

    # Block 5: O(1)
    return x + y
```

Total: O(1) + O(n) + O(n log n) + O(n) + O(1) = O(n log n + 2n + 2) = **O(n log n).**

The n log n dominates everything else.

**With different inputs:**

```python
def func(arr1, arr2):
    for x in arr1:        # O(a)
        print(x)
    for y in arr2:        # O(b)
        print(y)
```

Total: **O(a + b).** Cannot simplify further. They are independent.

---

## Skill 5: Nested Loops — MULTIPLY

When a loop is **inside** another loop, **multiply** their iteration counts.

**Why multiply?** Because the outer loop runs some number of times, and **for EACH of those times**, the inner loop runs its full count.

### Basic Nesting — Same Input

```python
for i in range(n):           # n times
    for j in range(n):       # n times each
        print(i, j)          # O(1)
```

n × n × O(1) = **O(n²).**

Trace with n = 3:
```
i=0: j=0,1,2  → 3 operations
i=1: j=0,1,2  → 3 operations
i=2: j=0,1,2  → 3 operations
Total: 9 = 3²
```

Three levels: **O(n³).** Four levels: **O(n⁴).** And so on.

### Nesting With Different Inputs

```python
for x in arr1:               # a times
    for y in arr2:           # b times each
        print(x, y)
```

a × b = **O(a × b).** NOT O(n²).

### Dependent Inner Bounds — Type 1: Inner Grows

```python
for i in range(n):
    for j in range(i):       # j depends on i
        print(i, j)
```

Trace with n = 5:
```
i=0: j runs 0 times  → 0
i=1: j runs 1 time   → 1
i=2: j runs 2 times  → 2
i=3: j runs 3 times  → 3
i=4: j runs 4 times  → 4
Total: 0+1+2+3+4 = 10
```

General: 0 + 1 + 2 + ... + (n-1) = **n(n-1)/2 = n²/2 - n/2 → O(n²).**

### Dependent Inner Bounds — Type 2: Inner Shrinks

```python
for i in range(n):
    for j in range(i, n):    # starts at i, goes to n
        print(i, j)
```

Trace with n = 4:
```
i=0: j runs 4 times → 4
i=1: j runs 3 times → 3
i=2: j runs 2 times → 2
i=3: j runs 1 time  → 1
Total: 4+3+2+1 = 10
```

Same sum, different order. Still **O(n²).**

**General rule: If the inner loop's bound changes linearly with the outer variable, and you're summing something like 1+2+3+...+n, it's always O(n²).**

### Dependent Inner Bounds — Type 3: The Harmonic Pattern

```python
for i in range(1, n + 1):
    for j in range(0, n, i):      # step size is i
        print(j)
```

This is trickier. The inner loop runs n/i times for each i:

```
i=1: inner runs n/1 = n times
i=2: inner runs n/2 times
i=3: inner runs n/3 times
...
i=n: inner runs n/n = 1 time
```

Total: n/1 + n/2 + n/3 + ... + n/n = n × (1 + 1/2 + 1/3 + ... + 1/n)

The sum (1 + 1/2 + 1/3 + ... + 1/n) is the **harmonic series** ≈ ln(n).

Total: **O(n log n).**

This pattern appears in problems involving divisors, the Sieve of Eratosthenes, and certain graph algorithms.

### The Technique For Any Dependent Nesting

When the inner bound depends on the outer variable and you can't recognize the pattern:

1. Write out the work done for each iteration of the outer loop
2. Sum it up
3. Recognize the series (arithmetic → O(n²), harmonic → O(n log n), constant → O(n))

---

## Skill 6: What's INSIDE the Loop

**This is where most people get destroyed.** The real formula is:

> **Total = (number of iterations) × (cost per iteration)**

If cost per iteration is O(1), easy. But you must CHECK every single line inside against the cheat sheet.

### Hidden Linear Operations

```python
for i in range(n):
    if arr[i] in some_list:       # ⚠️ "in" on LIST is O(n)
        print("found")
```

You see one `for` keyword. But `x in list` scans the entire list. That's a hidden second loop.

Total: n × O(n) = **O(n²).**

Compare with:

```python
for i in range(n):
    if arr[i] in some_set:        # ✅ "in" on SET is O(1)
        print("found")
```

Same looking code. Total: n × O(1) = **O(n).** Completely different.

### Hidden O(n) String Operations

```python
result = ""
for word in words:               # n iterations
    result = result + word        # ⚠️ O(len(result)) each time
```

Each concatenation copies the entire existing string into a new one. As result grows: 1 + 2 + 3 + ... + n = **O(n²).**

### Sorting Inside a Loop

```python
for i in range(n):
    arr.sort()                    # ⚠️ O(n log n) EACH iteration
```

Total: n × O(n log n) = **O(n² log n).**

### Slicing Inside a Loop

```python
for i in range(n):
    sub = arr[0:i]                # ⚠️ O(i) — creates new list
    print(sub)
```

Total: O(0) + O(1) + O(2) + ... + O(n-1) = **O(n²).**

### Function Calls Inside a Loop

```python
def helper(arr):
    total = 0
    for num in arr:               # O(n)
        total += num
    return total

def main(arr):
    for i in range(len(arr)):     # O(n)
        print(helper(arr))        # helper is O(n) per call
```

**Always analyze the called function FIRST.** Get its complexity. Then multiply.

Total: n × O(n) = **O(n²).**

### Conditional Branches Inside Loops

```python
for i in range(n):
    if some_condition:
        x += 1                    # O(1)
    else:
        for j in range(n):       # O(n)
            print(j)
```

The two branches have different costs: O(1) vs O(n).

**Rule: For worst case analysis, assume the most expensive branch ALWAYS executes.**

Worst case: the else branch runs every iteration. Total: n × O(n) = **O(n²).**

However, if you can **prove** a branch only runs a limited number of times, you can use that:

```python
for i in range(n):
    if i == 0:                    # Only true ONCE
        for j in range(n):       # O(n), but runs only once total
            print(j)
    else:
        x += 1                   # O(1), runs n-1 times
```

Total: O(n) + O(n-1) = **O(n).** The expensive branch only triggers once.

**When in doubt: take the worst branch. Only refine if you can mathematically prove the expensive branch is limited.**

---

# PART 4: THE COMPLETE FRAMEWORK FOR SPACE COMPLEXITY

**We only count EXTRA memory your code creates. The input itself doesn't count.**

## Step 1: List Every Variable and Data Structure

Go through the code line by line. Write down everything that's created.

## Step 2: Classify Each One

**Fixed (O(1)):** Single numbers, booleans, pointers, characters. These don't grow with input. Even 50 such variables is still O(1).

```python
x = 0
y = 0
temp = ""
flag = True
count = 0
# ALL of this together is O(1)
```

**Growing (O(something)):** Lists, sets, dictionaries, strings that **accumulate elements.**

```python
result = []
for num in arr:
    result.append(num * 2)    # result grows to n elements → O(n)
```

## Step 3: Determine Worst Case Size for Each Growing Structure

Ask: "In the worst case, how many elements can this hold?"

```python
seen = set()
for num in arr:
    seen.add(num)
# Worst case: every element is unique → n elements → O(n)
```

```python
matrix = []
for i in range(n):
    row = [0] * n
    matrix.append(row)
# n rows × n columns → O(n²)
```

## Step 4: Handle Multiple Structures

**From the same input:**

```python
seen = set()          # grows to at most n
result = []           # grows to at most n
```

O(n) + O(n) = O(2n) = **O(n).** Same input bounds both.

**From different inputs:**

```python
copy1 = list(arr1)    # O(a)
copy2 = list(arr2)    # O(b)
```

**O(a + b).** Different inputs, different variables.

## Step 5: The Call Stack — The Hidden Space Cost

**This is critical and most people miss it.**

Every function call goes onto the **call stack.** Each call creates a **stack frame** that holds its local variables. Recursive functions stack these frames up.

```python
def count_down(n):
    if n == 0:
        return
    count_down(n - 1)
```

When you call count_down(5):

```
Frame: count_down(5) — waiting
  Frame: count_down(4) — waiting
    Frame: count_down(3) — waiting
      Frame: count_down(2) — waiting
        Frame: count_down(1) — waiting
          Frame: count_down(0) — returns
        resumes and returns
      resumes and returns
    resumes and returns
  resumes and returns
resumes and returns
```

**6 frames in memory simultaneously.** For count_down(n), that's n+1 frames. **O(n) space** just from the call stack, even though the code creates no lists, sets, or arrays.

**Rule: Maximum depth of recursion = call stack space.**

We'll drill this extensively when we reach Recursion. For now, know it exists: **recursive calls cost space.**

---

# PART 5: RECURSIVE TIME COMPLEXITY — INTRODUCTION

I'm introducing this now so there are no gaps, but we will **master** it when we cover Recursion as a topic.

Loops repeat work **iteratively.** Recursion repeats work by **calling itself.** You can't use the loop counting method. You need a different tool.

### Linear Recursion

```python
def sum_array(arr, i=0):
    if i == len(arr):
        return 0
    return arr[i] + sum_array(arr, i + 1)
```

The function calls itself n times (once per element), doing O(1) work each call.

Time: **O(n).** Space: **O(n)** from the call stack.

### Branching Recursion

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

Each call makes **two** more calls. This creates a tree of calls:

```
                    fib(5)
                   /      \
              fib(4)      fib(3)
             /    \       /    \
         fib(3)  fib(2) fib(2) fib(1)
         /   \
     fib(2) fib(1)
```

The tree has roughly 2ⁿ nodes. Time: **O(2ⁿ).** Space: **O(n)** (maximum depth of the tree = call stack depth).

### The General Principle

For recursion, ask:
1. **How many total calls are made?** → gives time
2. **What's the maximum depth?** → gives stack space
3. **How much work per call?** → multiply with total calls

We'll learn formal tools (recurrence relations, recursion trees, the Master Theorem) when we cover recursion and divide-and-conquer sorting.

---

# PART 6: CODE EXAMPLES OF EACH COMPLEXITY CLASS

So you can recognize what O(2ⁿ) and O(n!) code actually looks like:

### O(1) — Constant

```python
def get_middle(arr):
    return arr[len(arr) // 2]
```

### O(log n) — Logarithmic

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Each iteration cuts the search space in half.

### O(n) — Linear

```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

### O(n log n) — Linearithmic

```python
def sort_and_process(arr):
    arr.sort()                    # O(n log n)
    for num in arr:               # O(n)
        print(num)
# Total: O(n log n) dominates
```

### O(n²) — Quadratic

```python
def print_all_pairs(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            print(arr[i], arr[j])
```

### O(2ⁿ) — Exponential

```python
def all_subsets(arr, index=0, current=[]):
    if index == len(arr):
        print(current)
        return
    all_subsets(arr, index + 1, current + [arr[index]])  # include
    all_subsets(arr, index + 1, current)                  # exclude
```

Each element: 2 choices (include or exclude). n elements → 2ⁿ paths.

### O(n!) — Factorial

```python
def all_permutations(arr, start=0):
    if start == len(arr):
        print(arr)
        return
    for i in range(start, len(arr)):
        arr[start], arr[i] = arr[i], arr[start]
        all_permutations(arr, start + 1)
        arr[start], arr[i] = arr[i], arr[start]
```

First position: n choices. Second: n-1. Third: n-2. Total: n! paths.

---

# PART 7: HOW TO COMMUNICATE COMPLEXITY IN AN INTERVIEW

Knowing the analysis isn't enough. You must **say it correctly.**

### When To State It

1. **After explaining your approach, BEFORE coding:** *"This approach will be O(n log n) time, O(n) space. Should I proceed?"*
2. **After coding, when asked:** Walk through the analysis block by block.

### How To Walk Through It Verbally

> *"The outer loop runs n times. Inside, I'm doing a set lookup which is O(1). So that block is O(n). Then the sort is O(k log k) where k is the size of the result set. Overall: O(n + k log k). Worst case, k approaches n, so O(n log n). Space is O(n) for the hash set."*

Short. Block by block. State the final answer.

### How To Handle "Can You Do Better?"

This means your complexity isn't good enough. Use the constraints table to figure out the target:

- Your solution is O(n²) and n can be 10⁵? They want O(n log n) or O(n).
- Your solution is O(n log n)? They might want O(n).

Then think about what data structure or technique gets you there.

### Discussing Tradeoffs

When you present a solution, **proactively** mention:

> *"We could also do this in O(n²) time with O(1) space if memory is a constraint. The hash set approach gives us O(n) time but uses O(n) space. Depends on whether we're optimizing for time or memory."*

This is what separates senior-level thinking from junior-level.

---

# PART 8: THE COMPLETE RECIPE

Your step-by-step machine for analyzing **any** code:

```
╔══════════════════════════════════════════════════════════════╗
║                    THE COMPLEXITY RECIPE                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STEP 1: IDENTIFY INPUTS                                     ║
║    - What are the inputs?                                    ║
║    - Label their sizes (n, a, b, r, c, etc.)                 ║
║    - Different inputs → different variables                  ║
║                                                              ║
║  STEP 2: BREAK INTO BLOCKS                                   ║
║    - Separate code into sequential chunks                    ║
║    - A chunk = single operation / loop / nested loop /       ║
║      function call                                           ║
║                                                              ║
║  STEP 3: ANALYZE EACH BLOCK                                  ║
║    For each block:                                           ║
║    a) If single operation(s) → check cheat sheet → likely    ║
║       O(1) unless it's sort/search/copy/slice                ║
║    b) If a loop → how many iterations?                       ║
║       - Linear (i++) → O(n)                                  ║
║       - Constant step (i+=3) → O(n)                          ║
║       - Halving/doubling/multiplying → O(log n)              ║
║       - Squaring → O(log log n)                              ║
║       - Fixed count → O(1)                                   ║
║    c) Check INSIDE the loop:                                 ║
║       - Every line against the cheat sheet                   ║
║       - Any function calls? → analyze function first         ║
║       - Any branches? → take worst case branch               ║
║         (unless you can PROVE the expensive branch is        ║
║          limited)                                            ║
║       - Multiply: iterations × cost per iteration            ║
║    d) If nested loops → multiply loop counts                 ║
║       - Same input nested → likely O(n²)                     ║
║       - Different inputs nested → O(a × b)                   ║
║       - Dependent bounds → trace and sum                     ║
║       - Harmonic pattern (step = i) → O(n log n)             ║
║    e) If recursion → count total calls × work per call       ║
║                                                              ║
║  STEP 4: COMBINE BLOCKS                                      ║
║    - Sequential blocks → ADD                                 ║
║    - Simplify: drop constants, drop non-dominant terms       ║
║    - Keep different input variables separate                 ║
║                                                              ║
║  STEP 5: ANALYZE SPACE                                       ║
║    - Ignore input (don't count it)                           ║
║    - List every extra variable and data structure            ║
║    - Fixed variables (int, bool, etc.) → O(1)                ║
║    - Growing structures → how large in worst case?           ║
║    - Don't forget the CALL STACK for recursion               ║
║    - Add up all growing ones, simplify                       ║
║                                                              ║
║  STEP 6: STATE ANSWER                                        ║
║    - "Time: O(___), Space: O(___)"                           ║
║    - Give worst case                                         ║
║    - Mention tradeoffs if relevant                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

# PART 9: TESTING — 8 PROBLEMS, ESCALATING DIFFICULTY

**Rules:**
- Show ALL steps of the recipe for each problem
- Don't skip steps even if the answer seems obvious
- For each problem, give both Time AND Space complexity

---

### Problem 1: Warm-Up

```python
def func(arr):
    x = arr[0]
    y = arr[-1]
    return x + y
```

---

### Problem 2: Single Loop

```python
def func(n):
    i = 1
    while i < n:
        print(i)
        i *= 3
```

---

### Problem 3: Sequential Blocks With a Trap

```python
def func(arr):
    result = []
    for num in arr:
        result.append(num * 2)

    result.sort()

    text = ""
    for num in result:
        text = text + str(num)

    return text
```

---

### Problem 4: Conditional Branches Inside a Loop

```python
def func(arr, threshold):
    output = []
    for i in range(len(arr)):
        if arr[i] > threshold:
            output.append(arr[i])
        else:
            for j in range(len(arr)):
                output.append(arr[i] + arr[j])
    return output
```

---

### Problem 5: Different Inputs With Nested Operations

```python
def func(names, blocked):
    blocked_set = set(blocked)
    result = []
    for name in names:
        if name not in blocked_set:
            result.append(name)
    result.sort()
    return result
```

---

### Problem 6: Function Call Inside a Loop

```python
def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def func(matrix):
    count = 0
    for row in matrix:
        if is_sorted(row):
            count += 1
    return count
```

---

### Problem 7: Dependent Nesting With Inner Work

```python
def func(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        for j in range(i, n):
            sub = arr[i:j+1]
            total += sum(sub)
    return total
```

---

### Problem 8: The Boss — Large Multi-Block Function

```python
def analyze_orders(orders, vip_list, min_amount):
    # Block 1
    vips = set(vip_list)

    # Block 2
    totals = {}
    for order in orders:
        uid = order["user_id"]
        amt = order["amount"]
        if uid in vips:
            if uid not in totals:
                totals[uid] = 0
            totals[uid] += amt

    # Block 3
    qualified = []
    for uid in totals:
        if totals[uid] >= min_amount:
            qualified.append(uid)

    # Block 4
    qualified.sort()

    # Block 5
    report = ""
    for uid in qualified:
        report = report + uid + ": " + str(totals[uid]) + "\n"

    return report
```

---

**Take your time. Follow the recipe mechanically for every single problem. Show all work. I will grade ruthlessly.**

**When you're done, I'll also know exactly where your understanding is strong and where it's still shaky. That determines whether we move to Day 2 or drill again.**

# Problem 1: Warm-Up

```python
def func(arr):
    x = arr[0]
    y = arr[-1]
    return x + y
```

**STEP 1: Identify Inputs**
- `arr` → n = len(arr)

**STEP 2: Break Into Blocks**
- One block: three single operations

**STEP 3: Analyze Each Block**
- `arr[0]` → direct index access → O(1)
- `arr[-1]` → direct index access → O(1)
- `x + y` → arithmetic → O(1)
- `return` → O(1)
- Block total: O(1)

**STEP 4: Combine**
- Only one block. **O(1).**

**STEP 5: Space**
- `x` → single variable → O(1)
- `y` → single variable → O(1)
- No growing structures.
- Total extra space: **O(1)**

**STEP 6: Answer**
> **Time: O(1), Space: O(1)**

---

# Problem 2: Single Loop

```python
def func(n):
    i = 1
    while i < n:
        print(i)
        i *= 3
```

**STEP 1: Identify Inputs**
- `n` → n is already a number. The input IS n.

**STEP 2: Break Into Blocks**
- Block 1: `i = 1` → single operation
- Block 2: the while loop

**STEP 3: Analyze Each Block**

*Block 1:* Assignment → O(1)

*Block 2:*
- Loop variable `i` is **multiplied by 3** each iteration
- i goes: 1 → 3 → 9 → 27 → 81 → ... until i ≥ n
- After k iterations: i = 3^k. We stop when 3^k ≥ n → k = log₃(n)
- This is the "multiplying by a constant" pattern → **O(log n)**
- Inside: `print(i)` → O(1). `i *= 3` → O(1). Cost per iteration: O(1)
- Block 2 total: O(log n) × O(1) = **O(log n)**

**STEP 4: Combine**
O(1) + O(log n) = **O(log n)**

**STEP 5: Space**
- `i` → single variable → O(1)
- No growing structures. No recursion.
- Total extra space: **O(1)**

**STEP 6: Answer**
> **Time: O(log n), Space: O(1)**

---

# Problem 3: Sequential Blocks With a Trap

```python
def func(arr):
    result = []
    for num in arr:
        result.append(num * 2)

    result.sort()

    text = ""
    for num in result:
        text = text + str(num)

    return text
```

**STEP 1: Identify Inputs**
- `arr` → n = len(arr)

**STEP 2: Break Into Blocks**
- Block 1: Build `result` list (the loop)
- Block 2: `result.sort()`
- Block 3: Build `text` string (the loop)
- Block 4: `return text`

**STEP 3: Analyze Each Block**

*Block 1:*
- Loop runs **n** times
- Inside: `num * 2` → O(1). `result.append(...)` → O(1) amortized.
- Block 1 total: **O(n)**

*Block 2:*
- `result.sort()` → result has n elements → **O(n log n)**

*Block 3:* ⚠️ **THE TRAP**
- Loop runs **n** times
- Inside: `text = text + str(num)` → string concatenation
- `str(num)` → O(1) (converting a single number to string, fixed-length)
- `text + str(num)` → ⚠️ **creates a brand new string**, copies all of `text` plus the new piece
- As `text` grows, each concatenation costs O(len(text))
- Iteration 1: text has ~length 1 → copy ~1 characters
- Iteration 2: text has ~length 2 → copy ~2 characters
- ...
- Iteration n: text has ~length n → copy ~n characters
- Total: 1 + 2 + 3 + ... + n = **n(n-1)/2 → O(n²)**

*Block 4:* `return text` → O(1)

**STEP 4: Combine**
O(n) + O(n log n) + O(n²) + O(1)

Drop non-dominant terms: O(n²) dominates everything.

**O(n²)**

**STEP 5: Space**
- `result` → list that grows to n elements → **O(n)**
- `text` → string that grows to hold all numbers → worst case **O(n)** total characters (assuming bounded digit numbers; more precisely O(total characters), but bounded by n × max_digits, which scales as O(n))
- `num` → single variable → O(1)
- Total extra space: O(n) + O(n) = **O(n)**

**STEP 6: Answer**
> **Time: O(n²), Space: O(n)**

The string concatenation trap turns what looks like O(n log n) code into O(n²). The fix: `text = "".join(str(num) for num in result)` → O(n) instead of O(n²), making the overall time O(n log n) with the sort dominating.

---

# Problem 4: Conditional Branches Inside a Loop

```python
def func(arr, threshold):
    output = []
    for i in range(len(arr)):
        if arr[i] > threshold:
            output.append(arr[i])
        else:
            for j in range(len(arr)):
                output.append(arr[i] + arr[j])
    return output
```

**STEP 1: Identify Inputs**
- `arr` → n = len(arr)
- `threshold` → a single number, not a collection. Does not contribute a size variable.

**STEP 2: Break Into Blocks**
- Block 1: The outer for loop (contains everything)
- Block 2: `return output`

**STEP 3: Analyze Each Block**

*Block 1:*
- Outer loop runs **n** times
- Inside there's a conditional branch. Two paths:
  - **If branch:** `output.append(arr[i])` → O(1)
  - **Else branch:** inner loop runs **n** times, each doing `output.append(arr[i] + arr[j])` → O(1) per iteration → **O(n)** per else execution

- **Worst case analysis:** assume the expensive branch (else) fires **every** iteration. We cannot prove it's limited without knowing `threshold`.
- Worst case: every element ≤ threshold → else runs all n times
- Each else execution: O(n)
- Total: n × O(n) = **O(n²)**

*Block 2:* O(1)

**STEP 4: Combine**
O(n²) + O(1) = **O(n²)**

**STEP 5: Space**
- `output` → this is the key. In the worst case (else branch fires every iteration), each of the n outer iterations appends n elements. Total elements in output: **n × n = n²**
- `i`, `j` → O(1)
- Total extra space: **O(n²)**

**STEP 6: Answer**
> **Time: O(n²), Space: O(n²)**

---

# Problem 5: Different Inputs With Nested Operations

```python
def func(names, blocked):
    blocked_set = set(blocked)
    result = []
    for name in names:
        if name not in blocked_set:
            result.append(name)
    result.sort()
    return result
```

**STEP 1: Identify Inputs**
- `names` → **a = len(names)**
- `blocked` → **b = len(blocked)**
- Two independent inputs. Two variables.

**STEP 2: Break Into Blocks**
- Block 1: `blocked_set = set(blocked)`
- Block 2: The for loop building `result`
- Block 3: `result.sort()`
- Block 4: `return result`

**STEP 3: Analyze Each Block**

*Block 1:*
- `set(blocked)` iterates through all b elements, inserting each → **O(b)**

*Block 2:*
- Loop runs **a** times (once per name)
- Inside: `name not in blocked_set` → set lookup → **O(1)** ✅
- `result.append(name)` → O(1) amortized
- Cost per iteration: O(1)
- Block 2 total: **O(a)**

*Block 3:*
- `result.sort()` → O(k log k) where k = len(result)
- What is k worst case? Every name passes the filter (none are blocked) → k = a
- Block 3 total: worst case **O(a log a)**

*Block 4:* O(1)

**STEP 4: Combine**
O(b) + O(a) + O(a log a) + O(1)

- O(a) is dominated by O(a log a). Drop it.
- O(1) is dominated. Drop it.

**O(b + a log a)**

**STEP 5: Space**
- `blocked_set` → set with b elements → **O(b)**
- `result` → list with at most a elements → **O(a)**
- `name` → O(1)
- Total extra space: **O(a + b)**

**STEP 6: Answer**
> **Time: O(b + a log a), Space: O(a + b)**

---

# Problem 6: Function Call Inside a Loop

```python
def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def func(matrix):
    count = 0
    for row in matrix:
        if is_sorted(row):
            count += 1
    return count
```

**STEP 1: Identify Inputs**
- `matrix` → a 2D array
- **r = number of rows**, **c = number of columns** (length of each row)
- Or if rows can have different lengths, c_i = len(row_i). I'll assume uniform rows of length c for clarity.

**STEP 2: Break Into Blocks**
- First: analyze `is_sorted` independently
- Then: analyze `func`

**STEP 3: Analyze Each Block**

*Analyzing `is_sorted(arr)` first:*
- Input: a single row of length c
- Loop runs c - 1 times
- Inside: `arr[i]` → O(1), `arr[i+1]` → O(1), comparison → O(1)
- Worst case (array is sorted, no early return): all c - 1 iterations run
- `is_sorted` total: **O(c)**

*Now `func`:*

- Block 1: `count = 0` → O(1)
- Block 2: The for loop
  - Loop runs **r** times (once per row)
  - Inside: `is_sorted(row)` → **O(c)** per call (analyzed above)
  - `count += 1` → O(1)
  - Cost per iteration: O(c)
  - Block 2 total: r × O(c) = **O(r × c)**
- Block 3: `return count` → O(1)

**STEP 4: Combine**
O(1) + O(r × c) + O(1) = **O(r × c)**

Note: r × c = total number of cells in the matrix. This makes sense — in the worst case we examine every cell.

**STEP 5: Space**
- `count` → O(1)
- `i` inside `is_sorted` → O(1)
- No growing structures anywhere
- No recursion
- Total extra space: **O(1)**

**STEP 6: Answer**
> **Time: O(r × c), Space: O(1)**
> Where r = number of rows, c = number of columns

---

# Problem 7: Dependent Nesting With Inner Work

```python
def func(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        for j in range(i, n):
            sub = arr[i:j+1]
            total += sum(sub)
    return total
```

**STEP 1: Identify Inputs**
- `arr` → n = len(arr)

**STEP 2: Break Into Blocks**
- Block 1: `n = len(arr)`, `total = 0` → single operations
- Block 2: The nested loops (the main event)
- Block 3: `return total`

**STEP 3: Analyze Each Block**

*Block 1:* O(1)

*Block 2:* This needs careful analysis. Three layers of cost here.

**Outer loop:** runs n times (i = 0 to n-1)

**Inner loop:** for each i, j runs from i to n-1. That's (n - i) iterations.

**Inside the inner loop — THIS IS THE CRITICAL PART:**

- `arr[i:j+1]` → ⚠️ **slicing creates a new list** of length (j + 1 - i). Cost: **O(j + 1 - i)**
- `sum(sub)` → ⚠️ **iterates through the entire slice** to sum it. Cost: **O(j + 1 - i)**
- `total += sum(sub)` → O(1) for the addition
- Cost per inner iteration: O(j + 1 - i) + O(j + 1 - i) = **O(j - i)**

So for each (i, j) pair, the work is proportional to the length of the subarray, which is (j - i + 1). Let me compute the total:

$$\text{Total} = \sum_{i=0}^{n-1} \sum_{j=i}^{n-1} (j - i + 1)$$

For a fixed i, let k = j - i + 1 (the subarray length). As j goes from i to n-1, k goes from 1 to (n - i):

$$\sum_{k=1}^{n-i} k = \frac{(n-i)(n-i+1)}{2}$$

Now sum over all i:

$$\sum_{i=0}^{n-1} \frac{(n-i)(n-i+1)}{2}$$

Let m = n - i. As i goes 0 to n-1, m goes n down to 1:

$$\sum_{m=1}^{n} \frac{m(m+1)}{2} = \frac{1}{2}\sum_{m=1}^{n} (m^2 + m) = \frac{1}{2}\left(\frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2}\right)$$

The dominant term is the m² sum: **n(n+1)(2n+1)/6 ≈ n³/3**

Total: **O(n³)**

*Block 3:* O(1)

**STEP 4: Combine**
O(1) + O(n³) + O(1) = **O(n³)**

**STEP 5: Space**
- `n`, `total`, `i`, `j` → O(1) each
- `sub` → ⚠️ this is created fresh each inner iteration. At any one moment, only ONE `sub` exists (the previous one gets garbage collected). Its maximum size is n (when i=0, j=n-1).
- `sum(sub)` doesn't create additional structures
- So at any point, extra memory is at most one slice of size up to n
- Total extra space: **O(n)**

**STEP 6: Answer**
> **Time: O(n³), Space: O(n)**

The O(n³) comes not from triple-nested loops, but from **two loops with O(n) work hidden inside the inner loop** (slicing + summing). This is exactly the Skill 6 trap — the nested loops alone would be O(n²), but the inner work adds another factor of n.

---

# Problem 8: The Boss

```python
def analyze_orders(orders, vip_list, min_amount):
    # Block 1
    vips = set(vip_list)

    # Block 2
    totals = {}
    for order in orders:
        uid = order["user_id"]
        amt = order["amount"]
        if uid in vips:
            if uid not in totals:
                totals[uid] = 0
            totals[uid] += amt

    # Block 3
    qualified = []
    for uid in totals:
        if totals[uid] >= min_amount:
            qualified.append(uid)

    # Block 4
    qualified.sort()

    # Block 5
    report = ""
    for uid in qualified:
        report = report + uid + ": " + str(totals[uid]) + "\n"

    return report
```

**STEP 1: Identify Inputs**
- `orders` → **n = len(orders)**
- `vip_list` → **v = len(vip_list)**
- `min_amount` → a single number, not a collection. No size variable needed.
- Two independent collection inputs → two variables.

**STEP 2: Break Into Blocks**
Already marked. Five blocks.

**STEP 3: Analyze Each Block**

*Block 1:*
- `set(vip_list)` → iterates through all v elements, O(1) insertion each
- Block 1 total: **O(v)**

*Block 2:*
- Loop runs **n** times (once per order)
- Inside:
  - `order["user_id"]` → dict access → O(1)
  - `order["amount"]` → dict access → O(1)
  - `uid in vips` → set lookup → **O(1)** ✅
  - `uid not in totals` → dict lookup → **O(1)** ✅
  - `totals[uid] = 0` → dict assignment → O(1)
  - `totals[uid] += amt` → dict access + assignment → O(1)
- Every operation inside is O(1). Cost per iteration: O(1)
- Block 2 total: **O(n)**

*Block 3:*
- Loop runs **k** times where k = len(totals)
- What is k? `totals` has one entry per unique VIP user found in orders. So **k ≤ min(n, v)** — can't exceed number of orders or number of VIPs.
- Inside: dict access O(1), comparison O(1), append O(1)
- Block 3 total: **O(k)**

*Block 4:*
- `qualified.sort()` → O(q log q) where q = len(qualified)
- q ≤ k ≤ min(n, v)
- Block 4 total: **O(q log q)**

*Block 5:* ⚠️ **THE STRING CONCATENATION TRAP AGAIN**
- Loop runs **q** times
- Inside: `report = report + uid + ": " + str(totals[uid]) + "\n"`
- This is string concatenation. Each iteration creates a **brand new string**, copying all of `report` plus the new piece.
- Let's say each uid + formatting adds roughly some characters of length L per entry. `report` grows each iteration.
- Iteration 1: copy ~L characters
- Iteration 2: copy ~2L characters
- ...
- Iteration q: copy ~qL characters
- Total: L(1 + 2 + 3 + ... + q) = L × q(q+1)/2 = **O(q²)** (treating L as bounded/constant, or more precisely O(q² × L) if uid lengths vary)

Assuming uid lengths are bounded by a constant: **O(q²)**

*Return:* O(1)

**STEP 4: Combine**

O(v) + O(n) + O(k) + O(q log q) + O(q²)

Simplification chain:
- q ≤ k, so O(k) is ≥ O(q). But O(q²) dominates O(k) if q is large, and O(q²) dominates O(q log q).
- The dominant terms are: O(v), O(n), and O(q²)

**O(v + n + q²)** where q ≤ min(n, v)

Conservative worst case (all orders are from unique VIPs, all qualify): q ≈ min(n, v)

**O(v + n + min(n,v)²)**

If v ≤ n: O(n + v²). If n ≤ v: O(v + n²).

**STEP 5: Space**
- `vips` → set with v elements → **O(v)**
- `totals` → dict with at most k entries → **O(k)**
- `qualified` → list with at most q entries → **O(q)**
- `report` → string that grows. At any point, one copy exists. Max size = q × (average entry length). If entry lengths are bounded: **O(q)**
- `uid`, `amt` → O(1)

Total: O(v) + O(k) + O(q) + O(q)

Since q ≤ k: O(v) + O(k) = **O(v + k)**

Conservative worst case: **O(v + n)** (since k ≤ n)

**STEP 6: Answer**
> **Time: O(v + n + q²)** where v = len(vip_list), n = len(orders), q = number of qualified VIP users, q ≤ min(n, v)
> Conservative worst case: **O(v + n + min(n,v)²)**

> **Space: O(v + k)** where k = number of unique VIP users in orders, k ≤ min(n, v)
> Conservative worst case: **O(v + n)**

> **Note:** Block 5 is the bottleneck due to the string concatenation trap. Replacing it with `"\n".join(f"{uid}: {totals[uid]}" for uid in qualified)` would eliminate the O(q²) term, making the overall time **O(v + n + q log q)** — dominated by the sort — which is a massive improvement.

# Problem 9: While Loop Analysis

```python
def compress(arr):
    n = len(arr)
    result = []
    i = 0
    while i < n:
        j = i
        while j < n and arr[j] == arr[i]:
            j += 1
        result.append((arr[i], j - i))
        i = j
    return result
```

---

## STEP 1: Identify Inputs

- `arr` → **n = len(arr)**
- Single input, single variable.

---

## STEP 2: Break Into Blocks

- Block 1: `n = len(arr)`, `result = []`, `i = 0` → single operations
- Block 2: The outer while loop (contains everything important)
- Block 3: `return result`

---

## STEP 3: Analyze Each Block

**Block 1:** Three assignments → **O(1)**

**Block 2:** This is where it gets interesting. There's a nested while loop, so the instinct is to multiply. **But that instinct is WRONG here.** Let me prove why.

First, let me trace this with a concrete example to understand what the code does:

```
arr = [a, a, a, b, b, c, c, c, c]
       0  1  2  3  4  5  6  7  8      n = 9
```

```
Outer iteration 1:
  i = 0, j starts at 0
  Inner: j=0 arr[0]==arr[0]? a==a yes → j=1
         j=1 arr[1]==arr[0]? a==a yes → j=2
         j=2 arr[2]==arr[0]? a==a yes → j=3
         j=3 arr[3]==arr[0]? b==a NO  → stop
  append('a', 3)
  i = j = 3

Outer iteration 2:
  i = 3, j starts at 3
  Inner: j=3 arr[3]==arr[3]? b==b yes → j=4
         j=4 arr[4]==arr[3]? b==b yes → j=5
         j=5 arr[5]==arr[3]? c==b NO  → stop
  append('b', 2)
  i = j = 5

Outer iteration 3:
  i = 5, j starts at 5
  Inner: j=5 arr[5]==arr[5]? c==c yes → j=6
         j=6 arr[6]==arr[5]? c==c yes → j=7
         j=7 arr[7]==arr[5]? c==c yes → j=8
         j=8 arr[8]==arr[5]? c==c yes → j=9
         j=9 → j < n fails → stop
  append('c', 4)
  i = j = 9

Outer: i = 9, 9 < 9 false → stop
```

**The critical observation:** `j` scans forward through the array and **never goes backward.** After the inner loop finishes, `i` jumps to `j`. The inner loop then picks up from that new position. Every element of the array is visited by `j` **exactly once** across ALL iterations of the outer loop combined.

Let me count the total number of inner loop iterations across the entire execution:
- Outer iteration 1: j visits indices 0, 1, 2, 3 → 4 checks
- Outer iteration 2: j visits indices 3, 4, 5 → 3 checks
- Outer iteration 3: j visits indices 5, 6, 7, 8, 9 → 5 checks

Wait — there's slight overlap at boundaries (j checks the failing condition). Let me count more carefully. Each `j += 1` happens once per element that matches plus one final failing check per outer iteration. But the total `j += 1` executions across all inner loop runs = n (because j goes from 0 to n total). The number of failing checks equals the number of outer iterations, which is at most n.

**Total inner loop iterations across all outer iterations: at most 2n** → O(n).

This is a **pointer-chasing pattern.** Two pointers (`i` and `j`) both march left-to-right through the array without resetting. Even though the loops are nested in the code structure, **the total combined work is linear.**

Inside the inner loop:
- `j < n` → O(1) comparison
- `arr[j] == arr[i]` → O(1) comparison (assuming element comparison is O(1))
- `j += 1` → O(1)
- Cost per inner iteration: **O(1)**

Inside the outer loop (outside the inner loop):
- `j = i` → O(1)
- `result.append((arr[i], j - i))` → O(1) amortized
- `i = j` → O(1)

Block 2 total: **O(n)**

**Block 3:** `return result` → O(1)

---

## STEP 4: Combine

O(1) + O(n) + O(1) = **O(n)**

---

## STEP 5: Space

- `n`, `i`, `j` → single variables → O(1)
- `result` → list of tuples. How large can it get?
  - Worst case: every element is different → `[a, b, c, d, ...]` → n tuples
  - Best case: all elements the same → `[a, a, a, ...]` → 1 tuple
  - Worst case: **O(n)**

Total extra space: **O(n)**

---

## STEP 6: Answer

> **Time: O(n), Space: O(n)**

### The Lesson Here

**Nested loops do NOT automatically mean multiply.** The rule is multiply when the inner loop runs its full count **independently for each outer iteration.** Here, the inner loop's work is **shared** across outer iterations — the pointer `j` never resets to 0. The total work of the inner loop across ALL outer iterations is n, not n per outer iteration.

**How to spot this pattern:**
- A pointer advances forward and **never resets**
- After the inner loop, the outer variable **jumps to where the inner left off** (`i = j`)
- The inner loop picks up from the new position, not from 0

This is the **two-pointer / sliding window** pattern. You'll see it constantly in interview problems. It always looks like O(n²) but is actually **O(n).**

---

---

# Problem 10: Preprocess + Query Pattern

```python
def build_index(products):
    index = {}
    for product in products:
        category = product["category"]
        if category not in index:
            index[category] = []
        index[category].append(product["name"])

    for category in index:
        index[category].sort()

    return index

def search(index, category, prefix):
    if category not in index:
        return []
    result = []
    for name in index[category]:
        if name.startswith(prefix):
            result.append(name)
    return result
```

---

# Part A: Complexity of `build_index`

## STEP 1: Identify Inputs

- `products` → **n = len(products)**
- Each product has a `"category"` and a `"name"` (strings)
- Let **c = number of unique categories** that appear in products
- Let **L = average length of a product name** (needed for string comparisons during sort)

## STEP 2: Break Into Blocks

- Block 1: `index = {}` → single operation
- Block 2: First for loop (building the lists)
- Block 3: Second for loop (sorting each category's list)
- Block 4: `return index`

## STEP 3: Analyze Each Block

**Block 1:** O(1)

**Block 2:**
- Loop runs **n** times (once per product)
- Inside:
  - `product["category"]` → dict access → O(1)
  - `category not in index` → dict lookup → O(1)
  - `index[category] = []` → dict assignment → O(1)
  - `index[category].append(product["name"])` → dict access O(1), append O(1) amortized
- Cost per iteration: **O(1)**
- Block 2 total: **O(n)**

**Block 3:** This requires careful thinking.
- Loop runs **c** times (once per unique category)
- Inside: `index[category].sort()` → sorts the list for that category

Now, how large is each category's list? Let's say category `i` has `nᵢ` products. We know:

$$n_1 + n_2 + n_3 + \ldots + n_c = n$$

All products are distributed across the c categories. The total work for sorting all categories is:

$$\sum_{i=1}^{c} n_i \log(n_i)$$

Since each $n_i \log(n_i) \leq n_i \log(n)$ (because $n_i \leq n$):

$$\sum_{i=1}^{c} n_i \log(n_i) \leq \sum_{i=1}^{c} n_i \log(n) = n \log(n)$$

Block 3 total: **O(n log n)**

*(Note: If we account for string comparison cost during sort, each comparison is O(L), making it O(L · n log n). I'll note this but keep L out of the main answer for clarity since the lesson focuses on structural complexity.)*

**Block 4:** O(1)

## STEP 4: Combine

O(1) + O(n) + O(n log n) + O(1)

O(n) is dominated by O(n log n). Drop it.

**Time for `build_index`: O(n log n)**

## STEP 5: Space

- `index` → dictionary with c keys. The values are lists containing ALL n product names distributed across the categories. Total elements stored across all lists: **n**
- `category` → O(1) single variable
- No recursion

Total extra space: **O(n + c)**

But since c ≤ n (can't have more categories than products): **O(n)**

## STEP 6: Answer for `build_index`

> **Time: O(n log n), Space: O(n)**

---

# Part B: Complexity of a Single Call to `search`

```python
def search(index, category, prefix):
    if category not in index:
        return []
    result = []
    for name in index[category]:
        if name.startswith(prefix):
            result.append(name)
    return result
```

## STEP 1: Identify Inputs

This is subtle. The inputs to `search` are:
- `index` → the pre-built dictionary (we treat this as already existing, not a cost to build)
- `category` → a single string
- `prefix` → a single string, let **p = len(prefix)**

The relevant size for this function: **m = number of products in the given category** = len(index[category])

## STEP 2: Break Into Blocks

- Block 1: `category not in index` check + possible early return
- Block 2: `result = []`
- Block 3: The for loop
- Block 4: `return result`

## STEP 3: Analyze Each Block

**Block 1:** Dict lookup → O(1). Early return → O(1). → **O(1)**

**Block 2:** O(1)

**Block 3:**
- Loop runs **m** times (once per name in that category)
- Inside:
  - `name.startswith(prefix)` → ⚠️ What does this cost? It compares the first `p` characters of `name` against `prefix`. Cost: **O(p)**
  - `result.append(name)` → O(1) amortized
- Cost per iteration: **O(p)**
- Block 3 total: **O(m × p)**

**Block 4:** O(1)

## STEP 4: Combine

O(1) + O(1) + O(m × p) + O(1) = **O(m × p)**

If we treat prefix length as a small constant (which is common in practice): **O(m)**

## STEP 5: Space

- `result` → worst case, every name matches the prefix → m elements → **O(m)**
- `name` → single variable → O(1)

Total extra space: **O(m)**

## STEP 6: Answer for single `search` call

> **Time: O(m × p)** where m = number of products in queried category, p = len(prefix)
> Simplified (if p treated as constant): **O(m)**
> **Space: O(m)**

---

# Part C: Total Complexity — Build Once, Search q Times

## Setup

- `build_index` is called **once**: O(n log n) time, O(n) space
- `search` is called **q times**

For each search call `i`, let:
- $m_i$ = number of products in the queried category
- $p_i$ = length of the prefix

## Time Analysis

$$T_{total} = \underbrace{O(n \log n)}_{\text{build}} + \underbrace{\sum_{i=1}^{q} O(m_i \cdot p_i)}_{\text{all searches}}$$

**Worst case for each search:** The queried category contains all n products (one giant category), and prefix is long.

$$T_{worst} = O(n \log n) + O(q \cdot n \cdot p)$$

If prefix length is bounded/constant:

$$T_{worst} = O(n \log n + q \cdot n)$$

**But in practice**, the whole point of building the index is that $m_i \ll n$ for most queries. If products are spread across c roughly equal categories, each $m_i ≈ n/c$:

$$T_{practical} = O\left(n \log n + q \cdot \frac{n}{c} \cdot p\right)$$

## Space Analysis

- The `index` persists in memory throughout all queries: **O(n)**
- Each `search` call creates a `result` list: **O(m_i)** per call, but it's returned and (presumably) doesn't accumulate — only one search's `result` exists at a time
- Total persistent space: **O(n)** for the index

## Final Answer

> **Build: O(n log n) time, O(n) space**
> **Per search: O(m · p) time, O(m) space** — where m = category size, p = prefix length
> **Total (build once + q searches): O(n log n + q · m · p) time, O(n) space**
> **Conservative worst case: O(n log n + q · n · p) time**

---

## The Real-World Lesson

This is the **precomputation pattern.** You see it everywhere:

| System | Build Phase | Query Phase |
|---|---|---|
| Search engine | Crawl + index web pages | User types query |
| Database index | Build B-tree on column | Run SELECT queries |
| This problem | Sort products by category | Look up by category + prefix |
| Spell checker | Build dictionary hash set | Check each typed word |

The idea: **spend more time upfront (build) so that every subsequent query is fast.** If you skip the build phase and do a naive search every time, you pay O(n) per query × q queries = O(qn). With the index, each query drops to O(m) where m ≪ n.

The break-even question: Is O(n log n) build + O(q · m) queries cheaper than O(q · n) brute force? **Yes, whenever q is large and m is much smaller than n** — which is almost always the real-world scenario.

