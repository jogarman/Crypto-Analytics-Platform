from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, PositiveInt


class SeriesPoint(BaseModel):
    timestamp: datetime
    price: float = Field(..., description="Closing price for the window.")
    volume: float = Field(..., description="Volume observed during the window.")


class AnalyticsMetrics(BaseModel):
    latest_price: float = Field(..., description="Last evaluated price.")
    lowest_price: float = Field(..., description="Lowest price in the range.")
    highest_price: float = Field(..., description="Highest price in the range.")
    total_volume: float = Field(..., description="Accumulated volume for the whole range.")


class AnalyticsResponse(BaseModel):
    coin_id: str
    vs_currency: str
    points: List[SeriesPoint]
    metrics: AnalyticsMetrics


class LatestPointResponse(BaseModel):
    coin_id: str
    vs_currency: str
    point: SeriesPoint


class AnalyticsQuery(BaseModel):
    from_ts: PositiveInt | None = Field(None, alias="from", description="Unix timestamp (seconds) to start the range.")
    to_ts: PositiveInt | None = Field(None, alias="to", description="Unix timestamp (seconds) to end the range.")
    interval_minutes: PositiveInt = Field(
        default=5, description="Sampling interval in minutes."
    )

