<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 4 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 4 Retention.keys.md`. Attempt first, then grade.

# MODULE 4 RETENTION GRILL — LINKED LISTS + STACKS & QUEUES

**With answers.** Use blind first: cover the answer blocks, speak/write your solution, then check.

**Governance:** Cumulative light pull from Arrays, Hashing, Recursion, Binary Search, Sorting — only earned tools. Graph BFS depth = PREVIEW if it appears; do not treat as Module 4 credit.

**Pass bar (suggested):** Rapid fire ≥ 80% · Conceptual solid teach-back · Problems ≥ 6/8 first-pass correct reasoning (code may have small syntax slips if logic is right). Tag misses: knowledge-gap / misread / time-pressure / careless-slip.

---

# SECTION A: RAPID FIRE

Answer in one breath. Then check.

---

## A1. Why is `arr[i]` O(1) but walking to the i-th linked-list node O(n)?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 1)

## A2. Why do arrays often beat linked lists in practice for sequential scans even when both are O(n)?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 2)

## A3. Singly vs doubly: when do you need `prev`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 3)

## A4. What does a dummy head buy you?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 4)

## A5. Floyd cycle detection: slow +1, fast +2. If they meet, is there a cycle? How do you find the entrance?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 5)

## A6. Remove nth from end in one pass — what's the setup?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 6)

## A7. Stack vs queue in one sentence each. Python implementations?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 7)

## A8. Why is `list.pop(0)` wrong for a queue?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 8)

## A9. Monotonic stack: why O(n) for next greater?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 9)

## A10. Daily temperatures vs next greater — what's the only difference?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 10)

## A11. Sliding window maximum: why a deque, and what does the front represent?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 11)

## A12. Min stack: how is getMin O(1)?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 12)

## A13. Valid parentheses: why isn't counting open/close enough?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 13)

## A14. Recursion on a linked list: what's the hidden cost?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 14)

## A15. Intersection of two LLs: why `a is b`, not `a.val == b.val`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 15)

# SECTION B: CONCEPTUAL (TEACH-BACK)

Speak answers out loud like an interview. Then compare.

---

## B1. Walk through iterative reverse of `1→2→3`. Name the three pointers and the Save→Rewire→Advance order.


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 16)

## B2. Explain merge two sorted lists with a dummy. What do you do when one list empties?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 17)

## B3. Histogram largest rectangle: what does the monotonic stack find for each bar?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 18)

## B4. Queue via two stacks: where does the amortization come from?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 19)

## B5. Decode string `"3[a2[c]]"` — what is on the stack when you hit the first `]`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 20)

## B6. When would you choose a linked list over a dynamic array in an interview design question?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 21)

## B7. Cumulative — Arrays: Fixed sliding window sum vs variable window "min length with sum ≥ target" — one sentence each on the pointer motion.


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 22)

## B8. Cumulative — Hashing: Why is "two sum → indices" a hash map problem, not two pointers, on an unsorted array?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 23)

## B9. Cumulative — Recursion: Three components of every recursive function?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 24)

## B10. Cumulative — Binary search: What must be true about the search space?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 25)

# SECTION C: PROBLEMS (6–8) — FULL SOLUTIONS

For each: identify pattern, solve, trace, complexity. Answers included below each problem.

---

### Problem 1: Reverse Linked List (warm)

Reverse `1→2→3→4→5`. Return new head.

#### Answer

**Pattern:** Iterative 3-pointer reverse.

```python
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev
```

**Trace:** Links flip leftward; final `prev=5`.  
**Time O(n), Space O(1).**

---

### Problem 2: Linked List Cycle (detect only)

Return whether a cycle exists.

```
3→2→0→-4
  ↑______|
```

#### Answer

**Pattern:** Floyd.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

**Trace:** Eventually meet inside the loop.  
**Time O(n), Space O(1).**  
**Trap:** `slow.val == fast.val` is wrong.

---

### Problem 3: Remove Nth From End

`1→2→3→4→5`, n=2 → `1→2→3→5`. Also handle n = length (remove head).

#### Answer

**Pattern:** Dummy + gap-n two pointers.

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
```

**Trace:** fast starts at 2; after joint walk slow at 3; skip 4.  
n=5: fast at 5 after advance; `fast.next` None immediately; slow stays dummy; removes head.  
**Time O(n), Space O(1).**

---

### Problem 4: Daily Temperatures

`[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`

#### Answer

**Pattern:** Monotonic decreasing stack of indices.

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

**Trace:** 76 resolves 72, then 75 (distance 4 from index 2).  
**Time O(n), Space O(n).**

---

### Problem 5: Sliding Window Maximum

`nums=[1,3,-1,-3,5,3,6,7], k=3` → `[3,3,5,5,6,7]`

#### Answer

**Pattern:** Monotonic decreasing deque.

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

