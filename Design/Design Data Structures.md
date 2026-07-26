# DESIGN DATA STRUCTURES — THE COMPLETE LESSON

**Module:** Coverage gap — Design DS (beyond LRU)  
**Status:** `content-delivered` — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Hash maps, linked lists / ordered dict, heaps, stacks, binary search.  
**Cross-refs:** Full LRU is **Part 15 below** (canonical coded version). Linked Lists Pattern 8 = DLL motivation. This hub also covers the rest of the design family.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.


# PART 1: WHY DS DESIGN INTERVIEWS EXIST

Interviewers are not asking you to invent Redis. They want:

1. **Correct API** under stated complexity
2. **Composition** of known structures (hash + list, hash + heap, hash + sorted list)
3. **Tradeoff talk** — what you sacrifice
4. **Edge cases** — empty, duplicates, time ties, invalid ops

## Principles of DS Design Interviews (Memorize)

| Principle | Practice |
|---|---|
| Write the API first | Method signatures + complexities before code |
| Name the invariant | "map key → node"; "heap holds (freq, id)" |
| One structure per need | Fast lookup ≠ fast order — combine |
| Lazy deletion OK | Heaps often need stale-skip |
| Amortized vs worst | Say which you provide |
| Don't overbuild | Skip unused features |

**Interview opener:**  
> "I'll support [ops] in [complexities] using [structures]. Invariant: …"

---

# PART 2: MIN STACK

## 2A: Problem

`push`, `pop`, `top`, `getMin` — all O(1).

## 2B: Dual Stack

```python
class MinStack:
    def __init__(self):
        self.st = []
        self.mn = []  # mn[-1] = min of stack so far

    def push(self, val):
        self.st.append(val)
        if not self.mn or val <= self.mn[-1]:
            self.mn.append(val)

    def pop(self):
        val = self.st.pop()
        if val == self.mn[-1]:
            self.mn.pop()
        return val

    def top(self):
        return self.st[-1]

    def getMin(self):
        return self.mn[-1]
```

**Invariant:** `mn` stores non-increasing mins; pop min only when popping that value.

### Trace
```
push 3 → st[3] mn[3]
push 5 → st[3,5] mn[3]
push 2 → st[3,5,2] mn[3,2]
push 2 → st[...,2] mn[3,2,2]
pop → mn pops one 2
getMin → 2
```

**TRAP:** use `<=` when pushing to `mn` so duplicate mins both recorded.

---

# PART 3: MAX STACK — INTUITION

Same as MinStack with max auxiliary stack (`>=`).  
Harder LC "Max Stack" adds `popMax` → need structure for remove-arbitrary (TreeMap + DLL, or two heaps with lazy delete). **Interview light version:** dual stack for `getMax` only.

```python
# Soft max stack (getMax only) — mirror MinStack with >=
```

**Full popMax sketch:** doubly linked list of values + balanced BST / sorted dict of value→nodes; hash for id. Mention complexity O(log n).

---

# PART 4: RANDOMIZED SET (Insert / Remove / GetRandom O(1))

## 4A: Hash Map + Array Swap-Remove

```python
import random

class RandomizedSet:
    def __init__(self):
        self.arr = []
        self.pos = {}  # val → index in arr

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.arr)
        self.arr.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.arr[-1]
        self.arr[i] = last
        self.pos[last] = i
        self.arr.pop()
        del self.pos[val]
        return True

    def getRandom(self):
        return random.choice(self.arr)
```

**Why swap with last:** O(1) delete from array without shifting.

### Trace
```
insert 1,2,3 → arr[1,2,3]
remove 2 → swap 3 into index1 → arr[1,3], pos{1:0,3:1}
getRandom → uniform among remaining
```

**TRAP:** update `pos[last]` **before** popping; handle removing last element carefully (same code works).

---

# PART 5: TIME-BASED KEY-VALUE STORE (TimeMap)

```python
import bisect

class TimeMap:
    def __init__(self):
        self.m = {}  # key → list of (timestamp, value) sorted by time

    def set(self, key, value, timestamp):
        self.m.setdefault(key, []).append((timestamp, value))
        # Problem guarantees timestamps increasing per key

    def get(self, key, timestamp):
        if key not in self.m:
            return ""
        arr = self.m[key]
        i = bisect.bisect_right(arr, (timestamp, chr(127))) - 1
        # or bisect on timestamps only
        return arr[i][1] if i >= 0 else ""
```

Cleaner bisect on parallel lists or:

