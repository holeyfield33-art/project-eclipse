import { Link, useLocation } from 'react-router-dom'
import { Shield, Search, Bell, FolderOpen, FileText, Activity } from 'lucide-react'
import clsx from 'clsx'

const nav = [
  { to: '/', label: 'Overview', icon: Activity },
  { to: '/alerts', label: 'Alerts', icon: Bell },
  { to: '/entities', label: 'Entities', icon: Search },
  { to: '/cases', label: 'Cases', icon: FolderOpen },
  { to: '/reports', label: 'Reports', icon: FileText },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()

  return (
    <div className="min-h-screen flex bg-slate-950">
      <aside className="w-64 border-r border-slate-800 bg-slate-900/50 flex flex-col">
        <div className="p-5 flex items-center gap-3 border-b border-slate-800">
          <Shield className="w-8 h-8 text-eclipse-500" />
          <div>
            <div className="font-semibold text-lg tracking-tight">Eclipse</div>
            <div className="text-xs text-slate-400">Threat Intelligence</div>
          </div>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {nav.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                location.pathname === to || (to !== '/' && location.pathname.startsWith(to))
                  ? 'bg-eclipse-600/20 text-eclipse-500'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              )}
            >
              <Icon className="w-5 h-5" />
              {label}
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
          v2.0 · See threats before they surface
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  )
}
