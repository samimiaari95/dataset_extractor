# Dataset Extractor

Dataset Extractor converts daily climate and geospatial CSV data into
analysis-ready weekly summaries. It provides a reproducible pipeline, a Python
API, and lower-level commands for file discovery and MERRA URL harvesting.

The repository uses GitHub Actions for test and package-build checks. These
checks run on every push and pull request. GitHub Pages deployment is
intentionally not configured for this repository.

## Pipeline stages

The supported pipeline:

1. Finds `.csv` files whose names contain the selected variable name.
2. Combines the files and validates the `date` and subbasin columns.
3. Parses dates, removes invalid dates, and drops February 29 by default.
4. Aggregates the selected subbasin by ISO calendar year and week.
5. Writes `agg_<variable>.csv` to the output directory.
6. Optionally discovers MERRA `.nc4` links and writes `merra_urls.txt`.

The pipeline creates output directories automatically. URL discovery creates a
list only; it does not download the remote files.

## Install from the repository root

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

If activation is unavailable:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The editable install makes the package and its console commands available when
run from the repository root.

## Run the complete pipeline

From the repository root:

```powershell
python -m dataset_converter pipeline `
  .\data `
  .\output `
  soil_moisture `
  main_nile
```

The equivalent installed command is:

```powershell
dataset-pipeline .\data .\output soil_moisture main_nile
```

If `data/` contains files such as `soil_moisture_1983.csv` with columns
`date,main_nile`, the command creates:

```text
output/
└── agg_soil_moisture.csv
```

The output columns are `year`, `week`, and `soil_moisture`, where the final
column is the weekly sum for the requested subbasin.

### Optional MERRA URL discovery

```powershell
python -m dataset_converter pipeline `
  .\data `
  .\output `
  soil_moisture `
  main_nile `
  --merra-base-url "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXLND.5.12.4" `
  --start-year 1980 `
  --end-year 2021 `
  --start-month 1 `
  --end-month 12
```

This additionally creates `output/merra_urls.txt`. HTTP errors stop the run
and are reported rather than producing an incomplete success output.

### Pipeline options

| Option | Default | Description |
| --- | --- | --- |
| `--merra-base-url` | disabled | Enable MERRA URL discovery |
| `--start-year` | `1980` | First MERRA year, inclusive |
| `--end-year` | `2021` | Last MERRA year, inclusive |
| `--start-month` | `1` | First month, inclusive |
| `--end-month` | `12` | Last month, inclusive |
| `--keep-leap-day` | off | Keep February 29 rows |

## Python API

```python
from pathlib import Path

from dataset_converter import PipelineConfig, run_pipeline

result = run_pipeline(
    PipelineConfig(
        input_dir=Path("data"),
        output_dir=Path("output"),
        variable_name="soil_moisture",
        subbasin="main_nile",
    )
)

print(result.aggregate_path)
```

Set `merra_base_url` in `PipelineConfig` to enable URL discovery. The returned
`merra_urls_path` is otherwise `None`.

## Individual commands

The original lower-level commands remain available:

```powershell
python -m dataset_converter aggregate .\data .\output\weekly.csv soil_moisture main_nile
python -m dataset_converter list-files .\data .csv soil_moisture --single
python -m dataset_converter download-urls .\output\merra_urls.txt `
  "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXLND.5.12.4" `
  --start-year 1980 --end-year 2021
```

## Input and error behavior

- The input directory must exist and contain matching CSV files.
- Matching is case-insensitive and uses the variable name as a filename
  substring.
- Every input must contain `date` and the requested subbasin column.
- Invalid dates are ignored. Missing files or required columns raise errors and
  return a non-zero command status.
- Existing output files with the same names are replaced.

## Tests

```powershell
python -m pip install pytest
python -m pytest -q
```

The tests cover file discovery, weekly aggregation, and pipeline output
creation.

## Continuous integration

The [CI workflow](.github/workflows/ci.yml) runs the test suite on Python 3.10,
3.11, and 3.12. The [build workflow](.github/workflows/build.yml) builds the
source and wheel distributions and validates their metadata with Twine.
Neither workflow deploys files to GitHub Pages or publishes a package.

## Repository layout

```text
src/dataset_converter/
├── core.py          # File discovery and CSV aggregation
├── downloaders.py   # MERRA URL discovery
├── pipeline.py      # Pipeline configuration and orchestration
├── cli.py           # Command-line interface
└── __main__.py      # python -m dataset_converter
```

The scripts under `legacy/` are historical, dataset-specific examples and are
not invoked by the supported pipeline.
