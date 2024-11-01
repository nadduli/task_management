#!/usr/bin/python3
"""Route file to group task related operations"""


from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from api.v1.auth.dependencies import AccessTokenBearer
from .schema import TaskCreate, TaskUpdate, TaskModel
from .service import TaskService
from .models import Task


task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()


@task_router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskModel])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    """Retrieve a paginated list of tasks."""
    tasks = await task_service.get_tasks(session, skip=skip, limit=limit)
    return tasks


@task_router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskModel)
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    """Retrieve a task by its ID."""
    task = await task_service.get_task(task_id, session)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not Found"
        )
    return task


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskModel)
async def create_tasks(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    """Create a new task."""
    new_task = await task_service.create_task(task_data, session)
    return new_task


@task_router.patch(
    "/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK
)
async def update_tasks(
    task_id: str,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    """Update an existing task by its ID."""
    task = await task_service.update_task(task_id, task_data, session)
    if not task:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasks(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    """Delete a task by its ID."""
    task = await task_service.delete_task(task_id, session)
    if task:
        return {"detail": "Task deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
