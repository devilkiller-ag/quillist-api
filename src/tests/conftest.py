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
    yield mock_session


app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[refresh_token_bearer] = Mock()
app.dependency_overrides[role_checker] = Mock()


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_book_service():
    return mock_book_service


@pytest.fixture
def test_book():
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
