# 003 docker_env_debug: get the service running in Docker

**Goal:** environment troubleshooting (image, dependency resolution, lock file), the part of the original test that is not about application code.
**Standalone:** `router=None`, its own project under `service/`; reference lives in `src/reference/docker_env_debug/service/`.
**Seeded defects:** (1) base image `python:3.12` vs `requires-python >=3.13`; (2) no `uv.lock` committed while the Dockerfile does `COPY uv.lock` and `uv sync --frozen`; (3) `uvicorn` missing from `dependencies`.
**Acceptance:** `docker compose up --build` serves `/` and `/hash` on :8000 and reloads on edit. Not covered by pytest (needs a Docker daemon).
