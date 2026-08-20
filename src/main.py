from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm


from auth import (
    create_access_token,
    get_current_user,
    authenticate_user
)

app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# * HEALTHCHECK

@app.get("/", tags=["Health Check"])
async def read_root():
    """Hello world / health check endpoint."""
    return {"message": "Hello, World!"}

# ! TOKEN ROUTES

@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
async def read_current_user(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"username": current_user["username"]}
