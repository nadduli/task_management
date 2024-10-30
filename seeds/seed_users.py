#!/usr/bin/python3
"""Seed users module"""

import asyncio
import sys
import os
from faker import Faker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from passlib.hash import bcrypt
import uuid
from api.v1.auth.models import User
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/tasks_db"
engine = create_async_engine(DATABASE_URL, echo=True)


async def seed_users(n: int = 20):
    """Method to seed the database with users"""
    async with AsyncSession(engine) as session:
        for _ in range(n):
            user = User(
                id=uuid.uuid4(),
                username=fake.user_name(),
                email=fake.unique.email(),
                password=bcrypt.hash("password123"),
                isVerified=fake.boolean(chance_of_getting_true=75),
            )
            session.add(user)
        await session.commit()
    print(f"Seeded {n} users successfully!")


async def main():
    """Entry point of the seed module"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await seed_users(20)


if __name__ == "__main__":
    asyncio.run(main())
