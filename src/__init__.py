from fastapi import FastAPI
from src.books.routes import book_router


version = "v1"
app = FastAPI(
    title="Quillist",
    description="A REST API for book review web service.",
    version=version
)


@app.get('/')
async def hello_world():
    return {
        "message": "Quillist says Hello World!"
    }


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
