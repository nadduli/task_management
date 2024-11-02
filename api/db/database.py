#!/usr/bin/python3
"""Database Connection Module"""

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from api.core.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=False))


async def init_db() -> None:
    async with async_engine.begin() as conn:
        from api.v1.tasks.models import Task

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Database Dependency"""
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
