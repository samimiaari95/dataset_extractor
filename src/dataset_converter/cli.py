from __future__ import annotations

import argparse
from pathlib import Path

from .core import aggregate_weekly_csv, find_input_files
from .downloaders import save_merra_urls


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dataset conversion utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    aggregate = subparsers.add_parser("aggregate", help="Aggregate daily CSV data into weekly totals.")
    aggregate.add_argument("input_dir", type=Path, help="Directory containing the source CSV files.")
    aggregate.add_argument("output_path", type=Path, help="Destination CSV file for the aggregated data.")
    aggregate.add_argument("variable_name", help="Filename keyword used to find the input files.")
    aggregate.add_argument("subbasin", help="Column name to aggregate for the target subbasin.")

    files = subparsers.add_parser("list-files", help="List files matching a keyword and extension.")
    files.add_argument("input_dir", type=Path)
    files.add_argument("extension", default=".csv")
    files.add_argument("keyword")
    files.add_argument("--single", action="store_true", help="Require exactly one file.")

    download = subparsers.add_parser("download-urls", help="Download the list of MERRA NC4 URLs.")
    download.add_argument("output_path", type=Path)
    download.add_argument("base_url")
    download.add_argument("--start-year", type=int, default=1980)
    download.add_argument("--end-year", type=int, default=2021)
    download.add_argument("--start-month", type=int, default=1)
    download.add_argument("--end-month", type=int, default=12)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "aggregate":
        aggregate_weekly_csv(
            input_dir=args.input_dir,
            output_path=args.output_path,
            variable_name=args.variable_name,
            subbasin=args.subbasin,
        )
        return 0

    if args.command == "list-files":
        matches = find_input_files(args.input_dir, args.extension, args.keyword, onefile=args.single)
        for match in matches:
            print(match)
        return 0

    if args.command == "download-urls":
        save_merra_urls(
            args.output_path,
            args.base_url,
            start_year=args.start_year,
            end_year=args.end_year,
            start_month=args.start_month,
            end_month=args.end_month,
        )
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
