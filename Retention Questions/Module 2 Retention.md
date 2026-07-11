<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 2 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 2 Retention.keys.md`. Attempt first, then grade.

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 1)

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 2)

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 3)

## A4.

```python
def f(s):
    out = []
    for c in s:
        out.append(c)
    return "".join(out)
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 4)

## A5.

```python
def f(arr, x):
    return x in arr  # arr is a list
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 5)

## A6.

```python
def f(n):
    if n <= 1:
        return n
    return f(n - 1) + f(n - 2)
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 6)

## A7.

```python
def f(arr):
    n = len(arr)
    for i in range(n):
        arr[:i]  # slicing
    return arr
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 7)

## A8.

```python
def f(a, b):
    # a length n, b length m
    for x in a:
        for y in b:
            pass
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 8)

## A9.

```python
def f(arr):
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    return freq
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 9)

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 10)

## A11.

Dependent nesting: outer `i = 1..n`, inner `j = 1; j < n; j += i`. Complexity?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 11)

## A12.

`dict` average vs worst lookup? When does worst happen?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 12)

# SECTION B: CONCEPTUAL (TEACH-BACK)

Speak like an interview. Then compare.

---

## B1. State the three Big-O simplification rules.


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 13)

## B2. Why is string concatenation in a loop often O(n²) in Python?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 14)

## B3. Two pointers vs sliding window — when each?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 15)

## B4. Prefix sum: what does `prefix[r+1] - prefix[l]` give? Empty range?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 16)

## B5. Why hash maps for subarray sum = k?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 17)

## B6. Explain collision handling at a high level. What does Python use?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 18)

## B7. Recursion: base case, recursive case, combine. Call-stack space?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 19)

## B8. Memoization vs tabulation (intro level).


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 20)

## B9. Backtracking skeleton in one breath.


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 21)

## B10. When is a hash set the wrong tool vs two pointers on a sorted array?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 22)

# SECTION C: PROBLEM SOLVING (8+)

For each: approach → code → complexity. Full answers below.

---

## C1. Two Sum (unsorted) — return indices


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 23)

## C2. Longest Substring Without Repeating Characters


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 24)

## C3. Subarray Sum Equals K (count)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 25)

## C4. Product of Array Except Self (no division)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 26)

## C5. Valid Anagram / Group Anagrams (pick group)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 27)

## C6. Climbing Stairs / Fibonacci with memo


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 28)

## C7. Subsets (backtracking)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 29)

## C8. Minimum Size Subarray Sum (positives, target)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 30)

## C9. Decode Ways (memoized recursion) — `"226"`


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 31)

## C10. Longest Consecutive Sequence (O(n))


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 32)

# SECTION D: TRICK QUESTIONS

These catch shallow understanding.

---

## D1. True/False: Sliding window always works for "subarray sum = k".


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 33)

## D2. Is `freq[x] += 1` safe when `x` missing?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 34)

## D3. Complexity of building `set(arr)` then `for x in arr: if x in s`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 35)

## D4. Recurrence T(n)=2T(n/2)+O(n). What algorithm family? Is Master Theorem required to say O(n log n)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 36)

## D5. Does memoization always reduce exponential recursion to linear?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 37)

## D6. `for i in range(n): for j in range(n): for k in range(j):` — complexity?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 38)

## D7. Why is `arr.pop(0)` O(n) but `dict.pop(key)` average O(1)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 39)

## D8. Can you replace a trie (not yet taught) for "anagram groups"?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 40)

## D9. Space of DFS recursion on a linked structure of n nodes vs iterative with explicit stack?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 41)

## D10. Interview says "optimize this O(n²) pair search." First questions you ask?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 42)

# SECTION E: CUMULATIVE MINI MIX (BLIND STYLE)

Short prompts — answers compressed.

---

## E1. Reverse words in a string (strip multiple spaces) — approach?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 43)

## E2. Find all duplicates in array where `1 ≤ a[i] ≤ n` — O(n) time O(1) extra?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 44)

## E3. Generate parentheses n pairs — tool?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 45)

## E4. Is `"ab"/"eidbaooo"` a permutation inclusion (Permutation in String)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 46)

## E5. Max profit one buy/sell stock — need DP?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 47)

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 48)

## A14.

```python
def f(s, t):
    return t in s  # substring
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 49)

## A15.

```python
def f(n):
    if n == 0: return
    f(n-1); f(n-1)
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 50)

## A16.

```python
from functools import lru_cache
@lru_cache(None)
def f(n):
    if n <= 1: return n
    return f(n-1)+f(n-2)
```


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 51)

## A17. Why is `append` amortized O(1)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 52)

## A18. `while j: j //= 2` inside `for i in range(n)`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 53)

## A19. `sorted(set(arr))`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 54)

## A20. Space of storing all subsets as copied paths?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 55)

## A21. `for i in range(1,n+1): for j in range(i,n+1,i):`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 56)

## A22. `d[k]` vs `d.get(k)` vs `k in d`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 57)

## A23. Nested n×n with early break — quote which complexity?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 58)

## A24. T(n)=T(n-1)+O(n)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 59)

## A25. T(n)=2T(n-1)+O(1)?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 60)

## A26. n× `insert(0,x)` on list?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 61)

## A27. `"".join(n chars)`?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 62)

## A28. Hash n strings length L into set?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 63)

## A29. DFS stack on tree height h?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 64)

## A30. Master Theorem on this grill?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 65)

# SECTION I: EXPANDED CONCEPTUAL (B11–B20)

---

## B11. Load factor + resize?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 66)

## B12. Why `freq[p-k]` can be >1?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 67)

## B13. Longest vs minimum window — when update best?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 68)

## B14. Leap of faith?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 69)

## B15. Backtracking vs DP?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 70)

## B16. In-place reverse invariant?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 71)

## B17. Kadane vs prefix for max subarray?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 72)

## B18. Why sort for 3Sum?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 73)

## B19. Call stack vs explicit stack?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 74)

## B20. MT deferred where?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 75)

# SECTION J: MORE PROBLEMS (C11–C20)

---

## C11. Group Anagrams — 26-count key


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 76)

## C12. Longest Palindromic Substring — expand centers


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 77)

## C13. Subarrays divisible by K


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 78)

## C14. Permutation in String


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 79)

## C15. Generate Parentheses


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 80)

## C16. Combination Sum (reuse allowed)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 81)

## C17. Sort Colors Dutch flag


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 82)

## C18. Best Time Stock I


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 83)

## C19. Word Break memo


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 84)

## C20. Find All Anagrams


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 85)

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


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 86)

## L2. Word Search I (single word)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 87)

## L3. Target Sum (±)


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 88)

## L4. Clone LL random — map old→new


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 89)

## L5. Subset sum count vs list all subsets


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 90)

## L6. Top-K frequent before heaps module?


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 91)

# SECTION M: WEEK-1-STYLE TRACES

---

## M1. Subarray sum k=`3`, nums=`[1,2,3]`


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 92)

## M2. Decode ways `"2101"`


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 93)

## M3. Min size subarray sum target 7, `[2,3,1,2,4,3]`


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 94)

## M4. Two Sum `[3,2,4]`, target 6


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 95)

## M5. Longest substring no repeat `"pwwkew"`


> **Answer key:** `Retention Questions/keys/Module 2 Retention.keys.md` (block 96)

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
