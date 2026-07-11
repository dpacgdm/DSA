# PHASE A AUDIT LOG

**Protocol:** `QA/Battle Test Protocol.md`  
**Pass date:** 2026-07-09  
**Scope:** Spot-check of named high-risk claims (not a full line-by-line of every lesson).

---

## FINDINGS SUMMARY

| # | Claim | File | Result | Fix applied? |
|---|---|---|---|---|
| 1 | Binary Search mid formulas | `Searching & Sorting/Binary Search.md` | **OK** | N |
| 2 | Master Theorem cases summary | `Searching & Sorting/Sorting.md` | **FIX NEEDED** → fixed | **Y** |
| 3 | Dijkstra lazy heap note | `Graphs/Graphs II.md` | **OK** | N |
| 4 | DP coin change impossible case | `Dynamic Programming/DP I.md` | **OK** | N |
| 5 | Floyd cycle | `Linked Lists/Linked Lists.md` | **FIX NEEDED** → fixed | **Y** |

---

## Detailed findings

### 1. Binary Search mid formulas — OK

**File:** `Searching & Sorting/Binary Search.md` (§1B–1D, templates)

**Checked:**
- Primary formula `mid = lo + (hi - lo) // 2` used consistently in inclusive and exclusive templates
- Python overflow note correct (arbitrary precision; safe form still taught for habit / other languages)
- Inclusive vs exclusive update table present; mixing warned as infinite-loop source
- Progress guarantee checklist present

**Result:** **OK** — no edit required.

---

### 2. Master Theorem cases summary — FIX NEEDED (fixed)

**File:** `Searching & Sorting/Sorting.md` (§3B cases + §3L drill)

**Checked:**
- Cases 1/2/3 CLRS-style comparison of `log_b a` vs `c` — **correct**
- Extended case 2 and failure modes — **correct**
- §3L item 2 contained draft self-talk: `Θ(n³ log n)? Wait c=3…` / `Actually f=n³…` — **noise / unprofessional for ≥95% craft floor**; answer itself was right (Case 2 → Θ(n³ log n))

**Result:** **FIX NEEDED**  
**Fix applied:** Cleaned §3L item 2 to a single clean Case 2 line + parenthetical (removed "Wait" / "Actually" draft phrasing).

---

### 3. Dijkstra lazy heap note — OK

**File:** `Graphs/Graphs II.md` (§3B Binary-Heap Dijkstra)

**Checked:**
- Lazy Dijkstra defined: push improved `(nd, v)` without decrease-key; skip when `d > dist[u]` on pop
- Complexity stated as O((V+E) log V) interview bound with duplicate entries noted
- Negative-weight failure explained separately (Part 4)
- Memorize snippet includes stale-entry `continue`

**Result:** **OK** — no edit required.

---

### 4. DP coin change impossible case — OK

**File:** `Dynamic Programming/DP I.md` (Classic 4 + Problem 4)

**Checked:**
- Problem statement: −1 if impossible
- `INF = amount + 1`; init; `dp[0]=0`; return `-1` when still INF
- Explicit impossible trace: `coins=[2], amount=3` → `dp[3]` stays ∞ → −1
- Trap list mentions using 0 as impossible sentinel

**Result:** **OK** — no edit required.

---

### 5. Floyd cycle — FIX NEEDED (fixed)

**File:** `Linked Lists/Linked Lists.md` (Pattern 2 + Problem 2)

**Checked:**
- Detect cycle + find entrance algorithms — **correct**
- Identity vs value trap — **correct**
- Worked traces (including entrance) — **correct**
- Math sketch was vague: `L + k = mC related distances` — **too hand-wavy for interview defense**

**Result:** **FIX NEEDED**  
**Fix applied:** Replaced math sketch with standard modular argument: slow travels L+a, fast 2(L+a) ⇒ L ≡ −a (mod C); reset-to-head walk meets at entrance.

---

## Follow-ups (not blocking this pass)

| Item | Notes |
|---|---|
| Expand problem-bank coverage | `problem-bank/` harness exists; few/no problem dirs yet — wire BS / coin / Floyd when bank grows |
| Practice Spines | Folder present; populate per-module unlabeled lists and point `ledger.json` hints at real files |
| Full Module 3–11 line audit | Schedule later; this log is the named spot-check only |

---

*Next audit: after major lesson edits or student-found contradictions.*


---

## 2026-07-11 — Pedagogy / coverage 9.5 pass

**Scope:** Structural craft + coverage holes (approved plan D1–D6).

| Change | Result |
|---|---|
| Arrays dual-lesson | `Arrays&Strings.md` archived; Arrays stripped matrix/bitwise dups; Part 10 capped at 3 exemplars (~3653→~1974 lines) |
| Big O / DP I | Chat residue removed; DP I Part 32 checklist fixed (was Graphs II paste) |
| Retention keys | Split to `Retention Questions/keys/` |
| Must-add | 0-1 BFS (Graphs II), Tree DP (Trees 9B), LRU full (Design 15), serialize BFS protocol |
| Spines | M5/M7/M8/Math/Matrix/Strings aligned; Count of Range Sum / Tarjan demoted |
| Bank | +`25_zero_one_bfs`, +`26_lru_cache` (26/26 green) |
| Ledger | Seeded M3–M11 + coverage subskills |
| Entry | Root `README.md` + unlabeled timed stubs |

**Follow-ups:** Continue deflating Hashing/Recursion in-lesson banks; expand bank toward full spine; full line audit still not claimed as ≥95% craft.
