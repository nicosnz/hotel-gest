import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import Reservas from './pages/Reservas'
import Huespedes from './pages/Huespedes'
import Habitaciones from './pages/Habitaciones'
import Servicios from './pages/Servicios'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/reservas" replace />} />
          <Route path="reservas"     element={<Reservas />} />
          <Route path="huespedes"    element={<Huespedes />} />
          <Route path="habitaciones" element={<Habitaciones />} />
          <Route path="servicios"    element={<Servicios />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
