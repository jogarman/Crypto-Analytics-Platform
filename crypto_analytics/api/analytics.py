from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query

from ..schemas.analytics import (
    AnalyticsMetrics,
    AnalyticsResponse,
    AnalyticsQuery,
    LatestPointResponse,
    SeriesPoint,
)
from ..services.mock_data import generate_series
from ..store import store

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def _resolve_range(query: AnalyticsQuery) -> tuple[datetime, datetime]:
    now = datetime.utcnow()
    to_ts = datetime.utcfromtimestamp(query.to_ts) if query.to_ts else now
    from_ts = (
        datetime.utcfromtimestamp(query.from_ts)
        if query.from_ts
        else to_ts - timedelta(hours=24)
    )
    if from_ts >= to_ts:
        raise HTTPException(status_code=400, detail="`from` must be before `to`.")
    return from_ts, to_ts


def _build_metrics(points: list[SeriesPoint]) -> AnalyticsMetrics:
    prices = [p.price for p in points]
    volume = sum(p.volume for p in points)
    return AnalyticsMetrics(
        latest_price=prices[-1],
        lowest_price=min(prices),
        highest_price=max(prices),
        total_volume=round(volume, 2),
    )


@router.get("/{coin_id}/{vs_currency}", response_model=AnalyticsResponse)
async def describe_pair(
    coin_id: str,
    vs_currency: str,
    from_ts: int | None = Query(None, alias="from"),
    to_ts: int | None = Query(None, alias="to"),
    interval_minutes: int = Query(5, gt=0),
) -> AnalyticsResponse:
    store.get_pair(coin_id, vs_currency)  # ensure the pair exists or raise
    query = AnalyticsQuery(from_ts=from_ts, to_ts=to_ts, interval_minutes=interval_minutes)
    start, end = _resolve_range(query)
    raw_points = generate_series(coin_id, vs_currency, start, end, interval_minutes)
    points = [SeriesPoint(timestamp=ts, price=price, volume=volume) for ts, price, volume in raw_points]
    if not points:
        raise HTTPException(status_code=404, detail="No data available for the requested range.")
    metrics = _build_metrics(points)
    return AnalyticsResponse(
        coin_id=coin_id,
        vs_currency=vs_currency,
        points=points,
        metrics=metrics,
    )


@router.get("/{coin_id}/{vs_currency}/latest", response_model=LatestPointResponse)
async def latest_value(
    coin_id: str,
    vs_currency: str,
    interval_minutes: int = Query(5, gt=0),
) -> LatestPointResponse:
    store.get_pair(coin_id, vs_currency)
    end = datetime.utcnow()
    start = end - timedelta(hours=1)
    raw_points = generate_series(coin_id, vs_currency, start, end, interval_minutes)
    if not raw_points:
        raise HTTPException(status_code=404, detail="No data points available.")
    ts, price, volume = raw_points[-1]
    return LatestPointResponse(
        coin_id=coin_id,
        vs_currency=vs_currency,
        point=SeriesPoint(timestamp=ts, price=price, volume=volume),
    )

