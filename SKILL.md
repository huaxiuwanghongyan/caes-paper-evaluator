---
name: caes-paper-evaluator
description: Evaluate, plan, audit, and help write compressed-air energy storage papers from local project folders. Use when the task involves CAES, AA-CAES, LAES/CAES comparisons, thermal energy storage for CAES, TCES-coupled CAES, MATLAB/Python simulation results, paper-readiness assessment, journal-style structure, reviewer-style critique, figure/table standards, missing analyses, or drafting manuscript sections for compressed air energy storage research.
---

# CAES Paper Evaluator

## Core Posture

Treat every request as a CAES-domain manuscript-readiness task unless the user asks only for narrow editing. First check whether the local code, parameters, results, figures, and claims can support a paper; then write or revise text. Do not make the paper sound stronger than the evidence.

Use this skill for CAES/AA-CAES/TCES projects, especially folders containing MATLAB/Python models, result logs, notes, Markdown plans, figures, spreadsheets, or draft manuscripts.

## Quick Workflow

1. Inventory the project.
   - Use `rg --files` to list code, references, drafts, data, figures, and result files.
   - Identify the main simulation entry point, parameter files, model modules, and local planning documents.
   - If useful, run `scripts/collect_caes_project_snapshot.py <project_root>` to get a compact inventory.

2. Verify executable evidence before judging manuscript claims.
   - Run syntax/static checks where practical (`checkcode` for MATLAB, tests or import checks for Python).
   - Run the main model if the user asks for current results or if results may be stale.
   - Record key outputs: RTE, compressor work, turbine work, stage inlet/outlet temperatures, heat storage/release, TES/TCES share, storage volume, pressure range, water balance, and loss assumptions.

3. Compare the work against CAES paper expectations.
   - Read `references/paper_readiness_rubric.md` for readiness scoring.
   - Read `references/caes_literature_map.md` before making novelty or literature-gap claims.
   - Read `references/figures_and_tables.md` when judging or designing figures.
   - Read `references/writing_patterns.md` when drafting manuscript text.
   - When literature is needed, run `scripts/search_caes_literature.py --topic <topic> --limit 10` or use web search for source verification.

4. Produce a structured assessment before writing.
   - State whether the current folder is ready for: internal memo, conference abstract, short paper, full journal paper, or not yet.
   - Separate `supported claims`, `weak claims`, `missing analyses`, `model risks`, and `next experiments`.
   - For every major paper claim, point to the code/result artifact that supports it or mark it unsupported.
   - For a quick folder-level readiness score, run `scripts/score_paper_readiness.py <project_root>`.

5. Draft only after the evidence chain is clear.
   - Keep claims proportional to evidence.
   - Use CAES terminology precisely: compressor/turbine, cavern/storage vessel, charging/discharging, TES/TCES, sensible/latent/thermochemical heat, exergy, RTE, LCOS.
   - Preserve the user's current model boundary unless it is physically inconsistent; flag boundary changes explicitly.

## Assessment Output Shape

Use this order for paper-readiness reviews:

```markdown
**Readiness**
[One-paragraph verdict: current paper level and why.]

**Supported Claims**
- [Claim] -> [specific evidence/result/code]

**Blocking Gaps**
- [Gap] -> [why reviewers will care] -> [minimum fix]

**Model And Physics Risks**
- [Risk] -> [current assumption] -> [recommended validation/sensitivity]

**Figures And Tables Needed**
- [Figure/table] -> [message it should prove] -> [required data]

**Writing Plan**
- [Section-by-section outline or next writing task]
```

For manuscript drafting, use:

```markdown
**Assumptions Used**
[Only if assumptions matter.]

**Draft**
[Publication-style prose.]

**Evidence To Insert**
- [Citation/result/figure to insert]
```

## CAES-Specific Checks

Always check these before accepting a result as paper-ready:

- Same system boundary for TCES and baseline: pressure limits, charge/discharge time, mass flow, turbine outlet pressure, storage initial/final pressure.
- RTE definition: `W_turb_total * t_dch / (W_comp_total * t_ch)` unless the user specifies another boundary.
- Charging path continuity: compressor outlet should feed the modeled heat recovery/cooling step and then the next compressor inlet.
- Discharging path continuity: storage outlet should feed preheat/TCES reheat and then the turbine inlet without undocumented temperature resets.
- Storage process: initial pressure, minimum pressure, maximum pressure, standby time, and thermal loss assumptions must be explicit.
- Thermal storage accounting: stored heat, released heat, standby heat loss, TCES chemical heat, solid sensible heat, and water sensible heat should not be double-counted.
- TCES water closure: dehydration water released and hydration water consumed should close or the imbalance must be explained.
- Material plausibility: TCES platform temperature must be reachable from the corresponding compressor outlet temperature.
- Stage matching: high-temperature storage should serve high-value early expansion stages unless a different architecture is justified.
- Baseline fairness: pure-water or packed-bed TES baseline should receive comparable heat exchanger assumptions and system boundaries.

## Novelty Discipline

Do not claim "first ever TCES + CAES" without a fresh literature check. Safer novelty framings usually include:

- Cascaded material-temperature matching for multistage AA-CAES.
- Hybrid TCES + sensible heat storage that reduces hot-water inventory.
- Reverse discharge matching of high-temperature TCES to early turbine stages.
- Exergy-based explanation of why thermochemical storage outperforms a sensible-heat baseline.

Use web search when the user asks for current literature, citations, latest work, journal positioning, or source-supported claims.

For a quick no-key metadata search, use:

```bash
python scripts/search_caes_literature.py --topic tces-caes --limit 10
python scripts/search_caes_literature.py --query "AA-CAES packed bed thermal storage exergy" --limit 10
python scripts/search_caes_literature.py --topic salt-hydrate-tces --from-year 2020 --min-score 20 --limit 10
```

Available preset topics:

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

## Writing Standards

Energy-system manuscripts should be concrete and quantitative:

- Prefer "RTE increased from 58.22% to 61.33%" over "efficiency improved significantly".
- Name the mechanism: higher turbine inlet temperature, reduced sensible heat loss, better temperature-grade matching, smaller hot-water inventory.
- Acknowledge simplifications: ideal gas, lumped cavern, finite heat-transfer model, material kinetics assumptions, omitted auxiliary equipment, simplified condensation/evaporation.
- Do not bury limitations; turn them into future-work or sensitivity-analysis paragraphs.

## Resource Guide

- `references/paper_readiness_rubric.md`: use for scoring current folders and listing missing work.
- `references/caes_literature_map.md`: use for literature positioning and citation-search targets.
- `references/figures_and_tables.md`: use for figure/table plans, color/style rules, and chart messages.
- `references/writing_patterns.md`: use for section-level prose, claim language, and limitation wording.
- `references/advanced_writing_templates.md`: use for Methods, exergy, validation, sensitivity, limitations, highlights, and reviewer-response drafting.
- `scripts/collect_caes_project_snapshot.py`: run to inventory files and detect likely MATLAB/Python entry points.
- `scripts/score_paper_readiness.py`: run to produce a heuristic paper-readiness score without binding to one result format.
- `scripts/search_caes_literature.py`: run no-key Crossref searches for CAES/TCES topics and optionally export JSON/BibTeX.
