from datetime import datetime

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from ..schemas.pairs import PairStatus, TrackedPair, TrackedPairCreate


class PairAlreadyTracked(Exception):
    """Raised when the requested coin/vs pair already exists in the database."""


class PairNotFound(Exception):
    """Raised when attempting to operate on an unavailable pair."""


class TrackedPairRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.tracked_pairs

    async def create(self, payload: TrackedPairCreate) -> TrackedPair:
        now = datetime.utcnow()
        document = {
            "coin_id": payload.coin_id,
            "vs_currency": payload.vs_currency,
            "user_id": payload.user_id,
            "status": PairStatus.ACTIVE.value,
            "created_at": now,
            "updated_at": now,
        }
        try:
            await self._collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise PairAlreadyTracked(f"{payload.coin_id}/{payload.vs_currency} is already tracked.") from exc
        return TrackedPair(**document)

    async def list(self, status: PairStatus | None = None) -> list[TrackedPair]:
        query = {}
        if status:
            query["status"] = status.value
        cursor = self._collection.find(query).sort("created_at", -1)
        return [TrackedPair(**doc) for doc in await cursor.to_list(length=None)]

    async def stop(self, coin_id: str, vs_currency: str) -> TrackedPair:
        result = await self._collection.find_one_and_update(
            {"coin_id": coin_id, "vs_currency": vs_currency},
            {"$set": {"status": PairStatus.STOPPED.value, "updated_at": datetime.utcnow()}},
            return_document=True,
        )
        if not result:
            raise PairNotFound(f"Pair {coin_id}/{vs_currency} is not tracked.")
        return TrackedPair(**result)

    async def get(self, coin_id: str, vs_currency: str) -> TrackedPair:
        document = await self._collection.find_one({"coin_id": coin_id, "vs_currency": vs_currency})
        if not document:
            raise PairNotFound(f"Pair {coin_id}/{vs_currency} is not tracked.")
        return TrackedPair(**document)

