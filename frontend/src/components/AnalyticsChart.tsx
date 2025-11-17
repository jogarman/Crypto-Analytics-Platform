import { useMemo, type RefObject } from 'react'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

import type { AnalyticsPoint } from '../types/analytics'

type Props = {
  points: AnalyticsPoint[]
  loading?: boolean
  chartRef?: RefObject<HighchartsReact.RefObject | null>
}

function AnalyticsChart({ points, loading, chartRef }: Props) {
  const options = useMemo(() => {
    const priceSeries = points.map((point) => [point.timestamp, point.price] as const)
    const volumeSeries = points.map((point) => [point.timestamp, point.volume] as const)

    return {
      chart: {
        height: 360,
        backgroundColor: 'transparent',
        zoomType: 'x',
      },
      title: { text: '' },
      xAxis: {
        type: 'datetime',
        gridLineColor: '#e2e8f0',
        labels: { style: { color: '#475569' } },
        tickWidth: 0,
      },
      yAxis: [
        {
          title: { text: 'Price', style: { color: '#1d4ed8' } },
          labels: { style: { color: '#1d4ed8' } },
          opposite: false,
        },
        {
          title: { text: 'Volume', style: { color: '#0ea5e9' } },
          labels: { style: { color: '#0ea5e9' } },
          opposite: true,
        },
      ],
      tooltip: {
        shared: true,
        borderRadius: 12,
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        style: { color: '#f8fafc' },
        valueDecimals: 2,
      },
      series: [
        {
          type: 'line',
          name: 'Price',
          data: priceSeries,
          color: '#1d4ed8',
          marker: { enabled: false },
          tooltip: { valueDecimals: 2 },
        },
        {
          type: 'column',
          name: 'Volume',
          data: volumeSeries,
          color: '#0ea5e9',
          yAxis: 1,
          pointPadding: 0.2,
          borderWidth: 0,
        },
      ],
      credits: { enabled: false },
    }
  }, [points])

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
      {loading ? (
        <div className="flex h-80 items-center justify-center text-sm text-slate-500">
          Loading chart...
        </div>
      ) : (
        <HighchartsReact highcharts={Highcharts} options={options} ref={chartRef} />
      )}
    </div>
  )
}

export default AnalyticsChart

