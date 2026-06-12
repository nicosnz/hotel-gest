import { useState, useEffect, useCallback } from 'react'
import type { Reserva, EstadoReserva } from '../api/types'
import { reservas as reservasApi } from '../api/reservas'
import Table from '../components/Table'
import Badge from '../components/Badge'
import Modal from '../components/Modal'
import ReservaForm from '../components/ReservaForm'
import ReservaDetalle from '../components/ReservaDetalle'

const estadoVariant = (e: EstadoReserva) => {
  const m: Record<EstadoReserva, 'success' | 'info' | 'warning' | 'danger' | 'neutral'> = {
    CONFIRMADA: 'info', CHECKIN: 'success', FINALIZADA: 'neutral',
    CANCELADA: 'danger', PENDIENTE: 'warning',
  }
  return m[e]
}

export default function Reservas() {
  const [data, setData]         = useState<Reserva[]>([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [showForm, setShowForm] = useState(false)
  const [detalle, setDetalle]   = useState<Reserva | null>(null)

  const cargar = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const res = await reservasApi.listar()
      setData(res)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error al cargar reservas')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return (
    <>
      {/* Header actions */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
        <button
          onClick={() => setShowForm(true)}
          style={{
            display: 'flex', alignItems: 'center', gap: 7,
            padding: '9px 18px', background: 'var(--accent)', color: '#fff',
            border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 14, fontWeight: 600,
            boxShadow: 'var(--shadow)',
          }}
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Nueva reserva
        </button>
      </div>

      {loading && (
        <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Cargando reservas…</p>
      )}

      {error && (
        <div style={{
          padding: '12px 16px', background: 'var(--danger-bg)', color: 'var(--danger)',
          borderRadius: 8, fontSize: 14, marginBottom: 12,
        }}>
          {error}
        </div>
      )}

      {!loading && !error && (
        <Table
          columns={[
            { key: 'habitacion_numero', header: 'Hab.' },
            {
              key: 'titular',
              header: 'Titular',
              render: (r) => {
                const t = r.huespedes.find((h) => h.es_titular)
                return t ? `${t.apellido}, ${t.nombre}` : '—'
              },
            },
            { key: 'fecha_checkin_esperado',  header: 'Check-in' },
            { key: 'fecha_checkout_esperado', header: 'Check-out' },
            {
              key: 'estado',
              header: 'Estado',
              render: (r) => <Badge label={r.estado} variant={estadoVariant(r.estado)} />,
            },
            {
              key: 'huespedes',
              header: 'Huéspedes',
              render: (r) => (
                <span style={{ color: 'var(--text-secondary)', fontSize: 13 }}>
                  {r.huespedes.length}
                </span>
              ),
            },
            {
              key: 'acciones',
              header: '',
              render: (r) => (
                <button
                  onClick={() => setDetalle(r)}
                  style={{
                    padding: '5px 12px', background: 'var(--accent-light)', color: 'var(--accent)',
                    border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 12, fontWeight: 600,
                  }}
                >
                  Ver detalle
                </button>
              ),
            },
          ]}
          data={data.map((r) => ({ ...r, id: r.id }))}
        />
      )}

      {!loading && !error && data.length === 0 && (
        <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 8 }}>
          No hay reservas registradas.
        </p>
      )}

      {/* Modal: nueva reserva */}
      {showForm && (
        <Modal title="Nueva reserva" onClose={() => setShowForm(false)} width={620}>
          <ReservaForm
            onSuccess={() => { setShowForm(false); cargar() }}
            onCancel={() => setShowForm(false)}
          />
        </Modal>
      )}

      {/* Modal: detalle */}
      {detalle && (
        <Modal
          title={`Reserva · Hab. ${detalle.habitacion_numero}`}
          onClose={() => setDetalle(null)}
          width={580}
        >
          <ReservaDetalle reserva={detalle} />
        </Modal>
      )}
    </>
  )
}
