from typing import Annotated, Union, Optional

from fastapi import FastAPI, Cookie, Depends, Request
from fastapi_users import FastAPIUsers

from auth.manager import auth_backend, fastapi_users
from auth.manager import get_user_manager
from auth.models import User
from auth.manager import current_user
from auth.schemas import UserRead, UserCreate

from post.routers import post_router, like_router, comment_router


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
app.include_router(comment_router)

@app.get("/")
async def index(request: Request, current: Annotated[User, Depends(current_user)] = None):
    return {"request" : request, "current" : current}

@app.get("/users/me")
async def read_users_me(current: Annotated[User, Depends(current_user)]):
    return current