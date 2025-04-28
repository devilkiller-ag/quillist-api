import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Disable Uvicorn's default access log
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):
    """
    Register middlewares for the FastAPI application.
    """

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        """
        Middleware to log request details.
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
    #     Middleware to check for authorization header.
    #     This is an alternative to using FastAPI's dependency injection. Use this if you want to enforce authorization for all routes.
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ],
    )
