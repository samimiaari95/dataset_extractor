# Dataset Converter

Dataset Converter is a Python project for turning raw climate and geospatial datasets into structured, analysis-ready CSV outputs. It centralizes the common tasks behind data preparation: finding files, aggregating daily time series into weekly summaries, and collecting remote dataset URLs for download workflows.

## Project goals

- Standardize messy data-conversion workflows.
- Remove hard-coded local paths and duplicated logic.
- Provide a reusable Python package with a small CLI.
- Make the project easy to install, run, and extend.

## Repository structure

```text
.
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── dataset_converter/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       └── downloaders.py
├── tests/
│   └── test_dataset_converter.py
├── legacy/
│   └── README.md
├── crop_tif_rasterio.py
├── download_data_scraper.py
├── download_urls.py
├── gdaltranslate_rasterio.py
├── ndvi_mod_irrigated_area.py
├── prepare_csv_data.py
├── river_discharge_copernicus.py
├── soil_moisture_merra.py
├── wind_speed_copernicus_nc.py
└── .gitignore
```

The files at the repository root are retained as historical or project-specific scripts. The supported and maintained workflow lives under the `src/dataset_converter` package.

## Installation

### Option 1: local editable install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### Option 2: install dependencies directly

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Quick usage

### Aggregate CSV inputs into weekly totals

```bash
dataset-converter aggregate ./data ./output/agg_soil_moisture.csv soil_moisture main_nile
```

This expects CSV files containing a `date` column and a subbasin column such as `main_nile`.

### List files matching a pattern

```bash
dataset-converter list-files ./data .csv soil_moisture --single
```

### Extract MERRA .nc4 URLs

```bash
dataset-converter download-urls ./data/merra_urls.txt "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXLND.5.12.4" \
  --start-year 1980 --end-year 2021
```

## Core modules

- `dataset_converter.core`: file discovery and aggregation logic.
- `dataset_converter.downloaders`: remote URL discovery for data sources.
- `dataset_converter.cli`: command-line interface for operational tasks.

## Testing

```bash
python -m pip install pytest
PYTHONPATH=src python -m pytest -q
```

## Notes on legacy scripts

The project originally contained a set of hard-coded, Windows-specific scripts for GIS and dataset extraction. Those scripts are not production-ready as-is and should be treated as historical examples unless they are intentionally reworked for a specific dataset pipeline. The refactored package is the supported interface going forward.

## License

This project is provided for research and internal data-preparation workflows. Update or extend the license terms as needed for your organization or publication context.
