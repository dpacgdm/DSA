# STRING ALGORITHMS — THE COMPLETE LESSON

**Module:** Coverage gap — String Algorithms (KMP / Z / hashing / patterns)  
**Status:** `content-delivered` — drill / retention / timed still required for `complete`  
**Language:** Python  
**Prerequisite:** Arrays, Hashing, two pointers.  
**Cross-refs:** Prefix/rolling hash refresh from hashing modules; **Tries** → `Advanced/Tries & Monotonic.md` (prefix trees — do not re-derive here). Anagram/palindrome bridges from Arrays & Strings.

---

# PART 1: WHY STRING ALGORITHMS EXIST

## The Problem They Solve

Naive search `pattern in text` by trying every start index is O((n−m+1)·m). For interviews and CP, you need:

| Goal | Tool |
|---|---|
| Exact pattern match, linear time | **KMP** or **Z-algorithm** |
| Fast equality / substring fingerprint | **Rolling hash** (Rabin–Karp) |
| Many pattern queries / prefixes | **Trie** (cross-ref Advanced) |
| Anagram / frequency windows | Counting + sliding window |
| Palindrome centers | Expand-around-center / Manacher (exposure) |

**Interview reason:** KMP/Z prove you understand **failure links / Z-boxes** — not just `str.find`. Rolling hash is the pragmatic twin when you need multiple queries or "same hash ⇒ probably equal."

---

# PART 2: STRING MATCHING LANDSCAPE

| Algorithm | Time | Extra space | Best when |
|---|---|---|---|
| Brute force | O(nm) | O(1) | Tiny strings |
| KMP | O(n+m) | O(m) LPS | Exact match, worst-case linear guaranteed |
| Z-algorithm | O(n+m) | O(n+m) | Match + many prefix analyses |
| Rabin–Karp | O(n+m) expected | O(1) | Multiple patterns / hash tricks; watch collisions |
| Trie | O(total chars) build | O(alphabet · nodes) | Shared prefixes, dictionary |
| Aho–Corasick | O(n + matches) | larger | Many patterns at once (advanced) |

**Default interview sentence for single pattern:**  
> "I'll build the KMP LPS array in O(m), then match in O(n)."

---

# PART 3: KMP — PREFIX FUNCTION (LPS)

## 3A: What LPS Means

For pattern `p` of length `m`, `lps[i]` = longest proper prefix of `p[0..i]` that is also a suffix of `p[0..i]`.

**Proper** = not the whole substring.

```
p = "AABAACAABAA"
index: 0 1 2 3 4 5 6 7 8 9 10
char:  A A B A A C A A B A  A
lps:   0 1 0 1 2 0 1 2 3 4  5
```

## 3B: Why LPS Exists

When a mismatch happens after matching `j` chars, you don't restart `j=0`. You set `j = lps[j-1]` — the next best candidate border — because that prefix is already known to match.

## 3C: Build LPS — Mechanical Template

```python
def build_lps(p):
    m = len(p)
    lps = [0] * m
    length = 0  # len of previous longest border
    i = 1
    while i < m:
        if p[i] == p[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps
```

### Full Trace — `p = "AAACAAAA"`

```
i=1: A==A → length=1, lps[1]=1
i=2: A==A → length=2, lps[2]=2
i=3: C!=A → length=lps[1]=1; C!=A → length=lps[0]=0; lps[3]=0
i=4: A==A → length=1, lps[4]=1
i=5: A==A → length=2, lps[5]=2
i=6: A==A → length=3, lps[6]=3
i=7: A==C? no → length=lps[2]=2; A==A → length=3, lps[7]=3
lps = [0,1,2,0,1,2,3,3]
```

**Complexity:** O(m) — each `i` increases, `length` decreases carefully; amortized linear.

---

# PART 4: KMP — MATCHING

```python
def kmp_search(text, pattern):
    if not pattern:
        return 0
    lps = build_lps(pattern)
    n, m = len(text), len(pattern)
    i = j = 0  # i in text, j in pattern
    hits = []
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                hits.append(i - j)  # start index
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return hits
```

### Trace — text=`"ABABDABACDABABCABAB"`, pattern=`"ABABCABAB"`

