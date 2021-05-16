FROM python:3.8-slim-buster as base

ARG USER=thoth_issue_predictor
ARG UID=1000
ARG GID=1000
ARG WORKDIR="/opt/$USER"
ARG LOCALBIN="/home/$USER/.local/bin"
ARG PIPENV="/home/$USER/.pipenv/bin"
ARG VCS_URL="https://gitlab.ictmedia.cz/device-security/cloud/network_checker.git"
ARG BUILD_DATE
ARG VCS_BRANCH
ARG VCS_REF

LABEL image.build-date=$BUILD_DATE\
      image.name=$USER\
      project.vcs-url=$VCS_URL\
      project.version="0.1.0"\
      project.vcs-branch=$VCS_BRANCH\
      project.vcs_ref=$VCS_REF


ENV PYTHONUNBUFFERED 1
ENV PATH=$PATH:$LOCALBIN:$PIPENV

RUN apt-get update && apt-get upgrade -y \
 && apt-get install -y \
    libpq-dev \
    gcc \
    git \
    curl \
    pipenv \
    graphviz \
 && groupadd -g $GID $USER \
 && useradd -m -u $UID -g $GID -s /bin/bash $USER \
 && install -d -m 0755 -o $USER -g $USER $WORKDIR

FROM base as poetry

USER $USER

SHELL ["/bin/bash", "-c"]

RUN mkdir -p -m 700 "$HOME/.ssh/"

FROM poetry as deployment

WORKDIR $WORKDIR

COPY --chown=$USER . $WORKDIR

RUN --mount=type=ssh,uid=1000 pipenv install

ENTRYPOINT ["pipenv", "run"]
