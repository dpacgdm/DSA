# Phase A — Interview DSA Mastery

FAANG-style coding interview curriculum: frameworks first, evidence gates, spaced retention, timed transfer.

**Not** a guarantee of offers. Success = gates G1–G7 in [`Handoff Doc.md`](Handoff%20Doc.md).

---

## Day 1 path

1. Read this README + [`Phase A Curriculum Index.md`](Phase%20A%20Curriculum%20Index.md)  
2. Skim governance: status enum + gates in [`Handoff Doc.md`](Handoff%20Doc.md) §2A–2B  
3. Start **Module 1**:
   - [`Big O & Complexity Analysis.md`](Big%20O%20%26%20Complexity%20Analysis.md)
   - [`Arrays/Arrays.md`](Arrays/Arrays.md) *(canonical — do **not** also grind archived `Arrays/Arrays&Strings.md`)*
4. Teach-back prompts at end of lesson → [`Retention Questions/Week 1.md`](Retention%20Questions/Week%201.md) **blind**  
5. Grade with [`Retention Questions/keys/`](Retention%20Questions/keys/)  
6. Drill [`Practice Spines/Phase A MVP Spines.md`](Practice%20Spines/Phase%20A%20MVP%20Spines.md) § Module 1  
7. Local red/green: `python problem-bank/run_all.py` (74 problems) · progress: `Metrics/Spine Tracker.md`  
8. Log timed work: `python tools/scoreboard_update.py` · spaced plan: `python tools/spaced_drill.py --write`

---

## Lesson contract (every module)

| Block | Role |
|---|---|
| Framework / recipe | Memorize cold |
| 2–3 traced exemplars | In-lesson only |
| Cheat sheet + traps | Reference |
| Teach-back | Before retention |
| Retention (questions-only) | Blind grill |
| Keys | `Retention Questions/keys/` |
| Spine | Timed / MVP list |
| Bank | Executable subset |

---

## Map

| Need | Open |
|---|---|
| Module order | `Phase A Curriculum Index.md` |
| Problem lists | `Practice Spines/Phase A MVP Spines.md` |
| Timed protocol | `Practice/Timed Transfer Protocol.md` |
| Unlabeled sets | `Practice/Unlabeled Timed Sets/` |
| Mocks | `Gauntlet/Phase A Gauntlet.md` |
| Templates | `Templates/python_templates.py` |
| Metrics | `Metrics/ledger.json`, `Metrics/scoreboard.json` |

---

## Must-know coverage notes (post-9.5 pass)

- **0-1 BFS** — `Graphs/Graphs II.md` Part 2B + bank `25_zero_one_bfs`  
- **Tree DP** — `Trees/Binary Trees.md` Part 9B  
- **LRU full** — `Design/Design Data Structures.md` Part 15 + bank `26_lru_cache`  
- **Serialize** — Trees Part 9 (preorder + BFS protocols)  
- Bitwise / Matrix — **canonical modules**, not Arrays bolt-ons
- **Digit DP + Bitmask DP** — `Dynamic Programming/DP II.md`
- **Chill Interview gaps** — TTL cache, rate limiter, Simplify Path, interval intersection, Longest Increasing Path
- Giants deflated — Hashing / Recursion exemplars capped; **Advanced Hashing / Advanced Recursion archived stubs**  

---

## Language

Phase A is **Python**. Phase B (CP) / Phase C (System Design) are deferred tracks in the Handoff.

---

## Spine / bank honesty (gate rule)

Local bank covers **~45%** of spine rows. That is **not** full coverage.

- `timed-verified` for a module requires clearing that module's **gate spine** (see `Practice Spines/Phase A MVP Spines.md` + `Metrics/spine_tracker.json`).
- Rows with `in_bank: true` → prefer `problem-bank/`.
- Rows with `in_bank: false` → **LC-required**; must be logged on the scoreboard before claiming the module timed gate.
- Run `python tools/spine_status.py --gate` before declaring a module `timed-verified`.

