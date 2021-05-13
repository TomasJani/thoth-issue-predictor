from thoth_issue_predictor.loader.config import AMUN_API, ID_DIR, SPECIFICATION_DIR
from thoth_issue_predictor.loader.requester import BaseRequester


class AmunRequester(BaseRequester):
    def __init__(self):
        super().__init__(url=AMUN_API, specs_path=SPECIFICATION_DIR, id_path=ID_DIR)

    def save_to_ids(self, response):
        self.response_data.append(
            (
                response.get("inspection_id"),
                response.get("parameters", {}).get("batch_size"),
            )
        )


if __name__ == "__main__":
    requester = AmunRequester()
    requester.send_specifications()
