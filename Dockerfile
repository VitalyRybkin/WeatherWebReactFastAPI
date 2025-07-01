FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

ARG PROJECT_ENV

ENV PROJECT_ENV=${PROJECT_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \

  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.1


RUN pip3 install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install $(test "$PROJECT_ENV" == production && echo "--only=main") --no-interaction --no-ansi --no-root

COPY ./app /code/app


