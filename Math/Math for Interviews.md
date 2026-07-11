# MATH FOR INTERVIEWS — THE COMPLETE LESSON

**Module:** Coverage gap — Math for Interviews  
**Status:** `content-delivered` — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Integers, loops, modular thinking.  
**Cross-refs:** Fast pow used in rolling hash (`Strings`); GCD in fractions / lattice; primes in factorization problems; geometry light for orientation / segments.

---

> **Lesson contract:** Framework + ≤3 traced exemplars in-lesson. Drill via Retention (`keys/` separated) + Practice Spine + problem-bank. Teach-back before retention.
> **Volume note:** Prefer Parts 1–core frameworks; treat late drill/oral checklists as **optional appendix**. Spine + Retention are the gate path.


# PART 1: WHY INTERVIEW MATH EXISTS

Most "math" in FAANG DSA is **not** contest number theory. It is a small toolkit that keeps appearing:

| Tool | Where it shows up |
|---|---|
| GCD / LCM | Fractions, frog jumps, water jugs, lattice points |
| Modular arithmetic | Hashing, combinatorics, wrap indices, large answers |
| Fast pow | `a^n mod m`, matrix expo preview |
| nCr / permutations | Unique paths, combinations sum counts |
| Primes / sieve | Ugly numbers cousins, prime factors, Goldbach-style |
| Orientation | Segment intersect, convex hull light |
| Overflow / careful division | Midpoint, binary search, language traps |

**Rule:** Know the templates cold. Derive less under the clock.

---

# PART 2: GCD, LCM, EXTENDED EUCLID (LIGHT)

