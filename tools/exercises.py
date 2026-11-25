#!/usr/bin/env python3
"""Maintainer tooling (never shipped to candidates).

    uv run python tools/exercises.py check                       # registry, manifests, ownership, README
    uv run python tools/exercises.py readme --write              # regenerate the README exercise table
    uv run python tools/exercises.py new my_slug --order 4       # scaffold a new exercise
    uv run python tools/exercises.py select --track 20           # random set for a 20-minute interview
    uv run python tools/exercises.py build --track 20 --out dist # build a zip from a random set
    uv run python tools/exercises.py build --set a,b --out dist  # build a zip from an explicit set
"""
import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from harness.registry import discover  # noqa: E402

ROOT_DIR = "technical-test-backend"
TABLE_RE = re.compile(r"(<!-- EXERCISES:TABLE:START -->\n).*?(<!-- EXERCISES:TABLE:END -->)", re.S)
DEV_ONLY_RE = re.compile(r"^<!-- DEV-ONLY:START -->$.*?^<!-- DEV-ONLY:END -->$\n?", re.S | re.M)
# Directories whose top-level entries must each be owned by exactly one manifest.
OWNED_DIRS = ["src/exercises", "src/reference", ".specs", ".answer-keys"]
FORBIDDEN_WORDS = ["answer key", "answer-key", "export-ignore", "interviewer"]


def manifests() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / "manifests").glob("*.json"))}


def normalize(slug: str) -> str:
    """Accept `auth-debug` for `auth_debug`: a hyphen typo should not fail a build."""
    return slug.strip().replace("-", "_")


def track_name(track: str) -> str:
    return track if track.endswith("min") else f"{track} min"


def select(track: str, rng: random.Random | None = None) -> list[str]:
    """Pick the exercises for one interview track at random.

    Each track (a duration) offers `quota` exercises (tools/tracks.json). Exercises whose manifest says
    `"pinned": true` are always included and count toward the quota. Stateless: it does not remember
    what it picked last time.
    """
    rng = rng or random.SystemRandom()
    name = track_name(track)
    tracks = json.loads((ROOT / "tools" / "tracks.json").read_text())
    if name not in tracks:
        sys.exit(f'unknown track "{track}" (known: {", ".join(tracks)})')
    ms = manifests()
    pool = sorted((m for m in ms.values() if m["duration"] == name), key=lambda m: m["order"])
    if not pool:
        sys.exit(f"no exercises with duration {name}")
    pinned = [m["slug"] for m in pool if m.get("pinned")]
    rest = [m["slug"] for m in pool if not m.get("pinned")]
    extra = max(tracks[name]["quota"] - len(pinned), 0)
    chosen = pinned + rng.sample(rest, min(extra, len(rest)))
    return sorted(chosen, key=lambda s: ms[s]["order"])


def render_table(descriptors) -> str:
    rows = [
        "| # | Exercise | What it is | Type | Length | Level |",
        "|---|----------|-----------|------|--------|-------|",
    ]
    for e in descriptors:
        where = f"`src/exercises/{e.slug}/`"
        rows.append(f"| {e.order} | {where} | **{e.title}.** {e.description} | {e.kind} | {e.duration} | {e.difficulty} |")
    return "\n".join(rows) + "\n"


def with_table(readme: str, descriptors) -> str:
    return TABLE_RE.sub(lambda m: m.group(1) + render_table(descriptors) + m.group(2), readme)


def denylist() -> list[str]:
    out = []
    for line in (ROOT / ".gitattributes").read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1] == "export-ignore" and not line.startswith("#"):
            out.append(parts[0].lstrip("/"))
    return out


