# STACKS & QUEUES — THE COMPLETE LESSON

**Module:** 4 (Linked Lists + Stacks & Queues)  
**Monotonic ownership:** This file is the **intro** — next greater, daily temps, histogram, sliding-window max. The **deep dive** (contribution technique, harder families, mono vs range structures) lives in Module 10: `Advanced/Tries & Monotonic.md`. See `QA/Monotonic Ownership.md`.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHAT STACKS AND QUEUES ACTUALLY ARE

## Why You Need To Know This

Stacks and queues are not "just APIs." They are **access policies** that turn hard problems into mechanical ones:

- **Stack (LIFO)** — last in, first out. Matches nested structure, deferred work, "nearest previous larger," undo, DFS call simulation.
- **Queue (FIFO)** — first in, first out. Matches arrival order, BFS layer order, sliding-window candidates (as a deque).

If you only memorize `append`/`pop`, you will miss:
- Why monotonic stacks solve "next greater" in O(n)
- Why a deque (not a list) is the right sliding-window structure
- How min-stack and "queue via stacks" are interview classics that test invariant thinking
- When Python `list` is fine vs when `collections.deque` is mandatory

---

## 1A: The ADTs

### Stack

```
Operations:
  push(x)  — add to top
  pop()    — remove from top
  peek/top — read top without remove
  empty()

Only the TOP is accessible.
```

```
push 1, push 2, push 3:

    | 3 |  ← top
    | 2 |
    | 1 |
    -----

pop → 3, then top is 2
```

### Queue

```
Operations:
  enqueue(x) — add to back
  dequeue()  — remove from front
  front/peek — read front
  empty()

Front leaves first; back receives new arrivals.
```

```
enqueue 1, 2, 3:

  front → 1  2  3 ← back

dequeue → 1
```

### Deque (Double-Ended Queue)

Insert/delete at **both** ends in O(1). Superset used for:
- Sliding window maximum (monotonic queue)
- 0-1 BFS (PREVIEW — graphs)
- Palindrome checks with two ends

---

## 1B: Python — `list` vs `deque`

### Stack in Python

```python
stack = []
stack.append(x)   # push — O(1) amortized
stack.pop()       # pop from end — O(1)
stack[-1]         # peek
```

**Use a list for stacks.** End operations are O(1).

### Queue — the trap

```python
# BAD as a queue for large n
q = []
q.append(x)      # enqueue at end — OK
q.pop(0)         # dequeue from front — O(n) !!! shifts everything
```

```python
from collections import deque

q = deque()
q.append(x)      # enqueue right — O(1)
q.popleft()      # dequeue left — O(1)
q.appendleft(x)  # O(1)
q.pop()          # O(1) from right
```

**Rule:** Stack → `list`. Queue / deque / sliding window → `collections.deque`.

### Complexity Truth Table

| Structure | push/append right | pop right | pop left | append left |
|---|---|---|---|---|
| `list` | O(1) amort. | O(1) | **O(n)** | **O(n)** |
| `deque` | O(1) | O(1) | O(1) | O(1) |

**Interview talk:** "I'll use a list as a stack. For a queue I'll use `deque` so front removal stays O(1)."

---

## 1C: When Stacks/Queues Are the Right Mental Model

| Problem smell | Structure |
|---|---|
| Matching brackets / nesting | Stack |
| Undo, back button, browser history | Stack |
| Evaluate RPN / calculator | Stack |
| "Next greater/smaller to the right/left" | Monotonic stack |
| Process in arrival order | Queue |
| Level-order / BFS | Queue (**Graphs own deep BFS** — see preview note) |
| Sliding window max/min | Monotonic deque |
| Cache eviction order (LRU) | DLL ≈ deque of keys + map (LL module) |

---

# PART 2: CLASSIC STACK PATTERNS

## Pattern 1: Valid Parentheses

### Framework

```
For each char:
  if opener → push
  if closer → stack must be non-empty and top must match; else invalid
After loop → stack must be empty
```

```python
def is_valid(s):
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()
    return not stack
```

### Trace: `"{[]}"`

```
{ → push
[ → push
] → top [ matches → pop
} → top { matches → pop
empty → True
```

### Trace: `"(]"`

```
( → push
] → top ( != [ → False
```

**TRAP:** Only checking counts, not order — `([)]` has equal counts but is invalid.

---

## Pattern 2: Min Stack

Design a stack that supports push, pop, top, and **getMin in O(1)**.

### Framework — store running minima

