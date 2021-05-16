.PHONY: format lint precommit

format:
	black .
	black-nb .
	isort --profile black .

precommit:
	pre-commit run --all-files

lint: format precommit
	flake8 . --ignore E2,W5 --select E,W,F,N --max-line-length=120

.DEFAULT_GOAL := lint

.PHONY: black-ci isort-ci flake8-ci

black-ci:
	black .
	black-nb .

isort-ci:
	isort --profile black .

flake8-ci:
	flake8 . --ignore E2,W5 --select E,W,F,N --max-line-length=120

aicoe-ci:
	precommit
