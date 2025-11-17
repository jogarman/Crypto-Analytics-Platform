import { useCallback, useEffect, useMemo, useState } from 'react'
import dayjs from 'dayjs'

import { defaultPairs, fetchAnalyticsMock } from '../mocks/analytics'
import type { AnalyticsPayload, DateRange, PairSelection } from '../types/analytics'

type Status = 'idle' | 'loading' | 'ready' | 'empty' | 'error'

const DEFAULT_INTERVAL_MINUTES = 5

const defaultRange: DateRange = (() => {
  const to = new Date()
  const from = dayjs(to).subtract(7, 'day').toDate()
  return { from, to }
})()

export function useAnalyticsState() {
  const [selectedPair, setSelectedPair] = useState<PairSelection>(defaultPairs[0])
  const [range, setRange] = useState<DateRange>(defaultRange)
  const [status, setStatus] = useState<Status>('idle')
  const [error, setError] = useState<string | null>(null)
  const [payload, setPayload] = useState<AnalyticsPayload | null>(null)
  const [isTracking, setIsTracking] = useState<boolean>(false)

  const refresh = useCallback(async () => {
    setStatus('loading')
    setError(null)
    try {
      const data = await fetchAnalyticsMock({
        pair: selectedPair,
        range,
        intervalMinutes: DEFAULT_INTERVAL_MINUTES,
      })
      setPayload(data)
      setStatus(data.points.length > 0 ? 'ready' : 'empty')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error')
      setStatus('error')
    }
  }, [range, selectedPair])

  useEffect(() => {
    refresh()
  }, [refresh])

  const toggleTracking = useCallback(() => {
    setIsTracking((prev) => !prev)
  }, [])

  const retry = useCallback(() => {
    refresh()
  }, [refresh])

  const points = payload?.points ?? []

  const chartSeries = useMemo(() => {
    const priceSeries = points.map((point) => [point.timestamp, point.price] as const)
    const volumeSeries = points.map((point) => [point.timestamp, point.volume] as const)

    return {
      priceSeries,
      volumeSeries,
    }
  }, [points])

  const metrics = payload?.metrics ?? null

  return {
    selectedPair,
    setSelectedPair,
    range,
    setRange,
    status,
    error,
    chartSeries,
    points,
    metrics,
    isTracking,
    toggleTracking,
    retry,
  }
}

