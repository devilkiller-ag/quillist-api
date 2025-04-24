from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        """Get all books."""
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()

        return books

    async def get_book(self, book_uid: str, session: AsyncSession):
        """Get a book."""
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """Create a book."""
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        """Update a book."""
        book_to_update = await self.get_book(book_uid, session)

        if not book_to_update:
            return None

        update_data_dict = update_data.model_dump()

        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)

        await session.commit()

        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        """Delete a book."""
        book_to_delete = await self.get_book(book_uid, session)

        if not book_to_delete:
            return None

        await session.delete(book_to_delete)
        await session.commit()

        return book_to_delete
