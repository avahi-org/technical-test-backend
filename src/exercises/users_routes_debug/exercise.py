from harness.descriptor import ExerciseDescriptor

from .router import router

exercise = ExerciseDescriptor(
    slug="users_routes_debug",
    order=2,
    title="Fix the users routes",
    description="A small users API where one route never responds as documented and a missing user is not reported correctly.",
    duration="20 min",
    difficulty="Medium",
    kind="debug",
    designed_by="Oscar Segura",
    router=router,
)
