#!/usr/bin/env python3
"""Check your predictions and drills.

    python check.py 5        predictions + tests for work/r05_*.py
    python check.py all      every routine you've started in work/
    python check.py 5 -s     run the reference solution instead
    python check.py 5 -d     run the untouched drill file (everything should be todo)
"""
import argparse
import contextlib
import io
import os
import re
import sys
import traceback
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRILLS = ROOT / "drills"
SOLUTIONS = ROOT / "solutions"
WORK = ROOT / "work"
TODO = "???"

# Every prediction snippet starts with these names already imported.
PRELUDE = """\
import math, sys, copy, heapq, bisect, itertools, functools, operator, collections, string
from collections import Counter, defaultdict, deque, OrderedDict, namedtuple
from heapq import heappush, heappop, heapify, heappushpop, heapreplace, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from itertools import accumulate, chain, combinations, groupby, permutations, product
from functools import lru_cache, reduce, cmp_to_key
from dataclasses import dataclass, field
try:
    from functools import cache
except ImportError:
    pass
"""

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
if USE_COLOR and os.name == "nt":
    os.system("")  # turns on ANSI escape handling in the Windows console
GREEN, RED, YELLOW, BOLD, DIM = "32", "31", "33", "1", "2"


def paint(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def rel(path):
    try:
        return Path(os.path.relpath(path, ROOT)).as_posix()
    except ValueError:
        return str(path)


def routines():
    return {int(p.name[1:3]): p for p in sorted(DRILLS.glob("r[0-9][0-9]_*.py"))}


def load(path):
    ns = {"__name__": "drill_" + path.stem, "__file__": str(path)}
    source = path.read_text(encoding="utf-8")
    exec(compile(source, str(path), "exec"), ns)
    return ns


def title_of(ns, path):
    doc = (ns.get("__doc__") or "").strip().splitlines()
    return doc[0].strip() if doc else path.stem


# ---------------------------------------------------------------- predictions

def normalize(text):
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def parse_predict(text):
    """Split a PREDICT block into examples. Blank lines separate examples;
    '>>>' starts a statement, '...' continues it, anything else is output."""
    examples = []
    for block in re.split(r"\n\s*\n", text.strip()):
        code, stmts, expected = [], [], []
        for line in block.splitlines():
            if line.startswith(">>>"):
                stmts.append([line[4:]])
                code.append(line)
            elif line.startswith("...") and stmts:
                stmts[-1].append(line[4:])
                code.append(line)
            else:
                expected.append(line)
        if stmts:
            examples.append({
                "code": code,
                "stmts": ["\n".join(s) for s in stmts],
                "expected": normalize("\n".join(expected)),
            })
    return examples


def run_snippet(stmts):
    """Run statements the way the REPL does: expression values are echoed, and
    an exception prints just its class name and moves on to the next line."""
    ns = {"__name__": "__main__"}
    exec(PRELUDE, ns)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for src in stmts:
            try:
                exec(compile(src + "\n", "<predict>", "single"), ns)
            except Exception as exc:
                print(type(exc).__name__)
    return normalize(buf.getvalue())


def check_predictions(target):
    results = []
    for i, ex in enumerate(parse_predict(target.get("PREDICT") or ""), 1):
        if not ex["expected"] or TODO in ex["expected"]:
            results.append(("todo", i, ex, None))
            continue
        actual = run_snippet(ex["stmts"])
        results.append(("ok" if actual == ex["expected"] else "wrong", i, ex, actual))
    return results


# ---------------------------------------------------------------- quiz

def squash(answer):
    s = str(answer).lower()
    for old, new in (("**", "^"), ("²", "^2"), ("³", "^3"), ("log(n)", "logn"), ("·", "*")):
        s = s.replace(old, new)
    return re.sub(r"[\s\-_]+", "", s)


def check_quiz(target, key, solution_mode):
    answers = key.get("QUIZ") or {}
    results = []
    for question, given in (target.get("QUIZ") or {}).items():
        accepted = answers.get(question) or []
        accepted = [accepted] if isinstance(accepted, str) else list(accepted)
        if solution_mode:
            given = accepted[0] if accepted else TODO
        if given is None or str(given).strip() in ("", TODO):
            results.append(("todo", question, given, accepted))
        else:
            ok = squash(given) in {squash(a) for a in accepted}
            results.append(("ok" if ok else "wrong", question, given, accepted))
    return results


# ---------------------------------------------------------------- tests

def describe(exc):
    frames = traceback.extract_tb(exc.__traceback__)
    ours = [f for f in frames if str(ROOT) in str(Path(f.filename).resolve())]
    frame = (ours or frames or [None])[-1]
    lines = []
    if frame is not None:
        lines.append(f"{rel(frame.filename)}:{frame.lineno}  {(frame.line or '').strip()}")
    message = str(exc)
    if not isinstance(exc, AssertionError):
        message = f"{type(exc).__name__}: {message}"
    if message and not (lines and message in lines[0]):
        lines.append(message)
    return lines


def run_tests(drill, target, inject):
    if inject:
        for name, value in target.items():
            if not name.startswith(("_", "test_")) and name not in ("PREDICT", "QUIZ"):
                drill[name] = value
    tests = [(n, f) for n, f in drill.items() if n.startswith("test_") and callable(f)]
    tests += [(n, f) for n, f in target.items()
              if n.startswith("test_") and callable(f) and n not in drill]
    results = []
    for name, fn in tests:
        try:
            fn()
        except NotImplementedError:
            results.append(("todo", name, []))
        except KeyboardInterrupt:
            results.append(("STOPPED", name, ["interrupted (infinite loop?)"]))
            break
        except AssertionError as exc:
            results.append(("FAIL", name, describe(exc)))
        except Exception as exc:
            results.append(("ERROR", name, describe(exc)))
        else:
            results.append(("ok", name, []))
    return results


# ---------------------------------------------------------------- reporting

def tally(results):
    counts = {}
    for r in results:
        counts[r[0]] = counts.get(r[0], 0) + 1
    return counts


def summary(kind, results, good="right"):
    counts = tally(results)
    text = f"{counts.get('ok', 0)}/{len(results)} {good}"
    order = ["FAIL", "ERROR", "STOPPED", "wrong", "todo"]
    for k in sorted((k for k in counts if k != "ok"), key=order.index):
        color = YELLOW if k == "todo" else RED
        text += ", " + paint(f"{counts[k]} {k.lower()}", color)
    return f"  {kind:<8} {text}"


def show_check(mode, drill_path, target_path, verbose):
    """Check one routine. Returns True when nothing is wrong."""
    try:
        drill = load(drill_path)
    except Exception as exc:
        print(paint(f"can't load {rel(drill_path)}: {exc!r}", RED))
        return False
    title = title_of(drill, drill_path)
    print(paint(title, BOLD) + "   " + paint(rel(target_path), DIM))
    try:
        target = drill if mode == "drill" else load(target_path)
    except Exception as exc:
        print(paint(f"  can't load your file: {type(exc).__name__}: {exc}", RED))
        return False
    key = {}
    sol_path = SOLUTIONS / drill_path.name
    if "QUIZ" in drill and sol_path.exists():
        key = target if mode == "solution" else load(sol_path)

    predictions = check_predictions(target)
    quiz = check_quiz(target, key, mode == "solution")
    tests = run_tests(drill, target, inject=(mode != "drill"))

    if predictions:
        print(summary("predict", predictions))
        for status, i, ex, actual in predictions:
            if status != "wrong" or not verbose:
                continue
            print(paint(f"     wrong #{i}", RED))
            for line in ex["code"]:
                print("         " + line)
            print("         you wrote:  " + ex["expected"].replace("\n", "\n                     "))
            print("         python:     " + actual.replace("\n", "\n                     "))
    if quiz:
        print(summary("quiz", quiz))
        for status, question, given, accepted in quiz:
            if status == "wrong" and verbose:
                print(paint(f"     wrong: {question}", RED) + f"  you: {given!r}  expected: {accepted[0]!r}")
    if tests:
        print(summary("tests", tests, good="passed"))
        for status, name, details in tests:
            if status in ("ok", "todo") or not verbose:
                continue
            print("     " + paint(f"{status:<5}", RED) + " " + name)
            for line in details:
                print("           " + line)
        todo = [name[5:] for status, name, _ in tests if status == "todo"]
        if todo and verbose and mode != "drill":
            print("     " + paint("todo ", YELLOW) + " " + ", ".join(todo))

    bad = {"wrong", "FAIL", "ERROR", "STOPPED"}
    statuses = [r[0] for r in predictions + quiz + tests]
    if mode == "solution":
        bad.add("todo")
    if mode == "drill":
        # A stub should pass nothing: a passing test means the test checks nothing.
        passing = [r[1] for r in tests if r[0] == "ok"]
        if passing:
            print(paint(f"  passes without an implementation: {', '.join(passing)}", RED))
            return False
        filled = [r[1] for r in predictions if r[0] != "todo"]
        if filled:
            print(paint(f"  predictions already filled in: {filled}", RED))
            return False
        bad.discard("todo")
    return not any(s in bad for s in statuses)


def main():
    parser = argparse.ArgumentParser(description="Check predictions and drills for a routine.")
    parser.add_argument("routine", help="routine number (e.g. 5) or 'all'")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-s", "--solution", action="store_true", help="check the reference solution")
    mode.add_argument("-d", "--drill", action="store_true", help="check the untouched drill file")
    parser.add_argument("-q", "--quiet", action="store_true", help="summaries only")
    args = parser.parse_args()
    mode = "solution" if args.solution else "drill" if args.drill else "work"

    if sys.version_info < (3, 10):
        print(paint("Python 3.10+ recommended (snippets were checked on 3.12).", YELLOW))

    found = routines()
    if args.routine == "all":
        numbers = list(found)
        if mode == "work":
            numbers = [n for n in numbers if (WORK / found[n].name).exists()]
            if not numbers:
                print("Nothing in work/ yet. Start with: python new.py 0")
                return 0
        verbose = not args.quiet and mode == "work"
    else:
        try:
            numbers = [int(args.routine)]
        except ValueError:
            parser.error("routine must be a number or 'all'")
        if numbers[0] not in found:
            parser.error(f"no drill file for routine {numbers[0]}")
        verbose = not args.quiet

    all_good = True
    for n in numbers:
        drill_path = found[n]
        target = {"work": WORK, "solution": SOLUTIONS, "drill": DRILLS}[mode] / drill_path.name
        if not target.exists():
            print(f"No {rel(target)} yet. Start it with: python new.py {n}")
            all_good = False
            continue
        all_good &= show_check(mode, drill_path, target, verbose)
        if len(numbers) > 1:
            print()
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
