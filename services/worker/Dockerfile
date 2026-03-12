FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY . .
RUN uv sync --frozen --no-dev


CMD ["uv", "run", "worker"]
