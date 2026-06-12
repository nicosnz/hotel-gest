import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import AppLayout from './layouts/AppLayout'
import Login from './pages/Login'
import Reservas from './pages/Reservas'
import Huespedes from './pages/Huespedes'
import Habitaciones from './pages/Habitaciones'
import Servicios from './pages/Servicios'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }>
            <Route index element={<Navigate to="/reservas" replace />} />
            <Route path="reservas"      element={<Reservas />} />
            <Route path="huespedes"     element={<Huespedes />} />
            <Route path="habitaciones"  element={<Habitaciones />} />
            <Route path="servicios"     element={<Servicios />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
