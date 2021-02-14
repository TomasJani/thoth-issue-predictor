import glob
import json
import logging
from pathlib import Path
from time import sleep
from typing import Optional

from thoth_issue_predictor.loader.config import (
    AMUN_API,
    AMUN_RESULT,
    AMUN_SPECS,
    AMUN_STATUS,
    MAX_TRIES,
    OUTPUT_DIR,
    SPECIFICATION_DIR,
    WAIT_TIME,
)
from thoth_issue_predictor.loader.status import Status
from thoth_issue_predictor.loader.utils import (
    _write_to_file,
    send_get_amun,
    send_post_amun,
)

logging.basicConfig(level=logging.INFO)


def sent_specification_requests() -> list[tuple[Optional[str], int]]:
    responses = []
    specification_files = glob.glob(f"{SPECIFICATION_DIR}/*.json")

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


def check_status(inspection_id: str) -> Status:
    status_url = AMUN_STATUS.format(id=inspection_id)

    for _ in range(MAX_TRIES):
        sleep(WAIT_TIME)
        response = send_get_amun(status_url)
        workflow = response.get("status").get("workflow")
        build = response.get("status").get("build")
        if (build is not None and workflow.get("finished_at") is not None) or (
            workflow is not None and workflow.get("finishedAt") is not None
        ):
            logging.info(
                "Inspection with is %s was loaded successfully.", inspection_id
            )
            return Status.FINISHED

    logging.warning(
        "Inspection with id %s was not loaded successfully.", inspection_id
    )
    return Status.UNFINISHED


def get_specification(inspection_id: str):
    url = AMUN_SPECS.format(id=inspection_id)
    response = send_get_amun(url)
    specifications = response.get("specification")
    spec_file_path = Path(f"{OUTPUT_DIR}/{inspection_id}/build/specification")
    _write_to_file(spec_file_path, specifications)


def get_result(inspection_id: str, batch_size: int):
    for batch_number in range(batch_size):
        for _ in range(MAX_TRIES):
            url = AMUN_RESULT.format(id=inspection_id, number=batch_number)
            response = send_get_amun(url)
            inspection_file_path = Path(
                f"{OUTPUT_DIR}/{inspection_id}/results/{batch_number}/result"
            )
            if response is not None:
                _write_to_file(inspection_file_path, response.get("result"))
                break


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    responses = sent_specification_requests()
    # responses = [("inspection-tf-conv1d-6a493bdf", 5)]
    for inspection_id, batch_size in responses:
        status = check_status(inspection_id)
        if status == Status.FINISHED:
            get_specification(inspection_id)
            get_result(inspection_id, batch_size)


if __name__ == "__main__":
    main()
