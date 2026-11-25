import logging

from fastapi import FastAPI

from .registry import Registry, discover

log = logging.getLogger("harness")


def create_app(registry: Registry | None = None) -> FastAPI:
    registry = registry or discover()
    app = FastAPI(
        title="Backend interview exercises",
        description="Open an exercise's README under src/exercises/<slug>/, then use /docs to explore its routes.",
    )

    for folder, reason in registry.errors.items():
        log.error("exercise %s skipped: %s", folder, reason)

    for exercise in registry.exercises:
        if exercise.router is not None:
            app.include_router(exercise.router, prefix=f"/{exercise.slug}", tags=[exercise.slug])

    @app.get("/", tags=["platform"])
    async def index():
        """Lists every exercise, like the front-end home page."""
        return {
            "exercises": [
                {
                    "order": e.order,
                    "slug": e.slug,
                    "title": e.title,
                    "description": e.description,
                    "kind": e.kind,
                    "duration": e.duration,
                    "difficulty": e.difficulty,
                    "readme": f"src/exercises/{e.slug}/README.md",
                    "mounted_at": f"/{e.slug}" if e.router is not None else None,
                }
                for e in registry.exercises
            ],
            "errors": registry.errors,
        }

    return app


app = create_app()
