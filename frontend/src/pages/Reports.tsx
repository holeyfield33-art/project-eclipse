const templates = [
  { id: 'sar', name: 'Suspicious Activity Report (SAR)', formats: 'PDF, CSV' },
  { id: 'compliance_summary', name: 'Compliance Summary', formats: 'PDF, CSV' },
  { id: 'executive', name: 'Executive Dashboard', formats: 'PDF' },
]

export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Reports</h1>
        <p className="text-slate-400 mt-1">Pre-built templates and custom exports</p>
      </div>
      <div className="grid gap-4">
        {templates.map((t) => (
          <div
            key={t.id}
            className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 flex items-center justify-between"
          >
            <div>
              <div className="font-medium">{t.name}</div>
              <div className="text-sm text-slate-500">{t.formats}</div>
            </div>
            <button
              className="px-4 py-2 rounded-lg bg-eclipse-600 hover:bg-eclipse-700 text-sm font-medium transition-colors"
              disabled
            >
              Generate
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
