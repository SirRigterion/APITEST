from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.settings import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("Database URL is ", SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
    future=True,
    )


async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session