#!/usr/bin/python3
"""
Main entry point of the Task Management application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.tasks.routes import task_router
from api.v1.auth.routes import auth_router

from api.db.database import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    """method to run when starting the app"""
    print("Connected to the database..!")
    await init_db()
    yield
    print("Disconnected from the database...!")


VERSION = "v1"

app = FastAPI(
    title="Tasks Management API",
    description="**API to manage task management with FastAPI**",
    version=VERSION,
    lifespan=life_span,
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


app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
app.include_router(task_router, prefix=f"/api/{VERSION}/tasks", tags=["tasks"])
