# Crypto Analytics Platform — Iteration 1 Architecture

## Overview
- Frontend: React (19) + TypeScript + Vite + Tailwind. Single-page experience with routes managed by React Router and UI pieces in `src/components`. Charts rely on Highcharts via `highcharts-react-official`. The build pipeline stays with Vite (dev server `npm run dev`, build `npm run build`).
- Backend: Python 3.10+ orchestrated through Poetry, delivering a FastAPI app with Uvicorn. Services expose OpenAPI docs and instrument a healthz endpoint. MongoDB (local Atlas-compatible) stores tracked pairs and price data; Firestore is reserved for authentication metadata and optional experimentation.
- Background: Python/Poetry worker(s) that poll CoinGecko every 5 minutes per active pair, performing idempotent upserts keyed by `(coinId, vsCurrency, timestamp)` and respecting rate limits (retry/backoff). Scripts (seed/backfill/list) live alongside the API for local iteration.

## Frontend architecture
- Entry point: `src/main.tsx` boots React and injects `App`. Routing is centralized in `src/App.tsx` with routes like `/analytics`, `/settings`, `/track`.
- Pages live under `src/pages`. `AnalyticsPage` orchestrates the pair selector dropdown, date-range picker and metrics cards alongside the Highcharts canvas.
- State layer:
  - `useAnalyticsState` hook encapsulates the selected pair, date range, `status` (`idle|loading|ready|error|empty`), metrics, and chart series. It exposes `setPair`, `setRange`, `retry`, and `toggleTracking` (fake tracking flag for the mock).
  - Calls into `src/mocks/analytics.ts`, simulating fetches with 500 ms latency and deterministic synthetic price/volume series per `{coinId, vsCurrency, from, to}`. Errors appear roughly 1/8 calls to exercise error states.
- Presentation: small, reusable components in `src/components/ui` (Button, Card, Badge) are styled with Tailwind. Metrics cards (latest price, volume delta, percent change) and a stubbed “Track/Stop tracking” button live on the page together with the Highcharts line/area chart.
- Env + tooling: `.env` drives `VITE_API_BASE_URL` and `VITE_MODE` (`mock` vs `api`). `README.md` documents `npm install`, `npm run dev`, `npm run build`, how to switch to prod, and where to delete the local mocks in Iteration 2.5.

## Backend architecture
- FastAPI app in `app/` with routers grouped by feature (`routers/todos.py` currently — plan to replace with `routers/pairs.py` and `routers/analytics.py`). Core dependencies (config, Firestore helper, middlewares) remain similar to the TODO example but get reoriented toward Mongo/Coingecko.
- Proposed endpoints:
  1. `POST /api/pairs` starts tracking a pair (stores in `tracked_pairs` with status `active`).  
  2. `GET /api/pairs` lists tracked pairs (with optional filters).  
  3. `DELETE /api/pairs/{coinId}/{vsCurrency}` stops tracking.  
  4. `GET /api/analytics/{coinId}/{vsCurrency}` with `from`, `to`, `interval`.  
  5. `GET /api/analytics/{coinId}/{vsCurrency}/latest` for the freshest values.
- Mongo collections follow the suggested schema: `users`, `tracked_pairs` (unique `(userId, coinId, vsCurrency)`), `price_data` (compound indexes on `(coinId, vsCurrency, timestamp)`), with configuration read from `.env`.
- Background collectors: base job template triggers every 5 minutes (simulate via `asyncio` tasks + `async def collect_pair`). Use `CoinGecko` client wrapper supporting `/market_chart/range`. Inject retries/backoff and log structured info. Workers run via `poetry run python -m app.workers.collector` (documented in README).

## Iteration notes
- Iteration 1 focuses on the mocked frontend experience, no auth or backend wire-up. Frameworks and components mimic the `todo_front` scaffolding for familiarity, but all API calls remain local and deterministic until Iteration 2.5.
- Iterate future integrations by replacing `src/mocks/analytics.ts` with real `src/api` hooks calling FastAPI endpoints, swapping the UI tracking button to hit `/api/pairs`, and by wiring Firebase auth + JWT validation middleware.


