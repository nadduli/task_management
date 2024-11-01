#!/usr/bin/python3
"""User Model"""

from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    """User data Model"""

    id: uuid.UUID
    username: str
    email: EmailStr
    password: str
    isverified: Optional[bool] = False
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    """data class to create a new user"""

    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    """update user data"""

    username: str
    password: str


class LoginModel(BaseModel):
    """login model"""

    email: str
    password: str
