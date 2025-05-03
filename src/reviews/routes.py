"""
This module defines the API routes related to review management in the system.

Routes:
- get_all_reviews: Retrieve all reviews in the system (accessible by admin only).
- get_review: Retrieve the details of a specific review by its unique identifier.
- add_review_to_book: Add a new review to a specific book by an authenticated user.
- delete_book: Delete a review from a book (allowed for the review author or an admin).
"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.db.main import get_session
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreateModel
from src.auth.dependencies import RoleChecker, get_current_user


review_router = APIRouter()

review_service = ReviewService()

admin_role_checker = RoleChecker(allowed_roles=["admin"])
user_role_checker = RoleChecker(allowed_roles=["user", "admin"])


@review_router.get("/", dependencies=[Depends(admin_role_checker)])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    """
    Retrieve all reviews in the system (admin only).

    Args:
        session (AsyncSession): SQLAlchemy session object injected via dependency.

    Dependencies:
        - RoleChecker: Ensures the user has the 'admin' role.

    Returns:
        List[Review]: A list of all reviews in the database.
    """

    reviews = await review_service.get_all_reviews(session)

    return reviews


@review_router.get("/{review_uid}", dependencies=[Depends(user_role_checker)])
async def get_review(review_uid: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a specific review by its UID.

    Args:
        review_uid (str): Unique identifier of the review.
        session (AsyncSession): SQLAlchemy session object.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        Review: The requested review object, if found.
    """

    review = await review_service.get_review(review_uid, session)

    return review


@review_router.post("/book/{book_uid}", dependencies=[Depends(user_role_checker)])
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Add a new review to a specific book.

    Args:
        book_uid (str): UID of the book to which the review is being added.
        review_data (ReviewCreateModel): Data for the new review.
        current_user (User): Currently authenticated user.
        session (AsyncSession): SQLAlchemy session object.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        Review: The newly created review object.
    """

    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session,
    )

    return new_review


@review_router.delete(
    "/{review_uid}",
    dependencies=[Depends(user_role_checker)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    review_uid: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a review by its UID. Only the reviewer or an admin can perform this action.

    Args:
        review_uid (str): UID of the review to be deleted.
        current_user (User): Currently authenticated user.
        session (AsyncSession): SQLAlchemy session object.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        None
    """

    await review_service.delete_review_to_from_book(
        review_uid=review_uid, user_email=current_user.email, session=session
    )

    return None
