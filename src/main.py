

from typing import Annotated, Union

from fastapi import FastAPI, Cookie, Depends
from fastapi_users import FastAPIUsers

from auth.manager import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate


app = FastAPI()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

current_user = fastapi_users.current_user()
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)): # Получаем последнего пользователя
    return f"Hello, {user.login}"