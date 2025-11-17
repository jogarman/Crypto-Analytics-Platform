import argparse
import logging
from datetime import datetime, timedelta

from crypto_analytics.schemas.pairs import TrackedPairCreate
from crypto_analytics.services.mock_data import generate_series
from crypto_analytics.store import PairNotFound, store


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def parse_timestamp(value: str | None, default: datetime) -> datetime:
    if value is None:
        return default
    try:
        return datetime.utcfromtimestamp(int(value))
    except ValueError:
        return datetime.fromisoformat(value)


def ensure_pair(coin_id: str, vs_currency: str):
    try:
        return store.get_pair(coin_id, vs_currency)
    except PairNotFound:
        logging.info("Pair %s/%s not tracked yet; adding as active.", coin_id, vs_currency)
        return store.add_pair(TrackedPairCreate(coin_id=coin_id, vs_currency=vs_currency))


def run_backfill(coin_id: str, vs_currency: str, points_window: timedelta, interval_minutes: int):
    end = datetime.utcnow()
    start = end - points_window
    ensure_pair(coin_id, vs_currency)
    raw_points = generate_series(coin_id, vs_currency, start, end, interval_minutes)
    logging.info(
        "Backfilled %d points for %s/%s between %s and %s",
        len(raw_points),
        coin_id,
        vs_currency,
        start.isoformat(),
        end.isoformat(),
    )
    return raw_points


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill historical analytics data for a pair.")
    parser.add_argument("pair", help="Pair identifier formatted as coinId/vsCurrency (e.g. bitcoin/usd).")
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="How many hours back to backfill (default 24).",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval minutes between samples.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coin_id, vs_currency = args.pair.split("/", 1)
    window = timedelta(hours=args.hours)
    run_backfill(coin_id, vs_currency, window, args.interval)


if __name__ == "__main__":
    main()

