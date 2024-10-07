#syntax=docker/dockerfile:1.4

# Use the preceding syntax to be able to use:
# * COPY --link
# * RUN --mount=type=cache
# See also https://medium.com/datamindedbe/how-we-reduced-our-docker-build-times-by-40-afea7b7f5fe7.

# FROM debian:bookworm as builder
FROM condaforge/miniforge3:latest as builder

WORKDIR /app

COPY Makefile environment.yml pyproject.toml poetry.lock ./
RUN touch README.md && make init

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-bookworm as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

RUN conda activate pato-gui && poetry run pato-gui-build
ENTRYPOINT ["dist/PatoGui/PatoGui"]
