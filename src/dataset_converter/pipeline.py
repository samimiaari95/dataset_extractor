from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .core import aggregate_weekly_csv
from .downloaders import save_merra_urls


@dataclass(frozen=True)
class PipelineConfig:
    """Configuration for one reproducible dataset-conversion run."""

    input_dir: Path
    output_dir: Path
    variable_name: str
    subbasin: str
    merra_base_url: str | None = None
    start_year: int = 1980
    end_year: int = 2021
    start_month: int = 1
    end_month: int = 12
    drop_leap_day: bool = True


@dataclass(frozen=True)
class PipelineResult:
    """Paths produced by a pipeline run."""

    aggregate_path: Path
    merra_urls_path: Path | None = None


class DatasetPipeline:
    """Run the supported conversion stages in a predictable order."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config

    def run(self) -> PipelineResult:
        """Aggregate local CSV files and optionally collect MERRA download URLs."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        aggregate_path = self.config.output_dir / f"agg_{self.config.variable_name}.csv"
        aggregate_weekly_csv(
            input_dir=self.config.input_dir,
            output_path=aggregate_path,
            variable_name=self.config.variable_name,
            subbasin=self.config.subbasin,
            drop_leap_day=self.config.drop_leap_day,
        )

        merra_urls_path: Path | None = None
        if self.config.merra_base_url:
            merra_urls_path = self.config.output_dir / "merra_urls.txt"
            save_merra_urls(
                merra_urls_path,
                self.config.merra_base_url,
                start_year=self.config.start_year,
                end_year=self.config.end_year,
                start_month=self.config.start_month,
                end_month=self.config.end_month,
            )

        return PipelineResult(aggregate_path, merra_urls_path)


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    """Convenience function for applications and notebooks."""
    return DatasetPipeline(config).run()
