"""
This module contains the API routes related to book management in the system.

Routes:
- get_all_books: Retrieve all books from the database.
- get_user_book_submissions: Retrieve books submitted by a specific user.
- create_a_book: Create a new book record in the system.
- get_book: Retrieve the details of a specific book by its unique identifier.
- update_book: Update an existing book record.
- delete_book: Delete a book from the system.
"""

from typing import List
from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.books.service import BookService
from src.books.schemas import Book, BookDetailModel, BookCreateModel, BookUpdateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import BookNotFound

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@book_router.get("/", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """
    Retrieve a list of all books from the database.

    Args:
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.

    Returns:
        List[Book]: A list of books retrieved from the database.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Raises:
        BookNotFound: If no books are found in the database.
    """

    books = await book_service.get_all_books(session)

    if books is None:
        raise BookNotFound()

    return books


@book_router.get(
    "/user/{user_uid}", response_model=List[Book], dependencies=[Depends(role_checker)]
)
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """
    Retrieve all books submitted by a specific user.

    Args:
        user_uid (str): The unique identifier of the user whose books are to be retrieved.
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.

    Returns:
        List[Book]: A list of books submitted by the specified user.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Raises:
        BookNotFound: If no books are found for the given user.
    """

    books = await book_service.get_user_books(user_uid, session)

    if books is None:
        raise BookNotFound()

    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[Depends(role_checker)],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """
    Create a new book record in the database.

    Args:
        book_data (BookCreateModel): The data required to create a new book.
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        Book: The newly created book record.


    Raises:
        Exception: Any other exceptions encountered during book creation.
    """

    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid, session)

    return new_book


@book_router.get(
    "/{book_uid}", response_model=BookDetailModel, dependencies=[Depends(role_checker)]
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """
    Retrieve the details of a specific book by its unique identifier.

    Args:
        book_uid (str): The unique identifier of the book to retrieve.
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.

    Returns:
        BookDetailModel: The detailed information of the requested book.

    Raises:
        BookNotFound: If the book with the specified UID does not exist.
    """

    book = await book_service.get_book(book_uid, session)

    if book is None:
        raise BookNotFound()

    return book


@book_router.patch(
    "/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)]
)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """
    Update an existing book record in the database.

    Args:
        book_uid (str): The unique identifier of the book to update.
        book_update_data (BookUpdateModel): The data to update the book record with.
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.

    Returns:
        Book: The updated book record.

    Raises:
        BookNotFound: If the book with the specified UID does not exist.
    """

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise BookNotFound()

    return updated_book


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(role_checker)],
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """
    Delete a book from the database by its unique identifier.

    Args:
        book_uid (str): The unique identifier of the book to delete.
        session (AsyncSession): The database session dependency to interact with the database.
        token_details (dict): The dependency to get decoded JWT token, containing user details.
    Returns:
        None: If the book is successfully deleted, a 204 status code is returned.

    Raises:
        BookNotFound: If the book with the specified UID does not exist.
    """

    deleted_book = await book_service.delete_book(book_uid, session)

    if not deleted_book:
        raise BookNotFound()
