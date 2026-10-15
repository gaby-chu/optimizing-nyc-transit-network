# optimizing-nyc-transit-network

This project routes NYC's observed multimodal travel demand (subway, Citi Bike, Uber/Lyft/taxi) over a multilayer network at minimum generalized cost, compares that optimal flow with actual travel, and tests which network changes close the gap. See the proposal in [docs/nyc_multimodal_proposal.md](docs/nyc_multimodal_proposal.md).

## Layout

```text
data/raw/        downloads as received (gitignored), one folder per source
data/interim/    cleaned Parquet, one per source
data/processed/  zone-level OD graphs, layer graphs, travel-time matrices
docs/            proposal and write-ups
notebooks/       numbered in pipeline order; run from notebooks/
src/nyctransit/  reusable functions
scripts/         download and conversion scripts
outputs/         figures and tables
references/      papers and data dictionaries
```

## Pipeline

Notebook numbers follow the proposal's Methods steps.

| Notebook | Proposal step | Status |
| --- | --- | --- |
| `01_supply_network` | 1. Multilayer supply network (walk, bike, street, subway, bus, zone connectors) | to do |
| `02_observed_od` | 2. Observed OD graphs by mode, January 2026 | weekday AM peak done; hour and day of week to add |
| `03_demand_structure` | 3–4. Mode-blind OD graph; hubs, communities, flow types | to do |
| `04_optimal_flow` | 5. Uncapacitated optimal flow (Dijkstra, generalized cost) | to do |
| `05_actual_vs_optimal` | 6–7. Actual vs. optimal; last-mile signature | to do |
| `06_crowding` | Second stage 1–2. Frank–Wolfe system optimum; price of crowding | to do |
| `07_gaps_interventions` | Second stage 3–4. True gaps; new station and added frequency | to do |
| `08_time_equity` | Second stage 5 and equity. Weekday vs. weekend, earlier years, income tiers | to do |

## Setup

```bash
uv sync
uv run python -m ipykernel install --user --name nyctransit
uv run python scripts/convert_mta_od.py data/raw/mta_od/mta_od_2026-01.csv
```
