#!/usr/bin/python3

"""REDIS Client"""

import aioredis

from api.core.config import Config

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_block_list(jti: str) -> None:
    """Add token jti string to blacklist"""
    await token_blocklist
