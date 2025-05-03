"""
This module contains fixtures and configuration for setting up tests in the FastAPI backend application.
It includes mock objects and dependencies, as well as configurations for the test client, services,
and session overrides, to facilitate unit testing.

Fixtures:
- test_client: A fixture that provides a TestClient instance for simulating requests to the FastAPI app.
- fake_session: A fixture that returns a mocked database session.
- fake_user_service: A fixture that returns a mocked user service.
- fake_book_service: A fixture that returns a mocked book service.
- test_book: A fixture that provides a mock Book object with sample data.

The file also includes overrides for FastAPI dependencies to mock external services and components used in the app.
"""

import uuid
import pytest
from datetime import datetime
from unittest.mock import Mock
from fastapi.testclient import TestClient

from src import app
from src.db.models import Book
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker


mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()

access_tocken_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(["admin"])


def get_mock_session():
    """
    Provides a mock session for database operations during testing.

    Yields:
        Mock: A mocked database session object to simulate database interactions.
    """

    yield mock_session


# Override FastAPI dependencies with the mocked versions for testing
app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[refresh_token_bearer] = Mock()
app.dependency_overrides[role_checker] = Mock()


@pytest.fixture
def test_client():
    """
    Provides a TestClient instance to simulate HTTP requests to the FastAPI app.

    Returns:
        TestClient: A test client for the FastAPI app that can be used to send requests
        and receive responses during tests.
    """

    return TestClient(app)


@pytest.fixture
def fake_session():
    """
    Provides a mocked database session for testing database-related operations.

    Returns:
        Mock: A mock session object to simulate interactions with the database.
    """

    return mock_session


@pytest.fixture
def fake_user_service():
    """
    Provides a mocked user service for testing user-related functionality.

    Returns:
        Mock: A mock user service object that simulates user management.
    """

    return mock_user_service


@pytest.fixture
def fake_book_service():
    """
    Provides a mocked book service for testing book-related functionality.

    Returns:
        Mock: A mock book service object that simulates book management.
    """

    return mock_book_service


@pytest.fixture
def test_book():
    """
    Provides a mock Book object with sample data for testing.

    Returns:
        Book: A Book object initialized with mock data for use in tests.
    """

    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="Italian Brainrot",
        description="Tralalero Tralala",
        page_count=143,
        language="Italian",
        published_date=datetime.now(),
        update_at=datetime.now(),
    )
