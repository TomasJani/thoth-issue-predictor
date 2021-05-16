"""Implementation of BaseRequester for DM service."""
from thoth_issue_predictor.loader.base_requester import BaseRequester
from thoth_issue_predictor.loader.config import DM_API, DM_ID_DIR, DM_SPECIFICATION_DIR


class DmRequester(BaseRequester):
    """Implementation of BaseRequester for DM service."""

    def __init__(self):
        """Initialize object attributes."""
        super().__init__(url=DM_API, specs_path=DM_SPECIFICATION_DIR, id_path=DM_ID_DIR)

    def save_to_ids(self, response):
        """Add chosen fields from response to list of results."""
        self.response_data.append(response.get("analysis_id"))


if __name__ == "__main__":
    requester = DmRequester()
    requester.send_specifications()
