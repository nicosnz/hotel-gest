import { useState, useEffect } from 'react'
import type { Servicio } from '../api/types'
import { servicios as serviciosApi } from '../api/servicios'
import Table from '../components/Table'
import Badge from '../components/Badge'

export default function Servicios() {
  const [data, setData]       = useState<Servicio[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')

  useEffect(() => {
    serviciosApi.listar()
      .then(setData)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Error al cargar'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Cargando servicios…</p>
  if (error)   return (
    <div style={{ padding: '12px 16px', background: 'var(--danger-bg)', color: 'var(--danger)', borderRadius: 8, fontSize: 14 }}>
      {error}
    </div>
  )

  return (
    <Table
      columns={[
        { key: 'nombre',      header: 'Nombre' },
        { key: 'descripcion', header: 'Descripción', render: (r) => r.descripcion ?? '—' },
        { key: 'precio',      header: 'Precio',      render: (r) => `$${r.precio}` },
        {
          key: 'activo',
          header: 'Estado',
          render: (r) => (
            <Badge
              label={r.activo ? 'Activo' : 'Inactivo'}
              variant={r.activo ? 'success' : 'neutral'}
            />
          ),
        },
      ]}
      data={data}
    />
  )
}
