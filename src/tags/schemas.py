"""
This module contains Pydantic models used for serializing and deserializing tag-related data in the system.

Schemas:
- TagModel: Represents the structure of a tag returned by the API.
- TagCreateModel: Represents the structure of the data required to create a new tag.
- TagAddModel: Represents the structure for adding multiple tags to a book.
"""

import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel


class TagModel(BaseModel):
    """
    TagModel represents the structure of a tag object returned by the API.

    Attributes:
        uid (uuid.UUID): A unique identifier for the tag.
        name (str): The name of the tag.
        created_at (datetime): The timestamp when the tag was created.
    """

    uid: uuid.UUID
    name: str
    created_at: datetime


class TagCreateModel(BaseModel):
    """
    TagCreateModel represents the data required to create a new tag.

    Attributes:
        name (str): The name of the tag to be created.
    """

    name: str


class TagAddModel(BaseModel):
    """
    TagAddModel represents the structure for adding multiple tags at once.

    Attributes:
        tags (List[TagCreateModel]): A list of tags to be added.
    """

    tags: List[TagCreateModel]
