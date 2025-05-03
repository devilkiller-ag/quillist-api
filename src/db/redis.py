"""
This module provides utility functions for managing JWT token blocklisting using Redis.
It is primarily used to support logout functionality in a FastAPI application by temporarily
storing JWT IDs (jti) that should be considered invalid even before their expiry time.

Constants:
- JTI_EXPIRY: The expiry time (in seconds) for a JWT ID stored in the Redis blocklist.
"""

from redis.asyncio import Redis

from src.config import Config


# The number of seconds a JWT ID remains in the Redis blocklist (used for token invalidation)
JTI_EXPIRY = 3600  # 1 hour

redis_token_blocklist = Redis.from_url(Config.REDIS_URL)


async def add_jti_to_blocklist(jti: str):
    """
    Add a JWT ID (jti) to the Redis blocklist to mark it as invalid.

    This is typically used during logout to prevent reuse of the JWT token.

    Args:
        jti (str): The unique identifier of the JWT to be blocklisted.
    """

    await redis_token_blocklist.setex(name=jti, time=JTI_EXPIRY, value="")


async def token_in_blocklist(jti: str):
    """
    Check whether a JWT ID (jti) is present in the Redis blocklist.

    Args:
        jti (str): The unique identifier of the JWT to be checked.

    Returns:
        bool: True if the token is blocklisted, False otherwise.
    """

    result = await redis_token_blocklist.exists(jti)
    return bool(result)
