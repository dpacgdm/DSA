# PHASE A — CURRICULUM INDEX (CONTENT DELIVERED)

**Delivered:** 2026-07-09  
**Updated:** 2026-07-09 — tools, timed protocol, QA, machine-readable metrics  
**Mode:** Teacher-side complete. Learner gates (timed / retention pass / mocks) remain for when practice resumes.  
**Content craft target:** ≥95%  
**Answer keys:** Retention files **intentionally keep** full answer keys for self-grade / tutor sessions (not removed).

This index is the map. Study in module order.

---

## Module 1 — Complexity + Arrays & Strings

| Material | Path |
|---|---|
| Lesson | `Big O & Complexity Analysis.md` |
| Lesson | `Arrays/Arrays.md` |
| Lesson | `Arrays/Arrays&Strings.md` |
| Retention | `Retention Questions/Week 1.md` |
| Spine | `Practice Spines/Phase A MVP Spines.md` § Module 1 |

## Module 2 — Hashing + Recursion

| Material | Path |
|---|---|
| Lesson | `Hashing/Hash maps&sets.md` |
| Lesson | `Hashing/Advanced Hashing.md` |
| Lesson | `Recursion/Recursion.md` |
| Lesson | `Recursion/Advanced Recursion.md` |
| Drill | `Retention Questions/Week 2 Drilling Set.md` (PREVIEW: #7, #11, #12) |
| Retention | `Retention Questions/Module 2 Retention.md` |

## Module 3 — Searching & Sorting

| Material | Path |
|---|---|
| Lesson | `Searching & Sorting/Binary Search.md` |
| Lesson | `Searching & Sorting/Sorting.md` (**Master Theorem home**) |
| Retention | `Retention Questions/Module 3 Retention.md` |
| Re-credit | Count of Range Sum (earned in Sorting + M3 retention) |

## Module 4 — Linked Lists + Stacks & Queues

| Material | Path |
|---|---|
| Lesson | `Linked Lists/Linked Lists.md` |
| Lesson | `Stacks & Queues/Stacks & Queues.md` (monotonic **intro**) |
| Retention | `Retention Questions/Module 4 Retention.md` |
| Ownership | `QA/Monotonic Ownership.md` |
| Mocks | First mini-mock protocol in `Gauntlet/Phase A Gauntlet.md` |

## Module 5 — Trees

| Material | Path |
|---|---|
| Lesson | `Trees/Binary Trees.md` |
| Lesson | `Trees/Binary Search Trees.md` |
| Retention | `Retention Questions/Module 5 Retention.md` |

## Module 6 — Heaps + Advanced Array Patterns

| Material | Path |
|---|---|
| Lesson | `Heaps/Heaps & Priority Queues.md` |
| Lesson | `Arrays/Advanced Patterns.md` |
| Retention | `Retention Questions/Module 6 Retention.md` |

## Module 7 — Graphs I

| Material | Path |
|---|---|
| Lesson | `Graphs/Graphs I.md` |
| Retention | `Retention Questions/Module 7 Retention.md` |
| Re-credit | Word Ladder + Alien Dictionary (earned in Graphs I) |

## Module 8 — Graphs II + DP I

| Material | Path |
|---|---|
| Lesson | `Graphs/Graphs II.md` |
| Lesson | `Dynamic Programming/DP I.md` |
| Retention | `Retention Questions/Module 8 Retention.md` |

## Module 9 — DP II + Backtracking + Greedy

| Material | Path |
|---|---|
| Lesson | `Dynamic Programming/DP II.md` |
| Lesson | `Backtracking/Backtracking & Greedy.md` |
| Retention | `Retention Questions/Module 9 Retention.md` |

## Module 10 — Advanced Structures

| Material | Path |
|---|---|
| Lesson | `Advanced/Tries & Monotonic.md` (monotonic **deep dive**) |
| Lesson | `Advanced/Segment & Fenwick Exposure.md` (exposure, not mastery) |
| Retention | `Retention Questions/Module 10 Retention.md` |
| Ownership | `QA/Monotonic Ownership.md` |

## Module 11 — Gauntlet (Phase A close)

| Material | Path |
|---|---|
| Gauntlet | `Gauntlet/Phase A Gauntlet.md` |
| Final assessment | `Retention Questions/Module 11 Final Assessment.md` |

---

## Coverage modules (interview gaps closed)

Schedule after Module 3–6 foundations (or interleaved). Full lessons + shared retention.

| Material | Path |
|---|---|
| Intervals & Sweep Line | `Intervals/Intervals & Sweep Line.md` |
| Bit Manipulation | `Bitwise/Bit Manipulation.md` |
| String Algorithms (KMP/Z/hash) | `Strings/String Algorithms.md` |
| Math for Interviews | `Math/Math for Interviews.md` |
| Matrix & Grid Patterns | `Matrix/Matrix & Grid Patterns.md` |
| Design Data Structures | `Design/Design Data Structures.md` |
| Retention (all six) | `Retention Questions/Coverage Gaps Retention.md` |

## Practice, tools, QA

| Area | Path | Role |
|---|---|---|
| Timed transfer | `Practice/Timed Transfer Protocol.md` | 45/60/90 templates, screen-pass rubric, anti-cheat, module blueprints |
| MVP spines | `Practice Spines/Phase A MVP Spines.md` | 15–25 problems per module + coverage spine |
| Problem bank | `problem-bank/` | 24 executable problems, 133 tests (`py -3 run_all.py`) |
| Debugging pedagogy | `Debugging/Debugging Diagnosis.md` | Taxonomy + diagnosis trees + failed-case walkthroughs |
| Templates (prose) | `Templates/Interview Templates.md` | Hygiene + how to use shells |
| Templates (code) | `Templates/python_templates.py` | Copy-paste BS/window/BFS/UF/Dijkstra/DP/backtrack/trie/LL/heap/mono |
| Spaced drill tool | `tools/spaced_drill.py` | Due/weak plan → `Metrics/drill_plan_latest.md` |
| Scoreboard tool | `tools/scoreboard_update.py` | Append timed/mock → JSON + regen MD |
| Tools docs | `tools/README.md` | Usage |
| Battle-test QA | `QA/Battle Test Protocol.md` | Pressure-test lessons |
| Audit log | `QA/Phase A Audit Log.md` | Spot-check findings + fixes |
| Monotonic ownership | `QA/Monotonic Ownership.md` | M4 intro vs M10 deep dive |

---

## Governance & metrics

| File | Role |
|---|---|
| `Handoff Doc.md` | Source of truth: goals, gates, status enum, decision log |
| `Metrics/Scoreboard.md` | Human scoreboard (generated from JSON) |
| `Metrics/scoreboard.json` | Machine-readable timed / mock / gate data |
| `Metrics/Retention Ledger.md` | Human spaced heat map |
| `Metrics/ledger.json` | Machine-readable ledger (drill generator SoT) |

---

## Suggested self-study order (no tutor required)

For each module M3→M11:
1. Read lesson(s) end-to-end  
2. Re-derive frameworks on paper  
3. Attempt retention **without** looking at answers  
4. Grade against answer key (keys are kept on purpose)  
5. Update `Metrics/ledger.json` / Retention Ledger; log timed work via `tools/scoreboard_update.py`  
6. Run `py -3 tools/spaced_drill.py --write` for due review  
7. Timed blind set per `Practice/Timed Transfer Protocol.md` / Gauntlet  

Phase A **learner-ready declaration** still requires gates G1–G7 in the Handoff — content delivery ≠ gate pass.
