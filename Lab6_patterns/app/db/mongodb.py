from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        settings = get_settings()
        logger.info("Connecting to MongoDB at %s", settings.mongodb_uri)
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    client = get_client()
    settings = get_settings()
    return client[settings.mongodb_db]


async def close_client() -> None:
    global _client
    if _client:
        logger.info("Closing MongoDB connection")
        _client.close()
        _client = None


@asynccontextmanager
async def lifespan_db() -> AsyncIterator[AsyncIOMotorDatabase]:
    db = get_database()
    try:
        yield db
    finally:
        await close_client()
