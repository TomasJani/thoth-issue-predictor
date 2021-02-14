import json
import logging
from pathlib import Path
from typing import Optional, Union

import requests


def _write_to_file(file_path: Path, data: Union[str, dict, list]):
    dir_name = file_path.parent
    dir_name.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)
        logging.info("Successfully written data into %s", file_path)


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
