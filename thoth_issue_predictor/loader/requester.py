"""Helper for loading and retrieving inspections."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from thoth_issue_predictor.loader.config import (
    AMUN_API,
    ID_DIR,
    OUTPUT_DIR,
    SPECIFICATION_DIR,
)
from thoth_issue_predictor.loader.utils import write_to_file, post_parsed

logging.basicConfig(level=logging.INFO)


def sent_specification_requests() -> List[Tuple[Optional[str], int]]:
    """Send spec request to AMUN retrieved from files."""
    responses = []
    specification_files = list(Path(SPECIFICATION_DIR).rglob("*.json"))

    for file in specification_files:
        with open(file, "r") as spec_file:
            data = json.load(spec_file)

            response = post_parsed(AMUN_API, data)
            responses.append(
                (
                    response.get("inspection_id"),
                    response.get("parameters", {}).get("batch_size"),
                )
            )

    return responses


def send_specifications():
    """Send specs from retrieved files to Amun."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(ID_DIR).mkdir(parents=True, exist_ok=True)
    responses = sent_specification_requests()
    inspection_file_path = Path(f"{ID_DIR}/{datetime.now()}.json")
    print(responses)
    write_to_file(inspection_file_path, responses)


if __name__ == "__main__":
    send_specifications()
