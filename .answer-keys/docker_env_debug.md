# docker_env_debug answer key
Three independent failures, hit in this order:
1. Build stops at `COPY pyproject.toml uv.lock`: `"/uv.lock": not found`. Fix: run `uv lock` and commit it.
2. Build stops at `uv sync --frozen`: `No interpreter found for Python >=3.13`. Cause: `python:3.12-slim`. Fix: `python:3.13-slim` in BOTH stages.
3. Image builds, container fails to start: `exec: "uvicorn": executable file not found in $PATH`. Fix: add `uvicorn` to dependencies and re-lock.
(Verified end to end with Docker on 2026-11-24, including auto-reload on edit and the reference project.)
- Strong signals: reads each error rather than guessing; re-locks after changing dependencies; keeps `--frozen`.
- Weak signals: removes `--frozen`, `pip install`s by hand in the Dockerfile, lowers `requires-python` without discussing why.
- Note: the reference omits `uv.lock` on purpose; generate it with `uv lock`.
