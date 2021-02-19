.PHONY: format lint

format:
	black .
	black-nb .
	isort --profile black --line-length 79 .

lint: format
	flake8 .
	#pylint thoth_issue_predictor

.DEFAULT_GOAL := lint

.PHONY: black-ci isort-ci flake8-ci

black-ci:
	black --line-length 79 .
	black-nb --line-length 79 .

isort-ci:
	isort --profile black --line-length 79 .

flake8-ci:
	flake8 .

#pylint-ci:
#	pylint thoth_issue_predictor
