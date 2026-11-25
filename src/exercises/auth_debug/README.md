# Debug the login flow

A small FastAPI service issues JWTs at `POST /token` and protects `GET /me`.

## Run it

```bash
uv sync
uv run uvicorn main:app --app-dir src --reload   # http://localhost:8000/docs
uv run pytest src/exercises/auth_debug           # the checks you need to turn green
```

Routes are mounted under `/auth_debug` (so `/auth_debug/token`, `/auth_debug/me`).

## Reported behaviour

- `POST /auth_debug/token` with `john_doe` / `password` returns a bearer token.
- Using that token on `GET /auth_debug/me` should return `{"username": "john_doe"}`.

Right now the second step does not work as documented.

## Your task

Reproduce the problem, find the root cause, fix it, and be ready to explain how you found it.
Code to look at: `auth.py` and `router.py` in this folder. Do not edit `tests/`.
