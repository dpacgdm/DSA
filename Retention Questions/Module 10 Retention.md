<!-- ANSWER KEYS MOVED: see Retention Questions/keys/Module 10 Retention.keys.md -->
> **Blind mode:** Answers were moved to `keys/Module 10 Retention.keys.md`. Attempt first, then grade.

# MODULE 10 RETENTION — TRIES, MONOTONIC DEEP DIVE, FENWICK EXPOSURE

**With answers.** Blind first: cover answers, solve/speak, then check.

**Materials:**
- `Advanced/Tries & Monotonic.md`
- `Advanced/Segment & Fenwick Exposure.md` (**exposure only**)

**Cumulative light pull:** stacks/queues mono intro (M4), sliding window (M1/M6), hashing vs trie judgment, recursion/backtracking for wildcard / board+trie.

**Pass bar (suggested):** Rapid fire ≥ 80% · Conceptual teach-back solid · Problems ≥ 6/8 · Fenwick section = recognition + simple reasoning (not CP mastery). Tag misses.

**Label:** Fenwick/segment questions are **exposure**. Failing to hand-write a full segment tree does **not** fail Module 10 if tries + monotonic are strong and you can explain when BIT/segtree apply.

---

# SECTION A: RAPID FIRE

---

## A1. What two fields does every trie node need at minimum?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 1)

## A2. Time of insert and exact search for a word of length L?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 2)

## A3. `search("app")` after only inserting `"apple"` — True or False? `startsWith("app")`?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 3)

## A4. Why is a hash set enough for exact dictionary membership but weak for autocomplete?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 4)

## A5. Wildcard `.` in Word Dictionary — what changes in search?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 5)

## A6. Replace words: why stop at the first `is_end` while walking?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 6)

## A7. Monotonic stack O(n) law?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 7)

## A8. Sum of subarray minimums: what do you count per index?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 8)

## A9. Why asymmetric strictness on left vs right spans for equal elements?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 9)

## A10. Remove k digits for smallest number — stack invariant?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 10)

## A11. Stock span: what does the stack store and why amortized O(1)?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 11)

## A12. Sliding window max vs min — deque order?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 12)

## A13. Longest subarray with max−min ≤ limit — tools?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 13)

## A14. Max chunks (permutation 0..n-1) — one-line rule?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 14)

## A15. Fenwick exposure: point update + range sum complexities?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 15)

## A16. When is Fenwick/segment overkill in an interview?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 16)

# SECTION B: CONCEPTUAL TEACH-BACK

---

## B1. Draw/describe a trie after inserting `cat`, `car`, `dog`. Where are `is_end` flags?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 17)

## B2. Explain Word Search II pruning: why trie + board DFS beats "DFS + set of words" alone?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 18)

## B3. Derive contribution for sum of subarray mins on `[3,1,2]` (mod not needed). Walk spans.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 19)

## B4. Remove k digits `"1432219"`, k=3 — narrate pops.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 20)

## B5. Online stock span vs offline next greater — relationship?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 21)

## B6. Fenwick: what does range sum(L,R) reduce to? Why keep a copy of the array for LC307 updates?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 22)

## B7. Trie vs dict of words for Replace Words — tradeoff?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 23)

# SECTION C: PROBLEM SOLVING (WITH ANSWERS)

---

## C1. Implement Trie (insert / search / startsWith)


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 24)

## C2. WordDictionary with `.`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 25)

## C3. Sum of Subarray Minimums


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 26)

## C4. Remove K Digits


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 27)

## C5. StockSpanner


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 28)

## C6. Longest Subarray max−min ≤ limit


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 29)

## C7. Max Chunks To Sorted (0..n-1 permutation)


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 30)

## C8. Replace Words


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 31)

## C9. [Exposure] NumArray mutable range sum via Fenwick


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 32)

## C10. [Hard] Sketch Word Search II approach (code optional)


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 33)

# SECTION D: TRICK / JUDGMENT

---

## D1. True/False: You need a segment tree for sliding window maximum.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 34)

## D2. True/False: Module 10 complete requires coding lazy segment trees.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 35)

## D3. For static array range sums, interviewer asks to optimize updates later — what do you say?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 36)

## D4. Can contribution technique for subarray mins use a deque instead of stack?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 37)

## D5. Autocomplete: is storing top-k at every trie node required for LC?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 38)

