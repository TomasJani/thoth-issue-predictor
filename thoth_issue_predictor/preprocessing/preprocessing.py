"""Prepares achieved dataset into structure which is possible to process with model."""
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from parver import Version
from thoth.report_processing.components import AmunInspections

from thoth_issue_predictor.preprocessing.config import DATASET_PATH, INSPECTIONS_PATH
from thoth_issue_predictor.preprocessing.utils import extract_zip_file

logger = logging.getLogger("thoth.report_processing.components.inspection")
logger.setLevel(logging.ERROR)


class Preprocessing:
    """Implementation of preprocessing class for predictive model."""

    def __init__(self):
        """Initialize object attributes."""
        self.inspections_df: pd.DataFrame = None
        self.python_packages_versions: Dict[str, Any] = {"python": []}
        self.python_indexes: List[str] = ["unknown"]
        self.python_packages_names: List[str] = []

    def prepare_df(
        self, dataset_path: str = DATASET_PATH, inspections_path: str = INSPECTIONS_PATH
    ) -> pd.DataFrame:
        """Assemble dataframe with all data from inspections."""
        extract_zip_file(dataset_path, inspections_path)
        inspection_runs = self._aggregate_inspections()
        processed_inspection_runs = self._process_inspections(inspection_runs)
        inspections_df = AmunInspections().create_inspections_dataframe(
            processed_inspection_runs=processed_inspection_runs,
        )
        self.inspections_df = inspections_df
        return inspections_df

    def create_df(self) -> Tuple[pd.DataFrame, List[str]]:
        """Create DF for predicting build/runtime issues."""
        columns_packages = self._get_columns_names()
        software_stacks = self.inspections_df[columns_packages].iterrows()

        for _, row in software_stacks:
            self._add_python_version(row)
            self._add_packages(row)

        return (
            pd.DataFrame(self.python_packages_versions),
            self.python_indexes,
        )

    def _process_inspections(self, inspection_runs):
        (
            processed_inspection_runs,
            failed_inspection_runs,
        ) = AmunInspections().process_inspection_runs(
            inspection_runs,
        )
        return {
            **processed_inspection_runs,
            **failed_inspection_runs,
        }

    def _aggregate_inspections(self):
        current_path = Path.cwd()
        inspection_runs = AmunInspections().aggregate_thoth_inspections_results(
            is_local=True,
            repo_path=current_path.joinpath("inspections"),
            store_files=[
                "specification",
                "results",
            ],
        )
        return inspection_runs

    def _add_python_version(self, row: Dict):
        """Add python version to dataframe."""
        python_version = row["requirements_locked___meta__requires__python_version"]
        if pd.isnull(python_version):
            self.python_packages_versions["python"].append(0)
        else:
            self.python_packages_versions["python"].append(
                int(python_version.replace(".", ""))
            )

    def _add_packages(self, row: Dict):
        """Add packages info to dataframe."""
        for package in self.python_packages_names:
            package_version = row[f"requirements_locked__default__{package}__version"]

            package_index = row[f"requirements_locked__default__{package}__index"]

            has_new_index = not pd.isnull(package_index) and (
                package_index not in self.python_indexes
            )
            if has_new_index:
                self.python_indexes.append(package_index)

            is_missing_package = pd.isnull(package_version)
            if is_missing_package:
                self._add_missing_package(package)
            else:
                self._save_package(package, package_index, package_version)

    def _save_package(self, package: str, package_index: str, package_version: str):
        """Parse and add packages info to dataframe."""
        has_version = f"{package}_major" in self.python_packages_versions.keys()
        if not has_version:
            self._add_package_column(package)

        package_version = self._parse_version(package_version)

        self._add_major(package, package_version)
        self._add_minor(package, package_version)
        self._add_micro(package, package_version)
        self._add_version(package, package_index)

    def _add_version(self, package, package_index):
        """Add version to dataframe."""
        self.python_packages_versions[f"{package}_index"].append(
            self.python_indexes.index(package_index)
        )

    def _add_micro(self, package, package_version):
        """Add micro version to dataframe."""
        self.python_packages_versions[f"{package}_micro"].append(
            package_version.release[2] if len(package_version.release) > 2 else 0
        )

    def _add_minor(self, package, package_version):
        """Add minor version to dataframe."""
        self.python_packages_versions[f"{package}_minor"].append(
            package_version.release[1] if len(package_version.release) > 1 else 0
        )

    def _add_major(self, package, package_version):
        """Add major version to dataframe."""
        self.python_packages_versions[f"{package}_major"].append(
            package_version.release[0] if len(package_version.release) > 0 else 0
        )

    def _add_package_column(self, package: str):
        """Create new columns for given package."""
        self.python_packages_versions[f"{package}_major"] = []
        self.python_packages_versions[f"{package}_minor"] = []
        self.python_packages_versions[f"{package}_micro"] = []
        self.python_packages_versions[f"{package}_index"] = []

    @staticmethod
    def _parse_version(package_version: str):
        """Parse release part from version string."""
        try:
            package_version = Version.parse(
                package_version.replace("==", "")
            ).normalize()
        except ValueError:
            package_version = Version.parse("0.0.0")
        return package_version

    def _add_missing_package(self, package: str):
        """Create new columns for package thar is not present."""
        if f"{package}_major" not in self.python_packages_versions.keys():
            self._add_package_column(package)
        self._set_defaults(package)

    def _set_defaults(self, package: str):
        """Add default values to package."""
        self.python_packages_versions[f"{package}_major"].append(0)
        self.python_packages_versions[f"{package}_minor"].append(0)
        self.python_packages_versions[f"{package}_micro"].append(0)
        self.python_packages_versions[f"{package}_index"].append(0)

    def _get_columns_names(self) -> List[str]:
        """Get names of packages from inspection dataframe."""
        columns_packages = ["requirements_locked___meta__requires__python_version"]
        sws_df = self.inspections_df[
            [col for col in self.inspections_df.columns.values if "__index" in col]
        ]
        for c_name in sws_df.columns.values:
            if "__index" in c_name:
                self.python_packages_names.append(c_name.split("__")[2])
        for package in self.python_packages_names:
            columns_packages.append(f"requirements_locked__default__{package}__index")
            columns_packages.append(f"requirements_locked__default__{package}__version")
        return columns_packages
