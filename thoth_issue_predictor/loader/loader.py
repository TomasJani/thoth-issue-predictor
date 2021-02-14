import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from thoth_issue_predictor.loader.config import (
    AMUN_API,
    ID_DIR,
    OUTPUT_DIR,
    SPECIFICATION_DIR,
)
from thoth_issue_predictor.loader.utils import _write_to_file, send_post_amun

logging.basicConfig(level=logging.INFO)


def sent_specification_requests() -> list[tuple[Optional[str], int]]:
    responses = []
    specification_files = list(Path(SPECIFICATION_DIR).rglob("*.json"))

    for file in specification_files:
        with open(file, "r") as spec_file:
            data = json.load(spec_file)

            response = send_post_amun(AMUN_API, data)
            responses.append(
                (
                    response.get("inspection_id"),
                    response.get("parameters").get("batch_size"),
                )
            )

    return responses


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(ID_DIR).mkdir(parents=True, exist_ok=True)
    responses = sent_specification_requests()
    inspection_file_path = Path(f"{ID_DIR}/{datetime.now()}")
    _write_to_file(inspection_file_path, responses)


if __name__ == "__main__":
    main()
