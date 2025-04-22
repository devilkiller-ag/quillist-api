from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

books = [
    {
        "id": 1,
        "title": "The Quantum Enigma",
        "author": "Brian Greene",
        "publisher": "Penguin Books",
        "published_date": "2018-03-12",
        "page_count": 352,
        "language": "en"
    },
    {
        "id": 2,
        "title": "Pythonic Thinking",
        "author": "Dan Bader",
        "publisher": "Leanpub",
        "published_date": "2020-07-15",
        "page_count": 230,
        "language": "en"
    },
    {
        "id": 3,
        "title": "Deep Work",
        "author": "Cal Newport",
        "publisher": "Grand Central Publishing",
        "published_date": "2016-01-05",
        "page_count": 304,
        "language": "en"
    },
    {
        "id": 4,
        "title": "Atomic Habits",
        "author": "James Clear",
        "publisher": "Avery",
        "published_date": "2018-10-16",
        "page_count": 320,
        "language": "en"
    },
    {
        "id": 5,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "en"
    },
    {
        "id": 6,
        "title": "Kafka on the Shore",
        "author": "Haruki Murakami",
        "publisher": "Vintage",
        "published_date": "2005-01-03",
        "page_count": 467,
        "language": "en"
    },
    {
        "id": 7,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "publisher": "Farrar, Straus and Giroux",
        "published_date": "2011-10-25",
        "page_count": 499,
        "language": "en"
    },
    {
        "id": 8,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "publisher": "MIT Press",
        "published_date": "2009-07-31",
        "page_count": 1312,
        "language": "en"
    },
    {
        "id": 9,
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "publisher": "Harper",
        "published_date": "2015-02-10",
        "page_count": 464,
        "language": "en"
    },
    {
        "id": 10,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publisher": "HarperOne",
        "published_date": "1993-05-01",
        "page_count": 208,
        "language": "en"
    }
]


app = FastAPI()

@app.get('/')
async def hello_worl():
    return {
        "message": "Quillist says Hello World!"
    }


@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.get('/books/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

@app.patch('/books/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
