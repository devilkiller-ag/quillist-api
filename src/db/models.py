"""
This module defines all SQLModel-based ORM classes used in the application.
It includes models for User, Book, Tag, Review, and the many-to-many relationship
between Book and Tag. These models define the schema for corresponding tables
in the PostgreSQL database using UUIDs as primary keys.
"""

import uuid
from typing import List, Optional
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship


class User(SQLModel, table=True):
    """
    Represents a registered user in the system.

    Attributes:
        uid (UUID): Unique identifier for the user.
        username (str): Chosen username.
        email (str): User's email address.
        first_name (str): First name.
        last_name (str): Last name.
        role (str): Role of the user (e.g., user, admin).
        is_verified (bool): Whether the user's email is verified.
        password_hash (str): Hashed password (excluded from serialization).
        created_at (datetime): Timestamp of account creation.
        updated_at (datetime): Timestamp of last update.
        books (List[Book]): Books submitted by the user.
        reviews (List[Review]): Reviews written by the user.
    """

    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class BookTag(SQLModel, table=True):
    """
    Association table for many-to-many relationship between Books and Tags.

    Attributes:
        book_uid (UUID): Foreign key referencing Book.
        tag_uid (UUID): Foreign key referencing Tag.
    """

    book_uid: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_uid: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Tag(SQLModel, table=True):
    """
    Represents a tag that can be associated with multiple books.

    Attributes:
        uid (UUID): Unique identifier for the tag.
        name (str): Tag name.
        created_at (datetime): Timestamp of tag creation.
        books (List[Book]): Books associated with this tag.
    """

    __tablename__ = "tags"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class Book(SQLModel, table=True):
    """
    Represents a book submitted by a user.

    Attributes:
        uid (UUID): Unique identifier for the book.
        title (str): Book title.
        author (str): Author name.
        publisher (str): Publishing house.
        published_date (date): Original publication date.
        page_count (int): Total number of pages.
        language (str): Language of the book.
        user_uid (UUID): Foreign key referencing submitting user.
        created_at (datetime): Timestamp of submission.
        updated_at (datetime): Timestamp of last update.
        user (User): Submitting user.
        reviews (List[Review]): Reviews associated with this book.
        tags (List[Tag]): Tags associated with this book.
    """

    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tags: List["Tag"] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    """
    Represents a review given by a user for a book.

    Attributes:
        uid (UUID): Unique identifier for the review.
        rating (int): Rating between 1 and 5.
        review_text (str): Review description.
        user_uid (UUID): Foreign key referencing the user.
        book_uid (UUID): Foreign key referencing the book.
        created_at (datetime): Timestamp of review creation.
        updated_at (datetime): Timestamp of last update.
        user (User): User who wrote the review.
        book (Book): Book being reviewed.
    """

    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(gt=0, lt=6)
    review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
