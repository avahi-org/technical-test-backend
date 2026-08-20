# technical-test-backend
![Python](https://img.shields.io/badge/Python-grey?logo=python)
## Overview

A minimal [FastAPI](https://fastapi.tiangolo.com/) application that implements JWT-based authentication.
Your goal is to get it running correctly and verify that every endpoint responds as documented below.

---

## Prerequisites

| Tool | Install |
|------|---------|
| [`uv`](https://docs.astral.sh/uv/getting-started/installation/) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Docker](https://docs.docker.com/get-docker/) + Compose plugin | Official Docker docs |

---

## Running with Docker

```bash
# 1. Generate / refresh the dependency lock file
uv lock

# 2. Build the image and start the container
docker compose up --build
```

The API will be available at <http://localhost:8000>.

---

## Running Locally

```bash
# Install the virtual environment
uv sync

# Start the development server
uv run uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

---

## Verifying the API

All examples assume the service is reachable at `http://localhost:8000`.

### Health check

```bash
curl -s http://localhost:8000/
# Expected → {"message":"Hello, World!"}
```

### Obtain a JWT

```bash
curl -s -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=password"
# Expected → {"access_token":"<token>","token_type":"bearer"}
```

### Access a protected route

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=password" \
  | jq -r .access_token)

curl -s http://localhost:8000/me \
  -H "Authorization: Bearer $TOKEN"
# Expected → {"username":"john_doe"}
```

---

## API Reference

| Method | Path     | Auth         | Description                    |
|--------|----------|--------------|--------------------------------|
| GET    | `/`      | —            | Health check                   |
| POST   | `/token` | —            | Exchange credentials for a JWT |
| GET    | `/me`    | Bearer token | Return the authenticated user  |