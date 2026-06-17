import { useState, useEffect } from 'react'
import type { Habitacion } from '../api/types'
import { habitaciones as habitacionesApi } from '../api/habitaciones'
import Table from '../components/Table'
import Badge from '../components/Badge'

const estadoVariant = (estado: string) => {
  const map: Record<string, 'success' | 'danger' | 'warning' | 'info' | 'neutral'> = {
    DISPONIBLE:    'success',
    OCUPADA:       'danger',
    RESERVADA:     'info',
    MANTENIMIENTO: 'warning',
  }
  return map[estado] ?? 'neutral'
}

export default function Habitaciones() {
  const [data, setData]       = useState<Habitacion[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')

  useEffect(() => {
    habitacionesApi.listar()
      .then(setData)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Error al cargar'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Cargando habitaciones…</p>
  if (error)   return (
    <div style={{ padding: '12px 16px', background: 'var(--danger-bg)', color: 'var(--danger)', borderRadius: 8, fontSize: 14 }}>
      {error}
    </div>
  )

  return (
    <Table
      columns={[
        { key: 'numero',          header: 'Nro.' },
        { key: 'piso',            header: 'Piso' },
        { key: 'tipo',            header: 'Tipo' },
        { key: 'capacidad',       header: 'Capacidad', render: (r) => `${r.capacidad} pers.` },
        { key: 'precio_por_noche', header: 'Precio/noche', render: (r) => `$${r.precio_por_noche}` },
        {
          key: 'estado',
          header: 'Estado',
          render: (r) => <Badge label={r.estado} variant={estadoVariant(r.estado)} />,
        },
      ]}
      data={data}
    />
  )
}
