# Answer Key — Module 2 Retention.md

**Source questions:** `Retention Questions/Module 2 Retention.md`

Attempt the questions file first. Do not open this during timed/blind work.

---

<!-- answer block 1 -->
### Answer

Outer `i`: n values. Inner `j`: `n - i` iterations. Total iterations = n + (n-1) + … + 1 = n(n+1)/2 → **O(n²)** time.  
Body is O(1). Space: scalars → **O(1)**.

> **Time: O(n²), Space: O(1)**

---


<!-- answer block 2 -->
### Answer

Outer: n iterations. Inner: `j` doubles → **O(log n)** per outer. Total **O(n log n)**. Space **O(1)**.

> **Time: O(n log n), Space: O(1)**

---


<!-- answer block 3 -->
### Answer

Classic "two pointers advance" / run-length style. Each index visited by `j` at most once; `i` jumps to `j`. **O(n)** time, **O(1)** space. Not O(n²) — inner work is amortized linear.

> **Time: O(n), Space: O(1)**

---


<!-- answer block 4 -->
### Answer

Append O(1) amortized each; join O(n). **O(n)** time, **O(n)** space. Contrast with `out = out + c` which would be O(n²).

> **Time: O(n), Space: O(n)**

---


<!-- answer block 5 -->
### Answer

List membership is linear scan → **O(n)** time, **O(1)** space. If `arr` were a `set`, O(1) average.

> **Time: O(n), Space: O(1)**

---


<!-- answer block 6 -->
### Answer

Classic fib tree: **O(φⁿ) ⊂ O(2ⁿ)** time, **O(n)** stack space. Recurrence T(n)=T(n-1)+T(n-2)+O(1). Overlapping subproblems → memo makes O(n) time / O(n) space.

> **Time: O(2ⁿ), Space: O(n)** (naive)

---


<!-- answer block 7 -->
### Answer

Slice `arr[:i]` costs O(i) and allocates. Sum 0+1+…+(n-1) → **O(n²)** time, **O(n)** extra peak space for largest slice.

> **Time: O(n²), Space: O(n)**

---


<!-- answer block 8 -->
### Answer

Different inputs → **O(n·m)** time, **O(1)** space. Do not collapse to O(n²) unless n=m is stated.

> **Time: O(n·m), Space: O(1)**

---


<!-- answer block 9 -->
### Answer

n dict ops, O(1) average each → **O(n)** time, **O(k)** space (k = distinct keys ≤ n).

> **Time: O(n), Space: O(k) ≤ O(n)**

---


<!-- answer block 10 -->
### Answer

n! leaves; work along paths → **O(n·n!)** time typical (copy path O(n) at leaves, or O(n!) nodes × branching). Space: O(n) recursion depth + O(n·n!) output.

> **Time: O(n·n!), Space: O(n) stack + output**

---


<!-- answer block 11 -->
### Answer

For each i, inner runs ~ n/i times. Total Σ_{i=1}^{n} n/i = n·H_n = **O(n log n)** (harmonic series).

> **Time: O(n log n)**

---


<!-- answer block 12 -->
### Answer

Average **O(1)**; worst **O(n)** with pathological collisions (or adversarial keys historically). Python uses open addressing + randomized hash seed — treat as amortized O(1) in interviews unless asked about attacks.

---


<!-- answer block 13 -->
### Answer

1. Drop constant factors (`3n` → O(n)).  
2. Drop non-dominant terms (`n² + n` → O(n²)).  
3. Different input sizes → different variables (`O(n + m)`, not fake `O(n)`).

---


<!-- answer block 14 -->
### Answer

Strings are **immutable**. Each `s = s + c` allocates a new string and copies the old characters. Lengths 1+2+…+n → O(n²). Fix: list append + `join`, or bytearray.

---


<!-- answer block 15 -->
### Answer

**Two pointers:** ordered structure / opposite ends / partition / pair sums on sorted data; pointers move based on a condition, often toward each other or in tandem.  
**Sliding window:** contiguous subarray/substring; maintain a valid window invariant; expand right, shrink left (fixed or variable size).  
Window is a special case of same-direction two pointers with a segment invariant.

---


<!-- answer block 16 -->
### Answer

Sum of `arr[l..r]` inclusive if `prefix[i] = sum(arr[0..i-1])` (length n+1, `prefix[0]=0`). Empty: `l > r` or use `prefix[i]-prefix[i]=0`. Sentinel `prefix[0]=0` makes subarrays starting at 0 clean.

---


<!-- answer block 17 -->
### Answer

Running prefix `p`. Need prior prefix `p - k`. Store first/last index or frequency of prefixes in a dict → O(n) instead of O(n²). Classic: count of subarrays, longest/shortest with sum k (with care for zeros/negatives).

---


<!-- answer block 18 -->
### Answer

