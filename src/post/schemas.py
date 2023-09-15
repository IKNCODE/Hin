from datetime import datetime
from typing import Optional
from auth.models import User

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    name: str
    content: str
    author_id: User
    date_create: datetime

class Like(BaseModel):
    id: int
    account_id: User
    post_id: Post
    date: datetime

class Comment(BaseModel):
    id: int
    text: str
    account_id: User
    post_id: Post
    date: datetime

