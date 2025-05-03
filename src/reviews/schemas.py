"""
This module defines the Pydantic schemas used for review-related operations in the system.

Schemas:
- ReviewModel: Represents the full structure of a review returned from the database.
- ReviewCreateModel: Represents the data required to create a new review.
"""

import uuid
from sqlmodel import Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ReviewModel(BaseModel):
    """
    Schema for representing a review retrieved from the database.

    Attributes:
        uid (uuid.UUID): Unique identifier for the review.
        rating (int): Rating value given by the user (must be between 1 and 5).
        review_text (str): Textual content of the review.
        user_uid (Optional[uuid.UUID]): Unique identifier of the user who wrote the review.
        book_uid (Optional[uuid.UUID]): Unique identifier of the book being reviewed.
        created_at (datetime): Timestamp when the review was created.
        updated_at (datetime): Timestamp when the review was last updated.
    """

    uid: uuid.UUID
    rating: int = Field(gt=0, lt=6)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    """
    Schema for creating a new review.

    Attributes:
        rating (int): Rating value given by the user (must be between 1 and 5).
        review_text (str): Textual content of the review.
    """

    rating: int = Field(gt=0, lt=6)
    review_text: str
