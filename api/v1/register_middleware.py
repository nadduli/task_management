#!/usr/bin/python3
"""Register Middleware Module"""

from fastapi import FastAPI
from fastapi.requests import Request
from time import time
import logging


logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):
    """Register Middleware"""

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        """Custom Logging Middleware for API"""

        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url} - {response.status_code} - completed in {process_time}s"
        print(message)
        return response