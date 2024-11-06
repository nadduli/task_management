#!/usr/bin/python3
"""Task Model"""

from sqlmodel import Field, Column, String, ARRAY, SQLModel, Index
import uuid
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


class Task(SQLModel, table=True):
    """Class Task which inherits from BaseModel"""
    __tablename__ = "tasks"
    
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4))
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    title: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=False))
    due_date: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True))
    status: str = Field(sa_column=Column(String, nullable=False, index=True))
    priority: Optional[str] = Field(sa_column=Column(String, nullable=True, index=True))
    assigned_to: Optional[EmailStr]
    tags: Optional[List[str]] = Field(sa_column=Column(ARRAY(String), index=True))
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")


    def __repr__(self):
        return f"<Task {self.title}>"
