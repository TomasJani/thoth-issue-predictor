"""Helper for sending specification files to Thoth services."""
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from thoth_issue_predictor.loader.utils import post_parsed, write_to_file

logging.basicConfig(level=logging.INFO)


class BaseRequester(ABC):
    """Helper for sending specification files to Thoth services."""

    def __init__(self, url: str, specs_path: str, id_path: str):
        """Initialize object attributes."""
        self.url: str = url
        self.specs_path: str = specs_path
        self.id_path: str = id_path
        self.response_data: List[Tuple[Optional[str], int]] = []

    def sent_specification_requests(self):
        """Send specification retrieved from file to given service."""
        specification_files = list(Path(self.specs_path).rglob("*.json"))

        for file in specification_files:
            with open(file, "r") as spec_file:
                data = json.load(spec_file)

                response = post_parsed(self.url, data)
                self.save_to_ids(response)

    @abstractmethod
    def save_to_ids(self, response):
        """Add chosen fields from response to list of results."""

    def send_specifications(self):
        """Send specs from retrieved files to given service."""
        Path(self.id_path).mkdir(parents=True, exist_ok=True)
        self.sent_specification_requests()
        inspection_file_path = Path(f"{self.id_path}/{datetime.now()}.json")
        write_to_file(inspection_file_path, self.response_data)
