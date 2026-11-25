"""Platform invariants. They survive adding or removing exercises: nothing here lists slugs."""
import subprocess
import sys
from pathlib import Path

from harness.registry import discover

ROOT = Path(__file__).resolve().parent.parent


def test_every_exercise_loads_and_is_valid():
    registry = discover()
    assert registry.errors == {}
    assert registry.exercises


def test_mounted_exercises_have_a_reference_router():
    for e in discover().exercises:
        if e.router is not None:
            from harness.registry import load_router

            assert load_router(e.slug, "reference") is not None


def test_a_broken_exercise_does_not_take_the_registry_down(tmp_path, monkeypatch):
    pkg = tmp_path / "bad_pkg"
    (pkg / "broken").mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "broken" / "__init__.py").write_text("")
    (pkg / "broken" / "exercise.py").write_text("raise RuntimeError('boom')")
    monkeypatch.syspath_prepend(str(tmp_path))
    registry = discover("bad_pkg")
    assert "broken" in registry.errors and registry.exercises == []


def test_manifests_ownership_and_readme_are_consistent():
    result = subprocess.run([sys.executable, "tools/exercises.py", "check"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