```python
i = bisect.bisect_right([t for t, _ in arr], timestamp) - 1
```

**Complexity:** set O(1) append; get O(log n).

---

# PART 6: SNAPSHOT ARRAY (LIGHT)

```python
class SnapshotArray:
    def __init__(self, length):
        self.snap_id = 0
        self.data = [{0: 0} for _ in range(length)]  # index → {snap_id: val}

    def set(self, index, val):
        self.data[index][self.snap_id] = val

    def snap(self):
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        hist = self.data[index]
        # largest snap_id' <= snap_id with an entry
        keys = sorted(hist)
        import bisect
        i = bisect.bisect_right(keys, snap_id) - 1
        return hist[keys[i]]
```

**Idea:** don't copy whole array each snap — store sparse history per index.  
**Tradeoff:** get is O(log S) per index history length.

---

# PART 7: ALL O(1) DATA STRUCTURE (Freq Map)

Support `inc`, `dec`, `getMaxKey`, `getMinKey` in O(1).

**Structure:**
- `key → freq`
- `freq → OrderedSet/DLL of keys` at that freq
- track `minf`, `maxf`

```python
from collections import defaultdict

class AllOne:
    def __init__(self):
        self.key_freq = {}
        self.freq_keys = defaultdict(set)
        self.minf = self.maxf = 0

    def inc(self, key):
        f = self.key_freq.get(key, 0)
        if f:
            self.freq_keys[f].discard(key)
            if not self.freq_keys[f] and self.minf == f:
                self.minf += 1
        nf = f + 1
        self.key_freq[key] = nf
        self.freq_keys[nf].add(key)
        self.maxf = max(self.maxf, nf)
        if f == 0:
            self.minf = 1 if self.minf == 0 else min(self.minf, 1)

    def dec(self, key):
        f = self.key_freq[key]
        self.freq_keys[f].discard(key)
        if not self.freq_keys[f]:
            if self.maxf == f:
                self.maxf -= 1
            if self.minf == f:
                self.minf = f - 1 if f > 1 else (min(self.freq_keys) if self.key_freq else 0)
        if f == 1:
            del self.key_freq[key]
        else:
            self.key_freq[key] = f - 1
            self.freq_keys[f - 1].add(key)

    def getMaxKey(self):
        if not self.maxf:
            return ""
        return next(iter(self.freq_keys[self.maxf]))

    def getMinKey(self):
        if not self.minf:
            return ""
        return next(iter(self.freq_keys[self.minf]))
```

**Note:** Production-quality AllOne uses DLL of freq buckets for true O(1) min update without scanning. The sketch above is **intuition**; in interview, draw **freq buckets as a doubly linked list** of sets.

**Interview drawing:**
```
key→freq map
freq buckets DLL: 1:{a,b} ↔ 2:{c} ↔ 5:{d}
min = head, max = tail
```

---

# PART 8: FREQUENCY STACK (FreqStack)

`push` / `pop` most frequent; ties → most recent.

```python
from collections import defaultdict

class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)
        self.group = defaultdict(list)  # freq → stack of vals
        self.maxf = 0

    def push(self, val):
        self.freq[val] += 1
        f = self.freq[val]
        self.group[f].append(val)
        self.maxf = max(self.maxf, f)

    def pop(self):
        val = self.group[self.maxf].pop()
        self.freq[val] -= 1
        if not self.group[self.maxf]:
            self.maxf -= 1
        return val
```

### Trace
```
push 5,7,5,7,4,5
freq: 5→3,7→2,4→1
pop → 5 (freq3)
pop → 7 (freq2, more recent than other 5? groups: 2:[7,7]? actually 2:[7,4? wait]
```
Careful dry-run:
```
after pushes: group[1]=[5,7,4], group[2]=[5,7], group[3]=[5]
pop → 5 from group3; maxf=2
pop → 7 from group2
pop → 5 from group2
```

---

# PART 9: TWITTER / DESIGN FEED (LIGHT)

**API:** `postTweet`, `follow`, `unfollow`, `getNewsFeed` (10 most recent from self+followees).

```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)  # user → list of (time, id)
        self.followees = defaultdict(set)

    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def follow(self, followerId, followeeId):
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.followees[followerId].discard(followeeId)

    def getNewsFeed(self, userId):
        people = set(self.followees[userId])
        people.add(userId)
        heap = []
        for u in people:
            for t, tid in self.tweets[u][-10:]:  # prune
                heapq.heappush(heap, (-t, tid))
        feed = []
        while heap and len(feed) < 10:
            feed.append(heapq.heappop(heap)[1])
        return feed
```