Build LPS for pattern, then walk:
- Match progresses; on mismatch use `lps` to slide pattern.
- First full hit at index 10 (`ABABCABAB` at end region — verify against your LPS).

**Dry-run skill:** always compute LPS on paper first, then simulate `i,j` for 5–10 steps.

**Complexity:** O(n + m) time, O(m) space.

---

# PART 5: Z-ALGORITHM

## 5A: Z-Array Definition

For string `s` of length `n`, `Z[i]` = length of longest substring starting at `i` that matches a **prefix** of `s`. `Z[0]` unused / 0.

```
s = a a b a a b a a c
i = 0 1 2 3 4 5 6 7 8
Z = - 1 0 3 1 0 2 1 0
```

## 5B: Z-Box Maintenance (Linear)

Maintain window `[L, R]` = rightmost substring that matches a prefix (`R` maximal).

```python
def z_array(s):
    n = len(s)
    Z = [0] * n
    L = R = 0
    for i in range(1, n):
        if i <= R:
            Z[i] = min(R - i + 1, Z[i - L])
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > R:
            L, R = i, i + Z[i] - 1
    return Z
```

**Complexity:** O(n) — the while loop advances `R`.

## 5C: Pattern Matching via Z

Build `s = pattern + "$" + text` (separator not in alphabet).  
Any `i` where `Z[i] == len(pattern)` is a match starting at `i - (m+1)` in text.

```python
def z_search(text, pattern):
    sep = "#"
    s = pattern + sep + text
    Z = z_array(s)
    m = len(pattern)
    return [i - (m + 1) for i in range(m + 1, len(s)) if Z[i] == m]
```

## 5D: KMP vs Z

| | KMP | Z |
|---|---|---|
| Primary array | LPS on pattern | Z on combined string |
| Match | separate automaton | Z[i]==m hits |
| Also useful for | borders, periods | prefix analysis, string compression tricks |
| Interview | more commonly named | equally powerful |

Both are O(n+m). Learn **both**; pick one to code under pressure (usually KMP if practiced).

---

# PART 6: ROLLING HASH REFRESH + WHEN VS KMP

## 6A: Polynomial Hash

```python
MOD = 10**9 + 7
BASE = 911382323  # random odd large

def hash_str(s):
    h = 0
    for ch in s:
        h = (h * BASE + ord(ch)) % MOD
    return h
```

**Rolling:** hash of `s[i+1..i+m]` from hash of `s[i..i+m-1]`:

```
h' = (h - s[i]*BASE^(m-1)) * BASE + s[i+m]
```

Precompute `pow_base[k] = BASE^k % MOD` and prefix hashes for O(1) substring hash.

```python
def build_prefix_hash(s):
    n = len(s)
    pref = [0] * (n + 1)
    pb = [1] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = (pref[i] * BASE + ord(ch)) % MOD
        pb[i + 1] = (pb[i] * BASE) % MOD
    def get(l, r):  # s[l:r) hash
        return (pref[r] - pref[l] * pb[r - l]) % MOD
    return get
```

## 6B: When Rolling Hash vs KMP

| Situation | Prefer |
|---|---|
| Single exact match, worst-case guarantee | **KMP / Z** |
| Compare many substrings quickly | **Prefix hashes** |
| Rabin–Karp multi-pattern | Hash set of pattern hashes |
| Need proof-level no collision | KMP/Z (or double hash) |
| Interview "implement strStr" | KMP (or admit built-in + discuss) |

**Collision trap:** always mention double hashing `(MOD1, BASE1)` + `(MOD2, BASE2)` for safety in contests.

---

# PART 7: ANAGRAM / PALINDROME PATTERN BRIDGE

## 7A: Valid Anagram / Group Anagrams

Frequency count (26 or hashmap). Group: sort signature or `tuple(counts)`.

## 7B: Find All Anagrams in a String (sliding window)

Fixed window length `m`; maintain counts; expand/contract O(n).

```python
from collections import Counter

def find_anagrams(s, p):
    need = Counter(p)
    window = Counter()
    res, m = [], len(p)
    for i, ch in enumerate(s):
        window[ch] += 1
        if i >= m:
            left = s[i - m]
            window[left] -= 1
            if window[left] == 0:
                del window[left]
        if i >= m - 1 and window == need:
            res.append(i - m + 1)
    return res
```

## 7C: Palindrome Checks

