"""Implementation of BaseRequester for Amun service."""
from thoth_issue_predictor.loader.base_requester import BaseRequester
from thoth_issue_predictor.loader.config import AMUN_API, ID_DIR, SPECIFICATION_DIR


class AmunRequester(BaseRequester):
    """Implementation of BaseRequester for Amun service."""

    def __init__(self):
        """Initialize object attributes."""
        super().__init__(url=AMUN_API, specs_path=SPECIFICATION_DIR, id_path=ID_DIR)

    def save_to_ids(self, response):
        """Add chosen fields from response to list of results."""
        self.response_data.append(
            (
                response.get("inspection_id"),
                response.get("parameters", {}).get("batch_size"),
            )
        )


if __name__ == "__main__":
    requester = AmunRequester()
    requester.send_specifications()
