from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, constr


class PairStatus(str, Enum):
    ACTIVE = "active"
    STOPPED = "stopped"


class TrackedPairBase(BaseModel):
    coin_id: constr(strip_whitespace=True, min_length=1) = Field(..., description="Identifier used by CoinGecko.")
    vs_currency: constr(strip_whitespace=True, min_length=1) = Field(
        ..., description="Quote currency used for the pair."
    )
    user_id: constr(strip_whitespace=True, min_length=1) | None = Field(
        None, description="Optional user identifier."
    )


class TrackedPairCreate(TrackedPairBase):
    pass


class TrackedPair(TrackedPairBase):
    status: PairStatus = Field(default=PairStatus.ACTIVE, description="Current tracking status.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

