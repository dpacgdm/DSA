# BIT MANIPULATION — THE COMPLETE LESSON

**Module:** Coverage gap — Bitwise (standalone deep dive)  
**Status:** `content-delivered` — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Integers, loops, basic arrays.  
**Cross-refs:** Subsets via bits ↔ Backtracking; bit DP preview ↔ DP II; Arrays Part 8 was a bolt-on — **this file is the canonical deep lesson**.

---

# PART 1: WHY BITWISE EXISTS

## The Problem Bits Solve

Every integer is a bag of independent **yes/no flags** (bits). Bitwise ops let you:

| Need | Bitwise move |
|---|---|
| Toggle / test flags | mask AND/OR/XOR |
| Pack multiple booleans | one int as bitset |
| Find unique / missing via cancel | XOR |
| Enumerate all subsets of n≤20 | iterate `0..(1<<n)-1` |
| Clear lowest set bit | `n & (n-1)` |
| Fast power-of-two tests | `n & (n-1) == 0` |

**Interview reason:** some problems are *awkward* with arrays/hashmaps but *trivial* once you see the bit identity. Others are overkill — knowing **when not to** is part of mastery.

### Real-World Intuition

Think of a light panel with 32 switches. Each switch is a bit. AND = "which lights are on in both panels?", OR = "lights on in either", XOR = "lights that differ", shifts = "slide the whole panel left/right."

---

# PART 2: BINARY FUNDAMENTALS

## 2A: Place Values

```
Decimal 13 = 1101₂

  8  4  2  1
  1  1  0  1   → 8+4+0+1 = 13
```

**Bit index:** bit 0 = least significant (rightmost), value `2^0`.

```python
# Python: bin(), bit_length()
bin(13)        # '0b1101'
(13).bit_length()  # 4
```

## 2B: Signed Integers (Interview Awareness)

Python ints are arbitrary precision (no fixed 32-bit overflow). LeetCode "32-bit signed" problems still ask you to **simulate** 32-bit two's complement (e.g. Reverse Bits, Sum of Two Integers constraints).

**Two's complement (n-bit):** negative `-x` stored as `2^n - x`.  
MSB = sign bit in fixed width.

**For interviews in Python:** mask with `0xFFFFFFFF` when simulating 32-bit; handle sign with `if n & (1<<31): n -= 1<<32`.

## 2C: Powers of Two Table (Memorize Common)

| Bits | Value |
|---|---|
| `1<<0` | 1 |
| `1<<1` | 2 |
| `1<<3` | 8 |
| `1<<10` | 1024 |
| `1<<20` | ~1e6 |
| `1<<30` | ~1e9 |
| `1<<63` | huge (careful in fixed 64-bit langs) |

---

# PART 3: THE SIX OPERATORS

## 3A: AND `&` — Keep Bits Set in BOTH

```
  1101   (13)
& 1011   (11)
= 1001   (9)
```

**Uses:** clear bits, extract flags, check if bit i set: `n & (1<<i)`.

## 3B: OR `|` — Set Bits That Are in EITHER

```
  1101
| 1011
= 1111
```

**Uses:** set bit i: `n | (1<<i)`.

## 3C: XOR `^` — Differ Bits (Add Mod 2)

```
  1101
^ 1011
= 0110
```

**Critical properties (memorize):**
1. `a ^ a = 0`
2. `a ^ 0 = a`
3. Commutative & associative
4. `a ^ b ^ a = b` (cancel pairs)

**Uses:** find unique number, swap without temp, toggle bit: `n ^ (1<<i)`.

## 3D: NOT `~` — Flip All Bits

