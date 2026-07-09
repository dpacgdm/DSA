#!/usr/bin/env python3
"""Discover and run all problem-bank tests. Stdlib only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from harness import discover_problems, run_problem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run problem-bank tests")
    parser.add_argument(
        "filter",
        nargs="?",
        default="",
        help="Optional substring filter on problem folder name",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only print summary and failures",
    )
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent / "problems"
    problems = discover_problems(root)
    if args.filter:
        problems = [p for p in problems if args.filter.lower() in p.name.lower()]

    if not problems:
        print("No problems found.")
        return 1

    ok_n = 0
    fail_n = 0
    total_cases = 0
    passed_cases = 0

    print(f"Running {len(problems)} problem(s)...\n")
    for p in problems:
        ok, msg, passed, total = run_problem(p)
        total_cases += total
        passed_cases += passed
        status = "PASS" if ok else "FAIL"
        if ok:
            ok_n += 1
            if not args.quiet:
                print(f"[{status}] {p.name}: {msg}")
        else:
            fail_n += 1
            print(f"[{status}] {p.name}: {msg}")

    print()
    print("=" * 60)
    print(
        f"Problems: {ok_n} passed, {fail_n} failed, {len(problems)} total | "
        f"Cases: {passed_cases}/{total_cases}"
    )
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
