# MODULE 2 RETENTION GRILL — BIG O + ARRAYS + HASHING + RECURSION

**CRITICAL BLOCKING GATE** (Handoff Doc §6): Hashing + Recursion stay below `complete` until this grill passes, then timed verify.

**With answers.** Blind first: cover answer blocks, speak/write your solution, then check.

**Ledger pull (due-now):** Big O simplification, loop patterns, dependent nesting, hidden Python costs, space/call stack; Arrays two pointers / sliding window / prefix / in-place / string immutability; Hashing internals + frequency/prefix-hash; Recursion base/stack/trees/memo intro/backtracking skeleton. **Master Theorem = NOT taught — do not treat as mastered.**

**Pass bar (suggested):** Rapid fire ≥ 80% · Conceptual solid teach-back · Problems ≥ 6/8 first-pass correct reasoning · Trick section exposes shallow gaps (retag and re-teach). Tag misses: `knowledge-gap` / `misread` / `time-pressure` / `careless-slip`.

**Rules:**
1. No pattern labels on the problem side — identify the tool yourself.
2. PREVIEW items (if any) earn no mastery credit.
3. Passing this grill ≠ `complete`. Still need timed verification + ledger/scoreboard updates.

---

# SECTION A: RAPID FIRE — COMPLEXITY

Answer time + space. Then check.

---

## A1.

```python
def f(arr):
    n = len(arr)
    s = 0
    for i in range(n):
        for j in range(i, n):
            s += arr[j]
    return s
```

### Answer

Outer `i`: n values. Inner `j`: `n - i` iterations. Total iterations = n + (n-1) + … + 1 = n(n+1)/2 → **O(n²)** time.  
Body is O(1). Space: scalars → **O(1)**.

> **Time: O(n²), Space: O(1)**

---

## A2.

```python
def f(n):
    i = 1
    while i < n:
        j = 1
        while j < n:
            j *= 2
        i += 1
    return i
```

### Answer

Outer: n iterations. Inner: `j` doubles → **O(log n)** per outer. Total **O(n log n)**. Space **O(1)**.

> **Time: O(n log n), Space: O(1)**

---

## A3.

```python
def f(arr):
    n = len(arr)
    i = 0
    while i < n:
        j = i
        while j < n and arr[j] == arr[i]:
            j += 1
        i = j
    return i
```

### Answer

Classic "two pointers advance" / run-length style. Each index visited by `j` at most once; `i` jumps to `j`. **O(n)** time, **O(1)** space. Not O(n²) — inner work is amortized linear.

> **Time: O(n), Space: O(1)**

---

## A4.

```python
def f(s):
    out = []
    for c in s:
        out.append(c)
    return "".join(out)
```

### Answer

Append O(1) amortized each; join O(n). **O(n)** time, **O(n)** space. Contrast with `out = out + c` which would be O(n²).

> **Time: O(n), Space: O(n)**

---

## A5.

```python
def f(arr, x):
    return x in arr  # arr is a list
```

### Answer

List membership is linear scan → **O(n)** time, **O(1)** space. If `arr` were a `set`, O(1) average.

> **Time: O(n), Space: O(1)**

---

## A6.

```python
def f(n):
    if n <= 1:
        return n
    return f(n - 1) + f(n - 2)
```

### Answer

Classic fib tree: **O(φⁿ) ⊂ O(2ⁿ)** time, **O(n)** stack space. Recurrence T(n)=T(n-1)+T(n-2)+O(1). Overlapping subproblems → memo makes O(n) time / O(n) space.

> **Time: O(2ⁿ), Space: O(n)** (naive)

---

## A7.

```python
def f(arr):
    n = len(arr)
    for i in range(n):
        arr[:i]  # slicing
    return arr
```

### Answer

Slice `arr[:i]` costs O(i) and allocates. Sum 0+1+…+(n-1) → **O(n²)** time, **O(n)** extra peak space for largest slice.

