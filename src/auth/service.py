"""
This module contains the UserService class, which encapsulates the business logic related to user management.
The service includes methods for creating, retrieving, updating users, and checking user existence.
It interacts with the database through SQLModel's AsyncSession and provides asynchronous operations to ensure
non-blocking I/O operations.
"""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_password_hash


class UserService:
    """
    A service class that contains methods for user-related operations such as:
    retrieving a user by email, checking if a user exists, creating a new user,
    and updating an existing user's information.
    """

    async def get_user_by_email(self, email: str, session: AsyncSession):
        """
        Retrieves a user from the database by their email address.

        Args:
            email (str): The email of the user to search for.
            session (AsyncSession): The database session to interact with the database.

        Returns:
            User: The first user matching the provided email, or None if no user is found.
        """

        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user

    async def user_exists(self, email: str, session: AsyncSession):
        """
        Checks if a user already exists in the database by their email.

        Args:
            email (str): The email to check for the existence of a user.
            session (AsyncSession): The database session to interact with the database.

        Returns:
            bool: True if the user exists, False otherwise.
        """

        user = await self.get_user_by_email(email=email, session=session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """
        Creates a new user in the database using the provided user data.

        Args:
            user_data (UserCreateModel): The data for the new user, including username, email, password, etc.
            session (AsyncSession): The database session to interact with the database.

        Returns:
            User: The newly created user object.
        """

        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user

    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        """
        Updates an existing user's information in the database.

        Args:
            user (User): The user object to update.
            user_data (dict): A dictionary of fields to update and their new values.
            session (AsyncSession): The database session to interact with the database.

        Returns:
            User: The updated user object.
        """

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await session.commit()

        return user
