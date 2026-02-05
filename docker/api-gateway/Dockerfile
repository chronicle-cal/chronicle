FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./services/api-gateway /app/services/api-gateway

COPY ./packages/shared /app/packages/shared

RUN apt install 

WORKDIR /app/services/api-gateway
RUN uv sync --frozen

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]