> **Time: O(n²), Space: O(n)**

---

## A8.

```python
def f(a, b):
    # a length n, b length m
    for x in a:
        for y in b:
            pass
```

### Answer

Different inputs → **O(n·m)** time, **O(1)** space. Do not collapse to O(n²) unless n=m is stated.

> **Time: O(n·m), Space: O(1)**

---

## A9.

```python
def f(arr):
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    return freq
```

### Answer

n dict ops, O(1) average each → **O(n)** time, **O(k)** space (k = distinct keys ≤ n).

> **Time: O(n), Space: O(k) ≤ O(n)**

---

## A10.

```python
def permute(path, used, nums, out):
    if len(path) == len(nums):
        out.append(path[:])
        return
    for i in range(len(nums)):
        if used[i]:
            continue
        used[i] = True
        path.append(nums[i])
        permute(path, used, nums, out)
        path.pop()
        used[i] = False
```

### Answer

n! leaves; work along paths → **O(n·n!)** time typical (copy path O(n) at leaves, or O(n!) nodes × branching). Space: O(n) recursion depth + O(n·n!) output.

> **Time: O(n·n!), Space: O(n) stack + output**

---

## A11.

Dependent nesting: outer `i = 1..n`, inner `j = 1; j < n; j += i`. Complexity?

### Answer

For each i, inner runs ~ n/i times. Total Σ_{i=1}^{n} n/i = n·H_n = **O(n log n)** (harmonic series).

> **Time: O(n log n)**

---

## A12.

`dict` average vs worst lookup? When does worst happen?

### Answer

Average **O(1)**; worst **O(n)** with pathological collisions (or adversarial keys historically). Python uses open addressing + randomized hash seed — treat as amortized O(1) in interviews unless asked about attacks.

---

# SECTION B: CONCEPTUAL (TEACH-BACK)

Speak like an interview. Then compare.

---

## B1. State the three Big-O simplification rules.

### Answer

1. Drop constant factors (`3n` → O(n)).  
2. Drop non-dominant terms (`n² + n` → O(n²)).  
3. Different input sizes → different variables (`O(n + m)`, not fake `O(n)`).

---

## B2. Why is string concatenation in a loop often O(n²) in Python?

### Answer

Strings are **immutable**. Each `s = s + c` allocates a new string and copies the old characters. Lengths 1+2+…+n → O(n²). Fix: list append + `join`, or bytearray.

---

## B3. Two pointers vs sliding window — when each?

### Answer

**Two pointers:** ordered structure / opposite ends / partition / pair sums on sorted data; pointers move based on a condition, often toward each other or in tandem.  
**Sliding window:** contiguous subarray/substring; maintain a valid window invariant; expand right, shrink left (fixed or variable size).  
Window is a special case of same-direction two pointers with a segment invariant.

---

## B4. Prefix sum: what does `prefix[r+1] - prefix[l]` give? Empty range?

### Answer

Sum of `arr[l..r]` inclusive if `prefix[i] = sum(arr[0..i-1])` (length n+1, `prefix[0]=0`). Empty: `l > r` or use `prefix[i]-prefix[i]=0`. Sentinel `prefix[0]=0` makes subarrays starting at 0 clean.

---

## B5. Why hash maps for subarray sum = k?

### Answer

Running prefix `p`. Need prior prefix `p - k`. Store first/last index or frequency of prefixes in a dict → O(n) instead of O(n²). Classic: count of subarrays, longest/shortest with sum k (with care for zeros/negatives).

---

## B6. Explain collision handling at a high level. What does Python use?

### Answer

Two keys → same bucket index. Strategies: chaining (list per bucket) or open addressing (probe). CPython dict: **open addressing** with perturbed probing; hash randomization. Load factor triggers resize (amortized O(1) inserts).

---

## B7. Recursion: base case, recursive case, combine. Call-stack space?

### Answer

