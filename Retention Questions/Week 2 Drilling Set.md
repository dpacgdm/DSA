# WEEK 2: PROBLEM DRILLING — INTEGRATION SET

---

**The rules are different now.**

Days 1-4 told you which pattern to use. Real interviews and competitions don't. These problems:

1. **Don't tell you the pattern.** You identify it.
2. **May combine multiple techniques** from different topics.
3. **May have multiple valid approaches** — choose the best and justify why.
4. **Include traps** — problems that look like one pattern but are actually another.
5. **Escalate sharply.**

For each problem:
- State your approach **before** coding
- Justify why you chose it over alternatives
- Full solution, trace, edge cases, complexity

---

### Problem 1: Longest Palindromic Substring

Given a string `s`, return the longest palindromic substring.

```
Input: "babad"
Output: "bab" (or "aba" — both valid)

Input: "cbbd"
Output: "bb"
```

---

### Problem 2: Product of Array Except Self

Given an integer array, return an array where each element is the product of all elements except itself. **You must solve it in O(n) time without using division.**

```
Input: [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

---

### Problem 3: Find the Duplicate Number

Given an array of `n+1` integers where each integer is in the range `[1, n]`, there is exactly **one** duplicate number (but it may appear more than twice). Find it.

**Constraints:**
- You must not modify the array
- You must use only O(1) extra space

```
Input: [1, 3, 4, 2, 2]
Output: 2

Input: [3, 1, 3, 4, 2]
Output: 3
```

Hint: Think beyond arrays and hashing. What data structure does this array implicitly define?

---

### Problem 4: Decode Ways

A message containing letters A-Z is encoded as numbers: 'A' → 1, 'B' → 2, ..., 'Z' → 26. Given a string of digits, count the number of ways to decode it.

```
Input: "226"
Output: 3 ("BZ" = 2,26 | "VF" = 22,6 | "BBF" = 2,2,6)

