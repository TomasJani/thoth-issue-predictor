"""Loader configuration file."""

AMUN_API = "https://amun.moc.thoth-station.ninja/api/v1/inspect"
AMUN_STATUS = "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/status"
AMUN_RESULT = (
    "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/job/{number}/result"
)
AMUN_SPECS = "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/specification"
AMUN_BATCH = "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/job/batch-size"

DM_API = "https://management.moc.thoth-station.ninja/api/v1/dependency-monkey/python"
DM_STATUS = "https://management.moc.thoth-station.ninja/api/v1/dependency-monkey/python/{id}/status"
DM_RESULT = "https://management.moc.thoth-station.ninja/api/v1/dependency-monkey/python/{id}/report"

SPECIFICATION_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/amun/specifications/"
OUTPUT_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/amun/inspections"
ID_DIR = (
    "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/amun/ids"
)

DM_SPECIFICATION_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/dm/specifications/"
DM_OUTPUT_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/dm/inspections"
DM_ID_DIR = (
    "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/dm/ids"
)

WAIT_TIME = 1
MAX_TRIES = 10
