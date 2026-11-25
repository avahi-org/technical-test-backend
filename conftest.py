"""Shared pytest fixtures: every exercise's tests get a ``client`` for its own router."""
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from harness.registry import load_router


def pytest_addoption(parser):
    parser.addoption(
        "--target",
        default="exercise",
        choices=["exercise", "reference"],
        help="Run the exercise tests against the candidate code or the solved reference.",
    )


def _slug_of(path: Path) -> str:
    parts = path.parts
    return parts[parts.index("exercises") + 1]


@pytest.fixture
def client(request) -> TestClient:
    """A client rooted at the exercise's URL prefix, so tests call ``client.get("/token")``."""
    slug = _slug_of(request.path)
    app = FastAPI()
    app.include_router(load_router(slug, request.config.getoption("--target")), prefix=f"/{slug}")
    return TestClient(app, base_url=f"http://testserver/{slug}")
