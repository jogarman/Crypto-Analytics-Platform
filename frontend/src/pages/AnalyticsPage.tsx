import { useCallback, useRef } from 'react'

import type HighchartsReact from 'highcharts-react-official'

import PairSelector from '../components/PairSelector'
import DateRangePicker from '../components/DateRangePicker'
import MetricsCard from '../components/MetricsCard'
import AnalyticsChart from '../components/AnalyticsChart'
import { useAnalyticsState } from '../hooks/useAnalyticsState'

const formatPrice = (value: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }).format(value)

const formatVolume = (value: number) =>
  `${Math.round(value).toLocaleString()} units`

function statusLabel(status: string) {
  switch (status) {
    case 'loading':
      return 'Loading analytics...'
    case 'error':
      return 'Unable to load current data.'
    case 'empty':
      return 'No data available for that range.'
    default:
      return 'Data loaded.'
  }
}

function AnalyticsPage() {
  const {
    selectedPair,
    setSelectedPair,
    range,
    setRange,
    status,
    error,
    points,
    metrics,
    isTracking,
    toggleTracking,
    retry,
  } = useAnalyticsState()

  const chartRef = useRef<HighchartsReact.RefObject | null>(null)

  const adjustZoom = useCallback((direction: 'in' | 'out') => {
    const chart = chartRef.current?.chart
    if (!chart) return
    const axis = chart.xAxis[0]
    if (!axis) return
    const { min, max, dataMin, dataMax } = axis.getExtremes()
    const span = Math.max(max - min, 5 * 60 * 1000)
    const dataSpan = dataMax - dataMin
    if (!dataSpan) return
    const factor = direction === 'in' ? 0.75 : 1.25
    let newSpan = span * factor
    newSpan = Math.max(newSpan, 5 * 60 * 1000)
    newSpan = Math.min(newSpan, dataSpan)
    const center = min + span / 2
    let newMin = center - newSpan / 2
    let newMax = center + newSpan / 2
    if (newMin < dataMin) {
      newMin = dataMin
      newMax = newMin + newSpan
    }
    if (newMax > dataMax) {
      newMax = dataMax
      newMin = newMax - newSpan
    }
    axis.setExtremes(newMin, newMax, true, undefined, { trigger: 'zoom' })
  }, [])

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-4 py-10">
      <header className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
              Crypto Analytics
            </p>
            <h1 className="text-3xl font-semibold text-slate-900">Market overview</h1>
            <p className="text-sm text-slate-500">
              Select a pair and a date range to see price & volume trends.
            </p>
          </div>
          <button
            onClick={toggleTracking}
            className="rounded-2xl border border-transparent bg-brand-500 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600"
          >
            {isTracking ? 'Stop tracking' : 'Track pair'}
          </button>
        </div>
        <div className="mt-4 flex items-center justify-between text-sm text-slate-500">
          <span>{statusLabel(status)}</span>
          {status === 'error' && (
            <button onClick={retry} className="text-blue-600 underline-offset-4 hover:text-blue-500">
              Retry
            </button>
          )}
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-[280px,1fr]">
        <aside className="space-y-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <PairSelector value={selectedPair} onChange={setSelectedPair} />
          <div className="space-y-1">
            <p className="text-sm font-semibold text-slate-600">Date range</p>
            <DateRangePicker range={range} onChange={setRange} />
          </div>
          <div className="rounded-2xl border border-dashed border-slate-200 p-4 text-sm text-slate-500">
            Analytics refresh automatically with simulated latency. Use “Retry” if the mock fails (roughly 1/8 calls).
          </div>
        </aside>

        <section className="space-y-6">
          <div className="grid gap-4 md:grid-cols-3">
            <MetricsCard
              label="Latest price"
              value={metrics ? formatPrice(metrics.latestPrice) : '—'}
              helper="Real-time price"
              trend={metrics?.percentageChange}
            />
            <MetricsCard
              label="24h range"
              value={
                metrics
                  ? `${formatPrice(metrics.lowestPrice)} — ${formatPrice(metrics.highestPrice)}`
                  : '—'
              }
              helper="Lowest / highest in the range"
            />
            <MetricsCard
              label="Volume"
              value={metrics ? formatVolume(metrics.totalVolume) : '—'}
              helper="Aggregated trade volume"
            />
          </div>

          {status === 'loading' && (
            <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center text-slate-500 shadow-sm">
              Loading historical chart...
            </div>
          )}

          {status === 'error' && error && (
            <div className="rounded-3xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700 shadow-sm">
              <p>{error}</p>
            </div>
          )}

          <div className="flex items-center justify-end gap-2 text-sm">
            <button
              type="button"
              onClick={() => adjustZoom('in')}
              className="rounded-full border border-slate-300 bg-white px-3 py-1 shadow-sm hover:border-slate-400"
            >
              Zoom +
            </button>
            <button
              type="button"
              onClick={() => adjustZoom('out')}
              className="rounded-full border border-slate-300 bg-white px-3 py-1 shadow-sm hover:border-slate-400"
            >
              Zoom -
            </button>
          </div>

          <AnalyticsChart points={points} loading={status === 'loading'} chartRef={chartRef} />
        </section>
      </div>
    </main>
  )
}

export default AnalyticsPage

