# 001 auth_debug: debug the login flow

**Goal:** the candidate reproduces a "token issued but rejected" bug, finds the root cause and fixes it.
**Contract:** `POST /token` (john_doe / password) → bearer token; `GET /me` with it → `{"username": "john_doe"}`.
**Seeded defect:** `fake_users_db["john_doe"]["username"] == "admin"`, so the JWT `sub` is `admin` and `get_current_user` looks up a key that does not exist.
**Acceptance:** `pytest src/exercises/auth_debug` fails 1 test before the fix and passes after; `--target reference` passes.
