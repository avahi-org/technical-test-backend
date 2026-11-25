# auth_debug answer key
- Root cause: `fake_users_db["john_doe"]["username"]` is `"admin"`. The token `sub` is `"admin"`, then `get_current_user` does `fake_users_db.get("admin")` → None → 401.
- Fix: make the record's username `john_doe` (or look users up by the stored username consistently).
- Strong signals: decodes the JWT to inspect `sub`; reads the two lookups side by side rather than guessing at secrets/expiry.
- Weak signals: edits the SECRET_KEY or token expiry; edits the tests.
- Debrief: where should users be keyed? why is a plaintext secret in code a problem?
