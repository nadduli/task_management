#!/usr/bin/python3
"""
Main entry point of the Task Management application.
"""

from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from api.v1.tasks.routes import task_router
from api.v1.auth.routes import auth_router
from api.v1.errors import register_all_errors
from api.v1.middleware import register_middleware


version = "v1"

app = FastAPI(
    title="Tasks Management API",
    description="**Advanced Task Management API**",
    version=version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    openapi_url=f"/api/{version}/openapi.json",
    terms_of_service="http://danielInnovations.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://danielInnovations.com/support",
        "email": "naddulidaniel1994@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

register_all_errors(app)

register_middleware(app)


app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(task_router, prefix=f"/api/{version}/tasks", tags=["tasks"])
