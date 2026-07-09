# Debugging Diagnosis

Interview debugging is a skill separate from “knowing the algorithm.” When a case fails, you need a repeatable diagnosis loop — not random rewrites.

This lesson maps failure modes to fixes, walks five full examples, and ends with an interview checklist + cheat sheet.

---

## 1. Bug taxonomy

Tag every miss with **one primary** type (same honesty rule as the Handoff G7 tags, expanded for code bugs):

| Tag | What it means | Typical signal |
|---|---|---|
| **knowledge-gap** | You don’t know the right pattern / invariant | Blank on approach; invents O(n²) when O(n) pattern exists |
| **misread** | Solved a different problem than stated | Wrong output shape; ignored “exactly one”, “circular”, “sorted” |
| **off-by-one** | Boundary arithmetic wrong | Fails on `n=1`, last index, `lo<=hi` vs `lo<hi`, window length |
| **wrong-state** | State machine / DP / pointers track the wrong thing | Passes tiny cases; fails when state should reset or carry |
| **mutation** | In-place edit corrupts later reads | Works on copy of input; fails when grid/list reused; aliasing bugs |
| **complexity-timeout** | Asymptotically too slow (or hidden quadratic) | TLE on n≈10⁴–10⁵; nested loops; repeated `in list` |
| **edge-empty-null** | Empty / null / single-element / all-equal not handled | Crashes or wrong on `[]`, `None`, one node, zeros |

Secondary tags (optional): **careless-slip** (knew it, mistyped), **time-pressure** (right idea, incomplete).

---

## 2. Diagnosis tree

When tests fail, do **not** start by rewriting the whole solution.

```
failed case(s)
    │
    ▼
REPRODUCE — run only the failing input; print inputs + your output + expected
    │
    ▼
MINIMIZE — shrink array/string/graph until the bug still appears (binary search the input)
    │
    ▼
CLASSIFY — pick a taxonomy tag (table above)
    │
    ▼
HYPOTHESIZE — one sentence: “I think X is wrong because Y”
    │
    ▼
INSTRUMENT — assert invariants / print pointer positions / DP row (temporary)
    │
    ▼
FIX — smallest change that restores the invariant
    │
    ▼
REGRESSION — re-run failing case + neighbors (empty, n=1, previous pass cases)
```

**Rule:** If you cannot state the hypothesis in one sentence, you are still in minimize/classify — not fix.

---

## 3. Worked examples — “Your code failed these 3 cases”

Each example: buggy sketch → failing cases → diagnosis walkthrough → fix.

### Example A — Arrays / sliding window (LC 3 style)

**Buggy idea:** expand `right`; when duplicate seen, set `left = last[ch] + 1` **without** checking `last[ch] >= left`.

```python
def length_of_longest_substring(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last:                    # BUG: stale index
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**Failed cases:**

| Input | Expected | Got |
|---|---|---|
| `"abba"` | `2` | `3` (wrong) |
| `"dvdf"` | `3` | often `2` or wrong depending on variant |
| `"pwwkew"` | `3` | may still pass |

**Diagnosis:**

1. Reproduce `"abba"`: at second `b`, `last['a']=0` is **left of** current window start after moving past first `b`… actually classic: after seeing `bb`, `left=2`; then `a` appears with `last['a']=0`; setting `left = 0+1 = 1` **pulls left backward** into a region already exited.
2. Minimize: `"abba"` is already minimal.
3. Tag: **wrong-state** (window left not monotonic) + **off-by-one** risk on length.
4. Hypothesis: “`left` must never decrease; only update from `last[ch]` if that index is still inside the window.”
5. Fix: `if ch in last and last[ch] >= left: left = last[ch] + 1`.
6. Regression: `"abba"`, `"dvdf"`, `""`, `" "`, `"bbbbb"`.

**Bank link:** `problem-bank/problems/03_longest_substr_no_repeat`.

---

### Example B — Binary search (LC 704 / insert)

**Buggy idea:** `while lo < hi` with `hi = mid - 1` on equal path mixed incorrectly; or `mid = (lo+hi)//2` with `lo = mid` on the “go right” branch → infinite loop.

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid          # BUG: should be mid + 1
        elif nums[mid] > target:
            hi = mid - 1
        else:
            return mid
    return -1
```

**Failed cases:**

| Input | Expected | Behavior |
|---|---|---|
| `nums=[1,2,3], target=3` | `2` | infinite loop / TLE |
| `nums=[5], target=5` | `0` | may hang if `lo=mid=0` forever |
| `nums=[], target=1` | `-1` | OK if empty handled |

**Diagnosis:**

1. Reproduce: `lo=mid=1`, `nums[1]=2 < 3`, `lo = mid` stays 1 → loop.
2. Tag: **off-by-one** (progress guarantee broken) → manifests as **complexity-timeout**.
3. Hypothesis: “Every branch must shrink the searchable range; `lo = mid` does not when `lo == mid`.”
4. Fix: `lo = mid + 1`. For lower-bound templates use half-open `[lo, hi)` with `hi = mid` / `lo = mid + 1` consistently.
5. Regression: first/last element, missing target, empty array, single element.

**Bank links:** `05_binary_search`, `06_search_insert`.

---

### Example C — Graphs / BFS (Word Ladder)

**Buggy idea:** count **edges** instead of **nodes** in the path length; or forget to mark `begin_word` visited; or require `begin_word` in the dictionary.

```python
def ladder_length(begin, end, word_list):
    words = set(word_list)
    q = deque([(begin, 0)])   # BUG: dist 0 → returns edge count
    seen = set()
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                nw = w[:i] + c + w[i+1:]
                if nw in words and nw not in seen:
                    seen.add(nw)
                    q.append((nw, d + 1))
    return 0
