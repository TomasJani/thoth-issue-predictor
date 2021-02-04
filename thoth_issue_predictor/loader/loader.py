import glob
import json
import logging
from pathlib import Path
from time import sleep
from typing import Optional

import requests

from thoth_issue_predictor.loader.config import (
    AMUN_API,
    AMUN_RESULT,
    AMUN_STATUS,
    MAX_TRIES,
    OUTPUT_DIR,
    SPECIFICATION_DIR,
    WAIT_TIME,
)
from thoth_issue_predictor.loader.status import Status


def send_get_amun(url: str) -> Optional[dict]:
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(
            "Get request to %s received %s status code.",
            url,
            response.status_code,
        )
        return None
    logging.info("Get request to %s was successful.", url)
    return json.loads(response.text)


def send_post_amun(url: str, data: dict) -> Optional[dict]:
    response = requests.post(url, json=data)
    if response.status_code != 202:
        logging.warning(
            "Post request to %s received %s status code.",
            url,
            response.status_code,
        )
        return None
    logging.info("Post request to %s was successful.", url)
    return json.loads(response.text)


def sent_specification_requests() -> (Optional[str], int):
    specification_files = glob.glob(f"{SPECIFICATION_DIR}/*.json")

    for file in specification_files:
        with open(file, "r") as spec_file:
            data = json.load(spec_file)

            response = send_post_amun(AMUN_API, data)

    return response.get("inspection_id"), response.get("parameters").get(
        "batch_size"
    )


def check_status(inspecion_id: str) -> Status:
    status_url = AMUN_STATUS.format(id=inspecion_id)

    for _ in range(MAX_TRIES):
        sleep(WAIT_TIME)
        response = send_get_amun(status_url)
        build = response.get("status").get("build")
        if build is not None and build.get("state") == "terminated":
            logging.info(
                "Inspection with is %s was loaded successfully.", inspecion_id
            )
            return Status.FINISHED

    logging.warning(
        "Inspection with id %s was not loaded successfully.", inspecion_id
    )
    return Status.UNFINISHED


def get_inspections(inspection_id: str, batch_size: int):
    for batch_number in range(batch_size):
        for _ in range(MAX_TRIES):
            sleep(WAIT_TIME)
            url = AMUN_RESULT.format(id=inspection_id, number=batch_number)
            response = send_get_amun(url)
            inspection_file_name = (
                f"{OUTPUT_DIR}/{inspection_id}_{batch_number}.json"
            )
            if response is not None:
                with open(inspection_file_name, "w") as inspection_file:
                    json.dump(
                        response, inspection_file, indent=4, sort_keys=True
                    )
                    logging.info(
                        "Inspection batch with id %s and number %s was saved to %s.",
                        inspection_id,
                        batch_size,
                        inspection_file_name,
                    )
                break


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # inspection_id, batch_size = sent_specification_requests()
    inspection_id = "inspection-tf-conv1d-bcd487ef"
    batch_size = 1
    status = check_status(inspection_id)
    if status == Status.FINISHED:
        get_inspections(inspection_id, batch_size)


if __name__ == "__main__":
    main()
