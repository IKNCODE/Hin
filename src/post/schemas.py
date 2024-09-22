from datetime import datetime
from typing import Optional
from auth.models import User
from post.models import Post, Like, Comment
from auth.schemas import UserRead

from pydantic import BaseModel, validator


class PostCreate(BaseModel):
    name: str
    content: str

    class Config:
        arbitrary_types_allowed = True


class LikeCreate(BaseModel):

    post_id: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

        arbitrary_types_allowed = True

class CommentCreate(BaseModel):
    text: str
    post_id: int
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),

        }

        arbitrary_types_allowed = True