# SECTION E: CUMULATIVE PULL (LIGHT)

---

## E1. Daily temperatures (M4) vs stock span — one difference?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 39)

## E2. Histogram largest rectangle — still mono stack?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 40)

## E3. Prefix sum + hash vs Fenwick — when each?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 41)

# SECTION F: SELF-AUDIT

| Check | Done? |
|---|---|
| Trie insert/search/prefix/`is_end` cold | |
| Wildcard + replace words reasoning | |
| Contribution / remove k digits / stock span / dual deque | |
| Fenwick: when + O(log n) + delta update idea | |
| Did not confuse exposure with mastery | |
| Ledger + scoreboard updated | |
| Timed verify for M10 patterns still required for `complete` | |

---

# SECTION G: EXPANDED RAPID FIRE (A17–A40)

---

## A17. What does storing `word` on a trie terminal buy you in Word Search II?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 42)

## A18. Why mark board cells `#` and unmark after DFS?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 43)

## A19. Contribution: if `left[i]=2` and `right[i]=3`, how many subarrays have `arr[i]` as exclusive min?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 44)

## A20. Sum of subarray ranges = ?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 45)

## A21. Remove k digits on an already non-decreasing number — what happens?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 46)

## A22. Stock span vs daily temperatures — online vs offline?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 47)

## A23. Dual deque window: what do you do when `left` advances past `maxq[0]`?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 48)

## A24. Max chunks permutation: `arr=[0,1,2]` chunks?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 49)

## A25. Fenwick `range_sum(0,0)` equals?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 50)

## A26. True/False: Segment tree is required for Phase A complete.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 51)

## A27. Asteroid collision: `[5,10,-5]` result?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 52)

## A28. 132 pattern: need i < j < k with nums[i] < nums[k] < nums[j]. Mono direction?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 53)

## A29. Map Sum: overwrite key — what do you add along the path?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 54)

## A30. Trie children as `list[26]` vs `dict` — when list?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 55)

## A31. Histogram sentinels of height 0 — why?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 56)

## A32. Maximal rectangle in binary matrix — reduction?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 57)

## A33. Remove duplicate letters: when may you pop the stack top?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 58)

## A34. Word Dictionary: search `"a.a"` with only `"aa"` inserted?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 59)

## A35. Complexity of building trie from words with total characters T?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 60)

## A36. Sliding window minimum deque order?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 61)

## A37. LC 307 without Fenwick — acceptable?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 62)

## A38. Prefix sums vs Fenwick one-liner?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 63)

## A39. Can `startsWith` be implemented using `search`?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 64)

## A40. Monotonic stack storing values not indices — when OK?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 65)

# SECTION H: MORE CONCEPTUAL TEACH-BACKS

---

## B8. Walk Word Search II on a 1×3 board `a b a` with words `["aba","ba"]`.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 66)

## B9. Derive sum of subarray mins for `[1,2,1]` with asymmetric spans. Show enumeration.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 67)

## B10. Explain remove duplicate letters on `"bcabc"`.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 68)

## B11. Why dual deques for max−min constraint, not one?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 69)

## B12. Fenwick interview 60-second pitch.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 70)

# SECTION I: FULL PROBLEM SET (WITH COMPLETE ANSWERS)

---

## C11. Implement Trie — with delete (optional stretch)


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 71)

## C12. MapSum


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 72)

## C13. Sum of Subarray Ranges — full code


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 73)

## C14. Largest Rectangle in Histogram — full code + trace `[2,4]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 74)

## C15. Maximal Rectangle


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 75)

## C16. Remove Duplicate Letters


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 76)

## C17. Asteroid Collision — `"10,2,-5"` 


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 77)

## C18. Find 132 Pattern


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 78)

## C19. Online Stock Span — implement + stream `[31,41,48,59,79]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 79)

## C20. Longest subarray max−min ≤ 0


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 80)

## C21. [Exposure] Fenwick — count of range sum queries after updates

**Prompt:** Start `[1,2,3,4]`; `sum(0,3)`; `add(2,+5)`; `sum(2,3)`.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 81)

## C22. Word Search II — return order


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 82)

## C23. Magic Dictionary (one edit)


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 83)

## C24. Max Chunks II (general) — explain stack of maxima


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 84)

# SECTION J: TRICK BANK (EXPANDED)

---

