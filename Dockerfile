# --- Builder stage: resolve and install backend dependencies with uv ---
FROM python:3.12-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/var/task-venv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /build

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# --- Runtime stage: Python base image ---
FROM python:3.12-slim AS app

WORKDIR /app
COPY --from=builder /var/task-venv /var/task-venv
ENV PATH="/var/task-venv/bin:$PATH"

# Backend application source.
COPY src/ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
