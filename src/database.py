from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

""" Создание асинхронного движка ORM БД """
engine = create_async_engine(DATABASE_URL) # Инициализация асинхроного движка
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

""" Функция для получения асинхронной сессии (используется в routers) """
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session