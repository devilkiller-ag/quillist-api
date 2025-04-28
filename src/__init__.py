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
    """Lifespan context manager for FastAPI."""
    print("Server Starting up...")
    await init_db()

    yield

    print("Server shutting down...")


version = "v1"

app = FastAPI(
    title="Quillist",
    description="A REST API for book review web service.",
    version=version,
    # lifespan=lifespan, # Uncomment this line to use the init_db() in the custom lifespan context manager. Currently we are using alembic for migrations and default FastAPI lifespan context manager.
)


register_all_errors(app)

register_middleware(app)


@app.get("/")
async def hello_world():
    return {"message": "Quillist says Hello World!"}


app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
