#!/usr/bin/env python3
"""Start a routine with a fresh copy of its drill file.

    python new.py        list the routines and what you've started
    python new.py 5      copy drills/r05_*.py into work/ (an older attempt gets archived)
"""
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRILLS = ROOT / "drills"
WORK = ROOT / "work"
ARCHIVE = WORK / "archive"
LOGS = {
    "gotchas.md": "# Gotchas\n\nEvery prediction you got wrong, plus the reason in one line.\n\n",
    "triggers.md": "# Triggers\n\nProblem signal -> pattern -> why it fits.\n\n",
}


def routines():
    return {int(p.name[1:3]): p for p in sorted(DRILLS.glob("r[0-9][0-9]_*.py"))}


def title(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip().strip('"').strip()
        if line:
            return line
    return path.stem


def setup_work():
    WORK.mkdir(exist_ok=True)
    for name, text in LOGS.items():
        log = WORK / name
        if not log.exists():
            log.write_text(text, encoding="utf-8")


def show_list(found):
    print(__doc__.strip(), end="\n\n")
    for path in found.values():
        status = "started" if (WORK / path.name).exists() else ""
        earlier = len(list(ARCHIVE.glob(path.stem + ".*.py"))) if ARCHIVE.exists() else 0
        if earlier:
            status += f" (+{earlier} earlier)"
        print(f"  {title(path):<55} {status}")


def start(n, found):
    if n not in found:
        sys.exit(f"No routine {n}. Run `python new.py` to see the list.")
    src = found[n]
    setup_work()
    dest = WORK / src.name
    if dest.exists():
        ARCHIVE.mkdir(exist_ok=True)
        moved = ARCHIVE / f"{src.stem}.{time.strftime('%Y%m%d-%H%M%S')}.py"
        shutil.move(str(dest), str(moved))
        print(f"Archived your previous attempt to {moved.relative_to(ROOT)}")
    shutil.copyfile(src, dest)
    print(f"Fresh copy: {dest.relative_to(ROOT)}")
    print(f"Fill in the ??? predictions and the functions, then run: python check.py {n}")


def main():
    found = routines()
    if len(sys.argv) < 2:
        show_list(found)
        return
    try:
        n = int(sys.argv[1])
    except ValueError:
        sys.exit(__doc__.strip())
    start(n, found)


if __name__ == "__main__":
    main()
