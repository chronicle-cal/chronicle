FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS python

FROM python AS python-build-stage

ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=0

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  git

COPY services/backend/pyproject.toml services/backend/uv.lock ./
COPY services/backend ./
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
