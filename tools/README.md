# Tools — Phase A DSA

Windows-friendly Python 3 helpers. Prefer the launcher:

```text
py -3 tools/<script>.py …
```

Repo root is detected from the script location; run from anywhere.

---

## `spaced_drill.py` — today's spaced drill plan

**Reads:** `Metrics/ledger.json` (preferred) or best-effort parse of `Metrics/Retention Ledger.md`.  
**Writes (optional):** `Metrics/drill_plan_latest.md`

```text
py -3 tools/spaced_drill.py
py -3 tools/spaced_drill.py --write
py -3 tools/spaced_drill.py --date 2026-07-15 --limit 8 --write
py -3 tools/spaced_drill.py --from-md --write
```

| Flag | Meaning |
|---|---|
| `--write` | Also save `Metrics/drill_plan_latest.md` |
| `--date YYYY-MM-DD` | Override "today" for due checks |
| `--limit N` | Max subskills in the plan (default 10) |
| `--from-md` | Force parse the markdown ledger |
| `--json-out` | Print selected rows as JSON after the markdown |

**Priority:** due `weak` → due `shaky` → due `strong`, then suggests Practice Spine pulls for modules touched.

**After drilling:** edit `Metrics/ledger.json` (`heat`, `last_pass`, `next_due`, `fail_count`). Keep `Retention Ledger.md` in sync when you want a human-readable mirror.

---

## `scoreboard_update.py` — timed / mock logging

**Source of truth:** `Metrics/scoreboard.json`  
**Regenerates:** `Metrics/Scoreboard.md`

### Timed set

```text
py -3 tools/scoreboard_update.py timed --module 3 --duration 60 --problems 4 --blind Y --first-pass 3 --hints N --difficulty medium --screen Y --notes "BS + sort"
```

### Mini-mock

```text
py -3 tools/scoreboard_update.py mock --after-module 4 --duration 45 --clarity 4 --correctness 5 --complexity 4 --code 4 --recovery 3 --notes "Mini-mock #1"
```

### Error tag / redo / regen

```text
py -3 tools/scoreboard_update.py error --problem "LC 322" --type knowledge-gap --fix "Re-teach INF sentinel"
py -3 tools/scoreboard_update.py redo --problem "LC 200" --failed-on 2026-07-01 --due 2026-07-09
py -3 tools/scoreboard_update.py regen
```

Error `--type` must be one of: `knowledge-gap`, `misread`, `time-pressure`, `careless-slip`.

Rolling G3/G4/G5/G7 fields are recomputed on every write. G1/G2 remain manual in the JSON until learner evidence is logged.

---

## Related docs

| Doc | Role |
|---|---|
| `Practice/Timed Transfer Protocol.md` | Weekly timed blocks + screen-pass rubric |
| `QA/Battle Test Protocol.md` | Pressure-test lessons |
| `Metrics/Retention Ledger.md` | Human ledger mirror |
| `Handoff Doc.md` | Gates G1–G7 |
| `Gauntlet/Phase A Gauntlet.md` | Mocks + mixed sets |

## Spine coverage

```bash
python tools/spine_status.py
```
