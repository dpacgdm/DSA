# DRILL PLAN — 2026-07-11

**Generated:** 2026-07-11 09:35
**Source:** `Metrics/ledger.json`
**Rule:** Weak/due first; mix review + Practice Spine pulls. Chat-guided != timed credit.

## Due snapshot

| Heat due | Count |
|---|---|
| weak | 35 |
| shaky | 13 |
| strong | 7 |
| not due (pool) | 0 |

## Today's prioritized subskills

| # | Module | Subskill | Heat | Next due | Fail | Action |
|---|---|---|---|---|---|---|
| 1 | M2 | Backtracking skeleton | weak | 2026-07-09 | 0 | RE-TEACH then quiz |
| 2 | M2 | Rolling hash exposure | weak | 2026-07-09 | 0 | RE-TEACH then quiz |
| 3 | M3 | Binary search closed/open templates | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 4 | M3 | Binary search on answer / monotonic predicate | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 5 | M3 | Master Theorem awareness (appendix) | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 6 | M3 | Sorting stability + Python sort | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 7 | M4 | Linked list dummy head / reverse / Floyd | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 8 | M4 | Monotonic stack intro | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 9 | M4 | Sliding window maximum deque | weak | 2026-07-11 | 0 | RE-TEACH then quiz |
| 10 | M5 | BST invariant + validate + LCA | weak | 2026-07-11 | 0 | RE-TEACH then quiz |

## Practice Spine pulls (suggested)

- Module 2: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 2`
- Module 3: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 3`
- Module 4: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 4`
- Module 5: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 5`

## Session recipe (30–45 min)

1. Clear **weak** due rows first (re-teach → 1 applied question).
2. Hit **shaky** due rows (recall + one short problem).
3. Pull 1–2 unlabeled problems from the Practice Spine paths above.
4. Optional: one timed mini-block per `Practice/Timed Transfer Protocol.md`.
5. Update `Metrics/ledger.json` heats + `next_due`; log timed work via `tools/scoreboard_update.py`.

## After the session

- Pass → upgrade heat / push `next_due` by interval in ledger.json
- Fail → downgrade heat, bump `fail_count`, shorten `next_due`
- Retention grill still must pull due ledger rows (Handoff §2C)
