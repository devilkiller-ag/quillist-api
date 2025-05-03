"""
This module contains test cases for the book-related endpoints of the FastAPI backend application.
"""

from src import api_prefix
from src.books.schemas import BookCreateModel


books_prefix = f"{api_prefix}/books"


def test_get_all_books(test_client, fake_book_service, fake_session):
    """
    Test case for retrieving all books from the /books endpoint.

    This test simulates sending a GET request to the /books endpoint.
    It ensures that the book service is called to retrieve all books from the database.

    Args:
        test_client (TestClient): A TestClient instance to simulate HTTP requests to the FastAPI app.
        fake_book_service (Mock): A mocked book service to simulate book-related functionality.
        fake_session (Mock): A mocked database session used for the test.

    Asserts:
        - The get_all_books method of the book service is called once with the correct session.
    """

    response = test_client.get(url=f"{books_prefix}")

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_create_book(test_client, fake_book_service, fake_session):
    """
    Test case for creating a new book via the /books endpoint.

    This test simulates sending a POST request to the /books endpoint with book data.
    It verifies that the book service is correctly called to create a new book.

    Args:
        test_client (TestClient): A TestClient instance to simulate HTTP requests to the FastAPI app.
        fake_book_service (Mock): A mocked book service to simulate book-related functionality.
        fake_session (Mock): A mocked database session used for the test.

    Asserts:
        - The create_book method of the book service is called once with the correct book data and session.
    """

    book_data = {
        "title": "Test Title",
        "author": "Test Author",
        "publisher": "Test Publications",
        "published_date": "2024-12-10",
        "language": "English",
        "page_count": 215,
    }
    response = test_client.post(url=f"{books_prefix}", json=book_data)

    book_create_data = BookCreateModel(**book_data)
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(
        book_create_data, fake_session
    )


def test_get_book_by_uid(test_client, fake_book_service, test_book, fake_session):
    """
    Test case for retrieving a book by its unique identifier (UID) via the /books/{book_uid} endpoint.

    This test simulates sending a GET request to the /books/{book_uid} endpoint with a specific book UID.
    It ensures that the book service is called to retrieve the book by its UID.

    Args:
        test_client (TestClient): A TestClient instance to simulate HTTP requests to the FastAPI app.
        fake_book_service (Mock): A mocked book service to simulate book-related functionality.
        test_book (Book): A mocked book object to simulate a book being fetched by UID.
        fake_session (Mock): A mocked database session used for the test.

    Asserts:
        - The get_book method of the book service is called once with the correct book UID and session.
    """

    response = test_client.get(f"{books_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid, fake_session)


def test_update_book_by_uid(test_client, fake_book_service, test_book, fake_session):
    """
    Test case for updating a book by its unique identifier (UID) via the /books/{book_uid} endpoint.

    This test simulates sending a PUT request to the /books/{book_uid} endpoint with a specific book UID.
    It ensures that the book service is called to retrieve the book by UID and perform the update.

    Args:
        test_client (TestClient): A TestClient instance to simulate HTTP requests to the FastAPI app.
        fake_book_service (Mock): A mocked book service to simulate book-related functionality.
        test_book (Book): A mocked book object to simulate a book being updated by UID.
        fake_session (Mock): A mocked database session used for the test.

    Asserts:
        - The get_book method of the book service is called once with the correct book UID and session.
    """

    response = test_client.put(f"{books_prefix}/{test_book.uid}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.uid, fake_session)
