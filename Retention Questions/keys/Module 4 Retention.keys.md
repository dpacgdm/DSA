# Answer Key — Module 4 Retention.md

**Source questions:** `Retention Questions/Module 4 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
**Answer:** Arrays are contiguous — address = base + i × size (one arithmetic jump). Linked lists are pointer chains — you must follow `next` i times. No random access.

---


<!-- answer block 2 -->
**Answer:** **Cache locality.** Contiguous array elements ride into CPU cache together. LL nodes are scattered heap allocations → frequent cache misses.

---


<!-- answer block 3 -->
**Answer:** When you must **delete/move an arbitrary known node in O(1)** without scanning for its predecessor (classic: **LRU** with hash map + DLL).

---


<!-- answer block 4 -->
**Answer:** One code path for mutations that might change the real head (delete head, merge, remove nth from end). Return `dummy.next` as the new head.

---


<!-- answer block 5 -->
**Answer:** Meeting ⇒ cycle (or they'd hit `None`). Then put one pointer at `head`, both walk +1; meeting point = entrance. Compare nodes with `is`, not values.

---


<!-- answer block 6 -->
**Answer:** Dummy → head. Advance `fast` by n from dummy. Walk `fast` and `slow` until `fast.next` is None. `slow` is before the victim; splice `slow.next = slow.next.next`.

---


<!-- answer block 7 -->
**Answer:** Stack = LIFO → `list` (`append`/`pop`). Queue = FIFO → `collections.deque` (`append`/`popleft`). Never `list.pop(0)` for a hot queue.

---


<!-- answer block 8 -->
**Answer:** O(n) — every element shifts left. `deque.popleft()` is O(1).

---


<!-- answer block 9 -->
**Answer:** Each index is **pushed once and popped at most once**. Total stack ops ≤ 2n.

---


<!-- answer block 10 -->
**Answer:** Same decreasing monotonic stack. Next greater stores **values**; daily temps stores **index distances** `i - j`.

---


<!-- answer block 11 -->
**Answer:** Need O(1) expire from front and discard dominated from back. Front index = **current window's maximum**.

---


<!-- answer block 12 -->
**Answer:** Store `(val, min_so_far)` on each push (or a parallel mins stack). Top's min field is the answer — no scan.

---


<!-- answer block 13 -->
**Answer:** Order matters. `([)]` has balanced counts but wrong nesting. Stack enforces LIFO matching.

---


<!-- answer block 14 -->
**Answer:** O(n) **call stack** space (and Python's ~1000 recursion limit on long lists). Prefer iterative reverse when space/limit matters.

---


<!-- answer block 15 -->
**Answer:** Intersection means **shared nodes** (same object identity), not equal values that happen to match.

---


<!-- answer block 16 -->
**Answer:**  
`prev=None`, `cur=1`.  
Loop: `nxt=cur.next` (Save) → `cur.next=prev` (Rewire) → `prev=cur; cur=nxt` (Advance).  
After: `prev=3` is new head → `3→2→1`.  
If you rewire before saving `nxt`, you lose the rest of the list.

---


<!-- answer block 17 -->
**Answer:** `dummy` + `tail`. Always attach the smaller head of `list1`/`list2`, advance that list and `tail`. When one is exhausted: `tail.next = list1 or list2` (attach the leftover chain). Return `dummy.next`. Reuses nodes — O(1) extra space.

---


<!-- answer block 18 -->
**Answer:** For each bar height h, the largest rectangle of height h extends left/right until a **strictly shorter** bar. An increasing monotonic stack finds **previous smaller** and **next smaller** as bounds. Area = `h * (right - left - 1)`. Sentinels of height 0 avoid empty-stack edge cases.

---


<!-- answer block 19 -->
**Answer:** `in_s` receives pushes. On pop/peek, if `out_s` is empty, pour all of `in_s` into `out_s` (reverses order → FIFO). Each element is moved **at most once** in→out, so amortized O(1) per op.

---


<!-- answer block 20 -->
**Answer:** After `3[a2[c`: stack has `("", 3)` then `("a", 2)`, `cur_str="c"`. First `]` pops `("a", 2)` → `cur_str = "a" + "c"*2 = "acc"`. Second `]` pops `("", 3)` → `"acc"*3 = "accaccacc"`.

---


<!-- answer block 21 -->
**Answer:** When you already hold a node reference and need **O(1) local insert/delete/splice**, or the problem API is `ListNode`, or you're building **LRU** (DLL + map). If you need index access or tight loops over data, prefer arrays/deques and say so (cache).

---


<!-- answer block 22 -->
**Answer:** Fixed: add right, subtract left when window exceeds size k. Variable (positives): expand right; while sum ≥ target shrink left and track min length — classic two-pointer window.

---


<!-- answer block 23 -->
**Answer:** Unsorted → can't rely on ordered two pointers without sorting (which loses indices or needs pairs). Map `value → index` gives O(n) complement lookup. (Sorted + two pointers works for the *values* variant if indices aren't required.)

---


<!-- answer block 24 -->
**Answer:** **Base case** (stop), **recursive case** (shrink), **combination** (use sub-result). Missing any → infinite recursion or wrong answer.

---


<!-- answer block 25 -->
**Answer:** It must be **monotonic** with respect to the predicate (sorted values, or a boolean feasible/infeasible that flips once). BS answers "first true / last false" on that space — not on arbitrary unsorted data.

---


<!-- answer block 26 -->
**Answer:** Lost `nxt`. After `cur.next = prev`, `cur.next` is the old prev — you cannot advance. Fix: `nxt = cur.next` before rewiring.

---


<!-- answer block 27 -->
**Answer:** Correct functionally, **O(n)** per dequeue. Use `deque.popleft()`.

---


<!-- answer block 28 -->
**Answer:** If stack stores **indices**, compare `nums[stack[-1]] < nums[i]`, not `stack[-1] < nums[i]`.

---


<!-- answer block 29 -->
**Answer:** Value collision ≠ cycle. Use `slow is fast`.

---


<!-- answer block 30 -->
**Answer:** Should be **index distance** `i - j`, not temperature difference.

---


<!-- answer block 31 -->
**Answer:** Must `if dq[0] <= i - k: dq.popleft()` before reading the max — otherwise expired indices poison the front.

---


<!-- answer block 32 -->
**Answer:** Missing `tail.next = l1 or l2` — leftover chain dropped.

---


<!-- answer block 33 -->
**Answer:** Find middle (slow/fast) → reverse second half → weave/merge alternate.

---


<!-- answer block 34 -->
**Answer:** Full rotations are no-ops. Without mod, you walk off the list or do useless O(k) work when k ≫ n.

---


<!-- answer block 35 -->
**Answer:** `[4, 2]` — because `13/5 → 2` (toward zero).

---


<!-- answer block 36 -->
**Answer:** Guarantees every bar gets popped/finalized; avoids empty-stack special cases for left bound.

---


<!-- answer block 37 -->
**Answer:** First pass create `old→new` nodes; second pass set each copy's `next`/`random` via the map.

---


<!-- answer block 38 -->
**Answer:** No — negatives move left, positives right, never meet if already ordered that way.

---


<!-- answer block 39 -->
**Answer:** Occasional O(n) resize (≈2×) spreads over many cheap appends; geometric series → amortized O(1).

---


<!-- answer block 40 -->
**Answer:** List scans; set hashes to a bucket.

---


<!-- answer block 41 -->
**Answer:** Only when `out_s` is empty on pop/peek — preserves FIFO and amortizes moves.

---


<!-- answer block 42 -->
**Answer:** The second half (from the middle). Then compare first half vs reversed second.

---


<!-- answer block 43 -->
**Answer:** You need **positions** to compute `i - j`. Values alone cannot give day distance. Indices also let you look up `T[j]` when comparing.

---


<!-- answer block 44 -->
**Answer:** Hash map `key → node` for O(1) lookup. Doubly linked list orders keys by recency (MRU↔LRU). `get`/`put` move node to MRU; on capacity, delete LRU node and map entry. DLL needed so middle removal is O(1).

---


<!-- answer block 45 -->
**Answer:** Case 2 (work matches root): **Θ(n log n)** — like mergesort. (Confirm a=2,b=2, f=O(n), n^{log_b a}=n.)

---


<!-- answer block 46 -->
**Answer:** When nums can be **negative** (or zero in ways that break monotonic window sum). Use prefix + hash instead.

---

**Next:** Timed verification set for Module 4 patterns (blind, no labels). Then first mini-mock when `drilled`.

*End of Module 4 Retention Grill*

