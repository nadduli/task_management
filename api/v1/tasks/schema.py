#!/usr/bin/python3
"""Task Schema Module"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class TaskModel(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    due_date: Optional[datetime]
    status: str
    # created_by: uuid.UUID
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]
    status: str
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None
