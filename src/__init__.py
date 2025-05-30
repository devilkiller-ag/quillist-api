"""
Main entry point for the Quillist FastAPI application.

This module initializes the FastAPI app, registers middleware and error handlers,
and includes all the route routers (auth, books, reviews, tags).

It also defines a custom lifespan context manager for startup/shutdown logic
and provides an overview of the API in the OpenAPI schema.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.main import init_db
from src.auth.routes import auth_router
from src.tags.routes import tags_router
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.errors import register_all_errors
from src.middleware import register_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Custom lifespan context manager for FastAPI.

    Executes tasks during application startup and shutdown.
    Currently initializes the database connection on startup.

    Args:
        app (FastAPI): The FastAPI app instance.

    Yields:
        None
    """

    print("Server Starting up...")
    await init_db()

    yield

    print("Server shutting down...")


# API versioning and base path prefix
api_version = "v1"
api_prefix = f"/api/{api_version}"

# OpenAPI/Swagger documentation description
api_description = f"""
    A REST API for book review web service.
    
    This API allows users to:
    - Create an account and log in to the service using access token and refresh token.
    - CURD books, reviews, and tags.
    - Password reset and email verification.
    
    Additionally, it has the following features:
    - Background tasks for sending emails.
    - Token blacklisting for security.
    - Custom error handling.
    - Middleware for logging and performance monitoring.
    - Dependency injection for database session management, authentication, and authorization.
    - API documentation using OpenAPI Specification, Swagger UI and Redoc.
    - Testing using Pytest.
    
    It uses following technologies:
    - FastAPI for building the API.
    - PostgreSQL (NeonDB) for database.
    - SQLAlchemy and SQLModel for database ORM.
    - Alembic for database migrations.
    - Pydantic for data validation.
    - UUID for generating unique identifiers.
    - JWT for authentication.
    - Passlib for password hashing.
    - itsdangerous for generating and verifying tokens.
    - FastAPI-Mail for sending emails.
    - Logging for logging.
    - Redis for Token blacklisting, and Background Task queue (ex: sending emails).
    - Celery for background tasks (ex: sending emails).
    - Flower for background task monitoring.
    - Asgiref for async function to sync function conversion.
    - Pytest for testing.
    - Schemathesis for document driven testing.
    - OpenAPI Specification, Swagger UI and Redoc for API documentation.
    - Python-dotenv for environment variable management.
    - Render for deploying the API.
    
    Important Links:
    - Quillist API GitHub Repository: https://github.com/devilkiller-ag/quillist-api/
    - Quillist API: https://quillist-api.onrender.com/api/{api_version}
    - Quillist API Swagger UI Documentation: https://quillist-api.onrender.com/api/{api_version}/docs
    - Quillist API Redoc Documentation: https://quillist-api.onrender.com/api/{api_version}/redoc
"""

# Initialize FastAPI app
app = FastAPI(
    title="Quillist",
    description=api_description,
    api_version=api_version,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/mit"},
    contact={
        "name": "Ashmit JaiSarita Gupta",
        "url": "https://ashmit.dev",
        "email": "ashmitgupta.social@gmail.com",
    },
    openapi_url=f"{api_prefix}/openapi.json",
    docs_url=f"{api_prefix}/docs",
    redoc_url=f"{api_prefix}/redoc",
    # lifespan=lifespan, # Uncomment this line to use the init_db() in the custom lifespan context manager. Currently we are using alembic for migrations and default FastAPI lifespan context manager.
)


# Register global error handlers and middleware
register_all_errors(app)

register_middleware(app)


@app.get("/")
async def hello_world():
    """
    Health check endpoint.

    Returns a simple welcome message to confirm the API is running.
    """

    return {"message": "Quillist says Hello World!"}


# Include all route routers with API version prefix and tag grouping
app.include_router(auth_router, prefix=f"{api_prefix}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"{api_prefix}/books", tags=["books"])
app.include_router(review_router, prefix=f"{api_prefix}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"{api_prefix}/tags", tags=["tags"])
