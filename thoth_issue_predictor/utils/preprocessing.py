"""Utility functions."""
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from parver import Version
from thoth.report_processing.components.inspection import AmunInspections

from thoth_issue_predictor.utils.utils import extract_zip_file

logger = logging.getLogger("thoth.report_processing.components.inspection")
logger.setLevel(logging.ERROR)


# TODO this is only temporary, create custom method for my DF later
def prepare_df(file_name):
    """Assemble issue DF with all data from inspections."""
    # TODO uncomment when files not present
    extract_zip_file(file_name, "./inspections/")

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

    # TODO this function can return just one dict
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


# TODO Ignored, will be refactored later
# pylint: disable=too-many-branches,too-complex
def create_python_version_packege_df(
    inspections_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any], List[str]]:
    """Create DF for predicting build/runtime issues."""
    python_packages_versions: Dict[str, Any] = {}
    python_packages_names = []
    python_indexes = ["unknown"]

    sws_df = inspections_df[
        [col for col in inspections_df.columns.values if "__index" in col]
    ]

    for c_name in sws_df.columns.values:
        if "__index" in c_name:
            python_packages_names.append(c_name.split("__")[2])

    columns_packages = ["requirements_locked___meta__requires__python_version"]
    for package in python_packages_names:
        columns_packages.append(
            "".join(["requirements_locked__default__", package, "__index"])
        )
        columns_packages.append(
            "".join(["requirements_locked__default__", package, "__version"])
        )

    python_packages_versions["python"] = []
    for _, row in inspections_df[columns_packages].iterrows():
        python_version = row["requirements_locked___meta__requires__python_version"]

        if pd.isnull(python_version):
            python_packages_versions["python"].append(0)
        else:
            python_packages_versions["python"].append(
                int(python_version.replace(".", ""))
            )

        for package in python_packages_names:
            version = row[
                "".join(["requirements_locked__default__", package, "__version"])
            ]

            index = row["".join(["requirements_locked__default__", package, "__index"])]

            if not pd.isnull(index) and (index not in python_indexes):
                python_indexes.append(index)

            if pd.isnull(version):
                if f"{package}_major" not in python_packages_versions.keys():
                    python_packages_versions[f"{package}_major"] = []
                    python_packages_versions[f"{package}_minor"] = []
                    python_packages_versions[f"{package}_patch"] = []
                    python_packages_versions[f"{package}_index"] = []

                python_packages_versions[f"{package}_major"].append(0)
                python_packages_versions[f"{package}_minor"].append(0)
                python_packages_versions[f"{package}_patch"].append(0)
                python_packages_versions[f"{package}_index"].append(0)

            else:
                if f"{package}_major" not in python_packages_versions.keys():
                    python_packages_versions[f"{package}_major"] = []
                    python_packages_versions[f"{package}_minor"] = []
                    python_packages_versions[f"{package}_patch"] = []
                    python_packages_versions[f"{package}_index"] = []

                try:
                    package_version = Version.parse(
                        version.replace("==", "")
                    ).normalize()
                except ValueError:
                    package_version = Version.parse("0.0.0")

                python_packages_versions[f"{package}_major"].append(
                    package_version.release[0]
                    if len(package_version.release) > 0
                    else 0
                )
                python_packages_versions[f"{package}_minor"].append(
                    package_version.release[1]
                    if len(package_version.release) > 1
                    else 0
                )
                python_packages_versions[f"{package}_patch"].append(
                    package_version.release[2]
                    if len(package_version.release) > 2
                    else 0
                )
                python_packages_versions[f"{package}_index"].append(
                    python_indexes.index(index)
                )

    return (
        pd.DataFrame(python_packages_versions),
        python_packages_versions,
        python_indexes,
    )
