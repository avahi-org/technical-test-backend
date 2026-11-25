import importlib
import pkgutil
from dataclasses import dataclass, field

from fastapi import APIRouter

from .descriptor import ExerciseDescriptor


@dataclass
class Registry:
    exercises: list[ExerciseDescriptor] = field(default_factory=list)
    # folder -> reason. One broken exercise is reported here instead of taking the app down.
    errors: dict[str, str] = field(default_factory=dict)


def discover(package_name: str = "exercises") -> Registry:
    """Find every ``<package>/<slug>/exercise.py`` and validate its descriptor."""
    registry = Registry()
    package = importlib.import_module(package_name)
    seen_slugs: dict[str, str] = {}
    seen_orders: dict[int, str] = {}

    for info in sorted(pkgutil.iter_modules(package.__path__), key=lambda m: m.name):
        if not info.ispkg:
            continue
        folder = info.name
        try:
            exercise = importlib.import_module(f"{package_name}.{folder}.exercise").exercise
        except Exception as exc:  # noqa: BLE001 - isolate any exercise failure
            registry.errors[folder] = f"failed to load: {type(exc).__name__}: {exc}"
            continue

        if exercise.slug != folder:
            registry.errors[folder] = f'slug "{exercise.slug}" must match its folder name "{folder}"'
        elif exercise.slug in seen_slugs:
            registry.errors[folder] = f'duplicate slug "{exercise.slug}"'
        elif exercise.order in seen_orders:
            registry.errors[folder] = f"duplicate order {exercise.order} (also {seen_orders[exercise.order]})"
        else:
            seen_slugs[exercise.slug] = folder
            seen_orders[exercise.order] = folder
            registry.exercises.append(exercise)

    registry.exercises.sort(key=lambda e: e.order)
    return registry


def load_router(slug: str, target: str = "exercise") -> APIRouter:
    """The router for an exercise (what the candidate edits) or its solved reference."""
    if target == "reference":
        return importlib.import_module(f"reference.{slug}.router").router
    for exercise in discover().exercises:
        if exercise.slug == slug and exercise.router is not None:
            return exercise.router
    raise LookupError(f'no mounted exercise "{slug}"')
