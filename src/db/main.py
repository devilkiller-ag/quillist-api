"""
This module handles the setup and initialization of the asynchronous database engine,
and provides utility functions for creating the database schema and generating
asynchronous sessions to interact with the database.
"""

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config


# Create an asynchronous SQLAlchemy engine using the database URL from the configuration
engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=False))


async def init_db():
    """
    Initialize the database schema.

    This function creates all tables defined in the SQLModel metadata if they don't exist.
    It is usually called once at application startup.
    """

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Yield a new asynchronous database session.

    This function is used as a dependency in FastAPI endpoints to provide a database session
    for performing queries and transactions.

    Yields:
        AsyncSession: An instance of the SQLAlchemy async session.
    """

    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        yield session
