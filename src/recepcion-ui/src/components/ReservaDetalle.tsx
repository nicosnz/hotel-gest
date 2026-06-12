import type { Reserva } from '../api/types'
import Badge from './Badge'

const estadoVariant = (e: string) => {
  const m: Record<string, 'success' | 'info' | 'warning' | 'danger' | 'neutral'> = {
    CONFIRMADA: 'info', CHECKIN: 'success', FINALIZADA: 'neutral', CANCELADA: 'danger', PENDIENTE: 'warning',
  }
  return m[e] ?? 'neutral'
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', gap: 8, padding: '7px 0', borderBottom: '1px solid var(--border)' }}>
      <span style={{ width: 180, flexShrink: 0, fontSize: 13, color: 'var(--text-secondary)', fontWeight: 500 }}>{label}</span>
      <span style={{ fontSize: 13, color: 'var(--text-primary)' }}>{value}</span>
    </div>
  )
}

interface Props { reserva: Reserva }

export default function ReservaDetalle({ reserva }: Props) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

      {/* General */}
      <section>
        <h3 style={{ fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: 8 }}>Información general</h3>
        <Row label="ID reserva"       value={<code style={{ fontSize: 12 }}>{reserva.id}</code>} />
        <Row label="Habitación"       value={`Nro. ${reserva.habitacion_numero}`} />
        <Row label="Estado"           value={<Badge label={reserva.estado} variant={estadoVariant(reserva.estado)} />} />
        <Row label="Check-in esperado"  value={reserva.fecha_checkin_esperado} />
        <Row label="Check-out esperado" value={reserva.fecha_checkout_esperado} />
        <Row label="Check-in real"    value={reserva.fecha_checkin_real ?? '—'} />
        <Row label="Check-out real"   value={reserva.fecha_checkout_real ?? '—'} />
        <Row label="Observaciones"    value={reserva.observaciones ?? '—'} />
      </section>

      {/* Huéspedes */}
      <section>
        <h3 style={{ fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: 8 }}>
          Huéspedes ({reserva.huespedes.length})
        </h3>
        {reserva.huespedes.length === 0 ? (
          <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Sin huéspedes registrados.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {reserva.huespedes.map((h) => (
              <div key={h.id} style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '10px 12px', background: 'var(--bg)', borderRadius: 8, fontSize: 13,
              }}>
                <div>
                  <span style={{ fontWeight: 600 }}>{h.apellido}, {h.nombre}</span>
                  <span style={{ color: 'var(--text-secondary)', marginLeft: 8 }}>{h.documento_identidad}</span>
                </div>
                {h.es_titular && <Badge label="Titular" variant="info" />}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Consumos */}
      <section>
        <h3 style={{ fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: 8 }}>
          Consumos ({reserva.consumos.length})
        </h3>
        {reserva.consumos.length === 0 ? (
          <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Sin consumos registrados.</p>
        ) : (
          <>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                  {['Servicio','Cant.','P. Unit.','Subtotal','Fecha'].map(h => (
                    <th key={h} style={{ textAlign: 'left', padding: '6px 8px', color: 'var(--text-secondary)', fontWeight: 600, fontSize: 12 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {reserva.consumos.map((c, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '8px 8px' }}>{c.servicio_nombre}</td>
                    <td style={{ padding: '8px 8px' }}>{c.cantidad}</td>
                    <td style={{ padding: '8px 8px' }}>${c.precio_unitario}</td>
                    <td style={{ padding: '8px 8px', fontWeight: 600 }}>${c.subtotal}</td>
                    <td style={{ padding: '8px 8px', color: 'var(--text-secondary)' }}>{c.fecha_consumo.slice(0, 10)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ textAlign: 'right', marginTop: 8, fontWeight: 700, fontSize: 14 }}>
              Total: ${reserva.consumos.reduce((s, c) => s + parseFloat(c.subtotal), 0).toFixed(2)}
            </div>
          </>
        )}
      </section>
    </div>
  )
}
