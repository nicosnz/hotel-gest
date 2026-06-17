import { useState, useEffect, type FormEvent } from 'react'
import type { Huesped, HabitacionDisponible, MetodoPago } from '../api/types'
import { habitaciones as habitacionesApi } from '../api/habitaciones'
import { huespedes as huespedApi } from '../api/huespedes'
import { reservas as reservasApi } from '../api/reservas'

interface Props {
  onSuccess: () => void
  onCancel: () => void
}

const inputStyle: React.CSSProperties = {
  width: '100%', padding: '8px 10px', borderRadius: 7,
  border: '1px solid var(--border)', fontSize: 13,
  outline: 'none', background: '#fff', color: 'var(--text-primary)',
}

const labelStyle: React.CSSProperties = {
  fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)',
  display: 'block', marginBottom: 4,
}

const sectionTitle: React.CSSProperties = {
  fontSize: 12, fontWeight: 700, textTransform: 'uppercase' as const,
  letterSpacing: '0.05em', color: 'var(--text-secondary)',
  borderBottom: '1px solid var(--border)', paddingBottom: 6, marginBottom: 12,
}

export default function ReservaForm({ onSuccess, onCancel }: Props) {
  // Fechas
  const [checkin, setCheckin]   = useState('')
  const [checkout, setCheckout] = useState('')

  // Habitaciones disponibles
  const [rooms, setRooms]           = useState<HabitacionDisponible[]>([])
  const [loadingRooms, setLoadingRooms] = useState(false)
  const [roomError, setRoomError]   = useState('')
  const [selectedRoom, setSelectedRoom] = useState<HabitacionDisponible | null>(null)

  // Huéspedes (todos)
  const [allHuespedes, setAllHuespedes] = useState<Huesped[]>([])
  const [huespedSearch, setHuespedSearch] = useState('')

  // Titular
  const [titular, setTitular] = useState<Huesped | null>(null)

  // Adicionales
  const [adicionales, setAdicionales] = useState<Huesped[]>([])
  const [addSearch, setAddSearch]     = useState('')

  // Nuevo huésped inline
  const [showNuevo, setShowNuevo] = useState(false)
  const [nuevoNombre, setNuevoNombre]       = useState('')
  const [nuevoApellido, setNuevoApellido]   = useState('')
  const [nuevoDoc, setNuevoDoc]             = useState('')
  const [nuevoCorreo, setNuevoCorreo]       = useState('')
  const [nuevoTel, setNuevoTel]             = useState('')
  const [creandoHuesped, setCreandoHuesped] = useState(false)
  const [nuevoError, setNuevoError]         = useState('')

  // Pago
  const [monto, setMonto]     = useState('')
  const [metodo, setMetodo]   = useState<MetodoPago>('EFECTIVO')

  // Submit
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState('')

  useEffect(() => {
    huespedApi.listar().then(setAllHuespedes).catch(() => {})
  }, [])

  const buscarHabitaciones = async () => {
    if (!checkin || !checkout) return
    setLoadingRooms(true); setRoomError(''); setSelectedRoom(null); setRooms([])
    try {
      const res = await habitacionesApi.disponibilidad(checkin, checkout)
      setRooms(res.habitaciones)
      if (res.habitaciones.length === 0) setRoomError('No hay habitaciones disponibles para ese rango.')
    } catch (e: unknown) {
      setRoomError(e instanceof Error ? e.message : 'Error al buscar habitaciones')
    } finally {
      setLoadingRooms(false)
    }
  }

  const filteredHuespedes = (search: string) =>
    allHuespedes.filter((h) => {
      const q = search.toLowerCase()
      return (
        h.nombre.toLowerCase().includes(q) ||
        h.apellido.toLowerCase().includes(q) ||
        h.documento_identidad.toLowerCase().includes(q)
      )
    }).filter(
      (h) => h.id !== titular?.id && !adicionales.some((a) => a.id === h.id)
    ).slice(0, 5)

  const crearNuevoHuesped = async () => {
    if (!nuevoNombre || !nuevoApellido || !nuevoDoc) {
      setNuevoError('Nombre, apellido y documento son obligatorios.'); return
    }
    setCreandoHuesped(true); setNuevoError('')
    try {
      const h = await huespedApi.crear({
        nombre: nuevoNombre, apellido: nuevoApellido,
        documento_identidad: nuevoDoc,
        correo: nuevoCorreo || undefined, telefono: nuevoTel || undefined,
      })
      setAllHuespedes((prev) => [...prev, h])
      if (!titular) setTitular(h)
      else setAdicionales((prev) => [...prev, h])
      setShowNuevo(false)
      setNuevoNombre(''); setNuevoApellido(''); setNuevoDoc(''); setNuevoCorreo(''); setNuevoTel('')
    } catch (e: unknown) {
      setNuevoError(e instanceof Error ? e.message : 'Error al crear huésped')
    } finally {
      setCreandoHuesped(false)
    }
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!selectedRoom) { setSubmitError('Seleccioná una habitación.'); return }
    if (!titular)      { setSubmitError('Seleccioná un huésped titular.'); return }
    if (!monto)        { setSubmitError('Ingresá el monto de adelanto.'); return }
    setSubmitting(true); setSubmitError('')
    try {
      await reservasApi.crear({
        habitacion_id: selectedRoom.id,
        fecha_checkin_esperado: checkin,
        fecha_checkout_esperado: checkout,
        huesped_titular_id: titular.id,
        huespedes_adicionales: adicionales.map((h) => h.id),
        monto_adelanto: monto,
        metodo_pago: metodo,
      })
      onSuccess()
    } catch (e: unknown) {
      setSubmitError(e instanceof Error ? e.message : 'Error al crear la reserva')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

      {/* Fechas */}
      <section>
        <p style={sectionTitle}>1. Fechas</p>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <div>
            <label style={labelStyle}>Check-in</label>
            <input type="date" style={inputStyle} value={checkin}
              onChange={(e) => { setCheckin(e.target.value); setSelectedRoom(null); setRooms([]) }} />
          </div>
          <div>
            <label style={labelStyle}>Check-out</label>
            <input type="date" style={inputStyle} value={checkout}
              onChange={(e) => { setCheckout(e.target.value); setSelectedRoom(null); setRooms([]) }} />
          </div>
        </div>
        <button type="button" onClick={buscarHabitaciones} disabled={!checkin || !checkout || loadingRooms}
          style={{
            marginTop: 10, padding: '8px 16px', background: 'var(--accent)', color: '#fff',
            border: 'none', borderRadius: 7, cursor: 'pointer', fontSize: 13, fontWeight: 600,
            opacity: (!checkin || !checkout) ? 0.5 : 1,
          }}>
          {loadingRooms ? 'Buscando…' : 'Buscar habitaciones disponibles'}
        </button>
        {roomError && <p style={{ color: 'var(--danger)', fontSize: 12, marginTop: 6 }}>{roomError}</p>}
      </section>

      {/* Habitación */}
      {rooms.length > 0 && (
        <section>
          <p style={sectionTitle}>2. Habitación</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {rooms.map((r) => (
              <label key={r.id} style={{
                display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px',
                border: `2px solid ${selectedRoom?.id === r.id ? 'var(--accent)' : 'var(--border)'}`,
                borderRadius: 8, cursor: 'pointer', fontSize: 13,
                background: selectedRoom?.id === r.id ? 'var(--accent-light)' : '#fff',
              }}>
                <input type="radio" name="room" style={{ accentColor: 'var(--accent)' }}
                  checked={selectedRoom?.id === r.id}
                  onChange={() => setSelectedRoom(r)} />
                <span>
                  <strong>Hab. {r.numero}</strong> — Piso {r.piso} · {r.tipo} · {r.capacidad} pers.
                </span>
                <span style={{ marginLeft: 'auto', fontWeight: 700, color: 'var(--accent)' }}>
                  ${r.precio_por_noche}/noche
                </span>
              </label>
            ))}
          </div>
        </section>
      )}

      {/* Huéspedes */}
      <section>
        <p style={sectionTitle}>3. Huéspedes</p>

        {/* Titular */}
        <label style={labelStyle}>Titular *</label>
        {titular ? (
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '8px 12px', background: 'var(--accent-light)', border: '1px solid var(--accent)',
            borderRadius: 7, fontSize: 13, marginBottom: 8,
          }}>
            <span><strong>{titular.apellido}, {titular.nombre}</strong> · {titular.documento_identidad}</span>
            <button type="button" onClick={() => setTitular(null)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--danger)', fontSize: 16, lineHeight: 1 }}>×</button>
          </div>
        ) : (
          <div style={{ position: 'relative', marginBottom: 8 }}>
            <input placeholder="Buscar por nombre o documento…" style={inputStyle} value={huespedSearch}
              onChange={(e) => setHuespedSearch(e.target.value)} />
            {huespedSearch && filteredHuespedes(huespedSearch).length > 0 && (
              <div style={{
                position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 10,
                background: '#fff', border: '1px solid var(--border)', borderRadius: 7,
                boxShadow: 'var(--shadow-md)', maxHeight: 180, overflowY: 'auto',
              }}>
                {filteredHuespedes(huespedSearch).map((h) => (
                  <button key={h.id} type="button"
                    onClick={() => { setTitular(h); setHuespedSearch('') }}
                    style={{
                      width: '100%', textAlign: 'left', padding: '9px 12px',
                      border: 'none', background: 'none', cursor: 'pointer', fontSize: 13,
                      borderBottom: '1px solid var(--border)',
                    }}>
                    {h.apellido}, {h.nombre} · <span style={{ color: 'var(--text-secondary)' }}>{h.documento_identidad}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Adicionales */}
        <label style={{ ...labelStyle, marginTop: 8 }}>Adicionales</label>
        {adicionales.length > 0 && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 8 }}>
            {adicionales.map((h) => (
              <span key={h.id} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '4px 10px',
                background: '#f1f5f9', borderRadius: 999, fontSize: 12, fontWeight: 500,
              }}>
                {h.apellido}, {h.nombre}
                <button type="button" onClick={() => setAdicionales((prev) => prev.filter((a) => a.id !== h.id))}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', fontSize: 14, lineHeight: 1, padding: 0 }}>×</button>
              </span>
            ))}
          </div>
        )}
        <div style={{ position: 'relative' }}>
          <input placeholder="Agregar huésped adicional…" style={inputStyle} value={addSearch}
            onChange={(e) => setAddSearch(e.target.value)} />
          {addSearch && filteredHuespedes(addSearch).length > 0 && (
            <div style={{
              position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 10,
              background: '#fff', border: '1px solid var(--border)', borderRadius: 7,
              boxShadow: 'var(--shadow-md)', maxHeight: 160, overflowY: 'auto',
            }}>
              {filteredHuespedes(addSearch).map((h) => (
                <button key={h.id} type="button"
                  onClick={() => { setAdicionales((prev) => [...prev, h]); setAddSearch('') }}
                  style={{
                    width: '100%', textAlign: 'left', padding: '9px 12px',
                    border: 'none', background: 'none', cursor: 'pointer', fontSize: 13,
                    borderBottom: '1px solid var(--border)',
                  }}>
                  {h.apellido}, {h.nombre} · <span style={{ color: 'var(--text-secondary)' }}>{h.documento_identidad}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Crear nuevo huésped */}
        <button type="button" onClick={() => setShowNuevo(!showNuevo)}
          style={{
            marginTop: 10, padding: '7px 14px', background: 'none',
            border: '1px dashed var(--border)', borderRadius: 7,
            cursor: 'pointer', fontSize: 12, color: 'var(--accent)', fontWeight: 600,
          }}>
          + Nuevo huésped
        </button>
        {showNuevo && (
          <div style={{
            marginTop: 10, padding: 14, background: '#f8fafc',
            border: '1px solid var(--border)', borderRadius: 8,
          }}>
            <p style={{ ...sectionTitle, marginBottom: 10 }}>Crear nuevo huésped</p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
              <div><label style={labelStyle}>Nombre *</label>
                <input style={inputStyle} value={nuevoNombre} onChange={(e) => setNuevoNombre(e.target.value)} /></div>
              <div><label style={labelStyle}>Apellido *</label>
                <input style={inputStyle} value={nuevoApellido} onChange={(e) => setNuevoApellido(e.target.value)} /></div>
              <div><label style={labelStyle}>Documento *</label>
                <input style={inputStyle} value={nuevoDoc} onChange={(e) => setNuevoDoc(e.target.value)} /></div>
              <div><label style={labelStyle}>Correo</label>
                <input style={inputStyle} type="email" value={nuevoCorreo} onChange={(e) => setNuevoCorreo(e.target.value)} /></div>
              <div style={{ gridColumn: '1 / -1' }}><label style={labelStyle}>Teléfono</label>
                <input style={inputStyle} value={nuevoTel} onChange={(e) => setNuevoTel(e.target.value)} /></div>
            </div>
            {nuevoError && <p style={{ color: 'var(--danger)', fontSize: 12, marginTop: 6 }}>{nuevoError}</p>}
            <button type="button" onClick={crearNuevoHuesped} disabled={creandoHuesped}
              style={{
                marginTop: 10, padding: '7px 14px', background: 'var(--accent)', color: '#fff',
                border: 'none', borderRadius: 7, cursor: 'pointer', fontSize: 13, fontWeight: 600,
              }}>
              {creandoHuesped ? 'Guardando…' : 'Guardar huésped'}
            </button>
          </div>
        )}
      </section>

      {/* Pago */}
      <section>
        <p style={sectionTitle}>4. Pago de adelanto</p>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <div>
            <label style={labelStyle}>Monto adelanto *</label>
            <input type="number" min="0" step="0.01" style={inputStyle} placeholder="0.00"
              value={monto} onChange={(e) => setMonto(e.target.value)} />
          </div>
          <div>
            <label style={labelStyle}>Método de pago *</label>
            <select style={{ ...inputStyle }} value={metodo} onChange={(e) => setMetodo(e.target.value as MetodoPago)}>
              <option value="EFECTIVO">Efectivo</option>
              <option value="TARJETA">Tarjeta</option>
              <option value="TRANSFERENCIA">Transferencia</option>
              <option value="QR">QR</option>
            </select>
          </div>
        </div>
      </section>

      {submitError && (
        <p style={{
          padding: '10px 14px', background: 'var(--danger-bg)', color: 'var(--danger)',
          borderRadius: 7, fontSize: 13, fontWeight: 500,
        }}>{submitError}</p>
      )}

      {/* Footer buttons */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, paddingTop: 4 }}>
        <button type="button" onClick={onCancel}
          style={{
            padding: '9px 20px', background: 'none', border: '1px solid var(--border)',
            borderRadius: 8, cursor: 'pointer', fontSize: 14, fontWeight: 600, color: 'var(--text-secondary)',
          }}>
          Cancelar
        </button>
        <button type="submit" disabled={submitting}
          style={{
            padding: '9px 20px', background: 'var(--accent)', color: '#fff',
            border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 14, fontWeight: 600,
            opacity: submitting ? 0.7 : 1,
          }}>
          {submitting ? 'Creando…' : 'Confirmar reserva'}
        </button>
      </div>
    </form>
  )
}
