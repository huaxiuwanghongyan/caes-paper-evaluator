# CAES Literature Map

Use this file to position CAES/AA-CAES/TCES papers. Verify exact bibliographic details with web search or reference managers before final citation.

## Search Themes

For a quick metadata search, run:

```bash
python scripts/search_caes_literature.py --topic aa-caes-thermal-storage --limit 10
python scripts/search_caes_literature.py --topic tces-caes --limit 10
python scripts/search_caes_literature.py --topic salt-hydrate-tces --from-year 2020 --min-score 20 --limit 10
```

Use `--cache references/caes_literature_cache.json` or `--bibtex references/caes_core_bibliography.bib` when the user wants a local seed bibliography.

### AA-CAES thermal storage
Search terms:
- `adiabatic compressed air energy storage thermal energy storage packed bed`
- `AA-CAES thermal energy storage review`
- `dynamic simulation adiabatic compressed air energy storage integrated thermal storage`
- `compressed air energy storage sensible heat storage water tank`

Use these papers to support:
- Why thermal storage is central to AA-CAES.
- Typical RTE ranges.
- Packed-bed, water, oil, molten salt, PCM, and cascade TES comparisons.
- Component-level models and validation data.

### CAES exergy analysis
Search terms:
- `exergy analysis adiabatic compressed air energy storage`
- `exergy destruction AA-CAES thermal storage`
- `cascade phase change material adiabatic compressed air energy storage exergy`

Use these papers to support:
- Component exergy equations.
- Why temperature-grade matching matters.
- Grassmann/Sankey-style exergy flow diagrams.

### TCES and salt hydrates
Search terms:
- `thermochemical energy storage salt hydrates review magnesium chloride magnesium sulfate`
- `zeolite 13X water thermochemical energy storage dehydration temperature`
- `MgCl2 6H2O thermochemical heat storage dehydration hydration`
- `MgSO4 water thermochemical energy storage kinetics`
- `modified Mg(OH)2 MgO thermochemical heat storage low temperature`

Use these papers to support:
- Material temperature ranges.
- Reaction enthalpy and water capacity.
- Cycling stability.
- Kinetic limitations and hydration/dehydration hysteresis.
- Practical risks: corrosion, agglomeration, deliquescence, HCl formation, slow hydration.

### TCES + CAES coupling
Search terms:
- `thermochemical heat recuperation compressed air energy storage`
- `compressed air energy storage thermochemical energy storage`
- `A-CAES thermochemical storage`

Use these papers carefully:
- They may show that TCES-CAES coupling is not completely absent.
- Position novelty as a specific architecture, material cascade, matched thermal-grade strategy, or validated comparison, not as an unsupported first-ever claim.

## Safer Novelty Phrases

Use:
- "This work investigates a cascaded TCES architecture tailored to the temperature ladder of multistage AA-CAES."
- "The contribution lies in stage-wise material matching and a fair comparison against a sensible hot-water baseline."
- "The model quantifies how TCES shifts heat recovery from sensible storage to higher-grade chemical storage."

Avoid unless verified:
- "No previous study has investigated TCES in CAES."
- "This is the first TCES-CAES system."
- "The proposed material set is optimal."

## Typical Reference Categories Needed

For introduction:
- CAES/AA-CAES review.
- Thermal storage in CAES review.
- TCES/salt hydrate review.
- Existing TCES-CAES or thermochemical recuperation work.

For methods:
- Compressor/turbine isentropic efficiency modeling.
- Packed-bed or water heat exchanger model.
- TCES kinetic and equilibrium model.
- Cavern/storage thermodynamic model.

For discussion:
- Exergy analysis in AA-CAES.
- TES material cost or energy density.
- Salt hydrate/adsorbent stability and practical limitations.
