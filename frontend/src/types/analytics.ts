export interface PairSelection {
  coinId: string
  vsCurrency: string
}

export interface DateRange {
  from: Date
  to: Date
}

export interface AnalyticsPoint {
  timestamp: number
  price: number
  volume: number
}

export interface AnalyticsMetrics {
  latestPrice: number
  lowestPrice: number
  highestPrice: number
  totalVolume: number
  percentageChange: number
}

export interface AnalyticsPayload {
  points: AnalyticsPoint[]
  metrics: AnalyticsMetrics
}

