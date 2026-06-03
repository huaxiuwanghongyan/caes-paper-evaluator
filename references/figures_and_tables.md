# Figures And Tables For CAES Papers

Use figures to prove mechanisms, not to decorate the paper.

## Core Figure Set

### Figure 1: System architecture
Message: how charge, storage, and discharge flow through compressor, TES/TCES, storage, turbine, and water loop.

Requirements:
- Separate charge and discharge arrows.
- Mark pressure boundaries and stage mapping.
- Show reverse TCES matching on discharge if used.
- Use consistent colors for air, water, TCES material, and electricity.

### Figure 2: Temperature-stage matching
Message: TCES material platforms match the compressor outlet temperature ladder and turbine reheat needs.

Plot:
- x-axis: stage number.
- y-axis: temperature.
- series: compressor outlet temperature, TCES platform range, turbine inlet TCES, turbine inlet baseline.

### Figure 3: Baseline performance comparison
Message: proposed system improves RTE, turbine output, released heat, or storage volume.

Use:
- grouped bars for RTE, turbine power, storage volume.
- annotate absolute values and differences.

### Figure 4: Heat flow split
Message: heat shifts from water sensible storage to TCES chemical storage.

Use:
- stacked bars for charge and discharge heat.
- separate TCES and water.

### Figure 5: Exergy destruction
Message: where losses decrease or move when TCES is used.

Use:
- stacked component bars or Grassmann/Sankey diagram.
- components: compressors, heat recovery, storage, TCES dehydration, TCES hydration, water storage, turbines.

### Figure 6: Sensitivity analysis
Message: advantage is robust, not a single tuned point.

Useful variables:
- TCES inventory scale.
- hot-water inventory.
- pressure upper limit.
- standby time.
- heat loss coefficient.
- compressor/turbine efficiency.
- TCES approach temperature.

## Essential Tables

### Table 1: System parameters
Include:
- pressure limits, mass flow, charge/discharge time, efficiencies, number of stages, ambient state, storage volume.

### Table 2: TCES material parameters
Include:
- material, type, temperature range, enthalpy, water capacity, molar mass, activation energy, heat capacity, bulk density, reference.

### Table 3: Result comparison
Include:
- RTE, compressor power, turbine power, stored heat, released heat, hot-water volume, cavern volume, water balance, TCES heat share.

### Table 4: Model validation
Include:
- variable, present model, literature/experiment, relative error, source.

## Visual Style

For energy-system papers:
- Prefer clean white background.
- Use 300-600 dpi for raster exports.
- Use vector PDF/SVG/EPS for line plots when possible.
- Avoid gradients, shadows, 3D bars, and rainbow color maps.
- Use consistent palette:
  - compressed air: blue
  - hot water/sensible heat: orange
  - TCES/chemical heat: green
  - electricity/work: dark gray or purple
  - losses: red or muted gray
- Use color-blind safe combinations when possible.
- Use line widths of 1.5-2 pt and font sizes readable at single-column width.

## Caption Pattern

Good captions state the claim:

`Stage-wise turbine inlet temperatures under TCES-assisted and water-only storage. TCES increases the inlet temperature of all four expansion stages, with the largest gains in EXP1 and EXP2 because high-temperature TCES is assigned to early high-pressure expansion.`

Avoid captions that only name the plot:

`Temperature comparison.`
