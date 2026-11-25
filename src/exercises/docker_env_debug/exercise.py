from harness.descriptor import ExerciseDescriptor

exercise = ExerciseDescriptor(
    slug="docker_env_debug",
    order=3,
    title="Get the service running in Docker",
    description="A small API that will not build or start in Docker. Troubleshoot the image, the dependency setup and the lock file until it answers on port 8000.",
    duration="60 min",
    difficulty="Hard",
    kind="debug",
    designed_by="Oscar Segura",
    router=None,  # standalone: it has its own project under service/
)