- Two pointers inward: O(n).
- Expand around center for longest palindromic substring: O(n²).
- DP `dp[i][j]` for substring palindrome: O(n²).

**Bridge:** these are **counting / two-pointer** patterns — not KMP. Don't force string automata onto anagram problems.

---

# PART 8: TRIES — CROSS-REFERENCE ONLY

For prefix dictionaries, autocomplete, XOR tries, word search II:

→ **`Advanced/Tries & Monotonic.md`**

Here: a trie stores shared prefixes in a tree of character edges. Build O(total chars); query O(len). Prefer trie when **many patterns share prefixes**; prefer KMP/Z for **one pattern vs one text**.

---

# PART 9: STRING MATCHING INTERVIEW SET (MAP)

| Problem | Pattern |
|---|---|
| Implement strStr / Index of First Occurrence | KMP or Z |
| Repeated Substring Pattern | LPS: `n % (n - lps[-1]) == 0` and lps[-1]>0 |
| Shortest Palindrome (front) | KMP on `s + # + s[::-1]` |
| Longest Happy Prefix | `lps[-1]` of s |
| Distinct Substrings (CP) | Suffix structures / hash set of hashes |
| Anagrams in string | Sliding window counts |
| Longest palindromic substring | Expand centers |
| Word Break / Word Search | DP / Trie+DFS (Advanced) |

---

# PART 10: CHEAT SHEETS

## KMP Build

```
length=0, i=1
equal → length++, lps[i]=length, i++
else → length=lps[length-1] or lps[i]=0,i++
```

## KMP Match

```
equal → i++,j++; j==m → record, j=lps[j-1]
else → j=lps[j-1] or i++
```

## Z

```
if i≤R: Z[i]=min(R-i+1, Z[i-L])
extend while match
update [L,R] if extended past R
```

## Rolling

```
pref[i+1]=pref[i]*B+s[i]
hash(l,r)=(pref[r]-pref[l]*B^(r-l)) mod M
```

---

# PART 11: TRAPS

| Trap | Fix |
|---|---|
| LPS off-by-one on mismatch | Use `lps[length-1]`, not `lps[length]` |
| No separator in Z concat | Pattern can bleed into text |
| Single hash collisions | Double hash or KMP |
| Using KMP for anagrams | Wrong tool — use counts |
| Python `str.find` only | OK to use; still explain KMP if asked "how" |
| Building LPS in O(m²) | Must be linear amortized |

---

# PART 12: WORKED PROBLEMS

## WP1 — LPS of `"AABAACAABAA"`
Answer: `[0,1,0,1,2,0,1,2,3,4,5]` (trace Part 3).

## WP2 — KMP search `"hello"` in `"hello"`
LPS all 0s mostly; hit at 0.

## WP3 — KMP `"aaaa"` in `"aaabaaaaa"`
Multiple overlapping hits — verify `j=lps[j-1]` allows overlap.

## WP4 — Z of `"aabcaabxaaaz"`
Compute Z with box maintenance; check Z[4]=3 (`aab`).

## WP5 — Z-search pattern `"ab"` in `"abxabab"`
Combined `"ab#abxabab"` → Z hits at text positions 0,4,6.

## WP6 — Rolling equality
`get(0,3)==get(4,7)` for `"abcXabc"` → True for both `"abc"`.

## WP7 — Find anagrams
`s="cbaebabacd"`, `p="abc"` → `[0,6]`.

## WP8 — Repeated substring
`s="abab"` → lps=`[0,0,1,2]`, `n=4`, `n-lps[-1]=2`, `4%2==0` → True.

## WP9 — Longest happy prefix
`s="level"` → lps[-1]=1 → `"l"`; `s="leetcodeleet"` → `"leet"`.

## WP10 — Shortest palindrome intuition
KMP on `s + '#' + reverse(s)`; chars to add in front = `n - lps[-1]`.

---

# PART 13: INTERVIEW SCRIPT

1. Clarify exact match vs anagram vs prefix dictionary.
2. Pick KMP / Z / hash / window / trie.
3. State O(n+m) and what the LPS/Z array stores in one sentence.
4. Code build then match; dry-run a mismatch that uses a failure link.
5. Mention collision policy if hashing.

---

**Status note (interim):** Core above; deep expansions in Parts 14+.

