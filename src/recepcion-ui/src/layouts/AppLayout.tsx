import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from '../components/Sidebar'

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  '/reservas':    { title: 'Reservas',    subtitle: 'Gestión de reservas y check-in / check-out' },
  '/huespedes':   { title: 'Huéspedes',   subtitle: 'Registro y administración de huéspedes' },
  '/habitaciones':{ title: 'Habitaciones',subtitle: 'Estado y disponibilidad de habitaciones' },
  '/servicios':   { title: 'Servicios',   subtitle: 'Servicios adicionales del hotel' },
}

export default function AppLayout() {
  const location = useLocation()
  const page = pageTitles[location.pathname] ?? { title: '', subtitle: '' }

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100%' }}>
      <Sidebar />

      <main style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        background: 'var(--bg)',
      }}>
        {/* Top bar */}
        <header style={{
          padding: '20px 32px 0',
          flexShrink: 0,
        }}>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: 'var(--text-primary)' }}>
            {page.title}
          </h1>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 2 }}>
            {page.subtitle}
          </p>
        </header>

        {/* Content */}
        <div style={{
          flex: 1,
          overflow: 'auto',
          padding: '20px 32px 32px',
        }}>
          <Outlet />
        </div>
      </main>
    </div>
  )
}