```python
class MinStack:
    def __init__(self):
        self.stack = []      # (val, min_so_far)

    def push(self, val):
        if not self.stack:
            self.stack.append((val, val))
        else:
            self.stack.append((val, min(val, self.stack[-1][1])))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
```

**Invariant:** top's second field is the minimum of the entire stack content.

### Trace

```
push 5 → [(5,5)]  min=5
push 3 → [(5,5),(3,3)]  min=3
push 7 → [(5,5),(3,3),(7,3)]  min=3
pop    → [(5,5),(3,3)]  min=3
pop    → [(5,5)]  min=5
```

**Alternative:** two stacks (values + mins). Same idea.

---

## Pattern 3: Implement Queue Using Stacks

### Framework — input stack + output stack

```python
class MyQueue:
    def __init__(self):
        self.in_s = []
        self.out_s = []

    def push(self, x):
        self.in_s.append(x)

    def _move(self):
        if not self.out_s:
            while self.in_s:
                self.out_s.append(self.in_s.pop())

    def pop(self):
        self._move()
        return self.out_s.pop()

    def peek(self):
        self._move()
        return self.out_s[-1]

    def empty(self):
        return not self.in_s and not self.out_s
```

**Amortized O(1)** per operation: each element moves at most once from in→out.

### Trace

```
push 1, push 2
in=[1,2] out=[]
peek → move → out=[2,1] → peek 1
pop → 1
push 3
in=[3] out=[2]
pop → 2 (no move needed)
pop → move 3 to out → 3
```

---

## Pattern 4: Decode String

`k[encoded]` — decode nested patterns.

```
Input: "3[a2[c]]"
Output: "accaccacc"
```

### Framework — stack of (prev_string, repeat_count)

```python
def decode_string(s):
    stack = []
    cur_str = ""
    cur_num = 0
    for ch in s:
        if ch.isdigit():
            cur_num = cur_num * 10 + int(ch)
        elif ch == '[':
            stack.append((cur_str, cur_num))
            cur_str = ""
            cur_num = 0
        elif ch == ']':
            prev, num = stack.pop()
            cur_str = prev + cur_str * num
        else:
            cur_str += ch
    return cur_str
```

### Trace: `"3[a2[c]]"`

```
'3' → num=3
'[' → push ("", 3); reset
'a' → cur="a"
'2' → num=2
'[' → push ("a", 2); reset
'c' → cur="c"
']' → pop ("a",2) → cur = "a" + "c"*2 = "acc"
']' → pop ("",3) → cur = "" + "acc"*3 = "accaccacc"
```

**TRAP:** Multi-digit numbers (`12[a]`) — accumulate `cur_num * 10 + digit`.

---

## Pattern 5: Asteroid Collision

Asteroids on a line; positive = right, negative = left. Same direction = never collide. Opposite = collide (smaller explodes; equal both explode).

### Framework — stack of survivors moving rightward logic

```python
def asteroid_collision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
                continue
            elif stack[-1] == -a:
                stack.pop()
            alive = False
        if alive:
            stack.append(a)
    return stack
```

### Trace: `[5, 10, -5]`

```
5 → [5]
10 → [5,10]
-5 → fights 10; 10 > 5 → -5 dies → [5,10]
```

### Trace: `[10, 2, -5]`

```
10, 2 → [10,2]
-5 vs 2 → 2 dies; -5 vs 10 → -5 dies → [10]
```

**Only** `stack_top > 0` and `a < 0` can collide.

---

# PART 3: MONOTONIC STACK — INTRODUCTION + DEEP PATTERNS

## What "Monotonic" Means

A **monotonic stack** keeps elements in sorted order (strict or non-strict) by **popping violators** before pushing.

```
Increasing stack (bottom→top): values never decrease
Decreasing stack (bottom→top): values never increase
```

**Why it exists:** For each index, you need the **nearest** greater/smaller element to the left or right. Naive is O(n²). Monotonic stack does all answers in **O(n)** because each index is pushed and popped at most once.

### The Universal Framework

```
For each index i in order (or reverse order):
    while stack not empty and [ordering violated by nums[i]]:
        j = stack.pop()
        # nums[i] is the "next greater/smaller" for j (if scanning L→R for next-to-right)
        answer[j] = ...
    stack.append(i)   # store INDICES, usually — need positions
```

**Store indices, not values** — you need positions for distance/width/answer array.

### Decision Table

| Want | Scan direction | Stack order (by value) | While condition |
|---|---|---|---|
| Next greater to the **right** | L → R | Decreasing | `nums[stack.top] < nums[i]` |
| Next greater to the **left** | L → R | Decreasing | same, answer when pushing? or scan R→L |
| Next smaller to the right | L → R | Increasing | `nums[stack.top] > nums[i]` |
| Previous smaller (histogram) | L → R | Increasing | `nums[stack.top] >= nums[i]` (variants) |

