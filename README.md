# Thoth Issue Predictor

![Lint](https://github.com/TomasJani/thoth-issue-predictor/workflows/CI/badge.svg)

The goal of this thesis is to create a predictive model that can, based on data aggregated, spot patterns
causing issues in software stacks and predict which software stacks will likely not work without actually
running the application. An example of an issue can be a specific version of TensorFlow installed together
with a specific version of numpy that cause API incompatibility issues spotted on run time.

## Prerequisites

Docker with Docker buildkit.

Commands below work only if docker runs on root user.

## Run using Docker container

```bash
export APP_NAME="thoth_issue_predictor"
export BUILD_DATE=$(date +'%Y-%m-%d %H:%M:%S')
export VCS_BRANCH=$(git branch --show-current)
export VCS_REF=$(git rev-parse HEAD)

DOCKER_BUILDKIT=1 docker build . \
       --tag "$APP_NAME":"$VCS_REF" \
       --target deployment \
       --build-arg BUILD_DATE="$BUILD_DATE"  \
       --build-arg VCS_BRANCH="$VCS_BRANCH" \
       --build-arg VCS_REF="$VCS_REF" \
       --ssh default
```

```bash
export APP_NAME="thoth_issue_predictor"
export VCS_REF=$(git rev-parse HEAD)

docker run --net=host \
           --rm \
           --name "$APP_NAME"_cmd \
           --log-opt tag=$APP_NAME \
           --log-driver=journald \
           "$APP_NAME":"$VCS_REF" \
           jupyter lab
```

## Run development environment
