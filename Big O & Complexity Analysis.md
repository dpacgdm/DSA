# PHASE 1 — THE FOUNDATION
## Week 1, Day 1: Big O & Complexity Analysis

---

## Why This First? Why Not Arrays or Coding?

Because **every single decision** you make in DSA — which data structure to pick, which algorithm to use, whether your solution is garbage or genius — comes down to ONE question:

> **"How does this perform as the input grows?"**

If you don't understand complexity analysis, you're a chef who can't taste. You'll write code and have **zero idea** if it's good. Every FAANG interviewer will ask: *"What's the time and space complexity?"* If you stumble, interview over.

This is the lens through which you will see **everything** from today forward.

---

## The Core Problem That Created Big O

Imagine I give you a list of 10 names and say *"Find John."*

Easy. You scan through. Takes a second.

Now I give you **10 billion names.**

Suddenly, *how* you search matters. The difference between a good approach and a bad one is the difference between **1 second and 300 years.**

Computer scientists needed a language to **describe** how algorithms behave as input grows. Not exact time — because that depends on your machine. They needed something **machine-independent** and **universal.**

That language is **Big O Notation.**

---

## What Big O Actually Means

Big O describes the **upper bound** of growth. It answers:

> "In the **worst case**, how does the number of operations grow relative to input size *n*?"

It does NOT tell you:
- Exact time in seconds
- How fast your computer is
- What happens with small inputs

It DOES tell you:
- **The shape of growth** as n gets massive

Think of it like this. I don't care if your car goes 60mph or 62mph. I care whether you're in a **car, a bicycle, or a rocket.** Big O tells you which vehicle you're in.

---

## The Big O Family — From Best to Worst

Let me introduce you to the family. Burn this order into your skull.

```
O(1)        — Constant        🟢 The dream
O(log n)    — Logarithmic     🟢 Excellent  
O(n)        — Linear          🟡 Acceptable
O(n log n)  — Linearithmic    🟡 Common for sorting
O(n²)       — Quadratic       🟠 Getting dangerous
O(n³)       — Cubic           🔴 Pain
O(2ⁿ)       — Exponential     🔴 Agony
O(n!)       — Factorial       💀 Death
```

Let's make these **real.**

---

### O(1) — Constant Time

```python
def get_first(arr):
    return arr[0]
```

Doesn't matter if the array has 10 elements or 10 billion. You grab the first one. **One operation.** Input size is irrelevant.

---

### O(n) — Linear Time

```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

You must look at **every element once.** 10 elements = ~10 operations. 1 million elements = ~1 million operations. Growth is **proportional** to input.

---

### O(n²) — Quadratic Time

```python
def print_pairs(arr):
    for i in arr:
        for j in arr:
            print(i, j)
```

A loop **inside** a loop. Each element pairs with every other element.

- n = 10 → 100 operations
- n = 1,000 → 1,000,000 operations
- n = 100,000 → 10,000,000,000 operations 💀

**This is where bad solutions live.**

---

### O(log n) — Logarithmic Time

This one is critical and most beginners get confused here.

Think of a **phone book** with 1,000 pages. You're looking for "Smith."

Do you start at page 1? No. You open the **middle.** You see "M." Smith is after M, so you **throw away the entire left half.** Now you have 500 pages. Open the middle again. Repeat.

```
1000 → 500 → 250 → 125 → 63 → 32 → 16 → 8 → 4 → 2 → 1
```

That's roughly **10 steps** to search 1,000 items. For 1,000,000 items? Only about **20 steps.**

You're cutting the problem **in half** each time. That's the signature of O(log n). This is **binary search** — we'll master it soon.

---

## The Rules of Big O

### Rule 1: Drop the Constants

O(2n) → **O(n)**
O(500) → **O(1)**
O(n/2) → **O(n)**

Why? Because when n is 10 billion, the constant is irrelevant. The **shape** of growth is what matters.

### Rule 2: Drop Non-Dominant Terms

O(n² + n) → **O(n²)**
O(n + log n) → **O(n)**

The biggest term **eats** the smaller ones at scale. When n = 1 million, n² = 1,000,000,000,000. The extra n = 1,000,000 is a rounding error.

### Rule 3: Different Inputs = Different Variables

```python
def compare(arr1, arr2):
    for i in arr1:       # O(a)
        for j in arr2:   # O(b)
            print(i, j)
```

This is **O(a × b)**, NOT O(n²). They're different arrays. Different sizes. **FAANG interviewers test this specifically.**

---

## Space Complexity — The Forgotten Twin

Time complexity measures operations. **Space complexity** measures **memory.**

```python
def create_copy(arr):
    new_arr = []
    for num in arr:
        new_arr.append(num)
    return new_arr
```

- Time: O(n)
- Space: O(n) — you created a whole new array

```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

- Time: O(n)
- Space: O(1) — you only used one extra variable regardless of input size

**At FAANG, they want both.** "Can you do it in O(1) space?" is a question you'll hear constantly.

---

## A Real Example: Why This Matters

**Problem:** Find if an array has any duplicates.

### Approach 1 — Brute Force
```python
def has_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```
- Time: **O(n²)**
- Space: **O(1)**

### Approach 2 — Hash Set
```python
def has_duplicate(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```
- Time: **O(n)**
- Space: **O(n)**

See the **tradeoff?** Approach 2 is astronomically faster but uses more memory. This is the eternal tension in DSA: **time vs space.** 

For n = 100,000:
- Approach 1: up to **5 billion** comparisons
- Approach 2: up to **100,000** operations

Same problem. Same correct answer. One gets you **hired.** One gets you **rejected.**

---

## Stop. 

That's the teaching for today. Before tomorrow, I need to know you **own** this.

I have **7 questions** for you. Answer every single one. No Googling. No looking up. Wrong answers mean we revisit this tomorrow instead of moving forward.

---

### Question 1
What is the time complexity of this code?
```python
def mystery(n):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                print(i, j, k)
```

### Question 2
What is the time complexity?
```python
def mystery2(arr):
    total = 0
    total += arr[0]
    total += arr[len(arr) - 1]
    return total
```

### Question 3
Simplify: O(3n² + 7n + 1000). What's the final Big O?

### Question 4
```python
def func(arr1, arr2):
    for x in arr1:
        print(x)
    for y in arr2:
        print(y)
```
Is this O(2n)? If not, what is it and **why?**

### Question 5
What's the **space** complexity of this?
```python
def build(n):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result
```

### Question 6
In your own words — **why do we drop constants** in Big O? Don't give me a textbook answer. Explain it like you're convincing a skeptic.

### Question 7
I have two solutions to the same problem. Solution A is O(n log n) time, O(1) space. Solution B is O(n) time, O(n) space. Which one is "better" and **why is that a trick question?**

---

