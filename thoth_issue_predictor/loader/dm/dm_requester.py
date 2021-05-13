from thoth_issue_predictor.loader.config import DM_API, DM_ID_DIR, DM_SPECIFICATION_DIR
from thoth_issue_predictor.loader.requester import BaseRequester


class DmRequester(BaseRequester):
    def __init__(self):
        super().__init__(url=DM_API, specs_path=DM_SPECIFICATION_DIR, id_path=DM_ID_DIR)

    def save_to_ids(self, response):
        self.response_data.append(response.get("analysis_id"))


if __name__ == "__main__":
    requester = DmRequester()
    requester.send_specifications()
