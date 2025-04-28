from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import Book
from src.db.main import get_session
from src.tags.service import TagService
from src.tags.schemas import TagAddModel, TagCreateModel, TagModel
from src.auth.dependencies import RoleChecker


tags_router = APIRouter()

tag_service = TagService()

user_role_checker = RoleChecker(["user", "admin"])


@tags_router.get(
    "/", response_model=List[TagModel], dependencies=[Depends(user_role_checker)]
)
async def get_all_tags(session: AsyncSession = Depends(get_session)):
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
    deleted_tag = await tag_service.delete_tag(tag_uid, session)

    if not deleted_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
