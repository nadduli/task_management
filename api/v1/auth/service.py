#!/usr/bin/python3
"""Service module for User"""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schema import UserCreate
from .utils import generate_password_hash


class UserService:
    """Class Auth to handle authentication logic"""

    async def get_user(self, email: str, session: AsyncSession):
        """Get user from database by email"""

        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, email, session: AsyncSession):
        """Check whether the user exists method"""
        user = await self.get_user(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        """Create a new user"""
        user_data_dict = dict(user_data)
        new_user = User(**user_data_dict)
        new_user.password = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"
        session.add(new_user)
        await session.commit()

        return new_user
