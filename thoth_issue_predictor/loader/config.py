"""Loader configuration file."""

AMUN_API = "https://amun_api.com"
AMUN_STATUS = "https://amun_api.com/{id}/status"
AMUN_RESULT = "https://amun_api.com/{id}/job/{number}/result"
AMUN_SPECS = "https://amun_api.com/{id}/specification"
AMUN_BATCH = "https://amun_api.com/{id}/job/batch-size"

DM_API = "https://management_api.com/python"
DM_STATUS = "https://management_api.com/python/{id}/status"
DM_RESULT = "https://management_api.com/python/{id}/report"

AMUN_SPECIFICATION_DIR = (
    "path/thoth-issue-predictor/thoth_issue_predictor/loader/amun/specifications/"
)
AMUN_OUTPUT_DIR = (
    "path/thoth-issue-predictor/thoth_issue_predictor/loader/amun/inspections"
)
AMUN_ID_DIR = "path/thoth-issue-predictor/thoth_issue_predictor/loader/amun/ids"

DM_SPECIFICATION_DIR = (
    "path/thoth-issue-predictor/thoth_issue_predictor/loader/dm/specifications/"
)
DM_OUTPUT_DIR = "path/thoth-issue-predictor/thoth_issue_predictor/loader/dm/inspections"
DM_ID_DIR = "path/thoth-issue-predictor/thoth_issue_predictor/loader/dm/ids"

WAIT_TIME = 1
MAX_TRIES = 10
