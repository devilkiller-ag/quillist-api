"""
This module defines and registers global middleware for the FastAPI backend.

Middlewares included:
- Custom request logging for API monitoring.
- CORS configuration to allow all origins and headers.
- TrustedHostMiddleware to allow requests from specific hosts.
- (Optional) Authorization middleware for global token validation.
"""


import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


# Disable default Uvicorn access logs to reduce terminal clutter
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):
    """
    Registers all necessary middleware components to the given FastAPI app.

    This includes:
    - Custom HTTP logging middleware
    - CORS middleware for handling cross-origin requests
    - TrustedHostMiddleware to restrict allowed hosts
    - (Optional) Authorization middleware for global token validation

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        """
        Logs request metadata such as client IP, method, path, status code, and processing time.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler in the chain.

        Returns:
            Response: The final HTTP response after request handling.
        """

        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        processing_time = end_time - start_time
        message = f"QUILLIST API LOGGER: {request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"
        print(message)

        return response

    # @app.middleware("http")
    # async def authorization(request: Request, call_next):
    #     """
    #     Checks if the Authorization header is present in each request.
    #     Can be used to enforce authentication globally across the app.
    #     This is an alternative to using FastAPI's dependency injection. Use this if you want to enforce authorization for all routes.

    #     Args:
    #         request (Request): The incoming HTTP request.
    #         call_next (Callable): The next middleware or route handler.

    #     Returns:
    #         JSONResponse or Response: Unauthorized message or the normal HTTP response.
    #     """
    #     if "Authorization" not in request.headers:
    #         return JSONResponse(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             content={
    #                 "message": "Not Authenticated: Authorization header missing",
    #                 "error_code": "authorization_header_missing",
    #                 "resolution": "Please login, provide an authorization header",
    #             },
    #         )
    #     response = await call_next(request)
    #     return response

    # Enable Cross-Origin Resource Sharing (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],            # Allow all domains (for development)
        allow_methods=["*"],            # Allow all HTTP methods
        allow_headers=["*"],            # Allow all headers
        allow_credentials=True,         # Support cookies/auth headers
    )

    # Allow only requests from these trusted hostnames
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "quillist-api.onrender.com",  # Production host
        ],
    )