**Better:** k-way merge of sorted tweet lists with heap of pointers — O(k log k) for k followees.

---

# PART 10: ITERATOR DESIGNS

## 10A: BST Iterator

Inorder controlled: stack of left spine; `next` pops and pushes right's left spine. O(1) amortized, O(h) space.

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
        self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)
```

## 10B: Peeking Iterator

Wrap iterator; cache `next` value for `peek`.

## 10C: Flatten Nested List Iterator

Stack of lists/indices or recursive flatten to queue — discuss lazy vs eager.

## 10D: Zigzag / Vector2D Iterator

Index into list of lists; skip empty inner lists.

---

# PART 11: DESIGN CHEAT SHEET

| Problem | Core combo |
|---|---|
| LRU Cache | HashMap + DLL / OrderedDict |
| LFU Cache | Hash + freq buckets DLL |
| MinStack | Stack + min stack |
| RandomizedSet | Array + Hash index |
| TimeMap | Hash + sorted list + bisect |
| Snapshot Array | Per-index sparse history |
| All O(1) | key↔freq + freq buckets |
| FreqStack | freq map + stack per freq |
| Twitter | tweets lists + heap merge |
| BST Iterator | stack spine |
| MaxStack popMax | DLL + sorted map (log n) |

---

# PART 12: TRAPS

| Trap | Fix |
|---|---|
| MinStack forget duplicate mins | Push on `<=` |
| RandomizedSet forget update moved index | Always `pos[last]=i` |
| TimeMap assume exact timestamp | `bisect_right - 1` |
| Snapshot full copy each snap | Sparse history |
| FreqStack pop wrong on tie | Stack order = recency |
| Twitter include self tweets | Add self to people set |
| Iterator mutate during iterate | Define fail-fast or copy |

---

# PART 13: WORKED PROBLEMS

## WP1 — MinStack sequence
push −2,0,−3; getMin −3; pop; top 0; getMin −2.

## WP2 — RandomizedSet
insert 1 True; remove 2 False; insert 2; getRandom ∈{1,2}; remove 1; insert 2 False.

## WP3 — TimeMap
set(a,bar,1); set(a,bar2,4); get(a,1)=bar; get(a,3)=bar; get(a,4)=bar2; get(a,0)="".

## WP4 — Snapshot
set(0,5); snap→0; set(0,6); get(0,0)=5.

## WP5 — FreqStack
As Part 8 trace → pops 5,7,5,4,7,5.

## WP6 — BST Iterator
Tree [7,3,15,null,null,9,20] → next sequence 3,7,9,15,20.

## WP7 — Twitter light
post, follow, post, getNewsFeed order by time desc.

## WP8 — PeekingIterator
peek same as next without advance; then next advances.

## WP9 — Design hit counter (bonus)
Queue of timestamps; binary search / bucket 300s.

## WP10 — API complexity table for your AllOne drawing

---

# PART 14: INTERVIEW SCRIPT

1. Restate ops + required complexities.
2. Propose structure combo + invariant.
3. Walk one happy path + one edge (empty / duplicate).
4. Code cleanly; name helpers.
5. State space and what you'd optimize next (LFU, true O(1) min).

---

**Status note (interim):** Core above; deep expansions in Parts 15+.

---

# PART 15: LRU CACHE — FULL WORKED (MUST-KNOW)

**LC 146.** Capacity `C`. `get(key)` / `put(key, value)` both **O(1)** average. Evict **least recently used** on overflow.

## Why HashMap + Doubly Linked List

| Need | Structure |
|---|---|
| Find node by key in O(1) | `dict[key] → node` |
| Move refreshed key to MRU in O(1) | Splice node in DLL |
| Evict LRU in O(1) | Tail (or head) sentinel of DLL |

Singly list fails: removing middle needs prev pointer. Array fails: moves are O(C).

## Sentinel DLL sketch

```
sentinel ↔ MRU ↔ ... ↔ LRU ↔ sentinel   (circular) 
# or: head=MRU end, tail=LRU end — pick one convention and stick to it
```

## Full Python (manual DLL — interview preferred over hiding behind OrderedDict)

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()  # head=MRU side, tail=LRU side
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_mru(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if not node:
            return -1
        self._remove(node)
        self._add_mru(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_mru(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self._add_mru(node)
```

## Trace

