# Crypto Analytics Platform

This repository holds the first iteration of the backend for the **Crypto Analytics Platform** described in `Instructions.txt` and documented in `ARCHITECTURE.md`.

## Getting started

1. Copy `.env` to `.env.local` if you want to customize values or keep secrets out of source control.
2. Install dependencies with `poetry install`.
3. Run the API with:
   ```bash
   poetry run uvicorn crypto_analytics.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment variables

The default `.env` defines placeholders for:

- `MONGO_URI`: target MongoDB connection string.
- `COINGECKO_API_BASE`: CoinGecko base URL for future collectors.
- `FIREBASE_*`: Firebase project credentials for auth integration.
- `SECRET_KEY`: symmetric key for future JWT usage.
- `VITE_*`: frontend base URL and mode.

## Available endpoints

- `GET /healthz` — basic health indicator.
- `POST /api/pairs` — creates a tracked pair.
- `GET /api/pairs` — lists tracked pairs (filters by status optional).
- `DELETE /api/pairs/{coin_id}/{vs_currency}` — marks a pair as stopped.
- `GET /api/analytics/{coin_id}/{vs_currency}` — returns mock metric series with query parameters `from`, `to`, `interval_minutes`.
- `GET /api/analytics/{coin_id}/{vs_currency}/latest` — returns the last simulated datapoint.

## Testing

Run `poetry run pytest` once tests land in future iterations; currently this scaffolding has no test files but the tooling is wired up.

## Background scripts

- `poetry run python scripts/collector.py` — executes one collection window; add `--loop` to keep it running every `--interval` minutes and `--window` to control how many minutes of history it fakes per run.
- `poetry run python scripts/backfill.py bitcoin/usd` — produces deterministic historical data for the requested pair (default 24 hours of 5-minute samples). Adjust `--hours`/`--interval` to change the range.

## Frontend mock

- `frontend/` hosts the React + Vite + Tailwind iteration 1 UI.  
- Run `npm install` then `npm run dev` inside `frontend/` to see the analytics dashboard with Highcharts charts, pair selector, date-range picker, and metrics cards.  
- `src/mocks/analytics.ts` simulates the CoinGecko feeds with 500 ms latency and occasional errors; `useAnalyticsState` in `src/hooks/` consumes it and wires the rest of the UI.  
- The “Track pair” button is currently local to the SPA so we can later hook it into `/api/pairs`.


