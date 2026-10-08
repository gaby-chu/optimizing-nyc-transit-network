# optimizing-nyc-transit-network
This project aims to optimize NYC's multimodal transit based on changing commute patterns and evaluate the feasibility of the optimal network.

## Layout

```
data/raw/        downloads as received (gitignored), one folder per source
data/interim/    cleaned Parquet, one per source
data/processed/  zone-level OD graphs, layer graphs, travel-time matrices
notebooks/       numbered in pipeline order; run from notebooks/
src/nyctransit/  reusable functions
scripts/         download and conversion scripts
outputs/         figures and tables
references/      papers and data dictionaries
```

## Setup

```
uv sync
uv run python -m ipykernel install --user --name nyctransit
uv run python scripts/convert_mta_od.py data/raw/mta_od/mta_od_2026-01.csv
```
