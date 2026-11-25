"""Entry point: ``uvicorn main:app --app-dir src``. All logic lives in the harness."""
from harness.app import app

__all__ = ["app"]
