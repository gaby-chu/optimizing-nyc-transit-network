"""Convert a raw MTA subway OD CSV to Parquet with snake_case columns.

Usage: python scripts/convert_mta_od.py data/raw/mta_od/mta_od_2026-01.csv
Writes data/interim/<same name>.parquet.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main(src):
    src = Path(src)
    od = pd.read_csv(src, thousands=",", low_memory=False)
    od.columns = od.columns.str.strip().str.lower().str.replace(" ", "_")
    # WKT point columns duplicate the lat/lon columns
    od = od.drop(columns=["origin_point", "destination_point"])
    od["timestamp"] = pd.to_datetime(od["timestamp"], format="%m/%d/%Y %I:%M:%S %p")
    od["day_of_week"] = od["day_of_week"].astype("category")
    for side in ["origin", "destination"]:
        od[f"{side}_station_complex_name"] = od[f"{side}_station_complex_name"].astype("category")

    out = ROOT / "data" / "interim" / f"{src.stem}.parquet"
    od.to_parquet(out, index=False)
    print(f"{len(od):,} rows -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
