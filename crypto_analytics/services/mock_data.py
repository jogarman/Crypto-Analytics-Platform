from datetime import datetime, timedelta
import math
import random
from typing import Iterable, List, Tuple


def _seed_for_pair(coin_id: str, vs_currency: str, start: datetime, end: datetime) -> int:
    return hash((coin_id.lower(), vs_currency.lower(), int(start.timestamp()), int(end.timestamp())))


def generate_series(
    coin_id: str,
    vs_currency: str,
    start: datetime,
    end: datetime,
    interval_minutes: int = 5,
) -> List[Tuple[datetime, float, float]]:
    if start >= end:
        return []

    rng = random.Random(_seed_for_pair(coin_id, vs_currency, start, end))
    points: List[Tuple[datetime, float, float]] = []
    current = start
    base_price = 50 + rng.random() * 100
    volatility = 0.03
    while current <= end:
        drift = math.sin(current.timestamp() / 300_000) * 2
        noise = rng.uniform(-1, 1)
        price = max(0.01, base_price + drift + noise)
        volume = max(1, rng.uniform(10, 100) * (1 + rng.random() * 0.5))
        points.append((current, round(price, 2), round(volume, 2)))
        base_price = price
        current += timedelta(minutes=interval_minutes)
    return points