**Interview talk:** "Each element enters and leaves the stack once → O(n). The stack stores candidates that haven't found their next greater yet."

---

## Deep Pattern A: Next Greater Element

```
nums = [2, 1, 2, 4, 3]
next greater to right: [4, 2, 4, -1, -1]
```

```python
def next_greater(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []  # indices, decreasing values
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            ans[j] = x
        stack.append(i)
    return ans
```

### Trace

```
i=0,2: stack=[0]
i=1,1: 2!<1; stack=[0,1]
i=2,2: pop 1 → ans[1]=2; stack=[0]; 2!<2; stack=[0,2]
i=3,4: pop 2 → ans[2]=4; pop 0 → ans[0]=4; stack=[3]
i=4,3: 4!<3; stack=[3,4]
done: ans=[4,2,4,-1,-1]
```

---

## Deep Pattern B: Daily Temperatures

Given temperatures, for each day return how many days until a warmer temperature (0 if none).

```
T = [73,74,75,71,69,72,76,73]
Out= [1, 1, 4, 2, 1, 1, 0, 0]
```

**Same as next greater**, but answer is **index distance**, not value.

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    ans = [0] * n
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
```

### Trace (abbrev)

```
73 → [0]
74 → pop 0, ans[0]=1; stack=[1]
75 → pop 1, ans[1]=1; stack=[2]
71 → [2,3]
69 → [2,3,4]
72 → pop 4 ans[4]=1; pop 3 ans[3]=2; stack=[2,5]
76 → pop 5 ans[5]=1; pop 2 ans[2]=4; stack=[6]
73 → [6,7]
```

---

## Deep Pattern C: Largest Rectangle in Histogram

Heights of bars width 1. Largest rectangle area in histogram.

```
heights = [2,1,5,6,2,3]
Answer: 10  (bars 5 and 6 → area 5*2)
```

### WHY Monotonic Stack

For each bar `i` with height `h`, the largest rectangle **with height exactly h** using bar i extends:
- Left until a bar **strictly shorter** than h
- Right until a bar **strictly shorter** than h

Area = `h * (right_boundary - left_boundary - 1)`

Monotonic **increasing** stack finds previous-smaller and next-smaller efficiently.

### Framework

```python
def largest_rectangle_area(heights):
    # sentinel 0s simplify empty-stack / end flushing
    h = [0] + heights + [0]
    stack = [0]  # indices into h; increasing heights
    best = 0
    for i in range(1, len(h)):
        while h[i] < h[stack[-1]]:
            height = h[stack.pop()]
            width = i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best
```

### Trace (core idea)

```
When we see a shorter bar, everything taller on the stack can finalize its rectangle —
the new bar is the first shorter to the right; new stack top is first shorter to the left.
```

```
heights [2,1,5,6,2,3] with sentinels:
[0,2,1,5,6,2,3,0]

... when i at second 2 (index of value 2 after 6):
  pop 6: height 6, width limited by 5 on left and 2 on right → 6*1=6
  pop 5: height 5, width spans to left sentinel-ish → 5*2=10  ← best
```

**TRAP:** Off-by-one on width. Sentinels (`0` at both ends) prevent special cases.

**Interview talk:** "For each bar I need previous and next smaller. Monotonic increasing stack gives both as I scan once. Area = height * width between those bounds."

---

## Full Histogram Trace (do this until automatic)

```
heights = [2, 1, 5, 6, 2, 3]
h       = [0, 2, 1, 5, 6, 2, 3, 0]   # with sentinels
indices =  0  1  2  3  4  5  6  7

stack starts [0]  (sentinel index)

i=1, h=2: 2 > 0 → push 1          stack [0,1]
i=2, h=1: 1 < 2 → pop 1, height=2, width=2-0-1=1, area=2
          1 > 0 → push 2          stack [0,2]
i=3, h=5: 5 > 1 → push 3          stack [0,2,3]
i=4, h=6: 6 > 5 → push 4          stack [0,2,3,4]
i=5, h=2: 2 < 6 → pop 4, height=6, width=5-3-1=1, area=6
          2 < 5 → pop 3, height=5, width=5-2-1=2, area=10  ← best
          2 > 1 → push 5          stack [0,2,5]
i=6, h=3: 3 > 2 → push 6          stack [0,2,5,6]
i=7, h=0: 0 < 3 → pop 6, height=3, width=7-5-1=1, area=3
          0 < 2 → pop 5, height=2, width=7-2-1=4, area=8
          0 < 1 → pop 2, height=1, width=7-0-1=6, area=6
          push 7

