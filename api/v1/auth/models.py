#!/usr/bin/python3
"""User Model"""

from datetime import datetime
import uuid
from typing import List
from sqlmodel import Field, Column, SQLModel, Relationship
from api.v1.tasks import models
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    """User Model which inherits from basemodel"""

    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True,
                         nullable=False, default=uuid.uuid4)
    )
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    email: str
    username: str
    password: str = Field(exclude=True)
    isVerified: bool = Field(default=False)
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    tasks: List["models.Task"] = Relationship(back_populates= "user", sa_relationship_kwargs={'lazy': 'selectin'})

    def __repr__(self) -> str:
        return f"<User {self.username}>"
