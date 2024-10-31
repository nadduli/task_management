#!/usr/bin/python3
"""Task Model"""

from sqlmodel import Field, Column, String, ARRAY, SQLModel
import uuid
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


class Task(SQLModel, table=True):
    """Class Task which inherits from BaseModel"""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    title: str
    description: str
    due_date: Optional[datetime] = Field(nullable=True)
    status: str
    priority: Optional[str]
    assigned_to: Optional[EmailStr]
    tags: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))

    def __repr__(self):
        return f"<Task {self.title}>"
