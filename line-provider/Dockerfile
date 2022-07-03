FROM python:3.10.1-alpine

ARG PROJECT_ROOT=$PROJECT_ROOT
ARG DOCKER_GROUP=$DOCKER_GROUP
ARG DOCKER_USER=$DOCKER_USER
ARG PROJECT_NAME=$PROJECT_NAME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER_GROUP=test \
    DOCKER_USER=test  \
    PROJECT_ROOT=/testapp/line-provider \
    PROJECT_NAME="line-provider"

WORKDIR $PROJECT_ROOT

COPY pyproject.toml .

RUN apk upgrade \
    && apk add --no-cache python3-dev libffi-dev gcc g++ \
    && pip3 install --upgrade pip \
    && apk add postgresql-dev mailcap musl-dev \
    && apk add bash coreutils

RUN set -exo pipefail \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install -vv


RUN addgroup -S $DOCKER_GROUP \
    && adduser -Ss /bin/bash -h "$PROJECT_ROOT" -G $DOCKER_GROUP $DOCKER_USER \
    && chown -R $DOCKER_USER:$DOCKER_GROUP "$PROJECT_ROOT"


USER $DOCKER_USER


ENV PYTHONPATH="$PYTHONPATH:$PROJECT_ROOT:$PROJECT_ROOT/$PROJECT_NAME"

COPY . $PROJECT_ROOT

ENTRYPOINT ["python", "main.py"]