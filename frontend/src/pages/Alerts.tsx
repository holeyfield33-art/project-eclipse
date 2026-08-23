export default function Alerts() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Alerts</h1>
        <p className="text-slate-400 mt-1">Live feed of risk-scored alerts</p>
      </div>
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-center text-slate-500">
        Connect <code className="text-eclipse-500">/api/v1/alerts</code> to populate the feed.
      </div>
    </div>
  )
}
