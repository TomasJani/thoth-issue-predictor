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
            f"Get request to {url} received {response.status_code} status code."
        )
        return
    logging.info(f"Get request to {url} was successful.")
    return json.loads(response.text)


def send_post_amun(url: str, data: dict) -> Optional[dict]:
    response = requests.post(url, json=data)
    if response.status_code != 202:
        logging.warning(
            f"Post request to {url} received {response.status_code} status code."
        )
        return
    logging.info(f"Post request to {url} was successful.")
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


def check_status(id: str) -> Status:
    status_url = AMUN_STATUS.format(id=id)

    for _ in range(MAX_TRIES):
        sleep(WAIT_TIME)
        response = send_get_amun(status_url)
        build = response.get("status").get("build")
        if build is not None and build.get("state") == "terminated":
            logging.info(f"Inspection with is {id} was loaded successfully.")
            return Status.FINISHED

    logging.warning(f"Inspection with id {id} was not loaded successfully.")
    return Status.UNFINISHED


def get_inspections(id: str, batch_size: int):
    for batch_number in range(batch_size):
        for _ in range(MAX_TRIES):
            sleep(WAIT_TIME)
            url = AMUN_RESULT.format(id=id, number=batch_number)
            response = send_get_amun(url)
            inspection_file_name = f"{OUTPUT_DIR}/{id}_{batch_number}.json"
            if response is not None:
                with open(inspection_file_name, "w") as inspection_file:
                    json.dump(response, inspection_file, indent=4, sort_keys=True)
                    logging.info(
                        f"Inspection batch with id {id} and number {batch_size} was saved to {inspection_file_name}."
                    )
                break


def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # id, batch_size = sent_specification_requests()
    id = "inspection-tf-conv1d-bcd487ef"
    batch_size = 1
    status = check_status(id)
    if status == Status.FINISHED:
        get_inspections(id, batch_size)


if __name__ == "__main__":
    main()
