#!/usr/bin/python3
"""
Main entry point of the Task Management application.
"""

from fastapi import FastAPI
from api.v1.tasks.routes import task_router
from api.v1.auth.routes import auth_router
from api.v1.errors import register_all_errors
from api.v1.middleware import register_middleware


VERSION = "v1"

app = FastAPI(
    title="Tasks Management API",
    description="**Advanced Task Management API**",
    version=VERSION,
    docs_url=f"/api/{VERSION}/docs",
    redoc_url=f"/api/{VERSION}/redoc",
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

register_all_errors(app)

register_middleware(app)


app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
app.include_router(task_router, prefix=f"/api/{VERSION}/tasks", tags=["tasks"])
