#!/usr/bin/python3
"""Register Middleware Module"""

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])
