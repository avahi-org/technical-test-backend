# users_routes_debug answer key
- Defect 1: `/users/{user_id}` declared before `/users/me`; "me" fails int validation (422). Fix: declare the static route first.
- Defect 2: `USERS.get()` returns None → `200 null`. Fix: raise `HTTPException(404)`.
- Strong signals: reads the 422 body, knows Starlette matches in declaration order.
- Debrief: alternatives (path converters, separate router, response models).
