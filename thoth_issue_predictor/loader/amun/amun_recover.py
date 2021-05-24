"""Implementation of BaseRecover for Amun service."""
import logging
from pathlib import Path
from time import sleep
from typing import Tuple

from thoth_issue_predictor.loader.base_recover import BaseRecover
from thoth_issue_predictor.loader.config import (
    AMUN_BATCH,
    AMUN_ID_DIR,
    AMUN_OUTPUT_DIR,
    AMUN_RESULT,
    AMUN_SPECS,
    AMUN_STATUS,
)
from thoth_issue_predictor.loader.status import Status
from thoth_issue_predictor.loader.utils import get_parsed, write_to_file


class AmunRecover(BaseRecover):
    """Implementation of BaseRecover for Amun service."""

    def __init__(self):
        """Initialize object attributes."""
        super().__init__(
            inspections_path=AMUN_OUTPUT_DIR,
            ids_path=AMUN_ID_DIR,
            status_url=AMUN_STATUS,
            result_url=AMUN_RESULT,
        )
        self.specs_url = AMUN_SPECS
        self.batch_url = AMUN_BATCH

    def check_status(self, inspection_id: str) -> Status:
        """Get status of inspection with given id."""
        status_url = self.status_url.format(id=inspection_id)

        for n_try in range(self.max_tries):
            sleep(self.wait_time)
            response = get_parsed(status_url)
            workflow = response.get("status", {}).get("workflow")
            build = response.get("status", {}).get("build")
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

    def get_specification(self, inspection_id: str):
        """Get specification for given inspection id."""
        url = self.specs_url.format(id=inspection_id)
        response = get_parsed(url)
        specifications = response.get("specification", {})
        spec_file_path = Path(
            f"{self.inspections_path}/{inspection_id}/build/specification"
        )
        write_to_file(spec_file_path, specifications)

    def get_result(self, inspection_id: str, *args):
        """Get result and specification of inspection with given id.."""
        batch_size = args[0]
        self.get_specification(inspection_id)
        for batch_number in range(batch_size):
            for _ in range(self.max_tries):
                url = self.result_url.format(id=inspection_id, number=batch_number)
                response = get_parsed(url)
                inspection_file_path = Path(
                    f"{self.inspections_path}/{inspection_id}/results/{batch_number}/result"
                )
                if response is not None:
                    write_to_file(inspection_file_path, response.get("result", {}))
                    break

    def parse_ids_file(self, row) -> Tuple[str, int]:
        """Parse data from ids file."""
        if isinstance(row, str):
            inspection_id = row
            url = self.batch_url.format(id=inspection_id)
            batch_size = get_parsed(url).get("batch_size", 0)
        else:
            inspection_id, batch_size = row

        return inspection_id, batch_size


if __name__ == "__main__":
    recover = AmunRecover()
    recover.recover()
