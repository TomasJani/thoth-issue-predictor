"""Utils for loader module."""

import json
import logging
from pathlib import Path
from typing import Union

import requests


def _write_to_file(file_path: Path, data: Union[str, dict, list]):
    """Write json to file."""
    dir_name = file_path.parent
    dir_name.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)
        logging.info("Successfully written data into %s", file_path)


def get_parsed(url: str) -> dict:
    """Send GET request to url and parse data."""
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(
            "Get request to %s received %s status code.",
            url,
            response.status_code,
        )
        return dict()
    logging.info("Get request to %s was successful.", url)

    return json.loads(response.text)


def post_parsed(url: str, data: dict) -> dict:
    """Send POST request to url and parse data."""
    response = requests.post(url, json=data)
    if response.status_code != 202:
        logging.warning(
            "Post request to %s received %s status code.",
            url,
            response.status_code,
        )
        return dict()
    logging.info("Post request to %s was successful.", url)

    return json.loads(response.text)
