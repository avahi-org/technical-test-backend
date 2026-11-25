# Backend Interview Exercises

![Python](https://img.shields.io/badge/Python-grey?logo=python)

A set of self-contained FastAPI exercises. Each one lives in its own folder under
`src/exercises/<slug>/` with its own README, code and tests. Read the README of the exercise you
were given first.

<!-- EXERCISES:TABLE:START -->
| # | Exercise | What it is | Type | Length | Level |
|---|----------|-----------|------|--------|-------|
| 1 | `src/exercises/auth_debug/` | **Debug the login flow.** A FastAPI JWT login that issues a token but rejects it on the protected route. Reproduce, find the cause and fix it. | debug | 20 min | Easy |
| 2 | `src/exercises/users_routes_debug/` | **Fix the users routes.** A small users API where one route never responds as documented and a missing user is not reported correctly. | debug | 20 min | Medium |
| 3 | `src/exercises/docker_env_debug/` | **Get the service running in Docker.** A small API that will not build or start in Docker. Troubleshoot the image, the dependency setup and the lock file until it answers on port 8000. | debug | 60 min | Hard |
<!-- EXERCISES:TABLE:END -->

## Getting started

Requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (it installs the right Python for you).

```bash
uv sync
uv run uvicorn main:app --app-dir src --reload     # http://localhost:8000
```

- `http://localhost:8000/` lists the exercises that are mounted; `/docs` lets you try their routes.
- Run the checks for one exercise: `uv run pytest src/exercises/<slug>`.
- For the debugging exercises, failing tests are expected at the start. They are your reproduction.
- Docker is only needed by the exercise that is about Docker; its README says so.

## Offline exercises

`offline-exercises/` holds two plain-text problems for when running code on this machine is not an
option. Answer them in writing or on paper.

<!-- DEV-ONLY:START -->
## Maintainers

Everything below and the paths in `.gitattributes` never reach a candidate. See `CLAUDE.md` for the full contributor guide.

| I want to... | Do this |
|---|---|
| Add an exercise | `uv run python tools/exercises.py new <slug> --order N`, fill the TODOs, then `readme --write` and `check` |
| Validate the repo | `uv run python tools/exercises.py check` and `uv run pytest` (includes `tests/`) |
| Prove an exercise is solvable | `uv run pytest src/exercises --target reference` (all green) |
| Build a zip, random set for a track | `uv run python tools/exercises.py build --track 20 --out dist` (`select --track 20` only prints the pick) |
| Build a zip, explicit set | `uv run python tools/exercises.py build --set auth_debug,users_routes_debug --out dist` (hyphens in slugs are accepted) |
| Build in GitHub | Actions: **Build candidate zip**, choose a track (random pick) or enter slugs, download the `candidate-zip` artifact |

A zip is built from `git archive HEAD`, so only **committed** files are packaged and `.gitattributes`
removes internal paths (reference solutions, specs, answer keys, manifests, tooling, workflows). The
build then prunes to the chosen exercises, regenerates the table above, strips these maintainer
sections, runs a leak check and verifies the extracted zip.

**Random pick.** `tools/tracks.json` says how many exercises each track offers (`20 min`: 2, `60 min`: 1). A
manifest may set `"pinned": true` to always include that exercise. The pick is stateless: it does not avoid
repeating the last set. It only varies once a track has more exercises than its quota.
<!-- DEV-ONLY:END -->
