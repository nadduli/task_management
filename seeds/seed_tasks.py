#!/usr/bin/python3
"""Seed tasks module"""
import sys
import os
import asyncio
from faker import Faker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from api.v1.tasks.models import Task

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/tasks_db"

engine = create_async_engine(DATABASE_URL, echo=True)


async def seed_tasks(n: int = 20):
    """Method to seed the database with tasks"""
    async with AsyncSession(engine) as session:
        for _ in range(n):
            task = Task(
                title=fake.sentence(),
                description=fake.text(),
                due_date=fake.date_time_between(
                    start_date="now",
                    end_date="+30d"),
                status=fake.random_element(
                    elements=[
                        "Pending",
                        "In Progress",
                        "Completed"]),
                priority=fake.random_element(
                    elements=[
                        "Low",
                        "Medium",
                        "High"]),
                assigned_to=fake.email(),
                tags=fake.words(
                    nb=3),
            )
            session.add(task)
        await session.commit()
    print(f"Seeded {n} tasks successfully!")


async def main():
    """Entry point of the seed module"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await seed_tasks(20)


if __name__ == "__main__":
    asyncio.run(main())