```

**Failed cases:**

| Input | Expected | Got |
|---|---|---|
| `hit → cog` classic | `5` | `4` |
| `begin == end` (if allowed) | `1` or `0` per problem | inconsistent |
| `end` not in list | `0` | may still search forever-ish / wrong |

**Diagnosis:**

1. LC 127 length is **number of words** in the sequence → start distance `1`, not `0`.
2. Tag: **misread** (definition of length) often mixed with **wrong-state** (seen set).
3. Also check: if `end not in words: return 0` early.
4. Fix: queue `(begin, 1)`; add `begin` to `seen`; pattern dict for O(n·L²) not O(n·26·L) if needed.
5. Regression: no path, one-letter words, begin equals a neighbor of end.

**Bank link:** `14_word_ladder`.

---

### Example D — DP / Coin Change

**Buggy idea:** greedy (always take largest coin); or `dp[0] = inf` instead of `0`; or iterate coins wrong so order matters incorrectly for combination count (different problem).

```python
def coin_change(coins, amount):
    coins = sorted(coins, reverse=True)
    count = 0
    for c in coins:                 # BUG: greedy
        count += amount // c
        amount %= c
    return count if amount == 0 else -1
```

**Failed cases:**

| Input | Expected | Got |
|---|---|---|
| `coins=[1,3,4], amount=6` | `2` (3+3) | `3` (4+1+1) |
| `coins=[186,419,83,408], amount=6249` | `20` | wrong greedy |
| `coins=[2], amount=3` | `-1` | `-1` (passes by luck) |

**Diagnosis:**

1. Minimize to `[1,3,4], 6` — greedy counterexample.
2. Tag: **knowledge-gap** (unbounded knapsack / DP required, not greedy).
3. Hypothesis: “Optimal substructure: `dp[a] = min(dp[a-c]+1)`.”
4. Fix: tabulate `dp[0]=0`, rest `inf`, relax all coins; return `-1` if `inf`.
5. Regression: `amount=0`, impossible amounts, single coin.

**Bank link:** `17_coin_change`.

---

### Example E — Linked list reverse

**Buggy idea:** lose the `next` pointer; or reverse links but return original `head`.

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        cur.next = prev      # BUG: lost nxt first
        prev = cur
        cur = cur.next       # follows prev → short list / None early
    return head              # BUG: should return prev
```

**Failed cases:**

| Input | Expected | Got |
|---|---|---|
| `[1,2,3]` | `[3,2,1]` | `[1]` or crash cycle |
| `[1,2]` | `[2,1]` | `[1]` |
| `[]` | `[]` | `[]` (may pass) |

**Diagnosis:**

1. Reproduce on `[1,2]`: after first iteration `1→None`, `cur = cur.next` is `None` — never processes `2`. Or with cycle if order differs.
2. Tag: **mutation** / pointer **wrong-state**; return value **misread** of “new head.”
3. Hypothesis: “Must save `nxt = cur.next` before rewiring; return `prev`.”
4. Fix: classic three-pointer loop; return `prev`.
5. Regression: empty, one node, two nodes, longer list.

**Bank link:** `08_reverse_linked_list`.

---

## 4. Interview checklist (when a test fails)

Use this out loud — interviewers grade recovery.

1. **Restate the failing case** in one line (input → expected → actual).
2. **Name the tag** (“this looks like off-by-one on the high bound”).
3. **Trace 30 seconds** on the minimized input — pointers / DP cell / queue front.
4. **State the invariant** you believe should hold (“`left` only moves right”).
5. **Patch the invariant**, not a special case for this test alone.
6. **Propose 2 regression cases** before re-submitting.
7. If stuck >2 minutes: say what you’d print next; ask if you may add a temporary assert.

**Do not:** silently rewrite from scratch; blame the judge; add `if input == failing: return expected`.

---

## 5. Cheat sheet

| Symptom | Likely tag | First check |
|---|---|---|
| Wrong on last/first index | off-by-one | `lo/hi`, `n-1`, window `r-l+1` |
| Wrong after duplicate / reset | wrong-state | when state clears; stale map indices |
| Works until large n | complexity-timeout | nested loops; `in list`; re-sort each step |
| Crash on empty | edge-empty-null | `if not head`, `k <= n`, `dp[0]` |
| Grid/list wrong mid-run | mutation | copy vs in-place; aliasing |
| “Almost LC sample” | misread | return type, 0- vs 1-index, inclusive ends |
| No idea of approach | knowledge-gap | stop coding; re-derive pattern from templates |

**Invariant prompts (say these):**

- Binary search: “What is the range meaning — inclusive or half-open?”
- Window: “What does `left` guarantee about the current window?”
- Graph BFS: “What does distance count — nodes or edges?”
- DP: “What does `dp[i]` mean in one sentence?”
- Linked list: “Which pointer is the new head?”

**Bank practice:** break a reference solution on purpose, run `python run_all.py <slug>`, then use this tree to fix it cold.