**Time O(n), Space O(k).**  
**Trap:** Using a sorted structure per window → worse; forgetting to expire `dq[0]`.

---

### Problem 6: Decode String

`"3[a2[c]]"` → `"accaccacc"`

#### Answer

**Pattern:** Stack of `(prev_str, count)` on `[`.

```python
def decode_string(s):
    stack = []
    cur_str, cur_num = "", 0
    for ch in s:
        if ch.isdigit():
            cur_num = cur_num * 10 + int(ch)
        elif ch == '[':
            stack.append((cur_str, cur_num))
            cur_str, cur_num = "", 0
        elif ch == ']':
            prev, num = stack.pop()
            cur_str = prev + cur_str * num
        else:
            cur_str += ch
    return cur_str
```

**Trap:** `"12[a]"` needs multi-digit accumulation.  
**Time O(output size), Space O(n).**

---

### Problem 7: Asteroid Collision

`[5,10,-5]` → `[5,10]`  
`[10,2,-5]` → `[10]`  
`[-2,-1,1,2]` → `[-2,-1,1,2]`

#### Answer

**Pattern:** Stack; collide only while top > 0 and incoming < 0.

```python
def asteroid_collision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and stack and stack[-1] > 0 and a < 0:
            if stack[-1] < -a:
                stack.pop()
                continue
            if stack[-1] == -a:
                stack.pop()
            alive = False
        if alive:
            stack.append(a)
    return stack
```

**Time O(n), Space O(n).**

---

### Problem 8: Integration (LL + two pointers idea) — Palindrome Linked List

`1→2→2→1` → True. O(1) extra space preferred.

#### Answer

**Pattern:** Middle (slow/fast) + reverse second half + compare.

```python
def is_palindrome(head):
    if not head or not head.next:
        return True
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev = None
    cur = slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    p1, p2 = head, prev
    while p2:
        if p1.val != p2.val:
            return False
        p1, p2 = p1.next, p2.next
    return True
```

**Cumulative note:** Same "find middle / reverse / compare" skill family as array palindrome two-pointers — different structure.  
**Time O(n), Space O(1).**  
If mutation forbidden: copy to array O(n) space, then two-pointer (Arrays skill).

---

### Problem 9 (bonus cumulative light): Two Sum indices

Unsorted `nums=[2,7,11,15], target=9` → `[0,1]`.

#### Answer

**Pattern:** Hash map (Module 2) — not monotonic stack, not LL.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
```

**Time O(n), Space O(n).**  
**Point:** Pattern ID under fatigue — Module 4 tools aren't always the answer.

---

### Problem 10 (bonus cumulative light): Binary search lower bound

First index in sorted `arr` with `arr[i] >= target`, or `len(arr)`.

#### Answer

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Point:** Monotonic predicate on a sorted array — BS module, not monotonic *stack*.

---

### Problem 11: Merge Two Sorted Lists

`1→2→4` and `1→3→4` → `1→1→2→3→4→4`.

#### Answer

**Pattern:** Dummy + two-pointer merge (LL).

```python
def merge_two_lists(list1, list2):
    dummy = ListNode(0)
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
```

**Trace:** Pick 1 (l1), 1 (l2), 2, 3, 4, attach leftover 4.  
**Trap:** Forgetting leftover attach.  
**Time O(n+m), Space O(1).**

---

### Problem 12: Rotate List

`1→2→3→4→5`, k=2 → `4→5→1→2→3`. Also k=7 (same as k=2).

#### Answer

**Pattern:** Length + ring + break.

```python
def rotate_right(head, k):
    if not head or not head.next:
        return head
    n, tail = 1, head
    while tail.next:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
```

**Trace:** n=5, k%=2; ring; new_tail at 3; open before 4.  
**Time O(n), Space O(1).**

---

### Problem 13: Reorder List

`1→2→3→4→5` → `1→5→2→4→3` (in place).

#### Answer

**Pattern:** Middle + reverse second half + weave.

```python
def reorder_list(head):
    if not head or not head.next:
        return
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev, cur = None, slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    first, second = head, prev
    while second.next:
        t1, t2 = first.next, second.next
        first.next = second
        second.next = t1
        first, second = t1, t2
```

**Composition check:** Same three moves as palindrome LL setup.  
**Time O(n), Space O(1).**

---

### Problem 14: Largest Rectangle in Histogram

`[2,1,5,6,2,3]` → `10`.

#### Answer

**Pattern:** Monotonic increasing stack + sentinels.

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

**Key moment:** When the bar after 6 arrives (height 2), finalize 6→area 6, then 5→area 10.  
**Time O(n), Space O(n).**

---

### Problem 15: Evaluate RPN

`["2","1","+","3","*"]` → `9`.

#### Answer

**Pattern:** Operand stack.

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
            else: stack.append(int(a / b))
    return stack[-1]
```

