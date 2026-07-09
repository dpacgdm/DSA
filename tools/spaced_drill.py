#!/usr/bin/env python3
"""Spaced drill plan generator for Phase A DSA mastery.

Reads Metrics/ledger.json (preferred) or best-effort-parses
Metrics/Retention Ledger.md. Prints today's drill plan to stdout and
optionally writes Metrics/drill_plan_latest.md.

Usage (Windows / Python 3):
  py -3 tools/spaced_drill.py
  py -3 tools/spaced_drill.py --write
  py -3 tools/spaced_drill.py --date 2026-07-15 --limit 8 --write
  py -3 tools/spaced_drill.py --from-md   # force parse Retention Ledger.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER_JSON = ROOT / "Metrics" / "ledger.json"
LEDGER_MD = ROOT / "Metrics" / "Retention Ledger.md"
OUT_MD = ROOT / "Metrics" / "drill_plan_latest.md"


def _configure_stdio() -> None:
    """Avoid Windows cp1252 crashes on Unicode in plan text."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass

HEAT_RANK = {"weak": 0, "shaky": 1, "strong": 2, "": 3, None: 3, "—": 3}


def parse_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    s = str(value).strip()
    if not s or s.lower() in {"none", "n/a", "—", "-"}:
        return None
    # ISO first
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except ValueError:
            pass
    # Soft tokens from the human ledger
    low = s.lower()
    if "due-now" in low or "due now" in low:
        return date.today()
    if "not m2" in low or "module 3" in low:
        return None
    if "retention" in low or "drilled" in low or "week" in low or "on start" in low:
        return date.today()  # treat as due until a real pass date exists
    return None