best = 10 ✅
```

**Invariant to say in interview:** "Stack holds increasing heights. When a shorter bar arrives, every taller bar on the stack can compute its max rectangle — the new bar is next-smaller-right; the new top is previous-smaller-left."

---

## Next Greater — Full Trace + Left Variant

### Next greater to the right (again, slower)

```
nums = [2, 1, 2, 4, 3]
ans  = [-1,-1,-1,-1,-1]
stack = []  # indices, decreasing values

i=0 (2): push 0                 [0]
i=1 (1): 2 !< 1; push 1         [0,1]
i=2 (2): pop 1 → ans[1]=2       [0]
         2 !< 2; push 2         [0,2]
i=3 (4): pop 2 → ans[2]=4       [0]
         pop 0 → ans[0]=4       []
         push 3                 [3]
i=4 (3): 4 !< 3; push 4         [3,4]

ans = [4, 2, 4, -1, -1]
```

### Previous smaller to the left (building block for histogram)

```python
def previous_smaller(nums):
    """For each i, nearest j < i with nums[j] < nums[i], else -1."""
    n = len(nums)
    ans = [-1] * n
    stack = []  # increasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] >= x:
            stack.pop()
        ans[i] = stack[-1] if stack else -1
        stack.append(i)
    return ans
```

```
nums=[2,1,5,6,2,3]
prev smaller indices: [-1,-1,1,2,1,4]
```

---

# PART 3B: EXPRESSION PARSING WITH STACKS

Expression problems are stack problems in disguise: operators and parentheses create **deferred work** that must resolve in the right order.

## Pattern: Basic Calculator II ( + - * / , no parens )

```
Input: "3+2*2"
Output: 7
```

### Framework

Scan numbers; for each operator, decide whether to apply immediately (`*`,`/`) or defer (`+`,`-` as signed terms on a stack).

```python
def calculate(s):
    stack = []
    num = 0
    op = '+'  # virtual op before first number
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in '+-*/' or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            elif op == '/':
                # truncate toward zero
                top = stack.pop()
                stack.append(int(top / num))
            op = ch
            num = 0
    return sum(stack)
```

### Trace: `"3+2*2"`

```
op='+', see 3, then '+': push 3; op='+'
see 2, then '*': push 2; op='*'
see 2, end: pop 2 * 2 → push 4
sum = 3+4 = 7 ✅
```

### Trace: `"14-3/2"`

```
op='+', complete 14 on seeing '-': push +14; op='-'
complete 3 on seeing '/': push -3; op='/'
complete 2 at end: pop -3, apply / 2 → int((-3)/2) with toward-zero → -1; push -1
sum(stack) = 14 + (-1) = 13 ✅
```

In Python 3, `int(a / b)` truncates toward zero (e.g. `int(3/2)==1`, `int(-3/2)==-1`).

**Interview talk:** "I treat + and - as pushing signed numbers. * and / apply to the last pushed term immediately — that encodes precedence without a shunting-yard full parser."

---

## Pattern: Evaluate Reverse Polish Notation

```
Input: ["2","1","+","3","*"]
Output: 9   # (2+1)*3
```

```python
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t not in '+-*/':
            stack.append(int(t))
        else:
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else: stack.append(int(a / b))  # toward zero
    return stack[-1]
```

### Trace

```
2 → [2]
1 → [2,1]
+ → pop 1,2 → push 3 → [3]
3 → [3,3]
* → pop 3,3 → push 9 → [9]
```

**TRAP:** Pop order — right operand is popped first (`b` then `a`).

---

## Pattern: Remove All Adjacent Duplicates / Path Simplify (stack as builder)

```python
def remove_duplicates(s):
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return ''.join(stack)
```

```
abbaca → a b b→pop b → a a→pop a → c a → "ca"
```

Same skeleton as path simplify (`".."` pops, `"."` skip, else push).

---

# PART 4: MONOTONIC QUEUE — SLIDING WINDOW MAXIMUM

## The Problem

```
nums = [1,3,-1,-3,5,3,6,7], k=3
Windows max: [3,3,5,5,6,7]
```

Naive: O(nk). Need O(n).

## Monotonic Deque Framework

Maintain a deque of **indices** with **decreasing** values:
- Front = index of current window maximum
- Before inserting `i`, pop back while `nums[back] <= nums[i]` (they can never be max while `i` is in window)
- Pop front if it's outside the window (`i - k`)

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # indices, nums[dq] decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

### Trace

```
k=3, nums=[1,3,-1,-3,5,3,6,7]

