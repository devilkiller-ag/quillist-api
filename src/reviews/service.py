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
    async def get_review(self, review_uid: str, session: AsyncSession):
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
