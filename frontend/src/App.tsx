import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import EntitySearch from './pages/EntitySearch'
import EntityProfile from './pages/EntityProfile'
import Alerts from './pages/Alerts'
import Cases from './pages/Cases'
import Reports from './pages/Reports'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/entities" element={<EntitySearch />} />
        <Route path="/entities/:id" element={<EntityProfile />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/cases" element={<Cases />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Layout>
  )
}
