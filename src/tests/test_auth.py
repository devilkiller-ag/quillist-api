from src import api_prefix
from src.auth.schemas import UserCreateModel


auth_prefix = f"{api_prefix}/auth"


def test_user_creation(fake_session, fake_user_service, test_client):
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