def check() -> list[str]:
    errors: list[str] = []
    registry = discover()
    errors += [f"exercise {k}: {v}" for k, v in registry.errors.items()]
    ms = manifests()
    by_slug = {e.slug: e for e in registry.exercises}

    for slug, m in ms.items():
        e = by_slug.get(slug)
        if e is None:
            errors.append(f"manifest {slug}: no matching exercise")
            continue
        if (m["slug"], m["order"], m["duration"]) != (e.slug, e.order, e.duration):
            errors.append(f"manifest {slug} disagrees with exercise.py (slug/order/duration)")
        for p in m["paths"]:
            if not (ROOT / p).exists():
                errors.append(f"manifest {slug}: path {p} does not exist")
        spec = [p for p in m["paths"] if p.startswith(".specs/")]
        if not spec or Path(spec[0]).name[:3] != f"{e.order:03d}":
            errors.append(f"manifest {slug}: spec dir number must equal order {e.order:03d}")
    for slug in by_slug.keys() - ms.keys():
        errors.append(f"exercise {slug}: no manifest")

    owners: dict[str, list[str]] = {}
    for slug, m in ms.items():
        for p in m["paths"]:
            owners.setdefault(p, []).append(slug)
    for d in OWNED_DIRS:
        for entry in sorted((ROOT / d).iterdir()):
            if entry.name in ("__init__.py", "__pycache__") or entry.name.startswith("."):
                continue
            rel = f"{d}/{entry.name}"
            n = len(owners.get(rel, []))
            if n != 1:
                errors.append(f"{rel}: owned by {n} manifests (must be exactly 1)")

    deny = denylist()
    for internal in ["manifests/", "tools/", "tests/", ".specs/", ".answer-keys/", "src/reference/", ".gitattributes"]:
        if internal not in deny:
            errors.append(f".gitattributes must export-ignore {internal}")

    readme = (ROOT / "README.md").read_text()
    if with_table(readme, registry.exercises) != readme:
        errors.append("README exercise table is stale: run `readme --write`")
    return errors


