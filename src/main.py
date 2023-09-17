from typing import Annotated, Union

from fastapi import FastAPI, Cookie, Depends
from fastapi_users import FastAPIUsers

from auth.manager import auth_backend, fastapi_users
from auth.manager import get_user_manager
from auth.models import User
from auth.manager import current_user
from auth.schemas import UserRead, UserCreate

from post.routers import post_router, like_router


app = FastAPI()




app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(post_router)
app.include_router(like_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)): # Получаем последнего пользователя
    return f"Hello, {user}"

@app.get("/users/me")
async def read_users_me(current: Annotated[User, Depends(current_user)]):
    return current