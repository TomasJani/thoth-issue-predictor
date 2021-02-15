import json
import logging
from pathlib import Path
from time import sleep

from thoth_issue_predictor.loader.config import (
    AMUN_BATCH,
    AMUN_RESULT,
    AMUN_SPECS,
    AMUN_STATUS,
    ID_DIR,
    MAX_TRIES,
    OUTPUT_DIR,
    WAIT_TIME,
)
from thoth_issue_predictor.loader.status import Status
from thoth_issue_predictor.loader.utils import _write_to_file, send_get_amun

logging.basicConfig(level=logging.INFO)


def check_status(inspection_id: str) -> Status:
    status_url = AMUN_STATUS.format(id=inspection_id)

    for n_try in range(MAX_TRIES):
        sleep(WAIT_TIME)
        response = send_get_amun(status_url)
        workflow = response.get("status").get("workflow")
        build = response.get("status").get("build")
        if (build is not None and build.get("finished_at") is not None) or (
            workflow is not None and workflow.get("finishedAt") is not None
        ):
            logging.info(
                "Inspection with id %s was loaded successfully.", inspection_id
            )
            return Status.FINISHED

        logging.info(
            "Inspection with is %s was not loaded on %s try.",
            inspection_id,
            (n_try + 1),
        )

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


def recover():
    id_files = list(Path(ID_DIR).glob("*.json"))
    id_file = max(id_files)
    with open(id_file, "r") as file:
        data = json.load(file)

    for row in data:
        if isinstance(row, str):
            inspection_id = row
            url = AMUN_BATCH.format(id=inspection_id)
            batch_size = send_get_amun(url).get("batch_size")
        else:
            inspection_id, batch_size = row

        status = check_status(inspection_id)
        if status == Status.FINISHED:
            get_specification(inspection_id)
            get_result(inspection_id, batch_size)


if __name__ == "__main__":
    recover()
