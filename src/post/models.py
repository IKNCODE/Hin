from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, Text, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from auth.models import User

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass

""" Таблица постов """
class Post(Base):
    __tablename__ = "post"


    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    date_create = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

""" Таблица лайков """
class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


""" Таблица комментариев """
class Comment(Base):
    __tablename__ = "comment"


    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


