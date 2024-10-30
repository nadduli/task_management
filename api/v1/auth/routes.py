#!/usr/bin/python3
"""Auth Router Module"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from .schema import UserCreate, UserModel
from .service import UserService


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register new user"""

    email = user_data.email

    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )
    new_user = await user_service.create_user(user_data, session)

    return new_user