i=0: dq=[0]
i=1: pop 0 (1<=3); dq=[1]; i>=2? no
i=2: 3> -1; dq=[1,2]; out ← nums[1]=3
i=3: dq=[1,2,3]; front 1 ok; out ← 3
i=4: pop 3,2,1 (all <=5); dq=[4]; out ← 5
i=5: dq=[4,5]; out ← 5
i=6: pop 5,4; dq=[6]; out ← 6
i=7: pop 6; dq=[7]; out ← 7
→ [3,3,5,5,6,7]
```

**Why deque not stack?** Need O(1) remove from **front** (expired indices) and **back** (dominated values).

**Interview talk:** "Monotonic decreasing deque; front is always the max of the current window."

---

# PART 5: BFS QUEUE PREVIEW (GRAPHS OWN BFS)

```python
from collections import deque

def bfs_preview(start, graph):
    q = deque([start])
    seen = {start}
    while q:
        node = q.popleft()
        for nei in graph[node]:
            if nei not in seen:
                seen.add(nei)
                q.append(nei)
```

**What you need from this module:** queue = FIFO = process earlier discoveries first → level order.

**What you do NOT need to master yet:** graph representations, shortest path proofs, multi-source BFS, 0-1 BFS. Those live in **Graphs I**. Label any graph BFS drill as **PREVIEW — no mastery credit** until that module.

Trees' level-order traversal is the same queue idea — full treatment in **Trees**.

---

# PART 6: EDGE CASES & TRAPS

| Trap | Fix |
|---|---|
| `list.pop(0)` as queue | Use `deque.popleft()` |
| Valid parentheses by counting only | Stack for order |
| Min stack scanning on getMin | Store running min |
| Monotonic stack storing values only | Store **indices** |
| Histogram width off-by-one | Sentinels + `i - stack[-1] - 1` |
| Sliding window forgetting expire | `if dq[0] <= i - k: popleft` |
| Decode string single-digit only | Accumulate multi-digit |
| Asteroid: same-direction collide | Only + then - can collide |
| Empty stack peek/pop | Guard `if stack` |

---

# PART 7: INTERVIEW WORKFLOW

1. **Identify access pattern** — LIFO nesting? FIFO order? Nearest greater? Window max?
2. **Pick structure** — list stack / deque queue / monotonic stack / monotonic deque.
3. **State invariant** — "stack is decreasing by temperature"; "deque front is max index in window."
4. **Complexity** — argue each element pushed/popped ≤ once → O(n).
5. **Trace** a small array on the whiteboard.
6. **Edge cases** — empty, k=1, all equal, strictly decreasing (next greater all -1).

**Phrase bank:**
- "Each index is pushed and popped at most once, so O(n)."
- "I'll keep a monotonic decreasing stack of indices."
- "For the queue I'll use `deque` for O(1) popleft."
- "BFS uses a queue; I'll treat deep graph BFS as a later module."

---

# PART 8: CHEAT SHEET

## ADT → Python

| ADT | Python | Core ops |
|---|---|---|
| Stack | `list` | `append`, `pop`, `[-1]` |
| Queue | `deque` | `append`, `popleft` |
| Deque | `deque` | both ends O(1) |

## Pattern → Structure

| Pattern | Tool |
|---|---|
| Brackets / nesting / decode | Stack |
| Min in O(1) | Stack of (val, min) |
| Queue via stacks | Two stacks |
| Next greater / daily temps | Monotonic decreasing stack |
| Histogram largest rectangle | Monotonic increasing stack |
| Sliding window max | Monotonic decreasing deque |
| Asteroid collision | Stack simulation |
| BFS / level order | Queue (preview / trees / graphs) |

## Monotonic One-Liners

- **Next greater right:** pop while `stack_top < me`; those popped get me as answer.
- **Window max:** deque decreasing; expire front; pop back dominated; front is max.

## Complexity

| Problem | Time | Space |
|---|---|---|
| Valid parentheses | O(n) | O(n) |
| Min stack ops | O(1) | O(n) |
| Queue via stacks | amort. O(1) | O(n) |
| Decode string | O(n × output) | O(n) |
| Asteroid | O(n) | O(n) |
| Next greater / daily temps | O(n) | O(n) |
| Histogram | O(n) | O(n) |
| Sliding window max | O(n) | O(k) |

---

# PART 9: WORKED PROBLEMS

---

### Problem 1: Valid Parentheses

```
Input: "()[]{}"
Output: True