Base: stops recursion. Recursive: smaller subproblem(s). Combine: build answer from returns. Space ≥ **depth** of simultaneous frames. Tail calls are **not** optimized in Python → depth-n recursion uses O(n) stack and may hit `RecursionError` (~1000).

---

## B8. Memoization vs tabulation (intro level).

### Answer

**Memo:** top-down recursion + cache; only needed states.  
**Tabulation:** bottom-up loops filling DP table.  
Same asymptotic family often; memo has recursion overhead/stack; tab can be tighter control. Full DP frameworks = Modules 8–9; here only the idea.

---

## B9. Backtracking skeleton in one breath.

### Answer

`choose → explore → unchoose` (or push/recurse/pop). Prune when partial solution can't work. Used for permutations, subsets, combinations, constraint search.

---

## B10. When is a hash set the wrong tool vs two pointers on a sorted array?

### Answer

If you need **ordered** pairs, closest values, or in-place O(1) extra space on sorted input — two pointers. Hash set wins for unsorted membership / pairwise complements when O(n) space is OK.

---

# SECTION C: PROBLEM SOLVING (8+)

For each: approach → code → complexity. Full answers below.

---

## C1. Two Sum (unsorted) — return indices

### Answer

**Pattern:** One-pass hash map value → index.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```

**Trace:** `nums=[2,7,11,15], target=9` → at 7, need 2 in seen → [0,1].

**Edges:** duplicates, no pair, negatives.

**Time O(n), Space O(n).** Sorted + two pointers also works but loses original indices unless you store pairs.

---

## C2. Longest Substring Without Repeating Characters

### Answer

**Pattern:** Variable sliding window + last-seen index (or set).

```python
def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)
    return best
```

**Time O(n), Space O(min(n, alphabet)).**

**Trap:** only advance `left` when the previous occurrence is inside the window.

---

## C3. Subarray Sum Equals K (count)

### Answer

**Pattern:** Prefix + frequency hash.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    freq = defaultdict(int)
    freq[0] = 1
    p = ans = 0
    for x in nums:
        p += x
        ans += freq[p - k]
        freq[p] += 1
    return ans
```

**Time O(n), Space O(n).** Works with negatives (window alone does not).

---

## C4. Product of Array Except Self (no division)

### Answer

**Pattern:** Prefix/suffix products.

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