`C=2`: put(1,1), put(2,2), get(1)→1 (1 becomes MRU), put(3,3) evicts key 2, get(2)→-1.

## Edge cases

- Capacity 1: every put may evict.  
- get miss → `-1`, must **not** change order.  
- put existing key: update value **and** mark MRU; no eviction.  
- Evict **before** insert when at capacity (or carefully if inserting new).

## OrderedDict shortcut (mention, then still know DLL)

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self.cap, self.od = capacity, OrderedDict()
    def get(self, key):
        if key not in self.od: return -1
        self.od.move_to_end(key)
        return self.od[key]
    def put(self, key, value):
        if key in self.od: self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap: self.od.popitem(last=False)
```

Interviewers often want the **DLL + hash** explanation even if you code OrderedDict — speak the invariant.

## Teach-back

1. Why doubly, not singly?  
2. What exactly is evicted and when?  
3. Draw put-on-full for capacity 2.

**Cross-ref:** DLL pointer skills in `Linked Lists/Linked Lists.md` Pattern 8.

**Netflix/Meta follow-ups:** TTL / expiring / weighted cache + rate limiter coding → `Design/TTL Cache & Rate Limiter.md`.

---

# PART 16: LFU INTUITION (BRIDGE FROM ALL O(1))

LFU = key→freq + freq→DLL of keys (recency within freq) + minfreq pointer.  
Same bucket idea as All O(1) / FreqStack family.

---

# PART 17: MAX STACK WITH popMax (SKETCH)

```
DLL of values in stack order
TreeMap/SortedList: value → set of node pointers
popMax: take max key in TreeMap, remove that node from DLL
```
Complexities O(log n). Soft interview: explain drawing even if coding MinStack only.

---

# PART 18: MORE DESIGN WORKED TRACES

## WP11 — MinStack duplicates
push 0,1,0; getMin 0; pop; getMin 0 — both zeros were on min stack.

## WP12 — RandomizedSet remove last
arr=[1], remove 1 — swap with self; must not break map.

## WP13 — TimeMap strictly increasing
If timestamps not increasing, need bisect insert — problem usually guarantees sorted appends.

## WP14 — Snapshot get historical
set(0,1); snap0; set(0,2); snap1; get(0,0)=1; get(0,1)=2.

## WP15 — FreqStack long
Push same value many times; pops unwind frequency layers.

## WP16 — Twitter unfollow
After unfollow, feed excludes that user's tweets.

## WP17 — NestedIterator lazy
Stack of `[list, index]`; hasNext advances until integer on top.

## WP18 — Hit Counter
Queue of timestamps; binary search first ≥ now-299; size = hits in window.

## WP19 — Design Underground System
Map id→(startStation,t); map (start,end)→(total,count).

## WP20 — Seat Manager / Exam Room
Heap of free seats / gap heuristics — priority queue design.

---

# PART 19: COMPLEXITY TABLE (MEMORIZE)

| Structure | insert | delete | special |
|---|---|---|---|
| MinStack | O(1) | O(1) | getMin O(1) |
| RandomizedSet | O(1) | O(1) | getRandom O(1) |
| TimeMap | O(1) append | — | get O(log n) |
| Snapshot | O(1) set | — | get O(log S) |
| FreqStack | O(1) | O(1) | pop mode |
| AllOne (DLL buckets) | O(1) | O(1) | min/max key |
| Twitter feed | O(1) post | — | feed O(F log F) merge |
| BST Iterator | — | — | next amort O(1) |

---

# PART 20: HOW TO TALK IN THE INTERVIEW (SCRIPTS)

**Script A — RandomizedSet**  
"I need O(1) insert, remove, and uniform random. Array gives random by index; hash map stores value→index; remove swaps with last to keep the array dense."

**Script B — TimeMap**  
"Per key I keep a sorted list of (timestamp, value). set appends because timestamps increase. get is binary search for rightmost timestamp ≤ query."

**Script C — FreqStack**  
"I track frequency of each value and a stack per frequency. pop from the max frequency stack so ties break by recency."

**Script D — All O(1)**  
"I'll maintain frequency buckets in a doubly linked list so min and max freq are at the ends, plus a key→freq map and freq→keys set."

---

# PART 21: FAILURE MODES CHECKLIST

- Empty structures: getMin/getMax/getRandom/getNewsFeed  
- Duplicate values vs unique keys  
- Timestamp ties  
- follow self  
- Iterator concurrent modification  
- Lazy heap entries stale  

---

# PART 22: 30-MINUTE DRILL

1. MinStack + RandomizedSet code from memory.  
2. TimeMap bisect get.  
3. FreqStack trace.  
4. BST Iterator spine.  
5. Draw AllOne buckets.  
6. Speak Script A–C without notes.

---

**End of Design lesson.** Status: `content-delivered`.

---

# PART 23: RANDOMIZED SET — EXTENDED TRACE

```
insert(10) → arr[10] pos{10:0}
insert(20) → arr[10,20] pos{10:0,20:1}
insert(30) → arr[10,20,30]
remove(10) → swap 30 into idx0 → arr[30,20] pos{30:0,20:1}
getRandom → 30 or 20
remove(30) → swap 20 → arr[20]
remove(20) → arr[]
```

---

# PART 24: TIMEMAP EXTENDED

```
set(foo, bar, 1)
set(foo, bar2, 4)
set(foo, bar3, 6)
get(foo, 0) → ""
get(foo, 1) → bar
get(foo, 5) → bar2
get(foo, 6) → bar3
get(foo, 100) → bar3
```

---

# PART 25: FREQSTACK EXTENDED TRACE

```
push 5 → freq1 group1[5]
push 7 → group1[5,7]
push 5 → freq2 group2[5]
push 7 → group2[5,7]
push 4 → group1[5,7,4]
push 5 → freq3 group3[5]
pop → 5 (g3)
pop → 7 (g2)
pop → 5 (g2)
pop → 4 (g1)
pop → 7 (g1)
pop → 5 (g1)
```

---

# PART 26: BST ITERATOR TRACE

Tree:
```
    7
   / \
  3   15
     /  \
    9    20
