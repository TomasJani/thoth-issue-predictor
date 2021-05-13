.PHONY: format lint precommit

format:
	black .
	black-nb .
	isort --profile black .

precommit:
	pre-commit run --all-files

lint: format precommit
	flake8 .

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
