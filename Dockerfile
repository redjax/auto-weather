ARG UV_BASE=${UV_IMAGE_VER:-0.4.27}
ARG PYTHON_BASE=${PYTHON_IMAGE_VER:-3.12-slim}

FROM ghcr.io/astral-sh/uv:${UV_BASE} AS uv
FROM python:${PYTHON_BASE} AS base

COPY --from=uv /uv /usr/bin/uv

WORKDIR /project

COPY pyproject.toml uv.lock alembic.ini README.md ./
COPY ./src ./src

RUN uv sync --dev --all-extras && \
    uv pip install -e .

FROM base AS run

CMD ["echo", "hello, world"]
