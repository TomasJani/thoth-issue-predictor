AMUN_API = "https://amun.moc.thoth-station.ninja/api/v1/inspect"
AMUN_STATUS = "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/status"
AMUN_RESULT = "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/job/{number}/result"
AMUN_SPECS = (
    "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/specification"
)
AMUN_BATCH = (
    "https://amun.moc.thoth-station.ninja/api/v1/inspect/{id}/job/batch-size"
)

SPECIFICATION_DIR = "./specifications"
OUTPUT_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/inspections"
ID_DIR = "/home/tjanicek/thesis/thoth-issue-predictor/thoth_issue_predictor/loader/ids"
WAIT_TIME = 1
MAX_TRIES = 10
