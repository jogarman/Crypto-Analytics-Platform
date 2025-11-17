from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError


class PriceDataRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.price_data

    async def upsert_points(
        self,
        coin_id: str,
        vs_currency: str,
        points: list[dict[str, float | datetime]],
        provider: str = "mock",
    ) -> None:
        operations = []
        for point in points:
            operations.append(
                UpdateOne(
                    {
                        "coin_id": coin_id,
                        "vs_currency": vs_currency,
                        "timestamp": point["timestamp"],
                    },
                    {
                        "$setOnInsert": {
                            "price": point["price"],
                            "volume": point["volume"],
                            "provider": provider,
                        }
                    },
                    upsert=True,
                )
            )
        if not operations:
            return
        try:
            await self._collection.bulk_write(operations, ordered=False)
        except BulkWriteError:
            # ignore duplicate writes
            pass

    async def fetch_range(
        self, coin_id: str, vs_currency: str, start: datetime, end: datetime
    ) -> list[dict]:
        cursor = self._collection.find(
            {
                "coin_id": coin_id,
                "vs_currency": vs_currency,
                "timestamp": {"$gte": start, "$lte": end},
            }
        ).sort("timestamp", 1)
        return await cursor.to_list(length=None)

    async def fetch_latest(self, coin_id: str, vs_currency: str) -> dict | None:
        document = await self._collection.find_one(
            {"coin_id": coin_id, "vs_currency": vs_currency},
            sort=[("timestamp", -1)],
        )
        return document