In Python, `~x = -x-1` (infinite sign-extension of two's complement).  
**TRAP:** rarely use bare `~` for interview bitmasks; prefer XOR with mask of ones.

```python
~5        # -6
(~5) & 0b1111  # 10 = 0b1010  (4-bit flip of 0101)
```

## 3E: Left Shift `<<` — Multiply by 2^k

`n << k` = `n * (2**k)` (within range).  
`1 << i` = bit i mask.

## 3F: Right Shift `>>` — Divide by 2^k (floor toward -∞ in Python)

`n >> k` = `n // (2**k)` for non-negative n.  
**Arithmetic vs logical:** Python `>>` is arithmetic on ints; for 32-bit logical shift, mask first.

---

# PART 4: BIT MASKING PRIMITIVES (DRILL COLD)

```python
def check_bit(n, i):
    return (n & (1 << i)) != 0

def set_bit(n, i):
    return n | (1 << i)

def clear_bit(n, i):
    return n & ~(1 << i)

def toggle_bit(n, i):
    return n ^ (1 << i)

def clear_lowest_set(n):
    """Turn off the rightmost 1 bit."""
    return n & (n - 1)

def lowest_set_bit(n):
    """Isolate rightmost 1 bit (value, not index)."""
    return n & -n  # two's complement trick; works in Python

def bit_count(n):
    return n.bit_count()  # Py 3.10+; else bin(n).count('1')
```

### Trace — clear lowest set

```
n = 12 = 1100
n-1 = 11 = 1011
n & (n-1) = 1000 = 8
```

Each call removes one set bit → loop counts bits in O(popcount) iterations.

---

# PART 5: XOR TRICKS FAMILY

## 5A: Single Number (all appear twice except one)

```python
def single_number(nums):
    x = 0
    for n in nums:
        x ^= n
    return x
```

**Why:** pairs cancel to 0; leftover is the unique.

**Trace:** `[4,1,2,1,2]` → `0^4^1^2^1^2 = 4`

## 5B: Missing Number (0..n with one missing)

```python
def missing_number(nums):
    x = 0
    for i, n in enumerate(nums):
        x ^= i ^ n
    x ^= len(nums)
    return x
```

Or XOR all indices `0..n` with all values.

## 5C: Single Number II (all appear 3 times except one)

Bit-count mod 3 per bit, or state machine with two bitmasks. Interview-friendly:

```python
def single_number_ii(nums):
    ones = twos = 0
    for n in nums:
        ones = (ones ^ n) & ~twos
        twos = (twos ^ n) & ~ones
    return ones
```

**Intuition:** `ones`/`twos` track bits seen mod 3.

## 5D: Two Single Numbers (all twice except two uniques)

1. XOR all → `x = a ^ b` (nonzero).
2. Find any set bit in `x` (differs between a and b): `mask = x & -x`.
3. Partition nums by that bit; XOR each partition → a and b.

```python
def single_number_iii(nums):
    x = 0
    for n in nums:
        x ^= n
    mask = x & -x
    a = b = 0
    for n in nums:
        if n & mask:
            a ^= n
        else:
            b ^= n
    return [a, b]
```

## 5E: Swap Without Temp

```python
a ^= b
b ^= a
a ^= b
```

Prefer tuple swap in Python: `a, b = b, a`. Know XOR swap for interviews in other languages.

---

# PART 6: n & (n-1) AND POWER OF TWO

## 6A: Power of Two

`n > 0` and exactly one bit set:

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

**Trace:** `8=1000`, `7=0111`, `8&7=0`. `6=110`, `5=101`, `6&5=100 ≠ 0`.

## 6B: Count Set Bits (Brian Kernighan)

```python
def hamming_weight(n):
    c = 0
    while n:
        n &= n - 1
        c += 1
    return c
```

## 6C: Counting Bits 0..n (DP)

```python
def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i & (i - 1)] + 1
    return ans
```

**Why:** `i & (i-1)` is i with lowest set bit cleared → popcount = that + 1.

---

# PART 7: SUBSETS VIA BITMASKS

For `n ≤ 20` (sometimes 20–24), enumerate all `2^n` subsets:

```python
def subsets(nums):
    n = len(nums)
    res = []
    for mask in range(1 << n):
        cur = []
        for i in range(n):
            if mask & (1 << i):
                cur.append(nums[i])
        res.append(cur)
    return res
```

**Trace:** `nums=[1,2]`, masks 0..3:
```
00 → []
01 → [1]
10 → [2]
11 → [1,2]
```

**When vs backtracking:** bitmasks are great for small n + need all masks as integers (bit DP). Backtracking is clearer for pruning / variable-length construction.

---

# PART 8: REVERSE BITS / RANGE BITWISE

## 8A: Reverse Bits (32-bit)

```python
def reverse_bits(n):
    ans = 0
    for _ in range(32):
        ans = (ans << 1) | (n & 1)
        n >>= 1
    return ans
```

**Trace (4-bit toy):** `n=13=1101` → reverse `1011=11`.

## 8B: Bitwise AND of Range [m, n]

Naive loop TLE. Insight: AND clears bits that flip anywhere in range → result is common prefix of m and n.

```python
def range_bitwise_and(m, n):
    shift = 0
    while m < n:
        m >>= 1
        n >>= 1
        shift += 1
    return m << shift
```

---

# PART 9: WHEN BITWISE IS RIGHT VS OVERKILL

| Signal | Prefer bitwise | Prefer something else |
|---|---|---|
| Unique via cancel / pairs | XOR | Hash map also works (extra space) |
| Flags / permissions | Bitmask | Set of strings if sparse & huge |
| All subsets n≤20 | Bitmask enum / bit DP | Backtracking if pruning heavy |
| Power of two / popcount | `n&(n-1)` | Math log (float risk) |
| General arithmetic | — | Normal `+ - * //` |
| Readability-critical code | — | Don't force bits |

**Rule:** If a hashmap O(n) space solution is clear and constraints allow, bits are optional flair. If problem says O(1) space or "without extra memory," XOR / in-place bits shine.

---

# PART 10: CHEAT SHEETS

## Operator Truth (1-bit)

| a | b | AND | OR | XOR |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

## Idioms

```
check i:     n & (1<<i)
set i:       n | (1<<i)
clear i:     n & ~(1<<i)
toggle i:    n ^ (1<<i)
clear low1:  n & (n-1)
low1 value:  n & -n
power2?:     n>0 and n&(n-1)==0
popcount:    loop n&=n-1 / bit_count()
```

## XOR Identities

```
x^x=0  x^0=x  commutative/associative  cancel pairs
```

---

# PART 11: TRAPS

| Trap | Fix |
|---|---|
| `~` in Python surprises | Mask width explicitly |
| Shift into sign / huge | Stay within problem width |
| `1<<i` when i≥31 in fixed langs | Use `1<<i` carefully / unsigned |
| Forgetting `n>0` in power-of-two | Reject 0 and negatives |
| Using bits for n=40 subsets | 2^40 impossible — wrong tool |
| Assuming 32-bit overflow in Python | Simulate with masks if required |

---

# PART 12: WORKED PROBLEMS

## WP1 — Number of 1 Bits
`n=11=1011` → Kernighan: 1011→1010→1000→0 → count 3.

## WP2 — Single Number
`[2,2,1]` → `0^2^2^1=1`.

## WP3 — Missing Number
`nums=[3,0,1]`, n=3 → XOR `0^1^2^3 ^ 3^0^1 = 2`.

## WP4 — Power of Two
`16` → True; `18` → False; `0` → False.

## WP5 — Subsets bitmask
`[1,2,3]` → 8 subsets (list them via masks 0..7).

## WP6 — Counting Bits
`n=5` → `[0,1,1,2,1,2]` via `ans[i]=ans[i&(i-1)]+1`.

## WP7 — Reverse Bits (8-bit toy)
`n=0b00000001` → `0b10000000`.

## WP8 — Single Number III
`[1,2,1,3,2,5]` → XOR all = `3^5=6=0110`, mask=`0010`, partition → `{3}` and `{5}`.

## WP9 — Get Sum without + (bonus)
XOR = sum without carry; AND<<1 = carry; repeat until carry 0. (Python infinite ints — mask to 32-bit for LC.)

## WP10 — Hamming Distance
`x^y` then popcount.

---

# PART 13: INTERVIEW SCRIPT

1. Restate: flags / unique / subsets / popcount?
2. Name the identity (`XOR cancel`, `n&(n-1)`, mask enum).
3. Complexity: usually O(n) or O(2^n · n) for subsets.
4. Mention Python int unlimited vs simulated 32-bit if relevant.
5. Dry-run on a 4-bit example out loud.

---

**Status note (interim):** Core above; deep expansions in Parts 14+.

---

# PART 14: DEEP DIVE — TWO'S COMPLEMENT & FIXED WIDTH

## 14A: Why Interviews Still Care
Python ints are unbounded, but LC problems say "32-bit signed." You must **simulate** width:

```python
MASK32 = 0xFFFFFFFF
SIGN = 1 << 31

def to_signed32(n):
    n &= MASK32
    return n - (1 << 32) if n & SIGN else n
```

## 14B: Arithmetic Right Shift vs Logical
Logical: fill with 0. Arithmetic: fill with sign bit.  
Python `>>` on ints behaves like infinite sign extension. For logical 32-bit: `(n & MASK32) >> k`.

## 14C: Trace — negative in 8-bit
`-5` in 8-bit two's complement: `256-5=251=11111011₂`.

---

# PART 15: BIT DP PREVIEW (WHEN MASKS MEET DP)

For `n ≤ 20`, `dp[mask]` = best answer using the subset `mask`.

```python
# Traveling salesman style skeleton (exposure)
n = len(cities)
N = 1 << n
dp = [[inf]*n for _ in range(N)]
dp[1][0] = 0  # start at 0
for mask in range(N):
    for u in range(n):
        if not (mask & (1 << u)):
            continue
        for v in range(n):
            if mask & (1 << v):
                continue
            dp[mask|(1<<v)][v] = min(dp[mask|(1<<v)][v], dp[mask][u] + dist[u][v])
```

**Bridge:** Subsets via bits (Part 7) is the enumeration engine; bit DP memoizes over masks. Full TSP deferred to DP II / CP.

---

# PART 16: MORE XOR / MASK WORKED PROBLEMS

## WP11 — Find the Duplicate Number (bit / Floyd note)
Bit count approach: for each bit, count in `1..n` vs in array; excess bits reconstruct duplicate. Floyd cycle is the usual O(1) space solution — bits are alternate.

## WP12 — Subsets with sum (meet in middle light)
`n=40` → split into 20+20; enumerate masks each half; sort/hash — bits enable 2^20.

## WP13 — Maximum XOR of two numbers in array
Trie of bits (see Advanced Tries) or sort+greedy bit. Standalone: for each num, try to maximize XOR with a previous num via bit trie.

## WP14 — Decode XORed array
`encoded[i] = a[i] XOR a[i+1]`; given `a[0]`, recover: `a[i+1]=a[i]^encoded[i]`.

## WP15 — Sum of Two Integers (full 32-bit)

```python
def get_sum(a, b):
    MASK = 0xFFFFFFFF
    while b & MASK:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return to_signed32(a) if b > MASK else a
```

## WP16 — Bitwise AND of numbers range
`m=5,n=7` → `101 & 110 & 111 = 100` = 4. Common prefix method: shift until equal.

## WP17 — Total Hamming Distance
For each bit 0..31, count zeros and ones; contribution = `zeros * ones`.

## WP18 — UTF-8 validation (bit patterns)
Check leading ones of first byte; subsequent bytes must be `10xxxxxx`.

---

# PART 17: OPERATOR DECISION TREE

```
Need unique / cancel pairs?     → XOR
Need flags / set membership n≤64? → bitmask int
Need all subsets n≤20?          → for mask in 1<<n
Need popcount / power2?         → n&(n-1)
Need reverse / extract fields?  → shifts + masks
Need general math?              → don't force bits
```

---

# PART 18: PYTHON BIT TOOLBOX

```python
n.bit_count()       # popcount 3.10+
n.bit_length()      # floor(log2(n))+1 for n>0
bin(n), hex(n), oct(n)
int('1011', 2)
(n >> i) & 1        # alternate check
```

---

# PART 19: TRAPS EXPANDED

| Trap | Example | Fix |
|---|---|---|
| `~0` is `-1` | mask building | `~x & ((1<<k)-1)` |
| Shift count ≥ width | UB in C | Mask shift or check |
| Enumerate 1<<40 | TLE/MLE | Meet in middle / different algo |
| Sign bit in reverse | LC Reverse Bits | Loop exactly 32 |
| Using float log for power2 | `log2(8)=3` ok; `log2(9)` | Prefer `n&(n-1)` |

---

# PART 20: 25-MINUTE DRILL

1. Write check/set/clear/toggle/lowbit from memory.  
2. Single Number I–III on paper.  
3. countBits DP for n=16.  
4. Subsets of `[a,b,c]` via masks.  
5. Explain when NOT to use bits (60s).

---

**End of Bitwise lesson.** Status: `content-delivered`.

---

# PART 21: BIT MASKING WORKED LAB

## Lab 1 — Manual bit board
Start `n=0`. Set bits 1,3,5. Clear bit 3. Toggle bit 7. Check bit 5.  
Expected path: `0 → 2 → 10 → 42 → 34 → 162 → bit5 true`.

## Lab 2 — Count bits two ways
`n=29=11101`: Kernighan count 4; `bin(29).count('1')` = 4.

## Lab 3 — Isolate lowest
`n=40=101000`, `n&-n=8=001000`.

## Lab 4 — Submasks iteration
```python
def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask
```
Trace mask=`0b1011` submasks.

---

# PART 22: SINGLE NUMBER FAMILY — UNIFIED VIEW

| Variant | Appearances | Tool |
|---|---|---|
| I | all 2× except 1× | XOR all |
| II | all 3× except 1× | ones/twos or bit mod 3 |
| III | all 2× except two 1× | XOR + partition by bit |
| Missing | 0..n one missing | XOR indices+vals |
| Duplicate | 1..n one dup | bits / Floyd |

---

# PART 23: SHIFT MULTIPLY/DIVIDE TRACES

```
5<<2 = 20
20>>2 = 5
-8>>1 in Python = -4 (floor)
Logical 32-bit of -8 >>1: (0xFFFFFFF8)>>1 under mask rules
```

---

# PART 24: WHEN BITWISE IS OVERKILL — CASE STUDIES

1. **Two Sum** — hashmap, not XOR (XOR doesn't give indices easily for arbitrary targets).  
2. **Contains Duplicate** — set, not bits (universe huge).  
3. **Sort colors** — Dutch flag, not bit tricks.  
4. **n=100 subsets** — impossible with 2^n masks; use backtracking/DP differently.

---

# PART 25: INTERVIEW Q&A

**Q: Why is XOR associative useful?**  
A: You can XOR in any order; streaming unique-finding works.

**Q: Difference between `n&1` and `n%2`?**  
A: Same for non-neg; bit form signals intent + micro-speed.

**Q: How does `n&-n` work?**  
A: Two's complement `-n = ~n+1` clears bits after lowest 1 and flips below; AND isolates lowest 1.

---

# PART 26: BLIND CODE CHECKLIST

- [ ] Width/mask if 32-bit required  
- [ ] `n>0` for power-of-two  
- [ ] Prefer `pow`/`bit_count` when clear  
- [ ] Don't use `~` bare in Python without mask  

---

**Final status:** Bit Manipulation — `content-delivered` (≥95% craft).

---

# PART 27: FULL WORKED SOLUTION BANK (BITWISE)

## S1 — Single Number
`x=0; for n in nums: x^=n; return x`

## S2 — Hamming Weight
Loop `n&=n-1` counting iterations.

## S3 — Counting Bits DP
`ans[i]=ans[i&(i-1)]+1`

## S4 — Power of Two / Four
`n>0 and n&(n-1)==0`; four: also `n&0x55555555`.

## S5 — Reverse Bits 32
32 iterations: `ans=(ans<<1)|(n&1); n>>=1`

## S6 — Missing Number
XOR all indices and values with `n`.

## S7 — Single Number III
XOR all → `mask=x&-x` → partition XOR.

## S8 — Subsets via masks
`for mask in range(1<<n)` collect bits.

## S9 — Hamming Distance
`(x^y).bit_count()`

## S10 — Range AND
Shift `left,right` until equal; shift back.

---

# PART 28: BITSET AS SMALL-UNIVERSE SET

```python
s = 0
s |= 1 << x      # add
s &= ~(1 << x)   # remove
(s >> x) & 1     # contains
s.bit_count()    # size
```

Universe `0..63` fits in one Python int; larger → array of ints or `set`.

---

# PART 29: GRAY CODE

```python
def grayCode(n):
    return [i ^ (i >> 1) for i in range(1 << n)]
```

Adjacent codes differ by one bit — useful for certain enumeration / hardware interview trivia.

---

# PART 30: SUBMASK ENUMERATION TRACE

Mask `0b1101` (13). Submasks via `s=(s-1)&mask`:
`1101, 1100, 1001, 1000, 0101, 0100, 0001, 0000`.

Used in SOS DP / subset DP transitions (advanced).

---

# PART 31: ORAL EXAM

1. Why XOR finds unique among pairs?  
2. What does `n&-n` isolate?  
3. Why `~` needs a width mask in Python?  
4. When is bitmask subset enum wrong?  
5. Hashmap vs XOR for single-number?

**Answers:** cancel pairs; lowest set bit value; infinite sign bits; n>~22; hashmap if need indices/counts beyond XOR algebra.

---

# PART 32: FINAL BITWISE MASTERY CHECK

Operators · masks · XOR family · `n&(n-1)` · subsets · when not bits.

**Final status:** Bit Manipulation — `content-delivered` (≥95% craft).
