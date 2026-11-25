from harness.descriptor import ExerciseDescriptor

from .router import router

exercise = ExerciseDescriptor(
    slug="auth_debug",
    order=1,
    title="Debug the login flow",
    description="A FastAPI JWT login that issues a token but rejects it on the protected route. Reproduce, find the cause and fix it.",
    duration="20 min",
    difficulty="Easy",
    kind="debug",
    designed_by="Oscar Segura",
    router=router,
)