**Trap:** Pop `b` then `a` (right operand first).  
**Time O(n), Space O(n).**

---

### Problem 16: Cumulative — Product of Array Except Self

`[1,2,3,4]` → `[24,12,8,6]`. O(n) time, no division. (Arrays)

#### Answer

**Pattern:** Prefix/suffix products (or left pass + right pass into output).

```python
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
```

**Trace:** left pass → `[1,1,2,6]`; right multiplies → `[24,12,8,6]`.  
**Time O(n), Space O(1) extra** (output doesn't count per LC convention).

---

### Problem 17: Cumulative — Subarray Sum Equals K (count)

`nums=[1,2,3], k=3` → `2` (`[1,2]`, `[3]`). (Hashing + prefix)

#### Answer

**Pattern:** Prefix sum + hash map of frequencies.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    pref = 0
    seen = defaultdict(int)
    seen[0] = 1
    for x in nums:
        pref += x
        count += seen[pref - k]
        seen[pref] += 1
    return count
```

**Why not sliding window?** Negatives allowed in the general problem — window fails.  
**Time O(n), Space O(n).**

---

### Problem 18: Cumulative — Recursion: Subsets

`nums=[1,2]` → `[[],[1],[2],[1,2]]`.

#### Answer

**Pattern:** Decision tree include/exclude (Recursion module).

```python
def subsets(nums):
    res = []
    def dfs(i, path):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])
        dfs(i + 1, path)
        path.pop()
        dfs(i + 1, path)
    dfs(0, [])
    return res
```

**Time O(n·2ⁿ), Space O(n) recursion (+ output).**  
**Not a stack/queue problem** — if you reach for monotonic stack here, stop.

---

### Problem 19: Cumulative — Sort + two pointers: 3Sum sketch

`nums=[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`.

#### Answer

**Pattern:** Sort, fix i, two pointers on remainder. Skip duplicates.

```python
def three_sum(nums):
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n):
        if i and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return res
```

**Time O(n²), Space O(1) extra** (ignoring output). Sorting is the Module 3 tool that unlocks ordered two pointers.

---

### Problem 20: Valid Parentheses + Min Stack combo check

(1) Is `"{[()]}"` valid? (2) After pushes 3,5,2,7 and one pop, what is getMin?

#### Answer

(1) **True** — stack empties cleanly: push `{ [ (`, then pop matching `) ] }`.

(2) Stack of `(val,min)`:  
`(3,3),(5,3),(2,2),(7,2)` → pop → `(3,3),(5,3),(2,2)` → **getMin = 2**.

---

# SECTION C2: TIMED-STYLE BLINDS (ANSWERS BELOW THE FOLD)

Do these with a 25-minute timer. No pattern labels.

---

### Blind 1: Swap Nodes in Pairs

`1→2→3→4` → `2→1→4→3`.

<details>
<summary>Answer</summary>

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next
        prev.next, a.next, b.next = b, b.next, a
        prev = a
    return dummy.next
```

**Time O(n), Space O(1).**
</details>

---

### Blind 2: Next Greater Element II (circular)

`[1,2,1]` → `[2,-1,2]`.

<details>
<summary>Answer</summary>

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

**Time O(n), Space O(n).**
</details>

---

### Blind 3: Intersection of Two Linked Lists

Explain the O(1)-space two-pointer switch in 4 sentences, then code.

<details>
<summary>Answer</summary>

Pointers `a` and `b` walk their lists. When one hits None, redirect to the other list's head. Both travel `|A|+|B|`, so they meet at the first shared node (or both None). Compare with `is`.

```python
def get_intersection_node(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
```
</details>

---

### Blind 4: Cumulative — Min Size Subarray Sum (positives)

`target=7, nums=[2,3,1,2,4,3]` → `2`.

<details>
<summary>Answer</summary>

**Variable sliding window** (Arrays). Expand right; while sum ≥ target shrink left; track min length.

```python
def min_subarray_len(target, nums):
    left = 0
    s = 0
    best = float('inf')
    for right, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, right - left + 1)
            s -= nums[left]
            left += 1
    return 0 if best == float('inf') else best
```

**Time O(n), Space O(1).**
</details>

---

# SECTION D: TRAP GALLERY (SPOT THE BUG)

---

## D1.

```python
def reverse(head):
    prev = None
    cur = head
    while cur:
        cur.next = prev
        prev = cur
        cur = cur.next  # ???
    return prev
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 26)

## D2.

```python
q = []
q.append(1)
q.append(2)
x = q.pop(0)  # as queue
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 27)

## D3.

