import type { AnalyticsMetrics, AnalyticsPayload, DateRange } from '../types/analytics'

const BASE_LATENCY_MS = 500

const KNOWN_PAIRS = [
  { coinId: 'bitcoin', vsCurrency: 'usd' },
  { coinId: 'ethereum', vsCurrency: 'usd' },
  { coinId: 'ethereum', vsCurrency: 'btc' },
  { coinId: 'solana', vsCurrency: 'usd' },
  { coinId: 'cardano', vsCurrency: 'usd' },
]

type FetchRequest = {
  pair: typeof KNOWN_PAIRS[number]
  range: DateRange
  intervalMinutes?: number
}

function mulberry32(seed: number) {
  return () => {
    let t = (seed += 0x6d2b79f5)
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function seedFromRequest(request: FetchRequest) {
  const { pair, range } = request
  const values = [
    pair.coinId.toLowerCase(),
    pair.vsCurrency.toLowerCase(),
    Math.floor(range.from.getTime() / 1000).toString(),
    Math.floor(range.to.getTime() / 1000).toString(),
  ]
  return values.reduce((acc, value) => {
    let hash = 0
    for (let i = 0; i < value.length; i += 1) {
      hash = (hash << 5) - hash + value.charCodeAt(i)
      hash |= 0
    }
    return acc ^ hash
  }, 0xdeadbeef)
}

function buildMetrics(points: AnalyticsPayload['points']): AnalyticsMetrics {
  const latest = points[points.length - 1]
  const first = points[0]
  const prices = points.map((point) => point.price)
  const totalVolume = points.reduce((acc, point) => acc + point.volume, 0)
  const percentageChange =
    first.price === 0
      ? 0
      : parseFloat((((latest.price - first.price) / first.price) * 100).toFixed(2))
  return {
    latestPrice: latest.price,
    highestPrice: Math.max(...prices),
    lowestPrice: Math.min(...prices),
    totalVolume: parseFloat(totalVolume.toFixed(2)),
    percentageChange,
  }
}

function generatePoints(request: FetchRequest) {
  const { pair, range, intervalMinutes = 5 } = request
  const stepMs = intervalMinutes * 60 * 1000
  const durationMs = range.to.getTime() - range.from.getTime()
  const steps = Math.max(2, Math.ceil(durationMs / stepMs))
  const rng = mulberry32(seedFromRequest(request))
  const baseline = pair.coinId.length * 2 + pair.vsCurrency.length
  let price = 30 + baseline + rng() * 40
  const series: AnalyticsPayload['points'] = []
  let current = range.from.getTime()

  for (let i = 0; i <= steps; i += 1) {
    const drift = Math.sin(current / 100000) * 2
    const noise = rng() * 2 - 1
    price = Math.max(0.01, parseFloat((price + drift + noise).toFixed(2)))
    const volume = parseFloat(((rng() * 80 + 20) * (1 + rng() * 0.5)).toFixed(2))
    series.push({
      timestamp: current,
      price,
      volume,
    })
    current += stepMs
  }
  return series
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function fetchAnalyticsMock(request: FetchRequest): Promise<AnalyticsPayload> {
  await sleep(BASE_LATENCY_MS)
  const rng = mulberry32(seedFromRequest(request))
  if (rng() < 0.16) {
    throw new Error('Mock network error. Try again.')
  }
  const points = generatePoints(request)
  if (!points.length) {
    throw new Error('No simulated data for the selected range.')
  }
  return {
    points,
    metrics: buildMetrics(points),
  }
}

export const defaultPairs = KNOWN_PAIRS