Two keys → same bucket index. Strategies: chaining (list per bucket) or open addressing (probe). CPython dict: **open addressing** with perturbed probing; hash randomization. Load factor triggers resize (amortized O(1) inserts).

---


<!-- answer block 19 -->
### Answer

Base: stops recursion. Recursive: smaller subproblem(s). Combine: build answer from returns. Space ≥ **depth** of simultaneous frames. Tail calls are **not** optimized in Python → depth-n recursion uses O(n) stack and may hit `RecursionError` (~1000).

---


<!-- answer block 20 -->
### Answer

**Memo:** top-down recursion + cache; only needed states.  
**Tabulation:** bottom-up loops filling DP table.  
Same asymptotic family often; memo has recursion overhead/stack; tab can be tighter control. Full DP frameworks = Modules 8–9; here only the idea.

---


<!-- answer block 21 -->
### Answer

`choose → explore → unchoose` (or push/recurse/pop). Prune when partial solution can't work. Used for permutations, subsets, combinations, constraint search.

---


<!-- answer block 22 -->
### Answer

If you need **ordered** pairs, closest values, or in-place O(1) extra space on sorted input — two pointers. Hash set wins for unsorted membership / pairwise complements when O(n) space is OK.

---


<!-- answer block 23 -->
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


<!-- answer block 24 -->
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


<!-- answer block 25 -->
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


<!-- answer block 26 -->
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


<!-- answer block 27 -->
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


<!-- answer block 28 -->
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


<!-- answer block 29 -->
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


<!-- answer block 30 -->
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


<!-- answer block 31 -->
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


<!-- answer block 32 -->
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


<!-- answer block 33 -->
### Answer

**False.** Standard shrink-window needs **non-negative** (or otherwise monotone) sums. With negatives, sum can grow when shrinking — use **prefix + hash**.

---


<!-- answer block 34 -->
### Answer

**No** on plain `dict` → KeyError. Use `freq[x] = freq.get(x,0)+1`, `defaultdict(int)`, or `Counter`.

---


<!-- answer block 35 -->
### Answer

Build O(n), each lookup O(1) avg → **O(n)** total. Not O(n²). Contrast `if x in arr` on a list inside a loop → O(n²).

---


<!-- answer block 36 -->
### Answer

Mergesort-shaped divide-and-conquer. You can unfold the tree: log n levels × O(n) per level → **O(n log n)** without naming Master Theorem. **MT formally deferred to Module 3** — recurrence setup is enough here.

---


<!-- answer block 37 -->
### Answer

**No.** Only when there are **overlapping subproblems** and a polynomial number of distinct states. Tree recursion for all permutations has ~n! states — memo doesn't make it polynomial.

---


<!-- answer block 38 -->
### Answer

k runs j times; j runs n; i runs n → i·Σ_j j = n·n(n-1)/2 → **O(n³)**.

---


<!-- answer block 39 -->
### Answer

List: contiguous array — removing front shifts all elements. Dict: hash table remove by key — no shift of arbitrary elements (rehash/probe maintenance amortized O(1)).

---


<!-- answer block 40 -->
### Answer

Yes — sorting/counting keys in a hash map is the right Module 2 tool. Trie is for **prefixes**, not anagram grouping.

---


<!-- answer block 41 -->
### Answer

Both **O(n)** worst-case stack space. Iterative avoids Python recursion limit; same asymptotic space class.

---


<!-- answer block 42 -->
### Answer

Sorted? Need indices? Duplicates? Online/stream? Memory limit? → choose two pointers vs hash vs sort+two pointers. Don't jump to exotic structures.

---


<!-- answer block 43 -->
### Answer

`split()` + reverse + join, or two pointers on a char list in-place. Careful with leading/trailing/multiple spaces. Time O(n).

---


<!-- answer block 44 -->
### Answer

Index-sign marking or cyclic sort style swaps. Hash set is O(n) space easier. In-place sign flip: for each x, mark `nums[abs(x)-1]` negative; if already negative, duplicate.

---


<!-- answer block 45 -->
### Answer

Backtracking with counts of open/close; prune `close > open` or `open > n`.

---


<!-- answer block 46 -->
### Answer

Fixed window of len(s1) + frequency match (hash/array counts). O(|s2|·26).

---


<!-- answer block 47 -->
### Answer

No — one pass track min price so far / max profit. O(n)/O(1). Kadane-flavored thinking, still Module 1–2 tools.

---


<!-- answer block 48 -->
### Answer

Outer: i doubles → O(log n) iterations. Inner lengths 1+2+4+…≤n → geometric **O(n)** time, O(1) space. Not O(n log n).

> **Time: O(n), Space: O(1)**

---


<!-- answer block 49 -->
### Answer

Interview-safe bound **O(n·m)** worst case; CPython is faster in practice. Space O(1) extra.

---


<!-- answer block 50 -->
### Answer

