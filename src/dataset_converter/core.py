from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd


def find_input_files(
    input_folder: str | Path,
    ext: str,
    keyword: str,
    onefile: bool = True,
) -> List[Path]:
    """Return files matching the requested extension and keyword."""
    folder = Path(input_folder)
    if not folder.exists():
        raise FileNotFoundError(f"Input folder does not exist: {folder}")

    matches = sorted(
        path
        for path in folder.iterdir()
        if path.is_file()
        and path.name.lower().endswith(ext.lower())
        and keyword.lower() in path.name.lower()
    )

    if not matches:
        raise FileNotFoundError(
            f"No files with extension '{ext}' and keyword '{keyword}' were found in {folder}."
        )

    if onefile:
        if len(matches) > 1:
            raise ValueError(
                f"Expected a single file matching '{keyword}', but found {len(matches)}: "
                + ", ".join(path.name for path in matches)
            )
        return [matches[0]]

    return matches


def aggregate_weekly_csv(
    input_dir: str | Path,
    output_path: str | Path,
    variable_name: str,
    subbasin: str,
    *,
    drop_leap_day: bool = True,
) -> pd.DataFrame:
    """Combine matching CSV files, drop leap-day rows, and aggregate by ISO week."""
    files = find_input_files(input_dir, ".csv", variable_name, onefile=False)
    if not files:
        raise FileNotFoundError(f"No CSV files found for variable '{variable_name}' in {input_dir}.")

    dataset = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
    if "date" not in dataset.columns:
        raise ValueError("Each CSV file must contain a 'date' column.")
    if subbasin not in dataset.columns:
        raise ValueError(f"Column '{subbasin}' not found in the input data.")

    dataset = dataset.copy()
    dataset["date"] = pd.to_datetime(dataset["date"], errors="coerce")
    dataset = dataset.dropna(subset=["date"]).reset_index(drop=True)

    if drop_leap_day:
        dataset = dataset[~((dataset["date"].dt.month == 2) & (dataset["date"].dt.day == 29))].copy()

    weekly = (
        dataset.assign(
            year=dataset["date"].dt.isocalendar().year,
            week=dataset["date"].dt.isocalendar().week,
        )
        .groupby(["year", "week"], as_index=False)[subbasin]
        .sum()
        .sort_values(["year", "week"])
        .reset_index(drop=True)
    )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    weekly.columns = ["year", "week", variable_name]
    weekly.to_csv(output_file, index=False)
    return weekly
