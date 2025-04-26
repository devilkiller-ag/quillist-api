import uuid
from sqlmodel import Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(gt=0, lt=6)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(gt=0, lt=6)
    review_text: str
