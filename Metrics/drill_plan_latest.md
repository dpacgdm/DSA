# DRILL PLAN — 2026-07-09

**Generated:** 2026-07-09 23:48
**Source:** `Metrics/ledger.json`
**Rule:** Weak/due first; mix review + Practice Spine pulls. Chat-guided != timed credit.

## Due snapshot

| Heat due | Count |
|---|---|
| weak | 2 |
| shaky | 13 |
| strong | 7 |
| not due (pool) | 0 |

## Today's prioritized subskills

| # | Module | Subskill | Heat | Next due | Fail | Action |
|---|---|---|---|---|---|---|
| 1 | M2 | Backtracking skeleton | weak | 2026-07-09 | 0 | RE-TEACH then quiz |
| 2 | M2 | Rolling hash exposure | weak | 2026-07-09 | 0 | RE-TEACH then quiz |
| 3 | M1 | Dependent nesting (sum / harmonic) | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 4 | M1 | Hidden costs (Python ops) | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 5 | M1 | In-place techniques | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 6 | M1 | Interview complexity communication | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 7 | M1 | Sliding window | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 8 | M2 | Base / recursive / combine | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 9 | M2 | Call stack space | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |
| 10 | M2 | Dict/set Python semantics | shaky | 2026-07-09 | 0 | Short quiz / 1 problem |

## Practice Spine pulls (suggested)

- Module 1: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 1`
- Module 2: pull 1–2 problems from `Practice Spines/Phase A MVP Spines.md § Module 2`

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
