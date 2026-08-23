import { useParams } from 'react-router-dom'

export default function EntityProfile() {
  const { id } = useParams()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Entity Profile</h1>
        <p className="text-slate-400 mt-1">ID: {id}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-medium mb-4">Summary</h2>
          <p className="text-sm text-slate-500">
            Risk score, linked entities, and key attributes will load from the API.
          </p>
        </div>
        <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-medium mb-4">Network Graph</h2>
          <p className="text-sm text-slate-500">
            Interactive Neo4j-powered graph of connected entities (scaffold).
          </p>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
        <h2 className="font-medium mb-4">Transaction History</h2>
        <p className="text-sm text-slate-500">Timeline with filters will appear here.</p>
      </div>
    </div>
  )
}
