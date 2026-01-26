FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

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