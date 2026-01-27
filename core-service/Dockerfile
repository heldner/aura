FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Install wget and Go for grpc_health_probe
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.29/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

COPY core-service/src ./src

COPY core-service/alembic.ini .
COPY core-service/migrations ./migrations

ENV PYTHONPATH=/app:/app/src:/app/src/proto

EXPOSE 50051

CMD ["python", "src/main.py"]