def load_ledger_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def parse_ledger_md(path: Path) -> list[dict[str, Any]]:
    """Best-effort table parse. Returns subskill dicts compatible with JSON rows."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = []
    current_module = 0
    current_name = ""
    module_re = re.compile(r"^##\s+Module\s+(\d+)\s*[—\-]\s*(.+?)\s*$", re.I)
    # | Subskill | Heat | Last pass | Next due | Fail count | Notes |
    row_re = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*)\|?\s*$"
    )

    for line in text.splitlines():
        m = module_re.match(line.strip())
        if m:
            current_module = int(m.group(1))
            current_name = m.group(2).strip()
            continue
        if not line.strip().startswith("|"):
            continue
        if "Subskill" in line and "Heat" in line:
            continue
        if re.match(r"^\|\s*-+", line):
            continue
        rm = row_re.match(line)
        if not rm or current_module == 0:
            continue
        subskill, heat, last_pass, next_due, fail, notes = [c.strip() for c in rm.groups()]
        if subskill.lower() in {"subskill", "module"}:
            continue
        if heat in {"—", "-"} and "not" in (last_pass or "").lower():
            continue  # Master Theorem deferral row etc.
        try:
            fail_count = int(re.sub(r"[^\d-]", "", fail) or "0")
        except ValueError:
            fail_count = 0
        heat_n = heat.lower().strip() if heat else "shaky"
        if heat_n not in HEAT_RANK:
            heat_n = "shaky"
        rows.append(
            {
                "id": f"md-m{current_module}-{len(rows)}",
                "subskill": subskill,
                "module": current_module,
                "module_name": current_name,
                "heat": heat_n,
                "last_pass": last_pass if last_pass and last_pass.lower() != "none" else None,
                "next_due": next_due,
                "fail_count": fail_count,
                "notes": notes,
            }
        )
    return rows


def is_due(item: dict[str, Any], today: date) -> bool:
    nd = parse_date(item.get("next_due"))
    if nd is None:
        # No due date → due if weak/shaky with no last_pass
        if item.get("heat") in {"weak", "shaky"} and not parse_date(item.get("last_pass")):
            return True
        return False
    return nd <= today


def priority_key(item: dict[str, Any], today: date) -> tuple:
    heat = (item.get("heat") or "").lower()
    due = is_due(item, today)
    nd = parse_date(item.get("next_due")) or today
    overdue_days = (today - nd).days if due else -999
    return (
        0 if due else 1,
        HEAT_RANK.get(heat, 3),
        -overdue_days,
        -int(item.get("fail_count") or 0),
        int(item.get("module") or 99),
        item.get("subskill") or "",
    )


def spine_hint(ledger: dict[str, Any], module: int) -> str:
    hints = ledger.get("practice_spine_hints") or {}
    return hints.get(str(module), f"Practice Spines/ (module {module})")


def build_plan(
    items: list[dict[str, Any]],
    ledger: dict[str, Any],
    today: date,
    limit: int,
) -> dict[str, Any]:
    ranked = sorted(items, key=lambda x: priority_key(x, today))
    due_weak = [x for x in ranked if is_due(x, today) and (x.get("heat") or "") == "weak"]
    due_shaky = [x for x in ranked if is_due(x, today) and (x.get("heat") or "") == "shaky"]
    due_strong = [x for x in ranked if is_due(x, today) and (x.get("heat") or "") == "strong"]
    not_due = [x for x in ranked if not is_due(x, today)]

    selected: list[dict[str, Any]] = []
    for bucket in (due_weak, due_shaky, due_strong):
        for x in bucket:
            if len(selected) >= limit:
                break
            selected.append(x)
        if len(selected) >= limit:
            break

    # Ensure mix: if we filled only weak, try add 1 strong review if room
    if len(selected) < limit and due_strong:
        for x in due_strong:
            if x not in selected:
                selected.append(x)
                break

    # Warm maintenance: one not-due strong if still room and we have capacity
    if len(selected) < max(3, limit // 2) and not_due:
        for x in not_due:
            if (x.get("heat") or "") == "strong":
                selected.append(x)
                break

    modules_touched = sorted({int(x["module"]) for x in selected if x.get("module") is not None})
    spine_lines = [f"- Module {m}: pull 1–2 problems from `{spine_hint(ledger, m)}`" for m in modules_touched]

    return {
        "date": today.isoformat(),
        "selected": selected,
        "due_counts": {
            "weak": len(due_weak),
            "shaky": len(due_shaky),
            "strong": len(due_strong),
            "not_due": len(not_due),
        },
        "spine_lines": spine_lines or ["- No due modules — open Practice Spines for current learner module."],
        "limit": limit,
    }


def render_markdown(plan: dict[str, Any], source: str) -> str:
    lines = [
        f"# DRILL PLAN — {plan['date']}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Source:** `{source}`",
        f"**Rule:** Weak/due first; mix review + Practice Spine pulls. Chat-guided != timed credit.",
        "",
        "## Due snapshot",
        "",
        f"| Heat due | Count |",
        f"|---|---|",
        f"| weak | {plan['due_counts']['weak']} |",
        f"| shaky | {plan['due_counts']['shaky']} |",
        f"| strong | {plan['due_counts']['strong']} |",
        f"| not due (pool) | {plan['due_counts']['not_due']} |",
        "",
        "## Today's prioritized subskills",
        "",
        "| # | Module | Subskill | Heat | Next due | Fail | Action |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, x in enumerate(plan["selected"], 1):
        action = "RE-TEACH then quiz" if x.get("heat") == "weak" else (
            "Short quiz / 1 problem" if x.get("heat") == "shaky" else "Quick recall"
        )
        lines.append(
            f"| {i} | M{x.get('module')} | {x.get('subskill')} | {x.get('heat')} | "
            f"{x.get('next_due')} | {x.get('fail_count', 0)} | {action} |"
        )
    if not plan["selected"]:
        lines.append("| — | — | (none due) | — | — | — | Maintain current module |")

    lines += [
        "",
        "## Practice Spine pulls (suggested)",
        "",
        *plan["spine_lines"],
        "",
        "## Session recipe (30–45 min)",
        "",
        "1. Clear **weak** due rows first (re-teach → 1 applied question).",
        "2. Hit **shaky** due rows (recall + one short problem).",
        "3. Pull 1–2 unlabeled problems from the Practice Spine paths above.",
        "4. Optional: one timed mini-block per `Practice/Timed Transfer Protocol.md`.",
        "5. Update `Metrics/ledger.json` heats + `next_due`; log timed work via `tools/scoreboard_update.py`.",
        "",
        "## After the session",
        "",
        "- Pass → upgrade heat / push `next_due` by interval in ledger.json",
        "- Fail → downgrade heat, bump `fail_count`, shorten `next_due`",
        "- Retention grill still must pull due ledger rows (Handoff §2C)",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Generate today's spaced drill plan.")
    parser.add_argument("--write", action="store_true", help=f"Write {OUT_MD.relative_to(ROOT)}")
    parser.add_argument("--date", default=None, help="Override today YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=10, help="Max subskills in plan (default 10)")
    parser.add_argument("--from-md", action="store_true", help="Parse Retention Ledger.md instead of JSON")
    parser.add_argument("--json-out", action="store_true", help="Also print plan JSON to stdout after markdown")
    args = parser.parse_args(argv)

    today = parse_date(args.date) or date.today()
    ledger: dict[str, Any] = {"practice_spine_hints": {}}
    source = "Metrics/ledger.json"

    if args.from_md or not LEDGER_JSON.exists():
        items = parse_ledger_md(LEDGER_MD)
        source = "Metrics/Retention Ledger.md"
        if LEDGER_JSON.exists():
            ledger = load_ledger_json(LEDGER_JSON)
    else:
        ledger = load_ledger_json(LEDGER_JSON)
        items = list(ledger.get("subskills") or [])
        if not items:
            items = parse_ledger_md(LEDGER_MD)
            source = "Metrics/Retention Ledger.md (fallback)"

    plan = build_plan(items, ledger, today, max(1, args.limit))
    md = render_markdown(plan, source)
    if args.write:
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text(md, encoding="utf-8")
        print(f"[wrote] {OUT_MD}", file=sys.stderr)
    print(md)
    if args.json_out:
        print(json.dumps({"date": plan["date"], "selected": plan["selected"], "due_counts": plan["due_counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
