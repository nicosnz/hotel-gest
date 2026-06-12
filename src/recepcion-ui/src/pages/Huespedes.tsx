import { useState, useEffect } from 'react'
import type { Huesped } from '../api/types'
import { huespedes as huespedesApi } from '../api/huespedes'
import Table from '../components/Table'

export default function Huespedes() {
  const [data, setData]       = useState<Huesped[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')

  useEffect(() => {
    huespedesApi.listar()
      .then(setData)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Error al cargar'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Cargando huéspedes…</p>
  if (error)   return (
    <div style={{ padding: '12px 16px', background: 'var(--danger-bg)', color: 'var(--danger)', borderRadius: 8, fontSize: 14 }}>
      {error}
    </div>
  )

  return (
    <Table
      columns={[
        { key: 'nombre',             header: 'Nombre' },
        { key: 'apellido',           header: 'Apellido' },
        { key: 'documento_identidad', header: 'Documento' },
        { key: 'correo',             header: 'Correo',   render: (r) => r.correo   ?? '—' },
        { key: 'telefono',           header: 'Teléfono', render: (r) => r.telefono ?? '—' },
      ]}
      data={data}
    />
  )
}