Input: "06"
Output: 0 (no valid decoding — '0' alone doesn't map to any letter)
```

---

### Problem 5: Subarray Sum Divisible by K

Given an array of integers and an integer `k`, return the number of contiguous subarrays whose sum is divisible by `k`.

```
Input: nums = [4, 5, 0, -2, -3, 1], k = 5
Output: 7
```

**This looks like a familiar pattern but has a mathematical twist. What is it?**

---

### Problem 6: Minimum Size Subarray Sum

Given an array of **positive** integers and a target, find the **minimal length** of a contiguous subarray whose sum is **greater than or equal to** target. Return 0 if no such subarray exists.

```
Input: target = 7, nums = [2, 3, 1, 2, 4, 3]
Output: 2 (subarray [4, 3])

Input: target = 4, nums = [1, 4, 4]
Output: 1
```

---

### Problem 7: Word Ladder Length

Given two words `beginWord` and `endWord`, and a word list, find the length of the shortest transformation sequence from `beginWord` to `endWord`, such that:
- Only one letter can be changed at a time
- Each transformed word must exist in the word list

Return 0 if no transformation sequence exists.

```
Input: beginWord = "hit", endWord = "cog"
       wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5 (hit → hot → dot → dog → cog)
```

**This is NOT a recursion problem. Think about what "shortest path" implies.**

---

### Problem 8: String Interleaving

Given strings `s1`, `s2`, and `s3`, determine if `s3` is formed by interleaving `s1` and `s2`.

An interleaving maintains the relative order of characters from each source string.

```
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: True

Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: False
```

---

### Problem 9: Next Permutation

Implement the "next permutation" function — rearrange the array into the next lexicographically greater permutation. If the array is the largest permutation, rearrange to the smallest (sorted ascending).

**Must be in-place with O(1) extra space.**

```
Input: [1, 2, 3] → Output: [1, 3, 2]
Input: [3, 2, 1] → Output: [1, 2, 3]
Input: [1, 1, 5] → Output: [1, 5, 1]
Input: [1, 3, 2] → Output: [2, 1, 3]
```

**This is a pure algorithmic thinking problem. No standard pattern applies directly.**

---

### Problem 10: Longest Valid Parentheses

Given a string containing only `(` and `)`, find the length of the longest valid (well-formed) parentheses substring.

```
Input: "(()"
Output: 2

Input: ")()())"
Output: 4

Input: ""
Output: 0
```

**Multiple approaches exist. Solve it two different ways — pick the best and explain why.**

---

### Problem 11: Count of Range Sum

Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums that lie in `[lower, upper]` inclusive.

Range sum `S(i, j)` = sum of elements from index i to j.

```
Input: nums = [-2, 5, -1], lower = -2, upper = 2
Output: 3 (ranges: [0,0]=-2, [2,2]=-1, [0,2]=2)
```

**Brute force is O(n²). Can you do O(n log n)?**

Hint: Think about what technique from this week handles "count pairs satisfying a condition on prefix sums."

---

### Problem 12: The Boss — Alien Dictionary

Given a list of words sorted in an alien language's alphabetical order, derive the order of characters in that language.

```
Input: ["wrt", "wrf", "er", "ett", "rftt"]
Output: "wertf"

Input: ["z", "x"]
Output: "zx"

Input: ["z", "x", "z"]
Output: "" (invalid — contradictory ordering)
```

**This combines multiple data structures and algorithms. Identify each piece before coding.**

---



**12 problems. No pattern labels. No hints about which topic applies (except where deliberately misdirecting). This is the real thing.**

**Go.**


# Problem 1: Longest Palindromic Substring

## Approach — Before Coding

**Pattern identified: Expand Around Center**

Why this over alternatives:
- **Brute force** (check all substrings): O(n³) — too slow
- **DP table** (dp[i][j] = is s[i..j] a palindrome): O(n²) time and O(n²) space
- **Expand around center**: O(n²) time and **O(1)** space — same time as DP but better space

Every palindrome has a center. For odd-length palindromes, the center is one character. For even-length, the center is between two characters. There are 2n-1 possible centers. From each center, expand outward while characters match.

## Solution

```python
def longest_palindrome(s):
    if len(s) < 2:
        return s

    start = 0
    max_len = 1

    def expand(left, right):
        nonlocal start, max_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                max_len = right - left + 1
                start = left
            left -= 1
            right += 1

    for i in range(len(s)):
        expand(i, i)       # odd-length palindromes
        expand(i, i + 1)   # even-length palindromes

    return s[start:start + max_len]
```

## Trace

```
s = "babad"

i=0: expand(0,0) 'b': left=-1 stop. len=1.
     expand(0,1) 'b','a': mismatch. skip.

i=1: expand(1,1) 'a': 
     expand to (0,2): s[0]='b', s[2]='b' match! len=3, start=0
     expand to (-1,3): stop.
     → "bab", len=3. max_len=3, start=0.
     expand(1,2) 'a','b': mismatch.

i=2: expand(2,2) 'b':
     expand to (1,3): s[1]='a', s[3]='a' match! len=3.
     expand to (0,4): s[0]='b', s[4]='d' mismatch.
     → "aba", len=3. Ties max, no update.
     expand(2,3) 'b','a': mismatch.

i=3: expand(3,3) 'a': expand to (2,4) 'b'≠'d'. len=1.
     expand(3,4) 'a','d': mismatch.

i=4: expand(4,4) 'd': len=1.

return s[0:3] = "bab" ✅
```

## Edge Cases

**Single character:** `s="a"` → return "a" ✅

**All same characters:** `s="aaaa"` → expand from center finds full string. return "aaaa" ✅

## Complexity

**Time:** n centers × each expansion at most O(n) → **O(n²)**

**Space:** Only tracking start, max_len → **O(1)**

> **Time: O(n²), Space: O(1)**

---

# Problem 2: Product of Array Except Self

## Approach — Before Coding

**Pattern identified: Prefix/Suffix Product (Two-Pass)**

Without division, we can't just compute total product and divide. Instead: for each position i, the answer is (product of everything to the left) × (product of everything to the right).

Pass 1: Build left prefix products. Pass 2: Build right suffix products. Multiply them together.

To achieve O(1) extra space (excluding output), we can use the output array for the left pass, then multiply in the right pass using a running variable.

## Solution

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n

    # Pass 1: left prefix products
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]

    # Pass 2: right suffix products, multiply into result
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]

    return result
```

## Trace

```
nums = [1, 2, 3, 4]

Pass 1 (left products):
  i=0: result[0]=1, left=1×1=1
  i=1: result[1]=1, left=1×2=2
  i=2: result[2]=2, left=2×3=6
  i=3: result[3]=6, left=6×4=24
  result = [1, 1, 2, 6]

Pass 2 (right products):
  i=3: result[3]=6×1=6, right=1×4=4
  i=2: result[2]=2×4=8, right=4×3=12
  i=1: result[1]=1×12=12, right=12×2=24
  i=0: result[0]=1×24=24, right=24×1=24
  result = [24, 12, 8, 6] ✅
```

## Edge Cases

**Contains zero:** `nums=[1,2,0,4]` → result=[0,0,8,0]. Only index 2 has non-zero (product of 1×2×4). ✅

**Two zeros:** `nums=[0,0]` → result=[0,0]. Both positions see a zero on the other side. ✅

## Complexity

**Time:** Two passes of n → **O(n)**

**Space:** Output array doesn't count. `left_product`, `right_product` → **O(1)** extra.

> **Time: O(n), Space: O(1)** extra

---

# Problem 3: Find the Duplicate Number

## Approach — Before Coding

**Pattern identified: Floyd's Cycle Detection (Tortoise and Hare)**

Can't modify array → no index-marking trick. O(1) space → no hash set. Can't sort → no adjacent comparison.

**The key insight:** Treat the array as a function f(i) = nums[i]. Since values are in [1, n] and the array has n+1 elements, this defines a mapping from {0, 1, ..., n} to {1, 2, ..., n}. Starting from index 0 and following the chain 0 → nums[0] → nums[nums[0]] → ..., we get a sequence that MUST have a cycle (by pigeonhole — n+1 values mapped into n slots). The duplicate number is the **entrance to the cycle.**

This is exactly Floyd's algorithm, used for linked list cycle detection.

## Solution

```python
def find_duplicate(nums):
    # Phase 1: Detect cycle (find meeting point)
    slow = nums[0]
    fast = nums[nums[0]]

    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # Phase 2: Find cycle entrance
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

## Why the Cycle Entrance Is the Duplicate

Consider the implicit linked list: 0 → nums[0] → nums[nums[0]] → ...

The duplicate value d appears at multiple indices. When following the chain, multiple nodes point to node d — that creates the junction where a "tail" meets a "cycle." The entrance to the cycle is the node that multiple pointers converge on, which is the duplicate value.

## Trace

```
nums = [1, 3, 4, 2, 2]
Indices: 0  1  2  3  4

Implicit graph: 0→1, 1→3, 2→4, 3→2, 4→2
Chain: 0 → 1 → 3 → 2 → 4 → 2 → 4 → 2 ...
                      ↑___________↓  (cycle: 2→4→2)

Phase 1:
slow = nums[0] = 1
fast = nums[nums[0]] = nums[1] = 3

Step 1: slow = nums[1] = 3, fast = nums[nums[3]] = nums[2] = 4
Step 2: slow = nums[3] = 2, fast = nums[nums[4]] = nums[2] = 4
Step 3: slow = nums[2] = 4, fast = nums[nums[4]] = nums[2] = 4
slow == fast = 4 (meeting point)

Phase 2:
slow = 0, fast = 4
Step 1: slow = nums[0] = 1, fast = nums[4] = 2
Step 2: slow = nums[1] = 3, fast = nums[2] = 4
Step 3: slow = nums[3] = 2, fast = nums[4] = 2
slow == fast = 2

return 2 ✅
```

## Edge Cases

**Duplicate appears many times:** `nums=[2,2,2,2,2]` → all point to index 2, cycle at node 2. ✅

**Minimum case:** `nums=[1,1]` → slow=1, fast=nums[1]=1. Meet at 1. Phase 2: slow=0, fast=1. slow=nums[0]=1, fast=nums[1]=1. Return 1. ✅

## Complexity

**Time:** Phase 1 and Phase 2 each traverse at most O(n) steps → **O(n)**

**Space:** Two pointers → **O(1)**

> **Time: O(n), Space: O(1)**

---

# Problem 4: Decode Ways

## Approach — Before Coding

**Pattern identified: Memoized Recursion / DP (Fibonacci-like)**

At each position, we have at most two choices:
1. Take one digit (if valid: 1-9)
2. Take two digits (if valid: 10-26)

This is similar to Fibonacci's structure: `dp[i]` depends on `dp[i-1]` and `dp[i-2]`. We can solve with O(1) space using two variables.

## Solution

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0

    n = len(s)
    prev2 = 1  # dp[i-2]: ways to decode empty string
    prev1 = 1  # dp[i-1]: ways to decode first character

    for i in range(1, n):
        current = 0

        # One-digit: s[i] alone
        if s[i] != '0':
            current += prev1

        # Two-digit: s[i-1..i] as a pair
        two_digit = int(s[i - 1:i + 1])
        if 10 <= two_digit <= 26:
            current += prev2

        prev2 = prev1
        prev1 = current

    return prev1
```

## Why '0' Is Special

'0' alone doesn't map to any letter. It can ONLY be valid as part of "10" or "20". If we encounter '0' and the previous digit doesn't form 10 or 20, there are zero decodings.

## Trace — "226"

```
s = "226"
s[0]='2' ≠ '0' → proceed
prev2=1, prev1=1

i=1, s[1]='2':
  One-digit: '2'≠'0' → current += prev1 = 1
  Two-digit: "22" = 22, 10≤22≤26 → current += prev2 = 1
  current = 2. prev2=1, prev1=2.

i=2, s[2]='6':
  One-digit: '6'≠'0' → current += prev1 = 2
  Two-digit: "26" = 26, 10≤26≤26 → current += prev2 = 1
  current = 3. prev2=2, prev1=3.

return 3 ✅ (BZ=2,26 | VF=22,6 | BBF=2,2,6)
```

## Trace — "06"

```
s = "06"
s[0]='0' → return 0 ✅
```

## Edge Cases

**Leading zero:** `s="0"` → return 0 ✅

**Contains "10":** `s="10"` → i=1: s[1]='0', one-digit=0. Two-digit="10"=10 valid, current=1. Return 1 ✅

**Contains "30":** `s="230"` → i=2: s[2]='0', one-digit=0. Two-digit="30"=30>26, invalid. current=0. Return 0 ✅

## Complexity

> **Time: O(n), Space: O(1)**

---

# Problem 5: Subarray Sum Divisible by K

## Approach — Before Coding

**Pattern identified: Prefix Sum + Hash Map with Modular Arithmetic Twist**

This looks like "subarray sum equals k" but asks for divisibility. The twist: if `prefix[j] % k == prefix[i] % k`, then `(prefix[j] - prefix[i]) % k == 0`, meaning the subarray sum from i+1 to j is divisible by k.

So we count prefix sums by their **remainder mod k.** If remainder r has appeared `count` times, any new prefix sum with remainder r can pair with any of those `count` previous occurrences, giving `count` new valid subarrays.

**Mathematical twist for negative numbers:** In Python, `(-1) % 5 = 4` (always non-negative), which is what we want. In some languages, you need `((prefix % k) + k) % k` to handle negatives.

## Solution

```python
def subarrays_div_by_k(nums, k):
    remainder_count = {0: 1}  # empty prefix has remainder 0
    prefix_sum = 0
    count = 0

    for num in nums:
        prefix_sum += num
        remainder = prefix_sum % k

        if remainder in remainder_count:
            count += remainder_count[remainder]

        remainder_count[remainder] = remainder_count.get(remainder, 0) + 1

    return count
```

## Why `{0: 1}` Initialization

If a prefix sum itself is divisible by k (remainder 0), the subarray from index 0 to current position is valid. We need to count it, so we seed remainder 0 with count 1 (the empty prefix).

## Trace

```
nums = [4, 5, 0, -2, -3, 1], k = 5
remainder_count = {0: 1}, prefix_sum = 0, count = 0

num=4: sum=4, rem=4%5=4
       4 not in map → skip
       map = {0:1, 4:1}

num=5: sum=9, rem=9%5=4
       4 in map, count += 1 → count=1
       (subarray [4,5] sum=9, 9%5=4... wait, 9 isn't divisible by 5)
       
Hmm, let me reconsider. rem=4 was seen before at prefix_sum=4. 
Current prefix=9. 9-4=5, which IS divisible by 5. ✅
       map = {0:1, 4:2}

num=0: sum=9, rem=9%5=4
       4 in map(count=2), count += 2 → count=3
       (subarrays: [5,0] sum=5, [4,5,0] sum=9... 
       9-4=5 and 9-0=9. Hmm: prefix at indices mapping:
       prefix sums: 0,4,9,9. rem 4 appeared at prefix 4 and 9.
       New prefix 9 pairs with both.)
       map = {0:1, 4:3}

num=-2: sum=7, rem=7%5=2
        2 not in map → skip
        map = {0:1, 4:3, 2:1}

num=-3: sum=4, rem=4%5=4
        4 in map(count=3), count += 3 → count=6
        map = {0:1, 4:4, 2:1}

num=1: sum=5, rem=5%5=0
       0 in map(count=1), count += 1 → count=7
       map = {0:2, 4:4, 2:1}

return 7 ✅
```

## Edge Cases

**All zeros:** `nums=[0,0], k=5` → sums: 0,0. Both rem=0. count = 1+2 = 3 (subarrays [0], [0], [0,0]) ✅

**Single element divisible:** `nums=[5], k=5` → sum=5, rem=0, 0 in map(1) → count=1 ✅

## Complexity

> **Time: O(n), Space: O(k)** (at most k different remainders)

---

# Problem 6: Minimum Size Subarray Sum

## Approach — Before Coding

**Pattern identified: Sliding Window (Variable Size)**

All values are **positive**, which is the critical property. This means:
- Expanding (moving right) always increases the sum
- Contracting (moving left) always decreases the sum
- Monotonicity enables sliding window

Unlike the earlier "shortest subarray with exact sum" with negatives, positivity guarantees the window behaves predictably.

## Solution

```python
def min_subarray_len(target, nums):
    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(len(nums)):
        current_sum += nums[right]

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0
```

## Trace

```
target = 7, nums = [2, 3, 1, 2, 4, 3]

right=0: sum=2. 2<7.
right=1: sum=5. 5<7.
right=2: sum=6. 6<7.
right=3: sum=8. 8≥7!
  min_len=4. Remove arr[0]=2, sum=6, left=1. 6<7, stop.
right=4: sum=10. 10≥7!
  min_len=min(4,4)=4. Remove arr[1]=3, sum=7, left=2. 7≥7!
  min_len=min(4,3)=3. Remove arr[2]=1, sum=6, left=3. 6<7, stop.
right=5: sum=9. 9≥7!
  min_len=min(3,3)=3. Remove arr[3]=2, sum=7, left=4. 7≥7!
  min_len=min(3,2)=2. Remove arr[4]=4, sum=3, left=5. 3<7, stop.

return 2 ✅ (subarray [4, 3])
```

## Edge Cases

**Single element suffices:** `target=4, nums=[1,4,4]` → right=1: sum=5≥4, min=2. Contract: sum=4≥4, min=1. Return 1 ✅

**Impossible:** `target=100, nums=[1,2,3]` → sum never reaches 100. Return 0 ✅

## Complexity

> **Time: O(n)** (left pointer moves at most n total), **Space: O(1)**

---

# Problem 7: Word Ladder Length

## Approach — Before Coding

**Pattern identified: BFS (Breadth-First Search) on Implicit Graph**

"Shortest transformation sequence" = shortest path in an unweighted graph. Each word is a node. An edge connects two words that differ by exactly one character. BFS finds the shortest path in unweighted graphs.

Why NOT DFS/recursion: DFS finds A path, not the SHORTEST path. BFS guarantees shortest by exploring level by level.

For neighbor generation: instead of comparing all pairs of words (O(n² × L)), for each word try all 26 replacements at each position (O(26 × L)) and check if the result is in the word set.

## Solution

```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)

    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, depth = queue.popleft()

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i + 1:]

                if next_word == end_word:
                    return depth + 1

                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, depth + 1))

    return 0
```

## Trace

```
begin = "hit", end = "cog"
word_set = {"hot","dot","dog","lot","log","cog"}

Queue: [("hit", 1)]

Process "hit" (depth 1):
  Try all 26 chars at each position:
  Position 0: ait, bit, ..., hot ← in word_set! Enqueue ("hot", 2)
  Position 1: hat, hbt, ..., none in set (except "hot" already found)
  Position 2: hia, hib, ..., none new

Queue: [("hot", 2)]
visited = {"hit", "hot"}

Process "hot" (depth 2):
  Position 0: aot, bot, ..., dot ← enqueue ("dot", 3). lot ← enqueue ("lot", 3).
  Position 2: hoa, hob, ..., hog not in set.

Queue: [("dot", 3), ("lot", 3)]
visited = {"hit", "hot", "dot", "lot"}

Process "dot" (depth 3):
  Position 2: doa, dob, ..., dog ← enqueue ("dog", 4).

Process "lot" (depth 3):
  Position 2: loa, ..., log ← enqueue ("log", 4).

Queue: [("dog", 4), ("log", 4)]

Process "dog" (depth 4):
  Position 0: aog, bog, cog ← == end_word! Return 4+1 = 5 ✅
```

## Edge Cases

**End word not in list:** Return 0 immediately ✅

**No path exists:** BFS exhausts all reachable words, queue empties → return 0 ✅

## Complexity

Let n = number of words, L = word length.

**Time:** Each word is dequeued once. For each word, we generate 26×L neighbors and check set membership (O(L) for string hashing). Total: **O(n × L × 26)** = **O(n × L)**

**Space:** word_set O(n×L), visited O(n×L), queue O(n) → **O(n × L)**

> **Time: O(n × L), Space: O(n × L)**

---

# Problem 8: String Interleaving

## Approach — Before Coding

**Pattern identified: Memoized Recursion / 2D DP**

At each point, we've consumed i characters from s1 and j characters from s2. The next character in s3 (at position i+j) must come from either s1[i] or s2[j]. We recurse on both choices and memoize by (i, j).

This is NOT greedy — a greedy approach could match the wrong character and miss a valid interleaving.

## Solution

```python
def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False

    memo = {}

    def dp(i, j):
        if (i, j) in memo:
            return memo[(i, j)]

        k = i + j  # position in s3

        if k == len(s3):
            result = (i == len(s1) and j == len(s2))
            memo[(i, j)] = result
            return result

        result = False

        # Try taking from s1
        if i < len(s1) and s1[i] == s3[k]:
            result = dp(i + 1, j)

        # Try taking from s2 (only if not already found)
        if not result and j < len(s2) and s2[j] == s3[k]:
            result = dp(i, j + 1)

        memo[(i, j)] = result
        return result

    return dp(0, 0)
```

## Trace

```
s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"

dp(0,0): k=0, s3[0]='a'. s1[0]='a' match → dp(1,0)
dp(1,0): k=1, s3[1]='a'. s1[1]='a' match → dp(2,0)
dp(2,0): k=2, s3[2]='d'. s1[2]='b'≠'d'. s2[0]='d' match → dp(2,1)
dp(2,1): k=3, s3[3]='b'. s1[2]='b' match → dp(3,1)
dp(3,1): k=4, s3[4]='b'. s1[3]='c'≠'b'. s2[1]='b' match → dp(3,2)
dp(3,2): k=5, s3[5]='c'. s1[3]='c' match → dp(4,2)
dp(4,2): k=6, s3[6]='b'. s1[4]='c'≠'b'. s2[2]='b' match → dp(4,3)
dp(4,3): k=7, s3[7]='c'. s1[4]='c' match → dp(5,3)
dp(5,3): k=8, s3[8]='a'. i=5=len(s1), skip s1. s2[3]='c'≠'a'. 
         Hmm, both fail → False. Backtrack.

dp(4,3) revisit: s2[3]='c' == 'c' → dp(4,4)
dp(4,4): k=8, s3[8]='a'. s1[4]='c'≠'a'. s2[4]='a' match → dp(4,5)
dp(4,5): k=9, s3[9]='c'. s1[4]='c' match → dp(5,5)
dp(5,5): k=10=len(s3), i=5=len(s1), j=5=len(s2) → True ✅
```

## Edge Cases

**Length mismatch:** `len(s1)+len(s2) != len(s3)` → False immediately ✅

**Empty strings:** `s1="", s2="", s3=""` → True. `s1="", s2="a", s3="a"` → True ✅

## Complexity

**States:** i ranges 0..len(s1), j ranges 0..len(s2). Total: (m+1)×(n+1)

> **Time: O(m × n), Space: O(m × n)** where m=len(s1), n=len(s2)

---

# Problem 9: Next Permutation

## Approach — Before Coding

**Pattern identified: Algorithmic reasoning (no standard pattern)**

The algorithm follows a specific mathematical procedure:

1. **Find the rightmost ascending pair:** Scan right-to-left, find the first index i where `nums[i] < nums[i+1]`. Everything to the right of i is in descending order (already the largest permutation of those elements).

2. **Find the smallest element larger than nums[i]:** Among elements to the right of i (which are in descending order), find the rightmost one that's greater than nums[i]. Swap them.

3. **Reverse the suffix:** The suffix right of i is still in descending order. Reverse it to get the smallest possible suffix.

If no ascending pair exists (step 1 fails), the entire array is descending — it's the last permutation. Reverse the whole array to get the first.

## Solution

```python
def next_permutation(nums):
    n = len(nums)

    # Step 1: Find rightmost ascending pair
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find rightmost element > nums[i]
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Swap
        nums[i], nums[j] = nums[j], nums[i]

    # Step 3: Reverse suffix after position i
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

## Why This Algorithm Works

The next permutation is the **smallest** rearrangement that is **larger** than the current one.

**Step 1** finds the "decision point" — the rightmost place where we can make a different (larger) choice. The suffix after i is already maximized (descending), so we must change position i.

**Step 2** finds the smallest possible upgrade for position i — the smallest value in the suffix that's still larger than nums[i]. Since the suffix is descending, the rightmost greater element is the smallest such value.

**Step 3** minimizes the suffix. After swapping, the suffix is still in descending order (the swap maintains the ordering property). Reversing it makes it ascending — the smallest possible arrangement.

## Trace

```
[1, 3, 2]

Step 1: i=1: nums[1]=3 ≥ nums[2]=2 → continue.
        i=0: nums[0]=1 < nums[1]=3 → found! i=0.

Step 2: j=2: nums[2]=2 > nums[0]=1 → found! j=2.
        Swap: nums[0]↔nums[2] → [2, 3, 1]

Step 3: Reverse suffix [i+1..end] = [1..2]:
        [3, 1] → [1, 3]
        
Result: [2, 1, 3] ✅
```

```
[3, 2, 1]

Step 1: i=1: 2≥1 → continue. i=0: 3≥2 → continue. i=-1.
        No ascending pair found → last permutation.

Step 3: Reverse entire array [0..2]:
        [3, 2, 1] → [1, 2, 3] ✅
```

```
[1, 1, 5]

Step 1: i=1: nums[1]=1 < nums[2]=5 → found! i=1.
Step 2: j=2: nums[2]=5 > nums[1]=1 → swap → [1, 5, 1]
Step 3: Reverse suffix [2..2] → single element, no change.
Result: [1, 5, 1] ✅
```

## Edge Cases

**Already maximum:** `[3,2,1]` → reverse to `[1,2,3]` ✅

**Single element:** `[1]` → i=-1, reverse suffix [0..0] → `[1]` ✅

## Complexity

> **Time: O(n)** (each step scans at most n elements), **Space: O(1)**

---

# Problem 10: Longest Valid Parentheses

## Approach — Before Coding

I'll solve it two ways and compare.

**Approach 1: Stack-based**
Use a stack storing indices. Push a "base" index (-1) initially. For each character:
- `(`: push index
- `)`: pop. If stack becomes empty, push current index as new base. Otherwise, current length = current_index - stack_top.

**Approach 2: Two-pass counter**
Scan left-to-right with open/close counters. When close > open, reset both. When equal, compute length = 2×close. Then scan right-to-left to catch cases where open > close throughout.

I'll implement both, then choose.

## Solution — Approach 1 (Stack)

```python
def longest_valid_parens_stack(s):
    stack = [-1]  # base index
    max_len = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # new base
            else:
                max_len = max(max_len, i - stack[-1])

    return max_len
```

## Solution — Approach 2 (Two-Pass)

```python
def longest_valid_parens_counter(s):
    max_len = 0

    # Left to right
    open_count = close_count = 0
    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        if open_count == close_count:
            max_len = max(max_len, 2 * close_count)
        elif close_count > open_count:
            open_count = close_count = 0

    # Right to left
    open_count = close_count = 0
    for char in reversed(s):
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        if open_count == close_count:
            max_len = max(max_len, 2 * open_count)
        elif open_count > close_count:
            open_count = close_count = 0

    return max_len
```

## Best Approach

**Approach 2 (Two-Pass)** is better: O(n) time and **O(1)** space vs O(n) space for the stack. Same time complexity, strictly better space.

## Why Two Passes Are Needed in Approach 2

Left-to-right alone misses cases like `"(()"` where open > close throughout — we never reach open==close to record a valid length. Right-to-left catches these by treating `)` as the opener and `(` as the closer.

## Trace — Approach 2

```
s = ")()())"

Left to right:
  ')': o=0,c=1. c>o → reset. o=0,c=0.
  '(': o=1,c=0.
  ')': o=1,c=1. Equal! max=2.
  '(': o=2,c=1.
  ')': o=2,c=2. Equal! max=4.
  ')': o=2,c=3. c>o → reset.
  max_len = 4.

Right to left:
  ')': o=0,c=1.
  '(': o=1,c=1. Equal! max=max(4,2)=4.
  ')': o=1,c=2. 
  '(': o=2,c=2. Equal! max=max(4,4)=4.
  ')': o=2,c=3.
  No reset needed, just doesn't update.
  
return 4 ✅
```

## Edge Cases

**Empty string:** `s=""` → loops don't run → 0 ✅

**All open:** `s="((("` → left pass: never equal. Right pass: o>c resets each time → 0 ✅

## Complexity (Approach 2)

> **Time: O(n), Space: O(1)**

---

# Problem 11: Count of Range Sum

## Approach — Before Coding

**Pattern identified: Modified Merge Sort on Prefix Sums (Divide and Conquer)**

Brute force counts all O(n²) range sums. We need O(n log n).

**Key insight:** Range sum S(i,j) = prefix[j+1] - prefix[i]. We need to count pairs (i,j) where i < j and `lower ≤ prefix[j] - prefix[i] ≤ upper`.

This is "count pairs satisfying a condition" — exactly what modified merge sort does (like counting inversions). During the merge step, for each element in the right half, count how many elements in the left half satisfy the range condition. Since both halves are sorted, this counting can be done with two pointers in O(n) per merge level.

## Solution

```python
def count_range_sum(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    def merge_count(arr, left, right):
        if right - left <= 1:
            return 0

        mid = (left + right) // 2
        count = merge_count(arr, left, mid) + merge_count(arr, mid, right)

        # Count cross-pairs: for each j in right half, count i in left half
        # where lower ≤ arr[j] - arr[i] ≤ upper
        # i.e., arr[j] - upper ≤ arr[i] ≤ arr[j] - lower
        lo = hi = left
        for j in range(mid, right):
            while lo < mid and arr[lo] < arr[j] - upper:
                lo += 1
            while hi < mid and arr[hi] <= arr[j] - lower:
                hi += 1
            count += hi - lo

        # Standard merge sort
        arr[left:right] = sorted(arr[left:right])

        return count

    return merge_count(prefix, 0, len(prefix))
```

## Why Two Pointers Work During Merge

The left half is sorted. For each `arr[j]` in the right half:
- `lo` finds the leftmost position where `arr[lo] >= arr[j] - upper`
- `hi` finds the leftmost position where `arr[hi] > arr[j] - lower`
- Elements in `[lo, hi)` satisfy the range condition
- Count = hi - lo

As j increases (right half is sorted), `arr[j]` increases, so both `arr[j] - upper` and `arr[j] - lower` increase, meaning lo and hi only move forward → O(n) total per merge level.

## Trace

```
nums = [-2, 5, -1], lower = -2, upper = 2
prefix = [0, -2, 3, 2]

merge_count([0, -2, 3, 2], 0, 4)
├─ merge_count([0, -2, 3, 2], 0, 2):  left=[0,-2]
│  ├─ merge_count(0, 1): single → 0
│  ├─ merge_count(1, 2): single → 0
│  └─ Count: for j=1 (val=-2):
│       lo: arr[lo] >= -2-2=-4. lo=0 (0≥-4).
│       hi: arr[hi] > -2-(-2)=0. arr[0]=0, 0>0? No. hi=0.
│       Wait, hi should find first > arr[j]-lower = -2-(-2) = 0.
│       arr[0]=0. 0 > 0? No. hi stays 0. count += 0-0 = 0.
│     Merge sort: [-2, 0]
│     return 0
│
├─ merge_count([0, -2, 3, 2], 2, 4): right=[3,2]
│  ├─ Count: for j=3 (val=2):
│       arr[2]=3. 3 >= 2-2=0? Yes. lo=2.
│       3 > 2-(-2)=4? No. hi=2. count += 0.
│     Merge sort: [2, 3]
│     return 0
│
└─ Count cross-pairs: left=[-2,0], right=[2,3]
   For j in [2,3] (values 2, 3):
     j=2, val=2: lo: find arr[i] >= 2-2=0. arr[0]=-2 < 0, arr[1]=0 >= 0. lo=1.
                  hi: find arr[i] > 2-(-2)=4. arr[0]=-2 ≤ 4, arr[1]=0 ≤ 4. hi=2.
                  count += 2-1 = 1. (prefix pair: prefix[i]=0, S=2-0=2 ✓)
     j=3, val=3: lo: find >= 3-2=1. arr[1]=0 < 1. lo=2.
                  hi: find > 3+2=5. hi=2.
                  count += 2-2 = 0.
   
   Total cross = 1.

Hmm, expected 3. Let me reconsider — I think I need to recount.

Actually, the valid range sums are:
S(0,0) = -2 ✓ (in [-2,2])
S(2,2) = -1 ✓ (in [-2,2])
S(0,2) = -2+5-1 = 2 ✓ (in [-2,2])

These correspond to prefix pairs:
prefix[1]-prefix[0] = -2-0 = -2 ✓
prefix[3]-prefix[2] = 2-3 = -1 ✓
prefix[3]-prefix[0] = 2-0 = 2 ✓

Let me redo with correct merge sort behavior.

The issue is my simplified `sorted()` doesn't track properly. Let me re-examine:

After left recursion: arr becomes [0, -2, 3, 2] → left portion sorted to [-2, 0]
After right recursion: right portion sorted to [2, 3]
Now: arr = [-2, 0, 2, 3]

Cross-pairs: left half [-2, 0], right half [2, 3]:
  j indexes right half values:
  val=2: lo finds first ≥ 2-2=0 in [-2,0] → index 1 (val=0). 
         hi finds first > 2+2=4 in [-2,0] → index 2 (past end).
         count += 2-1 = 1. (pair: prefix=0, 2-0=2 ✓)
  
  val=3: lo finds first ≥ 3-2=1 in [-2,0] → index 2 (none ≥1).
         hi = 2.
         count += 2-2 = 0.

Cross count = 1. Plus left recursion found S(0,0)=-2 and right found S(2,2)=-1.

Wait — I got 0 from both sub-recursions. Let me redo left recursion more carefully.

Left sub: merge_count on prefix [0, -2] (indices 0,1):
  Left: [0], Right: [-2]
  Cross: for val=-2: lo finds ≥ -2-2=-4 in [0] → lo=0. 
         hi finds > -2+2=0 in [0] → 0>0? No. hi=0.
         count += 0. 
  Sorted: [-2, 0].

Hmm that gives 0, but we need to count prefix[1]-prefix[0] = -2-0 = -2 which is in range.
The issue: the cross-pair check looks at j in right half and i in left half. Here left=[0], right=[-2]. For j=right, val=-2:
  Need: -2 ≤ -2 - arr[i] ≤ 2, so -2 ≤ -2-0 ≤ 2 → -2 ≤ -2 ✓ and -2 ≤ 2 ✓.
  Equivalently: arr[i] ≥ -2-2=-4 and arr[i] ≤ -2+2=0. arr[0]=0: 0≥-4 ✓ and 0≤0 ✓.
  lo=0 (first ≥ -4), hi should be first > 0: arr[0]=0, 0>0? No. hi=0.
  
The bug: hi condition should be `arr[hi] <= arr[j] - lower` not strict >.

Let me re-examine: we want `lower ≤ arr[j] - arr[i] ≤ upper`, i.e., `arr[j]-upper ≤ arr[i] ≤ arr[j]-lower`.

So elements in range [arr[j]-upper, arr[j]-lower].
lo = first index where arr[lo] >= arr[j]-upper
hi = first index where arr[hi] > arr[j]-lower

For val=-2, lower=-2, upper=2:
  Range for arr[i]: [-2-2, -2-(-2)] = [-4, 0]
  lo: first ≥ -4 → index 0
  hi: first > 0 → index 1 (past end of left half which has 1 element)
  count += 1-0 = 1! ✓
```

I had the hi loop condition wrong in my trace. Let me redo with the correct code:

```
while hi < mid and arr[hi] <= arr[j] - lower:
    hi += 1
```

`arr[j]-lower = -2-(-2) = 0`. `arr[0]=0, 0<=0` → True, hi=1. Then hi=1 = mid, stop.
count += 1-0 = 1. ✅

Now the full count: left sub returns 1, right sub returns 1, cross returns 1. Total = 3. ✅

## Edge Cases

**Single element:** `nums=[0], lower=0, upper=0` → prefix=[0,0]. One pair: prefix[1]-prefix[0]=0, in [0,0] → 1 ✅

**Empty array:** `nums=[]` → prefix=[0]. No pairs → 0 ✅

## Complexity

Same structure as merge sort: O(n) work per level, O(log n) levels.

> **Time: O(n log n), Space: O(n)**

---

# Problem 12: Alien Dictionary

## Approach — Before Coding

**This combines multiple techniques:**

1. **Comparison of adjacent words** → extract ordering constraints (edges in a directed graph)
2. **Directed graph** → represent character ordering relationships
3. **Topological sort** → determine a valid global ordering
4. **Cycle detection** → if the graph has a cycle, the ordering is invalid

The key insight: comparing adjacent words in the sorted list gives us ONE ordering constraint per pair (the first position where the words differ).

## Solution

```python
from collections import deque, defaultdict

def alien_order(words):
    # Step 1: Initialize graph with all unique characters
    graph = {}
    in_degree = {}
    for word in words:
        for char in word:
            if char not in graph:
                graph[char] = set()
                in_degree[char] = 0

    # Step 2: Extract ordering constraints from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))

        # CRITICAL CHECK: if w1 is a prefix of w2 but longer, invalid
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""

        for j in range(min_len):
            if w1[j] != w2[j]:
                # w1[j] comes before w2[j] in alien alphabet
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break  # only the FIRST difference matters

    # Step 3: Topological sort (Kahn's algorithm / BFS)
    queue = deque()
    for char in in_degree:
        if in_degree[char] == 0:
            queue.append(char)

    result = []
    while queue:
        char = queue.popleft()
        result.append(char)

        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 4: Cycle detection — if not all chars are in result, cycle exists
    if len(result) != len(graph):
        return ""

    return "".join(result)
```

## Why Only the First Difference Matters

In a sorted dictionary, two adjacent words share a common prefix. The FIRST position where they differ tells us the relative order of those two characters. Characters after the first difference could be in any order — the words' relative position is already determined by that first differing character.

## Why `len(w1) > len(w2)` With Same Prefix Is Invalid

In any valid dictionary, "app" comes before "apple" (prefix comes first). If we see "apple" before "app", the ordering contradicts this universal rule → invalid.

## Trace

```
words = ["wrt", "wrf", "er", "ett", "rftt"]

Step 1: All chars: {w, r, t, f, e}

Step 2: Compare adjacent pairs:
  "wrt" vs "wrf": first diff at index 2: t vs f → t before f
  "wrf" vs "er":  first diff at index 0: w vs e → w before e
  "er" vs "ett":  first diff at index 1: r vs t → r before t
  "ett" vs "rftt": first diff at index 0: e vs r → e before r

  Edges: t→f, w→e, r→t, e→r
  
  graph: {w: {e}, r: {t}, t: {f}, f: {}, e: {r}}
  in_degree: {w:0, r:1, t:1, f:1, e:1}

Step 3: BFS topological sort:
  Queue: [w] (only w has in_degree 0)
  
  Process w: result=[w]. Neighbor e: in_degree[e]=0 → queue=[e]
  Process e: result=[w,e]. Neighbor r: in_degree[r]=0 → queue=[r]
  Process r: result=[w,e,r]. Neighbor t: in_degree[t]=0 → queue=[t]
  Process t: result=[w,e,r,t]. Neighbor f: in_degree[f]=0 → queue=[f]
  Process f: result=[w,e,r,t,f]. No neighbors.

Step 4: len(result)=5 == len(graph)=5. No cycle.

return "wertf" ✅
```

## Trace — Invalid Case

```
words = ["z", "x", "z"]

Compare "z" vs "x": z before x → edge z→x
Compare "x" vs "z": x before z → edge x→z

graph: {z: {x}, x: {z}}
in_degree: {z:1, x:1}

BFS: no node has in_degree 0! Queue starts empty.
result = []. len(result)=0 ≠ len(graph)=2.

return "" ✅ (cycle detected — contradictory ordering)
```

## Edge Cases

**Single word:** `words=["abc"]` → no pairs to compare. All characters valid, order is any permutation. The algorithm returns them in whatever order they have in_degree=0. ✅

**Prefix violation:** `words=["abc", "ab"]` → "abc" > "ab" but "abc" comes first with same prefix → return "" ✅

## Complexity

Let C = total characters across all words, V = unique characters, E = number of edges extracted.

**Step 1:** O(C) to scan all characters.

**Step 2:** O(C) — we compare adjacent pairs, scanning characters until first difference. Total characters scanned across all comparisons ≤ C.

**Step 3:** O(V + E) — standard BFS topological sort.

E ≤ number of word pairs = len(words)-1. V ≤ 26.

> **Time: O(C), Space: O(V + E)** = **O(1)** for bounded alphabet, **O(C)** overall including input processing