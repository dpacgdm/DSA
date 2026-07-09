# BATTLE TEST PROTOCOL — LESSON QA

**Purpose:** Pressure-test Phase A lessons before trusting them under interview fire.  
**Craft floor:** ≥95% (Handoff). Answer keys in retention files are **intentionally kept** for self-grade — battle tests check lessons + keys for correctness, not whether keys exist.  
**Audit log:** Record passes in `QA/Phase A Audit Log.md`.

---

## 1. When to battle-test

- After writing or heavily editing a lesson
- Before raising content status psychologically to "shipped"
- When a student challenge exposes a soft claim
- Spot-check cadence: at least one claim family per module family (see audit log)

---

## 2. Student challenge checklist

Run as if a sharp student is attacking the lesson. Check each box.

| # | Challenge | Pass if… |
|---|---|---|
| 1 | "Show me the framework before examples." | Mechanical steps exist, not only demos |
| 2 | "What breaks this?" | Failure modes / traps section present |
| 3 | "Say the interview line." | 1–3 spoken pitches exist |
| 4 | "Python trap?" | Language-specific footguns named |
| 5 | "Complexity — why?" | T/S with justification, not bare O(·) |
| 6 | "Is this PREVIEW?" | Cross-module tools labeled; no false mastery |
| 7 | "Trace this." | At least one full worked trace |
| 8 | "Wrong mid / sentinel / identity?" | Classic bugs called out (BS mid, DP INF, `is` vs `==`) |
| 9 | "Where does this live vs later module?" | Ownership clear (e.g. monotonic M4 vs M10) |
| 10 | "Would this survive a 45-min screen?" | Enough to attempt blind; not tutorial-only |

---

## 3. Correctness checks against problem-bank

When `problem-bank/problems/<slug>/` exists:

```text
py -3 problem-bank/harness.py
# or per-problem as documented in harness
```

| Check | Action |
|---|---|
| Reference `solution.py` matches lesson snippet | Diff critical loops / base cases |
| `test_cases.py` covers impossible / empty / single | Lesson must mention the same edges |
| Lesson claims complexity | Agree with implementation |
| Lesson "return −1 if impossible" | Sentinel in code matches narrative |

If no bank entry yet: manually execute the lesson's primary snippet on 2 happy + 2 edge cases.

---

## 4. Trap audits (high-frequency interview landmines)

| Family | Must verify in lesson |
|---|---|
| Binary search | `mid = lo + (hi-lo)//2`; inclusive vs exclusive updates never mixed |
| Master Theorem | Three cases + when MT fails; single home = Sorting (M3) |
| Dijkstra | Lazy heap / stale skip; non-negative assumption |
| DP coin change | INF sentinel; impossible → −1; unbounded loop order |
| Floyd cycle | Identity compare; entrance reset math |
| Monotonic | M4 intro vs M10 deep dive ownership |
| Hash / prefix | Mod negative in Python; collision honesty |
| Recursion | Stack space; MT not claimed complete in M2 |

---

## 5. Retention key integrity

Answer keys stay in retention files **on purpose** (self-study + tutor grade). Battle-test keys by:

1. Solving 2 random problems blind yourself
2. Comparing to key — flag any wrong expected answer as **FIX NEEDED**
3. Never "fixing" by deleting keys

---

## 6. Output format

Append to `QA/Phase A Audit Log.md`:

```text
### YYYY-MM-DD — <topic>
- Claim: …
- File: `path`
- Result: OK | FIX NEEDED
- Notes: …
- Fix applied: Y/N (link commit / describe edit)
```

---

## 7. Severity

| Result | Meaning |
|---|---|
| **OK** | Claim accurate; examples consistent |
| **FIX NEEDED** | Error, draft noise, or misleading math — edit lesson before relying on it |
| **DEFER** | Real gap but explicitly out of Phase A scope — document, don't silently omit |
