from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.db.main import init_db


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
    lifespan=lifespan,
)


@app.get("/")
async def hello_world():
    return {"message": "Quillist says Hello World!"}


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
