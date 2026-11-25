import importlib.util
import random
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tools = load("exercises")


def fake_manifests(count, pinned=()):
    return {
        f"ex{i}": {"slug": f"ex{i}", "order": i, "duration": "20 min", **({"pinned": True} if f"ex{i}" in pinned else {})}
        for i in range(1, count + 1)
    }


# ---- random selection ----------------------------------------------------------------------------

def test_picks_exactly_quota_from_a_larger_pool(monkeypatch):
    monkeypatch.setattr(tools, "manifests", lambda: fake_manifests(6))
    picked = tools.select("20", random.Random(1))
    assert len(picked) == 2 and len(set(picked)) == 2


def test_selection_is_actually_random(monkeypatch):
    monkeypatch.setattr(tools, "manifests", lambda: fake_manifests(6))
    seen = {tuple(tools.select("20", random.Random(seed))) for seed in range(40)}
    assert len(seen) > 5


def test_same_seed_same_set(monkeypatch):
    monkeypatch.setattr(tools, "manifests", lambda: fake_manifests(6))
    assert tools.select("20", random.Random("x")) == tools.select("20", random.Random("x"))


def test_pinned_is_always_included_and_counts_toward_quota(monkeypatch):
    monkeypatch.setattr(tools, "manifests", lambda: fake_manifests(6, pinned={"ex4"}))
    for seed in range(20):
        picked = tools.select("20", random.Random(seed))
        assert "ex4" in picked and len(picked) == 2


def test_small_pool_returns_everything(monkeypatch):
    monkeypatch.setattr(tools, "manifests", lambda: fake_manifests(1))
    assert tools.select("20") == ["ex1"]


def test_unknown_track_exits():
    with pytest.raises(SystemExit):
        tools.select("5")


def test_hyphenated_slugs_are_accepted():
    assert tools.normalize("auth-debug") == "auth_debug"
