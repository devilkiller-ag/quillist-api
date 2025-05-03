"""
This module provides an asynchronous service class (`BookService`) that handles
business logic and database operations related to books.
The service includes methods for creating, retrieving, updating, and deleting books, as well as retrieving books submitted by a specific user.
It interacts with the database through SQLModel's AsyncSession and provides asynchronous operations to ensure non-blocking I/O operations.
"""

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel


class BookService:
    """
    Service class to handle book-related database operations.
    """

    async def get_all_books(self, session: AsyncSession):
        """
        Retrieve all books from the database, ordered by most recent.

        Args:
            session (AsyncSession): The async database session.

        Returns:
            List[Book]: A list of all book records.
        """

        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()

        return books

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        """
        Retrieve all books created by a specific user.

        Args:
            user_uid (str): Unique identifier of the user.
            session (AsyncSession): The async database session.

        Returns:
            List[Book]: A list of books created by the user.
        """

        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        books = result.all()

        return books

    async def get_book(self, book_uid: str, session: AsyncSession):
        """
        Retrieve a single book by its unique identifier.

        Args:
            book_uid (str): Unique identifier of the book.
            session (AsyncSession): The async database session.

        Returns:
            Book | None: The matching book instance if found, otherwise None.
        """

        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        """
        Create a new book entry in the database.

        Args:
            book_data (BookCreateModel): Data for the new book.
            user_uid (str): UID of the user creating the book.
            session (AsyncSession): The async database session.

        Returns:
            Book: The newly created book object.
        """

        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        new_book.user_uid = user_uid

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        """
        Update an existing book's details.

        Args:
            book_uid (str): UID of the book to update.
            update_data (BookUpdateModel): New data to update the book.
            session (AsyncSession): The async database session.

        Returns:
            Book | None: Updated book object if successful, otherwise None.
        """

        book_to_update = await self.get_book(book_uid, session)

        if not book_to_update:
            return None

        update_data_dict = update_data.model_dump()

        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)

        await session.commit()

        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        """
        Delete a book by its UID.

        Args:
            book_uid (str): UID of the book to delete.
            session (AsyncSession): The async database session.

        Returns:
            Book | None: The deleted book object if it existed, otherwise None.
        """

        book_to_delete = await self.get_book(book_uid, session)

        if not book_to_delete:
            return None

        await session.delete(book_to_delete)
        await session.commit()

        return book_to_delete
