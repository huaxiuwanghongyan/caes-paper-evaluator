#!/usr/bin/env python3
"""Collect a compact CAES project inventory for paper-readiness review."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


CODE_EXTS = {".m", ".py", ".jl", ".ipynb"}
DOC_EXTS = {".md", ".txt", ".docx", ".doc", ".pdf", ".rtf"}
DATA_EXTS = {".csv", ".xlsx", ".xls", ".mat", ".json"}
FIG_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".pdf", ".eps", ".fig"}


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in CODE_EXTS:
        return "code"
    if suffix in DOC_EXTS:
        return "docs"
    if suffix in DATA_EXTS:
        return "data"
    if suffix in FIG_EXTS:
        return "figures"
    return "other"


def should_skip(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return any(part in parts for part in {".git", "__pycache__", "slprj"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Project root does not exist: {root}")

    buckets: dict[str, list[Path]] = {k: [] for k in ["code", "docs", "data", "figures", "other"]}
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not should_skip(current / d)]
        for filename in filenames:
            path = current / filename
            if should_skip(path):
                continue
            buckets[classify(path)].append(path)

    print(f"Project: {root}")
    for bucket, files in buckets.items():
        print(f"\n[{bucket}] {len(files)} file(s)")
        for path in sorted(files)[:40]:
            rel = path.relative_to(root)
            print(f"  - {rel}")
        if len(files) > 40:
            print(f"  ... {len(files) - 40} more")

    matlab_files = sorted(p for p in buckets["code"] if p.suffix.lower() == ".m")
    if matlab_files:
        print("\n[matlab hints]")
        for path in matlab_files:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "main" in path.name.lower() or "run(" in text or "init_params" in text:
                print(f"  possible entry/helper: {path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
