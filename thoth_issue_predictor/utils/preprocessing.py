""""Utility functions """

from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from thoth.report_processing.components import AmunInspections


# TODO this is only temporary, create custom method for my DF later
def prepare_df(file_name):
    # TODO uncomment when files not present
    # extract_zip_file(file_name)

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
        processed_inspection_runs=(
            processed_inspection_runs | failed_inspection_runs
        ),
    )

    (
        python_packages_dataframe,
        _,
        python_indexes,
    ) = create_python_version_packege_df(inspections_df=inspections_df)

    python_packages_dataframe = python_packages_dataframe.loc[
        (python_packages_dataframe != 0).any(axis=1)
    ]

    python_packages_dataframe["exit_code"] = inspections_df[
        "exit_code"
    ].astype("int")

    return python_packages_dataframe, python_indexes


# pylint: disable=R1260
# TODO Ignored, will be refactored later
def create_python_version_packege_df(
    inspections_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, Any], List[str]]:
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
        python_version = row[
            "requirements_locked___meta__requires__python_version"
        ]

        if pd.isnull(python_version):
            python_packages_versions["python"].append(0)
        else:
            python_packages_versions["python"].append(
                int(python_version.replace(".", ""))
            )

        for package in python_packages_names:
            version = row[
                "".join(
                    ["requirements_locked__default__", package, "__version"]
                )
            ]

            index = row[
                "".join(["requirements_locked__default__", package, "__index"])
            ]

            if not pd.isnull(index) and (index not in python_indexes):
                python_indexes.append(index)

            if pd.isnull(version):
                if package not in python_packages_versions.keys():
                    python_packages_versions[package] = []
                    python_packages_versions[f"{package}_index"] = []

                python_packages_versions[package].append(0)
                python_packages_versions[f"{package}_index"].append(0)

            else:
                if package not in python_packages_versions.keys():
                    python_packages_versions[package] = []
                    python_packages_versions[f"{package}_index"] = []

                try:
                    # TODO separate by . and normalize number of ciphers
                    package_version = int(
                        version.replace("==", "").replace(".", "")
                    )
                except ValueError:
                    package_version = 0

                python_packages_versions[package].append(package_version)
                python_packages_versions[f"{package}_index"].append(
                    python_indexes.index(index)
                )

    return (
        pd.DataFrame(python_packages_versions),
        python_packages_versions,
        python_indexes,
    )
