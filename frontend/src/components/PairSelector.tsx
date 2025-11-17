import type { ChangeEvent } from 'react'

import { defaultPairs } from '../mocks/analytics'
import type { PairSelection } from '../types/analytics'

type Props = {
  value: PairSelection
  onChange: (value: PairSelection) => void
}

function PairSelector({ value, onChange }: Props) {
  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const [coinId, vsCurrency] = event.target.value.split('/')
    onChange({ coinId, vsCurrency })
  }

  return (
    <div className="space-y-1">
      <label className="text-sm font-semibold text-slate-600">Pair</label>
      <select
        value={`${value.coinId}/${value.vsCurrency}`}
        onChange={handleChange}
        className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
      >
        {defaultPairs.map((pair) => (
          <option key={`${pair.coinId}/${pair.vsCurrency}`} value={`${pair.coinId}/${pair.vsCurrency}`}>
            {pair.coinId.toUpperCase()} / {pair.vsCurrency.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  )
}

export default PairSelector

