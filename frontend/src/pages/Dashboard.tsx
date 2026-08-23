import { Activity, AlertTriangle, ShieldAlert, TrendingUp } from 'lucide-react'

const stats = [
  { label: 'High Risk', value: '—', icon: ShieldAlert, color: 'text-risk-high' },
  { label: 'Medium Risk', value: '—', icon: AlertTriangle, color: 'text-risk-medium' },
  { label: 'Low Risk', value: '—', icon: Activity, color: 'text-risk-low' },
  { label: 'New (24h)', value: '—', icon: TrendingUp, color: 'text-eclipse-500' },
]

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Threat Overview</h1>
        <p className="text-slate-400 mt-1">Real-time risk posture across monitored entities</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div
            key={label}
            className="rounded-xl border border-slate-800 bg-slate-900/60 p-5"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">{label}</span>
              <Icon className={`w-5 h-5 ${color}`} />
            </div>
            <div className="mt-3 text-3xl font-semibold">{value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-medium mb-4">Live Alert Feed</h2>
          <p className="text-sm text-slate-500">
            Connect the API to see chronological alerts with risk scores.
          </p>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-medium mb-4">Geographic Heatmap</h2>
          <p className="text-sm text-slate-500">
            High-risk jurisdiction activity will appear here.
          </p>
        </div>
      </div>
    </div>
  )
}
