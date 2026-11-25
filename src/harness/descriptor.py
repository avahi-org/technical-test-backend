from dataclasses import dataclass
from typing import Literal

from fastapi import APIRouter

Duration = Literal["20 min", "60 min"]
Difficulty = Literal["Easy", "Medium", "Hard"]
Kind = Literal["debug", "build", "test"]


@dataclass(frozen=True)
class ExerciseDescriptor:
    """Everything the platform needs to know about an exercise.

    Each exercise exports one as ``exercise`` from ``src/exercises/<slug>/exercise.py``.
    The registry discovers them, so adding or removing an exercise folder needs no edit
    to the app, the index or the README tooling.
    """

    slug: str  # Must match the folder name; also the URL prefix, e.g. /auth_debug
    order: int  # Fixed per exercise, never resequenced. Must match its manifest and spec number.
    title: str
    description: str
    duration: Duration
    difficulty: Difficulty
    kind: Kind
    designed_by: str
    # None => a standalone exercise (e.g. Docker): listed on the index, not mounted.
    router: APIRouter | None = None
