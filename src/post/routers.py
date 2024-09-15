from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, func
from post.models import Post, Like, Comment
from post.schemas import PostCreate, LikeCreate, CommentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from auth.manager import current_user
from random import randint
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

""" Просмотр рандомного поста из топ 10 """
@post_router.get("/top")
async def get_top_post(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Post.name, func.count(Like.id)).join(Like, Post.id == Like.post_id).group_by(Post.id).limit(10)
        result = await session.execute(query)
        return result.mappings().all()[randint(0,10)]
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

""" Удаление поста """

@post_router.delete("/delete")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        aut_len = await session.execute(select(Like).where(Like.post_id == post_id)) # получение кол-ва лайков
        while len(aut_len.mappings().all()) >= 1:  # Удаление всех лайков (т.к. привязка к постам)
            dis = delete(Like).where(Like.post_id == post_id)
            await session.execute(dis)
            await session.commit()
            aut_len = await session.execute(select(Like).where(Like.post_id == post_id))
        query = delete(Post).where(Post.id == post_id)
        await session.execute(query)
        await session.commit()
        return {"status" : "deleted"}
    except Exception as ex:
        return {"error": ex}

like_router = APIRouter(prefix="/like", tags=["Like"]) # Роутер для работы с лайками

""" Возможность поставить лайк (необходимо указать user_id и post_id) """

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

comment_router = APIRouter(prefix="/comment", tags=["Comment"]) # Роутер для работы с комментариями

""" Получение комментариев определенного поста """
@comment_router.get("/")
async def comment_of_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Comment).where(Comment.post_id == post_id)
        result = await session.execute(query)
        return result.mappings().all()
    except Exception as ex:
        return {"error" : ex}

""" Запись комментария под постом """
@comment_router.post("/write_comment")
async def add_comment(comment: CommentCreate, user : User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        comment.account_id = user.id
        query = insert(Comment).values(**comment.dict())
        await session.execute(query)
        await session.commit()
        return {"status" : 200}
    except Exception as ex:
        return {"error" : ex}

""" Удаления комментария под постом """
@comment_router.delete("/delete_comment")
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        del_comm = delete(Comment).where(Comment.id == comment_id)
        await session.execute(del_comm)
        await session.commit()
        return {"status" : "deleted"}
    except Exception as ex:
        return {"error": ex}