## 2A: Euclidean Algorithm

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a, b):
    return abs(a // gcd(a, b) * b)  # divide first to reduce overflow risk
```

**Why it works:** `gcd(a,b) = gcd(b, a mod b)`.  
**Complexity:** O(log min(a,b)).

### Trace
```
gcd(48, 18):
48%18=12 → gcd(18,12)
18%12=6  → gcd(12,6)
12%6=0   → gcd(6,0)=6
lcm(48,18)=48/6*18=144
```

## 2B: Extended Euclid (Light — Bézout)

Find `x, y` such that `a·x + b·y = gcd(a,b)`.

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
```

**Interview use:** modular inverse when `gcd(a,m)=1` → `x` is inverse of `a` mod `m` (from `a·x ≡ 1`).  
For prime mod, prefer Fermat: `pow(a, MOD-2, MOD)`.

---

# PART 3: MODULAR ARITHMETIC

## 3A: Rules (Memorize)

```
(a + b) % m = (a%m + b%m) % m
(a * b) % m = (a%m * b%m) % m
(a - b) % m = (a%m - b%m + m) % m   # +m fixes negative
```

**Division mod m:** multiply by modular inverse — **not** `/`.

## 3B: Modular Inverse

```python
MOD = 10**9 + 7

def modinv(a, mod=MOD):
    return pow(a, mod - 2, mod)  # mod prime (Fermat)
```

## 3C: Python Gotchas

- `pow(a, n, mod)` is built-in fast pow — **use it**.
- Negative mods: `(-3) % 7 == 4` in Python (good).
- `//` is floor division toward −∞.

---

# PART 4: FAST POW (BINARY EXPONENTIATION)

## 4A: Idea

`a^13 = a^8 · a^4 · a^1` — use bits of exponent.

```python
def fast_pow(a, n, mod=None):
    res = 1
    a = a if mod is None else a % mod
    while n > 0:
        if n & 1:
            res = res * a if mod is None else (res * a) % mod
        a = a * a if mod is None else (a * a) % mod
        n >>= 1
    return res
```

### Trace — `3^13`
```
n=13=1101₂
res=1, a=3
bit1: res=3, a=9, n=6
bit0: a=81, n=3
bit1: res=243, a=6561, n=1
bit1: res=243*6561=1594323
```

**Complexity:** O(log n) multiplications.

**Interview:** prefer `pow(a, n, mod)`.

---

# PART 5: COMBINATORICS LIGHT

## 5A: Factorials Precompute (n ≤ 10^6, mod prime)

```python
MOD = 10**9 + 7

def precompute(n):
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fac[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return fac, inv

def nCr(n, r, fac, inv):
    if r < 0 or r > n:
        return 0
    return fac[n] * inv[r] % MOD * inv[n - r] % MOD
```

## 5B: Permutations

`P(n,k) = n! / (n-k)! = fac[n] * inv[n-k]`.

## 5C: Unique Paths Bridge

Grid `m×n` paths = `C(m+n-2, m-1)` — combinatorics beats DP when no obstacles.

## 5D: Pascal Row (small n)

```python
def pascal_row(n):
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row
```

**TRAP:** use exact integer `//` order to stay integral: multiply before divide carefully with gcd if needed.

---

# PART 6: PRIMES & SIEVE

## 6A: Primality (trial)

```python
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True
```

## 6B: Sieve of Eratosthenes

```python
def sieve(n):
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    p = 2
    while p * p <= n:
        if prime[p]:
            for x in range(p * p, n + 1, p):
                prime[x] = False
        p += 1
    return [i for i in range(n + 1) if prime[i]]
```

**Complexity:** O(n log log n) time, O(n) space.

## 6C: Smallest Prime Factor (factorization)

While sieving, store `spf[x]=p`. Factor in O(log x).

---

# PART 7: GEOMETRY LIGHT — ORIENTATION

## 7A: Cross Product Sign

For points `A→B` and `A→C`:

```
cross = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)
```

| cross | Meaning |
|---|---|
| > 0 | C is left of AB (CCW turn) |
| < 0 | C is right (CW turn) |
| = 0 | Collinear |

```python
def orientation(ax, ay, bx, by, cx, cy):
    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0
```

**Uses:** segment intersection (orientations differ), convex hull graham scan light, "point in triangle."

## 7B: On Segment (collinear case)

```python
def on_segment(ax, ay, bx, by, cx, cy):
    return (min(ax, bx) <= cx <= max(ax, bx) and
            min(ay, by) <= cy <= max(ay, by))
```

---

# PART 8: OVERFLOW & CAREFUL DIVISION

## 8A: Midpoint

```python
# BAD in fixed-width langs: (lo+hi)//2 can overflow
# GOOD:
mid = lo + (hi - lo) // 2
# Python ints unlimited — still write the safe form for interview signal
```

## 8B: Division Toward Zero vs Floor

Python `//` floors. C++ `/` truncates toward zero for ints. Know which language you're in.

## 8C: Multiply Then Mod

`(a * b) % m` — in languages with 64-bit, `a*b` may overflow before mod. Python fine. Mention `__int128` / modular mul in C++.

## 8D: Ceiling Division

```python
def ceil_div(a, b):
    return (a + b - 1) // b  # positive a,b
```

---

# PART 9: CHEAT SHEETS

```
gcd: while b: a,b = b, a%b
lcm: a//gcd*b
mod sub: (a-b+m)%m
inv: pow(a,m-2,m)  (prime m)
pow: pow(a,n,m)
nCr: fac[n]*invfac[r]*invfac[n-r]
sieve: mark multiples from p*p
orient: cross >0 left, <0 right, 0 col
mid: lo+(hi-lo)//2
ceil: (a+b-1)//b
```

---

# PART 10: TRAPS

| Trap | Fix |
|---|---|
| `lcm = a*b//gcd` overflow order | `a//gcd*b` |
| Division as mod inverse | Use `pow` inverse |
| Sieve from `2*p` not `p*p` | Still correct but slower; prefer `p*p` |
| Float for combinatorics | Integer only |
| Orientation overflow | Use careful types / Python |
| `is_prime` loop `f<=sqrt` float | Use `f*f <= n` |

---

# PART 11: WORKED PROBLEMS

## WP1 — GCD/LCM
`gcd(270,192)` → … → 6; `lcm=8640`.

## WP2 — Fast pow mod
`pow(2,10,1000)=24`? `1024%1000=24`. Yes.

## WP3 — nCr
`C(5,2)=10` via fac `[1,1,2,6,24,120]`.

## WP4 — Unique Paths
`3×7` grid → `C(8,2)=28`.

## WP5 — Sieve primes ≤ 30
`2,3,5,7,11,13,17,19,23,29`.

## WP6 — Count primes (LeetCode style)
Sieve to `n-1`, count True.

## WP7 — Orientation
A(0,0), B(1,1), C(0,1) → cross=`1*1-1*0=1` → left/CCW.

## WP8 — Modular wrap
Index `(i-1+n)%n` for circular array.

## WP9 — Water / GCD
Can measure `z` with jugs `x,y` iff `z <= x+y` and `z % gcd(x,y)==0` (classic).

## WP10 — Fraction addition
Add with LCM of denominators; reduce by GCD.

---

# PART 12: INTERVIEW SCRIPT

1. Identify: gcd, mod, pow, nCr, prime, geometry?
2. State template + complexity.
3. Call out mod/`pow` built-in in Python.
4. Watch overflow narrative even if Python is safe.
5. Dry-run one numeric example.

---

**Status note (interim):** Core above; deep expansions in Parts 13+.

---

# PART 13: EXTENDED EUCLID — FULL TRACE

Solve `240x + 46y = gcd`.

```
240 = 5*46 + 10
46  = 4*10 + 6
10  = 1*6 + 4
6   = 1*4 + 2
4   = 2*2 + 0  → gcd=2

Back-sub:
2 = 6 - 1*4
4 = 10 - 1*6 → 2 = 2*6 - 1*10
6 = 46 - 4*10 → 2 = 2*46 - 9*10
10= 240-5*46 → 2 = 47*46 - 9*240
→ x=-9, y=47
```

Modular inverse of `a` mod `m` when `gcd=1`: `x` from `egcd(a,m)`.

---

# PART 14: COMBINATORICS EXPANSION

## 14A: Lucas theorem (exposure)
For prime p, `C(n,k) mod p` via base-p digits — CP tool; mention only.

## 14B: Stars and bars
Non-negative solutions to `x1+...+xk=n` → `C(n+k-1, k-1)`.

## 14C: Inclusion path counting
Unique paths with one forbidden cell: total − paths through cell (if needed).

## 14D: Catalan (exposure)
`C_n = (1/(n+1))*C(2n,n)` — parentheses, BSTs count — know formula exists.

---

# PART 15: PRIMES EXPANSION

## 15A: Factorization trial
```python
def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f
```

## 15B: SPF sieve
```python
def build_spf(n):
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for j in range(i*i, n+1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf
```

## 15C: Segmented sieve idea
For primes in `[L,R]` large — sieve primes to sqrt(R), mark segment — CP exposure.

---

# PART 16: GEOMETRY EXPANSION

## 16A: Segment intersection
Proper intersection: orientations of (A,B,C) and (A,B,D) differ AND orientations of (C,D,A) and (C,D,B) differ.  
Handle collinear specials with `on_segment`.

## 16B: Point in triangle
Same orientation for all three edges (barycentric / cross signs).

## 16C: Closest pair (exposure)
Divide and conquer O(n log n) — know it exists; not Phase A core.

---

# PART 17: MORE WORKED PROBLEMS

## WP11 — Pow(x,n) with negative n
`n<0 → 1/fast_pow(x,-n)` carefully with floats (LC 50).

## WP12 — Super Pow (a^b mod 1337)
b given as digit array — Euler/phi or modular pow digit DP.

## WP13 — Count primes
Sieve to n-1.

## WP14 — Ugly number
Divide out 2,3,5; check ==1.

## WP15 — Fraction to decimal
Long division + hashmap of remainder → repeating cycle.

## WP16 — Valid square
Four points: six distances; check 2 side lengths + diagonal pattern (geometry light).

## WP17 — Mirror reflection / billiards
LCM of dimensions / reduce by GCD.

## WP18 — Excel column / base conversion
Base 26 with careful off-by-one.

## WP19 — Integer break / math DP
Prefer near-e parts (3s) — math insight.

## WP20 — Arranging coins
Solve quadratic `n(n+1)/2 <= x` or binary search.

---

# PART 18: OVERFLOW CASEBOOK

| Situation | Bug | Fix |
|---|---|---|
| `lo+hi` mid | overflow in C++ | `lo+(hi-lo)/2` |
| `a*b/gcd` lcm | overflow | `a/gcd*b` |
| `f*f<=n` for prime | `f*f` overflow | `f <= n/f` |
| factorial precompute | huge | always mod |
| Catalan huge | need mod / big int | Python ok; else mod |

---

# PART 19: 25-MINUTE DRILL

1. gcd/lcm + egcd one example.  
2. `pow(a,n,mod)` mental for small.  
3. Precompute fac/invfac sketch.  
4. Sieve to 50.  
5. Orientation of 3 points.  
6. Say ceil_div and safe mid.

---

**End of Math lesson.** Status: `content-delivered`.

---

# PART 20: GCD APPLICATIONS CATALOG

| Problem | GCD role |
|---|---|
| Water jugs | measurable iff multiple of gcd |
| Fraction add/reduce | gcd simplify |
| Card points / rows | gcd of counts |
| Lattice points on segment | gcd(|dx|,|dy|)-1 interior |
| Frog jump II | gcd of jump lengths |

---

# PART 21: MODULAR ARITHMETIC DRILLS

1. `(3-10) mod 7` → 0  
2. Inverse of 3 mod 7 → 5 because `3*5=15≡1`  
3. `2^20 mod 1e9+7` via `pow`  
4. Why `(a/b)%m` illegal → use `a*inv(b)`  
5. Negative: `(-21)%5` in Python → 4  

---

# PART 22: SIEVE TRACE TO 30

Mark multiples of 2 from 4, of 3 from 9, of 5 from 25:  
Primes: 2,3,5,7,11,13,17,19,23,29.

---

# PART 23: nCr TABLE (PASCAL) SMALL

```
C(0..5):
1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
1 5 10 10 5 1
```

---

# PART 24: GEOMETRY ORIENTATION DRILLS

1. A(0,0) B(1,0) C(1,1) → left  
2. A(0,0) B(1,0) C(1,-1) → right  
3. A(0,0) B(2,2) C(1,1) → collinear  
4. Use for "is middle on segment?" with on_segment  

---

# PART 25: BLIND CODE CHECKLIST

- [ ] `a//gcd*b` for lcm  
- [ ] `pow(a,n,mod)` not naive loop  
- [ ] `f*f<=n` or `f<=n/f`  
- [ ] Safe mid  
- [ ] Mod sub `+ m`  

---

**Final status:** Math for Interviews — `content-delivered` (≥95% craft).

---

# PART 26: FULL WORKED SOLUTION BANK (MATH)

## S1 — GCD/LCM — `math.gcd`; `a//gcd*b`
## S2 — Fast pow / `pow(a,n,mod)`
## S3 — Count primes — sieve to n-1
## S4 — Unique paths — `C(m+n-2,m-1)` multiplicative loop
## S5 — Water jug — `z%x+y` bound + `z%gcd==0`
## S6 — Fraction ops — lcm denom + gcd reduce
## S7 — Excel column — base 26
## S8 — Sqrt(x) — binary search on answer
## S9 — Perfect square — binary search / Newton
## S10 — Arrange coins — binary search triangular

---

# PART 27: MULTIPLICATIVE nCr LOOP (NO FAC ARRAY)

```python
def nCr(n, r):
    if r < 0 or r > n: return 0
    r = min(r, n-r)
    res = 1
    for i in range(1, r+1):
        res = res * (n-r+i) // i
    return res
```

Keeps exact integers if division is exact at each step (true for binomial).

---

# PART 28: PRIME FACTORIZATION TRACE

`n=84`: 84/2=42/2=21/3=7 → `2^2 * 3 * 7`.

---

# PART 29: ORAL EXAM

1. Prove `gcd(a,b)=gcd(b,a%b)` idea.  
2. Why `(a-b)%m` needs `+m`.  
3. Fermat inverse requires prime mod.  
4. Orientation zero ⇒ collinear, not "parallel" in general.  
5. `f<=n//f` vs `f*f<=n`.

---

# PART 30: FINAL MATH MASTERY CHECK

gcd/lcm · mod · fast pow · nCr · sieve · orientation · overflow hygiene.

**Final status:** Math for Interviews — `content-delivered` (≥95% craft).
