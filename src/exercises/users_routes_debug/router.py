from fastapi import APIRouter, Header

router = APIRouter()

USERS = {
    1: {"id": 1, "name": "Ada"},
    2: {"id": 2, "name": "Linus"},
    3: {"id": 3, "name": "Grace"},
}


@router.get("/users")
async def list_users():
    return list(USERS.values())


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return USERS.get(user_id)


@router.get("/users/me")
async def get_me(x_user_id: int = Header(default=1)):
    """The caller's own record, identified by the X-User-Id header (defaults to 1)."""
    return USERS[x_user_id]
