# CAES Paper Evaluator

`caes-paper-evaluator` is a Codex skill for evaluating and writing compressed-air energy storage research papers from local project folders.

It is designed for projects involving:

- CAES / AA-CAES system modeling
- Thermal energy storage for CAES
- Thermochemical energy storage (TCES)
- TCES-coupled AA-CAES
- MATLAB or Python simulation results
- Paper-readiness assessment
- Manuscript structure, figure planning, and academic writing

## What It Does

The skill helps Codex act as a CAES-domain paper evaluator. It can:

- audit whether a local CAES project is ready for a paper
- compare code/results against expected energy-system manuscript standards
- identify missing validation, exergy analysis, sensitivity studies, and figures
- search CAES/AA-CAES/TCES literature metadata
- score paper readiness at the project-folder level
- guide paper structure, claims, limitations, and writing
- provide templates for Methods, Results, Validation, Sensitivity Analysis, and Limitations sections

The skill is intentionally not limited to one specific CAES model or result-output format.

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── advanced_writing_templates.md
│   ├── caes_literature_map.md
│   ├── figures_and_tables.md
│   ├── paper_readiness_rubric.md
│   └── writing_patterns.md
└── scripts/
    ├── collect_caes_project_snapshot.py
    ├── score_paper_readiness.py
    └── search_caes_literature.py
```

## Installation

Place or clone this folder under your Codex skills directory:

```powershell
git clone https://github.com/huaxiuwanghongyan/caes-paper-evaluator.git `
  C:\Users\zq\.codex\skills\caes-paper-evaluator
```

After restarting or refreshing Codex, the skill should be discoverable as:

```text
caes-paper-evaluator
```

## Typical Prompts

```text
Use caes-paper-evaluator to assess whether the current CAES project is ready for a journal paper.
```

```text
Use caes-paper-evaluator to identify missing analyses, figures, and validation work for this AA-CAES + TCES model.
```

```text
Use caes-paper-evaluator to draft the Methods section based on the current model and results.
```

```text
Use caes-paper-evaluator to find related TCES + CAES literature and explain how to position the novelty.
```

## Utility Scripts

### 1. Project Snapshot

Collect a compact inventory of a CAES project folder:

```powershell
python scripts\collect_caes_project_snapshot.py C:\path\to\caes-project
```

The script lists code, documents, data, figures, and likely MATLAB entry points.

### 2. Paper Readiness Score

Generate a heuristic paper-readiness score:

```powershell
python scripts\score_paper_readiness.py C:\path\to\caes-project
```

The scorer checks evidence for:

- executable model
- system boundary
- baseline comparison
- thermal storage split
- water or mass closure
- exergy analysis
- sensitivity analysis
- validation
- material references
- figures and tables

The score is a guide, not a substitute for expert review.

### 3. Literature Search

Search Crossref metadata for CAES-related literature:

```powershell
python scripts\search_caes_literature.py --topic tces-caes --limit 10
```

Available topics:

```text
aa-caes-thermal-storage
aa-caes-dynamic-model
caes-exergy
tces-caes
salt-hydrate-tces
zeolite-water-tces
mgoh2-mgo-tces
caes-economics
```

Useful filters:

```powershell
python scripts\search_caes_literature.py `
  --topic salt-hydrate-tces `
  --from-year 2020 `
  --min-score 20 `
  --limit 10
```

Export JSON and BibTeX:

```powershell
python scripts\search_caes_literature.py `
  --topic tces-caes `
  --limit 20 `
  --cache references\caes_literature_cache.json `
  --bibtex references\caes_core_bibliography.bib
```

## Current Scope

The skill focuses on compressed-air energy storage research. It is especially useful for:

- AA-CAES thermodynamic models
- sensible thermal storage baselines
- TCES material cascade concepts
- exergy-based mechanism analysis
- CAES paper argument structure
- energy-system figure and table planning

It does not currently provide:

- automatic full-text PDF reading
- journal impact-factor lookup
- guaranteed citation verification
- automatic figure generation
- detailed economic database integration

Those can be added later as separate scripts or references.

## Design Principle

The skill should not merely polish writing. Its first job is to ask:

```text
Does the current model and evidence actually support the paper's claims?
```

Only after that should it help with manuscript drafting.