**O(2ⁿ)** calls, **O(n)** stack.

---


<!-- answer block 51 -->
### Answer

Memo fib **O(n)** time, **O(n)** space.

---


<!-- answer block 52 -->
### Answer

Occasional geometric resize O(n) is rare; average per append O(1).

---


<!-- answer block 53 -->
### Answer

**O(n log n)** if j starts at n each time.

---


<!-- answer block 54 -->
### Answer

**O(n log n)** time, O(n) space.

---


<!-- answer block 55 -->
### Answer

**O(n·2ⁿ)** output + O(n) stack.

---


<!-- answer block 56 -->
### Answer

**O(n log n)** harmonic.

---


<!-- answer block 57 -->
### Answer

KeyError vs default vs membership — all O(1) avg; behavior differs on miss.

---


<!-- answer block 58 -->
### Answer

**Worst case O(n²)** unless exit is proven always.

---


<!-- answer block 59 -->
### Answer

**O(n²)**.

---


<!-- answer block 60 -->
### Answer

**O(2ⁿ)**.

---


<!-- answer block 61 -->
### Answer

**O(n²)**. Use deque or append+reverse.

---


<!-- answer block 62 -->
### Answer

**O(n)**.

---


<!-- answer block 63 -->
### Answer

**O(n·L)**.

---


<!-- answer block 64 -->
### Answer

**O(h)**; worst skew O(n).

---


<!-- answer block 65 -->
### Answer

**No** — deferred to Module 3. Use recursion trees.

---


<!-- answer block 66 -->
### Answer

n/capacity high → grow table, rehash all — O(n) rare, amortized O(1) inserts.

---


<!-- answer block 67 -->
### Answer

Multiple earlier prefixes equal `p-k` ⇒ multiple subarrays ending at i.

---


<!-- answer block 68 -->
### Answer

Longest: after making window valid (post-shrink). Minimum covering: while valid, update then shrink.

---


<!-- answer block 69 -->
### Answer

Assume smaller calls work; write base + combine only.

---


<!-- answer block 70 -->
### Answer

BT enumerates/prunes. DP reuses overlapping states for count/opt without listing all.

---


<!-- answer block 71 -->
### Answer

Outside `[lo,hi]` done; swap ends; move inward.

---


<!-- answer block 72 -->
### Answer

Both O(n); Kadane O(1) space classic; prefix tracks min prefix.

---


<!-- answer block 73 -->
### Answer

Ordered two-pointers + duplicate skipping.

---


<!-- answer block 74 -->
### Answer

Same O(depth) class; explicit avoids recursion limit.

---


<!-- answer block 75 -->
### Answer

Module 3 Sorting — recurrence setup only in Module 2.

---


<!-- answer block 76 -->
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


<!-- answer block 77 -->
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


<!-- answer block 78 -->
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


<!-- answer block 79 -->
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


<!-- answer block 80 -->
### Answer

BT with `opens<n` and `closes<opens` constraints. O(Catalan·n).

---


<!-- answer block 81 -->
### Answer

DFS `dfs(i, remain)` recurse same `i` for reuse; prune `cands[i]>remain`.

---


<!-- answer block 82 -->
### Answer

`lo,mid,hi` invariants; on swap 2 with hi, **don't** mid++.

---


<!-- answer block 83 -->
### Answer

Track min so far / max profit — O(n)/O(1).

---


<!-- answer block 84 -->
### Answer

`dp(i)`: try all `s[i:j] in words` and `dp(j)`. Memo O(n²·L) style.

---


<!-- answer block 85 -->
### Answer

Same fixed-window freq as C14; record start indices.

---


<!-- answer block 86 -->
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


<!-- answer block 87 -->
### Answer

Board BT mark/unmark — **no trie** required. O(RC·4^L).

---


<!-- answer block 88 -->
### Answer

Memo `(i,s)`; branch +/−. O(n·sumRange).

---


<!-- answer block 89 -->
### Answer

Hash map + two passes (Module 4 owns deep LL; map pattern is hashing).

---


<!-- answer block 90 -->
### Answer

Count → DP/memo. List all → BT must output exponential.

---


<!-- answer block 91 -->
### Answer

Counter + bucket by frequency is earned; `heapq.nlargest` OK but heap theory is Module 6.

---


<!-- answer block 92 -->
### Answer

Prefixes 1,3,6 → hits: `[1,2]` and `[3]` → **2**.

---


<!-- answer block 93 -->
### Answer

Only `2,10,1` — **1 way**. Zero handling kills `21,0,1`.

---


<!-- answer block 94 -->
### Answer

Best window `[4,3]` length **2**.

---


<!-- answer block 95 -->
### Answer

At 4 need 2 → indices `[1,2]`.

---


<!-- answer block 96 -->
### Answer

`"wke"` length **3**.

---


