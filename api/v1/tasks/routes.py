#!/usr/bin/python3
"""Route file to group task related operations"""


from typing import List, Optional
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from api.v1.auth.dependencies import AccessTokenBearer
from .schema import TaskCreate, TaskUpdate, TaskModel
from .service import TaskService
from .models import Task
from api.v1.auth.dependencies import RoleChecker
from api.v1.errors import TaskNotFound


task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@task_router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskModel], dependencies=[role_checker])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """Retrieve a paginated list of tasks."""
    tasks = await task_service.get_tasks(
        session, 
        skip=skip, 
        limit=limit, 
        status=status, 
        priority=priority, 
        tags=tags)
    return tasks

@task_router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=List[TaskModel], dependencies=[role_checker])
async def get_user_tasks(
     user_id,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """Retrieve a paginated list of tasks."""
    tasks = await task_service.get_user_tasks(user_id, session, skip=skip, limit=limit)
    return tasks

@task_router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskModel, dependencies=[role_checker])
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    """Retrieve a task by its ID."""
    task = await task_service.get_task(task_id, session)
    if not task:
        raise TaskNotFound()
    
    return task


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskModel, dependencies=[role_checker])
async def create_tasks(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """Create a new task."""
    user_id = token_details.get('user')['user_id']
    new_task = await task_service.create_task(task_data, user_id, session)
    return new_task


@task_router.patch(
    "/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK, dependencies=[role_checker]
)
async def update_tasks(
    task_id: str,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    """Update an existing task by its ID."""
    task = await task_service.update_task(task_id, task_data, session)
    if not task:
        raise TaskNotFound()
    
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_tasks(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    """Delete a task by its ID."""
    task = await task_service.delete_task(task_id, session)
    if task:
        return {"detail": "Task deleted successfully"}
    else:
        raise TaskNotFound()