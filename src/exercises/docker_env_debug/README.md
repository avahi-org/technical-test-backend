# Get the service running in Docker

`service/` is a self-contained project: its own `pyproject.toml`, `Dockerfile` and
`docker-compose.yaml`. It is **not** part of the shared app, so work inside that folder.

## Goal

```bash
cd src/exercises/docker_env_debug/service
docker compose up --build
curl -s http://localhost:8000/        # {"message":"Hello, World!"}
curl -s http://localhost:8000/hash    # {"hash":"$2b$..."}
```

Both calls must work, and editing `app/main.py` must reload the server inside the container.

## Your task

The stack does not build or start. Find every reason, fix it, and explain what each failure meant
and how you diagnosed it. Requirements: Docker with the Compose plugin and
[`uv`](https://docs.astral.sh/uv/getting-started/installation/).

Keep the multi-stage build and `uv sync --frozen`; the fix is not to remove them.
