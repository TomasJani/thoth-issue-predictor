# Thoth Issue Predictor

![Lint](https://github.com/TomasJani/thoth-issue-predictor/workflows/CI/badge.svg)

The goal of this [project](https://github.com/TomasJani/thoth-issue-predictor) is to create a predictive model that can, based on data aggregated, spot patterns
causing issues in software stacks and predict which software stacks will likely not work without actually
running the application. An example of an issue can be a specific version of TensorFlow installed together
with a specific version of numpy that cause API incompatibility issues spotted on run time.

## Modules

This project consist of four submodules:
 - notebooks
 - preprocessing
 - evaluation
 - loader

Each module contains README.md with brief description and manual.

## Dataset

**Git LTS is required for downloading using git. Otherwise,
the [dataset](https://github.com/TomasJani/thoth-issue-predictor/blob/main/thoth_issue_predictor/datasets/dataset.zip) needs to be downloaded manually.
Move this archive file to `thoth_issue_predictor/dataset` folder.**

## Terminology

 - **Software stack** is a group of packages working together to achieve a common goal.
An example of a software stack is the package Tensorflow. Tensorflow contains a list
of dependencies that need to be installed and functional so the Tensorflow can work.

 - **Inspection** is resolved software stack.

## Run using Docker container

### Prerequisites

Docker with Docker buildkit.

Commands below work only if docker runs on root user.

### Docker build

```bash
export APP_NAME="thoth_issue_predictor"
export BUILD_DATE=$(date +'%Y-%m-%d %H:%M:%S')

DOCKER_BUILDKIT=1 docker build . \
       --tag "$APP_NAME" \
       --target deployment \
       --build-arg BUILD_DATE="$BUILD_DATE"  \
       --ssh default
```

### Docker run

```bash
export APP_NAME="thoth_issue_predictor"

docker run --net=host \
           --rm \
           --name "$APP_NAME"_cmd \
           --log-opt tag=$APP_NAME \
           --log-driver=journald \
           "$APP_NAME" \
           jupyter lab
```

Exploratory analysis is located in `thoth_issue_predictor/notebooks/InspectionsExploration.ipynb`

Data preprocessing, training and evaluation is located in `thoth_issue_predictor/notebooks/ThothIssuePredictor.ipynb`

## Run development environment

### Prerequisites

Python, Graphwiz and Pipenv

### Set-up development environment

```bash
pipenv install
```

### Run jupyter lab server
```bash
pipenv run jupyter lab
```

### Linting

Command for running all liters:
```bash
pipenv run make lint
```
