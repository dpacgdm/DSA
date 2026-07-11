# LINKED LISTS — THE COMPLETE LESSON

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHAT A LINKED LIST ACTUALLY IS

## Why You Need To Know This

Arrays give you O(1) index access because elements sit in contiguous memory. Linked lists give you O(1) insert/delete **at a known node** because elements are connected by pointers, not by position.

If you only memorize "linked list = nodes with next," you will:
- Fail to choose between array and linked list under interview pressure
- Botch pointer rewiring (the #1 source of LL bugs)
- Miss that Floyd's cycle detection, "remove nth from end," and LRU all share the same pointer-skill family
- Not understand why real systems often prefer arrays/deques despite Big O favoring lists for inserts

This lesson builds the **mental model**, then the **rewiring frameworks**, then the **classic patterns**, then worked problems with full traces.

---

## 1A: The Node Model

A linked list is a chain of **nodes**. Each node holds:
1. A **value** (the data)
2. A **pointer/reference** to the next node (and optionally the previous)

```
Singly linked list:

  head
    ↓
┌─────────┐    ┌─────────┐    ┌─────────┐
│ val: 10 │ →  │ val: 20 │ →  │ val: 30 │ → None
│ next ───┼────┤ next ───┼────┤ next ───┼────
└─────────┘    └─────────┘    └─────────┘
```

**Critical vocabulary:**
- **Head** — first node. Your only guaranteed entry point for a singly linked list.
- **Tail** — last node. `tail.next is None` (for non-circular).
- **None / null** — the terminator. Losing the head without another reference = losing the whole list.

### Python Node

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

That's it. Interviews almost always use this (or an equivalent). You rarely need a full `LinkedList` class wrapper — you manipulate `ListNode` pointers directly.

### Building a List From Scratch

```python
def build_list(values):
    """[1,2,3] → 1 → 2 → 3 → None"""
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    """For debugging / asserts."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out
```

**Interview talk:** "I'll represent the list as `ListNode` objects. I'll keep a reference to the head, and I'll be careful never to lose the head while rewiring."

---

## 1B: Singly vs Doubly vs Circular

### Singly Linked List

```
A → B → C → None
```

- One pointer per node: `next`
- Forward traversal only
- Insert/delete at head: O(1)
- Insert/delete at known node: O(1) for *after* that node; deleting the node itself needs the previous pointer (or a clever overwrite trick)
- Memory: one pointer per node

### Doubly Linked List

```
None ← A ⇄ B ⇄ C → None
```

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

- Two pointers: `prev` and `next`
- Bidirectional traversal
- Delete a known node in O(1) **without** searching for previous (you already have `node.prev`)
- Extra memory; more rewiring bugs (must update both directions)
- **This is what LRU Cache uses** (with a hash map)

### Circular Linked List

```
A → B → C → A   (last points back to first)
```

- No natural `None` terminator — traversal must track start or use a counter
- Useful for round-robin scheduling, Josephus problem, circular buffers conceptually
- Cycle detection algorithms become "is this circular by design?" vs "is this a bug cycle?"

### Decision Snapshot

| Need | Prefer |
|---|---|
| Simple interview problems, reverse, merge | Singly |
| O(1) delete of arbitrary known node, LRU | Doubly |
| Round-robin / wrap-around | Circular (or deque) |
| Random access by index | **Array**, not LL |

---

## 1C: Why Linked Lists vs Arrays (Tradeoffs + Cache)

### Complexity Comparison (honest)

| Operation | Dynamic Array | Singly LL | Doubly LL |
|---|---|---|---|
| Access by index | O(1) | O(n) | O(n) |
| Search by value | O(n) | O(n) | O(n) |
| Insert/delete at head | O(n) shift / O(1) amortized append at end | O(1) | O(1) |
| Insert/delete at known node | O(n) shift | O(1)* | O(1) |
| Insert/delete at end (no tail ptr) | O(1) amortized | O(n) | O(n) / O(1) with tail |
| Extra memory per element | Low (contiguous) | 1 pointer | 2 pointers |
| Cache locality | Excellent | Poor | Poor |

\*Singly: O(1) to insert *after* a node, or to delete *next* of a node. Deleting the current node without `prev` is awkward.

### The Cache Reality (must be able to say this)

Arrays are contiguous → CPU cache prefetch wins.
Linked list nodes are heap-allocated → scattered addresses → cache misses on every hop.

**In practice:** for many workloads, an array/deque beats a linked list even when Big O looks the same for traversal, because constant factors and cache dominate.

**When LL still wins conceptually / in interviews:**
- You need O(1) splice/insert/delete given a node reference
- You are implementing structures that need pointer rewiring (LRU, some OS schedulers)
- The problem *is* about pointers (cycle detection, reverse, intersection)
- Interviewers want to test pointer manipulation skill

**Interview talk:**
> "Arrays win on random access and cache locality. Linked lists win when I already hold a node and need O(1) local rewiring. In Python interviews, I often still use lists for simplicity unless the problem forces a ListNode API."

---

# PART 2: IMPLEMENT FROM SCRATCH IN PYTHON

## 2A: Core Operations — Singly Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, val):
        """O(1) insert at front."""
        node = ListNode(val)
        node.next = self.head
        self.head = node

    def append(self, val):
        """O(n) without a tail pointer."""
        node = ListNode(val)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def find(self, val):
        """O(n). Return first matching node or None."""
        cur = self.head
        while cur:
            if cur.val == val:
                return cur
            cur = cur.next
        return None

    def delete_value(self, val):
        """Delete first node with val. O(n)."""
        dummy = ListNode(0, self.head)
        prev = dummy
        while prev.next:
            if prev.next.val == val:
                prev.next = prev.next.next
                break
            prev = prev.next
        self.head = dummy.next

    def length(self):
        n = 0
        cur = self.head
        while cur:
            n += 1
            cur = cur.next
        return n
```

### Trace: prepend then append

```
Start: head = None

prepend(2):
  node(2).next = None
  head → 2

prepend(1):
  node(1).next = 2
  head → 1 → 2

append(3):
  walk to 2, set 2.next = 3
  head → 1 → 2 → 3
```

---

## 2B: The Dummy Head Technique (Non-Negotiable)

**Problem:** special-casing "what if we delete/change the head?" creates bugs.

**Solution:** a fake node in front whose `.next` is the real head.

```python
dummy = ListNode(0)
dummy.next = head
# ... mutate using dummy as stable prev ...
return dummy.next  # real new head
```

### Why It Works

```
Before delete of head (val=1) in 1→2→3:

dummy → 1 → 2 → 3
prev = dummy

When prev.next.val == 1:
  prev.next = prev.next.next
  → dummy → 2 → 3

return dummy.next  # 2 → 3  (head correctly updated)
```

Without dummy, you'd write:
```python
if head and head.val == target:
    head = head.next
# then a separate loop for the rest — easy to miss
```

**Rule:** If the algorithm might change the head, start with a dummy.

**Interview talk:** "I'll use a dummy head so head deletion and middle deletion share one code path."

---

## 2C: Pointer Rewiring Mental Model

Every LL bug is one of:
1. Lost reference (overwrote `next` before saving what you needed)
2. Infinite loop (didn't advance, or created a cycle)
3. Off-by-one (stopped one node too early/late)
4. Forgot to return the new head

### The Safe Rewire Pattern

When changing links, **save before you overwrite**:

```python
# Reverse one link (iterative reverse fragment)
nxt = cur.next      # SAVE
cur.next = prev     # REWIRE
prev = cur          # ADVANCE
cur = nxt
```

Order mnemonic: **Save → Rewire → Advance**.

---

# PART 3: CORE PATTERNS

## Pattern Decision Framework

| Signal in the problem | Reach for |
|---|---|
| Reverse the list / reverse a segment | Iterative reverse (3 pointers) or recursion |
| Cycle? / find cycle start | Floyd (slow/fast) |
| Middle node / palindrome LL | Slow/fast (middle) |
| Merge two sorted lists | Dummy + two pointers |
| Remove nth from end | Two pointers gap of n |
| Intersection of two lists | Two-pointer switch / length align |
| Deep copy with random ptr | Hash map of old→new, or interweave |
| O(1) get + O(1) put cache | Hash map + doubly LL (LRU) |
| Delete node given only that node | Copy next's value (trick) / need prev normally |

---

## Pattern 1: Reverse a Linked List

### Framework (Iterative — preferred in interviews)

```
prev = None
cur = head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
return prev  # new head
```

### Trace

```
1 → 2 → 3 → None

init: prev=None, cur=1

step1: nxt=2, 1.next=None, prev=1, cur=2
  None ← 1    2 → 3 → None

step2: nxt=3, 2.next=1, prev=2, cur=3
  None ← 1 ← 2    3 → None

step3: nxt=None, 3.next=2, prev=3, cur=None
  None ← 1 ← 2 ← 3

return prev=3
```

### Recursive Reverse

```python
def reverse_list(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**Leap of faith:** `reverse_list(head.next)` returns the new head of the reversed suffix. Then attach current node to the end of that suffix via `head.next.next = head`.

**Space:** iterative O(1) extra; recursive O(n) stack. Prefer iterative unless asked for recursion.

---

## Pattern 2: Detect Cycle — Floyd's Tortoise and Hare

### Why It Works (intuition)

Slow moves 1, fast moves 2. If there's a cycle, fast enters the loop and gains on slow by 1 node per iteration → they must meet.

If no cycle, fast hits `None`.

### Detect Only

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

### Find Cycle Start (Interview Classic)

After they meet, put one pointer back at head. Move both 1 step at a time. Where they meet is the cycle entrance.

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow  # entrance
    return None
```

### Trace (cycle at node 2)

```
1 → 2 → 3 → 4
    ↑         │
    └─────────┘

Meet phase:
s,f at 1
s→2, f→3
s→3, f→2
s→4, f→4  MEET at 4

Entrance phase:
slow=1, fast=4
slow=2, fast=2  MEET at 2 ← entrance ✅
```

**Math sketch (interview-level):**  
Let L = head→entrance, C = cycle length, a = steps from entrance to the first meeting point.  
Slow travels L+a; fast travels 2(L+a). Their difference L+a is a multiple of C, so **L ≡ −a (mod C)**.  
Reset one pointer to head; both walk 1 step/turn. After L steps the head-pointer is at the entrance, and the cycle-pointer has also advanced L ≡ −a (mod C) from offset a → entrance.

**TRAP:** Comparing values (`slow.val == fast.val`) is wrong — compare **identity** (`slow is fast`).

---

## Pattern 3: Find the Middle

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

- Odd length: exact middle
- Even length: the **second** middle (LeetCode convention) when using this template

```
1→2→3→4→5  → middle 3
1→2→3→4    → middle 3
```

**Uses:** palindrome check (reverse second half), split list for merge sort on LL.

---

## Pattern 4: Merge Two Sorted Lists

### Framework

```
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

### Trace

```
l1: 1 → 2 → 4
l2: 1 → 3 → 4

pick 1 (l1), pick 1 (l2), pick 2, pick 3, pick 4, attach remaining 4
→ 1 → 1 → 2 → 3 → 4 → 4
```

**TRAP:** Forgetting to attach the leftover list after the loop.

---

## Pattern 5: Remove Nth Node From End

### Framework (one pass, two pointers)

```
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

Gap of n between fast and slow → when fast is at last node, slow is just before the victim.

### Trace: remove 2nd from end in 1→2→3→4→5

```
n=2
dummy→1→2→3→4→5
fast advances 2: at 2
then move both until fast.next is None:
  fast at 5, slow at 3
slow.next = slow.next.next  → remove 4
result: 1→2→3→5
```

**TRAP:** Removing the head (n == length) — dummy handles it.

---

## Pattern 6: Intersection of Two Linked Lists

Two lists share a suffix (same nodes by identity, not just values).

### Elegant O(1) Space

```python
def get_intersection_node(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a  # either intersection node or None
```

**Why:** Both pointers travel `|A| + |B|`. If intersection exists, they meet there; else both become None together.

### Trace

```
A: 4 → 1 → 8 → 4 → 5
B: 5 → 6 → 1 → 8 → 4 → 5
              ↑ shared from 8

After switch, both reach 8 at same time.
```

**TRAP:** Comparing `a.val == b.val` — must be `a is b`.

---

## Pattern 7: Copy List with Random Pointer

Each node has `next` and `random` (may point anywhere or None). Deep copy the whole graph of nodes.

### Approach A — Hash Map (clearest)

```python
def copy_random_list(head):
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next
    return old_to_new[head]
```

### Approach B — Interweave (O(1) extra space)

1. Clone each node and insert after original: `A→A'→B→B'`
2. Set `A'.random = A.random.next` (if A.random exists)
3. Unweave into original and copy lists

**Interview talk:** Prefer hash map unless they demand O(1) space.

---

## Pattern 8: LRU Cache Connection

**LRU = Hash Map + Doubly Linked List**

- Map: `key → node` for O(1) lookup
- DLL: most-recent at head (or tail — pick a convention and stick to it), least-recent at the other end
- `get`: move node to MRU position
- `put`: if full, evict LRU node; insert new as MRU

```
Map: {1: node1, 2: node2, 3: node3}

DLL (MRU ← ... → LRU):
  node2 ⇄ node1 ⇄ node3
```

Why doubly? Need O(1) remove from middle when a key is refreshed.

**This module's job:** understand *why* DLL appears. Full LRU implementation is often asked — treat coding it as a drill after this lesson.

---

## Pattern 9: Reorder List (compose three skills)

`L0→L1→…→Ln` becomes `L0→Ln→L1→Ln-1→…`.

```
Framework:
  1. slow/fast → middle (start of second half)
  2. reverse second half
  3. weave: first.next = second; second.next = first_next; advance both
```

**Why this is a mastery check:** You are not learning a fourth exotic trick — you are proving you can **compose** middle + reverse + merge without losing pointers.

**Interview talk:** "I'll solve this as three familiar passes. The weave stop condition is the only delicate part — I always trace both odd and even lengths."

---

## Pattern 10: Rotate List

Rotate right by k:

```
Framework:
  1. find n and tail
  2. k %= n; if k==0 return head
  3. tail.next = head          # ring
  4. walk n-k-1 steps from head to new_tail
  5. new_head = new_tail.next; new_tail.next = None
```

**Mental model:** Cutting a necklace and rejoining at a different clasp.

**TRAP:** Forgetting `k %= n`. Forgetting to break the ring (`new_tail.next = None`) → infinite loop for the caller.

---

# PART 4: RECURSION ON LINKED LISTS

Linked lists are recursive structures: a node + a smaller list (`head.next`).

### Template

```python
def solve(head):
    if head is None:          # base: empty
        return ...
    if head.next is None:     # base: single node (sometimes)
        return ...
    # recurse on head.next, then combine with head
```

### Examples

```python
def list_sum(head):
    if not head:
        return 0
    return head.val + list_sum(head.next)


def print_reverse(head):
    if not head:
        return
    print_reverse(head.next)
    print(head.val)
```

**Space:** O(n) call stack — mention this in interviews.

**When recursion shines:** reverse, merge (recursive merge is clean), some "swap pairs" solutions.

**When iteration wins:** long lists (Python recursion limit ~1000), tight O(1) space requirements.

---

# PART 5: EDGE CASES & TRAPS

## Edge Case Checklist

| Case | What breaks |
|---|---|
| Empty list (`head is None`) | Null deref |
| Single node | Reverse, remove nth, middle |
| Two nodes | Even-middle, swap pairs |
| Remove head | Need dummy or explicit head update |
| Remove tail | Off-by-one in two-pointer gap |
| All equal values | Delete duplicates logic |
| Cycle present when not expected | Infinite loop |
| Intersection by value not identity | Wrong node |
| Random pointer None | Copy random |

## Classic Traps

1. **Losing the head** — always keep `dummy` or `new_head`.
2. **`cur = cur.next` after `cur.next = ...` without saving** — lost the rest of the list.
3. **Value equality vs identity** — cycles and intersection need `is`.
4. **Forgetting leftover merge** — `tail.next = list1 or list2`.
5. **Even-length middle** — confirm which middle the problem wants.
6. **Recursive reverse without `head.next = None`** — creates a cycle.
7. **Assuming index access** — `lst[i]` is not a thing on ListNode; walk or convert.

---

# PART 6: INTERVIEW WORKFLOW FOR LL PROBLEMS

1. **Clarify API** — singly or doubly? Can I use extra space? Modify in place?
2. **Draw 3–5 nodes** — literally boxes and arrows on paper/whiteboard.
3. **Name pointers** — `prev`, `cur`, `nxt`, `slow`, `fast`, `dummy`.
4. **State the invariant** — e.g. "nodes before `prev` are already reversed."
5. **Code** — small steps; rewire with Save→Rewire→Advance.
6. **Trace one example + empty + single node.**
7. **Complexity** — time usually O(n); space O(1) or O(n) if hash/recursion.

**Phrase bank:**
- "I'll use a dummy head to unify edge cases."
- "Two pointers with a gap of n finds the node before the target from the end."
- "Floyd's algorithm gives cycle detection in O(1) space."
- "Arrays would be simpler here, but the signature forces ListNode manipulation."

---

# PART 7: CHEAT SHEET

## Complexity

| Pattern | Time | Extra Space |
|---|---|---|
| Traverse | O(n) | O(1) |
| Reverse (iterative) | O(n) | O(1) |
| Reverse (recursive) | O(n) | O(n) stack |
| Has cycle / find entrance | O(n) | O(1) |
| Middle | O(n) | O(1) |
| Merge two sorted | O(n+m) | O(1) |
| Remove nth from end | O(n) | O(1) |
| Intersection | O(n+m) | O(1) |
| Copy with random (hash) | O(n) | O(n) |
| LRU get/put | O(1) | O(capacity) |

## Templates to Memorize

```python
# Dummy
dummy = ListNode(0, head)

# Reverse
prev, cur = None, head
while cur:
    nxt = cur.next
    cur.next = prev
    prev, cur = cur, nxt

# Floyd
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast: ...

# Merge
# (dummy + compare + attach leftover)

# Remove nth from end
# (dummy + advance fast n + walk both)
```

## LL vs Array One-Liner

**Array:** index + cache. **LL:** local rewiring + no index.

---

# PART 8: WORKED PROBLEMS

---

### Problem 1: Reverse Linked List

Reverse a singly linked list. Return the new head.

```
Input: 1 → 2 → 3 → 4 → 5
Output: 5 → 4 → 3 → 2 → 1
```

## Pattern Identification

**Iterative three-pointer reverse.** Need O(1) extra space; classic rewiring.

## Solution

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```

## Trace Through Main Example

```
1→2→3→4→5

prev=None cur=1
  nxt=2; 1→None; prev=1 cur=2
prev=1 cur=2
  nxt=3; 2→1; prev=2 cur=3
prev=2 cur=3
  nxt=4; 3→2; prev=3 cur=4
prev=3 cur=4
  nxt=5; 4→3; prev=4 cur=5
prev=4 cur=5
  nxt=None; 5→4; prev=5 cur=None

return 5→4→3→2→1
```

## Edge Cases

- `None` → `None`
- Single node → same node
- Two nodes `1→2` → `2→1`

## Complexity Analysis

**Time:** O(n) — each node rewired once.  
**Space:** O(1)

## Interview Talk

"I'll iterate with prev/cur/next, reversing the link as I go, and return prev as the new head. Recursive works but uses O(n) stack."

---

### Problem 2: Linked List Cycle II (Find Entrance)

Return the node where the cycle begins, or `None`.

```
Input: 3 → 2 → 0 → -4
              ↑_________|
Output: node with val 2
```

## Pattern Identification

**Floyd meet + reset to head.**

## Solution

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

## Trace Through Main Example

```
3→2→0→-4
  ↑______|

Meet:
s,f=3
s=2,f=0
s=0,f=2
s=-4,f=-4  MEET

Reset slow=3, fast=-4
s=2,f=2  ENTRANCE ✅
```

## Edge Cases

- No cycle → `None`
- Cycle at head (full circle from first node)
- Single node with `next` to itself

## Complexity Analysis

**Time:** O(n)  
**Space:** O(1)

## Interview Talk

"After they meet inside the cycle, one pointer back to head; same-speed walk finds the entrance. I compare nodes by identity, not value."

---

### Problem 3: Middle of the Linked List

Return the middle node (second middle if even).

```
Input: 1→2→3→4→5→6
Output: 4→5→6
```

## Pattern Identification

**Slow/fast pointers.**

## Solution

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

## Trace Through Main Example

```
1→2→3→4→5→6
s=1 f=1
s=2 f=3
s=3 f=5
s=4 f=None (fast.next of 5 is 6, then fast=None after next iter)
Actually:
start s=1,f=1
loop: f and f.next → s=2,f=3
loop: s=3,f=5
loop: s=4,f=None (f was 5, f.next=6, f.next.next=None)
return 4 ✅
```

## Edge Cases

- One node → that node
- Two nodes → second node

## Complexity Analysis

**Time:** O(n)  
**Space:** O(1)

---

### Problem 4: Merge Two Sorted Lists

```
Input: 1→2→4 , 1→3→4
Output: 1→1→2→3→4→4
```

## Pattern Identification

**Dummy head + two-pointer merge** (same idea as merging sorted arrays, but with links).

## Solution

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
    tail.next = list1 if list1 else list2
    return dummy.next
```

## Trace Through Main Example

```
dummy→
compare 1 vs 1 → take list1's 1; tail at that 1
compare 2 vs 1 → take list2's 1
compare 2 vs 3 → take 2
compare 4 vs 3 → take 3
compare 4 vs 4 → take list1's 4
attach remaining list2's 4
→ 1→1→2→3→4→4
```

## Edge Cases

- One list empty → return the other
- Both empty → `None`
- Interleaved vs all of one list smaller

## Complexity Analysis

**Time:** O(n+m)  
**Space:** O(1) extra (reuses nodes)

## Interview Talk

"I reuse existing nodes — no new ListNode allocations except the dummy."

---

### Problem 5: Remove Nth Node From End of List

```
Input: 1→2→3→4→5, n=2
Output: 1→2→3→5
```

## Pattern Identification

**Dummy + two pointers with gap n.**

## Solution

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

## Trace Through Main Example

```
dummy→1→2→3→4→5, n=2
fast moves to 2
walk: fast→3 slow→1; fast→4 slow→2; fast→5 slow→3
fast.next is None → stop
slow.next = 5  (skip 4)
return 1→2→3→5
```

## Edge Cases

- n = length → remove head (dummy saves you)
- n = 1 → remove tail
- Single node, n=1 → empty list

## Complexity Analysis

**Time:** O(n)  
**Space:** O(1)

---

### Problem 6: Intersection of Two Linked Lists

```
A: a1→a2→c1→c2→c3
B: b1→b2→b3→c1→c2→c3
Return: c1
```

## Pattern Identification

**Two-pointer switch** (or length-align). O(1) space.

## Solution

```python
def get_intersection_node(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
```

## Trace Through Main Example

```
a path length to end + B prefix = b path length to end + A prefix
Both arrive at c1 synchronized.
If no intersection, both become None on the same iteration.
```

## Edge Cases

- No intersection → `None`
- Intersection at head of one list
- Different prefix lengths (the algorithm's whole point)

## Complexity Analysis

**Time:** O(n+m)  
**Space:** O(1)

---

### Problem 7: Palindrome Linked List

Return true if the linked list is a palindrome.

```
Input: 1→2→2→1
Output: True
```

## Pattern Identification

**Find middle + reverse second half + compare.** O(1) extra space (modifies list; can restore if required).

## Solution

```python
def is_palindrome(head):
    if not head or not head.next:
        return True

    # middle (first of second half for even: use slow/fast)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # reverse from slow
    prev = None
    cur = slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    second = prev

    # compare
    first = head
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    return True
```

## Trace Through Main Example

```
1→2→2→1
middle slow at second 2
reverse second half: 1→2
compare: 1==1, 2==2 → True
```

## Edge Cases

- Single node → True
- Two nodes equal/unequal
- Odd length `1→2→3→2→1` — middle 3 ignored on second half compare as first runs out in sync with second... actually second half includes middle; values still match for true palindromes when comparing while `second` remains.

## Complexity Analysis

**Time:** O(n)  
**Space:** O(1)

## Interview Talk

"I reverse the second half in place for O(1) space. If the interviewer forbids mutating, I'd copy values to an array and two-pointer check — O(n) space."

---

### Problem 8: Swap Nodes in Pairs

Swap every two adjacent nodes. Return the new head.

```
Input: 1→2→3→4
Output: 2→1→4→3
```

## Pattern Identification

**Dummy head + rewiring pairs.**

## Solution

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        # swap a and b
        prev.next = b
        a.next = b.next
        b.next = a
        prev = a
    return dummy.next
```

## Trace Through Main Example

```
dummy→1→2→3→4
a=1,b=2
prev.next=2; 1.next=3; 2.next=1
dummy→2→1→3→4
prev=1
a=3,b=4
prev.next=4; 3.next=None; 4.next=3
dummy→2→1→4→3
```

## Edge Cases

- Empty / one node → unchanged
- Odd length: last node stays

## Complexity Analysis

**Time:** O(n)  
**Space:** O(1)

## Interview Talk

"Dummy sits before the pair. I rewire `prev → b → a → rest`, then set `prev = a` so the next pair starts after the swapped couple. Odd leftover node is automatic — the while needs two nodes ahead."

---

### Problem 9: Reorder List

Reorder `L0 → L1 → … → Ln` into `L0 → Ln → L1 → Ln-1 → …` **in place**.

```
Input: 1 → 2 → 3 → 4 → 5
Output: 1 → 5 → 2 → 4 → 3
```

## Pattern Identification

**Find middle + reverse second half + merge alternate.** Three sub-skills you already have, composed.

## Solution

```python
def reorder_list(head):
    if not head or not head.next:
        return

    # 1) middle — slow ends at first-half tail for even? 
    #    standard: slow at start of second half
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2) reverse second half (starting at slow)
    prev = None
    cur = slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    second = prev  # head of reversed second half

    # 3) weave first and second
    first = head
    while second.next:  # stop before reusing the middle twice awkwardly
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

**Note:** After reverse, for `1→2→3→4→5`, first half conceptually `1→2→3`, second reversed `5→4→3` sharing middle — the `while second.next` weave is the common LeetCode idiom that leaves the middle correctly.

## Trace Through Main Example

```
1→2→3→4→5
middle slow at 3
reverse from 3: 5→4→3
weave:
  first=1, second=5
  1→5→2… ; advance first=2, second=4
  2→4→3 ; second.next is None-ish stop
result: 1→5→2→4→3 ✅
```

## Edge Cases

| Case | Result |
|---|---|
| 0–1 nodes | no-op |
| 2 nodes `1→2` | already "reordered" |
| Even length `1→2→3→4` | `1→4→2→3` |

## Complexity Analysis

**Time O(n), Space O(1)** — three linear passes, no extra list.

## Interview Talk

"I don't invent a new pattern — I compose middle, reverse, and careful merge. The bug surface is the weave stop condition; I always trace a 5-node and a 4-node example."

---

### Problem 10: Rotate List

Rotate the list to the right by `k` places.

```
Input: 1→2→3→4→5, k=2
Output: 4→5→1→2→3
```

## Pattern Identification

**Close into a ring, break at the new head.** Equivalent: new head is the `(n - k % n)`-th node (1-indexed from old head's next walk).

## Solution

```python
def rotate_right(head, k):
    if not head or not head.next or k == 0:
        return head

    # length + tail
    n = 1
    tail = head
    while tail.next:
        tail = tail.next
        n += 1

    k %= n
    if k == 0:
        return head

    # make circular
    tail.next = head

    # new tail is (n - k - 1) steps from head; new head is next
    steps = n - k
    new_tail = head
    for _ in range(steps - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
```

## Trace Through Main Example

```
1→2→3→4→5, k=2
n=5, k%=5 → 2
ring: 5→1
steps = 3; new_tail walks to 3
new_head = 4; 3.next = None
4→5→1→2→3 ✅
```

## Edge Cases

| Case | Handling |
|---|---|
| `k = 0` or `k % n == 0` | return head unchanged |
| `k > n` | `k %= n` first |
| Single node | early return |
| Empty | early return |

## Complexity Analysis

**Time O(n), Space O(1)**

## Interview Talk

"Rotate right by k is 'cut after n-k nodes.' I always mod k by n first — interviewers love the `k > n` case. Closing the ring then breaking is cleaner than splicing with two walks."

---

### Problem 11: Delete Node in a Linked List (given only that node)

You are given **only** the node to delete (not the head). It is not the tail.

```
Input: node pointing at 5 in 4→5→1→9
Output: 4→1→9
```

## Pattern Identification

**Overwrite trick** — cannot rewire previous without `prev`. Copy next's value into current, then skip next.

## Solution

```python
def delete_node(node):
    node.val = node.next.val
    node.next = node.next.next
```

## Trace

```
…→4→5→1→9
node=5: val←1, next←9
…→4→1→9 ✅
(node object still there, but now holds 1)
```

## Edge Cases / Constraints

- **Cannot** be used on the true tail (no `next` to copy)
- Interview: say out loud "I'm not deleting the node object — I'm stealing the next node's identity"

## Complexity

**Time O(1), Space O(1)**

---

### Problem 12: Odd Even Linked List

Group all odd-indexed nodes followed by even-indexed nodes (1-indexed positions). Relative order preserved.

```
Input: 1→2→3→4→5
Output: 1→3→5→2→4
```

## Pattern Identification

**Two tails (odd/even chains), then stitch.**

## Solution

```python
def odd_even_list(head):
    if not head or not head.next:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
```

## Trace

```
odd=1, even=2, even_head=2
1.next=3; odd=3; 2.next=4; even=4
3.next=5; odd=5; 4.next=None; even=None
5.next=2 → 1→3→5→2→4
```

## Edge Cases

- 1–2 nodes → unchanged structure essentially
- Even length vs odd length — loop condition handles both

## Complexity

**Time O(n), Space O(1)**

## Interview Talk

"I keep two separate chains without allocating new nodes, then attach even_head after the odd tail. Index here means position, not value parity — clarify that in the interview."

---

# PART 8B: DEEPER TRACES & EDGE-CASE DRILLS

## Drill: Reverse — every edge case on one page

```
None          → None
1             → 1
1→2           → 2→1
1→2→3         → 3→2→1
```

For `1→2`:  
`prev=None,cur=1` → save nxt=2, 1→None, prev=1,cur=2 → save nxt=None, 2→1, prev=2,cur=None → return 2.

## Drill: Remove nth — head and tail

```
List 1→2→3, n=3 (remove head):
  dummy→1→2→3; fast advances 3 to node 3
  fast.next is None → slow stays dummy
  dummy.next = 2 → return 2→3

List 1→2→3, n=1 (remove tail):
  fast to 1; walk until fast at 3, slow at 2
  2.next = None → 1→2
```

## Drill: Floyd entrance — cycle at head

```
1→2→3→1 (cycle entrance = head)

Meet somewhere in cycle; reset slow=head; both walk;
they meet at 1. Must handle "entrance is head" without special case —
the algorithm already does.
```

## Drill: Merge — one empty / all smaller

```
merge(None, 1→2) → 1→2
merge(1→2→3, 4→5) → 1→2→3→4→5  (leftover attach after first exhausted)
merge(5, 1→2→3) → 1→2→3→5
```

---

# PART 8C: INTERVIEW SCRIPT BANK (LINKED LISTS)

Use these as spoken openings — 20–30 seconds each.

**Reverse:**  
"I'll reverse iteratively with three pointers — prev, cur, next — so I use O(1) extra space. Each step I save next, point cur back to prev, then advance. New head is prev when cur becomes null."

**Cycle:**  
"Floyd's algorithm: slow one step, fast two. If there's a cycle they meet; if not, fast hits null. To find the entrance I reset one pointer to head and walk both one step at a time — the math guarantees they meet at the entrance. I compare node identity, not values."

**Remove nth from end:**  
"One pass with a dummy and two pointers. I advance fast by n from the dummy, then move both until fast is at the last node. Slow sits just before the target so I can splice it out. Dummy makes removing the head the same code path."

**Reorder:**  
"Three phases: find middle with slow/fast, reverse the second half, then weave the two halves. Same building blocks as palindrome check."

**Rotate:**  
"Compute length, reduce k mod n, connect tail to head to form a ring, walk to the new break point, open the ring. O(n) time, O(1) space."

**LL vs array (design):**  
"If I need index access or cache-friendly scans, I want an array or deque. If I already hold a node and need O(1) splice — or I'm building LRU with a map — a doubly linked list earns its keep. In Python interviews I'll say that out loud even when the API forces ListNode."

---

# PART 9: HOW THIS CONNECTS TO WHAT YOU ALREADY KNOW

| Prior tool | LL connection |
|---|---|
| Two pointers (arrays) | Slow/fast, gap-of-n, merge |
| Recursion | Node + recurse on `.next` |
| Hashing | Copy random; LRU map; intersection with set (worse space) |
| Arrays | Convert LL↔array when allowed; know cache tradeoff |

**Duplicate Number (array Floyd)** — treating indices as `next` pointers is the same cycle idea. If you saw that problem as PREVIEW, this module is the home for the technique.

---

# PART 10: STATUS & NEXT

| Item | Status after studying this file |
|---|---|
| Concept delivery (this doc) | `taught` when you've read + can teach back frameworks |
| Drill | Implement patterns blind; 6–8 timed mediums |
| Retention | `Retention Questions/Module 4 Retention.md` |
| Stacks & Queues | Companion Module 4 topic — study next |

**Do not mark Complete** until retention + timed gates pass (see Handoff Doc §2A).

---

*End of Linked Lists — Complete Lesson*
