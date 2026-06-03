#!/usr/bin/env python3
"""Heuristic paper-readiness scorer for CAES/AA-CAES/TCES project folders.

This script intentionally scores project evidence at the folder level rather
than parsing one specific simulation output format.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


CHECKS = {
    "model_executable": {
        "weight": 12,
        "patterns": [r"main_simulation", r"run\(", r"init_params"],
        "why": "A paper needs a reproducible model entry point.",
    },
    "system_boundary": {
        "weight": 10,
        "patterns": [r"P_stor", r"P_comp", r"P_turb", r"m_dot", r"t_ch", r"t_dch"],
        "why": "Pressure, flow, and time boundaries must be explicit.",
    },
    "baseline_comparison": {
        "weight": 10,
        "patterns": [r"baseline", r"water-only", r"pure water", r"comparison"],
        "why": "The proposed CAES configuration needs a fair baseline.",
    },
    "thermal_storage_split": {
        "weight": 10,
        "patterns": [r"TCES", r"water", r"stored heat", r"released heat", r"heat share"],
        "why": "TES/TCES heat accounting must support the mechanism claim.",
    },
    "water_or_mass_closure": {
        "weight": 8,
        "patterns": [r"water balance", r"m_H2O", r"mass balance", r"closure"],
        "why": "TCES hydration/dehydration requires water or species closure.",
    },
    "exergy_analysis": {
        "weight": 12,
        "patterns": [r"exergy", r"㶲", r"Ex_", r"exergy destruction"],
        "why": "TCES advantage should be explained through heat grade/exergy.",
    },
    "sensitivity_analysis": {
        "weight": 10,
        "patterns": [r"sensitivity", r"parametric", r"sweep", r"optimization"],
        "why": "A single operating point is weak for a full journal paper.",
    },
    "validation": {
        "weight": 10,
        "patterns": [r"validation", r"verify", r"literature", r"relative error"],
        "why": "Model validation is usually required for energy-system papers.",
    },
    "material_references": {
        "weight": 8,
        "patterns": [r"MgCl2", r"MgSO4", r"zeolite", r"hydrate", r"activation energy", r"enthalpy"],
        "why": "TCES material parameters need literature support.",
    },
    "figures_tables": {
        "weight": 10,
        "patterns": [r"\.png", r"\.svg", r"\.fig", r"figure", r"table", r"plot"],
        "why": "A paper needs figures/tables that prove the argument.",
    },
}


def read_project_text(root: Path) -> str:
    chunks = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "slprj"}]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in {".m", ".py", ".md", ".txt", ".json", ".csv"}:
                continue
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
                chunks.append(str(path.relative_to(root)))
            except OSError:
                pass
    return "\n".join(chunks)


def score_check(text: str, patterns: list[str]) -> float:
    hits = 0
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits += 1
    return hits / max(len(patterns), 1)


def readiness_level(score: float) -> str:
    if score < 25:
        return "Level 0: exploratory model only"
    if score < 45:
        return "Level 1: internal technical note"
    if score < 65:
        return "Level 2: conference abstract or short paper"
    if score < 85:
        return "Level 3: full journal draft"
    return "Level 4: submission-ready package"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    text = read_project_text(root)

    total = 0.0
    max_total = sum(item["weight"] for item in CHECKS.values())
    rows = []
    for name, item in CHECKS.items():
        ratio = score_check(text, item["patterns"])
        score = ratio * item["weight"]
        total += score
        rows.append((name, score, item["weight"], item["why"]))

    percent = 100 * total / max_total
    print(f"Project: {root}")
    print(f"Overall readiness: {percent:.1f}/100")
    print(f"Level: {readiness_level(percent)}\n")
    print("| Check | Score | Why it matters |")
    print("|---|---:|---|")
    for name, score, weight, why in rows:
        print(f"| {name} | {score:.1f}/{weight} | {why} |")

    print("\nPriority gaps:")
    for name, score, weight, why in rows:
        if score < 0.5 * weight:
            print(f"- {name}: {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
