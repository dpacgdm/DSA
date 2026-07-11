# Spine Tracker

SoT: `Metrics/spine_tracker.json` · CLI: `python tools/spine_status.py --gate`

## Honesty

Local bank ≠ full spine. Claiming `timed-verified` without clearing **gate_required** rows (bank **or** LC-logged) is a status lie.

| Metric | Value |
|---|---|
| Spine rows | 218 |
| In local bank | 97 (44%) |
| Gate-required rows | 205 |
| Gate-required with bank | 97 (47%) |

### Status enum (per row)

`not-started` → `drilled` → `bank-passed` *or* LC logged as `timed-passed` → done for gate.

Optional rows (`gate_required: false`): may stay `not-started` without blocking the module gate.
