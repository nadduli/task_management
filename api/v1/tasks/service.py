#!/usr/bin/python3
"""Service Module for Task"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from typing import Optional, List
from sqlalchemy import or_
from .schema import TaskCreate, TaskUpdate
from .models import Task


class TaskService:
    """class TaskService"""

    async def get_tasks(
            self,
            session: AsyncSession,
            skip: int = 0,
            limit: int = 10,
            status: Optional[str] = None,
            priority: Optional[str] = None,
            tags: Optional[List[str]] = None
            ):
        """Retrieves a list of tasks with pagination and optional filters"""
        
        statement = (
            select(Task).offset(skip).limit(
                limit).order_by(desc(Task.created_at))
        )
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if tags:
            statement = statement.where(Task.tags.contains(*tags))

        result = await session.exec(statement)
        return result.all()

    async def get_user_tasks(
            self,
            user_id,
            session: AsyncSession,
            skip: int = 0,
            limit: int = 10):
        """Retrieves a list of tasks with pagination"""
        statement = (
            select(Task).offset(skip).limit(
                limit).where(Task.user_id == user_id).order_by(desc(Task.created_at))
        )
        result = await session.exec(statement)
        return result.all()
    
    async def get_task(self, task_id: str, session: AsyncSession):
        """Retrieve a Task by id"""
        statement = select(Task).where(Task.id == task_id)
        result = await session.exec(statement)
        task = result.first()

        return task if task is not None else None

    async def create_task(self, task_data: TaskCreate, user_id, session: AsyncSession):
        """create tasks"""
        task_data_dict = dict(task_data)
        new_task = Task(**task_data_dict)
        new_task.user_id = user_id
        session.add(new_task)
        await session.commit()
        return new_task

    async def update_task(
        self, task_id: str, task_data: TaskUpdate, session: AsyncSession
    ):
        """Update a Task by ID"""

        task_to_update = await self.get_task(task_id, session)

        if task_to_update is not None:
            update_task_dict = task_data.dict(exclude_unset=True)
            for key, value in update_task_dict.items():
                setattr(task_to_update, key, value)
            await session.commit()
            await session.refresh(task_to_update)
            return task_to_update
        else:
            return None

    async def delete_task(self, task_id: str, session: AsyncSession):
        """Delete a Task by ID"""
        task_to_delete = await self.get_task(task_id, session)

        if task_to_delete is not None:
            await session.delete(task_to_delete)
            await session.commit()
            return True
        else:
            return False
