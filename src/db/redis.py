from redis.asyncio import Redis

from src.config import Config


JTI_EXPIRY = 3600  # 1 hour

redis_token_blocklist = Redis.from_url(Config.REDIS_URL)


# Add a JWT ID to the blocklist (for logout functionality)
async def add_jti_to_blocklist(jti: str):
    await redis_token_blocklist.setex(name=jti, time=JTI_EXPIRY, value="")


# Check if a JWT ID is blocklisted
async def token_in_blocklist(jti: str):
    result = await redis_token_blocklist.exists(jti)
    return bool(result)
