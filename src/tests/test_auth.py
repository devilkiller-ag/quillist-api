"""
This module contains test cases for the authentication-related endpoints.
"""

from src import api_prefix
from src.auth.schemas import UserCreateModel


auth_prefix = f"{api_prefix}/auth"


def test_user_creation(fake_session, fake_user_service, test_client):
    """
    Test case for creating a new user via the signup endpoint.

    This test simulates sending a POST request to the /signup endpoint with user data.
    It verifies that the user service is correctly called to check if the user already exists,
    and then to create the new user.

    Args:
        fake_session (Mock): A mocked session to simulate database operations.
        fake_user_service (Mock): A mocked user service to simulate user-related functionality.
        test_client (TestClient): A TestClient instance to simulate HTTP requests to the FastAPI app.

    Asserts:
        - The user_exisits method of the user service is called once with the correct arguments.
        - The user_create method of the user service is called once with the correct user data.
    """

    signup_data = {
        "email": "bomberdiro@gmail.com",
        "username": "bomberdiro",
        "password": "bomberpswd",
        "first_name": "Bomberdiro",
        "last_name": "Crocodilo",
    }
    user_data = UserCreateModel(**signup_data)

    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=signup_data,
    )

    assert fake_user_service.user_exisits_called_once()
    assert fake_user_service.user_exisits_called_once_with(
        signup_data["email"], fake_session
    )

    assert fake_user_service.user_create_called_once()
    assert fake_user_service.user_create_called_once_with(user_data, fake_session)
