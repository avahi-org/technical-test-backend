# Contributor guide

This repo is a platform of independent backend exercises. Adding one never requires editing the
harness. Modelled on the front-end exercises repo.

## Layout

- `src/harness/`: descriptor type, registry (discovers exercises) and the FastAPI app. Do not edit for a new exercise.
- `src/exercises/<slug>/`: what the candidate sees: `exercise.py` (descriptor), `router.py`, README, `tests/`.
- `src/reference/<slug>/`: the solved version (same module layout). Pytest runs the visible tests against it with `--target reference`.
- `.specs/NNN-<slug>/`: spec; `NNN` must equal the exercise `order`.
- `.answer-keys/<slug>.md`: interviewer notes.
- `manifests/<slug>.json`: the paths the exercise owns, plus order and duration.
- `offline-exercises/`: plain-text problems for candidates who do not run code. Ships as-is.
- `tools/exercises.py`: `new`, `check`, `readme`, `build`.

## Rules

- Slug = folder = URL prefix, a python identifier. Pick a neutral name: it ships to candidates, so never name the bug.
- Cross-exercise imports are forbidden. Shared code goes in `src/harness/` or a new `src/shared/`.
- Debug exercises: visible tests FAIL on the candidate code and PASS on the reference. Say so in the README.
- Standalone exercises (e.g. Docker) set `router=None` and keep their own project inside the exercise folder.
- The README exercise table is generated from the descriptors: run `readme --write`, never edit between the markers.
- Anything internal (specs, keys, manifests, tooling, workflows, reference, CLAUDE.md) must be in `.gitattributes` as `export-ignore`. Candidate-facing files must not contain internal vocabulary (the leak check fails the build).
- Run `uv run python tools/exercises.py check` and `uv run pytest` before committing; `git archive` only packages committed files.

## Releases and random selection

- `tools/tracks.json`: exercises offered per track. `select --track 20` / `build --track 20` pick at random (SystemRandom; `--seed` makes it reproducible). Manifests may add `"pinned": true`. Stateless, so it can repeat the previous pick, and it only varies once a track has more exercises than its quota.
- `--set a,b` builds an explicit set (hyphens in slugs are accepted); `--set all` builds everything.
- Workflows: `ci.yaml` (checks), `package.yaml` (internal `unstable` release), `build-candidate.yaml` (manual: track or slugs, zip attached to the run for 7 days). Distribution to the candidate is manual.
- Caution: if this repo is public, reference solutions, specs and answer keys are readable on GitHub even though the zip excludes them, and any release is public too.
