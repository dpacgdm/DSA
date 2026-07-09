# TIMED TRANSFER PROTOCOL — PHASE A

**Purpose:** Turn untimed "explain everything" practice into **blind transfer under clock pressure** — the skill that actually shows up in screens.  
**Governance:** Chat-guided solves ≠ timed credit. Log every block. See Handoff gates **G3 / G4 / G5 / G7**.  
**Gauntlet:** Full mocks and mixed sets live in [`Gauntlet/Phase A Gauntlet.md`](../Gauntlet/Phase%20A%20Gauntlet.md).  
**Logging:** Prefer `py -3 tools/scoreboard_update.py timed …` → `Metrics/scoreboard.json` + regenerated `Metrics/Scoreboard.md`.

---

## 1. Weekly timed block templates

Pick one primary block per week once Module 3+ is in play. Add a second block only if energy is high — quality of blindness beats volume.

### 45-minute screen block (default weekly)

| Segment | Minutes | What |
|---|---|---|
| Setup | 2 | Timer on; problem list sealed; no notes / no lesson tabs |
| Problem 1 (medium) | 20 | Restate → approach → code → trace |
| Problem 2 (medium) | 20 | Same; if stuck >3 min with no progress, mark and move |
| Buffer / second-pass | 3 | Fix one known bug only if time remains |
| Log | after | Scoreboard fields below; tag misses |

**Target:** 2 mediums, first-pass correct on ≥1 without hints. Stretch: both.

### 60-minute module verify (gate toward `timed-verified`)

| Segment | Minutes | What |
|---|---|---|
| Setup | 2 | Blind; module-appropriate mix only (earned patterns) |
| Problems | 50 | 3 mediums **or** 2 mediums + 1 hard |
| Close | 8 | Trace edges on finished code; no new problems |
| Log | after | Full scoreboard row + error tags |

### 90-minute transfer / mock-adjacent

| Segment | Minutes | What |
|---|---|---|
| Setup | 3 | Talk-aloud optional (counts toward mock skill if narrated) |
| Block A | 40 | 2 mediums |
| Short break | 5 | Stand up; **do not** open solutions |
| Block B | 40 | 1 hard **or** 2 mediums from a *different* module family |
| Log | after | Two scoreboard rows or one combined note |

Use 90-min when preparing for Gauntlet mocks or after Module 6+.

---

## 2. How to log to the scoreboard

### Required fields (timed set)

| Field | Meaning |
|---|---|
| `date` | YYYY-MM-DD |
| `module` | Primary module number (or lowest module in a mixed set) |
| `duration_min` | Clock time (45 / 60 / 90) |
| `problems` | Count attempted under timer |
| `difficulty` | `easy` / `medium` / `hard` / `mixed` (use `medium`/`hard` for G3/G4 windows) |
| `blind` | `Y` if no notes, no pattern labels, no lesson open |
| `first_pass_correct` | Count correct **before** any hint or solution peek |
| `hints` | `Y` if any hint / solution / AI assist during the block |
| `would_pass_screen` | `Y`/`N` — see rubric below |
| `notes` | Patterns, fails, redo candidates |

### CLI

```text
py -3 tools/scoreboard_update.py timed --module 3 --duration 60 --problems 3 --blind Y --first-pass 2 --hints N --difficulty medium --screen Y --notes "BS bounds + merge"
```

### Mock fields (G5)

Clarity / Correctness / Complexity / Code / Recovery (each 1–5), `after_module`, `duration_min`, average auto-computed. See Gauntlet rubric.

### Miss tagging (G7)

Every timed miss → one of: `knowledge-gap` | `misread` | `time-pressure` | `careless-slip`.

```text
py -3 tools/scoreboard_update.py error --problem "LC 33" --type misread --fix "Restate rotated-array invariant first"
```

---

## 3. Screen-pass rubric (would this pass a 45-min screen?)

Mark **`would_pass_screen = Y`** only if **all** of the following are true for the block as a whole:

1. **Blind** — no notes, no labeled "this is sliding window," no lesson open.
2. **Communication** — restated problem + complexity spoken (even if solo: out loud or written in 4–6 lines).
3. **Correctness bar** — at least one medium fully correct with edges traced, **or** two mediums substantially correct with only minor slips.
4. **Time** — finished coding with ≥3 minutes left to trace, **or** recovered a bug without opening solutions.
5. **No fatal process fail** — did not freeze >8 minutes with zero progress and no smaller example; did not paste a memorized solution you cannot explain.

If you needed a hint for the core idea → **N**, even if the code eventually passed tests.

---

## 4. Module-by-module timed blueprints

Counts are **targets**, not quotas. Difficulty mix assumes earned patterns only.

| Module | Duration | Problem count | Difficulty mix | Focus |
|---|---|---|---|---|
| 1 | 45 | 2 | 2 medium | Window / two pointers / prefix; complexity talk |
| 2 | 45–60 | 2–3 | 2M or 2M+1 easy | Hash + recursion/memo; no graph PREVIEW credit |
| 3 | 60 | 3 | 2M + 1M/H | BS templates + one sort/MT verbal or Count of Range Sum when earned |
| 4 | 60 | 3 | 2M + 1M | LL + stack/queue; one monotonic **intro** problem |
| 5 | 60 | 3 | 2M + 1H | Tree recursion + one BST |
| 6 | 60–90 | 3–4 | 2M + 1H | Heap top-K + advanced window |
| 7 | 60–90 | 3–4 | 2M + 1H | BFS/DFS/topo; Word Ladder / Alien when earned |
| 8 | 60–90 | 3 | 2M + 1H | Dijkstra/DSU **or** 1D DP |
| 9 | 60–90 | 3–4 | 2M + 1H | 2D DP / backtracking / greedy judgment |
| 10 | 60 | 2–3 | 2M + optional H | Trie **or** monotonic deep-dive (not both cold) |
| 11 | 90+ | Gauntlet | Mixed | Follow [`Gauntlet/Phase A Gauntlet.md`](../Gauntlet/Phase%20A%20Gauntlet.md) |

Pull unlabeled prompts from Practice Spines / retention timed sections / Gauntlet — never from a list that names the pattern in the title during the timed block.

---

## 5. Anti-cheating rules for self-timing

These exist so the scoreboard means something.

1. **Timer starts before you read the full prompt** (title + first sentence OK; no scrolling solutions).
2. **No pattern labels** on the problem sheet during the block.
3. **No lesson / chat / editorial** until the timer ends — even to "check one API."
4. **No pausing** for research. Bathroom pause: stop the problem, don't open materials.
5. **Hints count** — any external idea = `hints=Y` and that problem is not first-pass.
6. **Same-day retry** after peeking is **drill**, not timed credit. Re-queue ≥7 days for G6 redo.
7. **Don't inflate `first_pass_correct`** — if tests failed until you fixed a logic bug after peeking at expected output, it is not first-pass.
8. **Solo talk-aloud** is encouraged; silent perfect coding with notes open is not a screen pass.

---

## 6. Link to Gauntlet & drills

| Resource | Use |
|---|---|
| [`Gauntlet/Phase A Gauntlet.md`](../Gauntlet/Phase%20A%20Gauntlet.md) | Full mocks, mixed sets, declaration checklist |
| `py -3 tools/spaced_drill.py --write` | Due subskills before a timed block |
| `Practice Spines/` | Unlabeled problem sources by module |
| `QA/Battle Test Protocol.md` | When a lesson claim feels soft — pressure-test it |

---

*Timed transfer is a habit. One honest 45-minute block beats three compromised hours.*
