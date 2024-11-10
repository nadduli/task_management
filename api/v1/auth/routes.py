#!/usr/bin/python3
"""Auth Router Module"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from .schema import UserCreate, UserModel, LoginModel, UserTask, EmailModel
from .service import UserService
from .utils import (
    create_access_token,
    decode_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from api.db.redis import add_jti_to_block_list
from api.v1.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    UserNotFound,
)
from api.v1.mail import mail, create_message
from api.core.config import Config


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    """send mail"""
    email_addresses = emails.email_addresses

    html = "<h1>Welcome to Task Management </h1>"
    message = create_message(
        recipients=email_addresses, subject="Welcome to Task Management", body=html
    )
    await mail.send_message(message)
    return {"message": "Email sent successfully"}


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register new user"""

    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Welcome to Task Management</h1>
    <h2>Verify your email</h2>
    <p>Click the {link} below to verify your account:</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "User created successfully! Check your email to verify your account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    """Verify email route"""

    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user(user_email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {"isVerified": True}, session)

        return JSONResponse(
            content={"message": "Email verified successfully"},
            status_code=status.HTTP_200_OK,
        )
    raise InvalidToken()


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
                user_data={
                    "email": user.email,
                    "user_id": str(user.id),
                    "role": user.role,
                }
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
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """Create New Access Token"""
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserTask)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    """get current user routes"""
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    """logout endpoint"""
    jti = token_details["jti"]
    await add_jti_to_block_list(jti)
    return JSONResponse(
        content={"message": "Logout successfully"}, status_code=status.HTTP_200_OK
    )