**Time O(n), Space O(1) extra** (output doesn't count per LC convention).

---

## C5. Valid Anagram / Group Anagrams (pick group)

### Answer

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or 26-count tuple
        groups[key].append(s)
    return list(groups.values())
```

**Time O(n·L log L)** with sort key, or **O(n·L·26)** with counts. Space O(n·L).

---

## C6. Climbing Stairs / Fibonacci with memo

### Answer

```python
def climb(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = climb(n - 1, memo) + climb(n - 2, memo)
    return memo[n]
```

Or iterative O(n)/O(1): `a,b = 1,2; …`.

**Naive recursion fails time; memo O(n).** Recurrence setup: T(n)=T(n-1)+T(n-2)+O(1) before memo.

---

## C7. Subsets (backtracking)

### Answer

```python
def subsets(nums):
    out = []
    path = []
    def dfs(start):
        out.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return out
```

**Time O(n·2ⁿ), Space O(n) stack + output.**

---

## C8. Minimum Size Subarray Sum (positives, target)

### Answer

**Pattern:** Variable window (positives ⇒ shrinking is safe).

```python
def min_subarray_len(target, nums):
    left = 0
    s = 0
    best = float("inf")
    for right, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, right - left + 1)
            s -= nums[left]
            left += 1
    return 0 if best == float("inf") else best
```

**Time O(n), Space O(1).** Negatives → this breaks; use prefix+hash for other variants.

---

## C9. Decode Ways (memoized recursion) — `"226"`

### Answer

```python
def num_decodings(s):
    memo = {}
    def dp(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        if i in memo:
            return memo[i]
        ans = dp(i + 1)
        if i + 1 < len(s) and int(s[i:i+2]) <= 26:
            ans += dp(i + 2)
        memo[i] = ans
        return ans
    return dp(0)
```

`"226"` → 3 (`BBF`, `VF`, `BZ`). **Time O(n), Space O(n).**

---

## C10. Longest Consecutive Sequence (O(n))

### Answer

```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:  # start of a run
            y = x
            while y in s:
                y += 1
            best = max(best, y - x)
    return best
```

**Time O(n)** — each number visited constant times. Space O(n). Sorting is O(n log n); hash set is the intended trick.

---

# SECTION D: TRICK QUESTIONS

These catch shallow understanding.

---

## D1. True/False: Sliding window always works for "subarray sum = k".

### Answer

**False.** Standard shrink-window needs **non-negative** (or otherwise monotone) sums. With negatives, sum can grow when shrinking — use **prefix + hash**.

---

## D2. Is `freq[x] += 1` safe when `x` missing?

### Answer

**No** on plain `dict` → KeyError. Use `freq[x] = freq.get(x,0)+1`, `defaultdict(int)`, or `Counter`.

---

## D3. Complexity of building `set(arr)` then `for x in arr: if x in s`?

### Answer

Build O(n), each lookup O(1) avg → **O(n)** total. Not O(n²). Contrast `if x in arr` on a list inside a loop → O(n²).

---

## D4. Recurrence T(n)=2T(n/2)+O(n). What algorithm family? Is Master Theorem required to say O(n log n)?

### Answer

Mergesort-shaped divide-and-conquer. You can unfold the tree: log n levels × O(n) per level → **O(n log n)** without naming Master Theorem. **MT formally deferred to Module 3** — recurrence setup is enough here.

---

## D5. Does memoization always reduce exponential recursion to linear?

### Answer

**No.** Only when there are **overlapping subproblems** and a polynomial number of distinct states. Tree recursion for all permutations has ~n! states — memo doesn't make it polynomial.

---

## D6. `for i in range(n): for j in range(n): for k in range(j):` — complexity?

### Answer

k runs j times; j runs n; i runs n → i·Σ_j j = n·n(n-1)/2 → **O(n³)**.

---

## D7. Why is `arr.pop(0)` O(n) but `dict.pop(key)` average O(1)?

### Answer

List: contiguous array — removing front shifts all elements. Dict: hash table remove by key — no shift of arbitrary elements (rehash/probe maintenance amortized O(1)).

---

## D8. Can you replace a trie (not yet taught) for "anagram groups"?

### Answer

Yes — sorting/counting keys in a hash map is the right Module 2 tool. Trie is for **prefixes**, not anagram grouping.

---

## D9. Space of DFS recursion on a linked structure of n nodes vs iterative with explicit stack?

### Answer

Both **O(n)** worst-case stack space. Iterative avoids Python recursion limit; same asymptotic space class.

---

## D10. Interview says "optimize this O(n²) pair search." First questions you ask?

### Answer

Sorted? Need indices? Duplicates? Online/stream? Memory limit? → choose two pointers vs hash vs sort+two pointers. Don't jump to exotic structures.

---

# SECTION E: CUMULATIVE MINI MIX (BLIND STYLE)

Short prompts — answers compressed.

---

## E1. Reverse words in a string (strip multiple spaces) — approach?

### Answer

`split()` + reverse + join, or two pointers on a char list in-place. Careful with leading/trailing/multiple spaces. Time O(n).

---

## E2. Find all duplicates in array where `1 ≤ a[i] ≤ n` — O(n) time O(1) extra?

### Answer

Index-sign marking or cyclic sort style swaps. Hash set is O(n) space easier. In-place sign flip: for each x, mark `nums[abs(x)-1]` negative; if already negative, duplicate.

---

## E3. Generate parentheses n pairs — tool?

### Answer

Backtracking with counts of open/close; prune `close > open` or `open > n`.

---

## E4. Is `"ab"/"eidbaooo"` a permutation inclusion (Permutation in String)?

### Answer

Fixed window of len(s1) + frequency match (hash/array counts). O(|s2|·26).

---

## E5. Max profit one buy/sell stock — need DP?

### Answer

No — one pass track min price so far / max profit. O(n)/O(1). Kadane-flavored thinking, still Module 1–2 tools.

---

# SECTION F: SELF-AUDIT CHECKLIST

Before marking Module 2 retention **passed**:

| Check | Done? |
|---|---|
| Taught back Big O 6-skill / simplification without notes | |
| Two pointers + sliding window + prefix + string traps | |
| Hash frequency + prefix-hash + collision model | |
| Recursion stack + tree + memo intro + backtracking skeleton | |
| Did **not** claim Master Theorem mastery | |
| Misses tagged + ledger heats updated | |
| Scoreboard G2 updated | |
| Next: Module 2 **timed verify** (blind) | |

---

# SECTION G: ANSWER KEY QUICK INDEX

| ID | Core answer |
|---|---|
| A1 | O(n²)/O(1) dependent triangle |
| A2 | O(n log n)/O(1) |
| A3 | O(n) amortized runs |
| A4 | O(n) join pattern |
| A5 | list `in` is O(n) |
| A6 | O(2ⁿ)/O(n) fib |
| A7 | slicing O(n²) |
| A8 | O(n·m) |
| A9 | O(n)/O(k) |
| A10 | O(n·n!) |
| A11 | O(n log n) harmonic |
| A12 | avg O(1) / worst O(n) |
| C1–C10 | see full solutions above |
| D1 | window ≠ negatives |
| D4 | unfold tree; MT deferred |

---

**Handoff status after pass:** raise Hashing + Recursion toward `retention-passed`, then run timed verify → `timed-verified` → `complete` only with ledger entries.

---

# SECTION H: EXPANDED RAPID FIRE — COMPLEXITY (A13–A30)

---

## A13.

```python
def f(arr):
    n = len(arr)
    i = 1
    ans = 0
    while i < n:
        for j in range(i):
            ans += arr[j]
        i *= 2
    return ans
```

### Answer

Outer: i doubles → O(log n) iterations. Inner lengths 1+2+4+…≤n → geometric **O(n)** time, O(1) space. Not O(n log n).

> **Time: O(n), Space: O(1)**

---

## A14.

```python
def f(s, t):
    return t in s  # substring
```

### Answer

Interview-safe bound **O(n·m)** worst case; CPython is faster in practice. Space O(1) extra.

---

## A15.

```python
def f(n):
    if n == 0: return
    f(n-1); f(n-1)
```

### Answer

**O(2ⁿ)** calls, **O(n)** stack.

---

## A16.

```python
from functools import lru_cache
@lru_cache(None)
def f(n):
    if n <= 1: return n
    return f(n-1)+f(n-2)
```

### Answer

Memo fib **O(n)** time, **O(n)** space.

---

## A17. Why is `append` amortized O(1)?

### Answer

Occasional geometric resize O(n) is rare; average per append O(1).

---

## A18. `while j: j //= 2` inside `for i in range(n)`?

### Answer

**O(n log n)** if j starts at n each time.

---

## A19. `sorted(set(arr))`?

### Answer

**O(n log n)** time, O(n) space.

---

## A20. Space of storing all subsets as copied paths?

### Answer

**O(n·2ⁿ)** output + O(n) stack.

---

## A21. `for i in range(1,n+1): for j in range(i,n+1,i):`?

### Answer

**O(n log n)** harmonic.

---

## A22. `d[k]` vs `d.get(k)` vs `k in d`?

### Answer

KeyError vs default vs membership — all O(1) avg; behavior differs on miss.

---

## A23. Nested n×n with early break — quote which complexity?

### Answer

**Worst case O(n²)** unless exit is proven always.

---

## A24. T(n)=T(n-1)+O(n)?

### Answer

**O(n²)**.

---

## A25. T(n)=2T(n-1)+O(1)?

### Answer

**O(2ⁿ)**.

---

## A26. n× `insert(0,x)` on list?

### Answer

**O(n²)**. Use deque or append+reverse.

---

## A27. `"".join(n chars)`?

### Answer

**O(n)**.

---

## A28. Hash n strings length L into set?

### Answer

**O(n·L)**.

---

## A29. DFS stack on tree height h?

### Answer

**O(h)**; worst skew O(n).

---

## A30. Master Theorem on this grill?

### Answer

**No** — deferred to Module 3. Use recursion trees.

---

# SECTION I: EXPANDED CONCEPTUAL (B11–B20)

---

## B11. Load factor + resize?

### Answer

n/capacity high → grow table, rehash all — O(n) rare, amortized O(1) inserts.

---

## B12. Why `freq[p-k]` can be >1?

### Answer

Multiple earlier prefixes equal `p-k` ⇒ multiple subarrays ending at i.

---

## B13. Longest vs minimum window — when update best?

### Answer

Longest: after making window valid (post-shrink). Minimum covering: while valid, update then shrink.

---

## B14. Leap of faith?

### Answer

Assume smaller calls work; write base + combine only.

---

## B15. Backtracking vs DP?

### Answer

BT enumerates/prunes. DP reuses overlapping states for count/opt without listing all.

---

## B16. In-place reverse invariant?

### Answer

Outside `[lo,hi]` done; swap ends; move inward.

---

## B17. Kadane vs prefix for max subarray?

### Answer

Both O(n); Kadane O(1) space classic; prefix tracks min prefix.

---

## B18. Why sort for 3Sum?

### Answer

Ordered two-pointers + duplicate skipping.

---

## B19. Call stack vs explicit stack?

### Answer

Same O(depth) class; explicit avoids recursion limit.

---

## B20. MT deferred where?

### Answer

Module 3 Sorting — recurrence setup only in Module 2.

---

# SECTION J: MORE PROBLEMS (C11–C20)

---

## C11. Group Anagrams — 26-count key

### Answer

```python
from collections import defaultdict
def group_anagrams(strs):
    g = defaultdict(list)
    for s in strs:
        cnt = [0]*26
        for c in s: cnt[ord(c)-97]+=1
        g[tuple(cnt)].append(s)
    return list(g.values())
```

**O(n·L·26).**

---

## C12. Longest Palindromic Substring — expand centers

### Answer

```python
def longest_palindrome(s):
    def exp(l,r):
        while l>=0 and r<len(s) and s[l]==s[r]:
            l-=1; r+=1
        return s[l+1:r]
    best=""
    for i in range(len(s)):
        for pal in (exp(i,i), exp(i,i+1)):
            if len(pal)>len(best): best=pal
    return best
```

**O(n²)/O(1).**

---

## C13. Subarrays divisible by K

### Answer

```python
def subarraysDivByK(nums,k):
    freq={0:1}; p=ans=0
    for x in nums:
        p=(p+x)%k
        ans+=freq.get(p,0)
        freq[p]=freq.get(p,0)+1
    return ans
```

---

## C14. Permutation in String

### Answer

Fixed window Counter equality — O(|s2|·26).

```python
from collections import Counter
def checkInclusion(s1,s2):
    need,window=Counter(s1),Counter(); k=len(s1)
    for i,c in enumerate(s2):
        window[c]+=1
        if i>=k:
            left=s2[i-k]; window[left]-=1
            if window[left]==0: del window[left]
        if window==need: return True
    return False
```

---

## C15. Generate Parentheses

### Answer

BT with `opens<n` and `closes<opens` constraints. O(Catalan·n).

---

## C16. Combination Sum (reuse allowed)

### Answer

DFS `dfs(i, remain)` recurse same `i` for reuse; prune `cands[i]>remain`.

---

## C17. Sort Colors Dutch flag

### Answer

`lo,mid,hi` invariants; on swap 2 with hi, **don't** mid++.

---

## C18. Best Time Stock I

### Answer

Track min so far / max profit — O(n)/O(1).

---

## C19. Word Break memo

### Answer

`dp(i)`: try all `s[i:j] in words` and `dp(j)`. Memo O(n²·L) style.

---

## C20. Find All Anagrams

### Answer

Same fixed-window freq as C14; record start indices.

---

# SECTION K: TRICKS EXPANDED (D11–D25)

---

## D11. Counter always O(1)? **False** — build O(L); compare O(keys).

## D12. Memo on all permutations → polynomial? **False** — n! outputs.

## D13. Loop `pop(0)` n times? **O(n²)**.

## D14. Prefix of empty array? **`[0]`**.

## D15. Two pointers pair sum on unsorted? **Need sort or hash**.

## D16. Floyd on array duplicate — Module 2 earned? **Yes as array insight**.

## D17. `lru_cache` with list arg? **TypeError** — use tuple.

## D18. Memo fib recursion n=2000? **May RecursionError** — iterate.

## D19. Counting sort always O(n)? **O(n+U)** — U matters.

## D20. Dict worst O(1)? **Average**; worst O(n) pathological.

## D21. Exactly K distinct substrings? **`at_most(K)-at_most(K-1)`**.

## D22. Binary search unsorted values? **No**; answer-space BS later.

## D23. `s[::-1]` cost? **O(n)** time & space.

## D24. Why `freq[0]=1`? **Subarrays from index 0**.

## D25. Product Except Self need hash? **No** — prefix/suffix.

---

# SECTION L: HASHING + RECURSION INTEGRATION

---

## L1. Letter Combinations of Phone Number

### Answer

Dict digit→letters + BT. O(4ⁿ·n) style.

```python
def letterCombinations(digits):
    if not digits: return []
    m={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}
    out,path=[],[]
    def dfs(i):
        if i==len(digits):
            out.append("".join(path)); return
        for ch in m[digits[i]]:
            path.append(ch); dfs(i+1); path.pop()
    dfs(0); return out
```

---

## L2. Word Search I (single word)

### Answer

Board BT mark/unmark — **no trie** required. O(RC·4^L).

---

## L3. Target Sum (±)

### Answer

Memo `(i,s)`; branch +/−. O(n·sumRange).

---

## L4. Clone LL random — map old→new

### Answer

Hash map + two passes (Module 4 owns deep LL; map pattern is hashing).

---

## L5. Subset sum count vs list all subsets

### Answer

Count → DP/memo. List all → BT must output exponential.

---

## L6. Top-K frequent before heaps module?

### Answer

Counter + bucket by frequency is earned; `heapq.nlargest` OK but heap theory is Module 6.

---

# SECTION M: WEEK-1-STYLE TRACES

---

## M1. Subarray sum k=`3`, nums=`[1,2,3]`

### Answer

Prefixes 1,3,6 → hits: `[1,2]` and `[3]` → **2**.

---

## M2. Decode ways `"2101"`

### Answer

Only `2,10,1` — **1 way**. Zero handling kills `21,0,1`.

---

## M3. Min size subarray sum target 7, `[2,3,1,2,4,3]`

### Answer

Best window `[4,3]` length **2**.

---

## M4. Two Sum `[3,2,4]`, target 6

### Answer

At 4 need 2 → indices `[1,2]`.

---

## M5. Longest substring no repeat `"pwwkew"`

### Answer

`"wke"` length **3**.

---

# SECTION N: SELF-AUDIT EXPANDED

| Check | Done? |
|---|---|
| Big O + hidden costs + harmonic | |
| Arrays TP/window/prefix/strings | |
| Hash freq/prefix-hash/anagrams | |
| Recursion stack/memo/BT | |
| Integration L-set | |
| MT not claimed | |
| Tags → ledger + scoreboard | |
| Next: Module 2 timed verify | |

---

*End of Module 2 Retention Grill (expanded).*
