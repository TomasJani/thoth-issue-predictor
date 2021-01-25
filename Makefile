.PHONY: black isort format

format:
	black --line-length 79 .
	black-nb --line-length 79 .
	isort --profile black --line-length 79 .

lint: format
	flake8 .
	pylint thoth_issue_predictor

.DEFAULT_GOAL := lint
