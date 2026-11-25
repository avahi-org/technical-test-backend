# 002 users_routes_debug: fix the users routes

**Goal:** the candidate understands FastAPI route matching order and error handling.
**Contract:** see the exercise README table.
**Seeded defects:** (1) `/users/{user_id}` is declared before `/users/me`, so "me" is parsed as an int (422); (2) missing user returns `200 null` instead of `404`.
**Acceptance:** 4 visible tests fail before the fix, all pass after; `--target reference` passes.