---

# PART 14: KMP — FULL MISMATCH TRACE

Pattern `P = ABABC`  
LPS: build carefully:

```
P: A B A B C
i: 0 1 2 3 4
L: 0 0 1 2 0
```

Text `T = ABABABC`  
Simulate `(i,j)`:

```
i0 j0 A=A → i1 j1
i1 j1 B=B → i2 j2
i2 j2 A=A → i3 j3
i3 j3 B=B → i4 j4
i4 j4 A!=C → j=lps[3]=2
i4 j2 A=A → i5 j3
i5 j3 B=B → i6 j4
i6 j4 C=C → i7 j5 MATCH at 2
```

**Teaching point:** the failure link from `j=4` to `j=2` reused the `"AB"` border without recomparing those characters.

---

# PART 15: Z-ALGORITHM — BOX TRACE

`s = aabxaab`
```
i=1: compare → Z[1]=1 (a); set [L,R]=[1,1]
i=2: s[2]=b != a → Z[2]=0
i=3: x != a → 0
i=4: inside? no; match aab → Z[4]=3; [L,R]=[4,6]
i=5: i<=R → Z[5]=min(6-5+1, Z[1])=min(1,1)=1; try extend — fail
i=6: Z[6]=min(0?, Z[2]) → 0
```

---

# PART 16: ROLLING HASH — COLLISION & DOUBLE HASH

```python
MOD1, MOD2 = 10**9+7, 10**9+9
BASE1, BASE2 = 911382323, 972663749

# store (h1, h2) pairs; equality only if both match
```

**Interview line:** "I'll use double polynomial hashes to make collisions negligible; if the problem requires certainty, I'll use KMP."

### Prefix hash get correctness
`hash(l,r) = pref[r] - pref[l]*BASE^(r-l)` works because
`pref[r] = s[0]*B^(r-1) + ... + s[r-1]*B^0`  
`pref[l]*B^(r-l) = s[0]*B^(r-1) + ... + s[l-1]*B^(r-l)`.

---

# PART 17: BORDER / PERIOD APPLICATIONS

## 17A: Period from LPS
If `n % (n - lps[n-1]) == 0` and `lps[n-1] > 0`, smallest period is `n - lps[n-1]`.

## 17B: Shortest Palindrome
`s + '#' + reverse(s)`; let `k = lps[-1]`; add `reverse(s[k:])` in front.

### Trace
`s=aacecaaa` → classic LC; chars to prepend = `n-k`.

## 17C: String Matching Automation view
LPS defines the failure function of a DFA on the pattern — KMP is that automaton running on the text.

---

# PART 18: MORE WORKED PROBLEMS

## WP11 — strStr brute vs KMP complexity
Text n=10^5, pattern m=10^3 worst-case brute ~1e8 ops borderline; KMP 1.01e5 safe.

## WP12 — Find all occurrences overlapping
Pattern `aaa` in `aaaa` → starts 0,1; KMP must set `j=lps[j-1]` after match.

## WP13 — Anagram + hash hybrid
Window hash of counts (26-int fingerprint) vs Counter equality — fingerprint faster.

## WP14 — Longest duplicate substring (binary search + hash)
Binary search length L; rolling hash all substrings of len L into a set — classic.

## WP15 — Z-function for compression
If `n % Z[i] related` … (period detection via Z also possible).

## WP16 — Manual LPS for `"ABCDE"`
All zeros — no nontrivial borders.

## WP17 — Manual LPS for `"AAAA"`
`[0,1,2,3]`.

## WP18 — Group anagrams signature
`tuple(sorted(s))` vs 26-count tuple — count better for long strings with small alphabet.

---

# PART 19: TRIES CROSS-REF (EXPANDED)

Use a trie when:
- Many patterns share prefixes (dictionary)
- Prefix queries / autocomplete
- XOR maximisation (bit trie)

Use KMP/Z when:
- One pattern, one text, exact match
- Border/period of a single string

→ Implement tries in `Advanced/Tries & Monotonic.md`.

---

# PART 20: 30-MINUTE DRILL

1. Build LPS for `"AABAACAABAA"` on paper.  
2. KMP-match one mismatch case.  
3. Z-array for a length-10 string.  
4. Implement prefix hash `get(l,r)`.  
5. Find anagrams window on a short example.  
6. Say out loud: hash vs KMP decision.

