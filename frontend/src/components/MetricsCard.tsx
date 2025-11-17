import clsx from 'clsx'

type Props = {
  label: string
  value: string
  helper?: string
  trend?: number
}

function MetricsCard({ label, value, helper, trend }: Props) {
  const trendColor = trend === undefined ? 'text-slate-500' : trend >= 0 ? 'text-emerald-600' : 'text-rose-600'
  const trendLabel =
    trend === undefined ? null : (
      <span className={clsx('text-xs font-semibold', trendColor)}>
        {trend >= 0 ? '+' : ''}
        {trend.toFixed(2)}%
      </span>
    )

  return (
    <article className="flex flex-col gap-1 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between text-xs font-medium uppercase tracking-wide text-slate-500">
        <span>{label}</span>
        {trendLabel}
      </div>
      <p className="text-2xl font-semibold text-slate-900">{value}</p>
      {helper ? <p className="text-sm text-slate-500">{helper}</p> : null}
    </article>
  )
}

export default MetricsCard

