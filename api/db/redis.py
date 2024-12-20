#!/usr/bin/python3

"""REDIS Client"""

import redis.asyncio as aioredis
from api.core.config import Config


JTI_EXPIRY = 36000

token_blocklist = aioredis.from_url(Config.REDIS_URL, decode_responses=True)


async def add_jti_to_block_list(jti: str) -> None:
    """Add token jti string to blocklist with expiration time."""
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    """Check if a token's jti is in the blocklist."""
    jti = await token_blocklist.get(jti)
    return jti is not None