def cmd_check(_):
    errors = check()
    for e in errors:
        print(f"ERROR {e}")
    print("OK" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


def cmd_readme(args):
    readme_path = ROOT / "README.md"
    new = with_table(readme_path.read_text(), discover().exercises)
    if args.write:
        readme_path.write_text(new)
        print("README table written")
        return 0
    return 0 if new == readme_path.read_text() else (print("README table is stale") or 1)


def leak_check(tree: Path, removed: set[str]) -> list[str]:
    errors = []
    for pattern in denylist():
        if (tree / pattern.rstrip("/")).exists():
            errors.append(f"denylisted path shipped: {pattern}")
    for f in tree.rglob("*"):
        if not f.is_file() or ".venv" in f.parts or f.suffix in (".pyc", ".lock"):
            continue
        text = f.read_text(errors="ignore").lower()
        rel = f.relative_to(tree)
        errors += [f'{rel}: internal vocabulary "{w}"' for w in FORBIDDEN_WORDS if w in text]
        errors += [f"{rel}: mentions removed exercise {s}" for s in removed if s in text]
        if "DEV-ONLY" in f.read_text(errors="ignore"):
            errors.append(f"{rel}: DEV-ONLY marker left")
    return errors


def cmd_build(args):
    registry = discover()
    descriptors = {e.slug: e for e in registry.exercises}
    if args.track:
        keep = select(args.track, random.Random(args.seed) if args.seed else None)
    elif args.set == "all":
        keep = list(descriptors)
    else:
        keep = [normalize(s) for s in args.set.split(",") if s]
    unknown = set(keep) - descriptors.keys()
    if unknown or not keep:
        sys.exit(f"unknown or empty set: {sorted(unknown)}")
    if (problems := check()):
        sys.exit("check failed, refusing to build:\n  " + "\n  ".join(problems))
    ms = manifests()
    removed = set(descriptors) - set(keep)

    work = Path(tempfile.mkdtemp(prefix="build-"))
    try:
        tar = work / "src.tar"
        subprocess.run(["git", "archive", "--format=tar", f"--prefix={ROOT_DIR}/", "-o", str(tar), args.ref], cwd=ROOT, check=True)
        subprocess.run(["tar", "-xf", str(tar), "-C", str(work)], check=True)
        tree = work / ROOT_DIR
        for slug in removed:  # prune: the denylist already dropped reference/specs/keys
            for p in ms[slug]["paths"]:
                target = tree / p
                shutil.rmtree(target, ignore_errors=True) if target.is_dir() else target.unlink(missing_ok=True)
        readme = tree / "README.md"
        text = with_table(readme.read_text(), [descriptors[s] for s in sorted(keep, key=lambda s: descriptors[s].order)])
        readme.write_text(DEV_ONLY_RE.sub("", text))

        if (leaks := leak_check(tree, removed)):
            sys.exit("leak check failed:\n  " + "\n  ".join(leaks))

        out = Path(args.out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        zip_path = out / f"{ROOT_DIR}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(tree.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(work))

        if not args.skip_verify:  # verify the artifact, not the working tree
            check_dir = Path(tempfile.mkdtemp(prefix="verify-"))
            try:
                with zipfile.ZipFile(zip_path) as z:
                    z.extractall(check_dir)
                proj = check_dir / ROOT_DIR
                code = ("import sys; sys.path.insert(0,'src'); from harness.registry import discover; r=discover(); "
                        f"assert not r.errors, r.errors; assert [e.slug for e in r.exercises]=={sorted(keep, key=lambda s: descriptors[s].order)!r}, r.exercises")
                subprocess.run(["uv", "run", "python", "-c", code], cwd=proj, check=True)
                collected = subprocess.run(["uv", "run", "pytest", "--collect-only", "-q"], cwd=proj)
                if collected.returncode not in (0, 5):  # 5 = nothing collected: fine for standalone-only sets
                    sys.exit("pytest could not collect the extracted zip")
            finally:
                shutil.rmtree(check_dir, ignore_errors=True)

        meta = {"track": track_name(args.track) if args.track else None, "set": keep, "sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(), "size": zip_path.stat().st_size}
        (out / "build.json").write_text(json.dumps(meta, indent=2) + "\n")
        print(f"built {zip_path} ({meta['size']} bytes) set={keep}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


def cmd_select(args):
    print(",".join(select(args.track, random.Random(args.seed) if args.seed else None)))
    return 0


def cmd_new(args):
    slug, order = args.slug, args.order
    if not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
        sys.exit("slug must be a python identifier (lowercase, underscores)")
    ex, ref = ROOT / "src/exercises" / slug, ROOT / "src/reference" / slug
    spec = ROOT / ".specs" / f"{order:03d}-{slug}"
    for p in (ex, ref, spec):
        if p.exists():
            sys.exit(f"{p} already exists")
        p.mkdir(parents=True)
    (ex / "tests").mkdir()
    for p in (ex / "__init__.py", ref / "__init__.py"):
        p.write_text("")
    router = 'from fastapi import APIRouter\n\nrouter = APIRouter()\n\n\n@router.get("/")\nasync def read_root():\n    return {"message": "TODO"}\n'
    (ex / "router.py").write_text(router)
    (ref / "router.py").write_text(router)
    (ex / "exercise.py").write_text(
        "from harness.descriptor import ExerciseDescriptor\n\nfrom .router import router\n\n"
        f'exercise = ExerciseDescriptor(\n    slug="{slug}",\n    order={order},\n    title="TODO",\n    description="TODO",\n'
        '    duration="20 min",\n    difficulty="Medium",\n    kind="debug",  # debug | build | test\n    designed_by="TODO",\n    router=router,\n)\n'
    )
    (ex / "README.md").write_text(f"# TODO title\n\n## Run it\n\n```bash\nuv sync\nuv run pytest src/exercises/{slug}\n```\n\n## Your task\n\nTODO\n")
    (ex / "tests" / f"test_{slug}.py").write_text('def test_health(client):\n    assert client.get("/").status_code == 200\n')
    (spec / "spec.md").write_text(f"# {order:03d} {slug}\n\n**Goal:**\n**Contract:**\n**Seeded defects:**\n**Acceptance:**\n")
    (ROOT / ".answer-keys" / f"{slug}.md").write_text(f"# {slug} answer key\n\n- Root cause:\n- Fix:\n- Signals:\n")
    (ROOT / "manifests" / f"{slug}.json").write_text(json.dumps({
        "slug": slug, "order": order, "duration": "20 min",
        "paths": [f"src/exercises/{slug}", f"src/reference/{slug}", f".specs/{order:03d}-{slug}", f".answer-keys/{slug}.md"],
    }, indent=2) + "\n")
    print(f"scaffolded {slug}. Fill the TODOs, then: uv run python tools/exercises.py readme --write && uv run python tools/exercises.py check")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    r = sub.add_parser("readme"); r.add_argument("--write", action="store_true"); r.set_defaults(fn=cmd_readme)
    n = sub.add_parser("new"); n.add_argument("slug"); n.add_argument("--order", type=int, required=True); n.set_defaults(fn=cmd_new)
    sel = sub.add_parser("select", help="print a random set of slugs for a track"); sel.add_argument("--track", required=True); sel.add_argument("--seed"); sel.set_defaults(fn=cmd_select)
    b = sub.add_parser("build"); g = b.add_mutually_exclusive_group(required=True); g.add_argument("--set", help="comma-separated slugs, or `all`"); g.add_argument("--track", help="20 or 60: pick the exercises at random"); b.add_argument("--seed", help="make --track reproducible"); b.add_argument("--out", default="dist"); b.add_argument("--skip-verify", action="store_true"); b.add_argument("--ref", default="HEAD", help="git tree-ish to package (default HEAD: only committed files ship)"); b.set_defaults(fn=cmd_build)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
