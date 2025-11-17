from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import settings

_client: Optional[AsyncIOMotorClient] = None
_database: Optional[AsyncIOMotorDatabase] = None


def get_database() -> AsyncIOMotorDatabase:
    if _database is None:
        raise RuntimeError("Database has not been initialized yet.")
    return _database


async def init_database() -> AsyncIOMotorDatabase:
    global _client, _database
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)
    _database = _client[settings.mongo_db]
    await _database.tracked_pairs.create_index(
        [("coin_id", 1), ("vs_currency", 1)],
        unique=True,
        name="unique_pair",
    )
    await _database.price_data.create_index(
        [("coin_id", 1), ("vs_currency", 1), ("timestamp", 1)],
        unique=True,
        name="unique_price_point",
    )
    return _database


def close_database() -> None:
    if _client:
        _client.close()

