#!/usr/bin/python3
"""Auth Router Module"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from .schema import UserCreate, UserModel, LoginModel, UserTask
from .service import UserService
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from api.db.redis import add_jti_to_block_list
from api.v1.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken
    )


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
                                                ):
    """Register new user"""

    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login", response_model=dict)
async def login_users(
    user_data: LoginModel, session: AsyncSession = Depends(get_session)
):
    """Login route"""
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user(email, session)

    if user:
        valid_password = verify_password(password, user.password)
        if valid_password:
            access_token = create_access_token(
                user_data={"email": user.email, "user_id": str(user.id), "role": user.role}
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_id": str(user.id)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "id": str(user.id)},
                }
            )
    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()
                                  )):
    """Create New Access Token"""
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()

@auth_router.get('/me', response_model=UserTask)
async def get_current_user(user= Depends(get_current_user), _: bool = Depends(role_checker)):
    """get current user routes"""
    return user

@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    """logout endpoint"""
    jti = token_details['jti']
    await add_jti_to_block_list(jti)
    return JSONResponse(
        content={
            "message": "Logout successfully"
        },
        status_code=status.HTTP_200_OK
    )
