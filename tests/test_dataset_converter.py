from __future__ import annotations

from pathlib import Path

import pandas as pd

from dataset_converter.core import aggregate_weekly_csv, find_input_files
from dataset_converter.pipeline import PipelineConfig, run_pipeline


def test_find_input_files(tmp_path: Path) -> None:
    (tmp_path / "soil_moisture_1983.csv").write_text("date,main_nile\n1983-01-01,1\n")
    (tmp_path / "rainfall_1983.csv").write_text("date,main_nile\n1983-01-01,2\n")

    matches = find_input_files(tmp_path, ".csv", "soil_moisture")

    assert len(matches) == 1
    assert matches[0].name == "soil_moisture_1983.csv"


def test_aggregate_weekly_csv(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    data = pd.DataFrame(
        {
            "date": [
                "2020-01-01",
                "2020-01-02",
                "2020-01-08",
                "2020-01-09",
            ],
            "main_nile": [1.0, 2.0, 3.0, 4.0],
        }
    )
    data.to_csv(input_dir / "soil_moisture.csv", index=False)

    output_path = tmp_path / "output" / "agg_soil_moisture.csv"
    aggregate_weekly_csv(
        input_dir=input_dir,
        output_path=output_path,
        variable_name="soil_moisture",
        subbasin="main_nile",
    )

    result = pd.read_csv(output_path)
    assert list(result.columns) == ["year", "week", "soil_moisture"]
    assert len(result) == 2
    assert result["soil_moisture"].tolist() == [3.0, 7.0]


def test_pipeline_creates_outputs(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    pd.DataFrame({"date": ["2024-01-01"], "main_nile": [5.0]}).to_csv(
        input_dir / "rainfall.csv", index=False
    )

    result = run_pipeline(
        PipelineConfig(
            input_dir=input_dir,
            output_dir=tmp_path / "output",
            variable_name="rainfall",
            subbasin="main_nile",
        )
    )

    assert result.aggregate_path.exists()
    assert result.merra_urls_path is None
