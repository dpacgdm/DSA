#!/usr/bin/env python3
"""Append timed-set or mock results into Metrics/scoreboard.json and regenerate Scoreboard.md.

Usage (Windows / Python 3):
  py -3 tools/scoreboard_update.py timed --module 3 --duration 60 --problems 4 \\
      --blind Y --first-pass 3 --hints N --difficulty medium --notes "BS + sort mix"

  py -3 tools/scoreboard_update.py mock --after-module 4 --duration 45 \\
      --clarity 4 --correctness 5 --complexity 4 --code 4 --recovery 3 \\
      --notes "Mini-mock #1"

  py -3 tools/scoreboard_update.py error --problem "LC 322" --type knowledge-gap --fix "Re-teach coin INF"

  py -3 tools/scoreboard_update.py redo --problem "LC 200" --failed-on 2026-07-01 --due 2026-07-09

  py -3 tools/scoreboard_update.py regen   # rebuild Scoreboard.md from JSON only
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SB_JSON = ROOT / "Metrics" / "scoreboard.json"
SB_MD = ROOT / "Metrics" / "Scoreboard.md"

ERROR_TYPES = {"knowledge-gap", "misread", "time-pressure", "careless-slip"}


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass


def load_sb() -> dict[str, Any]:
    if not SB_JSON.exists():
        return {
            "version": 1,
            "last_updated": date.today().isoformat(),
            "phase_a_ready": False,
            "gates": {},
            "modules": [],
            "timed_sets": [],
            "error_log": [],
            "redo_queue": [],
            "mocks": [],
            "contests": [],
        }
    with SB_JSON.open(encoding="utf-8") as f:
        return json.load(f)


def save_sb(data: dict[str, Any]) -> None:
    data["last_updated"] = date.today().isoformat()
    recompute_gates(data)
    SB_JSON.parent.mkdir(parents=True, exist_ok=True)
    with SB_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def yn(s: str) -> bool:
    return str(s).strip().upper() in {"Y", "YES", "TRUE", "1"}


def recompute_gates(data: dict[str, Any]) -> None:
    timed = data.get("timed_sets") or []
    mediums = [t for t in timed if (t.get("difficulty") or "medium").lower() == "medium"]
    hards = [t for t in timed if (t.get("difficulty") or "").lower() == "hard"]
    last20 = mediums[-20:]
    last10 = hards[-10:]

    def first_pass_rate(rows: list[dict]) -> float | None:
        if not rows:
            return None
        ok = 0
        total_probs = 0
        for r in rows:
            fp = r.get("first_pass_correct")
            n = int(r.get("problems") or 0)
            if n <= 0:
                continue
            total_probs += n
            if fp is not None:
                ok += int(fp)
        if total_probs == 0:
            return None
        return 100.0 * ok / total_probs

    m_rate = first_pass_rate(last20)
    h_rate = first_pass_rate(last10)
    gates = data.setdefault("gates", {})
    g3 = gates.setdefault("G3", {})
    g4 = gates.setdefault("G4", {})
    if m_rate is None:
        g3["current"] = "0 timed logged" if not last20 else "insufficient medium rows"
        g3["met"] = False
    else:
        g3["current"] = f"{m_rate:.0f}% of last {len(last20)} medium sets (by problem count)"
        g3["met"] = m_rate >= 70.0

    if h_rate is None:
        g4["current"] = "0 timed logged" if not last10 else "insufficient hard rows"
        g4["met"] = False
    else:
        g4["current"] = f"{h_rate:.0f}% of last {len(last10)} hard sets"
        g4["met"] = h_rate >= 40.0

    mocks = data.get("mocks") or []
    last4 = mocks[-4:]
    g5 = gates.setdefault("G5", {})
    if not last4:
        g5["current"] = "0 mocks"
        g5["met"] = False
    else:
        avgs = [float(m["avg"]) for m in last4 if m.get("avg") is not None]
        if avgs:
            roll = sum(avgs) / len(avgs)
            g5["current"] = f"{roll:.2f} / 5.0 over last {len(avgs)}"
            g5["met"] = roll >= 4.0
        else:
            g5["current"] = "mocks missing averages"
            g5["met"] = False

    misses = data.get("error_log") or []
    g7 = gates.setdefault("G7", {})
    if not misses:
        g7["current"] = "N/A (no misses yet)"
        g7["met"] = None
    else:
        tagged = sum(1 for e in misses if e.get("type") in ERROR_TYPES)
        g7["current"] = f"{tagged}/{len(misses)} tagged"
        g7["met"] = tagged == len(misses)

    data["phase_a_ready"] = all(
        bool(gates.get(g, {}).get("met")) for g in ("G1", "G2", "G3", "G4", "G5", "G6")
    ) and gates.get("G7", {}).get("met") is not False


def render_md(data: dict[str, Any]) -> str:
    gates = data.get("gates") or {}
    lines = [
        "# SCOREBOARD — PHASE A (INTERVIEW DSA)",
        "",
        f"**Last updated:** {data.get('last_updated', date.today().isoformat())}  ",
        "**Rule:** Chat-guided solves != timed credit. Update after every timed set, retention grill, and mock.  ",
        "**Source of truth:** `Metrics/scoreboard.json` (regenerate this file via `tools/scoreboard_update.py`).  ",
        "**Content:** Phase A Modules 1–11 lessons + retention grills are **delivered**. See `Phase A Curriculum Index.md`.",
        "",
        "---",
        "",
        "## Delivery vs mastery",
        "",
        "| Layer | Status |",
        "|---|---|",
        "| Teacher content (M1–M11) | **FINISHED** |",
        f"| Learner Phase A ready (G1–G7) | **{'DECLARED' if data.get('phase_a_ready') else 'NOT DECLARED'}** |",
        "",
        "---",
        "",
        "## Phase A gate snapshot",
        "",
        "| Gate | Threshold | Current | Met? |",
        "|---|---|---|---|",
    ]
    for gid in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
        g = gates.get(gid) or {}
        met = g.get("met")
        met_s = "Yes" if met is True else ("Pending data" if met is None else "No")
        lines.append(
            f"| {gid} | {g.get('threshold', '')} | {g.get('current', '')} | {met_s} |"
        )
    lines += [
        "",
        f"**Phase A ready?** {'Yes' if data.get('phase_a_ready') else 'No — content ready, evidence not.'}",
        "",
        "---",
        "",
        "## Module status",
        "",
        "| Module | Name | Content | Learner |",
        "|---|---|---|---|",
    ]
    for m in data.get("modules") or []:
        lines.append(
            f"| {m.get('module')} | {m.get('name')} | {m.get('content')} | {m.get('learner')} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Timed sets log",
        "",
        "| Date | Module | Duration | Problems | Diff | Blind? | First-pass correct | Hints | Screen-pass? | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    timed = data.get("timed_sets") or []
    if not timed:
        lines.append("| — | — | — | — | — | — | — | — | — | None yet |")
    else:
        for t in timed:
            lines.append(
                f"| {t.get('date')} | {t.get('module')} | {t.get('duration_min')} | {t.get('problems')} | "
                f"{t.get('difficulty', 'medium')} | {t.get('blind')} | {t.get('first_pass_correct')} | "
                f"{t.get('hints')} | {t.get('would_pass_screen', '')} | {t.get('notes', '')} |"
            )

    # Rolling windows
    mediums = [t for t in timed if (t.get("difficulty") or "medium").lower() == "medium"][-20:]
    hards = [t for t in timed if (t.get("difficulty") or "").lower() == "hard"][-10:]

    def pct(rows: list) -> str:
        if not rows:
            return "n/a"
        ok = sum(int(r.get("first_pass_correct") or 0) for r in rows)
        tot = sum(int(r.get("problems") or 0) for r in rows)
        if tot == 0:
            return "n/a"
        return f"{100.0 * ok / tot:.0f}%"

    lines += [
        "",
        "### Rolling windows",
        "",
        f"- Last 20 mediums first-pass %: **{pct(mediums)}**",
        f"- Last 10 hards first-pass / recovery %: **{pct(hards)}**",
        "",
        "---",
        "",
        "## Error taxonomy (timed misses only)",
        "",
        "| Date | Problem | Error type | Fix / requeue |",
        "|---|---|---|---|",
    ]
    errs = data.get("error_log") or []
    if not errs:
        lines.append("| — | — | knowledge-gap / misread / time-pressure / careless-slip | — |")
    else:
        for e in errs:
            lines.append(
                f"| {e.get('date')} | {e.get('problem')} | {e.get('type')} | {e.get('fix', '')} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Redo queue (≥ 7 days later, blind)",
        "",
        "| Problem | Failed on | Due redo | Result | Notes |",
        "|---|---|---|---|---|",
    ]
    redo = data.get("redo_queue") or []
    if not redo:
        lines.append("| — | — | — | — | — |")
    else:
        for r in redo:
            lines.append(
                f"| {r.get('problem')} | {r.get('failed_on')} | {r.get('due')} | "
                f"{r.get('result', '')} | {r.get('notes', '')} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Mini-mock log",
        "",
        "| Date | After module | Duration | Clarity | Correctness | Complexity | Code | Recovery | Avg | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    mocks = data.get("mocks") or []
    if not mocks:
        lines.append(
            "| — | — | — | /5 | /5 | /5 | /5 | /5 | — | Protocols in `Gauntlet/Phase A Gauntlet.md` |"
        )
    else:
        for m in mocks:
            lines.append(
                f"| {m.get('date')} | {m.get('after_module')} | {m.get('duration_min')} | "
                f"{m.get('clarity')} | {m.get('correctness')} | {m.get('complexity')} | "
                f"{m.get('code')} | {m.get('recovery')} | {m.get('avg')} | {m.get('notes', '')} |"
            )

    last4 = mocks[-4:]
    if last4 and all(m.get("avg") is not None for m in last4):
        roll = sum(float(m["avg"]) for m in last4) / len(last4)
        roll_s = f"{roll:.2f}"
    else:
        roll_s = "n/a"
    lines += [
        "",
        f"**Rolling last-4 mock average:** {roll_s}",
        "",
        "---",
        "",
        "## Optional contests (do not gate Phase A)",
        "",
        "| Date | Platform | Result | Notes |",
        "|---|---|---|---|",
    ]
    contests = data.get("contests") or []
    if not contests:
        lines.append("| — | — | — | — |")
    else:
        for c in contests:
            lines.append(
                f"| {c.get('date')} | {c.get('platform')} | {c.get('result')} | {c.get('notes', '')} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Session pace (student-owned)",
        "",
        "| Preference | Current |",
        "|---|---|",
        "| Session length | Student choice |",
        "| Calendar deadline | **None** |",
        "| Content path | `Phase A Curriculum Index.md` |",
        "| Timed protocol | `Practice/Timed Transfer Protocol.md` |",
        "| Drill generator | `py -3 tools/spaced_drill.py --write` |",
        "| Next learner action | Module 2 Retention (self-grade vs answer key) |",
        "",
    ]
    return "\n".join(lines)


def cmd_timed(args: argparse.Namespace) -> None:
    data = load_sb()
    entry = {
        "date": args.date or date.today().isoformat(),
        "module": args.module,
        "duration_min": args.duration,
        "problems": args.problems,
        "difficulty": (args.difficulty or "medium").lower(),
        "blind": "Y" if yn(args.blind) else "N",
        "first_pass_correct": args.first_pass,
        "hints": "Y" if yn(args.hints) else "N",
        "would_pass_screen": ("Y" if yn(args.screen) else "N") if args.screen else "",
        "notes": args.notes or "",
    }
    data.setdefault("timed_sets", []).append(entry)
    save_sb(data)
    SB_MD.write_text(render_md(data), encoding="utf-8")
    print(f"Appended timed set; wrote {SB_JSON.name} + {SB_MD.name}")


def cmd_mock(args: argparse.Namespace) -> None:
    data = load_sb()
    scores = [args.clarity, args.correctness, args.complexity, args.code, args.recovery]
    avg = round(sum(scores) / 5.0, 2)
    entry = {
        "date": args.date or date.today().isoformat(),
        "after_module": args.after_module,
        "duration_min": args.duration,
        "clarity": args.clarity,
        "correctness": args.correctness,
        "complexity": args.complexity,
        "code": args.code,
        "recovery": args.recovery,
        "avg": avg,
        "notes": args.notes or "",
    }
    data.setdefault("mocks", []).append(entry)
    save_sb(data)
    SB_MD.write_text(render_md(data), encoding="utf-8")
    print(f"Appended mock (avg={avg}); wrote {SB_JSON.name} + {SB_MD.name}")


def cmd_error(args: argparse.Namespace) -> None:
    if args.type not in ERROR_TYPES:
        raise SystemExit(f"--type must be one of {sorted(ERROR_TYPES)}")
    data = load_sb()
    data.setdefault("error_log", []).append(
        {
            "date": args.date or date.today().isoformat(),
            "problem": args.problem,
            "type": args.type,
            "fix": args.fix or "",
        }
    )
    save_sb(data)
    SB_MD.write_text(render_md(data), encoding="utf-8")
    print(f"Appended error tag; wrote {SB_JSON.name} + {SB_MD.name}")


def cmd_redo(args: argparse.Namespace) -> None:
    data = load_sb()
    data.setdefault("redo_queue", []).append(
        {
            "problem": args.problem,
            "failed_on": args.failed_on,
            "due": args.due,
            "result": args.result or "",
            "notes": args.notes or "",
        }
    )
    save_sb(data)
    SB_MD.write_text(render_md(data), encoding="utf-8")
    print(f"Appended redo row; wrote {SB_JSON.name} + {SB_MD.name}")


def cmd_regen(_: argparse.Namespace) -> None:
    data = load_sb()
    save_sb(data)
    SB_MD.write_text(render_md(data), encoding="utf-8")
    print(f"Regenerated {SB_MD.name} from {SB_JSON.name}")


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Update Phase A scoreboard JSON + markdown.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_t = sub.add_parser("timed", help="Append a timed set")
    p_t.add_argument("--module", type=int, required=True)
    p_t.add_argument("--duration", type=int, required=True, help="Minutes")
    p_t.add_argument("--problems", type=int, required=True)
    p_t.add_argument("--blind", default="Y")
    p_t.add_argument("--first-pass", type=int, required=True, dest="first_pass")
    p_t.add_argument("--hints", default="N")
    p_t.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard", "mixed"])
    p_t.add_argument("--screen", default="", help="Y/N would-pass-screen")
    p_t.add_argument("--notes", default="")
    p_t.add_argument("--date", default=None)
    p_t.set_defaults(func=cmd_timed)

    p_m = sub.add_parser("mock", help="Append a mini-mock")
    p_m.add_argument("--after-module", type=int, required=True, dest="after_module")
    p_m.add_argument("--duration", type=int, default=45)
    p_m.add_argument("--clarity", type=int, required=True)
    p_m.add_argument("--correctness", type=int, required=True)
    p_m.add_argument("--complexity", type=int, required=True)
    p_m.add_argument("--code", type=int, required=True)
    p_m.add_argument("--recovery", type=int, required=True)
    p_m.add_argument("--notes", default="")
    p_m.add_argument("--date", default=None)
    p_m.set_defaults(func=cmd_mock)

    p_e = sub.add_parser("error", help="Tag a timed miss")
    p_e.add_argument("--problem", required=True)
    p_e.add_argument("--type", required=True)
    p_e.add_argument("--fix", default="")
    p_e.add_argument("--date", default=None)
    p_e.set_defaults(func=cmd_error)

    p_r = sub.add_parser("redo", help="Add redo-queue row")
    p_r.add_argument("--problem", required=True)
    p_r.add_argument("--failed-on", required=True, dest="failed_on")
    p_r.add_argument("--due", required=True)
    p_r.add_argument("--result", default="")
    p_r.add_argument("--notes", default="")
    p_r.set_defaults(func=cmd_redo)

    p_g = sub.add_parser("regen", help="Regenerate Scoreboard.md from JSON")
    p_g.set_defaults(func=cmd_regen)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
