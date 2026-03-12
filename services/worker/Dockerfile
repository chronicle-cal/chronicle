FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

COPY services/worker/pyproject.toml services/worker/uv.lock ./
COPY services/worker ./
RUN uv sync --frozen --no-dev


CMD ["uv", "run", "worker"]