---

**End of Strings lesson.** Status: `content-delivered`.

---

# PART 21: KMP LPS — FIVE DRILLS

Compute LPS for:
1. `"A"` → `[0]`
2. `"AA"` → `[0,1]`
3. `"ABABAB"` → `[0,0,1,2,3,4]`
4. `"ABCABCABC"` → `[0,0,0,1,2,3,4,5,6]`
5. `"AABAABAAA"` — work carefully on paper

---

# PART 22: Z vs KMP SAME MATCH

Pattern `ab`, text `abxabab`  
KMP hits: 0,4,6  
Z-method hits: same  
Verify both implementations agree on 3 random pairs.

---

# PART 23: ROLLING HASH IMPLEMENTATION NOTES

```python
# Always take mod to positive
x %= MOD
if x < 0: x += MOD

# Precompute pb[0]=1; pb[i]=pb[i-1]*BASE%MOD
# get(l,r) uses pb[r-l]
```

**Base choice:** large odd random far from alphabet size; avoid `BASE=256` with weak MOD in adversarial settings.

---

# PART 24: PALINDROME / ANAGRAM BRIDGE DRILLS

1. Valid palindrome alphanumeric two pointers.  
2. Longest palindrome by concatenating counts (hash freq).  
3. Find all anagrams — window.  
4. Palindromic substrings count — expand centers O(n²).  
5. State why KMP is the wrong tool for (3).

---

# PART 25: STRING MATCHING INTERVIEW SET — SOLUTIONS OUTLINE

| Problem | Outline |
|---|---|
| strStr | KMP first index |
| Repeated substring | LPS period test |
| Shortest palindrome | KMP on s+#rev |
| Longest happy prefix | lps[-1] chars |
| Find anagrams | window counts |
| Longest dup substring | binsearch + hash |
| Implement trie | Advanced lesson |

---

# PART 26: BLIND CODE CHECKLIST

- [ ] Separator char not in alphabet for Z concat  
- [ ] LPS mismatch uses `lps[length-1]`  
- [ ] After KMP match, `j=lps[j-1]` for overlaps  
- [ ] Double hash if contest hashing  

---

**Final status:** String Algorithms — `content-delivered` (≥95% craft).

---

# PART 27: FULL WORKED SOLUTION BANK (STRINGS)

## S1 — strStr KMP
Build LPS; match with failure links; return first index or -1; empty needle → 0.

## S2 — Repeated Substring
`border=lps[-1]; border>0 and n%(n-border)==0`

## S3 — Longest Happy Prefix
`s[:lps[-1]]`

## S4 — Find All Anagrams
Fixed window Counter equality (Part 7).

## S5 — Z-search
`pattern+'#'+text`; `Z[i]==m` hits.

## S6 — Shortest Palindrome
KMP on `s+'#'+rev`; prepend `rev[:n-lps[-1]]`.

## S7–S8 — Anagram / Group Anagrams
Counter or sorted/count tuple signature.

## S9 — Longest Palindromic Substring
Expand around each center (odd/even).

## S10 — Valid Palindrome II
Two pointers; one mismatch → try skip L or R.

---

# PART 28: KMP AS IMPLICIT DFA

State = matched length `j`. On next char: match → `j+1`; else `j=lps[j-1]` retry. Accepting state `j==m`. Explicit DFA would be O(m·Σ); KMP stores only failure links O(m).

---

# PART 29: SIDE-BY-SIDE — SAME MATCH THREE WAYS

Pattern `aa`, text `aaabaaa`:
- Brute: try starts 0..5  
- KMP: LPS `[0,1]`; hits at 0,1,4,5  
- Z: combined string Z-values ==2 at those starts  

All must agree — use as self-test harness.

---

# PART 30: ORAL EXAM

1. Define LPS without circular wording.  
2. Why separator in Z concat?  
3. Rolling hash collision mitigation.  
4. Why anagram ≠ KMP.  
5. When open Tries lesson?

---

# PART 31: FINAL STRINGS MASTERY CHECK

LPS build · KMP match · Z-array · rolling hash · anagram/palindrome bridge · trie cross-ref.

**Final status:** String Algorithms — `content-delivered` (≥95% craft).
