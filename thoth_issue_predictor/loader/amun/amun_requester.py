"""Implementation of BaseRequester for Amun service."""
from thoth_issue_predictor.loader.base_requester import BaseRequester
from thoth_issue_predictor.loader.config import (
    AMUN_API,
    AMUN_ID_DIR,
    AMUN_SPECIFICATION_DIR,
)


class AmunRequester(BaseRequester):
    """Implementation of BaseRequester for Amun service."""

    def __init__(self):
        """Initialize object attributes."""
        super().__init__(
            url=AMUN_API, specs_path=AMUN_SPECIFICATION_DIR, id_path=AMUN_ID_DIR
        )

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
