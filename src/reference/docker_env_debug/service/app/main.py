from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/hash")
async def hash_password(password: str = "password"):
    return {"hash": pwd_context.hash(password)}
