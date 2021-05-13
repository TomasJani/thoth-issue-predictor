import logging
from pathlib import Path
from time import sleep
from typing import List

from thoth_issue_predictor.loader.config import (
    DM_ID_DIR,
    DM_OUTPUT_DIR,
    DM_RESULT,
    DM_STATUS,
)
from thoth_issue_predictor.loader.recover import BaseRecover
from thoth_issue_predictor.loader.status import Status
from thoth_issue_predictor.loader.utils import get_parsed, write_to_file


class DmRecover(BaseRecover):
    def __init__(self):
        super().__init__(
            inspections_path=DM_OUTPUT_DIR,
            ids_path=DM_ID_DIR,
            status_url=DM_STATUS,
            result_url=DM_RESULT,
        )

    def check_status(self, inspection_id: str) -> Status:
        status_url = self.status_url.format(id=inspection_id)

        for n_try in range(self.max_tries):
            sleep(self.wait_time)
            response = get_parsed(status_url)
            state = response.get("status", {}).get("state")
            if state is not None and "succeeded" in state:
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

    def get_result(self, inspection_id: str, *args):
        for _ in range(self.max_tries):
            url = self.result_url.format(id=inspection_id)
            response = get_parsed(url)
            inspection_file_path = Path(f"{self.inspections_path}/{inspection_id}.json")
            if response is not None:
                write_to_file(inspection_file_path, response.get("report", {}))
                break

    def parse_ids_file(self, row) -> List[str]:
        return [row]


if __name__ == "__main__":
    recover = DmRecover()
    recover.recover()