```python
# next greater
while stack and stack[-1] < nums[i]:
    ans[stack.pop()] = nums[i]
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 28)

## D4.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow.val == fast.val:
            return True
    return False
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 29)

## D5.

```python
def daily_temperatures(T):
    ans = [0] * len(T)
    stack = []
    for i, t in enumerate(T):
        while stack and T[stack[-1]] < t:
            j = stack.pop()
            ans[j] = t - T[j]  # ???
        stack.append(i)
    return ans
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 30)

## D6.

```python
def max_sliding_window(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        # missing expire
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 31)

## D7.

```python
def merge(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    return dummy.next  # ???
```


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 32)

# SECTION E: INTERVIEW TALK RUBRIC (SELF-SCORE 1–5)

After a timed problem, score yourself:

| Dimension | 5 looks like |
|---|---|
| Clarity | Named pointers/invariant before coding |
| Correctness | Edge cases: empty, single, head delete, k=1 |
| Complexity | "Each index push/pop ≤ once → O(n)" said explicitly |
| Code quality | Dummy head / deque choice justified |
| Recovery | Found own bug on trace without hint |

Module 4 starts **mini-mocks** after `drilled` (Handoff Doc §2E). Aim ≥ 4.0 average over time.

### Sample 30-second openers (memorize tone, not script)

- **LL reverse:** "Three pointers, save-next then rewire, O(1) space; return prev."
- **Floyd:** "Meet proves cycle; reset to head finds entrance; identity compare."
- **Daily temps:** "Decreasing monotonic stack of indices; answer is i−j."
- **Window max:** "Decreasing deque; front is max; expire and dominate."
- **Histogram:** "Increasing stack with zero sentinels; width = i − top − 1."

---

# SECTION F: HEAT MAP UPDATE (FILL AFTER GRILL)

| Subskill | strong / shaky / weak |
|---|---|
| Node rewiring / reverse | |
| Dummy head | |
| Floyd cycle | |
| Merge / remove nth / intersection | |
| Reorder / rotate / swap pairs | |
| Stack basics + parentheses | |
| Min stack / queue via stacks | |
| Monotonic stack (next greater, temps, histogram) | |
| Monotonic deque (window max) | |
| Decode / asteroids / RPN / calculator | |
| Cumulative arrays/hash/recursion/BS/sort | |

Ledger: copy due items into `Metrics/Retention Ledger.md`. Fail → shorten next due; `weak` twice → re-teach from the module file.

---

# SECTION G: ANSWER KEY QUICK INDEX

| ID | One-line key |
|---|---|
| A1 | Contiguous arithmetic vs pointer chase |
| A2 | Cache |
| A3 | LRU / O(1) delete known node |
| A4 | Stable prev for head changes |
| A5 | Meet ⇒ cycle; reset to head for entrance |
| A6 | Dummy + gap n |
| A7 | LIFO list / FIFO deque |
| A8 | pop(0) is O(n) |
| A9 | Push/pop ≤ once each |
| A10 | Distance vs value |
| A11 | Front = window max index |
| A12 | Store running min |
| A13 | Order / nesting |
| A14 | O(n) stack + recursion limit |
| A15 | Identity |
| P1–P8 | Section C core |
| P9–P10 | Two sum map; BS lower bound |
| P11–P15 | Merge, rotate, reorder, histogram, RPN |
| P16–P19 | Product except self; subarray sum k; subsets; 3Sum |
| P20 | Parens + min stack |
| Blinds | Swap pairs; circular NGE; intersection; min window |
| D1–D7 | Save nxt; deque; nums[idx]; `is`; i−j; expire; leftover |

---

# SECTION H: MORE RAPID FIRE (A16–A25)

---

## A16. Reorder list — name the three phases.


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 33)

## A17. Rotate right by k — why `k %= n`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 34)

## A18. RPN: after tokens `["4","13","5","/","+"]`, what is the stack just before `+`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 35)

## A19. Histogram sentinels — why height 0 on both ends?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 36)

## A20. Copy list with random pointer — hash map approach in one sentence.


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 37)

## A21. Asteroid: do `[-2,-1,1,2]` collide?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 38)

## A22. Cumulative — amortized append on dynamic array is O(1). Why?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 39)

## A23. Cumulative — why is `x in list` O(n) but `x in set` average O(1)?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 40)

## A24. Queue via stacks: when do you pour `in_s` into `out_s`?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 41)

## A25. Palindrome LL O(1) space — what do you reverse?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 42)

# SECTION I: CONCEPTUAL ROUND 2

---

## B11. Why store indices (not values) in a monotonic stack for daily temperatures?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 43)

## B12. Explain LRU at Module 4 depth (no full code required).


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 44)

## B13. Cumulative — Master Theorem flash: T(n)=2T(n/2)+O(n). Case and result?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 45)

## B14. When is sliding window the wrong tool for "subarray sum = k"?


> **Answer key:** `Retention Questions/keys/Module 4 Retention.keys.md` (block 46)

