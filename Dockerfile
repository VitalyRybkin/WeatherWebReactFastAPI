FROM python:3.12-alpine

ARG PROJECT_ENV

ENV PROJECT_ENV=${PROJECT_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \

  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.1

RUN #curl -sSL https://install.python-poetry.org | python3 -
RUN pip3 install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry install $(test "$PROJECT_ENV" == production && echo "--only=main") --no-interaction --no-ansi --no-root

COPY . /app

