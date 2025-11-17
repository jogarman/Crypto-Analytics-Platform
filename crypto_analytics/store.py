from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

from .schemas.pairs import PairStatus, TrackedPair, TrackedPairCreate


PairKey = Tuple[str, str]


class PairAlreadyTracked(Exception):
    pass


class PairNotFound(Exception):
    pass


@dataclass
class InMemoryStore:
    tracked_pairs: Dict[PairKey, TrackedPair]

    def __init__(self):
        self.tracked_pairs = {}

    def _key(self, coin_id: str, vs_currency: str) -> PairKey:
        return coin_id.lower(), vs_currency.lower()

    def add_pair(self, payload: TrackedPairCreate) -> TrackedPair:
        key = self._key(payload.coin_id, payload.vs_currency)
        existing = self.tracked_pairs.get(key)
        now = datetime.utcnow()
        if existing and existing.status == PairStatus.ACTIVE:
            raise PairAlreadyTracked(f"Pair {payload.coin_id}/{payload.vs_currency} is already tracked.")
        tracked = TrackedPair(
            coin_id=payload.coin_id,
            vs_currency=payload.vs_currency,
            user_id=payload.user_id,
            status=PairStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        self.tracked_pairs[key] = tracked
        return tracked

    def list_pairs(self, status: PairStatus | None = None) -> List[TrackedPair]:
        pairs = list(self.tracked_pairs.values())
        if status:
            return [p for p in pairs if p.status == status]
        return pairs

    def stop_pair(self, coin_id: str, vs_currency: str) -> TrackedPair:
        key = self._key(coin_id, vs_currency)
        pair = self.tracked_pairs.get(key)
        if not pair:
            raise PairNotFound(f"Pair {coin_id}/{vs_currency} is not tracked.")
        pair.status = PairStatus.STOPPED
        pair.updated_at = datetime.utcnow()
        self.tracked_pairs[key] = pair
        return pair

    def get_pair(self, coin_id: str, vs_currency: str) -> TrackedPair:
        key = self._key(coin_id, vs_currency)
        pair = self.tracked_pairs.get(key)
        if not pair:
            raise PairNotFound(f"Pair {coin_id}/{vs_currency} is not tracked.")
        return pair


store = InMemoryStore()

