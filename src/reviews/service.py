"""
This module contains the service layer for handling review-related business logic in the system.
The service includes methods for creating, retrieving, and deleting reviews associated with books.
It interacts with the database through SQLModel's AsyncSession and provides asynchronous operations to ensure
non-blocking I/O operations.
"""

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from src.reviews.schemas import ReviewCreateModel
from src.errors import (
    UserNotFound,
    BookNotFound,
    ReviewNotFound,
    InsufficientPermission,
)

book_service = BookService()
user_service = UserService()


class ReviewService:
    """
    Service class to handle all review-related business logic.
    """

    async def get_review(self, review_uid: str, session: AsyncSession):
        """
        Retrieves a specific review by its unique identifier.

        Args:
            review_uid (str): The unique identifier of the review.
            session (AsyncSession): The database session to query.

        Returns:
            Review: The requested review.

        Raises:
            ReviewNotFound: If the review does not exist in the database.
            HTTPException: For any unexpected errors during the operation.
        """

        try:
            statement = select(Review).where(Review.uid == review_uid)
            result = await session.exec(statement)
            review = result.first()

            if not review:
                raise ReviewNotFound()

            return review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong while fetching the review: {e}",
            )

    async def get_all_reviews(self, session: AsyncSession):
        """
        Retrieves all reviews from the database, ordered by their creation date.

        Args:
            session (AsyncSession): The database session to query.

        Returns:
            List[Review]: A list of all reviews, ordered by creation date.

        Raises:
            ReviewNotFound: If no reviews are found in the database.
            HTTPException: For any unexpected errors during the operation.
        """

        try:
            statement = select(Review).order_by(desc(Review.created_at))
            result = await session.exec(statement)
            reviews = result.all()

            if not reviews:
                raise ReviewNotFound()

            return reviews

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong while fetching the reviews: {e}",
            )

    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        """
        Adds a review to a specific book.

        Args:
            user_email (str): The email of the user adding the review.
            book_uid (str): The unique identifier of the book being reviewed.
            review_data (ReviewCreateModel): The review data to be added.
            session (AsyncSession): The database session to execute the query.

        Returns:
            Review: The newly created review object.

        Raises:
            BookNotFound: If the book with the provided UID does not exist.
            UserNotFound: If the user with the provided email does not exist.
            HTTPException: For any unexpected errors during the operation.
        """

        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)

            if not book:
                raise BookNotFound()

            if not user:
                raise UserNotFound()

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()

            return new_review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong while adding the review: {e}",
            )

    async def delete_review_to_from_book(
        self, review_uid: str, user_email: str, session: AsyncSession
    ):
        """
        Deletes a review from a book.

        Args:
            review_uid (str): The unique identifier of the review to delete.
            user_email (str): The email of the user attempting to delete the review.
            session (AsyncSession): The database session to execute the query.

        Raises:
            ReviewNotFound: If the review with the provided UID does not exist.
            InsufficientPermission: If the user attempting to delete the review does not
                have permission (i.e., they are not the owner of the review).
            HTTPException: For any unexpected errors during the operation.
        """

        try:
            user = await user_service.get_user_by_email(user_email, session)

            review = await self.get_review(review_uid, session)

            if not review:
                raise ReviewNotFound()

            if review.user != user:
                raise InsufficientPermission()

            session.delete(review)
            await session.commit()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong while deleting the review: {e}",
            )
