import type { ChangeEvent } from 'react'

import type { DateRange } from '../types/analytics'

type Props = {
  range: DateRange
  onChange: (range: DateRange) => void
}

const formatInputDate = (date: Date) => date.toISOString().split('T')[0]

function DateRangePicker({ range, onChange }: Props) {
  const handleStart = (event: ChangeEvent<HTMLInputElement>) => {
    const next = new Date(event.target.value)
    onChange({ from: next, to: range.to })
  }

  const handleEnd = (event: ChangeEvent<HTMLInputElement>) => {
    const next = new Date(event.target.value)
    onChange({ from: range.from, to: next })
  }

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <label className="text-sm font-semibold text-slate-600">
        From
        <input
          type="date"
          value={formatInputDate(range.from)}
          onChange={handleStart}
          className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
        />
      </label>
      <label className="text-sm font-semibold text-slate-600">
        To
        <input
          type="date"
          value={formatInputDate(range.to)}
          onChange={handleEnd}
          className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
        />
      </label>
    </div>
  )
}

export default DateRangePicker

