import { Navigate, Route, Routes } from 'react-router-dom'
import { NavBar } from '@/components/nav-bar'
import BatchQueryPage from '@/pages/BatchQueryPage'
import FlowPage from '@/pages/FlowPage'
import FuzzyMatchPage from '@/pages/FuzzyMatchPage'

export default function App() {
  return (
    <div className="mx-auto flex min-h-svh flex-col">
      <NavBar />
      <main className="mx-auto w-full max-w-screen-2xl flex-1 p-6">
        <Routes>
          <Route path="/" element={<Navigate to="/batch" replace />} />
          <Route path="/fuzzy" element={<FuzzyMatchPage />} />
          <Route path="/batch" element={<BatchQueryPage />} />
          <Route path="/flow" element={<FlowPage />} />
        </Routes>
      </main>
    </div>
  )
}
