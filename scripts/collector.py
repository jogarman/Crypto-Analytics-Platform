import argparse
import asyncio
import logging
from datetime import datetime, timedelta

from crypto_analytics.schemas.pairs import PairStatus, TrackedPairCreate
from crypto_analytics.services.mock_data import generate_series
from crypto_analytics.store import store


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def ensure_default_pair() -> None:
    if store.list_pairs():
        return
    store.add_pair(TrackedPairCreate(coin_id="bitcoin", vs_currency="usd"))


async def collect_once(window_minutes: int, interval_minutes: int) -> None:
    ensure_default_pair()
    now = datetime.utcnow()
    start = now - timedelta(minutes=window_minutes)
    pairs = store.list_pairs(status=PairStatus.ACTIVE)
    if not pairs:
        logging.warning("No active pairs to collect for.")
        return

    for pair in pairs:
        points = generate_series(pair.coin_id, pair.vs_currency, start, now, interval_minutes)
        if not points:
            logging.warning("Pair %s/%s returned no points for window.", pair.coin_id, pair.vs_currency)
            continue
        timestamp, price, volume = points[-1]
        logging.info(
            "Collected %d points for %s/%s; latest @%s price=%.2f volume=%.2f",
            len(points),
            pair.coin_id,
            pair.vs_currency,
            timestamp.isoformat(),
            price,
            volume,
        )


async def main(window: int, interval: int, loop: bool) -> None:
    while True:
        await collect_once(window, interval)
        if not loop:
            break
        await asyncio.sleep(interval * 60)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Background collector that simulates CoinGecko ingestion every few minutes."
    )
    parser.add_argument("--window", type=int, default=60, help="Minutes of history to generate per collection.")
    parser.add_argument("--interval", type=int, default=5, help="Minutes between samples.")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Keep collecting every `interval` minutes (default action is a single run).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(window=args.window, interval=args.interval, loop=args.loop))

