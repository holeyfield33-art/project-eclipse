import { useState } from 'react'
import { Search } from 'lucide-react'

export default function EntitySearch() {
  const [query, setQuery] = useState('')

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Entity Search</h1>
        <p className="text-slate-400 mt-1">
          Search by name, account number, wallet address, or company
        </p>
      </div>

      <div className="relative max-w-xl">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter name, account, wallet, or company…"
          className="w-full pl-11 pr-4 py-3 rounded-lg bg-slate-900 border border-slate-700
                     focus:border-eclipse-500 focus:ring-1 focus:ring-eclipse-500 outline-none
                     text-slate-100 placeholder:text-slate-500"
        />
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-center text-slate-500">
        Results will appear here once the backend search endpoint is connected.
      </div>
    </div>
  )
}