```
Init stack: push 7,3 → stack[7,3]  
next→3, push nothing → [7]  
next→7, push 15,9 → [15,9]  
next→9 → [15]  
next→15, push 20 → [20]  
next→20 → []

---

# PART 27: DESIGN PROMPT → STRUCTURE MAP (EXPANDED)

| Prompt | Structures |
|---|---|
| Min stack | 2 stacks |
| Max stack + popMax | DLL + TreeMap |
| Random O(1) set | arr + hash |
| Random O(1) multiset | arr + hash of indices sets |
| Time travel KV | hash + bisect lists |
| Snapshots | sparse per-index history |
| Freq pop | freq + group stacks |
| All O(1) min/max key | freq buckets DLL |
| News feed | lists + heap merge |
| Inorder iterator | stack |
| Peeking | cache one next |
| Hit counter | queue / buckets |
| LRU/LFU | hash + DLL (+ freq) |

---

# PART 28: BLIND CODE CHECKLIST

- [ ] API + complexities written first  
- [ ] Invariant named  
- [ ] Empty ops defined  
- [ ] Duplicates policy  
- [ ] Lazy deletion mentioned if heap  

---

**Final status:** Design Data Structures — `content-delivered`.

---

# PART 29: FULL WORKED SOLUTION BANK (DESIGN)

## S1–S6
MinStack, RandomizedSet, TimeMap, Snapshot, FreqStack, BSTIterator — earlier parts.

## S7 — PeekingIterator
Cache `next` value; `peek` returns cache; `next` advances cache.

## S8 — Twitter light
Tweets lists + heap of recent by time; followee set includes self.

## S9 — Hit Counter
Deque of timestamps; popleft while `<= t-300`; size = hits.

## S10 — Underground System
`checkin[id]=(station,t)`; stats[(a,b)] = total,count; average = total/count.

## S11 — OrderedDict LRU sketch
`move_to_end` on get/put; `popitem(last=False)` on eviction.

## S12 — Vector2D iterator
Outer/inner indices; skip empty inners in `hasNext`.

---

# PART 30: COMPOSITION META-TABLE

| Requirements | Composition |
|---|---|
| lookup + recency | hash + DLL |
| lookup + uniform random | hash + dense array |
| lookup + time version | hash + sorted versions |
| lookup + freq extremes | hash + freq buckets |
| k-way recent merge | lists + heap |
| lazy inorder | stack spine |

---

# PART 31: ORAL EXAM

1. RandomizedSet remove steps in order.  
2. MinStack `<=` reason.  
3. TimeMap `bisect_right-1`.  
4. FreqStack tie-break.  
5. Three design principles.

---

# PART 32: FINAL DESIGN MASTERY CHECK

API-first · invariants · MinStack · RandomizedSet · TimeMap · FreqStack · iterators · feed merge.

**Final status:** Design Data Structures — `content-delivered`.
