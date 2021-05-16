"""Utilities for preprocessing model."""
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from thoth.report_processing.components.inspection import AmunInspections

from thoth_issue_predictor.preprocessing.config import DATASET_PATH, INSPECTIONS_PATH


def extract_zip_file(file_path: str, output_path: str) -> None:
    """Extract files from zip files."""
    with ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(path=output_path)


def prepare_df() -> pd.DataFrame:
    """Assemble issue DF with all data from inspections."""
    extract_zip_file(DATASET_PATH, INSPECTIONS_PATH)

    inspection = AmunInspections()

    current_path = Path.cwd()
    inspection_runs = inspection.aggregate_thoth_inspections_results(
        is_local=True,
        repo_path=current_path.joinpath("inspections"),
        store_files=[
            "specification",
            "results",
        ],
    )

    (
        processed_inspection_runs,
        failed_inspection_runs,
    ) = inspection.process_inspection_runs(
        inspection_runs,
    )

    inspections_df = inspection.create_inspections_dataframe(
        processed_inspection_runs={
            **processed_inspection_runs,
            **failed_inspection_runs,
        },
    )

    return inspections_df
