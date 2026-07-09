"""Minimal stdlib test harness for problem-bank solutions.

Each problem directory must provide:
  - solution.py  — reference (or student) implementation
  - test_cases.py — either:
      CASES: list of (args, expected) where args is a tuple/list of
             positional args to the primary function, OR a dict of kwargs
      TESTS: list of callables that take the solution module and assert
      PRIMARY: optional str naming the function to call for CASES
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Callable


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _call_primary(sol, primary: str | None, args):
    if primary is None:
        # Prefer common names, else first public callable
        for cand in ("solve", "solution", "main"):
            if hasattr(sol, cand) and callable(getattr(sol, cand)):
                primary = cand
                break
        if primary is None:
            publics = [
                n
                for n in dir(sol)
                if not n.startswith("_") and callable(getattr(sol, n))
            ]
            if not publics:
                raise AttributeError("No callable found in solution.py")
            primary = publics[0]
    fn = getattr(sol, primary)
    if isinstance(args, dict):
        return fn(**args)
    if isinstance(args, (list, tuple)):
        return fn(*args)
    return fn(args)


def _values_equal(got: Any, expected: Any) -> bool:
    if type(got) is not type(expected) and isinstance(got, (list, tuple)) and isinstance(
        expected, (list, tuple)
    ):
        got, expected = list(got), list(expected)
    if isinstance(expected, float) and isinstance(got, (int, float)):
        return abs(float(got) - expected) < 1e-9
    if isinstance(expected, set) and isinstance(got, (list, tuple, set)):
        return set(got) == expected
    # unordered pair / any-of: frozenset of frozensets
    if isinstance(expected, frozenset):
        if isinstance(got, (list, tuple)):
            return frozenset(got) == expected or frozenset(
                frozenset(x) if isinstance(x, (list, tuple)) else x for x in got
            ) == expected
        return got == expected
    return got == expected


def run_problem(problem_dir: Path) -> tuple[bool, str, int, int]:
    """Returns (ok, message, passed, total)."""
    sol_path = problem_dir / "solution.py"
    tc_path = problem_dir / "test_cases.py"
    if not sol_path.exists() or not tc_path.exists():
        return False, "missing solution.py or test_cases.py", 0, 0

    pid = problem_dir.name
    try:
        sol = load_module(sol_path, f"pb_sol_{pid}")
        tc = load_module(tc_path, f"pb_tc_{pid}")
    except Exception as e:
        return False, f"import error: {e}\n{traceback.format_exc()}", 0, 0

    primary = getattr(tc, "PRIMARY", None)
    cases = getattr(tc, "CASES", None)
    tests: list[Callable] = list(getattr(tc, "TESTS", []) or [])

    passed = 0
    total = 0
    failures: list[str] = []

    if cases:
        for i, case in enumerate(cases):
            total += 1
            try:
                if len(case) == 2:
                    args, expected = case
                    got = _call_primary(sol, primary, args)
                    if not _values_equal(got, expected):
                        failures.append(
                            f"CASES[{i}]: args={args!r} expected={expected!r} got={got!r}"
                        )
                    else:
                        passed += 1
                elif len(case) == 3:
                    args, expected, note = case
                    got = _call_primary(sol, primary, args)
                    if not _values_equal(got, expected):
                        failures.append(
                            f"CASES[{i}] ({note}): args={args!r} expected={expected!r} got={got!r}"
                        )
                    else:
                        passed += 1
                else:
                    failures.append(f"CASES[{i}]: bad case shape {case!r}")
            except Exception as e:
                failures.append(f"CASES[{i}]: raised {type(e).__name__}: {e}")

    for i, test_fn in enumerate(tests):
        total += 1
        try:
            test_fn(sol)
            passed += 1
        except AssertionError as e:
            failures.append(f"TESTS[{i}] ({getattr(test_fn, '__name__', i)}): {e}")
        except Exception as e:
            failures.append(
                f"TESTS[{i}] ({getattr(test_fn, '__name__', i)}): "
                f"{type(e).__name__}: {e}"
            )

    if total == 0:
        return False, "no CASES or TESTS defined", 0, 0

    if failures:
        msg = f"{passed}/{total} passed\n  " + "\n  ".join(failures[:8])
        if len(failures) > 8:
            msg += f"\n  ... +{len(failures) - 8} more"
        return False, msg, passed, total

    return True, f"{passed}/{total} passed", passed, total


def discover_problems(root: Path | None = None) -> list[Path]:
    root = root or Path(__file__).resolve().parent / "problems"
    if not root.is_dir():
        return []
    dirs = [p for p in sorted(root.iterdir()) if p.is_dir() and (p / "solution.py").exists()]
    return dirs
