#!/usr/bin/python3
"""Task Model"""

from sqlmodel import Field, Column, String, ARRAY, SQLModel, Index, Relationship
import uuid
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from api.v1.auth import models


class Task(SQLModel, table=True):
    """Task model"""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    title: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=False))
    due_date: Optional[datetime] = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True)
    )
    status: str = Field(sa_column=Column(String, nullable=False, index=True))
    priority: Optional[str] = Field(sa_column=Column(String, nullable=True, index=True))
    assigned_to: Optional[EmailStr]
    tags: Optional[List[str]] = Field(sa_column=Column(ARRAY(String), index=True))
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    user: Optional["models.User"] = Relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"
