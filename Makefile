.PHONY: format lint precommit

format:
	black .
	black-nb .
	isort --profile black .

lint: format
	flake8 .
	#pylint thoth_issue_predictor

precommit:
	pre-commit run --all-files
	pre-commit run --all-files

.DEFAULT_GOAL := lint

.PHONY: black-ci isort-ci flake8-ci

black-ci:
	black .
	black-nb .

isort-ci:
	isort --profile black .

flake8-ci:
	flake8 .

aicoe-ci:
	precommit
