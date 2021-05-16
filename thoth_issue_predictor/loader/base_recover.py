"""Implement inspection recover for Thoth services."""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

from thoth_issue_predictor.loader.config import (
    AMUN_BATCH,
    AMUN_SPECS,
    MAX_TRIES,
    WAIT_TIME,
)
from thoth_issue_predictor.loader.status import Status

logging.basicConfig(level=logging.INFO)


class BaseRecover(ABC):
    """Implement inspection recover for Thoth services."""

    def __init__(
        self, inspections_path: str, ids_path: str, status_url: str, result_url: str
    ):
        """Initialize object attributes."""
        self.inspections_path: str = inspections_path
        self.ids_path: str = ids_path
        self.status_url: str = status_url
        self.result_url: str = result_url
        self.specs_url: str = AMUN_SPECS
        self.batch_url: str = AMUN_BATCH
        self.wait_time: int = WAIT_TIME
        self.max_tries: int = MAX_TRIES

    @abstractmethod
    def check_status(self, inspection_id: str) -> Status:
        """Get status of inspection with given id."""

    @abstractmethod
    def get_result(self, inspection_id: str, *args):
        """Get result and specification of inspection with given id.."""

    @abstractmethod
    def parse_ids_file(self, row):
        """Parse data from ids file."""

    def recover(self):
        """Load identification data from files and retrieve their results."""
        Path(self.inspections_path).mkdir(parents=True, exist_ok=True)
        id_files = list(Path(self.ids_path).glob("*.json"))
        id_file = max(id_files)
        with open(id_file, "r") as file:
            data = json.load(file)

        for row in data:
            inspection_id, *other = self.parse_ids_file(row)

            status = self.check_status(inspection_id)
            if status == Status.FINISHED:
                self.get_result(inspection_id, *other)
