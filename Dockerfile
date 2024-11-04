ARG UV_BASE=${UV_IMAGE_VER:-0.4.27}
ARG PYTHON_BASE=${PYTHON_IMAGE_VER:-3.12-slim}

FROM ghcr.io/astral-sh/uv:${UV_BASE} AS uv
FROM python:${PYTHON_BASE} AS base

COPY --from=uv /uv /usr/bin/uv

WORKDIR /project

COPY pyproject.toml uv.lock alembic.ini README.md ./
COPY ./src ./src

FROM base AS stage

COPY --from=base /project /project

WORKDIR /project

RUN uv sync --dev --all-extras && \
    uv pip install -e .

FROM stage AS run

COPY --from=base /project /project

WORKDIR /project

CMD ["echo", "hello, world"]

FROM stage AS run_scripts

COPY --from=base /project /project

WORKDIR /project

COPY scripts /project/scripts

CMD ["echo", "hello, world"]

FROM stage AS alembic

COPY --from=base /project /project

WORKDIR /project

COPY alembic.ini /project/alembic.ini
COPY migrations /project/migrations

CMD ["echo", "hello, world"]
