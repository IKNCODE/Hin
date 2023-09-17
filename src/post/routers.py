from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from post.models import Post, Like, Comment
from post.schemas import PostCreate, LikeCreate, CommentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from auth.manager import current_user
from auth.models import User

from database import get_async_session


post_router = APIRouter(prefix="/post", tags=["Post"]) # Роутер для работы с постами

""" Просмотр всех постов """

@post_router.get("/")
async def get_all_post(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Post)
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as ex:
        return {"error": ex}

""" Просмотр всех постов определенного пользователя """

@post_router.get("/{user_id}")
async def get_user_posts(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Post).where(Post.author_id == user_id)
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as ex:
        return {"error": ex}

""" Добавление поста """

@post_router.post("/")
async def add_post(new_post: PostCreate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        new_post.author_id = user.id
        query = insert(Post).values(**new_post.dict())
        await session.execute(query)
        await session.commit()
        return {"status" : new_post}
    except Exception as ex:
        return {"error": ex}

like_router = APIRouter(prefix="/like", tags=["Like"]) # Роутер для работы с лайками

""" Возможность поставить лайк (необходимо указать user_id и post_id """

@like_router.post("/")
async def like_post(new_like: LikeCreate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        aut_len = await session.execute(select(Like).where(Like.account_id == new_like.account_id)) # Проверка, ставил ли пользователь лайк
        if len(aut_len.mappings().all()) >= 1: #В случае если да, лайк снимается
            dis = delete(Like).where(Like.account_id == new_like.account_id)
            await session.execute(dis)
            await session.commit()
            return {"dislike" : "dislike"}
        else:
            query = insert(Like).values(**new_like.dict())
            await session.execute(query)
            await session.commit()
            return {"status" : new_like}
    except Exception as ex:
        return {"error" : ex}



""" Возможность просмотра количество лайков под постом """

@like_router.get("/like_of_post")
async def like_post(post : int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Like).where(Like.post_id == post)
        result = await session.execute(query)
        return len(result.mappings().all())
    except Exception as ex:
        return {"error" : ex}