## D6. True/False: For sum of subarray mins, sorting the array first helps.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 85)

## D7. True/False: `search` can be used to implement autocomplete listing.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 86)

## D8. You pop from mono stack when `heights[stack[-1]] > h` (histogram). What if equal heights?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 87)

## D9. Interviewer: "Optimize Word Search I (single word) with a trie?"


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 88)

## D10. Can contribution technique compute sum of subarray GCDs easily?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 89)

## D11. StockSpanner: is worst-case single `next` O(n)?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 90)

## D12. Fenwick for "subarray sum equals k" on static array?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 91)

# SECTION K: CUMULATIVE INTEGRATION (M4–M10)

---

## K1. Daily temperatures + stock span: write both signatures and one shared insight.


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 92)

## K2. Sliding window max (M4) → longest max−min ≤ limit (M10). What was added?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 93)

## K3. Histogram (M4) → maximal rectangle (M10). What was added?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 94)

## K4. Hash set dictionary vs trie replace-words — when hash wins?


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 95)

## K5. Prefix+hash subarray sum vs Fenwick — classify three prompts.

| Prompt | Tool |
|---|---|
| Count subarrays sum=k, array fixed | Prefix+hash |
| Mutable array, sum ranges | Fenwick |
| Max in sliding window | Mono deque |

---

# SECTION L: BLINDED MINI TIMED SET (ANSWERS)

Do in 40 min, then check.

### L1. Implement startsWith only (no search) — still need is_end?  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 96)

### L2. Remove k digits `"10"`, k=2 →  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 97)

### L3. Sum subarray mins `[1]` →  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 98)

### L4. Window max nums=`[1,3,-1,-3,5,3,6,7]`, k=3 →  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 99)

### L5. Trie after insert `"a"`, search `""` →  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 100)

### L6. Exposure: static 1e5 range sums — structure?  

> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 101)

# SECTION M: SCORING RUBRIC FOR THIS GRILL

| Band | Meaning |
|---|---|
| ≥90% A + solid B + ≥10/14 C | Strong — proceed to timed verify |
| 75–89% | Shaky topics → ledger downgrade + drill |
| <75% | Re-teach weak half (trie vs mono) before timed |

**Fenwick subsection:** Score separately as exposure — missing segtree code ≠ fail Module 10.

---

*End of Module 10 Retention (expanded).*

---

# SECTION O: ADDITIONAL FULL-ANSWER PROBLEMS (C25–C36)

---

## C25. Implement Trie — array[26] children variant


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 102)

## C26. WordDictionary — full code


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 103)

## C27. Replace Words — hash-prefix alternate + trie compare


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 104)

## C28. Sum of Subarray Minimums — full code again with MOD


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 105)

## C29. Remove K Digits — `"10001"`, k=4


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 106)

## C30. StockSpanner stream `[71,71,71]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 107)

## C31. Longest subarray max−min ≤ limit — `[10,1,2,4,7]`, limit=5


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 108)

## C32. Max Chunks `[1,0,2,3,4]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 109)

## C33. Histogram `[2,1,5,6,2,3]` → 10


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 110)

## C34. Asteroids `[8,-8]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 111)

## C35. 132 pattern `[1,2,3,4]` / `[3,1,4,2]`


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 112)

## C36. Fenwick NumArray — implement class


> **Answer key:** `Retention Questions/keys/Module 10 Retention.keys.md` (block 113)

# SECTION P: ORAL TEACH-BACK RUBRIC (M10)

Score yourself 1–5 on each:

| Topic | 1–5 |
|---|---|
| Trie is_end vs startsWith | |
| Wildcard DFS | |
| Word Search II prune | |
| Contribution + ties | |
| Remove k digits greedy | |
| Stock span amortized | |
| Dual deque window | |
| Fenwick when/why (exposure) | |

Average ≥4 before timed verify.

---

# SECTION Q: ERROR-TAG PRACTICE

For each wrong answer in this grill, force a tag:

| Miss | Tag | Fix |
|---|---|---|
| Forgot is_end | knowledge-gap | Re-draw trie |
| Off-by-one window | careless-slip | Trace left/right |
| Used segtree for window max | knowledge-gap | Mono deque drill |
| Ran out of time on SOASM | time-pressure | Span drills first |
| Misread shortest vs longest root | misread | Restate ritual |

---

*End of Module 10 Retention (expanded).*