Input: "([)]"
Output: False
```

## Pattern Identification

**Stack matching** — order matters, not just counts.

## Solution

```python
def is_valid(s):
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in match.values():
            stack.append(ch)
        elif ch in match:
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()
        else:
            return False
    return not stack
```

## Trace: `"([)]"`

```
( push
[ push
) need (; top is [ → False
```

## Edge Cases

- `""` → True
- `"("` → False (non-empty stack)
- `")"` → False (empty on close)

## Complexity

**Time O(n), Space O(n)**

---

### Problem 2: Min Stack

Implement `push`, `pop`, `top`, `getMin` all O(1).

## Pattern Identification

**Augmented stack** — store min-so-far with each entry.

## Solution

(See Part 2 Pattern 2 — `stack` of `(val, min_so_far)`.)

## Trace

```
push(-2), push(0), push(-3)
getMin → -3
pop
top → 0
getMin → -2
```

## Complexity

**O(1) time per op, O(n) space**

---

### Problem 3: Daily Temperatures

```
Input: [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

## Pattern Identification

**Monotonic decreasing stack** — next greater by index distance.

## Solution

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    ans = [0] * n
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
```

## Trace Through Main Example

```
i0 73 stack[0]
i1 74 pop0 ans0=1 stack[1]
i2 75 pop1 ans1=1 stack[2]
i3 71 stack[2,3]
i4 69 stack[2,3,4]
i5 72 pop4 ans4=1; pop3 ans3=2; stack[2,5]
i6 76 pop5 ans5=1; pop2 ans2=4; stack[6]
i7 73 stack[6,7]
ans=[1,1,4,2,1,1,0,0]
```

## Edge Cases

- Strictly decreasing → all 0
- Strictly increasing → all 1s except last 0
- Single element → [0]

## Complexity

**Time O(n), Space O(n)**

## Interview Talk

"Same skeleton as next greater element; I store indices and write `i - j` into the answer."

---

### Problem 4: Sliding Window Maximum

```
Input: nums=[1,3,-1,-3,5,3,6,7], k=3
Output: [3,3,5,5,6,7]
```

## Pattern Identification

**Monotonic decreasing deque.**

## Solution

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

## Trace

(See Part 4 full trace → `[3,3,5,5,6,7]`)

## Edge Cases

- `k=1` → output equals nums
- `k=n` → single max
- All equal → that value each window

## Complexity

**Time O(n), Space O(k)**

---

### Problem 5: Largest Rectangle in Histogram

```
Input: [2,1,5,6,2,3]
Output: 10
```

## Pattern Identification

**Monotonic increasing stack** + previous/next smaller → width.

## Solution

```python
def largest_rectangle_area(heights):
    h = [0] + heights + [0]
    stack = [0]
    best = 0
    for i in range(1, len(h)):
        while h[i] < h[stack[-1]]:
            height = h[stack.pop()]
            width = i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best
```

## Trace (key moment)

```
When processing the bar of height 2 after 5,6:
  finalize height 6 with width 1 → 6
  finalize height 5 with width 2 → 10 ← answer
```

## Edge Cases

- `[1]` → 1
- `[1,1,1]` → 3
- Increasing then drop — sentinels flush remaining bars

## Complexity

**Time O(n), Space O(n)**

---

### Problem 6: Decode String

```
Input: "3[a2[c]]"
Output: "accaccacc"

Input: "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

## Pattern Identification

**Stack for nesting** — push context on `[`, pop on `]`.

## Solution

(See Part 2 Pattern 4.)

## Trace: `"2[abc]3[cd]ef"`

```
2 [ → push ("",2)
abc ] → cur = "" + "abc"*2 = "abcabc"
3 [ → push ("abcabc",3)
cd ] → cur = "abcabc" + "cd"*3 = "abcabccdcdcd"
ef → cur = "abcabccdcdcdef"
```

## Edge Cases

- `"10[a]"` — multi-digit
- Nested deep `"2[2[a]]"` → `"aaaa"`
- Trailing letters outside brackets

## Complexity

**Time O(n + output size), Space O(n + output)**

---

### Problem 7: Asteroid Collision

```
Input: [5,10,-5]
Output: [5,10]

Input: [-2,-1,1,2]
Output: [-2,-1,1,2]  # never meet
```

## Pattern Identification

**Stack simulation** — only right-moving top vs left-moving incoming collide.

## Solution

(See Part 2 Pattern 5.)

## Trace: `[8,-8]`

```
8 → [8]
-8 vs 8 equal → both die → []
```

## Edge Cases

- All positive / all negative → no collisions
- Equal size opposite → both explode

## Complexity

**Time O(n), Space O(n)**

---

### Problem 8: Next Greater Element I (subset variant)

`nums1` is subset of `nums2`. For each in nums1, find next greater in nums2.

```
nums1=[4,1,2], nums2=[1,3,4,2]
Output: [-1,3,-1]
```

## Pattern Identification

**Monotonic stack on nums2** → map value→next greater; query nums1.

## Solution

```python
def next_greater_element(nums1, nums2):
    nxt = {}
    stack = []
    for x in nums2:
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x
        stack.append(x)
    return [nxt.get(x, -1) for x in nums1]
```

## Trace

```
nums2: 1 → [1]
3 → nxt[1]=3; [3]
4 → nxt[3]=4; [4]
2 → [4,2]
map: 1→3, 3→4
nums1: 4→-1, 1→3, 2→-1
```

## Complexity

**Time O(n), Space O(n)**

---

### Problem 9: Evaluate Reverse Polish Notation

```
Input: ["4","13","5","/","+"]
Output: 6   # 4 + (13/5)
```

## Pattern Identification

**Stack of operands** — operators pop two, push one.

## Solution

```python
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t not in '+-*/':
            stack.append(int(t))
            continue
        b, a = stack.pop(), stack.pop()
        if t == '+': stack.append(a + b)
        elif t == '-': stack.append(a - b)
        elif t == '*': stack.append(a * b)
        else: stack.append(int(a / b))
    return stack[0]
```

## Trace

```
4 → [4]
13 → [4,13]
5 → [4,13,5]
/ → a=13,b=5 → 2 → [4,2]
+ → a=4,b=2 → 6 → [6]
```

## Edge Cases

- Single number token list
- Division truncates toward zero (`int(a/b)` in Py3)

## Complexity

**Time O(n), Space O(n)**

## Interview Talk

"RPN exists so precedence is already encoded in order — the stack never needs to peek at operators waiting. I stress pop order: right operand first."

---

### Problem 10: Basic Calculator II

```
Input: "3+2*2"
Output: 7

Input: " 3/2 "
Output: 1
```

## Pattern Identification

**Signed-term stack** — `*`/`/` reduce immediately; `+`/`-` push signed values; sum at end.

## Solution

```python
def calculate(s):
    s = s.replace(' ', '')
    stack = []
    num = 0
    op = '+'
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in '+-*/' or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            else:  # /
                stack.append(int(stack.pop() / num))
            op = ch
            num = 0
    return sum(stack)
```

## Trace: `"3+2*2"`

```
'+' before 3 → push 3
'+' then 2 → push 2
'*' then 2 → pop 2*2 push 4
sum 3+4=7
```

## Edge Cases

- Spaces — strip or skip
- Multi-digit numbers
- Division toward zero (`int(a/b)`)

## Complexity

**Time O(n), Space O(n)**

## Interview Talk

"Plus/minus push signed terms; multiply/divide fold into the last term. That encodes precedence without a full parser."

---

### Problem 11: Next Greater Element II (circular)

Same as next greater, but array is **circular**.

```
Input: [1,2,1]
Output: [2,-1,2]
```

## Pattern Identification

**Monotonic stack + scan twice** (or indices `0..2n-1` with `i % n`).

## Solution

```python
def next_greater_elements(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []
    for i in range(2 * n):
        x = nums[i % n]
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        if i < n:
            stack.append(i)
    return ans
```

## Trace

```
[1,2,1], n=3
i=0: stack[0]
i=1: pop0 ans0=2; stack[1]
i=2: 2!<1; stack[1,2]
i=3: x=1; ...
i=4: x=2; pop2 ans2=2; 2!<2 for stack[1]
i=5: ...
ans=[2,-1,2]
```

## Complexity

**Time O(n), Space O(n)** — still each index pushed once.

## Interview Talk

"Circular means I simulate two passes. I only push indices on the first pass so I don't duplicate stack entries."

---

### Problem 12: Remove K Digits (monotonic stack)

Given string num and integer k, return the smallest possible integer after removing k digits.

```
Input: num = "1432219", k = 3
Output: "1219"
```

## Pattern Identification

**Monotonic increasing digit stack** — pop larger previous digits while removals remain.

## Solution

```python
def remove_k_digits(num, k):
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    # if k left, remove from end
    if k:
        stack = stack[:-k]
    # strip leading zeros
    return ''.join(stack).lstrip('0') or '0'
```

## Trace: `"1432219", k=3`

```
1 → [1]
4 → [1,4]
3 → pop4 (k=2); [1,3]
2 → pop3 (k=1); [1,2]
2 → [1,2,2]
1 → pop2 (k=0); [1,2,1]
9 → [1,2,1,9]
→ "1219"
```

## Edge Cases

- Remove all digits → `"0"`
- Ascending digits → remove from the end
- Leading zeros after strip

## Complexity

**Time O(n), Space O(n)**

---

### Problem 13: Sliding Window Maximum — second full trace

```
nums=[9,8,7,6], k=2 → [9,8,7]
```

```
i=0,x=9: dq=[0]
i=1,x=8: 9>8 keep; dq=[0,1]; expire? 0<=1-2? no; out←9
i=2,x=7: 8>7 keep; dq=[0,1,2]; expire 0<=0 → popleft →[1,2]; out←8
i=3,x=6: 7>6 keep; dq=[1,2,3]; expire 1<=1 → popleft →[2,3]; out←7
→ [9,8,7]
```

**Interview talk:** "I pop back while `nums[back] <= x` so newer equals replace older — either `<=` or `<` works if you stay consistent; expire check is mandatory."

---

### Problem 14: Implement Stack using Queues (symmetric classic)

```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]

    def empty(self):
        return not self.q
```

**Idea:** After each push, rotate so newest is at front — popleft = stack pop.  
**Tradeoff:** push O(n), pop O(1). (Queue-via-stacks was the dual.)

---

# PART 9B: INTERVIEW SCRIPT BANK (STACKS & QUEUES)

**Monotonic stack opener:**  
"I'll keep a monotonic stack of indices. When the ordering breaks, the current element is the next greater/smaller for everyone I pop. Each index enters and leaves at most once, so O(n)."

**Window max:**  
"Deque of indices in decreasing value order. Front is the max. I drop expired fronts and dominated backs before inserting."

**Calculator II:**  
"I scan with a previous operator. Plus and minus push signed numbers. Times and divide mutate the last number on the stack so precedence falls out naturally. Final answer is the sum of the stack."

**Histogram:**  
"Sentinel zeros on both ends. Increasing stack. When I see a shorter bar I finalize popped heights with width = i - new_top - 1."

**Valid parentheses:**  
"Stack of openers. A closer must match the top. Empty stack at the end. Counting alone fails on interleaved cases like ([)]."

---

# PART 10: CONNECTION TO PRIOR MODULES

| Prior | Connection |
|---|---|
| Arrays / sliding window | Monotonic deque is the O(n) upgrade for window max |
| Recursion / call stack | Explicit stack can simulate DFS; recursion *is* a stack |
| Hashing | Next Greater I uses map after stack pass |
| Linked lists | LRU ≈ ordered structure + map; stack/queue are simpler cousins |
| Binary search / sort | Not required for these patterns — don't force them |

---

# PART 11: STATUS & NEXT

| Item | Notes |
|---|---|
| This file | Concept delivery for Module 4 stacks/queues + monotonic |
| Drill | Blind: parentheses, daily temps, window max, histogram, decode, asteroids |
| Retention | `Retention Questions/Module 4 Retention.md` |
| First mini-mock | Due after Module 4 reaches `drilled` (Handoff Doc) |
| Graphs BFS | Preview only — mastery in Graphs I |

**Do not mark Complete** until retention + timed gates pass.

---

*End of Stacks & Queues — Complete Lesson*

---

# PART — SIMPLIFY PATH / IMPLEMENT `cd` (LC 71)

Unix absolute path → canonical path. Stack of directories.

## Rules

| Token | Action |
|---|---|
| `""` or `"."` | skip |
| `".."` | pop if stack non-empty |
| else | push directory name |

```python
def simplify_path(path: str) -> str:
    stack = []
    for tok in path.split('/'):
        if tok == '' or tok == '.':
            continue
        if tok == '..':
            if stack:
                stack.pop()
        else:
            stack.append(tok)
    return '/' + '/'.join(stack)
```

### Worked trace — `/a//b/../c/`

`split('/')` → `['', 'a', '', 'b', '..', 'c', '']`

| Token | Action | Stack |
|---|---|---|
| `""` | skip | [] |
| `a` | push | [a] |
| `""` | skip | [a] |
| `b` | push | [a, b] |
| `..` | pop | [a] |
| `c` | push | [a, c] |
| `""` | skip | [a, c] |

Result: `'/' + 'a/c'` → `/a/c`.

Second trace — `/../`: tokens `['', '..', '']` → `..` on empty stack is no-op → `/`.

**Interview:** Confirm absolute vs relative; Windows paths out of scope unless asked.

## Teach-back

Why `split('/')` and not char-by-char? What does `/a//b/../c/` become?
