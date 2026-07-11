#!/usr/bin/env python3
"""Summarize Metrics/spine_tracker.json coverage."""
from __future__ import annotations
import json
from pathlib import Path

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "Metrics/spine_tracker.json").read_text())
    total = data["total"]
    bank = data["in_bank"]
    print(f"Spine rows: {total}")
    print(f"In local bank: {bank} ({100*bank/total:.1f}%)")
    print(f"LC-only / notebook: {total-bank}")
    by = {}
    for p in data["problems"]:
        # infer module from nothing — just list missing high diff
        pass
    missing_h = [p for p in data["problems"] if p["diff"]=="H" and not p["in_bank"]]
    print(f"Hard rows still LC-only: {len(missing_h)}")
    for p in missing_h[:12]:
        print(f"  - {p['name']} (LC {p['lc']})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
