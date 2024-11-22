#!/usr/bin/python3
"""Auth Router Module"""

from fastapi import APIRouter, Depends, Request, status, BackgroundTasks
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel.ext.asyncio.session import AsyncSession
from api.db.database import get_session
from api.v1.celery_tasks import send_email
from .schema import (
    UserCreate,
    UserModel,
    LoginModel,
    UserTask,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from .utils import (
    create_access_token,
    decode_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash,
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
    PasswordsDoNotMatch,
)
from api.v1.mail import mail, create_message
from api.core.config import Config


auth_router = APIRouter()

limter = Limiter(key_func=get_remote_address)
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post("/send_mail")
@limter.limit("1000/minute")
async def send_mail(request: Request, emails: EmailModel):
    """send mail"""
    email_addresses = emails.email_addresses

    html = "<h1>Welcome to Task Management App</h1>"
    subject = "Welcome to our App"

    send_email.delay(email_addresses, subject, html)

    return {"message": "Email sent successfully"}


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
@limter.limit("1000/minute")
async def register(
    user_data: UserCreate,
    bg_tasks: BackgroundTasks,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Register new user with username, email and password"""

    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html = f"""
    <h1>Welcome to Task Management</h1>
    <h2>Verify your email</h2>
    <p>Click the <a href="{link}">link</a> below to verify your account:</p>
    """
    emails = [email]
    subject = "Verify your email"

    send_email.delay(emails, subject, html)

    return {
        "message": "User created successfully! Check your email to verify your account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
@limter.limit("1000/minute")
async def verify_email(request: Request, token: str, session: AsyncSession = Depends(get_session)):
    """Verify email route"""

    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")  # type: ignore # type: ignore

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
@limter.limit("1000/minute")
async def login_users(
    user_data: LoginModel, request: Request, session: AsyncSession = Depends(get_session)
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
@limter.limit("1000/minute")
async def get_new_access_token(request: Request, token_details: dict = Depends(RefreshTokenBearer())):
    """Create New Access Token"""
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserTask)
@limter.limit("1000/minute")
async def get_current_user(request: Request,
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    """get current user routes"""
    return user


@auth_router.get("/logout")
@limter.limit("1000/minute")
async def revoke_token(request: Request, token_details: dict = Depends(AccessTokenBearer())):
    """logout endpoint"""
    jti = token_details["jti"]
    await add_jti_to_block_list(jti)
    return JSONResponse(
        content={"message": "Logout successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post("/password-reset-request", status_code=status.HTTP_200_OK)
@limter.limit("1000/minute")
async def password_reset_request(request: Request, email_data: PasswordResetRequestModel):
    """Reset Password"""
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset your password</h1>
    <p>Click the <a href="{link}">link</a> below to reset your password:</p>
    """

    message = create_message(
        recipients=[email], subject="Reset your password", body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email for a link to reset your password"
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}", status_code=status.HTTP_200_OK)
@limter.limit("1000/minute")
async def reset_password_confirm(
    request: Request,
    token: str,
    password_data: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    """Reset Password confirmation"""
    new_password = password_data.new_password
    confirm_password = password_data.confirm_new_password

    if new_password != confirm_password:
        raise PasswordsDoNotMatch()

    token_data = decode_url_safe_token(token)

    email = token_data.get("email")

    if email:
        user = await user_service.get_user(email, session)
        if not user:
            raise UserNotFound()

        password_hash = generate_password_hash(new_password)

        await user_service.update_user(user, {"password": password_hash}, session)

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
