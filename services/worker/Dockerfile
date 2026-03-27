FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY services/worker/pyproject.toml services/worker/uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY services/worker ./
RUN uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder --chown=appuser:appuser /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

CMD ["worker"]