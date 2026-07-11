#!/usr/bin/env python3
"""Summarize spine/bank coverage and gate readiness."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


DONE = {"bank-passed", "timed-passed", "skipped-optional"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gate",
        action="store_true",
        help="Show per-module gate blockers (gate_required and not done)",
    )
    parser.add_argument(
        "--module",
        type=int,
        default=None,
        help="Filter gate report to one module (0 = coverage)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "Metrics/spine_tracker.json").read_text())
    total = data["total"]
    bank = data["in_bank"]
    print(f"Spine rows: {total}")
    print(f"In local bank: {bank} ({100 * bank / total:.1f}%)")
    print(f"LC-required / notebook: {total - bank}")
    print(data.get("honesty", ""))

    missing_h = [p for p in data["problems"] if p["diff"] == "H" and not p["in_bank"]]
    print(f"Hard rows still LC-only: {len(missing_h)}")
    for p in missing_h[:12]:
        print(f"  - {p['name']} (LC {p['lc']})")

    if not args.gate:
        return 0

    print("\n=== GATE READINESS (gate_required rows) ===")
    by_mod: dict[int, list] = defaultdict(list)
    for p in data["problems"]:
        if not p.get("gate_required", True):
            continue
        by_mod[p.get("module")].append(p)

    mods = sorted(by_mod)
    if args.module is not None:
        mods = [args.module]

    blocked_modules = 0
    for m in mods:
        rows = by_mod.get(m, [])
        if not rows:
            continue
        pending = [p for p in rows if p.get("status", "not-started") not in DONE]
        done_n = len(rows) - len(pending)
        label = f"M{m}" if m and m > 0 else "Coverage"
        ok = len(pending) == 0
        if not ok:
            blocked_modules += 1
        print(
            f"{label}: {done_n}/{len(rows)} gate rows done "
            f"{'READY' if ok else 'BLOCKED'}"
        )
        # show up to 8 blockers
        for p in pending[:8]:
            src = p.get("source", "lc-required")
            print(f"  - [{p['status']}] {p['name']} ({src}"
                  f"{', '+p['bank_id'] if p.get('bank_id') else ''}"
                  f"{', LC '+str(p['lc']) if p.get('lc') and p['lc']!='—' else ''})")
        if len(pending) > 8:
            print(f"  ... +{len(pending)-8} more")

    print(
        f"\nModules with open gate rows: {blocked_modules}. "
        "Do not set learner status timed-verified while BLOCKED."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
