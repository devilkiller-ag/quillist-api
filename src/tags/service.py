"""
This module defines the TagService class that contains the business logic for managing tags within the application.
The service includes methods for creating, retrieving, updating, and deleting tags, as well as adding tags to books.
It interacts with the database through SQLModel's AsyncSession and provides asynchronous operations to ensure
non-blocking I/O operations.
"""

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Tag
from src.books.service import BookService
from src.tags.schemas import TagAddModel, TagCreateModel
from src.errors import (
    BookNotFound,
    TagNotFound,
    TagAlreadyExists,
)


book_service = BookService()


class TagService:
    """
    TagService handles the logic for managing tags in the system.
    """

    async def get_tags(self, session: AsyncSession):
        """
        Retrieve all tags from the database, ordered by the creation timestamp.

        Args:
            session (AsyncSession): The asynchronous session used for database operations.

        Returns:
            List[Tag]: A list of all tags, ordered by creation date.
        """

        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)

        return result.all()

    async def add_tags_to_book(
        self, book_uid: str, tag_data: TagAddModel, session: AsyncSession
    ):
        """
        Add tags to a specific book by its unique identifier.

        Args:
            book_uid (str): The unique identifier of the book to which tags will be added.
            tag_data (TagAddModel): The data containing the tags to be added.
            session (AsyncSession): The asynchronous session used for database operations.

        Returns:
            Book: The updated book with associated tags.

        Raises:
            BookNotFound: If no book with the specified UID is found.
        """

        book = await book_service.get_book(book_uid=book_uid, session=session)

        if not book:
            raise BookNotFound()

        for tag_item in tag_data.tags:
            result = await session.exec(select(Tag).where(Tag.name == tag_item.name))

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        """
        Retrieve a tag by its unique identifier.

        Args:
            tag_uid (str): The unique identifier of the tag.
            session (AsyncSession): The asynchronous session used for database operations.

        Returns:
            Tag: The tag corresponding to the provided UID.

        Raises:
            TagNotFound: If no tag with the specified UID is found.
        """

        statement = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(statement)

        return result.first()

    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        """
        Create a new tag and store it in the database.

        Args:
            tag_data (TagCreateModel): The data for the tag to be created.
            session (AsyncSession): The asynchronous session used for database operations.

        Returns:
            Tag: The newly created tag.

        Raises:
            TagAlreadyExists: If a tag with the same name already exists.
        """

        statement = select(Tag).where(Tag.name == tag_data.name)
        result = await session.exec(statement)
        tag = result.first()

        if tag:
            raise TagAlreadyExists()

        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)
        await session.commit()

        return new_tag

    async def update_tag(
        self, tag_uid, tag_update_data: TagCreateModel, session: AsyncSession
    ):
        """
        Update an existing tag with new data.

        Args:
            tag_uid (str): The unique identifier of the tag to be updated.
            tag_update_data (TagCreateModel): The updated data for the tag.
            session (AsyncSession): The asynchronous session used for database operations.

        Returns:
            Tag: The updated tag.

        Raises:
            TagNotFound: If no tag with the specified UID is found.
        """

        tag = await self.get_tag_by_uid(tag_uid, session)

        if not tag:
            raise TagNotFound()

        update_data_dict = tag_update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

            await session.commit()
            await session.refresh(tag)

        return tag

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        """Delete a tag"""

        tag = await self.get_tag_by_uid(tag_uid, session)

        if not tag:
            raise TagNotFound()

        await session.delete(tag)
        await session.commit()
