# CAES Paper Readiness Rubric

Use this rubric to judge whether a CAES/AA-CAES/TCES project folder is ready for manuscript writing.

## Readiness Levels

### Level 0: Exploratory model only
- Code runs partially or not at all.
- Results are not reproducible from a single entry point.
- System boundary is unclear.
- No fair baseline.

Minimum next step: make the model executable and print a complete result summary.

### Level 1: Internal technical note
- Main model runs.
- Key results are printed.
- Parameters are mostly visible.
- Major physical assumptions are known.

Minimum next step: add model checks, result tables, and limitation notes.

### Level 2: Conference abstract or short paper
- Main comparison is reproducible.
- Baseline and proposed system share a fair boundary.
- At least one clear performance gain is shown.
- Basic figures can be generated.

Minimum next step: add literature positioning and sensitivity analysis.

### Level 3: Full journal draft
- Validated model against literature or experimental data.
- Thermodynamic and exergy analyses are both included.
- Sensitivity or parametric study supports design choices.
- Figures/tables tell a coherent story.
- Material parameters have citations.
- Limitations are explicit.

Minimum next step: polish writing, complete citations, and improve figure quality.

### Level 4: Submission-ready paper
- Model validation is defensible.
- Claims are fully matched to figures/tables.
- Novelty is positioned against current literature.
- Uncertainty/sensitivity analysis covers fragile assumptions.
- Economic, sizing, or practical feasibility analysis is included if the target journal expects it.
- Figures meet journal quality standards.

## Mandatory Evidence For CAES/TCES Papers

### System model
- Architecture diagram for charge, storage, and discharge.
- Pressure/temperature/mass-flow boundary table.
- Component equations for compressor, turbine, storage, heat exchangers, and TES/TCES.
- Clear RTE definition and time basis.

### Baseline fairness
- Same pressure range.
- Same charge/discharge duration or explicitly normalized energy basis.
- Same air mass flow basis or justified scaling.
- Same heat exchanger effectiveness or justified technology-specific values.
- Same standby time and loss assumptions where relevant.

### TCES-specific evidence
- Material temperature platform reachable from compressor outlet.
- Reaction enthalpy, water capacity, kinetic constants, and cycle degradation assumptions.
- Dehydration/hydration water balance.
- TCES heat share during charge and discharge.
- Bed pressure drop or a reason it is excluded.
- Discussion of condensation/evaporation and water management.

### Results expected
- RTE comparison.
- Compressor work and turbine work.
- Stage-by-stage compressor outlet temperatures.
- Stage-by-stage turbine inlet temperatures.
- Stored and released heat by medium.
- TES inventory or reactor volume comparison.
- Exergy destruction by component.
- Sensitivity analysis.

## Common Blocking Gaps

- Claiming TCES advantage with no exergy analysis.
- Material selection without literature-backed temperature ranges.
- Comparing TCES to an underdeveloped water-only baseline.
- Ignoring auxiliary energy for pumps/fans/water handling while claiming economic superiority.
- Using a single favorable operating point without sensitivity checks.
- Reporting RTE without validating the model against a known AA-CAES or CAES case.
- Using non-closed water balance in TCES hydration/dehydration.

## Minimum Full-Paper Package

For a robust journal manuscript, aim for:

- One architecture figure.
- One model validation figure/table.
- One baseline comparison table.
- One stage temperature figure.
- One heat/exergy flow figure.
- One sensitivity figure.
- One material selection table.
- One limitations/practical feasibility subsection.
