"""
This module contains the FastAPI routes for managing tags in the system. It provides endpoints
for retrieving, creating, updating, and deleting tags, as well as adding tags to books.

Routes:
- get_all_tags: Retrieve all tags.
- create_tag: Create a new tag.
- add_tags_to_book: Add tags to a specific book.
- update_tag: Update an existing tag.
- delete_tag: Delete a tag.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import Book
from src.db.main import get_session
from src.tags.service import TagService
from src.tags.schemas import TagAddModel, TagCreateModel, TagModel
from src.auth.dependencies import RoleChecker
from src.errors import TagNotFound


tags_router = APIRouter()

tag_service = TagService()

user_role_checker = RoleChecker(["user", "admin"])


@tags_router.get(
    "/", response_model=List[TagModel], dependencies=[Depends(user_role_checker)]
)
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    """
    Retrieves a list of all tags from the system.

    Args:
        session (AsyncSession): The database session for querying.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        List[TagModel]: A list of tags in the system.
    """

    tags = await tag_service.get_tags(session)

    return tags


@tags_router.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(user_role_checker)],
)
async def create_tag(
    tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)
) -> TagModel:
    """
    Creates a new tag in the system.

    Args:
        tag_data (TagCreateModel): The data for the tag to be created.
        session (AsyncSession): The database session for committing the new tag.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        TagModel: The created tag.
    """

    tag_added = await tag_service.add_tag(tag_data=tag_data, session=session)

    return tag_added


@tags_router.post(
    "/book/{book_uid}/tags",
    response_model=Book,
    dependencies=[Depends(user_role_checker)],
)
async def add_tags_to_book(
    book_uid: str, tag_data: TagAddModel, session: AsyncSession = Depends(get_session)
) -> Book:
    """
    Adds tags to a specific book.

    Args:
        book_uid (str): The unique identifier of the book.
        tag_data (TagAddModel): The tags to be added to the book.
        session (AsyncSession): The database session for updating the book.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        Book: The updated book with the new tags.
    """

    book_with_tag = await tag_service.add_tags_to_book(
        book_uid=book_uid, tag_data=tag_data, session=session
    )

    return book_with_tag


@tags_router.put(
    "/{tag_uid}", response_model=TagModel, dependencies=[Depends(user_role_checker)]
)
async def update_tag(
    tag_uid: str,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
) -> TagModel:
    """
    Updates an existing tag with new data.

    Args:
        tag_uid (str): The unique identifier of the tag to be updated.
        tag_update_data (TagCreateModel): The new data for the tag.
        session (AsyncSession): The database session for committing the update.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Returns:
        TagModel: The updated tag.
    """

    updated_tag = await tag_service.update_tag(tag_uid, tag_update_data, session)

    return updated_tag


@tags_router.delete(
    "/{tag_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_role_checker)],
)
async def delete_tag(
    tag_uid: str, session: AsyncSession = Depends(get_session)
) -> None:
    """
    Deletes a tag from the system.

    Args:
        tag_uid (str): The unique identifier of the tag to be deleted.
        session (AsyncSession): The database session for committing the deletion.

    Dependencies:
        - RoleChecker: Ensures the user has the 'user' or 'admin' role.

    Raises:
        TagNotFound: If the tag with the specified UID does not exist.
    """

    deleted_tag = await tag_service.delete_tag(tag_uid, session)

    if not deleted_tag:
        raise TagNotFound()
