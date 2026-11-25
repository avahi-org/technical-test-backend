from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

USERS = {
    1: {"id": 1, "name": "Ada"},
    2: {"id": 2, "name": "Linus"},
    3: {"id": 3, "name": "Grace"},
}


@router.get("/users")
async def list_users():
    return list(USERS.values())


# Static paths must be declared before parametrised ones, or "/users/{user_id}" swallows "/users/me".
@router.get("/users/me")
async def get_me(x_user_id: int = Header(default=1)):
    return USERS[x_user_id]


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
