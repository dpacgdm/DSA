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
