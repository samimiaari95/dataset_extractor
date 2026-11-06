"""Dataset conversion utilities for geospatial and time-series data."""

from .core import aggregate_weekly_csv, find_input_files
from .pipeline import DatasetPipeline, PipelineConfig, PipelineResult, run_pipeline

__all__ = [
    "DatasetPipeline",
    "PipelineConfig",
    "PipelineResult",
    "aggregate_weekly_csv",
    "find_input_files",
    "run_pipeline",
]
__version__ = "0.1.0"
