# Fix the users routes

## Run it

```bash
uv sync
uv run uvicorn main:app --app-dir src --reload   # http://localhost:8000/docs
uv run pytest src/exercises/users_routes_debug
```

Routes are mounted under `/users_routes_debug`.

## Spec

| Method | Path | Behaviour |
|--------|------|-----------|
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | One user, or `404` if it does not exist |
| GET | `/users/me` | The caller's own record, chosen by the `X-User-Id` header (default `1`) |

## Your task

Two things are reported as broken. Find out why, fix them in `router.py`, and be ready to
explain the cause. Do not edit `tests/`.
